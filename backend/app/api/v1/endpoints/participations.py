"""Participation endpoints."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response
from fastapi import status as http_status

from app.api.v1.dependencies import get_participation_service
from app.api.v1.schemas import Page
from app.schemas.participation import ParticipationCreate, ParticipationResponse
from app.services.participation import ParticipationService

router = APIRouter(prefix="/participations", tags=["participation"])


@router.get("", response_model=Page[ParticipationResponse])
async def list_participations(
    service: Annotated[ParticipationService, Depends(get_participation_service)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    event_id: Annotated[UUID | None, Query()] = None,
    session_id: Annotated[str | None, Query()] = None,
) -> Page[ParticipationResponse]:
    if event_id is not None and session_id is not None:
        raise HTTPException(
            400, "Multiple filters provided but combined filtering is not supported."
        )
    if event_id is not None:
        items, total = await service.list_participations_for_event(event_id, offset, limit)
    elif session_id is not None:
        items = await service.list_participations_for_session(session_id)
        return Page[ParticipationResponse](
            items=[ParticipationResponse.model_validate(p) for p in items],
            total=len(items),
            offset=0,
            limit=len(items),
            has_next=False,
        )
    else:
        raise HTTPException(400, "At least one filter is required: event_id or session_id.")

    return Page[ParticipationResponse](
        items=[ParticipationResponse.model_validate(p) for p in items],
        total=total,
        offset=offset,
        limit=limit,
        has_next=offset + limit < total,
    )


@router.get("/{participation_id}", response_model=ParticipationResponse)
async def get_participation(
    participation_id: Annotated[UUID, Path()],
    service: Annotated[ParticipationService, Depends(get_participation_service)],
) -> ParticipationResponse:
    participation = await service.get_participation(participation_id)
    return ParticipationResponse.model_validate(participation)


@router.post("", status_code=http_status.HTTP_201_CREATED, response_model=ParticipationResponse)
async def create_participation(
    data: ParticipationCreate,
    service: Annotated[ParticipationService, Depends(get_participation_service)],
) -> ParticipationResponse:
    participation = await service.register_participation(data.event_id, data.session_id)
    return ParticipationResponse.model_validate(participation)


@router.delete(
    "/{participation_id}",
    status_code=http_status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_participation(
    participation_id: Annotated[UUID, Path()],
    service: Annotated[ParticipationService, Depends(get_participation_service)],
) -> Response:
    participation = await service.get_participation(participation_id)
    await service.cancel_participation(participation.event_id, participation.session_id)
    return Response(status_code=http_status.HTTP_204_NO_CONTENT)
