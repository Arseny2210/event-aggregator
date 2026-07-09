"""Session middleware — ensures every visitor has a session_id cookie.

Sets httponly `session_id` and JS-readable `session_id_client` cookies
on every response if they are not already present in the request.
Also stores the session_id in request.state so endpoints can read it.
"""

import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

COOKIE_NAME = "session_id"
CLIENT_COOKIE_NAME = "session_id_client"
STATE_KEY = "session_id"
MAX_AGE = 365 * 24 * 60 * 60


class SessionMiddleware(BaseHTTPMiddleware):
    """Assigns a unique session ID to every visitor."""

    async def dispatch(self, request: Request, call_next) -> Response:
        session_id = request.cookies.get(COOKIE_NAME)
        is_new = session_id is None

        if is_new:
            session_id = str(uuid.uuid4())

        request.state.__setattr__(STATE_KEY, session_id)

        response = await call_next(request)

        if is_new:
            response.set_cookie(
                key=COOKIE_NAME,
                value=session_id,
                max_age=MAX_AGE,
                httponly=True,
                samesite="lax",
            )
            response.set_cookie(
                key=CLIENT_COOKIE_NAME,
                value=session_id,
                max_age=MAX_AGE,
                httponly=False,
                samesite="lax",
            )

        return response
