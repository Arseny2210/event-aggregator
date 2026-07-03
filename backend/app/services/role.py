"""Service for managing roles and their permission assignments."""

from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.repositories.permission import PermissionRepository
from app.repositories.role import RoleRepository
from app.repositories.role_permission import RolePermissionRepository
from app.repositories.user import UserRepository
from app.services.exceptions import (
    DuplicateRoleNameError,
    PermissionNotFoundError,
    RoleInUseError,
    RoleNotFoundError,
)
from app.services.transaction import transactional


class RoleService:
    """Business logic for role and permission assignment management."""

    def __init__(
        self,
        session: AsyncSession,
        repository: RoleRepository,
        role_permission_repository: RolePermissionRepository,
        permission_repository: PermissionRepository,
        user_repository: UserRepository,
    ) -> None:
        self.session = session
        self.repository = repository
        self.role_permission_repository = role_permission_repository
        self.permission_repository = permission_repository
        self.user_repository = user_repository

    async def get_role(self, role_id: int) -> Role:
        role = await self.repository.get_by_id(role_id)
        if role is None:
            raise RoleNotFoundError(role_id)
        return role

    async def get_role_by_name(self, name: str) -> Role:
        role = await self.repository.get_by_name(name)
        if role is None:
            raise RoleNotFoundError(name)
        return role

    async def create_role(self, name: str, description: str | None = None) -> Role:
        if await self.repository.get_by_name(name) is not None:
            raise DuplicateRoleNameError(name)
        async with transactional(self.session):
            role = Role(name=name, description=description)
            return await self.repository.create(role)

    async def update_role(
        self,
        role_id: int,
        name: str | None = None,
        description: str | None = None,
    ) -> Role:
        role = await self.get_role(role_id)
        if name is not None and name != role.name:
            conflicting = await self.repository.get_by_name(name)
            if conflicting is not None and conflicting.id != role.id:
                raise DuplicateRoleNameError(name)
        async with transactional(self.session):
            if name is not None:
                role.name = name
            if description is not None:
                role.description = description
            return role

    async def delete_role(self, role_id: int) -> None:
        role = await self.get_role(role_id)
        _, total = await self.user_repository.get_by_role(role_id, 0, 1)
        if total > 0:
            raise RoleInUseError(role_id, total)
        async with transactional(self.session):
            await self.repository.delete(role)

    async def list_roles(self, offset: int, limit: int) -> tuple[list[Role], int]:
        return await self.repository.get_paginated(offset, limit)

    async def assign_permissions(
        self, role_id: int, permission_ids: Sequence[int]
    ) -> list[RolePermission]:
        role = await self.get_role(role_id)
        existing = await self.role_permission_repository.get_by_role(role_id)
        existing_ids = {rp.permission_id for rp in existing}
        to_create: list[RolePermission] = []
        for pid in permission_ids:
            if pid in existing_ids:
                continue
            permission = await self.permission_repository.get_by_id(pid)
            if permission is None:
                raise PermissionNotFoundError(pid)
            to_create.append(RolePermission(role_id=role.id, permission_id=permission.id))
        if not to_create:
            return []
        async with transactional(self.session):
            return await self.role_permission_repository.create_many(to_create)

    async def revoke_permissions(self, role_id: int, permission_ids: Sequence[int]) -> None:
        await self.get_role(role_id)
        existing = await self.role_permission_repository.get_by_role(role_id)
        target_ids = set(permission_ids)
        to_delete = [rp for rp in existing if rp.permission_id in target_ids]
        if not to_delete:
            return
        async with transactional(self.session):
            await self.role_permission_repository.delete_many(to_delete)

    async def get_permissions_for_role(self, role_id: int) -> list[Permission]:
        await self.get_role(role_id)
        return await self.permission_repository.get_by_role(role_id)
