"""Event endpoints — CRUD + advanced search."""

from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel, Field

from app.api.v1.dependencies import get_event_service
from app.core.constants import PERMISSION_EVENT_MANAGE
from app.dependencies.auth import require_permission
from app.models.enums import EventStatus
from app.models.user import User
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from app.schemas.event_search import EventSearchFilters, EventSort
from app.schemas.page import Page
from app.services.event import EventService

router = APIRouter()


class BatchStatusUpdate(BaseModel):
    event_ids: list[UUID] = Field(min_length=1, max_length=100)
    status: EventStatus


@router.get("/", response_model=Page[EventResponse])
async def list_events(
    event_service: Annotated[EventService, Depends(get_event_service)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    search: Annotated[str | None, Query(min_length=1, max_length=255)] = None,
    status: Annotated[EventStatus | None, Query()] = None,
    organizer_id: Annotated[UUID | None, Query()] = None,
    organizer_name: Annotated[str | None, Query(min_length=1, max_length=255)] = None,
    category_id: Annotated[UUID | None, Query()] = None,
    date_from: Annotated[date | None, Query()] = None,
    date_to: Annotated[date | None, Query()] = None,
    sort: Annotated[EventSort, Query()] = EventSort.DATE_ASC,
):
    try:
        filters = EventSearchFilters(
            search=search,
            status=status,
            organizer_id=organizer_id,
            organizer_name=organizer_name,
            category_id=category_id,
            date_from=date_from,
            date_to=date_to,
            sort=sort,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return await event_service.search(filters, offset, limit)


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: UUID,
    event_service: Annotated[EventService, Depends(get_event_service)],
):
    return await event_service.get_event_response(event_id)


@router.post("/", response_model=EventResponse, status_code=201)
async def create_event(
    data: EventCreate,
    current_user: Annotated[User, Depends(require_permission(PERMISSION_EVENT_MANAGE))],
    event_service: Annotated[EventService, Depends(get_event_service)],
):
    event = await event_service.create_event(data)
    return await event_service.get_event_response(event.id)


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: UUID,
    data: EventUpdate,
    current_user: Annotated[User, Depends(require_permission(PERMISSION_EVENT_MANAGE))],
    event_service: Annotated[EventService, Depends(get_event_service)],
):
    await event_service.update_event(event_id, data)
    return await event_service.get_event_response(event_id)


@router.delete("/{event_id}", response_class=Response, status_code=204)
async def delete_event(
    event_id: UUID,
    current_user: Annotated[User, Depends(require_permission(PERMISSION_EVENT_MANAGE))],
    event_service: Annotated[EventService, Depends(get_event_service)],
):
    await event_service.delete_event(event_id)
    return Response(status_code=204)


@router.post("/batch-status", response_model=dict)
async def batch_update_status(
    data: BatchStatusUpdate,
    current_user: Annotated[User, Depends(require_permission(PERMISSION_EVENT_MANAGE))],
    event_service: Annotated[EventService, Depends(get_event_service)],
):
    success = 0
    errors = []
    for eid in data.event_ids:
        try:
            await event_service.update_event(eid, EventUpdate(status=data.status))
            success += 1
        except Exception as exc:
            errors.append({"event_id": str(eid), "error": str(exc)})
    return {"success": success, "errors": errors}
