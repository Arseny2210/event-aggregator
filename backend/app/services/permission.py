"""Service for managing permissions."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission
from app.repositories.permission import PermissionRepository
from app.repositories.role_permission import RolePermissionRepository
from app.services.exceptions import (
    DuplicatePermissionNameError,
    PermissionInUseError,
    PermissionNotFoundError,
)
from app.services.transaction import transactional


class PermissionService:
    """Business logic for permission management."""

    def __init__(
        self,
        session: AsyncSession,
        repository: PermissionRepository,
        role_permission_repository: RolePermissionRepository,
    ) -> None:
        self.session = session
        self.repository = repository
        self.role_permission_repository = role_permission_repository

    async def get_permission(self, permission_id: int) -> Permission:
        permission = await self.repository.get_by_id(permission_id)
        if permission is None:
            raise PermissionNotFoundError(permission_id)
        return permission

    async def get_permission_by_name(self, name: str) -> Permission:
        permission = await self.repository.get_by_name(name)
        if permission is None:
            raise PermissionNotFoundError(name)
        return permission

    async def create_permission(self, name: str, description: str | None = None) -> Permission:
        if await self.repository.get_by_name(name) is not None:
            raise DuplicatePermissionNameError(name)
        async with transactional(self.session):
            permission = Permission(name=name, description=description)
            return await self.repository.create(permission)

    async def update_permission(
        self,
        permission_id: int,
        name: str | None = None,
        description: str | None = None,
    ) -> Permission:
        permission = await self.get_permission(permission_id)
        if name is not None and name != permission.name:
            conflicting = await self.repository.get_by_name(name)
            if conflicting is not None and conflicting.id != permission.id:
                raise DuplicatePermissionNameError(name)
        async with transactional(self.session):
            if name is not None:
                permission.name = name
            if description is not None:
                permission.description = description
            return permission

    async def delete_permission(self, permission_id: int) -> None:
        permission = await self.get_permission(permission_id)
        assignments = await self.role_permission_repository.get_by_permission(permission_id)
        if assignments:
            raise PermissionInUseError(permission_id, len(assignments))
        async with transactional(self.session):
            await self.repository.delete(permission)

    async def list_permissions(self, offset: int, limit: int) -> tuple[list[Permission], int]:
        return await self.repository.get_paginated(offset, limit)
