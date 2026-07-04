"""Tests for NotificationService."""

import pytest

from app.models.enums import NotificationChannelType, NotificationTemplateType
from app.repositories.notification import NotificationRepository
from app.repositories.notification_template import NotificationTemplateRepository
from app.schemas.notification import NotificationContext
from app.services.notification import NotificationService
from tests.factories import NotificationFactory, NotificationTemplateFactory


class DummySenderFactory:
    def dispatch_send(self, notification_id):
        pass


class DummyRenderer:
    def render(self, template_body, context):
        return f"rendered_{template_body}"

    def render_subject(self, subject, context):
        return subject


class TestNotificationService:
    def _make_service(self, db_session):
        return NotificationService(
            repository=NotificationRepository(db_session),
            template_repository=NotificationTemplateRepository(db_session),
            renderer=DummyRenderer(),
            sender_factory=DummySenderFactory(),
        )

    @pytest.mark.asyncio
    async def test_send_notification(self, db_session):
        await NotificationTemplateFactory.create(
            db_session,
            template_type=NotificationTemplateType.welcome,
            channel=NotificationChannelType.email,
        )
        svc = self._make_service(db_session)
        ctx = NotificationContext(user_name="Test User")
        notif = await svc.send(
            channel=NotificationChannelType.email,
            recipient="user@test.com",
            template_type=NotificationTemplateType.welcome,
            context=ctx,
        )
        assert notif is not None
        assert notif.recipient == "user@test.com"

    @pytest.mark.asyncio
    async def test_get_notification(self, db_session):
        n = await NotificationFactory.create(db_session)
        svc = self._make_service(db_session)
        found = await svc.get_notification(n.id)
        assert found.id == n.id

    @pytest.mark.asyncio
    async def test_list_notifications(self, db_session):
        await NotificationFactory.create(db_session)
        await NotificationFactory.create(db_session)
        svc = self._make_service(db_session)
        items, total = await svc.list_notifications(0, 10)
        assert total == 2

    @pytest.mark.asyncio
    async def test_list_templates(self, db_session):
        await NotificationTemplateFactory.create(db_session)
        svc = self._make_service(db_session)
        items, total = await svc.list_templates(0, 10)
        assert total == 1
