"""Event repository."""

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement

from app.models.enums import EventStatus
from app.models.event import Event
from app.models.organizer import Organizer
from app.repositories.base import BaseRepository
from app.schemas.event_search import EventSearchFilters, EventSort


@dataclass(frozen=True, slots=True)
class EventSearchResult:
    items: list[Event]
    total: int


_SORT_MAP: dict[EventSort, ColumnElement[Any]] = {
    EventSort.DATE_ASC: Event.start_date.asc(),
    EventSort.DATE_DESC: Event.start_date.desc(),
    EventSort.TITLE_ASC: Event.title.asc(),
    EventSort.TITLE_DESC: Event.title.desc(),
    EventSort.CREATED_AT_ASC: Event.created_at.asc(),
    EventSort.CREATED_AT_DESC: Event.created_at.desc(),
    EventSort.UPDATED_AT_ASC: Event.updated_at.asc(),
    EventSort.UPDATED_AT_DESC: Event.updated_at.desc(),
}


class EventRepository(BaseRepository[Event]):
    """Repository for Event entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Event)

    @staticmethod
    def _escape_like(value: str) -> str:
        return value.replace("%", r"\%").replace("_", r"\_")

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
        self, start_date: date, end_date: date, offset: int, limit: int
    ) -> tuple[list[Event], int]:
        statement = (
            select(Event)
            .where(Event.start_date.between(start_date, end_date))
            .order_by(Event.start_date)
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_statement = (
            select(func.count())
            .select_from(Event)
            .where(Event.start_date.between(start_date, end_date))
        )
        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total

    async def search_by_title(self, query: str, offset: int, limit: int) -> tuple[list[Event], int]:
        escaped = self._escape_like(query)
        like_pattern = f"%{escaped}%"

        where_clause = (
            Event.title.ilike(like_pattern)
            | Event.description.ilike(like_pattern)
            | Event.short_description.ilike(like_pattern)
            | Event.location.ilike(like_pattern)
        )

        statement = (
            select(Event).where(where_clause).order_by(Event.title).offset(offset).limit(limit)
        )
        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_statement = select(func.count()).select_from(Event).where(where_clause)
        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total

    async def search(
        self, filters: EventSearchFilters, offset: int, limit: int
    ) -> EventSearchResult:
        base = select(Event)
        conditions: list[ColumnElement[bool]] = []

        if filters.search:
            escaped = self._escape_like(filters.search)
            like_pattern = f"%{escaped}%"
            conditions.append(
                Event.title.ilike(like_pattern)
                | Event.description.ilike(like_pattern)
                | Event.short_description.ilike(like_pattern)
                | Event.location.ilike(like_pattern)
            )
        if filters.status is not None:
            conditions.append(Event.status == filters.status)
        if filters.organizer_id is not None:
            conditions.append(Event.organizer_id == filters.organizer_id)
        if filters.category_id is not None:
            conditions.append(Event.category_id == filters.category_id)
        if filters.date_from is not None:
            conditions.append(Event.start_date >= filters.date_from)
        if filters.date_to is not None:
            conditions.append(Event.start_date <= filters.date_to)

        if filters.organizer_name is not None:
            base = base.join(Organizer, Event.organizer_id == Organizer.id)
            conditions.append(
                Organizer.name.ilike(f"%{self._escape_like(filters.organizer_name)}%")
            )

        if conditions:
            base = base.where(*conditions)

        count_stmt = select(func.count()).select_from(base.subquery())
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar_one()

        sort_clause = _SORT_MAP[filters.sort]
        paginated = base.order_by(sort_clause, Event.id).offset(offset).limit(limit)
        result = await self.session.execute(paginated)
        items = list(result.scalars().all())

        return EventSearchResult(items=items, total=total)
