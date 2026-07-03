"""Authentication and authorization service."""

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

import jwt as pyjwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import UserMeResponse
from app.services.exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
    TokenExpiredError,
    UserInactiveError,
    UserNotFoundError,
)
from app.services.transaction import transactional


@dataclass(frozen=True, slots=True)
class LoginResult:
    user: User
    access_token: str
    refresh_token: str


@dataclass(frozen=True, slots=True)
class RefreshResult:
    access_token: str
    refresh_token: str


class AuthService:
    """Business logic for authentication and authorization."""

    def __init__(
        self,
        session: AsyncSession,
        user_repository: UserRepository,
    ) -> None:
        self.session = session
        self.user_repository = user_repository

    async def authenticate(self, username: str, password: str) -> User:
        user = await self.user_repository.get_by_username(username)
        if user is None:
            raise InvalidCredentialsError()
        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        return user

    async def login(self, username: str, password: str) -> LoginResult:
        user = await self.authenticate(username, password)
        if not user.is_active:
            raise UserInactiveError(user.id)
        async with transactional(self.session):
            user.last_login = datetime.now(UTC)
        return LoginResult(
            user=user,
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def refresh_access_token(self, refresh_token: str) -> RefreshResult:
        try:
            payload = decode_token(refresh_token)
        except pyjwt.ExpiredSignatureError as exc:
            raise TokenExpiredError() from exc
        except pyjwt.InvalidTokenError as exc:
            raise InvalidTokenError("Invalid refresh token") from exc
        if payload.type != "refresh":
            raise InvalidTokenError("Expected refresh token")
        user_id = UUID(payload.sub)
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        if not user.is_active:
            raise UserInactiveError(user_id)
        return RefreshResult(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def get_current_user(self, access_token: str) -> User:
        try:
            payload = decode_token(access_token)
        except pyjwt.ExpiredSignatureError as exc:
            raise TokenExpiredError() from exc
        except pyjwt.InvalidTokenError as exc:
            raise InvalidTokenError("Invalid access token") from exc
        if payload.type != "access":
            raise InvalidTokenError("Expected access token")
        user_id = UUID(payload.sub)
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        if not user.is_active:
            raise UserInactiveError(user_id)
        return user

    @staticmethod
    def build_me_response(user: User) -> UserMeResponse:
        permissions = [rp.permission.name for rp in user.role.role_permissions]
        return UserMeResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role_id=user.role_id,
            is_active=user.is_active,
            last_login=user.last_login,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role_name=user.role.name,
            permissions=permissions,
        )
