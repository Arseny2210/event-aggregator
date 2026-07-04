"""Integration tests for auth flow."""

import pytest


class TestAuthFlow:
    @pytest.mark.asyncio
    async def test_health_endpoint(self, async_client):
        response = await async_client.get("/api/v1/health")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_protected_route_requires_auth(self, async_client):
        response = await async_client.post("/api/v1/events/", json={})
        assert response.status_code in (401, 403)
