"""API tests for authentication endpoints."""

import pytest


class TestAuthAPI:
    @pytest.mark.asyncio
    async def test_login_invalid(self, async_client):
        response = await async_client.post(
            "/api/v1/auth/login",
            json={
                "username": "noone",
                "password": "wrong",
            },
        )
        assert response.status_code in (400, 401, 422)

    @pytest.mark.asyncio
    async def test_me_requires_auth(self, async_client):
        response = await async_client.get("/api/v1/auth/me")
        assert response.status_code in (401, 403)
