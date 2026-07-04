"""Tests for OrganizerService."""

import pytest

from app.repositories.event import EventRepository
from app.repositories.organizer import OrganizerRepository
from app.services.exceptions import OrganizerNotFoundError
from app.services.organizer import OrganizerService
from tests.factories import OrganizerFactory


class TestOrganizerService:
    def _make_service(self, db_session):
        return OrganizerService(
            session=db_session,
            repository=OrganizerRepository(db_session),
            event_repository=EventRepository(db_session),
        )

    @pytest.mark.asyncio
    async def test_get_organizer(self, db_session):
        org = await OrganizerFactory.create(db_session)
        svc = self._make_service(db_session)
        found = await svc.get_organizer(org.id)
        assert found.id == org.id

    @pytest.mark.asyncio
    async def test_get_organizer_not_found(self, db_session):
        from uuid import uuid4

        svc = self._make_service(db_session)
        with pytest.raises(OrganizerNotFoundError):
            await svc.get_organizer(uuid4())
