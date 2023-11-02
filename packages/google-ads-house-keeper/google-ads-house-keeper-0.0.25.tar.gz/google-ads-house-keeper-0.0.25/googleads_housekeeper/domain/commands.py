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

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from googleads_housekeeper.domain.task import TaskOutput
from googleads_housekeeper.services.enums import PlacementTypeEnum


class Command:
    ...


@dataclass
class RunTask(Command):
    id: int
    save_to_db: bool = True


@dataclass
class SaveTask(Command):
    exclusion_rule: str
    customer_ids: str
    from_days_ago: int = 0
    date_range: int = 7
    exclusion_level: str = "AD_GROUP"
    output: str = TaskOutput.EXCLUDE_AND_NOTIFY.name
    name: Optional[str] = None
    schedule: Optional[str] = None
    placement_types: Optional[str] = None
    task_id: Optional[str] = None


@dataclass
class DeleteTask(Command):
    task_id: int


@dataclass
class RunManualExclusion(Command):
    customer_ids: str
    placements: List[str]


@dataclass
class PreviewPlacements(Command):
    exclusion_rule: str
    placement_types: Optional[Tuple[str, ...]]
    customer_ids: List[str]
    from_days_ago: int
    lookback_days: int
    exclusion_level: str = "AD_GROUP"
    exclude_and_notify: str = "EXCLUDE_AND_NOTIFY"
    save_to_db: bool = True


@dataclass
class AddToAllowlisting(Command):
    placement: Dict[str, str]


@dataclass
class RemoveFromAllowlisting(Command):
    placement: Dict[str, str]


@dataclass
class SaveConfig(Command):
    id: str
    mcc_id: str
    email_address: str
    save_to_db: bool = False


@dataclass
class GetCustomerIds(Command):
    mcc_id: str


@dataclass
class GetMccIds(Command):
    ...
