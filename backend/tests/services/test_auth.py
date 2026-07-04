"""Tests for AuthService."""

import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.role import Role
from app.models.user import User
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.services.exceptions import InvalidCredentialsError
from tests.factories import RoleFactory, UserFactory


class TestAuthService:
    @pytest.mark.asyncio
    async def test_login_success(self, db_session):
        user = await UserFactory.create(db_session, username="loginuser", password="testpass123")
        await db_session.refresh(user)
        svc = AuthService(
            session=db_session,
            user_repository=UserRepository(db_session),
        )
        result = await svc.login("loginuser", "testpass123")
        assert result is not None
        assert result.user.id == user.id

    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, db_session):
        svc = AuthService(
            session=db_session,
            user_repository=UserRepository(db_session),
        )
        with pytest.raises(InvalidCredentialsError):
            await svc.login("nobody", "wrongpass")

    @pytest.mark.asyncio
    async def test_refresh_token(self, db_session):
        await UserFactory.create(db_session, username="refreshuser")
        svc = AuthService(
            session=db_session,
            user_repository=UserRepository(db_session),
        )
        result = await svc.login("refreshuser", "testpass123")
        assert result is not None

    @pytest.mark.asyncio
    async def test_me_response(self, db_session):
        role = await RoleFactory.create(db_session, name="me_role")
        user = await UserFactory.create(db_session, username="meuser", role=role)
        stmt = (
            select(User)
            .where(User.id == user.id)
            .options(selectinload(User.role).selectinload(Role.role_permissions))
        )
        result = await db_session.execute(stmt)
        loaded_user = result.scalar_one()
        svc = AuthService(
            session=db_session,
            user_repository=UserRepository(db_session),
        )
        me = svc.build_me_response(loaded_user)
        assert me.username == user.username
