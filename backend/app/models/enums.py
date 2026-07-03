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
