"""Participation endpoints — register, cancel, check status.

Uses cookie-based session_id (UUID v4) with 1-year expiry.
Reuses the existing ParticipationService.
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response
from pydantic import BaseModel

from app.api.v1.dependencies import get_participation_service
from app.schemas.participation import ParticipationResponse
from app.services.participation import ParticipationService

PARTICIPATION_COOKIE = "session_id"
COOKIE_MAX_AGE = 365 * 24 * 60 * 60  # 1 year


class ParticipationStatusResponse(BaseModel):
    is_registered: bool


def _get_or_create_session_id(response: Response, session_id: str | None) -> str:
    if session_id:
        return session_id
    sid = str(uuid.uuid4())
    response.set_cookie(
        key=PARTICIPATION_COOKIE,
        value=sid,
        max_age=COOKIE_MAX_AGE,
        httponly=True,
        samesite="lax",
    )
    return sid


router = APIRouter()


@router.post("/{event_id}/participate", response_model=ParticipationResponse, status_code=201)
async def register_for_event(
    event_id: uuid.UUID,
    response: Response,
    participation_service: Annotated[ParticipationService, Depends(get_participation_service)],
    session_id: Annotated[str | None, Cookie(alias=PARTICIPATION_COOKIE)] = None,
) -> ParticipationResponse:
    sid = _get_or_create_session_id(response, session_id)
    participation = await participation_service.register_participation(event_id, sid)
    return ParticipationResponse.model_validate(participation)


@router.delete("/{event_id}/participate", status_code=204)
async def cancel_participation(
    event_id: uuid.UUID,
    participation_service: Annotated[ParticipationService, Depends(get_participation_service)],
    session_id: Annotated[str | None, Cookie(alias=PARTICIPATION_COOKIE)] = None,
) -> Response:
    if session_id is None:
        return Response(status_code=204)
    await participation_service.cancel_participation(event_id, session_id)
    return Response(status_code=204)


@router.get("/{event_id}/participate", response_model=ParticipationStatusResponse)
async def get_participation_status(
    event_id: uuid.UUID,
    participation_service: Annotated[ParticipationService, Depends(get_participation_service)],
    session_id: Annotated[str | None, Cookie(alias=PARTICIPATION_COOKIE)] = None,
) -> ParticipationStatusResponse:
    if session_id is None:
        return ParticipationStatusResponse(is_registered=False)
    try:
        await participation_service.get_participation_by_event_and_session(event_id, session_id)
        return ParticipationStatusResponse(is_registered=True)
    except Exception:
        return ParticipationStatusResponse(is_registered=False)
