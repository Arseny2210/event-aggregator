"""Tests for Transactional context manager."""

import pytest

from app.repositories.event import EventRepository
from tests.factories import EventFactory


class TestTransactional:
    @pytest.mark.asyncio
    async def test_commit_on_success(self, db_session):
        event = await EventFactory.create(db_session)
        assert event.id is not None

    @pytest.mark.asyncio
    async def test_data_persisted(self, db_session):
        event = await EventFactory.create(db_session, title="Persisted")
        repo = EventRepository(db_session)
        found = await repo.get_by_id(event.id)
        assert found is not None
        assert found.title == "Persisted"
