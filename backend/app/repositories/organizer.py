"""Organizer repository."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organizer import Organizer
from app.repositories.base import BaseRepository


class OrganizerRepository(BaseRepository[Organizer]):
    """Repository for Organizer entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Organizer)

    async def get_by_id(self, entity_id: UUID) -> Organizer | None:
        statement = select(Organizer).where(Organizer.id == entity_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_multi_by_ids(self, ids: Sequence[UUID]) -> list[Organizer]:
        statement = select(Organizer).where(Organizer.id.in_(ids)).order_by(Organizer.id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_name(self, name: str) -> Organizer | None:
        statement = select(Organizer).where(Organizer.name == name)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def search_by_name(
        self, query: str, offset: int, limit: int
    ) -> tuple[list[Organizer], int]:
        escaped_query = query.replace("%", r"\%").replace("_", r"\_")

        statement = (
            select(Organizer)
            .where(Organizer.name.ilike(f"%{escaped_query}%"))
            .order_by(Organizer.name)
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_statement = (
            select(func.count())
            .select_from(Organizer)
            .where(Organizer.name.ilike(f"%{escaped_query}%"))
        )
        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total
