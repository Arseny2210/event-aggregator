"""RolePermission repository.

RolePermission uses a composite primary key (role_id, permission_id)
and overrides get_by_id with a two-argument signature.
Bulk deletion uses SQLAlchemy 2.0 DML for maximum performance.
"""

from collections.abc import Sequence

from sqlalchemy import delete as sa_delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role_permission import RolePermission
from app.repositories.base import BaseRepository


class RolePermissionRepository(BaseRepository[RolePermission]):
    """Repository for RolePermission junction table entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, RolePermission)

    async def get_by_id(self, role_id: int, permission_id: int) -> RolePermission | None:
        statement = select(RolePermission).where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id,
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create_many(self, entities: Sequence[RolePermission]) -> list[RolePermission]:
        self.session.add_all(entities)
        await self.session.flush()
        return list(entities)

    async def delete_many(self, entities: Sequence[RolePermission]) -> None:
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()

    async def get_by_role(self, role_id: int) -> list[RolePermission]:
        statement = (
            select(RolePermission)
            .where(RolePermission.role_id == role_id)
            .order_by(RolePermission.permission_id)
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_permission(self, permission_id: int) -> list[RolePermission]:
        statement = (
            select(RolePermission)
            .where(RolePermission.permission_id == permission_id)
            .order_by(RolePermission.role_id)
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def delete_by_role(self, role_id: int) -> None:
        statement = sa_delete(RolePermission).where(RolePermission.role_id == role_id)
        await self.session.execute(statement)
