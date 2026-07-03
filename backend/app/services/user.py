"""Service for managing users."""

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.exceptions import (
    DuplicateEmailError,
    DuplicateUsernameError,
    RoleNotFoundError,
    UserNotFoundError,
)
from app.services.transaction import transactional


class UserService:
    """Business logic for user management."""

    def __init__(
        self,
        session: AsyncSession,
        repository: UserRepository,
        role_repository: RoleRepository,
    ) -> None:
        self.session = session
        self.repository = repository
        self.role_repository = role_repository

    async def get_user(self, user_id: UUID) -> User:
        user = await self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user

    async def get_user_by_username(self, username: str) -> User:
        user = await self.repository.get_by_username(username)
        if user is None:
            raise UserNotFoundError(username)
        return user

    async def get_user_by_email(self, email: str) -> User:
        user = await self.repository.get_by_email(email)
        if user is None:
            raise UserNotFoundError(email)
        return user

    async def create_user(self, data: UserCreate, password_hash: str) -> User:
        if not password_hash:
            raise ValueError("password_hash is required to create a user")
        if await self.repository.get_by_username(data.username) is not None:
            raise DuplicateUsernameError(data.username)
        if await self.repository.get_by_email(data.email) is not None:
            raise DuplicateEmailError(data.email)
        if await self.role_repository.get_by_id(data.role_id) is None:
            raise RoleNotFoundError(data.role_id)
        async with transactional(self.session):
            user = User(
                username=data.username,
                email=data.email,
                password_hash=password_hash,
                role_id=data.role_id,
                is_active=True,
            )
            return await self.repository.create(user)

    async def update_user(
        self,
        user_id: UUID,
        data: UserUpdate,
        password_hash: str | None = None,
    ) -> User:
        user = await self.get_user(user_id)
        payload = data.model_dump(exclude_unset=True)
        if "password" in payload and password_hash is None:
            raise ValueError("password_hash is required when password is updated")
        if (
            "username" in payload
            and payload["username"] != user.username
            and await self.repository.get_by_username(payload["username"]) is not None
        ):
            raise DuplicateUsernameError(payload["username"])
        if (
            "email" in payload
            and payload["email"] != user.email
            and await self.repository.get_by_email(payload["email"]) is not None
        ):
            raise DuplicateEmailError(payload["email"])
        if (
            "role_id" in payload
            and payload["role_id"] is not None
            and await self.role_repository.get_by_id(payload["role_id"]) is None
        ):
            raise RoleNotFoundError(payload["role_id"])
        if password_hash is not None and not password_hash:
            raise ValueError("password_hash must not be empty")
        async with transactional(self.session):
            if password_hash is not None:
                user.password_hash = password_hash
            for field, value in payload.items():
                if field == "password":
                    continue
                setattr(user, field, value)
            return user

    async def delete_user(self, user_id: UUID) -> None:
        user = await self.get_user(user_id)
        async with transactional(self.session):
            await self.repository.delete(user)

    async def list_users(self, offset: int, limit: int) -> tuple[list[User], int]:
        return await self.repository.get_paginated(offset, limit)

    async def list_active_users(self, offset: int, limit: int) -> tuple[list[User], int]:
        return await self.repository.get_active_users(offset, limit)

    async def list_users_by_role(
        self, role_id: int, offset: int, limit: int
    ) -> tuple[list[User], int]:
        return await self.repository.get_by_role(role_id, offset, limit)

    async def update_last_login(self, user_id: UUID) -> User:
        user = await self.get_user(user_id)
        async with transactional(self.session):
            user.last_login = datetime.now(UTC)
            return user
