"""Participation repository."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.participation import Participation
from app.repositories.base import BaseRepository


class ParticipationRepository(BaseRepository[Participation]):
    """Repository for Participation entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Participation)

    async def get_by_id(self, entity_id: UUID) -> Participation | None:
        statement = select(Participation).where(Participation.id == entity_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_multi_by_ids(self, ids: Sequence[UUID]) -> list[Participation]:
        statement = (
            select(Participation).where(Participation.id.in_(ids)).order_by(Participation.id)
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_event(
        self, event_id: UUID, offset: int, limit: int
    ) -> tuple[list[Participation], int]:
        statement = (
            select(Participation)
            .where(Participation.event_id == event_id)
            .order_by(Participation.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_statement = (
            select(func.count())
            .select_from(Participation)
            .where(Participation.event_id == event_id)
        )
        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total

    async def get_by_session(self, session_id: str) -> list[Participation]:
        statement = (
            select(Participation)
            .where(Participation.session_id == session_id)
            .order_by(Participation.created_at.desc())
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_event_and_session(
        self, event_id: UUID, session_id: str
    ) -> Participation | None:
        statement = select(Participation).where(
            Participation.event_id == event_id,
            Participation.session_id == session_id,
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def count_by_event(self, event_id: UUID) -> int:
        statement = (
            select(func.count())
            .select_from(Participation)
            .where(Participation.event_id == event_id)
        )
        result = await self.session.execute(statement)
        return result.scalar_one()
