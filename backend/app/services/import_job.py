"""Service for managing Excel import job records and orchestration."""

import uuid as _uuid
from logging import getLogger
from pathlib import Path
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.config import settings
from app.core.storage import StorageBackend
from app.core.tasks import BackgroundTaskDispatcher
from app.models.enums import ImportRowStatus, ImportStatus
from app.models.import_job import ImportJob
from app.models.import_row_result import ImportJobRowResult
from app.models.user import User
from app.repositories.import_job import ImportJobRepository
from app.repositories.import_row_result import ImportJobRowResultRepository
from app.services.exceptions import (
    EmptyFileError,
    FileTooLargeError,
    ImportJobNotFoundError,
    InvalidFileFormatError,
    InvalidImportStatusTransitionError,
)
from app.services.import_processor import ImportProcessor
from app.services.transaction import transactional

logger = getLogger(__name__)

_ALLOWED_IMPORT_TRANSITIONS: dict[ImportStatus, frozenset[ImportStatus]] = {
    ImportStatus.processing: frozenset({ImportStatus.completed, ImportStatus.failed}),
    ImportStatus.completed: frozenset(),
    ImportStatus.failed: frozenset(),
}

_ALLOWED_EXTENSIONS: frozenset[str] = frozenset({".xlsx", ".xls"})


class ImportJobService:
    """Business logic for import job history, file upload, and status management."""

    def __init__(
        self,
        session: AsyncSession,
        repository: ImportJobRepository,
        row_result_repository: ImportJobRowResultRepository,
        storage: StorageBackend,
        dispatcher: BackgroundTaskDispatcher,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self.session = session
        self.repository = repository
        self.row_result_repository = row_result_repository
        self.storage = storage
        self.dispatcher = dispatcher
        self.session_factory = session_factory

    async def upload_file(self, filename: str, content: bytes, user: User) -> ImportJob:
        ext = Path(filename).suffix.lower()
        if ext not in _ALLOWED_EXTENSIONS:
            raise InvalidFileFormatError(ext)
        if not content:
            raise EmptyFileError()
        if len(content) > settings.max_upload_size_bytes:
            raise FileTooLargeError(len(content), settings.max_upload_size_bytes)

        safe_name = f"{_uuid.uuid4().hex}_{_sanitize(filename)}"
        file_path = await self.storage.save(safe_name, content)

        async with transactional(self.session):
            job = ImportJob(
                filename=filename,
                created_by=user.id,
                status=ImportStatus.processing,
                file_path=str(file_path),
            )
            created = await self.repository.create(job)

        processor = ImportProcessor(self.session_factory)
        self.dispatcher.dispatch(processor.process(created.id, file_path, user.id))

        logger.info(
            "Import job %s created by user %s for file %s",
            created.id,
            user.id,
            filename,
        )
        return created

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
        if job.file_path:
            try:
                file_key = Path(job.file_path).name
                await self.storage.delete(file_key)
            except Exception:
                pass

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

    async def list_row_results(
        self,
        job_id: UUID,
        offset: int,
        limit: int,
        status: ImportRowStatus | None = None,
    ) -> tuple[list[ImportJobRowResult], int]:
        await self.get_import_job(job_id)
        return await self.row_result_repository.get_by_import_job(
            job_id,
            offset,
            limit,
            status,
        )


def _sanitize(filename: str) -> str:
    return Path(filename).name.replace(" ", "_")
