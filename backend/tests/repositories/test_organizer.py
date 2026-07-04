"""Tests for OrganizerRepository."""

import pytest

from app.repositories.organizer import OrganizerRepository
from tests.factories import OrganizerFactory


class TestOrganizerRepository:
    @pytest.mark.asyncio
    async def test_get_by_id(self, db_session):
        org = await OrganizerFactory.create(db_session)
        repo = OrganizerRepository(db_session)
        found = await repo.get_by_id(org.id)
        assert found is not None

    @pytest.mark.asyncio
    async def test_get_by_name_found(self, db_session):
        await OrganizerFactory.create(db_session, name="Test Org")
        repo = OrganizerRepository(db_session)
        found = await repo.get_by_name("Test Org")
        assert found is not None
        assert found.name == "Test Org"

    @pytest.mark.asyncio
    async def test_get_by_name_not_found(self, db_session):
        repo = OrganizerRepository(db_session)
        found = await repo.get_by_name("Nonexistent")
        assert found is None

    @pytest.mark.asyncio
    async def test_get_paginated(self, db_session):
        await OrganizerFactory.create(db_session)
        await OrganizerFactory.create(db_session)
        repo = OrganizerRepository(db_session)
        items, total = await repo.get_paginated(0, 10)
        assert total == 2
