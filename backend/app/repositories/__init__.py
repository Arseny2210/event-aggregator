"""Repository layer for the Event Aggregator application."""

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

__all__ = [
    "EventRepository",
    "ImportJobRepository",
    "ImportJobRowResultRepository",
    "NotificationRepository",
    "NotificationTemplateRepository",
    "OrganizerRepository",
    "ParticipationRepository",
    "PermissionRepository",
    "RolePermissionRepository",
    "RoleRepository",
    "StatisticsRepository",
    "UserRepository",
]
