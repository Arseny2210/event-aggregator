"""Core-level exception for notification delivery failures.

Used by NotificationChannel implementations.
NOT a service-layer DomainError — this is a transport-layer concern.
"""


class NotificationDeliveryError(Exception):
    """Raised when a notification channel fails to deliver."""

    def __init__(self, message: str, channel: str) -> None:
        super().__init__(message)
        self.channel = channel
