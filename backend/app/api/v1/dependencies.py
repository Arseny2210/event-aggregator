"""Dependency injection providers for the API layer.

Each provider function receives an AsyncSession via ``Depends(get_db)``,
instantiates the required repositories, and returns a fully wired service
instance. Providers are plain ``async def`` functions — neither generators
nor context managers — because services and repositories hold no resources
that require cleanup. Session lifetime is managed by ``get_db()``.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.repositories.event import EventRepository
from app.repositories.import_job import ImportJobRepository
from app.repositories.organizer import OrganizerRepository
from app.repositories.participation import ParticipationRepository
from app.repositories.permission import PermissionRepository
from app.repositories.role import RoleRepository
from app.repositories.role_permission import RolePermissionRepository
from app.repositories.user import UserRepository
from app.services.event import EventService
from app.services.import_job import ImportJobService
from app.services.organizer import OrganizerService
from app.services.participation import ParticipationService
from app.services.permission import PermissionService
from app.services.role import RoleService
from app.services.user import UserService


async def get_organizer_service(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> OrganizerService:
    organizer_repo = OrganizerRepository(session)
    event_repo = EventRepository(session)
    return OrganizerService(session, organizer_repo, event_repo)


async def get_event_service(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> EventService:
    event_repo = EventRepository(session)
    organizer_repo = OrganizerRepository(session)
    return EventService(session, event_repo, organizer_repo)


async def get_participation_service(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> ParticipationService:
    participation_repo = ParticipationRepository(session)
    event_repo = EventRepository(session)
    return ParticipationService(session, participation_repo, event_repo)


async def get_user_service(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> UserService:
    user_repo = UserRepository(session)
    role_repo = RoleRepository(session)
    return UserService(session, user_repo, role_repo)


async def get_role_service(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> RoleService:
    role_repo = RoleRepository(session)
    role_permission_repo = RolePermissionRepository(session)
    permission_repo = PermissionRepository(session)
    user_repo = UserRepository(session)
    return RoleService(session, role_repo, role_permission_repo, permission_repo, user_repo)


async def get_permission_service(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> PermissionService:
    permission_repo = PermissionRepository(session)
    role_permission_repo = RolePermissionRepository(session)
    return PermissionService(session, permission_repo, role_permission_repo)


async def get_import_job_service(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> ImportJobService:
    import_job_repo = ImportJobRepository(session)
    return ImportJobService(session, import_job_repo)
