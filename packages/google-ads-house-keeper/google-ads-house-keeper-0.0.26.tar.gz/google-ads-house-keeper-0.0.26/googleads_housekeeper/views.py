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

from __future__ import annotations
from typing import Any, Dict, List, Optional
from dataclasses import asdict
from functools import lru_cache

from googleads_housekeeper.services import unit_of_work

registry = {}


def task(task_id: int,
         uow: unit_of_work.AbstractUnitOfWork) -> dict[str, Any] | None:
    with uow:
        if task := uow.tasks.get(task_id):
            return asdict(task)
        return None


def tasks(uow: unit_of_work.AbstractUnitOfWork) -> list[dict[str, Any]]:
    with uow:
        return [asdict(t) for t in uow.tasks.list()]


def config(uow: unit_of_work.AbstractUnitOfWork) -> list[dict[str, Any]]:
    with uow:
        return [asdict(c) for c in uow.settings.list()]


def allowlisted_placements(
        uow: unit_of_work.AbstractUnitOfWork) -> list[dict[str, Any]] | None:
    with uow:
        if allowlisted_placements := uow.allowlisting.list():
            return [asdict(t) for t in allowlisted_placements]
    return None


def executions(
        task_id: str,
        uow: unit_of_work.AbstractUnitOfWork) -> list[dict[str, Any]] | None:
    with uow:
        if task_executions := uow.executions.get_by_condition("task", task_id):
            return [asdict(t) for t in task_executions]
    return None


def execution_details(
        task_id: str, execution_id: str,
        uow: unit_of_work.AbstractUnitOfWork) -> list[dict[str, Any]] | None:
    with uow:
        if task_executions := uow.executions.get_by_condition("task", task_id):
            if execution_details := uow.execution_details.get_by_condition(
                    "execution_id", execution_id):
                return [asdict(t) for t in execution_details]
    return None


def customer_ids(uow: unit_of_work.AbstractUnitOfWork,
                 mcc_id: str) -> list[dict[str, Any]]:
    if customer_ids := registry.get("customer_ids"):
        if result := customer_ids.get(mcc_id):
            return result
    with uow:
        customer_ids = [asdict(r) for r in uow.customer_ids.list()]
        registry["customer_ids"] = {mcc_id: customer_ids}
        return customer_ids


def mcc_ids(uow: unit_of_work.AbstractUnitOfWork) -> list[dict[str, str]]:
    if mcc_ids := registry.get("mcc_ids"):
        return mcc_ids
    with uow:
        mcc_ids = [asdict(r) for r in uow.mcc_ids.list()]
        registry["mcc_ids"] = mcc_ids
        return mcc_ids
