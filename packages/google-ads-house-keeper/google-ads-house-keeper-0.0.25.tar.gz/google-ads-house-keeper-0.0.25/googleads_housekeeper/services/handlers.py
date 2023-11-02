# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Dict, Callable, List, Optional, Sequence, Tuple
from dataclasses import asdict
from datetime import datetime, timedelta
import logging
import json
import sqlalchemy

from gaarf.api_clients import GoogleAdsApiClient
from gaarf.report import GaarfReport
from gaarf.query_executor import AdsReportFetcher

from googleads_housekeeper.domain import allowlisting, commands, events, execution, settings, task
from googleads_housekeeper.domain.placements import Placements, PlacementsConversionSplit, aggregate_placements
from googleads_housekeeper.adapters import notifications, publisher

from . import unit_of_work
from .exclusion_service import PlacementExcluder
from .rules_parser import RulesParser
from .enums import ExclusionTypeEnum, ExclusionLevelEnum
from .exclusion_specification import BaseExclusionSpecification


def get_accessible_mcc_ids(cmd: commands.GetMccIds,
                           uow: unit_of_work.AbstractUnitOfWork,
                           ads_api_client: GoogleAdsApiClient) -> List[str]:
    api_client = ads_api_client.client
    customer_service = api_client.get_service("CustomerService")
    accessible_customers = customer_service.list_accessible_customers()
    mcc_ids = [
        resource.split('/')[1]
        for resource in accessible_customers.resource_names
    ]
    mcc_full = []
    for mcc in mcc_ids:
        report_fetcher = AdsReportFetcher(api_client=ads_api_client,
                                          customer_ids=mcc)
        try:
            mcc_data = report_fetcher.fetch("""
            SELECT
                customer_client.descriptive_name AS account_name,
                customer_client.id AS account_id
            FROM customer_client
            WHERE customer_client.manager = TRUE
            AND customer_client.status = "ENABLED"
            """)
            if mcc_data:
                mcc_full.append(mcc_data)
        except Exception:
            pass
    with uow:
        for mcc in mcc_full:
            for row in mcc:
                uow.mcc_ids.add(
                    settings.MccIds(mcc_id=row.account_id,
                                    account_name=row.account_name))
        try:
            uow.commit()
        except sqlalchemy.exc.IntegrityError:
            pass
    return mcc_ids


def get_customer_ids(
        cmd: commands.GetMccIds, uow: unit_of_work.AbstractUnitOfWork,
        ads_api_client: GoogleAdsApiClient) -> List[Dict[str, int]]:
    report_fetcher = AdsReportFetcher(api_client=ads_api_client,
                                      customer_ids=cmd.mcc_id)
    customer_ids = report_fetcher.fetch("""
    SELECT
        customer_client.descriptive_name AS account_name,
        customer_client.id AS customer_id
    FROM customer_client
    WHERE customer_client.manager = FALSE
    AND customer_client.status = "ENABLED"
    """)
    result = []
    with uow:
        for account_name, customer_id in customer_ids:
            result.append({"account_name": account_name, "id": customer_id})
            uow.customer_ids.add(
                settings.CustomerIds(mcc_id=cmd.mcc_id,
                                     account_name=account_name,
                                     id=customer_id))
        try:
            uow.commit()
        except sqlalchemy.exc.IntegrityError:
            pass
    return result


def run_manual_exclusion_task(cmd: commands.RunManualExclusion,
                              uow: unit_of_work.AbstractUnitOfWork,
                              ads_api_client: GoogleAdsApiClient):
    with uow:
        placement_excluder = PlacementExcluder(ads_api_client, uow)
        to_be_excluded_placements = [
            placement_info + [cmd.customer_ids]
            for placement_info in cmd.placements
        ]
        to_be_excluded_placements = GaarfReport(
            results=to_be_excluded_placements,
            column_names=[
                "ad_group_id", "placement_type", "placement", "criterion_id",
                "campaign_type", "customer_id"
            ])
        placement_excluder.exclude_placements(to_be_excluded_placements)


