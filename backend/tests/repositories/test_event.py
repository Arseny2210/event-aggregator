"""Tests for EventRepository."""

import pytest

from app.models.enums import EventStatus
from app.repositories.event import EventRepository
from app.schemas.event_search import EventSearchFilters, EventSort
from tests.factories import EventFactory, OrganizerFactory


class TestEventRepository:
    @pytest.mark.asyncio
    async def test_get_by_id(self, db_session):
        event = await EventFactory.create(db_session)
        repo = EventRepository(db_session)
        found = await repo.get_by_id(event.id)
        assert found is not None
        assert found.title == event.title

    @pytest.mark.asyncio
    async def test_get_by_organizer(self, db_session):
        org = await OrganizerFactory.create(db_session)
        await EventFactory.create(db_session, organizer=org)
        await EventFactory.create(db_session, organizer=org)
        repo = EventRepository(db_session)
        items, total = await repo.get_by_organizer(org.id, 0, 10)
        assert total == 2

    @pytest.mark.asyncio
    async def test_get_by_status(self, db_session):
        await EventFactory.create(db_session, status=EventStatus.draft)
        await EventFactory.create(db_session, status=EventStatus.published)
        repo = EventRepository(db_session)
        items, total = await repo.get_by_status(EventStatus.draft, 0, 10)
        assert total == 1

    @pytest.mark.asyncio
    async def test_get_by_date_range(self, db_session):
        from datetime import date

        await EventFactory.create(db_session, start_date=date(2026, 1, 15))
        await EventFactory.create(db_session, start_date=date(2026, 2, 1))
        repo = EventRepository(db_session)
        items, total = await repo.get_by_date_range(date(2026, 1, 1), date(2026, 1, 31), 0, 10)
        assert total == 1

    @pytest.mark.asyncio
    async def test_search_by_title(self, db_session):
        await EventFactory.create(db_session, title="Python Workshop")
        await EventFactory.create(db_session, title="Java Course")
        repo = EventRepository(db_session)
        items, total = await repo.search_by_title("Python", 0, 10)
        assert total == 1

    @pytest.mark.asyncio
    async def test_search_with_filters(self, db_session):
        await EventFactory.create(db_session, title="Python Workshop", status=EventStatus.draft)
        await EventFactory.create(db_session, title="Java Course", status=EventStatus.published)
        repo = EventRepository(db_session)
        filters = EventSearchFilters(status=EventStatus.draft, sort=EventSort.DATE_ASC)
        result = await repo.search(filters, 0, 10)
        assert result.total == 1

    @pytest.mark.asyncio
    async def test_search_no_filters_returns_all(self, db_session):
        await EventFactory.create(db_session)
        await EventFactory.create(db_session)
        repo = EventRepository(db_session)
        result = await repo.search(EventSearchFilters(), 0, 10)
        assert result.total == 2

    @pytest.mark.asyncio
    async def test_escape_like(self):
        repo = EventRepository(None)
        assert repo._escape_like("test") == "test"
        assert repo._escape_like("50% off") == r"50\% off"
        assert repo._escape_like("test_name") == r"test\_name"
