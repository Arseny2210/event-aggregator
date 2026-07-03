"""Role read-only endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.api.v1.dependencies import get_role_service
from app.api.v1.schemas import Page
from app.schemas.role import RoleResponse
from app.services.role import RoleService

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=Page[RoleResponse])
async def list_roles(
    service: Annotated[RoleService, Depends(get_role_service)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> Page[RoleResponse]:
    items, total = await service.list_roles(offset, limit)
    return Page[RoleResponse](
        items=[RoleResponse.model_validate(r) for r in items],
        total=total,
        offset=offset,
        limit=limit,
        has_next=offset + limit < total,
    )


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: Annotated[int, Path(ge=1)],
    service: Annotated[RoleService, Depends(get_role_service)],
) -> RoleResponse:
    role = await service.get_role(role_id)
    return RoleResponse.model_validate(role)
