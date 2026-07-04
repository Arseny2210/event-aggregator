"""API tests for dashboard endpoints."""

import pytest

from tests.factories import EventFactory


class TestDashboardAPI:
    @pytest.mark.asyncio
    async def test_dashboard_requires_auth(self, async_client):
        response = await async_client.get("/api/v1/dashboard/")
        assert response.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_dashboard_as_admin(self, admin_client):
        response = await admin_client.get("/api/v1/dashboard/")
        assert response.status_code == 200
        data = response.json()
        assert "events" in data
        assert "organizers" in data
        assert "users" in data

    @pytest.mark.asyncio
    async def test_dashboard_events(self, admin_client, db_session):
        await EventFactory.create(db_session)
        response = await admin_client.get("/api/v1/dashboard/events")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    @pytest.mark.asyncio
    async def test_dashboard_charts(self, admin_client, db_session):
        await EventFactory.create(db_session)
        response = await admin_client.get("/api/v1/dashboard/charts")
        assert response.status_code == 200
        data = response.json()
        assert "events_per_day" in data
        assert "events_by_status" in data
