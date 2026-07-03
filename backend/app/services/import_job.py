"""Service for managing Excel import job records."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import ImportStatus
from app.models.import_job import ImportJob
from app.repositories.import_job import ImportJobRepository
from app.services.exceptions import (
    ImportJobNotFoundError,
    InvalidImportStatusTransitionError,
)
from app.services.transaction import transactional

_ALLOWED_IMPORT_TRANSITIONS: dict[ImportStatus, frozenset[ImportStatus]] = {
    ImportStatus.processing: frozenset({ImportStatus.completed, ImportStatus.failed}),
    ImportStatus.completed: frozenset(),
    ImportStatus.failed: frozenset(),
}


class ImportJobService:
    """Business logic for import job history and status management."""

    def __init__(
        self,
        session: AsyncSession,
        repository: ImportJobRepository,
    ) -> None:
        self.session = session
        self.repository = repository

    async def get_import_job(self, import_job_id: UUID) -> ImportJob:
        job = await self.repository.get_by_id(import_job_id)
        if job is None:
            raise ImportJobNotFoundError(import_job_id)
        return job

    async def create_import_job(self, filename: str, created_by: UUID) -> ImportJob:
        async with transactional(self.session):
            job = ImportJob(
                filename=filename,
                created_by=created_by,
                status=ImportStatus.processing,
            )
            return await self.repository.create(job)

    async def update_import_job_status(
        self,
        import_job_id: UUID,
        status: ImportStatus,
        imported_rows: int = 0,
        failed_rows: int = 0,
        duration: int = 0,
    ) -> ImportJob:
        job = await self.get_import_job(import_job_id)
        allowed = _ALLOWED_IMPORT_TRANSITIONS.get(job.status, frozenset())
        if status not in allowed:
            raise InvalidImportStatusTransitionError(job.status, status)
        async with transactional(self.session):
            job.status = status
            job.imported_rows = imported_rows
            job.failed_rows = failed_rows
            job.duration = duration
            return job

    async def delete_import_job(self, import_job_id: UUID) -> None:
        job = await self.get_import_job(import_job_id)
        async with transactional(self.session):
            await self.repository.delete(job)

    async def list_import_jobs(self, offset: int, limit: int) -> tuple[list[ImportJob], int]:
        return await self.repository.get_paginated(offset, limit)

    async def list_import_jobs_by_user(
        self, user_id: UUID, offset: int, limit: int
    ) -> tuple[list[ImportJob], int]:
        return await self.repository.get_by_user(user_id, offset, limit)

    async def list_import_jobs_by_status(
        self, status: ImportStatus, offset: int, limit: int
    ) -> tuple[list[ImportJob], int]:
        return await self.repository.get_by_status(status, offset, limit)
