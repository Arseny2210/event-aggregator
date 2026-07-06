"""Organizer endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.v1.dependencies import get_organizer_service
from app.schemas.organizer import OrganizerResponse
from app.schemas.page import Page
from app.services.organizer import OrganizerService

router = APIRouter()


@router.get("/", response_model=Page[OrganizerResponse])
async def list_organizers(
    organizer_service: Annotated[OrganizerService, Depends(get_organizer_service)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    items, total = await organizer_service.list_organizers(offset, limit)
    return Page[OrganizerResponse](
        items=[
            OrganizerResponse(
                id=o.id,
                name=o.name,
                department=o.department,
                email=o.email,
                phone=o.phone,
                website=o.website,
                created_at=o.created_at,
                updated_at=o.updated_at,
            )
            for o in items
        ],
        total=total,
        offset=offset,
        limit=limit,
    )
