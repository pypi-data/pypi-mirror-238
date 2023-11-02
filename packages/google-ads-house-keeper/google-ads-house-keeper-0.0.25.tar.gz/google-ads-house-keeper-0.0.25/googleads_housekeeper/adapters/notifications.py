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

import abc

import os
from typing import Any, Dict, Optional, Union


class BaseNotifications(abc.ABC):

    @abc.abstractmethod
    def send(
            self,
            message_body: str,  # TODO: should it be GaarfReport?
            destination: Optional[str] = None,
            title: Optional[str] = None,
            custom_sender: Optional[str] = None,
            **kwargs: str) -> None:
        ...


class GoogleCloudAppEngineEmailNotifications(BaseNotifications):

    def __init__(self, project_id: str) -> None:
        from google.appengine.api import mail
        self.project_id = project_id
        self.project_id = f"no-reply@{project_id}.appspotmail.com"
        self.email_service = mail.EmailMessage

    def send(self,
             message_body,
             destination,
             title,
             custom_sender,
             **kwargs):
        if custom_sender:
            task_prefix = f"_{custom_sender}" if custom_sender else ''
            sender = "exclusions{task_prefix}@{self.project_id}.appspotmail.com"
        else:
            sender = "exclusions@{self.project_id}.appspotmail.com"
        message = self.email_service(sender=sender,
                                     subject=title,
                                     to=destination,
                                     body=message_body)
        message.send()


class SlackNotifications(BaseNotifications):

    def __init__(self, bot_token: str, channel: str) -> None:
        from slack import WebClient
        self.client = WebClient(token=bot_token)
        self.channel = channel

    def send(self,
             message_body,
             destination,
             title,
             **kwargs):

        file = message_body.to_csv(index=False, sep="\t")
        self.client.files_upload(
            channels=destination or self.channel,
            initial_comment=title,
            filename=f"{title}.tsv" if title else "cpr.tsv",
            content=file)


class ConsoleNotifications(BaseNotifications):

    def send(self, message_body, **kwargs):
        print(message_body)


class NullNofication(BaseNotifications):

    def __init__(self, notification_type: str, **kwargs):
        raise ValueError(f"{notification_type} is unknown writer type!")


class NotificationFactory:
    types: Dict[str, Dict[str, Union[BaseNotifications, Dict[str, Any]]]] = {}

    def __init__(self):
        self.load_types()

    def load_types(self):
        self.types["email"] = {
            "type": GoogleCloudAppEngineEmailNotifications,
            "args": {}
        }
        self.types["slack"] = {
            "type": SlackNotifications,
            "args": {
                "bot_token": os.environ.get("CPR_SLACK_BOT_TOKEN"),
                "channel": os.environ.get("CPR_SLACK_CHANNEL")
            }
        }
        self.types["console"] = {"type": ConsoleNotifications, "args": {}}

    def create_nofication_service(self, notification_type: str):
        if notification_type in self.types:
            if args := self.types[notification_type].get("args"):
                return self.types[notification_type].get("type")(**args)
            else:
                return self.types[notification_type].get("type")()
        else:
            return NullNotifications(notification_type)
