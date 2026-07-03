"""User read-only endpoints."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query

from app.api.v1.dependencies import get_user_service
from app.api.v1.schemas import Page
from app.schemas.user import UserResponse
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=Page[UserResponse])
async def list_users(
    service: Annotated[UserService, Depends(get_user_service)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    role_id: Annotated[int | None, Query(ge=1)] = None,
    active: Annotated[bool | None, Query()] = None,
) -> Page[UserResponse]:
    if role_id is not None and active is not None:
        raise HTTPException(
            400, "Multiple filters provided but combined filtering is not supported."
        )

    if role_id is not None:
        items, total = await service.list_users_by_role(role_id, offset, limit)
    elif active is not None:
        items, total = await service.list_active_users(offset, limit)
    else:
        items, total = await service.list_users(offset, limit)

    return Page[UserResponse](
        items=[UserResponse.model_validate(u) for u in items],
        total=total,
        offset=offset,
        limit=limit,
        has_next=offset + limit < total,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: Annotated[UUID, Path()],
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    user = await service.get_user(user_id)
    return UserResponse.model_validate(user)
