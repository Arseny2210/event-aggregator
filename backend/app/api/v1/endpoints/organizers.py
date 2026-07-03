"""Organizer CRUD endpoints."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, Response
from fastapi import status as http_status

from app.api.v1.dependencies import get_organizer_service
from app.api.v1.schemas import Page
from app.schemas.organizer import OrganizerCreate, OrganizerResponse, OrganizerUpdate
from app.services.organizer import OrganizerService

router = APIRouter(prefix="/organizers", tags=["organizers"])


@router.get("", response_model=Page[OrganizerResponse])
async def list_organizers(
    service: Annotated[OrganizerService, Depends(get_organizer_service)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> Page[OrganizerResponse]:
    items, total = await service.list_organizers(offset, limit)
    return Page[OrganizerResponse](
        items=[OrganizerResponse.model_validate(o) for o in items],
        total=total,
        offset=offset,
        limit=limit,
        has_next=offset + limit < total,
    )


@router.get("/{organizer_id}", response_model=OrganizerResponse)
async def get_organizer(
    organizer_id: Annotated[UUID, Path()],
    service: Annotated[OrganizerService, Depends(get_organizer_service)],
) -> OrganizerResponse:
    organizer = await service.get_organizer(organizer_id)
    return OrganizerResponse.model_validate(organizer)


@router.post("", status_code=http_status.HTTP_201_CREATED, response_model=OrganizerResponse)
async def create_organizer(
    data: OrganizerCreate,
    service: Annotated[OrganizerService, Depends(get_organizer_service)],
) -> OrganizerResponse:
    organizer = await service.create_organizer(data)
    return OrganizerResponse.model_validate(organizer)


@router.patch("/{organizer_id}", response_model=OrganizerResponse)
async def update_organizer(
    organizer_id: Annotated[UUID, Path()],
    data: OrganizerUpdate,
    service: Annotated[OrganizerService, Depends(get_organizer_service)],
) -> OrganizerResponse:
    organizer = await service.update_organizer(organizer_id, data)
    return OrganizerResponse.model_validate(organizer)


@router.delete(
    "/{organizer_id}",
    status_code=http_status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_organizer(
    organizer_id: Annotated[UUID, Path()],
    service: Annotated[OrganizerService, Depends(get_organizer_service)],
) -> Response:
    await service.delete_organizer(organizer_id)
    return Response(status_code=http_status.HTTP_204_NO_CONTENT)
