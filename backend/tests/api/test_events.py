"""API tests for event endpoints."""

from uuid import uuid4

import pytest

from app.models.enums import EventStatus
from tests.factories import EventFactory


class TestEventAPI:
    @pytest.mark.asyncio
    async def test_list_events_public(self, async_client, db_session):
        await EventFactory.create(db_session, status=EventStatus.draft)
        await EventFactory.create(db_session, status=EventStatus.published)
        await db_session.commit()
        response = await async_client.get("/api/v1/events/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 2

    @pytest.mark.asyncio
    async def test_list_events_with_status_filter(self, async_client, db_session):
        await EventFactory.create(db_session, status=EventStatus.draft)
        await db_session.commit()
        response = await async_client.get("/api/v1/events/?status=draft")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    @pytest.mark.asyncio
    async def test_get_event_by_id(self, async_client, db_session):
        event = await EventFactory.create(db_session, title="Public Event")
        await db_session.commit()
        response = await async_client.get(f"/api/v1/events/{event.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Public Event"

    @pytest.mark.asyncio
    async def test_get_event_not_found(self, async_client):
        response = await async_client.get(f"/api/v1/events/{uuid4()}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_create_event_requires_auth(self, async_client):
        response = await async_client.post(
            "/api/v1/events/",
            json={
                "title": "No Auth",
                "description": "Test",
            },
        )
        assert response.status_code in (401, 403)
