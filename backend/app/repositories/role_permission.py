"""RolePermission repository."""

from collections.abc import Sequence

from sqlalchemy import delete as sql_delete
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role_permission import RolePermission
from app.repositories.base import BaseRepository


class RolePermissionRepository(BaseRepository[RolePermission]):
    """Repository for RolePermission entities (composite PK)."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, RolePermission)

    async def get_by_id(self, entity_id: tuple[int, int]) -> RolePermission | None:
        role_id, permission_id = entity_id
        statement = select(RolePermission).where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id,
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_role(self, role_id: int) -> list[RolePermission]:
        statement = select(RolePermission).where(RolePermission.role_id == role_id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_permission(self, permission_id: int) -> list[RolePermission]:
        statement = select(RolePermission).where(RolePermission.permission_id == permission_id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_multi_by_ids(self, ids: Sequence[tuple[int, int]]) -> list[RolePermission]:
        conditions = [
            (RolePermission.role_id == rid) & (RolePermission.permission_id == pid)
            for rid, pid in ids
        ]
        statement = select(RolePermission).where(or_(*conditions)).order_by(RolePermission.role_id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def delete_by_role(self, role_id: int) -> None:
        stmt = sql_delete(RolePermission).where(RolePermission.role_id == role_id)
        await self.session.execute(stmt)
