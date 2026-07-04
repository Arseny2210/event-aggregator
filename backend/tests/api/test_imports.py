"""API tests for import endpoints."""

import pytest

from tests.factories import ImportJobFactory


class TestImportAPI:
    @pytest.mark.asyncio
    async def test_list_imports_requires_auth(self, async_client):
        response = await async_client.get("/api/v1/imports/")
        assert response.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_list_imports_as_admin(self, admin_client, db_session):
        await ImportJobFactory.create(db_session)
        response = await admin_client.get("/api/v1/imports/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    @pytest.mark.asyncio
    async def test_get_import_by_id(self, admin_client, db_session):
        job = await ImportJobFactory.create(db_session)
        response = await admin_client.get(f"/api/v1/imports/{job.id}")
        assert response.status_code == 200
