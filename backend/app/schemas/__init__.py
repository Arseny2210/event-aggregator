"""Pydantic v2 domain DTOs for the Event Aggregator application."""

from app.schemas.auth import LoginRequest, RefreshTokenRequest, TokenResponse, UserMeResponse
from app.schemas.event import EventBase, EventCreate, EventResponse, EventUpdate
from app.schemas.import_job import ImportJobResponse
from app.schemas.organizer import OrganizerBase, OrganizerCreate, OrganizerResponse, OrganizerUpdate
from app.schemas.participation import ParticipationCreate, ParticipationResponse
from app.schemas.permission import PermissionResponse
from app.schemas.role import RoleResponse
from app.schemas.role_permission import RolePermissionCreate, RolePermissionResponse
from app.schemas.user import UserBase, UserCreate, UserResponse, UserUpdate

__all__ = [
    "EventBase",
    "EventCreate",
    "EventResponse",
    "EventUpdate",
    "ImportJobResponse",
    "LoginRequest",
    "OrganizerBase",
    "OrganizerCreate",
    "OrganizerResponse",
    "OrganizerUpdate",
    "ParticipationCreate",
    "ParticipationResponse",
    "PermissionResponse",
    "RefreshTokenRequest",
    "RolePermissionCreate",
    "RolePermissionResponse",
    "RoleResponse",
    "TokenResponse",
    "UserBase",
    "UserCreate",
    "UserMeResponse",
    "UserResponse",
    "UserUpdate",
]
