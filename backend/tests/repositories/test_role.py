"""Tests for RoleRepository and PermissionRepository."""

import pytest

from app.repositories.permission import PermissionRepository
from app.repositories.role import RoleRepository
from tests.factories import (
    PermissionFactory,
    RoleFactory,
)


class TestRoleRepository:
    @pytest.mark.asyncio
    async def test_get_by_id(self, db_session):
        role = await RoleFactory.create(db_session)
        repo = RoleRepository(db_session)
        found = await repo.get_by_id(role.id)
        assert found is not None

    @pytest.mark.asyncio
    async def test_get_all_roles(self, db_session):
        await RoleFactory.create(db_session)
        await RoleFactory.create(db_session)
        repo = RoleRepository(db_session)
        items, total = await repo.get_paginated(0, 10)
        assert total == 2

    @pytest.mark.asyncio
    async def test_get_users_count(self, db_session):
        from tests.factories import UserFactory

        role = await RoleFactory.create(db_session)
        await UserFactory.create(db_session, role=role)
        await UserFactory.create(db_session, role=role)
        repo = RoleRepository(db_session)
        items, _ = await repo.get_paginated(0, 10)
        assert len(items) == 1


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
