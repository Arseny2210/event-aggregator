"""NotificationService — orchestrates template rendering, persistence, and dispatch.

Depends only on repositories and abstractions (renderer, sender_factory).
No AsyncSession injected. No FastAPI imports. No app.api imports.
No transport-specific code (no SMTP, no Telegram).
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from app.core.templates import TemplateRenderer
from app.models.enums import (
    NotificationChannelType,
    NotificationPriority,
    NotificationStatus,
    NotificationTemplateType,
)
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
