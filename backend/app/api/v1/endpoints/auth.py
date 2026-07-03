"""Authentication endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response

from app.dependencies.auth import (
    get_auth_service,
    get_current_active_user,
    get_current_user,
)
from app.models.user import User
from app.schemas.auth import LoginRequest, RefreshTokenRequest, TokenResponse, UserMeResponse
from app.services.auth import AuthService

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    result = await auth_service.login(data.username, data.password)
    return TokenResponse(access_token=result.access_token, refresh_token=result.refresh_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    data: RefreshTokenRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    result = await auth_service.refresh_access_token(data.refresh_token)
    return TokenResponse(access_token=result.access_token, refresh_token=result.refresh_token)


@router.post("/logout", response_class=Response, status_code=204)
async def logout(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return Response(status_code=204)


@router.get("/me", response_model=UserMeResponse)
async def me(
    current_user: Annotated[User, Depends(get_current_active_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return auth_service.build_me_response(current_user)
