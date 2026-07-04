"""Tests for PermissionRepository."""

import pytest

from app.repositories.permission import PermissionRepository
from tests.factories import PermissionFactory


class TestPermissionRepository:
    @pytest.mark.asyncio
    async def test_get_by_id(self, db_session):
        perm = await PermissionFactory.create(db_session)
        repo = PermissionRepository(db_session)
        found = await repo.get_by_id(perm.id)
        assert found is not None

    @pytest.mark.asyncio
    async def test_get_paginated(self, db_session):
        await PermissionFactory.create(db_session)
        await PermissionFactory.create(db_session)
        repo = PermissionRepository(db_session)
        items, total = await repo.get_paginated(0, 10)
        assert total == 2
