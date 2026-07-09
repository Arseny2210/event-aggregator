"""Public notification endpoints — accessible by session_id without authentication."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.api.v1.dependencies import get_notification_service
from app.schemas.notification import NotificationResponse
from app.schemas.page import Page
from app.services.notification import NotificationService

router = APIRouter()


@router.get("/public", response_model=Page[NotificationResponse])
async def list_public_notifications(
    session_id: Annotated[str, Query(min_length=1, max_length=255)],
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    items, total = await notification_service.get_public_notifications(session_id, offset, limit)
    return Page[NotificationResponse](
        items=[NotificationResponse.model_validate(item) for item in items],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.post("/{notification_id}/read", status_code=204)
async def mark_notification_as_read(
    notification_id: UUID,
    session_id: Annotated[str, Query(min_length=1, max_length=255)],
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
):
    await notification_service.mark_as_read(notification_id, session_id)


@router.delete("/{notification_id}", status_code=204)
async def delete_public_notification(
    notification_id: UUID,
    session_id: Annotated[str, Query(min_length=1, max_length=255)],
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
):
    await notification_service.delete_notification(notification_id, session_id)
