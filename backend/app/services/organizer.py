"""Service for managing event organizers."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organizer import Organizer
from app.repositories.event import EventRepository
from app.repositories.organizer import OrganizerRepository
from app.schemas.organizer import OrganizerCreate, OrganizerUpdate
from app.services.exceptions import (
    DuplicateOrganizerNameError,
    OrganizerInUseError,
    OrganizerNotFoundError,
)
from app.services.transaction import transactional


class OrganizerService:
    """Business logic for event organizer management."""

    def __init__(
        self,
        session: AsyncSession,
        repository: OrganizerRepository,
        event_repository: EventRepository,
    ) -> None:
        self.session = session
        self.repository = repository
        self.event_repository = event_repository

    async def get_organizer(self, organizer_id: UUID) -> Organizer:
        organizer = await self.repository.get_by_id(organizer_id)
        if organizer is None:
            raise OrganizerNotFoundError(organizer_id)
        return organizer

    async def create_organizer(self, data: OrganizerCreate) -> Organizer:
        existing = await self.repository.get_by_name(data.name)
        if existing is not None:
            raise DuplicateOrganizerNameError(data.name)
        organizer = Organizer(**data.model_dump())
        async with transactional(self.session):
            return await self.repository.create(organizer)

    async def update_organizer(self, organizer_id: UUID, data: OrganizerUpdate) -> Organizer:
        organizer = await self.get_organizer(organizer_id)
        payload = data.model_dump(exclude_unset=True)
        if "name" in payload and payload["name"] != organizer.name:
            conflicting = await self.repository.get_by_name(payload["name"])
            if conflicting is not None and conflicting.id != organizer.id:
                raise DuplicateOrganizerNameError(payload["name"])
        async with transactional(self.session):
            for field, value in payload.items():
                setattr(organizer, field, value)
            return organizer

    async def delete_organizer(self, organizer_id: UUID) -> None:
        organizer = await self.get_organizer(organizer_id)
        _, total = await self.event_repository.get_by_organizer(organizer_id, 0, 1)
        if total > 0:
            raise OrganizerInUseError(organizer_id, total)
        async with transactional(self.session):
            await self.repository.delete(organizer)

    async def list_organizers(self, offset: int, limit: int) -> tuple[list[Organizer], int]:
        return await self.repository.get_paginated(offset, limit)

    async def search_organizers(
        self, query: str, offset: int, limit: int
    ) -> tuple[list[Organizer], int]:
        return await self.repository.search_by_name(query, offset, limit)