def task_created(
    event: events.TaskCreated,
    publisher: publisher.BasePublisher
) -> None:
    publisher.publish("task_created", event)


def task_updated(
    event: events.TaskUpdated,
    publisher: publisher.BasePublisher
) -> None:
    publisher.publish("task_updated", event)


def task_deleted(
    event: events.TaskDeleted,
    publisher: publisher.BasePublisher
) -> None:
    publisher.publish("task_deleted", event)

def run_task(
        cmd: commands.RunTask,
        uow: unit_of_work.AbstractUnitOfWork,
        ads_api_client: GoogleAdsApiClient,
        notification_service: Optional[notifications.BaseNotifications] = None,
        save_to_db: bool = True):
    with uow:
        task_obj = uow.tasks.get(task_id=cmd.id)
        start_date, end_date = get_start_end_date(task_obj.from_days_ago,
                                                  task_obj.date_range)
        report_fetcher = AdsReportFetcher(api_client=ads_api_client,
                                          customer_ids=task_obj.customer_ids)
        exclusion_specification = RulesParser().generate_specifications(
            task_obj.exclusion_rule)
        placement_excluder = PlacementExcluder(ads_api_client, uow)
        placement_types = tuple(task_obj.placement_types.split(','))
        start_time = datetime.now()
        to_be_excluded_placements = find_placements_for_exclusion(
            start_date, end_date, placement_types, task_obj.exclusion_level,
            ads_api_client, report_fetcher, placement_excluder,
            exclusion_specification, uow, save_to_db)
        if notification_service and task_obj.output in (
                task.TaskOutput.NOTIFY, task.TaskOutput.EXCLUDE_AND_NOTIFY):
            message_body = to_be_excluded_placements[[
                "placement_type", "name"
            ]].to_pandas()
            notification_service.send(message_body=message_body,
                                      title=task_obj.name,
                                      custom_sender=task_obj.name)

        if to_be_excluded_placements and task_obj.output in (
                task.TaskOutput.EXCLUDE, task.TaskOutput.EXCLUDE_AND_NOTIFY):
            placement_excluder.exclude_placements(to_be_excluded_placements,
                                                  task_obj.exclusion_level)

            end_time = datetime.now()
            execution_obj = execution.Execution(task=cmd.id,
                                    start_time=start_time,
                                    end_time=end_time)
            uow.executions.add(execution_obj)
            if save_to_db:
                for placement in to_be_excluded_placements:
                    if hasattr(placement, "reason"):
                        exclusion_reason = placement.reason
                    else:
                        exclusion_reason = ""
                    uow.execution_details.add(
                        execution.ExecutionDetails(
                            execution_id=execution_obj.id,
                            placement=placement.name,
                            placement_type=placement.placement_type,
                            reason=exclusion_reason))
            uow.commit()


def preview_placements(cmd: commands.PreviewPlacements,
                       uow: unit_of_work.AbstractUnitOfWork,
                       ads_api_client: GoogleAdsApiClient,
                       save_to_db: bool = True) -> Dict[str, Any]:
    report_fetcher = AdsReportFetcher(api_client=ads_api_client,
                                      customer_ids=cmd.customer_ids)
    placement_excluder = PlacementExcluder(ads_api_client, uow)
    exclusion_specification = RulesParser().generate_specifications(
        cmd.exclusion_rule)
    start_date, end_date = get_start_end_date(cmd.from_days_ago,
                                              cmd.lookback_days)
    to_be_excluded_placements = find_placements_for_exclusion(
        start_date, end_date, cmd.placement_types, cmd.exclusion_level,
        ads_api_client, report_fetcher, placement_excluder,
        exclusion_specification, uow, save_to_db)
    if not to_be_excluded_placements:
        data = {}
    else:
        data = json.loads(
            to_be_excluded_placements.to_pandas().to_json(orient="index"))
    return {
        "data": data,
        "dates": {
            "date_from": start_date,
            "date_to": end_date
        }
    }


