"""Tests for ParticipationService."""

import pytest

from app.core.templates import TemplateRenderer
from app.repositories.event import EventRepository
from app.repositories.notification import NotificationRepository
from app.repositories.notification_template import NotificationTemplateRepository
from app.repositories.participation import ParticipationRepository
from app.services.notification import NotificationService
from app.services.notification_sender import NotificationSenderFactory
from app.services.participation import ParticipationService
from tests.factories import ParticipationFactory


def _make_notification_service(db_session) -> NotificationService:
    from unittest.mock import AsyncMock

    sender_factory = AsyncMock(spec=NotificationSenderFactory)
    return NotificationService(
        repository=NotificationRepository(db_session),
        template_repository=NotificationTemplateRepository(db_session),
        renderer=TemplateRenderer(),
        sender_factory=sender_factory,
    )


class TestParticipationService:
    def _make_service(self, db_session):
        return ParticipationService(
            session=db_session,
            repository=ParticipationRepository(db_session),
            event_repository=EventRepository(db_session),
            notification_service=_make_notification_service(db_session),
        )

    @pytest.mark.asyncio
    async def test_get_participation(self, db_session):
        part = await ParticipationFactory.create(db_session)
        svc = self._make_service(db_session)
        found = await svc.get_participation(part.id)
        assert found.id == part.id
