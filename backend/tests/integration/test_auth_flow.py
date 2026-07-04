"""Integration tests for auth flow."""

import pytest

from app.repositories.user import UserRepository
from tests.factories import RoleFactory, UserFactory


class TestAuthFlow:
    @pytest.mark.asyncio
    async def test_user_creation_and_retrieval(self, db_session):
        role = await RoleFactory.create(db_session)
        user = await UserFactory.create(
            db_session,
            username="flowuser",
            role=role,
        )
        repo = UserRepository(db_session)
        found = await repo.get_by_username("flowuser")
        assert found is not None
        assert found.id == user.id

    @pytest.mark.asyncio
    async def test_user_role_assignment(self, db_session):
        role = await RoleFactory.create(db_session, name="flowrole")
        user = await UserFactory.create(db_session, role=role)
        assert user.role.name == "flowrole"
