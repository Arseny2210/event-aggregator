"""Role repository."""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from app.repositories.base import BaseRepository


class RoleRepository(BaseRepository[Role]):
    """Repository for Role entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Role)

    async def get_by_id(self, entity_id: int) -> Role | None:
        statement = select(Role).where(Role.id == entity_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_multi_by_ids(self, ids: Sequence[int]) -> list[Role]:
        statement = select(Role).where(Role.id.in_(ids)).order_by(Role.id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_name(self, name: str) -> Role | None:
        statement = select(Role).where(Role.name == name)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
