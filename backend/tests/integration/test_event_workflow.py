"""Integration tests for event workflow."""

import pytest

from app.models.enums import EventStatus
from tests.factories import EventFactory, OrganizerFactory


class TestEventWorkflow:
    @pytest.mark.asyncio
    async def test_event_lifecycle(self, db_session):
        org = await OrganizerFactory.create(db_session)
        event = await EventFactory.create(db_session, organizer=org, status=EventStatus.draft)
        assert event.status == EventStatus.draft
        assert event.organizer_id == org.id

    @pytest.mark.asyncio
    async def test_multiple_events_for_organizer(self, db_session):
        org = await OrganizerFactory.create(db_session)
        await EventFactory.create(db_session, organizer=org)
        await EventFactory.create(db_session, organizer=org)
        from app.repositories.event import EventRepository

        repo = EventRepository(db_session)
        items, total = await repo.get_by_organizer(org.id, 0, 10)
        assert total == 2
