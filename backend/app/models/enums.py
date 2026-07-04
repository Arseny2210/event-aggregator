"""Enumerations used by ORM models."""

import enum


class UserRole(enum.Enum):
    administrator = "administrator"
    editor = "editor"


class EventStatus(enum.Enum):
    draft = "draft"
    published = "published"
    completed = "completed"
    archived = "archived"


class ParticipationStatus(enum.Enum):
    registered = "registered"
    confirmed = "confirmed"
    cancelled = "cancelled"


class ImportStatus(enum.Enum):
    processing = "processing"
    completed = "completed"
    failed = "failed"


class ImportRowStatus(enum.Enum):
    imported = "imported"
    warning = "warning"
    failed = "failed"


class ImportRowError(enum.Enum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    INVALID_DATE = "INVALID_DATE"
    INVALID_UUID = "INVALID_UUID"
    ORGANIZER_NOT_FOUND = "ORGANIZER_NOT_FOUND"
    CATEGORY_REQUIRED = "CATEGORY_REQUIRED"
    DEFAULT_CATEGORY_USED = "DEFAULT_CATEGORY_USED"
    DATABASE_ERROR = "DATABASE_ERROR"
