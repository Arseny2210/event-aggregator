"""Event repository."""

from collections.abc import Sequence
from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import EventStatus
from app.models.event import Event
from app.repositories.base import BaseRepository


class EventRepository(BaseRepository[Event]):
    """Repository for Event entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Event)

    async def get_by_id(self, entity_id: UUID) -> Event | None:
        statement = select(Event).where(Event.id == entity_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_multi_by_ids(self, ids: Sequence[UUID]) -> list[Event]:
        statement = select(Event).where(Event.id.in_(ids)).order_by(Event.id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_organizer(
        self, organizer_id: UUID, offset: int, limit: int
    ) -> tuple[list[Event], int]:
        statement = (
            select(Event)
            .where(Event.organizer_id == organizer_id)
            .order_by(Event.start_date.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_statement = (
            select(func.count()).select_from(Event).where(Event.organizer_id == organizer_id)
        )
        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total

    async def get_by_status(
        self, status: EventStatus, offset: int, limit: int
    ) -> tuple[list[Event], int]:
        statement = (
            select(Event)
            .where(Event.status == status)
            .order_by(Event.start_date.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_statement = select(func.count()).select_from(Event).where(Event.status == status)
        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total

    async def get_by_date_range(
        self, start: date, end: date, offset: int, limit: int
    ) -> tuple[list[Event], int]:
        statement = (
            select(Event)
            .where(Event.start_date.between(start, end))
            .order_by(Event.start_date.asc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_statement = (
            select(func.count()).select_from(Event).where(Event.start_date.between(start, end))
        )
        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total

    async def search_by_title(self, query: str, offset: int, limit: int) -> tuple[list[Event], int]:
        escaped_query = query.replace("%", r"\%").replace("_", r"\_")

        statement = (
            select(Event)
            .where(Event.title.ilike(f"%{escaped_query}%"))
            .order_by(Event.start_date.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_statement = (
            select(func.count()).select_from(Event).where(Event.title.ilike(f"%{escaped_query}%"))
        )
        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total
