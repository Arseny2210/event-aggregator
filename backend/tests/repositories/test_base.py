"""Tests for BaseRepository CRUD operations."""

import pytest

from app.models.event import Event
from app.repositories.base import BaseRepository
from tests.factories import EventFactory


class TestBaseRepository:
    @pytest.mark.asyncio
    async def test_create(self, db_session):
        BaseRepository(db_session, Event)
        event = await EventFactory.create(db_session)
        assert event.id is not None

    @pytest.mark.asyncio
    async def test_get_by_id_found(self, db_session):
        event = await EventFactory.create(db_session)
        repo = BaseRepository(db_session, Event)
        found = await repo.get_by_id(event.id)
        assert found is not None
        assert found.id == event.id

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, db_session):
        from uuid import uuid4

        repo = BaseRepository(db_session, Event)
        found = await repo.get_by_id(uuid4())
        assert found is None

    @pytest.mark.asyncio
    async def test_get_multi_by_ids(self, db_session):
        e1 = await EventFactory.create(db_session)
        e2 = await EventFactory.create(db_session)
        repo = BaseRepository(db_session, Event)
        results = await repo.get_multi_by_ids([e1.id, e2.id])
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_delete(self, db_session):
        event = await EventFactory.create(db_session)
        repo = BaseRepository(db_session, Event)
        await repo.delete(event)
        found = await repo.get_by_id(event.id)
        assert found is None

    @pytest.mark.asyncio
    async def test_get_paginated(self, db_session):
        for _ in range(5):
            await EventFactory.create(db_session)
        repo = BaseRepository(db_session, Event)
        items, total = await repo.get_paginated(offset=0, limit=3)
        assert len(items) == 3
        assert total == 5

    @pytest.mark.asyncio
    async def test_count(self, db_session):
        for _ in range(3):
            await EventFactory.create(db_session)
        repo = BaseRepository(db_session, Event)
        total = await repo.count()
        assert total == 3
