"""API tests for notification endpoints."""

import pytest

from app.models.enums import NotificationTemplateType
from tests.factories import NotificationFactory, NotificationTemplateFactory


class TestNotificationAPI:
    @pytest.mark.asyncio
    async def test_list_notifications_requires_auth(self, async_client):
        response = await async_client.get("/api/v1/notifications/")
        assert response.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_list_notifications_as_admin(self, admin_client, db_session):
        await NotificationFactory.create(db_session)
        response = await admin_client.get("/api/v1/notifications/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    @pytest.mark.asyncio
    async def test_get_notification_by_id(self, admin_client, db_session):
        n = await NotificationFactory.create(db_session)
        response = await admin_client.get(f"/api/v1/notifications/{n.id}")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_list_templates(self, admin_client, db_session):
        await NotificationTemplateFactory.create(
            db_session,
            template_type=NotificationTemplateType.import_completed,
        )
        response = await admin_client.get("/api/v1/notifications/templates")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