def find_placements_for_exclusion(start_date: str,
                                  end_date: str,
                                  placement_types: Tuple[str, ...],
                                  exclusion_level: str,
                                  ads_api_client: GoogleAdsApiClient,
                                  report_fetcher: AdsReportFetcher,
                                  placement_excluder: PlacementExcluder,
                                  exclusion_specification: Optional[Sequence[
                                      Sequence[BaseExclusionSpecification]]],
                                  uow: unit_of_work.AbstractUnitOfWork,
                                  save_to_db: bool = True) -> GaarfReport:
    is_regular_query = False
    is_conversion_query = False
    conversion_rules = []
    if exclusion_specification:
        for specification in exclusion_specification:
            for rule in specification:
                if rule.name == "conversion_name":
                    is_conversion_query = True
                    conversion_name = rule.value
                    conversion_rules.append(rule)
                else:
                    is_regular_query = True
    placements = report_fetcher.fetch(
        Placements(placement_types=placement_types,
                   start_date=start_date,
                   end_date=end_date))
    if not placements:
        return None
    if is_conversion_query:
        conversion_placements = report_fetcher.fetch(
            PlacementsConversionSplit(placement_types=placement_types,
                                      start_date=start_date,
                                      end_date=end_date))
        placements = join_conversion_split(placement_excluder, placements,
                                           conversion_placements,
                                           conversion_rules, conversion_name)
    placements = aggregate_placements(placements, exclusion_level)
    if not exclusion_specification:
        return placements
    for rule in exclusion_specification:
        # Identify all ads and non_ads specifications
        ads_specs = [
            r for r in rule
            if r.exclusion_type == ExclusionTypeEnum.GOOGLE_ADS_INFO
        ]
        non_ads_specs = [
            r for r in rule
            if r.exclusion_type != ExclusionTypeEnum.GOOGLE_ADS_INFO
        ]

        # If we don't have any non_ads specification proceed to applying them
        if ads_specs and not non_ads_specs:
            continue
        # If we have a mix of ads and non_ads specifications apply ads first
        # and then parse non-ads ones
        elif ads_specs and non_ads_specs:
            to_be_parsed_placements = (
                placement_excluder.prepare_placements_for_exclusion(
                    [ads_specs], placements))
            parse_via_external_parsers(to_be_parsed_placements, non_ads_specs,
                                       uow, save_to_db)
        # If there are only non_ads specification proceed to applying them
        elif not ads_specs and non_ads_specs:
            parse_via_external_parsers(placements, non_ads_specs, uow,
                                       save_to_db)

    return placement_excluder.prepare_placements_for_exclusion(
        exclusion_specification, placements)


def join_conversion_split(
        placement_excluder: PlacementExcluder, placements: GaarfReport,
        conversion_placements: GaarfReport,
        conversion_rules: Sequence[BaseExclusionSpecification],
        conversion_name: str) -> GaarfReport:
    conversion_placements = (
        placement_excluder.prepare_placements_for_exclusion(
            [conversion_rules], conversion_placements)).to_pandas()
    final_report_values = []
    for row in placements:
        conversion_row = conversion_placements.loc[
            (conversion_placements.ad_group_id == row.ad_group_id)
            & (conversion_placements.placement == row.placement)]
        data = list(row.data)
        if not (conversions := sum(conversion_row["conversions"].values)):
            conversions = 0.0
        if not (all_conversions := sum(
                conversion_row["all_conversions"].values)):
            all_conversions = 0.0
        data.extend([conversion_name, conversions, all_conversions])
        final_report_values.append(data)
    columns = list(placements.column_names)
    columns.extend(["conversion_name", "conversions_", "all_conversions_"])
    return GaarfReport(results=final_report_values, column_names=columns)


