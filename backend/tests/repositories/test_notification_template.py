"""Tests for NotificationTemplateRepository."""

import pytest

from app.models.enums import NotificationChannelType, NotificationTemplateType
from app.repositories.notification_template import NotificationTemplateRepository
from tests.factories import NotificationTemplateFactory


class TestNotificationTemplateRepository:
    @pytest.mark.asyncio
    async def test_get_by_id(self, db_session):
        tmpl = await NotificationTemplateFactory.create(db_session)
        repo = NotificationTemplateRepository(db_session)
        found = await repo.get_by_id(tmpl.id)
        assert found is not None

    @pytest.mark.asyncio
    async def test_get_by_type_channel_language(self, db_session):
        tmpl = await NotificationTemplateFactory.create(
            db_session,
            template_type=NotificationTemplateType.welcome,
            channel=NotificationChannelType.email,
            language="en",
        )
        repo = NotificationTemplateRepository(db_session)
        found = await repo.get_by_type_channel_language(
            NotificationTemplateType.welcome,
            NotificationChannelType.email,
            language="en",
        )
        assert found is not None
        assert found.id == tmpl.id

    @pytest.mark.asyncio
    async def test_get_by_type_not_found(self, db_session):
        repo = NotificationTemplateRepository(db_session)
        found = await repo.get_by_type_channel_language(
            NotificationTemplateType.password_reset,
            NotificationChannelType.email,
        )
        assert found is None

    @pytest.mark.asyncio
    async def test_get_all_active(self, db_session):
        await NotificationTemplateFactory.create(
            db_session,
            template_type=NotificationTemplateType.welcome,
        )
        await NotificationTemplateFactory.create(
            db_session,
            template_type=NotificationTemplateType.password_reset,
        )
        repo = NotificationTemplateRepository(db_session)
        items, total = await repo.get_all_active(0, 10)
        assert total == 2
