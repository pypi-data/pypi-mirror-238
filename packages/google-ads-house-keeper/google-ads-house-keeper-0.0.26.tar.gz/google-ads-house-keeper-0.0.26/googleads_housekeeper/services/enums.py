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

from enum import Enum, auto


class PlacementTypeEnum(Enum):
    WEBSITE = auto()
    YOUTUBE_VIDEO = auto()
    YOUTUBE_CHANNEL = auto()
    MOBILE_APPLICATION = auto()
    MOBILE_APP_CATEGORY = auto()


class ExclusionTypeEnum(Enum):
    GOOGLE_ADS_INFO = auto()
    YOUTUBE_CHANNEL_INFO = auto()
    YOUTUBE_VIDEO_INFO = auto()
    WEBSITE_INFO = auto()
    MOBILE_APPLICATION_INFO = auto()
    MOBILE_CATEGORY_INFO = auto()


class ExclusionLevelEnum(Enum):
    AD_GROUP = 1
    CAMPAIGN = 2
    ACCOUNT = 3
    MCC = 4
