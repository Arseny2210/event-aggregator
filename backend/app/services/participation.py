"""Service for managing event participation."""

from dataclasses import dataclass
from datetime import date
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import EventStatus, ParticipationStatus
from app.models.participation import Participation
from app.repositories.event import EventRepository
from app.repositories.participation import ParticipationRepository
from app.services.exceptions import (
    CannotRegisterForArchivedEventError,
    DuplicateParticipationError,
    EventNotFoundError,
    ParticipationNotFoundError,
    RegistrationClosedError,
)
from app.services.transaction import transactional

_STATISTICS_LIMIT = 100_000


@dataclass(frozen=True, slots=True)
class ParticipationStatistics:
    event_id: UUID
    total: int
    registered: int
    confirmed: int
    cancelled: int


class ParticipationService:
    """Business logic for participation registration."""

    def __init__(
        self,
        session: AsyncSession,
        repository: ParticipationRepository,
        event_repository: EventRepository,
    ) -> None:
        self.session = session
        self.repository = repository
        self.event_repository = event_repository

    async def register_participation(self, event_id: UUID, session_id: str) -> Participation:
        event = await self.event_repository.get_by_id(event_id)
        if event is None:
            raise EventNotFoundError(event_id)
        if event.status == EventStatus.archived:
            raise CannotRegisterForArchivedEventError(event_id)
        if event.start_date < date.today():
            raise RegistrationClosedError(event_id)
        existing = await self.repository.get_by_event_and_session(event_id, session_id)
        if existing is not None:
            raise DuplicateParticipationError(event_id, session_id)
        participation = Participation(
            event_id=event_id,
            session_id=session_id,
            status=ParticipationStatus.registered,
        )
        async with transactional(self.session):
            return await self.repository.create(participation)

    async def cancel_participation(self, event_id: UUID, session_id: str) -> None:
        participation = await self.repository.get_by_event_and_session(event_id, session_id)
        if participation is None:
            raise ParticipationNotFoundError(event_id=event_id, session_id=session_id)
        async with transactional(self.session):
            await self.repository.delete(participation)

    async def get_participation(self, participation_id: UUID) -> Participation:
        participation = await self.repository.get_by_id(participation_id)
        if participation is None:
            raise ParticipationNotFoundError(participation_id=participation_id)
        return participation

    async def list_participations_for_event(
        self, event_id: UUID, offset: int, limit: int
    ) -> tuple[list[Participation], int]:
        return await self.repository.get_by_event(event_id, offset, limit)

    async def list_participations_for_session(self, session_id: str) -> list[Participation]:
        return await self.repository.get_by_session(session_id)

    async def get_participation_statistics(self, event_id: UUID) -> ParticipationStatistics:
        event = await self.event_repository.get_by_id(event_id)
        if event is None:
            raise EventNotFoundError(event_id)
        participations, _ = await self.repository.get_by_event(event_id, 0, _STATISTICS_LIMIT)
        registered = sum(1 for p in participations if p.status == ParticipationStatus.registered)
        confirmed = sum(1 for p in participations if p.status == ParticipationStatus.confirmed)
        cancelled = sum(1 for p in participations if p.status == ParticipationStatus.cancelled)
        return ParticipationStatistics(
            event_id=event_id,
            total=len(participations),
            registered=registered,
            confirmed=confirmed,
            cancelled=cancelled,
        )
