"""RolePermission DTOs."""

from pydantic import Field

from app.schemas.base import BaseSchema


class RolePermissionCreate(BaseSchema):
    role_id: int = Field(ge=1)
    permission_id: int = Field(ge=1)


class RolePermissionResponse(BaseSchema):
    role_id: int
    permission_id: int
