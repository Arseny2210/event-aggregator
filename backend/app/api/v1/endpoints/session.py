"""Session endpoint — returns the current session_id."""

from typing import Annotated

from fastapi import APIRouter, Cookie, Request
from pydantic import BaseModel

PARTICIPATION_COOKIE = "session_id"


class SessionResponse(BaseModel):
    session_id: str


router = APIRouter()


@router.get("/", response_model=SessionResponse)
async def get_session(
    request: Request,
    session_id: Annotated[str | None, Cookie(alias=PARTICIPATION_COOKIE)] = None,
) -> SessionResponse:
    sid = session_id or getattr(request.state, "session_id", None)
    if sid is None:
        sid = ""
    return SessionResponse(session_id=sid)
