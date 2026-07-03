"""Authentication and authorization FastAPI dependencies."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import API_V1_PREFIX
from app.dependencies.database import get_db
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.services.exceptions import InsufficientPermissionsError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_V1_PREFIX}/auth/login")


def get_auth_service(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> AuthService:
    return AuthService(
        session=session,
        user_repository=UserRepository(session),
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    return await auth_service.get_current_user(token)


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user


def require_role(*roles: UserRole):
    async def _check(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        user_role = UserRole(current_user.role.name)
        if user_role not in roles:
            role_names = ", ".join(r.value for r in roles)
            raise InsufficientPermissionsError(f"role: {role_names}")
        return current_user

    return _check


def require_permission(permission_name: str):
    async def _check(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        user_permissions = {rp.permission.name for rp in current_user.role.role_permissions}
        if permission_name not in user_permissions:
            raise InsufficientPermissionsError(f"permission: {permission_name}")
        return current_user

    return _check
