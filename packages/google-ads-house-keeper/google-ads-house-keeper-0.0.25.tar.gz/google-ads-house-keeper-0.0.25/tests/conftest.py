from typing import List

from datetime import datetime
from googleads_housekeeper.adapters import repository
from googleads_housekeeper.domain import events, task
from googleads_housekeeper.services import unit_of_work, external_parsers
import pytest

class FakeRepository(repository.AbstractRepository):

    def __init__(self):
        super().__init__()
        self.session = list()

    def _add(self, element):
        self.session.append(element)

    def _get(self, task_id):
        return next(e for e in self.session if e.id == task_id)

    def _get_by_name(self, entity_name):
        return next(e for e in self.session if e.placement == entity_name)

    def _list(self):
        return list(self.session)

    def _update(self, task_id, update_dict):
        ...

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

