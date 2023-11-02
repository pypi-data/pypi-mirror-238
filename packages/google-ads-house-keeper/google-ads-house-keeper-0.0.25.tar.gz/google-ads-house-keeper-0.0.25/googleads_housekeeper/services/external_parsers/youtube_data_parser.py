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

import os
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Mapping, Optional, Set
from datetime import datetime
from googleapiclient.discovery import build

from .base_parser import BaseParser


class YouTubeDataConnector:

    def __init__(self,
                 api_version: str = "v3",
                 developer_key: str = os.getenv("YOUTUBE_DATA_API_KEY")):
        self.service = build("youtube",
                             api_version,
                             developerKey=developer_key)

    def get_response(self, type_, elements, element_id):
        if type_ == "videos":
            service = self.service.videos()
        elif type_ == "channels":
            service = self.service.channels()
        else:
            raise ValueError(f"Unsupported resource {type_}")
        return service.list(part=elements, id=element_id).execute()


@dataclass(frozen=True)
class ChannelInfo:
    placement: str
    title: Optional[str] = None
    description: Optional[str] = None
    country: Optional[str] = None
    viewCount: int = 0
    subscriberCount: int = 0
    videoCount: int = 0
    topicCategories: str = ""
    last_processed_time: datetime = datetime.now()
    is_processed: bool = True


@dataclass(frozen=True)
class VideoInfo:
    placement: str
    title: Optional[str] = None
    description: Optional[str] = None
    defaultLanguage: Optional[str] = None
    defaultAudioLanguage: Optional[str] = None
    commentCount: int = 0
    favouriteCount: int = 0
    likeCount: int = 0
    viewCount: int = 0
    madeForKids: bool = False
    tags: str = ""
    topicCategories: str = ""
    last_processed_time: datetime = datetime.now()
    is_processed: bool = True


class ChannelInfoParser(BaseParser):

    def __init__(self, data_connector=YouTubeDataConnector):
        self.data_connector = data_connector

    def parse(
            self,
            channel_id: str,
            elements: str = "id,snippet,statistics,topicDetails"
    ) -> ChannelInfo:
        response = self.data_connector().get_response("channels", elements,
                                                      channel_id)
        if not (items := response.get("items")):
            return ChannelInfo(placement=channel_id, is_processed=False)
        item = items[0]
        if snippet := item.get("snippet"):
            title = snippet.get("title")
            description = snippet.get("description")
            country = snippet.get("country")
        else:
            title = None
            description = None
            country = None
        if statistics := item.get("statistics"):
            subscriberCount = int(statistics.get("subscriberCount"))
            viewCount = int(statistics.get("viewCount"))
            videoCount = int(statistics.get("videoCount"))
        else:
            subscriberCount = 0
            viewCount = 0
            videoCount = 0
        topics = parse_topic_details(item.get("topicDetails"))
        return ChannelInfo(placement=channel_id,
                           title=title,
                           description=description,
                           country=country,
                           viewCount=viewCount,
                           subscriberCount=subscriberCount,
                           videoCount=videoCount,
                           topicCategories=topics)


class VideoInfoParser(BaseParser):

    def __init__(self, data_connector=YouTubeDataConnector):
        self.data_connector = data_connector

    def parse(
        self,
        video_id: str,
        elements:
        str = "id,status,snippet,statistics,contentDetails,topicDetails"
    ) -> VideoInfo:
        response = self.data_connector().get_response("videos", elements,
                                                      video_id)
        if not (items := response.get("items")):
            return VideoInfo(placement=video_info, is_processed=False)
        item = items[0]
        if snippet := item.get("snippet"):
            title = snippet.get("title")
            description = snippet.get("description")
            defaultLanguage = snippet.get("defaultLanguage")
            defaultAudioLanguage = snippet.get("defaultAudioLanguage")
            tags = snippet.get("tags")
        else:
            title = None
            description = None
            defaultLanguage = None
            defaultAudioLanguage = None
            tags = ""
        if statistics := item.get("statistics"):
            commentCount = int(statistics.get("commentCount"))
            favouriteCount = int(statistics.get("favouriteCount"))
            likeCount = int(statistics.get("likeCount"))
            viewCount = int(statistics.get("viewCount"))
        else:
            commentCount = 0
            favouriteCount = 0
            likeCount = 0
            viewCount = 0
        if status := item.get("status"):
            madeForKids = bool(status.get("madeForKids"))
        else:
            madeForKids = False
        topics = parse_topic_details(item.get("topicDetails"))
        if tags:
            tags = ",".join(tags)
        return VideoInfo(placement=video_id,
                         title=title,
                         description=description,
                         defaultLanguage=defaultLanguage,
                         defaultAudioLanguage=defaultAudioLanguage,
                         commentCount=commentCount,
                         favouriteCount=favouriteCount,
                         likeCount=likeCount,
                         viewCount=viewCount,
                         madeForKids=madeForKids,
                         tags=tags,
                         topicCategories=topics)


def parse_topic_details(topicDetails: Optional[Mapping[str, Any]]) -> str:
    if not topicDetails:
        return ""
    if not (topic_categories := topicDetails.get("topicCategories")):
        return ""
    return ",".join(
        list(set([topic.split("/")[-1] for topic in topic_categories])))
