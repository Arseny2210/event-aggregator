"""Tests for EventService business logic."""

from uuid import uuid4

import pytest

from app.models.enums import EventStatus
from app.repositories.event import EventRepository
from app.repositories.organizer import OrganizerRepository
from app.schemas.event import EventCreate
from app.schemas.event_search import EventSearchFilters
from app.services.event import EventService
from app.services.exceptions import EventNotFoundError, OrganizerNotFoundError
from tests.factories import CategoryFactory, EventFactory, OrganizerFactory


class TestEventService:
    @pytest.mark.asyncio
    async def test_get_event(self, db_session):
        event = await EventFactory.create(db_session)
        svc = EventService(
            session=db_session,
            repository=EventRepository(db_session),
            organizer_repository=OrganizerRepository(db_session),
        )
        found = await svc.get_event(event.id)
        assert found.id == event.id

    @pytest.mark.asyncio
    async def test_get_event_not_found(self, db_session):
        from uuid import uuid4

        svc = EventService(
            session=db_session,
            repository=EventRepository(db_session),
            organizer_repository=OrganizerRepository(db_session),
        )
        with pytest.raises(EventNotFoundError):
            await svc.get_event(uuid4())

    @pytest.mark.asyncio
    async def test_create_event(self, db_session):
        org = await OrganizerFactory.create(db_session)
        cat = await CategoryFactory.create(db_session)
        svc = EventService(
            session=db_session,
            repository=EventRepository(db_session),
            organizer_repository=OrganizerRepository(db_session),
        )
        data = EventCreate(
            title="New Event",
            description="Test description",
            start_date="2026-06-01",
            location="Test Location",
            organizer_id=org.id,
            category_id=cat.id,
        )
        event = await svc.create_event(data)
        assert event.title == "New Event"

    @pytest.mark.asyncio
    async def test_create_event_organizer_not_found(self, db_session):
        from uuid import uuid4

        svc = EventService(
            session=db_session,
            repository=EventRepository(db_session),
            organizer_repository=OrganizerRepository(db_session),
        )
        with pytest.raises(OrganizerNotFoundError):
            data = EventCreate(
                title="Orphan Event",
                description="Test",
                start_date="2026-06-01",
                location="Somewhere",
                organizer_id=uuid4(),
                category_id=uuid4(),
            )
            await svc.create_event(data)

    @pytest.mark.asyncio
    async def test_publish_event(self, db_session):
        event = await EventFactory.create(db_session, status=EventStatus.draft)
        svc = EventService(
            session=db_session,
            repository=EventRepository(db_session),
            organizer_repository=OrganizerRepository(db_session),
        )
        published = await svc.publish_event(event.id)
        assert published.status == EventStatus.published

    @pytest.mark.asyncio
    async def test_search_events(self, db_session):
        await EventFactory.create(db_session, title="Searchable Event", status=EventStatus.draft)
        await EventFactory.create(db_session, title="Other Event", status=EventStatus.draft)
        svc = EventService(
            session=db_session,
            repository=EventRepository(db_session),
            organizer_repository=OrganizerRepository(db_session),
        )
        result = await svc.search(EventSearchFilters(), 0, 10)
        assert result.total >= 2

    @pytest.mark.asyncio
    async def test_delete_event(self, db_session):
        event = await EventFactory.create(db_session)
        svc = EventService(
            session=db_session,
            repository=EventRepository(db_session),
            organizer_repository=OrganizerRepository(db_session),
        )
        await svc.delete_event(event.id)
        with pytest.raises(EventNotFoundError):
            await svc.get_event(event.id)
