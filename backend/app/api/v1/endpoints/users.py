"""User management endpoints — list users and change roles (admin only)."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.dependencies.auth import require_role
from app.dependencies.database import get_db
from app.models.enums import UserRole
from app.models.role import Role
from app.models.user import User
from app.schemas.auth import RoleInfo
from app.schemas.base import BaseSchema
from app.schemas.page import Page

router = APIRouter()


class UserResponse(BaseSchema):
    id: UUID
    username: str
    email: str
    role: RoleInfo
    is_active: bool


class ChangeRoleRequest(BaseModel):
    role_name: str = Field(min_length=1, max_length=100)


@router.get("/", response_model=Page[UserResponse])
async def list_users(
    current_user: Annotated[User, Depends(require_role(UserRole.administrator))],
    session: Annotated[AsyncSession, Depends(get_db)],
    offset: Annotated[int, Field(ge=0)] = 0,
    limit: Annotated[int, Field(ge=1, le=100)] = 20,
):
    count_result = await session.execute(select(User).order_by(User.username))
    all_users = list(count_result.scalars().all())
    total = len(all_users)

    items = all_users[offset : offset + limit]

    return Page[UserResponse](
        items=[
            UserResponse(
                id=u.id,
                username=u.username,
                email=u.email,
                role=RoleInfo(id=u.role.id, name=u.role.name),
                is_active=u.is_active,
            )
            for u in items
        ],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.patch("/{user_id}/role", response_model=UserResponse)
async def change_user_role(
    user_id: UUID,
    data: ChangeRoleRequest,
    current_user: Annotated[User, Depends(require_role(UserRole.administrator))],
    session: Annotated[AsyncSession, Depends(get_db)],
):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    role_result = await session.execute(select(Role).where(Role.name == data.role_name))
    role = role_result.scalar_one_or_none()
    if role is None:
        raise HTTPException(status_code=400, detail=f"Role '{data.role_name}' not found")

    user.role_id = role.id
    await session.commit()
    await session.refresh(user, ["role"])

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=RoleInfo(id=user.role.id, name=user.role.name),
        is_active=user.is_active,
    )


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)
    role_name: str = Field(default="editor")


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    data: CreateUserRequest,
    current_user: Annotated[User, Depends(require_role(UserRole.administrator))],
    session: Annotated[AsyncSession, Depends(get_db)],
):
    existing = await session.execute(select(User).where(User.username == data.username))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already taken")

    existing_email = await session.execute(select(User).where(User.email == data.email))
    if existing_email.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already taken")

    role_result = await session.execute(select(Role).where(Role.name == data.role_name))
    role = role_result.scalar_one_or_none()
    if role is None:
        raise HTTPException(status_code=400, detail=f"Role '{data.role_name}' not found")

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        role_id=role.id,
        is_active=True,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user, ["role"])

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=RoleInfo(id=user.role.id, name=user.role.name),
        is_active=user.is_active,
    )
