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

from dataclasses import dataclass, field
from itertools import count
from enum import Enum
from typing import Optional
from datetime import datetime
import uuid

from googleads_housekeeper.services.enums import ExclusionLevelEnum


class TaskStatus(Enum):
    ACTIVE = 0
    INACTIVE = 1


class TaskOutput(Enum):
    NOTIFY = 1
    EXCLUDE = 2
    EXCLUDE_AND_NOTIFY = 3


@dataclass
class Task:
    name: str
    exclusion_rule: str
    customer_ids: str
    date_range: int = 7
    from_days_ago: int = 0
    exclusion_level: ExclusionLevelEnum = ExclusionLevelEnum.AD_GROUP
    placement_types: Optional[str] = None
    output: TaskOutput = TaskOutput.EXCLUDE_AND_NOTIFY
    status: TaskStatus = TaskStatus.ACTIVE
    schedule: Optional[str] = None
    creation_date: datetime = datetime.now()
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
