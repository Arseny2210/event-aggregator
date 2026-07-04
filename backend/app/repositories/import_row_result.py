"""ImportJobRowResult repository."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import ImportRowStatus
from app.models.import_row_result import ImportJobRowResult
from app.repositories.base import BaseRepository


class ImportJobRowResultRepository(BaseRepository[ImportJobRowResult]):
    """Repository for ImportJobRowResult entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ImportJobRowResult)

    async def get_by_id(self, entity_id: UUID) -> ImportJobRowResult | None:
        statement = select(ImportJobRowResult).where(ImportJobRowResult.id == entity_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_multi_by_ids(self, ids: Sequence[UUID]) -> list[ImportJobRowResult]:
        statement = (
            select(ImportJobRowResult)
            .where(ImportJobRowResult.id.in_(ids))
            .order_by(ImportJobRowResult.row_number)
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_import_job(
        self,
        job_id: UUID,
        offset: int,
        limit: int,
        status: ImportRowStatus | None = None,
    ) -> tuple[list[ImportJobRowResult], int]:
        statement = select(ImportJobRowResult).where(ImportJobRowResult.import_job_id == job_id)
        count_statement = (
            select(func.count())
            .select_from(ImportJobRowResult)
            .where(ImportJobRowResult.import_job_id == job_id)
        )

        if status is not None:
            statement = statement.where(ImportJobRowResult.status == status)
            count_statement = count_statement.where(ImportJobRowResult.status == status)

        statement = statement.order_by(ImportJobRowResult.row_number).offset(offset).limit(limit)

        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total

    async def create_many(self, entities: Sequence[ImportJobRowResult]) -> list[ImportJobRowResult]:
        self.session.add_all(entities)
        await self.session.flush()
        return list(entities)

    async def delete_by_import_job(self, job_id: UUID) -> None:
        from sqlalchemy import delete as sa_delete

        statement = sa_delete(ImportJobRowResult).where(ImportJobRowResult.import_job_id == job_id)
        await self.session.execute(statement)
        await self.session.flush()
