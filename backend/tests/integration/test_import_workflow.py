"""Integration tests for import workflow."""

import pytest

from tests.factories import ImportJobFactory, ImportJobRowResultFactory


class TestImportWorkflow:
    @pytest.mark.asyncio
    async def test_create_import_job(self, db_session):
        job = await ImportJobFactory.create(db_session)
        assert job.id is not None
        assert job.filename is not None

    @pytest.mark.asyncio
    async def test_import_job_with_row_results(self, db_session):
        job = await ImportJobFactory.create(db_session)
        r1 = await ImportJobRowResultFactory.create(db_session, import_job=job)
        r2 = await ImportJobRowResultFactory.create(db_session, import_job=job)
        assert r1.import_job_id == job.id
        assert r2.import_job_id == job.id
