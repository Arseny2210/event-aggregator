"""Category endpoints — list and create."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import PERMISSION_EVENT_MANAGE
from app.dependencies.auth import require_permission
from app.dependencies.database import get_db
from app.models.category import Category
from app.models.user import User
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.transaction import transactional

router = APIRouter()


@router.get("/", response_model=list[CategoryResponse])
async def list_categories(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> list[CategoryResponse]:
    repo = CategoryRepository(session)
    categories = await repo.get_all()
    return [CategoryResponse.model_validate(c) for c in categories]


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    data: CategoryCreate,
    current_user: Annotated[User, Depends(require_permission(PERMISSION_EVENT_MANAGE))],
    session: Annotated[AsyncSession, Depends(get_db)],
) -> CategoryResponse:
    repo = CategoryRepository(session)
    category = Category(name=data.name, description=data.description)
    async with transactional(session):
        result = await repo.create(category)
    return CategoryResponse.model_validate(result)
