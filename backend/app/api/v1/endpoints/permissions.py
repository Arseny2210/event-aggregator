"""Permission read-only endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.api.v1.dependencies import get_permission_service
from app.api.v1.schemas import Page
from app.schemas.permission import PermissionResponse
from app.services.permission import PermissionService

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.get("", response_model=Page[PermissionResponse])
async def list_permissions(
    service: Annotated[PermissionService, Depends(get_permission_service)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> Page[PermissionResponse]:
    items, total = await service.list_permissions(offset, limit)
    return Page[PermissionResponse](
        items=[PermissionResponse.model_validate(p) for p in items],
        total=total,
        offset=offset,
        limit=limit,
        has_next=offset + limit < total,
    )


@router.get("/{permission_id}", response_model=PermissionResponse)
async def get_permission(
    permission_id: Annotated[int, Path(ge=1)],
    service: Annotated[PermissionService, Depends(get_permission_service)],
) -> PermissionResponse:
    permission = await service.get_permission(permission_id)
    return PermissionResponse.model_validate(permission)
