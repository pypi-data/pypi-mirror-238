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

from typing import Optional

import json
from dataclasses import asdict
from googleads_housekeeper.domain import events
import logging


class BasePublisher:
    ...


class RedisPublisher(BasePublisher):

    def __init__(self,
                 client: "redis.Redis",
                 topic_prefix: Optional[str] = None) -> None:
        self.client = client
        self.topic_prefix = topic_prefix

    def publish(self, topic: str, event: events.Event):
        if self.topic_prefix:
            topic = f"{self.topic_prefix}_{topic}"
        self.client.publish(topic, json.dumps(asdict(event)))


class GoogleCloudPubSubPublisher(BasePublisher):

    def __init__(self,
                 client: "google.cloud.pubsub_v1.PublisherClient",
                 project_id: str,
                 topic_prefix: Optional[str] = None) -> None:
        self.client = client
        self.project_id = project_id
        self.topic_prefix = topic_prefix

    def publish(self, topic: str, event: events.Event):
        if self.topic_prefix:
            topic = f"{self.topic_prefix}_{topic}"
        topic_name = f"projects/{self.project_id}/topics/{topic}"
        data = str(json.dumps(asdict(event))).encode("utf-8")
        future = self.client.publish(topic_name, data=data)
        future.result()


class LogPublisher(BasePublisher):

    def publish(self, topic: str, event: events.Event):
        logging.info("Published to topic '%s': %s", topic, asdict(event))

