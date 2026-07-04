"""Tests for UserService."""

import pytest

from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository
from app.services.exceptions import UserNotFoundError
from app.services.user import UserService
from tests.factories import UserFactory


class TestUserService:
    @pytest.mark.asyncio
    async def test_get_user(self, db_session):
        user = await UserFactory.create(db_session)
        svc = UserService(
            session=db_session,
            repository=UserRepository(db_session),
            role_repository=RoleRepository(db_session),
        )
        found = await svc.get_user(user.id)
        assert found.id == user.id

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, db_session):
        from uuid import uuid4

        svc = UserService(
            session=db_session,
            repository=UserRepository(db_session),
            role_repository=RoleRepository(db_session),
        )
        with pytest.raises(UserNotFoundError):
            await svc.get_user(uuid4())

    @pytest.mark.asyncio
    async def test_list_users(self, db_session):
        await UserFactory.create(db_session)
        await UserFactory.create(db_session)
        svc = UserService(
            session=db_session,
            repository=UserRepository(db_session),
            role_repository=RoleRepository(db_session),
        )
        items, total = await svc.list_users(0, 10)
        assert total == 2
