"""Tests for ImportJobRowResultRepository."""

import pytest

from app.repositories.import_row_result import ImportJobRowResultRepository
from tests.factories import ImportJobFactory, ImportJobRowResultFactory


class TestImportJobRowResultRepository:
    @pytest.mark.asyncio
    async def test_get_by_import_job(self, db_session):
        job = await ImportJobFactory.create(db_session)
        await ImportJobRowResultFactory.create(db_session, import_job=job)
        await ImportJobRowResultFactory.create(db_session, import_job=job)
        repo = ImportJobRowResultRepository(db_session)
        items, total = await repo.get_by_import_job(job.id, 0, 10)
        assert total == 2

    @pytest.mark.asyncio
    async def test_get_by_id(self, db_session):
        row = await ImportJobRowResultFactory.create(db_session)
        repo = ImportJobRowResultRepository(db_session)
        found = await repo.get_by_id(row.id)
        assert found is not None
