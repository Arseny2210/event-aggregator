"""Service layer for the Event Aggregator application.

Business logic, validation, repository orchestration, and transaction management.
"""

from app.services.auth import AuthService
from app.services.event import EventService
from app.services.exceptions import (
    AlreadyExistsError,
    AuthenticationError,
    AuthorizationError,
    BusinessRuleViolationError,
    DomainError,
    EmptyFileError,
    FileTooLargeError,
    ImportOperationError,
    ImportProcessingError,
    InsufficientPermissionsError,
    InvalidCredentialsError,
    InvalidFileFormatError,
    InvalidTokenError,
    NotFoundError,
    TokenExpiredError,
    UserInactiveError,
)
from app.services.import_job import ImportJobService
from app.services.import_processor import ImportProcessor
from app.services.organizer import OrganizerService
from app.services.participation import ParticipationService
from app.services.permission import PermissionService
from app.services.role import RoleService
from app.services.statistics import StatisticsService
from app.services.transaction import transactional
from app.services.user import UserService

__all__ = [
    "AlreadyExistsError",
    "AuthenticationError",
    "AuthService",
    "AuthorizationError",
    "BusinessRuleViolationError",
    "DomainError",
    "EmptyFileError",
    "EventService",
    "FileTooLargeError",
    "ImportJobService",
    "ImportOperationError",
    "ImportProcessingError",
    "ImportProcessor",
    "InsufficientPermissionsError",
    "InvalidCredentialsError",
    "InvalidFileFormatError",
    "InvalidTokenError",
    "NotFoundError",
    "OrganizerService",
    "ParticipationService",
    "PermissionService",
    "RoleService",
    "StatisticsService",
    "TokenExpiredError",
    "UserInactiveError",
    "UserService",
    "transactional",
]
