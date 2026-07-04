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


class NotificationChannelType(enum.Enum):
    email = "email"
    telegram = "telegram"
    in_app = "in_app"


class NotificationStatus(enum.Enum):
    pending = "pending"
    sent = "sent"
    failed = "failed"
    retrying = "retrying"


class NotificationTemplateType(enum.Enum):
    welcome = "welcome"
    password_reset = "password_reset"
    event_published = "event_published"
    event_reminder = "event_reminder"
    import_completed = "import_completed"
    import_failed = "import_failed"


class NotificationPriority(enum.Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"
