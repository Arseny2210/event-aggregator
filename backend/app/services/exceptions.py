"""Domain exceptions raised by service-layer business logic.

The service layer never raises HTTP exceptions. The API layer (a later stage)
catches these domain exceptions and translates them into HTTP responses.

Hierarchy:

    DomainError
    ├── NotFoundError
    │   ├── EventNotFound
    │   ├── OrganizerNotFound
    │   ├── ParticipationNotFound
    │   ├── UserNotFound
    │   ├── RoleNotFound
    │   ├── PermissionNotFound
    │   └── ImportJobNotFound
    ├── AlreadyExistsError
    │   ├── DuplicateUsername
    │   ├── DuplicateEmail
    │   ├── DuplicateOrganizerName
    │   ├── DuplicateRoleName
    │   ├── DuplicatePermissionName
    │   └── DuplicateParticipation
    ├── BusinessRuleViolationError
    │   ├── InvalidEventStatusTransition
    │   ├── EventNotPublishable
    │   ├── ArchivedEventNotEditable
    │   ├── CannotRegisterForArchivedEvent
    │   ├── RegistrationClosed
    │   ├── InvalidEventData
    │   ├── OrganizerInUse
    │   ├── RoleInUse
    │   └── PermissionInUse
    └── ImportOperationError
        └── InvalidImportStatusTransition
"""

import uuid

from app.models.enums import EventStatus, ImportStatus


class DomainError(Exception):
    """Base exception for all domain-level errors raised by services."""

    code: str = "domain_error"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotFoundError(DomainError):
    """A referenced resource was not found."""

    code = "not_found"


class AlreadyExistsError(DomainError):
    """A resource with the same unique attribute already exists."""

    code = "conflict"


class BusinessRuleViolationError(DomainError):
    """A business rule was violated."""

    code = "business_rule_violation"


class ImportOperationError(DomainError):
    """An import job operation was attempted in an invalid state."""

    code = "import_error"


class EventNotFoundError(NotFoundError):
    def __init__(self, event_id: uuid.UUID) -> None:
        super().__init__(f"Event not found: {event_id}")
        self.event_id = event_id


class OrganizerNotFoundError(NotFoundError):
    def __init__(self, organizer_id: uuid.UUID) -> None:
        super().__init__(f"Organizer not found: {organizer_id}")
        self.organizer_id = organizer_id


class ParticipationNotFoundError(NotFoundError):
    def __init__(
        self,
        participation_id: uuid.UUID | None = None,
        *,
        event_id: uuid.UUID | None = None,
        session_id: str | None = None,
    ) -> None:
        if participation_id is not None:
            message = f"Participation not found: {participation_id}"
        else:
            message = f"No participation found for event {event_id} and session {session_id!r}"
        super().__init__(message)
        self.participation_id = participation_id
        self.event_id = event_id
        self.session_id = session_id


class UserNotFoundError(NotFoundError):
    def __init__(self, identifier: uuid.UUID | str) -> None:
        super().__init__(f"User not found: {identifier}")
        self.identifier = identifier


class RoleNotFoundError(NotFoundError):
    def __init__(self, identifier: int | str) -> None:
        super().__init__(f"Role not found: {identifier}")
        self.identifier = identifier


class PermissionNotFoundError(NotFoundError):
    def __init__(self, identifier: int | str) -> None:
        super().__init__(f"Permission not found: {identifier}")
        self.identifier = identifier


class ImportJobNotFoundError(NotFoundError):
    def __init__(self, import_job_id: uuid.UUID) -> None:
        super().__init__(f"Import job not found: {import_job_id}")
        self.import_job_id = import_job_id


class DuplicateUsernameError(AlreadyExistsError):
    def __init__(self, username: str) -> None:
        super().__init__(f"Username already exists: {username}")
        self.username = username


class DuplicateEmailError(AlreadyExistsError):
    def __init__(self, email: str) -> None:
        super().__init__(f"Email already exists: {email}")
        self.email = email


class DuplicateOrganizerNameError(AlreadyExistsError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Organizer name already exists: {name}")
        self.name = name


class DuplicateRoleNameError(AlreadyExistsError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Role name already exists: {name}")
        self.name = name


class DuplicatePermissionNameError(AlreadyExistsError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Permission name already exists: {name}")
        self.name = name


class DuplicateParticipationError(AlreadyExistsError):
    def __init__(self, event_id: uuid.UUID, session_id: str) -> None:
        super().__init__(
            f"Participation already exists for event {event_id} and session {session_id!r}"
        )
        self.event_id = event_id
        self.session_id = session_id


class InvalidEventStatusTransitionError(BusinessRuleViolationError):
    def __init__(self, current: EventStatus, attempted: EventStatus) -> None:
        super().__init__(f"Cannot transition event from '{current.value}' to '{attempted.value}'")
        self.current = current
        self.attempted = attempted


class EventNotPublishableError(BusinessRuleViolationError):
    def __init__(self, event_id: uuid.UUID, reason: str) -> None:
        super().__init__(f"Event {event_id} is not publishable: {reason}")
        self.event_id = event_id
        self.reason = reason


class ArchivedEventNotEditableError(BusinessRuleViolationError):
    def __init__(self, event_id: uuid.UUID) -> None:
        super().__init__(f"Archived event {event_id} is not editable")
        self.event_id = event_id


class CannotRegisterForArchivedEventError(BusinessRuleViolationError):
    def __init__(self, event_id: uuid.UUID) -> None:
        super().__init__(f"Cannot register for archived event {event_id}")
        self.event_id = event_id


class RegistrationClosedError(BusinessRuleViolationError):
    def __init__(self, event_id: uuid.UUID) -> None:
        super().__init__(f"Registration for event {event_id} is closed")
        self.event_id = event_id


class InvalidEventDataError(BusinessRuleViolationError):
    def __init__(self, event_id: uuid.UUID | None, reason: str) -> None:
        prefix = f"Event {event_id}" if event_id is not None else "Event"
        super().__init__(f"{prefix} has invalid data: {reason}")
        self.event_id = event_id
        self.reason = reason


class OrganizerInUseError(BusinessRuleViolationError):
    def __init__(self, organizer_id: uuid.UUID, event_count: int) -> None:
        super().__init__(
            f"Organizer {organizer_id} cannot be deleted; {event_count} event(s) reference it"
        )
        self.organizer_id = organizer_id
        self.event_count = event_count


class RoleInUseError(BusinessRuleViolationError):
    def __init__(self, role_id: int, user_count: int) -> None:
        super().__init__(
            f"Role {role_id} cannot be deleted; {user_count} user(s) are assigned to it"
        )
        self.role_id = role_id
        self.user_count = user_count


class PermissionInUseError(BusinessRuleViolationError):
    def __init__(self, permission_id: int, role_count: int) -> None:
        super().__init__(
            f"Permission {permission_id} cannot be deleted; {role_count} role(s) use it"
        )
        self.permission_id = permission_id
        self.role_count = role_count


class InvalidImportStatusTransitionError(ImportOperationError):
    def __init__(self, current: ImportStatus, attempted: ImportStatus) -> None:
        super().__init__(
            f"Cannot transition import job from '{current.value}' to '{attempted.value}'"
        )
        self.current = current
        self.attempted = attempted
