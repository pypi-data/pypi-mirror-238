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

from sqlalchemy import (Table, MetaData, Column, Integer, String, DateTime,
                        Boolean, Enum, ForeignKey)
from sqlalchemy.orm import mapper, relationship, backref

from googleads_housekeeper.domain.task import Task, TaskStatus, TaskOutput
from googleads_housekeeper.domain.execution import Execution, ExecutionDetails
from googleads_housekeeper.domain.allowlisting import AllowlistedPlacement
from googleads_housekeeper.domain.settings import Config, CustomerIds, MccIds
from googleads_housekeeper.services.external_parsers import website_parser, youtube_data_parser
from googleads_housekeeper.services import enums

metadata = MetaData()

tasks = Table(
    "tasks",
    metadata,
    Column("_id", Integer, autoincrement=True),
    Column("id", String(36), primary_key=True),
    Column("name", String(255)),
    Column("exclusion_rule", String(255)),
    Column("customer_ids", String(255)),
    Column("date_range", Integer),
    Column("exclusion_level", Enum(enums.ExclusionLevelEnum)),
    Column("output", Enum(TaskOutput)),
    Column("from_days_ago", Integer),
    Column("placement_types", String(255)),
    Column("creation_date", DateTime),
    Column("status", Enum(TaskStatus)),
    Column("schedule", String(255)),
)

execution = Table("executions", metadata,
                  Column("_id", Integer, autoincrement=True),
                  Column("id", String(36), primary_key=True, nullable=False),
                  Column("task", ForeignKey("tasks.id"), nullable=False),
                  Column("start_time", DateTime, nullable=False),
                  Column("end_time", DateTime, nullable=False))

execution_details = Table(
    "execution_details",
    metadata,
    Column("_id", Integer, autoincrement=True),
    Column("id", String(36), primary_key=True, nullable=False),
    Column("execution_id",
           ForeignKey("executions.id"),
           nullable=False),
    Column("placement", String(255), nullable=False),
    Column("placement_type", String(255), nullable=False),
    Column("reason", String(255), nullable=False),
)

allowlisted_placements = Table(
    "allowlisted_placements", metadata,
    Column("_id", Integer, autoincrement=True),
    Column("id", String(36), primary_key=True, nullable=False),
    Column("type", Enum(enums.PlacementTypeEnum)),
    Column("name", String(255), unique=True))

config = Table("config", metadata,
               Column("_id", Integer, autoincrement=True),
               Column("id", String(36), primary_key=True, nullable=False),
               Column("mcc_id", String(10)),
               Column("save_to_db", Boolean),
               Column("email_address", String(50)))

customer_ids = Table("customer_ids", metadata,
                     Column("mcc_id", String(10), primary_key=True),
                     Column("account_name", String(255)),
                     Column("id", String(10), primary_key=True))

mcc_ids = Table(
    "mcc_ids",
    metadata,
    Column("mcc_id", String(10), primary_key=True),
    Column("account_name", String(255)),
)

website_info = Table(
    "external_parser.website_info", metadata,
    Column("_id", Integer, autoincrement=True),
    Column("id", String(36), primary_key=True, nullable=False),
    Column("placement", String(255)),
    Column("title", String(255), nullable=True),
    Column("description", String(1000), nullable=True),
    Column("keywords", String(1000), nullable=True),
    Column("last_processed_time", DateTime), Column("is_processed", Boolean))

youtube_channel_info = Table(
    "external_parser.youtube_channel_info", metadata,
    Column("_id", Integer, autoincrement=True),
    Column("id", String(36), primary_key=True, nullable=False),
    Column("placement", String(255)),
    Column("title", String(255), nullable=True),
    Column("description", String(1000), nullable=True),
    Column("viewCount", Integer), Column("subscriberCount", Integer),
    Column("videoCount", Integer),
    Column("topicCategories", String(1000), nullable=True),
    Column("last_processed_time", DateTime), Column("is_processed", Boolean))

youtube_video_info = Table(
    "external_parser.youtube_video_info", metadata,
    Column("_id", Integer, autoincrement=True),
    Column("id", String(36), primary_key=True, nullable=False),
    Column("placement", String(255)),
    Column("title", String(255), nullable=True),
    Column("description", String(1000), nullable=True),
    Column("defaultLanguage", String(10), nullable=True),
    Column("defaultAudioLanguage", String(10), nullable=True),
    Column("commentCount", Integer), Column("favouriteCount", Integer),
    Column("likeCount", Integer), Column("viewCount", Integer),
    Column("madeForKids", Boolean), Column("tags", String(1000)),
    Column("topicCategories", String(1000)),
    Column("last_processed_time", DateTime), Column("is_processed", Boolean))


def start_mappers(engine):
    execution_details_mapper = mapper(ExecutionDetails, execution_details)
    execution_mapper = mapper(Execution, execution,
                         properties={
                             "details":
                             relationship(execution_details_mapper,
                                          collection_class=list)
                         })
    task_mapper = mapper(Task,
                         tasks,
                         properties={
                             "executions":
                             relationship(execution_mapper,
                                          collection_class=list)
                         })
    settings_mapper = mapper(Config, config)
    allowlisted_placements_mapper = mapper(AllowlistedPlacement,
                                           allowlisted_placements)
    mcc_ids_mapper = mapper(MccIds, mcc_ids)
    customer_ids_mapper = mapper(CustomerIds, customer_ids)
    websites_info = mapper(website_parser.WebsiteInfo, website_info)
    youtube_channels_info = mapper(youtube_data_parser.ChannelInfo,
                                   youtube_channel_info)
    youtube_videos_info = mapper(youtube_data_parser.VideoInfo,
                                 youtube_video_info)
    if engine:
        metadata.create_all(engine)