def parse_via_external_parsers(
        to_be_parsed_placements: GaarfReport,
        non_ads_specs: Sequence[BaseExclusionSpecification],
        uow: unit_of_work.AbstractUnitOfWork,
        save_to_db: bool = True) -> None:
    with uow:
        for non_ads_spec_rule in non_ads_specs:
            for placement_info in to_be_parsed_placements:
                repo = getattr(uow, non_ads_spec_rule.repository_name)
                if (placement_info.placement_type ==
                        non_ads_spec_rule.corresponding_placement_type.name):

                    if not repo.get_by_name(placement_info.name):
                        parsed_placement_info = non_ads_spec_rule.parser(
                        ).parse(placement_info.placement)
                        if save_to_db:
                            repo.add(parsed_placement_info)
        uow.commit()


def save_task(
    cmd: commands.SaveTask,
    uow: unit_of_work.AbstractUnitOfWork,
) -> str:
    with uow:
        task_id = None
        task_obj = None
        if hasattr(cmd, "task_id") and cmd.task_id:
            task_id = cmd.task_id
            task_obj = uow.tasks.get(task_id=task_id)
            update_dict = asdict(cmd)
            update_dict.pop("task_id")
            uow.tasks.update(task_obj.id, update_dict)
            uow.published_events.append(events.TaskUpdated(task_obj.id))
        else:
            task_dict = asdict(cmd)
            task_dict.pop("task_id")
            task_obj = task.Task(**task_dict)
            uow.tasks.add(task_obj)
            task_id = task_obj.id
            uow.published_events.append(events.TaskCreated(task_id))
        uow.commit()
        task_id = task_obj.id
        return str(task_id)


def delete_task(
    cmd: commands.DeleteTask,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        task_obj = uow.tasks.get(task_id=cmd.task_id)
        if task_obj:
            uow.tasks.update(cmd.task_id, {"status": "INACTIVE"})
            uow.commit()
            uow.published_events.append(events.TaskDeleted(cmd.task_id))
        else:
            logging.warning("No task with id %d found!", cmd.id)


def save_config(
    cmd: commands.SaveConfig,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        task_id = None
        task_obj = None
        if hasattr(cmd, "id") and cmd.id:
            config_id = cmd.id
            config = uow.settings.get(config_id)
            update_dict = asdict(cmd)
            update_dict.pop("id")
            uow.settings.update(config.id, update_dict)
        else:
            config_dict = asdict(cmd)
            config_dict.pop("id")
            config = settings.Config(**config_dict)
            uow.settings.add(config)
        uow.commit()

def add_to_allowlisting(cmd: commands.AddToAllowlisting,
                        uow: unit_of_work.AbstractUnitOfWork) -> None:
    with uow:
        placement = allowlisting.AllowlistedPlacement(
            cmd.placement.get("type"), cmd.placement.get("name"))
        if not uow.allowlisting.get_by_name(placement.name):
            uow.allowlisting.add(placement)
            uow.commit()


def remove_from_allowlisting(cmd: commands.RemoveFromAllowlisting,
                             uow: unit_of_work.AbstractUnitOfWork) -> None:
    with uow:
        if allowlisted_placement := uow.allowlisting.get_by_name(cmd.placement.get("name")):
            uow.allowlisting.delete(allowlisted_placement.id)


EVENT_HANDLERS = {
    events.TaskCreated: [task_created],
    events.TaskUpdated: [task_updated],
    events.TaskDeleted: [task_deleted]
}

COMMAND_HANDLERS = {
    commands.RunTask: run_task,
    commands.SaveTask: save_task,
    commands.DeleteTask: delete_task,
    commands.RunManualExclusion: run_manual_exclusion_task,
    commands.PreviewPlacements: preview_placements,
    commands.SaveConfig: save_config,
    commands.GetCustomerIds: get_customer_ids,
    commands.GetMccIds: get_accessible_mcc_ids,
    commands.AddToAllowlisting: add_to_allowlisting,
    commands.RemoveFromAllowlisting: remove_from_allowlisting,
}


def get_start_end_date(from_days_ago: int,
                       lookback_days: int) -> Tuple[str, str]:
    start_date = (datetime.now() - timedelta(days=int(lookback_days))).date()
    end_date = (datetime.now() - timedelta(days=int(from_days_ago))).date()
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
