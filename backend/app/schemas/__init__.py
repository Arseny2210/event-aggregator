"""Pydantic v2 domain DTOs for the Event Aggregator application."""

from app.schemas.auth import LoginRequest, RefreshTokenRequest, TokenResponse, UserMeResponse
from app.schemas.event import EventBase, EventCreate, EventResponse, EventUpdate
from app.schemas.event_search import EventSearchFilters, EventSort
from app.schemas.import_job import ImportJobResponse, ImportSummary
from app.schemas.import_row import EventExcelRow
from app.schemas.import_row_result import RowResultResponse
from app.schemas.notification import (
    NotificationContext,
    NotificationResponse,
    NotificationTemplateResponse,
    SendNotificationRequest,
    SendTestNotificationRequest,
)
from app.schemas.organizer import OrganizerBase, OrganizerCreate, OrganizerResponse, OrganizerUpdate
from app.schemas.page import Page
from app.schemas.participation import ParticipationCreate, ParticipationResponse
from app.schemas.permission import PermissionResponse
from app.schemas.role import RoleResponse
from app.schemas.role_permission import RolePermissionCreate, RolePermissionResponse
from app.schemas.statistics import (
    ChartDataResponse,
    ChartSeries,
    DashboardOverviewResponse,
    EventStatisticsResponse,
    EventStatusCounts,
    ImportStatisticsResponse,
    ImportStatusCounts,
    OrganizerStatisticsResponse,
    OrganizerSummary,
    ParticipationStatisticsResponse,
    ParticipationStatusCounts,
    RoleUserCountResponse,
    TimeRange,
    TimeRangeFilter,
    TimeSeriesPoint,
    UserStatisticsResponse,
)
from app.schemas.user import UserBase, UserCreate, UserResponse, UserUpdate

__all__ = [
    "ChartDataResponse",
    "ChartSeries",
    "DashboardOverviewResponse",
    "EventBase",
    "EventCreate",
    "EventExcelRow",
    "EventResponse",
    "EventSearchFilters",
    "EventSort",
    "EventStatisticsResponse",
    "EventStatusCounts",
    "EventUpdate",
    "ImportJobResponse",
    "ImportStatisticsResponse",
    "ImportStatusCounts",
    "ImportSummary",
    "LoginRequest",
    "NotificationContext",
    "NotificationResponse",
    "NotificationTemplateResponse",
    "OrganizerBase",
    "OrganizerCreate",
    "OrganizerResponse",
    "OrganizerStatisticsResponse",
    "OrganizerSummary",
    "OrganizerUpdate",
    "Page",
    "ParticipationCreate",
    "ParticipationResponse",
    "ParticipationStatisticsResponse",
    "ParticipationStatusCounts",
    "PermissionResponse",
    "RefreshTokenRequest",
    "RolePermissionCreate",
    "RolePermissionResponse",
    "RoleResponse",
    "RoleUserCountResponse",
    "RowResultResponse",
    "SendNotificationRequest",
    "SendTestNotificationRequest",
    "TimeRange",
    "TimeRangeFilter",
    "TimeSeriesPoint",
    "TokenResponse",
    "UserBase",
    "UserCreate",
    "UserMeResponse",
    "UserResponse",
    "UserStatisticsResponse",
    "UserUpdate",
]
