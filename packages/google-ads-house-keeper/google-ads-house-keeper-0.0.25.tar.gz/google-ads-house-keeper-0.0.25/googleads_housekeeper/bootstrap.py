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
import inspect
from gaarf.api_clients import GoogleAdsApiClient

if os.getenv("ADS_HOUSEKEEPER_DEPLOYMENT_TYPE") == "Google Cloud":
    try:
        from google.cloud import datastore, pubsub_v1
    except ImportError as e:
        raise ImportError(
            "Please install googleads-housekeeper with Google Cloud support - `pip install googleads-housekeeper[gcp]`"
        ) from e

from googleads_housekeeper.adapters import orm, notifications, publisher
from googleads_housekeeper.services import handlers, messagebus, unit_of_work


class Bootstrapper:

    def __init__(self, type: str = "Local") -> None:
        if type == "Local":
            self.bootstrapper = LocalBootstrapper()
        if type == "Google Cloud":
            self.bootstrapper = GoogleCloudBootstrapper()
        if type == "Dev":
            self.bootstrapper = DevBootstrapper()

    def bootstrap_app(self):
        return self.bootstrapper._bootstrap()

    def _bootstrap(self):
        return bootstrap(start_orm=self.start_orm,
                         uow=self.uow,
                         publish_service=self.publish_service)


class GoogleCloudBootstrapper(Bootstrapper):

    def __init__(self,
                 datastore_client=None,
                 pubsub_client=None,
                 project_id: str = None,
                 start_orm: bool = False) -> None:
        self.start_orm = False
        self.uow = unit_of_work.DatastoreUnitOfWork(datastore.Client())
        self.publish_service = publisher.GoogleCloudPubSubPublisher(
            client=pubsub_v1.PublisherClient(),
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT"))


class LocalBootstrapper(Bootstrapper):

    def __init__(self) -> None:
        self.start_orm = True
        self.uow = unit_of_work.SqlAlchemyUnitOfWork(get_db_uri())
        self.publish_service = publisher.LogPublisher()


class DevBootstrapper(Bootstrapper):

    def __init__(self) -> None:
        self.start_orm = True
        self.uow = unit_of_work.SqlAlchemyUnitOfWork(
            f"sqlite:///{os.getcwd()}/ads_housekeeper_tasks.db")
        self.publish_service = publisher.LogPublisher()


def get_db_uri(host: str = os.environ.get("DB_HOST", "localhost"),
               port: int = int(os.environ.get("DB_PORT", 54321)),
               user: str = os.environ.get("DB_USER", "ads_housekeeper"),
               password: str = os.environ.get("DB_PASSWORD",
                                              "ads_housekeeper"),
               db_name: str = os.environ.get("DB_NAME", "ads_housekeeper"),
               db_engine: str = os.environ.get("DB_ENGINE",
                                               "postgresql")) -> str:
    if dev_db := os.environ.get("DEV_DB_HOST"):
        return f"sqlite:///{dev_db}"
    return f"{db_engine}://{user}:{password}@{host}:{port}/{db_name}"


def get_default_google_ads_api_client():
    return GoogleAdsApiClient(path_to_config=get_path_to_ads_config(),
                              version=get_ads_api_version())


def get_ads_api_version() -> str:
    return os.environ.get("GOOGLE_ADS_API_VERSION", "v14")


def get_path_to_ads_config() -> str:
    return os.environ.get("GOOGLE_ADS_PATH_TO_CONFIG", "~/google-ads.yaml")


def get_notification_service() -> notifications.BaseNotifications:
    notification_service_factory = notifications.NotificationFactory()
    notification_type = os.environ.get("ADS_HOUSEKEEPER_NOTIFICATION_TYPE", "console")
    notification_service = notification_service_factory.create_nofication_service(
        notification_type=notification_type)
    return notification_service



def bootstrap(
    ads_api_client: GoogleAdsApiClient = get_default_google_ads_api_client(),
    start_orm: bool = True,
    uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(
        get_db_uri()),
    notification_service: notifications.
    BaseNotifications = get_notification_service(),
    publish_service: publisher.BasePublisher = publisher.LogPublisher()
) -> messagebus.MessageBus:

    if start_orm:
        orm.start_mappers(engine=uow.engine)

    dependencies = {
        "uow": uow,
        "ads_api_client": ads_api_client,
        "notification_service": notification_service,
        "publisher": publish_service
    }
    injected_event_handlers = {
        event_type:
        [inject_dependencies(handler, dependencies) for handler in handlers]
        for event_type, handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }
    return messagebus.MessageBus(uow=uow,
                                 event_handlers=injected_event_handlers,
                                 command_handlers=injected_command_handlers,
                                 dependencies=dependencies)


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items() if name in params
    }
    return lambda message: handler(message, **deps)


