"""Notification endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.v1.dependencies import get_notification_service
from app.core.constants import (
    PERMISSION_NOTIFICATION_MANAGE,
    PERMISSION_NOTIFICATION_SEND,
    PERMISSION_NOTIFICATION_VIEW,
)
from app.dependencies.auth import require_permission
from app.models.enums import NotificationStatus
from app.models.user import User
from app.schemas.notification import (
    NotificationContext,
    NotificationResponse,
    NotificationTemplateResponse,
    SendNotificationRequest,
    SendTestNotificationRequest,
)
from app.schemas.page import Page
from app.services.notification import NotificationService

router = APIRouter()


@router.get("/", response_model=Page[NotificationResponse])
async def list_notifications(
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
    current_user: Annotated[User, Depends(require_permission(PERMISSION_NOTIFICATION_VIEW))],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    status: Annotated[NotificationStatus | None, Query()] = None,
):
    if status is not None:
        items, total = await notification_service.list_notifications_by_status(
            status, offset, limit
        )
    else:
        items, total = await notification_service.list_notifications(offset, limit)
    return Page[NotificationResponse](
        items=[NotificationResponse.model_validate(item) for item in items],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: str,
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
    current_user: Annotated[User, Depends(require_permission(PERMISSION_NOTIFICATION_VIEW))],
):
    from uuid import UUID

    notification = await notification_service.get_notification(UUID(notification_id))
    return NotificationResponse.model_validate(notification)


@router.post("/send", response_model=NotificationResponse, status_code=201)
async def send_notification(
    data: SendNotificationRequest,
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
    current_user: Annotated[User, Depends(require_permission(PERMISSION_NOTIFICATION_SEND))],
):
    context = NotificationContext(**data.context)
    notification = await notification_service.send(
        channel=data.channel,
        recipient=data.recipient,
        template_type=data.template_type,
        context=context,
        priority=data.priority,
        language=data.language,
        created_by=current_user.id,
    )
    return NotificationResponse.model_validate(notification)


@router.post("/test", response_model=NotificationResponse, status_code=201)
async def send_test_notification(
    data: SendTestNotificationRequest,
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
    current_user: Annotated[User, Depends(require_permission(PERMISSION_NOTIFICATION_MANAGE))],
):
    notification = await notification_service.send_test(
        channel=data.channel,
        recipient=data.recipient,
        template_type=data.template_type,
        language=data.language,
    )
    return NotificationResponse.model_validate(notification)


@router.get("/templates", response_model=Page[NotificationTemplateResponse])
async def list_notification_templates(
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
    current_user: Annotated[User, Depends(require_permission(PERMISSION_NOTIFICATION_VIEW))],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    items, total = await notification_service.list_templates(offset, limit)
    return Page[NotificationTemplateResponse](
        items=[NotificationTemplateResponse.model_validate(item) for item in items],
        total=total,
        offset=offset,
        limit=limit,
    )
