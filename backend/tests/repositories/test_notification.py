"""Tests for NotificationRepository."""

import pytest

from app.models.enums import NotificationStatus
from app.repositories.notification import NotificationRepository
from tests.factories import NotificationFactory


class TestNotificationRepository:
    @pytest.mark.asyncio
    async def test_get_by_id(self, db_session):
        notif = await NotificationFactory.create(db_session)
        repo = NotificationRepository(db_session)
        found = await repo.get_by_id(notif.id)
        assert found is not None

    @pytest.mark.asyncio
    async def test_get_by_status(self, db_session):
        await NotificationFactory.create(db_session, status=NotificationStatus.pending)
        await NotificationFactory.create(db_session, status=NotificationStatus.sent)
        repo = NotificationRepository(db_session)
        items, total = await repo.get_by_status(NotificationStatus.pending, 0, 10)
        assert total == 1

    @pytest.mark.asyncio
    async def test_get_by_recipient(self, db_session):
        await NotificationFactory.create(db_session, recipient="user@test.com")
        await NotificationFactory.create(db_session, recipient="other@test.com")
        repo = NotificationRepository(db_session)
        items, total = await repo.get_by_recipient("user@test.com", 0, 10)
        assert total == 1

    @pytest.mark.asyncio
    async def test_get_pending(self, db_session):
        await NotificationFactory.create(db_session, status=NotificationStatus.pending)
        await NotificationFactory.create(db_session, status=NotificationStatus.sent)
        repo = NotificationRepository(db_session)
        items = await repo.get_pending(0, 10)
        assert len(items) == 1

    @pytest.mark.asyncio
    async def test_update_status(self, db_session):
        notif = await NotificationFactory.create(db_session)
        repo = NotificationRepository(db_session)
        updated = await repo.update_status(
            notif.id,
            NotificationStatus.sent,
            attempts=1,
        )
        assert updated is not None
        assert updated.status == NotificationStatus.sent
        assert updated.attempts == 1

    @pytest.mark.asyncio
    async def test_get_paginated(self, db_session):
        await NotificationFactory.create(db_session)
        await NotificationFactory.create(db_session)
        repo = NotificationRepository(db_session)
        items, total = await repo.get_paginated(0, 10)
        assert total == 2
