"""Dashboard statistics endpoints."""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.v1.dependencies import get_statistics_service
from app.core.constants import PERMISSION_STATISTICS_VIEW
from app.dependencies.auth import require_permission
from app.models.user import User
from app.schemas.statistics import (
    ChartDataResponse,
    DashboardOverviewResponse,
    EventStatisticsResponse,
    ImportStatisticsResponse,
    ParticipationStatisticsResponse,
    TimeRange,
    TimeRangeFilter,
    UserStatisticsResponse,
)
from app.services.statistics import StatisticsService

router = APIRouter()


@router.get("/", response_model=DashboardOverviewResponse)
async def get_dashboard_overview(
    stat_service: Annotated[StatisticsService, Depends(get_statistics_service)],
    current_user: Annotated[User, Depends(require_permission(PERMISSION_STATISTICS_VIEW))],
    period: Annotated[TimeRange | None, Query()] = None,
    date_from: Annotated[date | None, Query()] = None,
    date_to: Annotated[date | None, Query()] = None,
):
    try:
        filters = TimeRangeFilter(period=period, date_from=date_from, date_to=date_to)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return await stat_service.get_dashboard_overview(filters)


@router.get("/events", response_model=EventStatisticsResponse)
async def get_event_statistics(
    stat_service: Annotated[StatisticsService, Depends(get_statistics_service)],
    current_user: Annotated[User, Depends(require_permission(PERMISSION_STATISTICS_VIEW))],
    period: Annotated[TimeRange | None, Query()] = None,
    date_from: Annotated[date | None, Query()] = None,
    date_to: Annotated[date | None, Query()] = None,
):
    try:
        filters = TimeRangeFilter(period=period, date_from=date_from, date_to=date_to)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return await stat_service.get_event_statistics(filters)


@router.get("/imports", response_model=ImportStatisticsResponse)
async def get_import_statistics(
    stat_service: Annotated[StatisticsService, Depends(get_statistics_service)],
    current_user: Annotated[User, Depends(require_permission(PERMISSION_STATISTICS_VIEW))],
    period: Annotated[TimeRange | None, Query()] = None,
    date_from: Annotated[date | None, Query()] = None,
    date_to: Annotated[date | None, Query()] = None,
):
    try:
        filters = TimeRangeFilter(period=period, date_from=date_from, date_to=date_to)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return await stat_service.get_import_statistics(filters)


@router.get("/users", response_model=UserStatisticsResponse)
async def get_user_statistics(
    stat_service: Annotated[StatisticsService, Depends(get_statistics_service)],
    current_user: Annotated[User, Depends(require_permission(PERMISSION_STATISTICS_VIEW))],
    period: Annotated[TimeRange | None, Query()] = None,
    date_from: Annotated[date | None, Query()] = None,
    date_to: Annotated[date | None, Query()] = None,
):
    try:
        filters = TimeRangeFilter(period=period, date_from=date_from, date_to=date_to)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return await stat_service.get_user_statistics(filters)


@router.get("/participations", response_model=ParticipationStatisticsResponse)
async def get_participation_statistics(
    stat_service: Annotated[StatisticsService, Depends(get_statistics_service)],
    current_user: Annotated[User, Depends(require_permission(PERMISSION_STATISTICS_VIEW))],
    period: Annotated[TimeRange | None, Query()] = None,
    date_from: Annotated[date | None, Query()] = None,
    date_to: Annotated[date | None, Query()] = None,
):
    try:
        filters = TimeRangeFilter(period=period, date_from=date_from, date_to=date_to)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return await stat_service.get_participation_statistics(filters)


@router.get("/charts", response_model=ChartDataResponse)
async def get_chart_data(
    stat_service: Annotated[StatisticsService, Depends(get_statistics_service)],
    current_user: Annotated[User, Depends(require_permission(PERMISSION_STATISTICS_VIEW))],
    period: Annotated[TimeRange | None, Query()] = None,
    date_from: Annotated[date | None, Query()] = None,
    date_to: Annotated[date | None, Query()] = None,
):
    try:
        filters = TimeRangeFilter(period=period, date_from=date_from, date_to=date_to)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return await stat_service.get_chart_data(filters)
