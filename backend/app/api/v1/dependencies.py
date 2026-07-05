"""Dependency injection providers for the API layer.

Each provider function receives an AsyncSession via ``Depends(get_db)``,
instantiates the required repositories, and returns a fully wired service
instance. Providers are plain ``async def`` functions — neither generators
nor context managers — because services and repositories hold no resources
that require cleanup. Session lifetime is managed by ``get_db()``.
"""

from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.email import SMTPEmailBackend
from app.core.notifications import (
    EmailNotificationChannel,
    InAppNotificationChannel,
    TelegramNotificationChannel,
)
from app.core.storage import LocalStorageBackend
from app.core.tasks import AsyncioBackgroundTaskDispatcher
from app.core.templates import TemplateRenderer
from app.database.session import async_session_factory
from app.dependencies.database import get_db
from app.models.enums import NotificationChannelType
from app.repositories.event import EventRepository
from app.repositories.import_job import ImportJobRepository
from app.repositories.import_row_result import ImportJobRowResultRepository
from app.repositories.notification import NotificationRepository
from app.repositories.notification_template import NotificationTemplateRepository
from app.repositories.organizer import OrganizerRepository
from app.repositories.participation import ParticipationRepository
from app.repositories.permission import PermissionRepository
from app.repositories.role import RoleRepository
from app.repositories.role_permission import RolePermissionRepository
from app.repositories.statistics import StatisticsRepository
from app.repositories.user import UserRepository
from app.services.event import EventService
from app.services.import_job import ImportJobService
from app.services.notification import NotificationService
from app.services.notification_sender import NotificationSenderFactory
from app.services.organizer import OrganizerService
from app.services.participation import ParticipationService
from app.services.permission import PermissionService
from app.services.role import RoleService
from app.services.statistics import StatisticsService
from app.services.user import UserService

_storage_backend = LocalStorageBackend(Path(settings.upload_dir))
_task_dispatcher = AsyncioBackgroundTaskDispatcher()
_email_backend = SMTPEmailBackend(
    host=settings.smtp_host,
    port=settings.smtp_port,
    username=settings.smtp_username,
    password=settings.smtp_password,
    use_tls=settings.smtp_use_tls,
    from_address=settings.smtp_from_address,
)
_notification_channels = {
    NotificationChannelType.email: EmailNotificationChannel(_email_backend),
    NotificationChannelType.telegram: TelegramNotificationChannel(),
    NotificationChannelType.in_app: InAppNotificationChannel(),
}
_template_renderer = TemplateRenderer()
_sender_factory = NotificationSenderFactory(
    session_factory=async_session_factory,
    channels=_notification_channels,
    dispatcher=_task_dispatcher,
    max_retries=settings.notification_max_retries,
)


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
    participation_repo = ParticipationRepository(session)
    return EventService(session, event_repo, organizer_repo, participation_repo)


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
    row_result_repo = ImportJobRowResultRepository(session)
    return ImportJobService(
        session=session,
        repository=import_job_repo,
        row_result_repository=row_result_repo,
        storage=_storage_backend,
        dispatcher=_task_dispatcher,
        session_factory=async_session_factory,
    )


async def get_statistics_service(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> StatisticsService:
    repo = StatisticsRepository(session)
    return StatisticsService(repo)


async def get_notification_service(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> NotificationService:
    notification_repo = NotificationRepository(session)
    template_repo = NotificationTemplateRepository(session)
    return NotificationService(
        repository=notification_repo,
        template_repository=template_repo,
        renderer=_template_renderer,
        sender_factory=_sender_factory,
    )
