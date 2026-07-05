"""Category endpoints — read-only list."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryResponse

router = APIRouter()


@router.get("/", response_model=list[CategoryResponse])
async def list_categories(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> list[CategoryResponse]:
    repo = CategoryRepository(session)
    categories = await repo.get_all()
    return [CategoryResponse.model_validate(c) for c in categories]
