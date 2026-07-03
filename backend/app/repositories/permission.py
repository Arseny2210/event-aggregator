"""Permission repository."""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.repositories.base import BaseRepository


class PermissionRepository(BaseRepository[Permission]):
    """Repository for Permission entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Permission)

    async def get_by_id(self, entity_id: int) -> Permission | None:
        statement = select(Permission).where(Permission.id == entity_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_multi_by_ids(self, ids: Sequence[int]) -> list[Permission]:
        statement = select(Permission).where(Permission.id.in_(ids)).order_by(Permission.id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_name(self, name: str) -> Permission | None:
        statement = select(Permission).where(Permission.name == name)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_role(self, role_id: int) -> list[Permission]:
        statement = (
            select(Permission)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .where(RolePermission.role_id == role_id)
            .order_by(Permission.name)
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())
