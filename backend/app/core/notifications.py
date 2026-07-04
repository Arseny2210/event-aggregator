"""Notification channel abstraction.

NotificationChannel ABC defines the contract for all delivery channels.
Implementations: Email, Telegram (stub), InApp (stub).

NotificationService never knows which channel implementation is used.
"""

from abc import ABC, abstractmethod
from logging import getLogger

from app.core.email import EmailBackend
from app.models.enums import NotificationChannelType

logger = getLogger(__name__)


class NotificationChannel(ABC):
    """Abstract interface for notification delivery channels."""

    @abstractmethod
    async def send(self, recipient: str, subject: str | None, body: str) -> None: ...

    @property
    @abstractmethod
    def channel_type(self) -> NotificationChannelType: ...


class EmailNotificationChannel(NotificationChannel):
    """Delivers notifications via email."""

    def __init__(self, backend: EmailBackend) -> None:
        self._backend = backend

    @property
    def channel_type(self) -> NotificationChannelType:
        return NotificationChannelType.email

    async def send(self, recipient: str, subject: str | None, body: str) -> None:
        await self._backend.send_email(
            to=recipient,
            subject=subject or "",
            html_body=body,
        )


class TelegramNotificationChannel(NotificationChannel):
    """Stub for future Telegram Bot API integration."""

    @property
    def channel_type(self) -> NotificationChannelType:
        return NotificationChannelType.telegram

    async def send(self, recipient: str, subject: str | None, body: str) -> None:
        logger.info("Telegram stub: would send to %s: %s", recipient, body)


class InAppNotificationChannel(NotificationChannel):
    """Stub for future in-app notification (WebSocket, push, etc.)."""

    @property
    def channel_type(self) -> NotificationChannelType:
        return NotificationChannelType.in_app

    async def send(self, recipient: str, subject: str | None, body: str) -> None:
        logger.info("InApp stub: would notify user %s: %s", recipient, body)
