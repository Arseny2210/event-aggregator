"""Tests for ParticipationRepository."""

import pytest

from app.repositories.participation import ParticipationRepository
from tests.factories import ParticipationFactory


class TestParticipationRepository:
    @pytest.mark.asyncio
    async def test_get_by_id(self, db_session):
        part = await ParticipationFactory.create(db_session)
        repo = ParticipationRepository(db_session)
        found = await repo.get_by_id(part.id)
        assert found is not None

    @pytest.mark.asyncio
    async def test_get_paginated(self, db_session):
        await ParticipationFactory.create(db_session)
        await ParticipationFactory.create(db_session)
        repo = ParticipationRepository(db_session)
        items, total = await repo.get_paginated(0, 10)
        assert total == 2
