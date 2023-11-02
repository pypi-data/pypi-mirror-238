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

from typing import Any, Dict, Iterable, Optional, Sequence, Tuple

from copy import deepcopy
import logging
from gaarf.api_clients import GoogleAdsApiClient
from gaarf.report import GaarfRow, GaarfReport
from google.api_core import exceptions
import itertools
from tenacity import Retrying, RetryError, retry_if_exception_type, stop_after_attempt, wait_exponential

from .exclusion_specification import Specification, BaseExclusionSpecification
from .enums import PlacementTypeEnum, ExclusionLevelEnum


class PlacementExcluder:
    """Class for excluding placements based on a sequence of exclusion specifications."""

    def __init__(self, client: GoogleAdsApiClient, db=None):
        self.client = client.client
        self.db = db

    def prepare_placements_for_exclusion(self, specifications: Sequence[
        Sequence[BaseExclusionSpecification]],
                             placements: GaarfReport) -> GaarfReport:
        """Get placements that satisfy exclusion specifications."""
        spec = Specification(self.db)
        to_be_excluded_placements = []
        for placement in placements:
            if reason := spec.satisfies(specifications, placement):
                reason_str = ",".join(list(itertools.chain(*reason)))
            else:
                reason_str = ""
            to_be_excluded_placements.append(placement.data + [reason_str])
        return GaarfReport(results=to_be_excluded_placements,
                           column_names=placements.column_names + ["reason"])
    def exclude_placements(
        self,
        to_be_excluded_placements: GaarfReport,
        exclusion_level: ExclusionLevelEnum = ExclusionLevelEnum.AD_GROUP
    ) -> Optional[GaarfReport]:
        """Excludes placements and optionally returns placements which cannot be excluded."""
        self._init_criterion_service_and_operation(exclusion_level)
        exclusion_operations, non_excluded_placements = (
            self.
            _create_placement_exclusion_operations_and_non_excluded_placements(
                to_be_excluded_placements, exclusion_level))
        if non_excluded_placements:
            for placement_info in non_excluded_placements:
                logging.warning(
                    "Placement '%s' cannot be excluded from VIDEO campaign '%s'",
                    placement_info.placement, placement_info.campaign_name)
        if exclusion_operations:
            excluded_placements_count = 0
            for customer_id, operations in exclusion_operations.items():
                try:
                    if operations:
                        self._exclude(customer_id, operations)
                        logging.info("Excluded %d placements from account %s",
                                     len(operations), customer_id)
                        excluded_placements_count += len(operations)
                except Exception as e:
                    logging.error(e)
            logging.info("%d placements was excluded",
                         excluded_placements_count)
        return non_excluded_placements

    def _init_criterion_service_and_operation(
            self, exclusion_level: ExclusionLevelEnum) -> None:
        if exclusion_level == ExclusionLevelEnum.CAMPAIGN:
            self.criterion_service = self.client.get_service(
                "CampaignCriterionService")
            self.criterion_operation = self.client.get_type(
                "CampaignCriterionOperation")
            self.criterion_path_method = self.criterion_service.campaign_criterion_path
            self.mutate_operation = self.criterion_service.mutate_campaign_criteria
            self.entity_name = "campaign_id"
        if exclusion_level == ExclusionLevelEnum.AD_GROUP:
            self.criterion_service = self.client.get_service(
                "AdGroupCriterionService")
            self.criterion_operation = self.client.get_type(
                "AdGroupCriterionOperation")
            self.criterion_path_method = self.criterion_service.ad_group_criterion_path
            self.mutate_operation = self.criterion_service.mutate_ad_group_criteria
            self.entity_name = "ad_group_id"
        if exclusion_level == ExclusionLevelEnum.ACCOUNT:
            self.criterion_service = self.client.get_service(
                "CustomerNegativeCriterionService")
            self.criterion_operation = self.client.get_type(
                "CustomerNegativeCriterionOperation")
            self.criterion_path_method = self.criterion_service.customer_negative_criterion_path
            self.mutate_operation = self.criterion_service.mutate_customer_negative_criteria
            self.entity_name = "customer_id"

    def _create_placement_exclusion_operations_and_non_excluded_placements(
        self, placements: GaarfReport, exclusion_level: ExclusionLevelEnum
    ) -> Tuple[Dict[str, Any], GaarfReport]:
        """Generates exclusion operations on customer_id level and get all placements that cannot be excluded."""
        operations_mapping: Dict[str, Any] = {}
        non_excluded_placements = []
        for placement_info in placements:
            customer_id, operation = self._create_placement_operation(
                placement_info, exclusion_level)
            if not operation:
                non_excluded_placements.append(placement_info.data)
                continue
            if isinstance(operations_mapping.get(customer_id), list):
                operations_mapping[customer_id].append(operation)
            else:
                operations_mapping[customer_id] = [operation]
        non_excluded_placements = GaarfReport(
            results=non_excluded_placements,
            column_names=placement_info.column_names)
        return operations_mapping, non_excluded_placements

    def _create_placement_operation(
            self, placement_info: GaarfRow,
            exclusion_level: ExclusionLevelEnum) -> Tuple[str, Any]:
        "Creates exclusion operation for a single placement." ""
        if placement_info.campaign_type == "VIDEO" and exclusion_level in (
                ExclusionLevelEnum.CAMPAIGN, ExclusionLevelEnum.AD_GROUP):
            return placement_info.customer_id, None
        if (placement_info.placement_type ==
                PlacementTypeEnum.MOBILE_APPLICATION.name):
            app_id = self._format_app_id(placement_info.placement)
        entity_criterion = self.criterion_operation.create
        if exclusion_level == ExclusionLevelEnum.ACCOUNT:
            entity_criterion.resource_name = (self.criterion_path_method(
                placement_info.customer_id, placement_info.criterion_id))
        else:
            entity_criterion.negative = True
            entity_criterion.resource_name = (self.criterion_path_method(
                placement_info.customer_id,
                placement_info.get(self.entity_name),
                placement_info.criterion_id))
        if (placement_info.placement_type == PlacementTypeEnum.WEBSITE.name):
            entity_criterion.placement.url = placement_info.placement
        if (placement_info.placement_type ==
                PlacementTypeEnum.MOBILE_APPLICATION.name):
            entity_criterion.mobile_application.app_id = app_id
        if (placement_info.placement_type ==
                PlacementTypeEnum.YOUTUBE_VIDEO.name):
            entity_criterion.youtube_video.video_id = placement_info.placement
        if (placement_info.placement_type ==
                PlacementTypeEnum.YOUTUBE_CHANNEL.name):
            entity_criterion.youtube_channel.channel_id = placement_info.placement
        operation = deepcopy(self.criterion_operation)
        return placement_info.customer_id, operation

    def _format_app_id(self, app_id: str) -> str:
        if app_id.startswith("mobileapp::"):
            criteria = app_id.split("-")
            app_id = criteria[-1]
            app_store = criteria[0].split("::")[-1]
            app_store = app_store.replace("mobileapp::1000", "")
            app_store = app_store.replace("1000", "")
            return f"{app_store}-{app_id}"
        return app_id

    def _exclude(self, customer_id: str, operations) -> None:
        """Applies exclusion operations for a single customer_id."""
        if not isinstance(operations, Iterable):
            operations = [operations]
        try:
            for attempt in Retrying(retry=retry_if_exception_type(
                    exceptions.InternalServerError),
                                    stop=stop_after_attempt(3),
                                    wait=wait_exponential()):
                with attempt:
                    self.mutate_operation(customer_id=str(customer_id),
                                          operations=operations)
        except RetryError as retry_failure:
            logging.error("Cannot exclude placements for account '%s' %d times",
                         customer_id,
                         retry_failure.last_attempt.attempt_number)
