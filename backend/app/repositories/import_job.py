"""ImportJob repository."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import ImportStatus
from app.models.import_job import ImportJob
from app.repositories.base import BaseRepository


class ImportJobRepository(BaseRepository[ImportJob]):
    """Repository for ImportJob entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ImportJob)

    async def get_by_id(self, entity_id: UUID) -> ImportJob | None:
        statement = select(ImportJob).where(ImportJob.id == entity_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_multi_by_ids(self, ids: Sequence[UUID]) -> list[ImportJob]:
        statement = select(ImportJob).where(ImportJob.id.in_(ids)).order_by(ImportJob.id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_user(
        self, user_id: UUID, offset: int, limit: int
    ) -> tuple[list[ImportJob], int]:
        statement = (
            select(ImportJob)
            .where(ImportJob.created_by == user_id)
            .order_by(ImportJob.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_statement = (
            select(func.count()).select_from(ImportJob).where(ImportJob.created_by == user_id)
        )
        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total

    async def get_by_status(
        self, status: ImportStatus, offset: int, limit: int
    ) -> tuple[list[ImportJob], int]:
        statement = (
            select(ImportJob)
            .where(ImportJob.status == status)
            .order_by(ImportJob.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_statement = (
            select(func.count()).select_from(ImportJob).where(ImportJob.status == status)
        )
        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total
