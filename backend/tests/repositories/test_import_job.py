"""Tests for ImportJobRepository."""

import pytest

from app.models.enums import ImportStatus
from app.repositories.import_job import ImportJobRepository
from tests.factories import ImportJobFactory


class TestImportJobRepository:
    @pytest.mark.asyncio
    async def test_get_by_id(self, db_session):
        job = await ImportJobFactory.create(db_session)
        repo = ImportJobRepository(db_session)
        found = await repo.get_by_id(job.id)
        assert found is not None

    @pytest.mark.asyncio
    async def test_get_by_user(self, db_session):
        job = await ImportJobFactory.create(db_session)
        repo = ImportJobRepository(db_session)
        items, total = await repo.get_by_user(job.created_by, 0, 10)
        assert total >= 1

    @pytest.mark.asyncio
    async def test_get_by_status(self, db_session):
        await ImportJobFactory.create(db_session, status=ImportStatus.processing)
        await ImportJobFactory.create(db_session, status=ImportStatus.completed)
        repo = ImportJobRepository(db_session)
        items, total = await repo.get_by_status(ImportStatus.processing, 0, 10)
        assert total == 1

    @pytest.mark.asyncio
    async def test_get_paginated(self, db_session):
        await ImportJobFactory.create(db_session)
        await ImportJobFactory.create(db_session)
        repo = ImportJobRepository(db_session)
        items, total = await repo.get_paginated(0, 10)
        assert total == 2
