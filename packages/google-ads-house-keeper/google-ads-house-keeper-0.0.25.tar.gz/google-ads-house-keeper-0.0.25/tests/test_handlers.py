from typing import List

from collections import defaultdict
from datetime import datetime
from googleads_housekeeper import bootstrap, views
from googleads_housekeeper.adapters import repository, notifications, publisher
from googleads_housekeeper.domain import commands, events, task
from googleads_housekeeper.services import unit_of_work, external_parsers
import pytest


class FakeGoogleAdsApiClient:
    ...


class FakeNotifications(notifications.BaseNotifications):

    def __init__(self):
        self.sent = defaultdict(list)  # type: Dict[str, List[str]]

    def publish(self, topic, event):
        self.sent[destination].append(message)


class FakePublisher(publisher.BasePublisher):

    def __init__(self):
        self.events = []  # type: Dict[str, List[str]]

    def publish(self, topic, event):
        self.events.append(event)


class FakeRepository(repository.AbstractRepository):

    def __init__(self):
        super().__init__()
        self.session = list()

    def _add(self, element):
        self.session.append(element)

    def _get(self, task_id):
        return next(e for e in self.session if e.id == task_id)

    def _get_by_name(self, entity_name):
        try:
            return next(e for e in self.session if e.name == entity_name)
        except StopIteration:
            return None

    def _list(self):
        return list(self.session)

    def _update(self, task_id, update_dict):
        element = self._get(task_id)
        element_dict = element.__dict__
        element_dict.update(update_dict)
        element.__init__(**element_dict)

    def _delete(self, task_id):
        element = self._get(task_id)
        self.session.remove(element)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    tasks: FakeRepository = FakeRepository()
    settings: FakeRepository = FakeRepository()
    customer_ids: FakeRepository = FakeRepository()
    mcc_ids: FakeRepository = FakeRepository()
    website_info: FakeRepository = FakeRepository()
    youtube_channel_info: FakeRepository = FakeRepository()
    youtube_video_info: FakeRepository = FakeRepository()
    allowlisting: FakeRepository = FakeRepository()
    executions: FakeRepository = FakeRepository()
    execution_details: FakeRepository = FakeRepository()
    published_events: List[events.Event] = []

    def __init__(self) -> None:
        ...

    def _commit(self):
        self.committed = True

    def rollback(self):
        ...


@pytest.fixture
def fake_uow():
    uow = FakeUnitOfWork()
    uow.website_info.add(
        external_parsers.website_parser.WebsiteInfo(
            placement="example.com",
            title="fun games",
            description="millions of fun games",
            keywords="browser games, free games",
            is_processed=True,
            last_processed_time=datetime.now()))
    uow.youtube_channel_info.add(
        external_parsers.youtube_data_parser.ChannelInfo(
            placement="1kdjf0skdjfw0dsdf",
            title="Gardening and Games",
            description="Everything about Games and Gardens",
            country="US",
            viewCount=1000,
            subscriberCount=100,
            videoCount=10,
            topicCategories="Gardening,Games",
            last_processed_time=datetime.now(),
            is_processed=True))
    uow.youtube_video_info.add(
        external_parsers.youtube_data_parser.VideoInfo(
            placement="jojoh",
            title="Gardening and Games Vol. 2",
            description="The second volumes of the Gardening and Games series",
            defaultLanguage="en",
            defaultAudioLanguage="en",
            commentCount=10,
            favouriteCount=10,
            likeCount=10,
            viewCount=1000,
            madeForKids=True,
            topicCategories="Gardening,Games",
            tags="#multiplayer,#mro,#garden",
            last_processed_time=datetime.now(),
            is_processed=True))
    return uow


@pytest.fixture(scope="module")
def fake_publisher():
    return FakePublisher()


@pytest.fixture(scope="module")
def bus(fake_publisher):
    return bootstrap.bootstrap(start_orm=False,
                               ads_api_client=FakeGoogleAdsApiClient(),
                               uow=FakeUnitOfWork(),
                               publish_service=fake_publisher)


