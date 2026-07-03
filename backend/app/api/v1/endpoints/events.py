"""Event CRUD endpoints."""

from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response
from fastapi import status as http_status

from app.api.v1.dependencies import get_event_service
from app.api.v1.schemas import Page
from app.models.enums import EventStatus
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from app.services.event import EventService

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=Page[EventResponse])
async def list_events(
    service: Annotated[EventService, Depends(get_event_service)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    sort_by: Annotated[str | None, Query(pattern=r"^-?(date|title|created_at)$")] = None,
    q: Annotated[str | None, Query()] = None,
    organizer_id: Annotated[UUID | None, Query()] = None,
    status: Annotated[EventStatus | None, Query()] = None,
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
) -> Page[EventResponse]:
    non_date = sum(1 for f in [q, organizer_id, status] if f is not None)
    date_count = 1 if (start_date is not None or end_date is not None) else 0
    if non_date + date_count > 1:
        raise HTTPException(
            400, "Multiple filters provided but combined filtering is not supported."
        )

    if q is not None:
        items, total = await service.search_events(q, offset, limit)
    elif organizer_id is not None:
        items, total = await service.list_events_by_organizer(organizer_id, offset, limit)
    elif status is not None:
        items, total = await service.list_events_by_status(status, offset, limit)
    elif start_date is not None or end_date is not None:
        if start_date is None or end_date is None:
            raise HTTPException(
                400, "Both start_date and end_date are required for date range filtering."
            )
        items, total = await service.list_events_by_date_range(start_date, end_date, offset, limit)
    else:
        items, total = await service.list_events(offset, limit, sort_by)

    return Page[EventResponse](
        items=[EventResponse.model_validate(e) for e in items],
        total=total,
        offset=offset,
        limit=limit,
        has_next=offset + limit < total,
    )


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: Annotated[UUID, Path()],
    service: Annotated[EventService, Depends(get_event_service)],
) -> EventResponse:
    event = await service.get_event(event_id)
    return EventResponse.model_validate(event)


@router.post("", status_code=http_status.HTTP_201_CREATED, response_model=EventResponse)
async def create_event(
    data: EventCreate,
    service: Annotated[EventService, Depends(get_event_service)],
) -> EventResponse:
    event = await service.create_event(data)
    return EventResponse.model_validate(event)


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: Annotated[UUID, Path()],
    data: EventUpdate,
    service: Annotated[EventService, Depends(get_event_service)],
) -> EventResponse:
    event = await service.update_event(event_id, data)
    return EventResponse.model_validate(event)


@router.delete("/{event_id}", status_code=http_status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_event(
    event_id: Annotated[UUID, Path()],
    service: Annotated[EventService, Depends(get_event_service)],
) -> Response:
    await service.delete_event(event_id)
    return Response(status_code=http_status.HTTP_204_NO_CONTENT)
