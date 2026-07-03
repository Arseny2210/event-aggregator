"""Password hashing and JWT token utilities.

Pure functions with no database or FastAPI dependencies.
"""

import uuid as _uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from passlib.context import CryptContext

from app.core.config import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass(frozen=True, slots=True)
class TokenPayload:
    sub: str
    exp: int
    iat: int
    type: str
    jti: str


def hash_password(plain: str) -> str:
    return _pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return _pwd_context.verify(plain, hashed)


def _create_token(user_id: UUID, token_type: str, expires_delta: timedelta) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        "type": token_type,
        "jti": _uuid.uuid4().hex,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(user_id: UUID) -> str:
    return _create_token(
        user_id,
        "access",
        timedelta(minutes=settings.access_token_expire_minutes),
    )


def create_refresh_token(user_id: UUID) -> str:
    return _create_token(
        user_id,
        "refresh",
        timedelta(days=settings.refresh_token_expire_days),
    )


def decode_token(token: str) -> TokenPayload:
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    return TokenPayload(
        sub=payload["sub"],
        exp=payload["exp"],
        iat=payload["iat"],
        type=payload["type"],
        jti=payload["jti"],
    )
