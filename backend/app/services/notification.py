"""NotificationService — orchestrates template rendering, persistence, and dispatch.

Depends only on repositories and abstractions (renderer, sender_factory).
No AsyncSession injected. No FastAPI imports. No app.api imports.
No transport-specific code (no SMTP, no Telegram).
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from app.core.templates import TemplateRenderer
from app.models.enums import (
    NotificationChannelType,
    NotificationPriority,
    NotificationStatus,
    NotificationTemplateType,
)
from app.models.event import Event
from app.models.notification import Notification
from app.models.notification_template import NotificationTemplate
from app.repositories.notification import NotificationRepository
from app.repositories.notification_template import NotificationTemplateRepository
from app.schemas.notification import NotificationContext
from app.services.exceptions import (
    NotificationNotFoundError,
    NotificationTemplateNotFoundError,
)
from app.services.notification_sender import NotificationSenderFactory
from app.services.transaction import transactional

_REMINDER_OFFSET: timedelta = timedelta(hours=1)
_REMINDER_LABEL: str = "1 час"
_EVENT_TZ = timezone(timedelta(hours=3))  # МСК (UTC+3)


class NotificationService:
    """Orchestrates notification lifecycle: render, persist, dispatch."""

    def __init__(
        self,
        repository: NotificationRepository,
        template_repository: NotificationTemplateRepository,
        renderer: TemplateRenderer,
        sender_factory: NotificationSenderFactory,
    ) -> None:
        self.repository = repository
        self.template_repository = template_repository
        self.renderer = renderer
        self.sender_factory = sender_factory

    async def send(
        self,
        channel: NotificationChannelType,
        recipient: str,
        template_type: NotificationTemplateType,
        context: NotificationContext,
        priority: NotificationPriority = NotificationPriority.NORMAL,
        language: str = "en",
        created_by: UUID | None = None,
    ) -> Notification:
        template = await self._get_active_template(template_type, channel, language)
        rendered_body = self.renderer.render(template.body, context)
        rendered_subject = self.renderer.render_subject(template.subject, context)

        payload = context.to_template_namespace()
        payload["rendered_body"] = rendered_body
        if rendered_subject is not None:
            payload["rendered_subject"] = rendered_subject

        async with transactional(self.repository.session):
            notification = Notification(
                channel=channel,
                recipient=recipient,
                template_type=template_type,
                payload=payload,
                subject=rendered_subject,
                status=NotificationStatus.pending,
                priority=priority,
                created_by=created_by,
            )
            created = await self.repository.create(notification)

        self.sender_factory.dispatch_send(created.id)
        return created

    async def send_bulk(
        self,
        channel: NotificationChannelType,
        recipients: list[str],
        template_type: NotificationTemplateType,
        context: NotificationContext,
        priority: NotificationPriority = NotificationPriority.NORMAL,
        language: str = "en",
        created_by: UUID | None = None,
    ) -> list[Notification]:
        template = await self._get_active_template(template_type, channel, language)
        rendered_body = self.renderer.render(template.body, context)
        rendered_subject = self.renderer.render_subject(template.subject, context)

        payload = context.to_template_namespace()
        payload["rendered_body"] = rendered_body
        if rendered_subject is not None:
            payload["rendered_subject"] = rendered_subject

        notifications: list[Notification] = []
        async with transactional(self.repository.session):
            for recipient in recipients:
                notification = Notification(
                    channel=channel,
                    recipient=recipient,
                    template_type=template_type,
                    payload=payload,
                    subject=rendered_subject,
                    status=NotificationStatus.pending,
                    priority=priority,
                    created_by=created_by,
                )
                created = await self.repository.create(notification)
                notifications.append(created)

        for n in notifications:
            self.sender_factory.dispatch_send(n.id)

        return notifications

    async def queue(
        self,
        channel: NotificationChannelType,
        recipient: str,
        template_type: NotificationTemplateType,
        context: NotificationContext,
        scheduled_at: Any,
        priority: NotificationPriority = NotificationPriority.NORMAL,
        language: str = "en",
        created_by: UUID | None = None,
    ) -> Notification:
        template = await self._get_active_template(template_type, channel, language)
        rendered_body = self.renderer.render(template.body, context)
        rendered_subject = self.renderer.render_subject(template.subject, context)

        payload = context.to_template_namespace()
        payload["rendered_body"] = rendered_body
        if rendered_subject is not None:
            payload["rendered_subject"] = rendered_subject

        async with transactional(self.repository.session):
            notification = Notification(
                channel=channel,
                recipient=recipient,
                template_type=template_type,
                payload=payload,
                subject=rendered_subject,
                status=NotificationStatus.pending,
                priority=priority,
                scheduled_at=scheduled_at,
                created_by=created_by,
            )
            return await self.repository.create(notification)

    async def send_test(
        self,
        channel: NotificationChannelType,
        recipient: str,
        template_type: NotificationTemplateType,
        language: str = "en",
    ) -> Notification:
        context = NotificationContext()
        return await self.send(
            channel=channel,
            recipient=recipient,
            template_type=template_type,
            context=context,
            priority=NotificationPriority.HIGH,
            language=language,
        )

    async def get_notification(self, notification_id: UUID) -> Notification:
        notification = await self.repository.get_by_id(notification_id)
        if notification is None:
            raise NotificationNotFoundError(notification_id)
        return notification

    async def list_notifications(self, offset: int, limit: int) -> tuple[list[Notification], int]:
        return await self.repository.get_paginated(offset, limit, Notification.created_at.desc())

    async def list_notifications_by_status(
        self, status: NotificationStatus, offset: int, limit: int
    ) -> tuple[list[Notification], int]:
        return await self.repository.get_by_status(status, offset, limit)

    async def list_templates(
        self, offset: int, limit: int
    ) -> tuple[list[NotificationTemplate], int]:
        return await self.template_repository.get_all_active(offset, limit)

    async def create_event_reminders(self, event: Event, session_id: str) -> list[Notification]:
        notifications: list[Notification] = []
        event_location = event.location or ""

        registration_notification = Notification(
            channel=NotificationChannelType.in_app,
            recipient=session_id,
            template_type=NotificationTemplateType.event_reminder,
            payload={
                "event_title": event.title,
                "event_location": event_location,
                "event_id": str(event.id),
                "rendered_body": (
                    f"Вы записаны на мероприятие «{event.title}»"
                    f"{' (' + event_location + ')' if event_location else ''}."
                ),
            },
            subject="Регистрация подтверждена",
            status=NotificationStatus.pending,
            priority=NotificationPriority.NORMAL,
            event_id=event.id,
        )
        notifications.append(registration_notification)

        if event.start_time is not None:
            start_dt = datetime.combine(event.start_date, event.start_time, tzinfo=_EVENT_TZ)

            try:
                template = await self._get_active_template(
                    NotificationTemplateType.event_reminder,
                    NotificationChannelType.in_app,
                    "ru",
                )
            except NotificationTemplateNotFoundError:
                template = None

            if template is not None:
                scheduled_at = start_dt - _REMINDER_OFFSET
                if scheduled_at > datetime.now(UTC):
                    context = NotificationContext(
                        event_title=event.title,
                        event_id=event.id,
                        event_start_date=event.start_date,
                        extra={"time_left": _REMINDER_LABEL, "event_location": event_location},
                    )
                    rendered_body = self.renderer.render(template.body, context)
                    rendered_subject = self.renderer.render_subject(template.subject, context)

                    payload = context.to_template_namespace()
                    payload["rendered_body"] = rendered_body
                    if rendered_subject is not None:
                        payload["rendered_subject"] = rendered_subject

                    reminder = Notification(
                        channel=NotificationChannelType.in_app,
                        recipient=session_id,
                        template_type=NotificationTemplateType.event_reminder,
                        payload=payload,
                        subject=rendered_subject,
                        status=NotificationStatus.pending,
                        priority=NotificationPriority.NORMAL,
                        scheduled_at=scheduled_at,
                        event_id=event.id,
                    )
                    notifications.append(reminder)

        async with transactional(self.repository.session):
            for n in notifications:
                self.repository.session.add(n)
            await self.repository.session.flush()

        return notifications

    async def create_cancel_notification(self, event: Event, session_id: str) -> None:
        event_location = event.location or ""
        notification = Notification(
            channel=NotificationChannelType.in_app,
            recipient=session_id,
            template_type=NotificationTemplateType.event_reminder,
            payload={
                "event_title": event.title,
                "event_location": event_location,
                "event_id": str(event.id),
                "rendered_body": (
                    f"Вы отменили запись на мероприятие «{event.title}»"
                    f"{' (' + event_location + ')' if event_location else ''}."
                ),
            },
            subject="Запись отменена",
            status=NotificationStatus.pending,
            priority=NotificationPriority.NORMAL,
            event_id=event.id,
        )
        async with transactional(self.repository.session):
            self.repository.session.add(notification)
            await self.repository.session.flush()

    async def get_public_notifications(
        self, session_id: str, offset: int, limit: int
    ) -> tuple[list[Notification], int]:
        return await self.repository.get_by_session_id(session_id, offset, limit)

    async def mark_as_read(self, notification_id: UUID, session_id: str) -> Notification:
        notification = await self.repository.get_by_id(notification_id)
        if notification is None:
            raise NotificationNotFoundError(notification_id)
        if notification.recipient != session_id:
            raise NotificationNotFoundError(notification_id)
        async with transactional(self.repository.session):
            await self.repository.mark_as_read(notification_id)
            notification.read_at = datetime.now(UTC)
            return notification

    async def delete_notification(self, notification_id: UUID, session_id: str) -> None:
        notification = await self.repository.get_by_id(notification_id)
        if notification is None:
            raise NotificationNotFoundError(notification_id)
        if notification.recipient != session_id:
            raise NotificationNotFoundError(notification_id)
        async with transactional(self.repository.session):
            await self.repository.soft_delete_notification(notification_id)

    async def cancel_event_reminders(self, session_id: str, event_id: UUID) -> int:
        return await self.repository.delete_by_session_and_event(session_id, event_id)

    async def cleanup_old_notifications(self, days: int = 7) -> int:
        return await self.repository.cleanup_old_notifications(days)

    async def _get_active_template(
        self,
        template_type: NotificationTemplateType,
        channel: NotificationChannelType,
        language: str,
    ) -> NotificationTemplate:
        template = await self.template_repository.get_by_type_channel_language(
            template_type, channel, language
        )
        if template is None:
            raise NotificationTemplateNotFoundError(template_type.value, channel.value, language)
        return template