class TestTask:

    def test_create_task_populated_repository(self, bus):
        cmd = commands.SaveTask(exclusion_rule="clicks > 0", customer_ids="1")
        bus.handle(cmd)
        assert bus.uow.tasks.list()

    def test_create_task_publish_task_create_event(self, bus, fake_publisher):
        cmd = commands.SaveTask(exclusion_rule="clicks > 0", customer_ids="1")
        bus.handle(cmd)
        assert isinstance(fake_publisher.events[0], events.TaskCreated)

    def test_create_task_process_queue(self, bus):
        cmd = commands.SaveTask(exclusion_rule="clicks > 0", customer_ids="1")
        bus.handle(cmd)
        assert not bus.queue

    def test_tasks_view_is_not_empty_after_creating_task(self, bus):
        cmd = commands.SaveTask(exclusion_rule="clicks > 0", customer_ids="1")
        bus.handle(cmd)
        assert views.tasks(bus.uow)

    def test_update_task_change_task_in_repository(self, bus):
        create_cmd = commands.SaveTask(exclusion_rule="clicks > 0",
                                       customer_ids="1")
        task_id = bus.handle(create_cmd)
        update_cmd = commands.SaveTask(exclusion_rule="clicks > 1",
                                       customer_ids="2",
                                       task_id=task_id)
        bus.handle(update_cmd)
        assert bus.uow.tasks.get(task_id).exclusion_rule == "clicks > 1"
        assert bus.uow.tasks.get(task_id).customer_ids == "2"

    def test_update_task_publish_task_updated_event(self, bus, fake_publisher):
        create_cmd = commands.SaveTask(exclusion_rule="clicks > 0",
                                       customer_ids="1")
        task_id = bus.handle(create_cmd)
        update_cmd = commands.SaveTask(exclusion_rule="clicks > 1",
                                       customer_ids="2",
                                       task_id=task_id)
        bus.handle(update_cmd)
        assert events.TaskCreated(task_id) in fake_publisher.events
        assert events.TaskUpdated(task_id) in fake_publisher.events

    def test_update_task_process_queue(self, bus):
        create_cmd = commands.SaveTask(exclusion_rule="clicks > 0",
                                       customer_ids="1")
        task_id = bus.handle(create_cmd)
        update_cmd = commands.SaveTask(exclusion_rule="clicks > 1",
                                       customer_ids="2",
                                       task_id=task_id)
        bus.handle(update_cmd)
        assert not bus.queue

    def test_delete_task_makes_task_status_inactive(self, bus):
        create_cmd = commands.SaveTask(exclusion_rule="clicks > 0",
                                       customer_ids="1")
        task_id = bus.handle(create_cmd)
        delete_cmd = commands.DeleteTask(task_id=task_id)
        bus.handle(delete_cmd)
        assert bus.uow.tasks.get(task_id).status == "INACTIVE"

    def test_delete_task_publishes_task_deleted_event(self, bus,
                                                      fake_publisher):
        create_cmd = commands.SaveTask(exclusion_rule="clicks > 0",
                                       customer_ids="1")
        task_id = bus.handle(create_cmd)
        delete_cmd = commands.DeleteTask(task_id=task_id)
        bus.handle(delete_cmd)
        assert events.TaskCreated(task_id) in fake_publisher.events
        assert events.TaskDeleted(task_id) in fake_publisher.events

    def test_delete_task_process_queue(self, bus, fake_publisher):
        create_cmd = commands.SaveTask(exclusion_rule="clicks > 0",
                                       customer_ids="1")
        task_id = bus.handle(create_cmd)
        delete_cmd = commands.DeleteTask(task_id=task_id)
        bus.handle(delete_cmd)
        assert not bus.queue


class TestAllowlisting:

    def test_add_to_allowlisting_create_entry_in_repository(self, bus):
        allowlisting_cmd = commands.AddToAllowlisting({"type": "fake_type", "name": "fake_name"})
        bus.handle(allowlisting_cmd)
        assert bus.uow.allowlisting.list()

    def test_remove_from_allowlisting_empties_in_repository(self, bus):
        allowlisting_cmd = commands.AddToAllowlisting({"type": "fake_type", "name": "fake_name"})
        bus.handle(allowlisting_cmd)
        removal_allowlisting_cmd = commands.RemoveFromAllowlisting({"type": "fake_type", "name": "fake_name"})
        bus.handle(removal_allowlisting_cmd)
        assert not bus.uow.allowlisting.list()
