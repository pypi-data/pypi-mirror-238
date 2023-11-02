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
from typing import Any, Dict, List
from dataclasses import asdict
from google.cloud import datastore

from googleads_housekeeper.domain.task import Task


class AbstractRepository(abc.ABC):

    def __init__(self):
        self.seen = set()

    def add(self, task: Task):
        self._add(task)

    def delete(self, task_id: str):
        self._delete(task_id)

    def get(self, task_id) -> Task:
        return self._get(task_id)

    def get_by_name(self, entity_name) -> Task:
        return self._get_by_name(entity_name)

    def get_by_condition(self, condition_name: str,
                         condition_value: str) -> Task:
        return self._get_by_condition(condition_name, condition_value)

    def list(self) -> List[Task]:
        return self._list()

    def update(self, task_id: int, update_dict: Dict[str, str]) -> Task:
        return self._update(task_id, update_dict)

    @abc.abstractmethod
    def _add(self, task: Task):
        ...

    @abc.abstractmethod
    def _get(self, task_id) -> Task:
        ...

    @abc.abstractmethod
    def _get_by_name(self, entity_name) -> Task:
        ...

    @abc.abstractmethod
    def _get_by_condition(self, entity_name, condition_value) -> Task:
        ...

    @abc.abstractmethod
    def _list(self) -> List[Task]:
        ...

    @abc.abstractmethod
    def _update(self, task_id, update_dict):
        ...

    @abc.abstractmethod
    def _delete(self, task_id):
        ...


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session, entity=Task):
        super().__init__()
        self.session = session
        self.entity = entity

    def _add(self, element):
        self.session.add(element)

    def _get(self, task_id):
        return self.session.query(self.entity).filter_by(id=task_id).first()

    def _get_by_name(self, entity_name):
        return self.session.query(
            self.entity).filter_by(name=entity_name).first()

    def _get_by_condition(self, condition_name, condition_value):
        return self.session.query(self.entity).filter(
            getattr(self.entity, condition_name) == condition_value).all()

    def _list(self):
        return self.session.query(self.entity).all()

    def _update(self, task_id, update_dict):
        return self.session.query(
            self.entity).filter_by(id=task_id).update(update_dict)

    def _delete(self, task_id):
        return self.session.query(self.entity).filter_by(id=task_id).delete()


class DatastoreRepository(AbstractRepository):

    def __init__(self, client, entity=Task):
        super().__init__()
        self.client = client
        self.entity = entity
        self.collection_name = entity.__name__

    def _add(self, element):
        if hasattr(element, "id"):
            element_id = element.id
        else:
            element_id = element._id
        new_entity = datastore.Entity(
            self.client.key(self.collection_name, str(element_id)))
        for key, value in asdict(element).items():
            if hasattr(value, "name"):
                value = value.name
            new_entity[key] = value
        self.client.put(new_entity)

    def _get(self, task_id: str):
        key = self.client.key(self.collection_name, str(task_id))
        result = self.client.get(key)
        if result:
            return self.entity(**dict(result.items()))
        return None

    def _get_by_name(self, entity_name: str):
        query = self.client.query(kind=self.collection_name).add_filter(
            "name", "=", entity_name)
        return list(query.fetch(limit=1))[0]

    def _get_by_condition(self, condition_name: str, condition_value: str):
        query = self.client.query(kind=self.collection_name).add_filter(
            condition_name, "=", condition_value)
        return list(query.fetch())

    def _list(self):
        results = self.client.query(kind=self.collection_name).fetch()
        entities = [self.entity(**dict(result.items())) for result in results]
        return entities

    def _update(self, task_id: str, update_dict: Dict[str, Any]):
        results = self.client.query(kind=self.collection_name).add_filter(
            "id", "=", task_id).fetch()
        entity = [result for result in results]
        if entity:
            entity = entity[0]
            for key, value in update_dict.items():
                entity[key] = value
            self.client.put(entity)

    def _delete(self, task_id: str) -> None:
        key = self.client.key(self.collection_name, str(task_id))
        self.client.delete(key)
