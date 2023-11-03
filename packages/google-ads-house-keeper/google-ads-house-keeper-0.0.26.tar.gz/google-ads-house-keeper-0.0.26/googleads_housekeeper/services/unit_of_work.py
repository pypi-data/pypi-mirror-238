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

from typing import List
import abc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from googleads_housekeeper.adapters import repository
from googleads_housekeeper.domain import allowlisting, execution, events, settings
from .external_parsers import website_parser, youtube_data_parser


class AbstractUnitOfWork(abc.ABC):
    tasks: repository.AbstractRepository
    settings: repository.AbstractRepository
    customer_ids: repository.AbstractRepository
    mcc_ids: repository.AbstractRepository
    website_info: repository.AbstractRepository
    youtube_channel_info: repository.AbstractRepository
    youtube_video_info: repository.AbstractRepository
    allowlisting: repository.AbstractRepository
    executions: repository.AbstractRepository
    execution_details: repository.AbstractRepository
    published_events: List[events.Event] = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        while self.published_events:
            yield self.published_events.pop(0)

    @abc.abstractmethod
    def _commit(self):
        ...

    @abc.abstractmethod
    def rollback(self):
        ...


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory: str) -> None:
        self.engine = create_engine(session_factory)
        self.session_factory = sessionmaker(self.engine)
        self.published_events: List[events.Event] = []

    def __enter__(self) -> None:
        self.session = self.session_factory()  # type: Session
        self.tasks = repository.SqlAlchemyRepository(self.session)
        self.settings = repository.SqlAlchemyRepository(session=self.session,
                                                        entity=settings.Config)
        self.customer_ids = repository.SqlAlchemyRepository(
            session=self.session, entity=settings.CustomerIds)
        self.mcc_ids = repository.SqlAlchemyRepository(session=self.session,
                                                       entity=settings.MccIds)
        self.website_info = repository.SqlAlchemyRepository(
            self.session, entity=website_parser.WebsiteInfo)
        self.youtube_channel_info = repository.SqlAlchemyRepository(
            self.session, entity=youtube_data_parser.ChannelInfo)
        self.youtube_video_info = repository.SqlAlchemyRepository(
            self.session, entity=youtube_data_parser.VideoInfo)
        self.allowlisting = repository.SqlAlchemyRepository(
            self.session, entity=allowlisting.AllowlistedPlacement)
        self.executions = repository.SqlAlchemyRepository(
            self.session, entity=execution.Execution)
        self.execution_details = repository.SqlAlchemyRepository(
            self.session, entity=execution.ExecutionDetails)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

class DatastoreUnitOfWork(AbstractUnitOfWork):

    def __init__(self, client: "google.cloud.datastore.Client") -> None:
        self.client = client
        self.published_events: List[events.Event] = []

    def __enter__(self):
        self.tasks = repository.DatastoreRepository(self.client)
        self.settings = repository.DatastoreRepository(client=self.client,
                                                        entity=settings.Config)
        self.customer_ids = repository.DatastoreRepository(
            client=self.client, entity=settings.CustomerIds)
        self.mcc_ids = repository.DatastoreRepository(client=self.client,
                                                       entity=settings.MccIds)
        self.website_info = repository.DatastoreRepository(
            self.client, entity=website_parser.WebsiteInfo)
        self.youtube_channel_info = repository.DatastoreRepository(
            self.client, entity=youtube_data_parser.ChannelInfo)
        self.youtube_video_info = repository.DatastoreRepository(
            self.client, entity=youtube_data_parser.VideoInfo)
        self.allowlisting = repository.DatastoreRepository(
            self.client, entity=allowlisting.AllowlistedPlacement)
        self.executions = repository.DatastoreRepository(
            self.client, entity=execution.Execution)
        self.execution_details = repository.DatastoreRepository(
            self.client, entity=execution.ExecutionDetails)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def _commit(self):
        ...

    def rollback(self):
        ...
