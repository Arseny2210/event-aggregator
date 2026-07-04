"""Integration tests for notification workflow."""

import pytest

from app.models.enums import (
    NotificationChannelType,
    NotificationStatus,
    NotificationTemplateType,
)
from tests.factories import NotificationFactory, NotificationTemplateFactory


class TestNotificationWorkflow:
    @pytest.mark.asyncio
    async def test_create_notification(self, db_session):
        n = await NotificationFactory.create(
            db_session,
            channel=NotificationChannelType.email,
            status=NotificationStatus.pending,
        )
        assert n.status == NotificationStatus.pending
        assert n.channel == NotificationChannelType.email

    @pytest.mark.asyncio
    async def test_notification_with_template(self, db_session):
        tmpl = await NotificationTemplateFactory.create(
            db_session,
            template_type=NotificationTemplateType.welcome,
        )
        n = await NotificationFactory.create(
            db_session,
            template_type=NotificationTemplateType.welcome,
        )
        assert n.template_type == tmpl.template_type
