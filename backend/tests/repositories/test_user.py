"""Tests for UserRepository."""

import pytest

from app.repositories.user import UserRepository
from tests.factories import UserFactory


class TestUserRepository:
    @pytest.mark.asyncio
    async def test_get_by_username(self, db_session):
        await UserFactory.create(db_session, username="johndoe")
        repo = UserRepository(db_session)
        found = await repo.get_by_username("johndoe")
        assert found is not None
        assert found.username == "johndoe"

    @pytest.mark.asyncio
    async def test_get_by_username_not_found(self, db_session):
        repo = UserRepository(db_session)
        found = await repo.get_by_username("nonexistent")
        assert found is None

    @pytest.mark.asyncio
    async def test_get_by_email(self, db_session):
        await UserFactory.create(db_session, email="john@test.com")
        repo = UserRepository(db_session)
        found = await repo.get_by_email("john@test.com")
        assert found is not None

    @pytest.mark.asyncio
    async def test_get_by_email_not_found(self, db_session):
        repo = UserRepository(db_session)
        found = await repo.get_by_email("no@test.com")
        assert found is None

    @pytest.mark.asyncio
    async def test_get_paginated(self, db_session):
        await UserFactory.create(db_session)
        await UserFactory.create(db_session)
        repo = UserRepository(db_session)
        items, total = await repo.get_paginated(0, 10)
        assert total == 2
