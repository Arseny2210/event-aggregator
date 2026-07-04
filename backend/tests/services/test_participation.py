"""Tests for ParticipationService."""

import pytest

from app.repositories.event import EventRepository
from app.repositories.participation import ParticipationRepository
from app.services.participation import ParticipationService
from tests.factories import ParticipationFactory


class TestParticipationService:
    def _make_service(self, db_session):
        return ParticipationService(
            session=db_session,
            repository=ParticipationRepository(db_session),
            event_repository=EventRepository(db_session),
        )

    @pytest.mark.asyncio
    async def test_get_participation(self, db_session):
        part = await ParticipationFactory.create(db_session)
        svc = self._make_service(db_session)
        found = await svc.get_participation(part.id)
        assert found.id == part.id
