"""ImportJob read-only endpoints."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query

from app.api.v1.dependencies import get_import_job_service
from app.api.v1.schemas import Page
from app.models.enums import ImportStatus
from app.schemas.import_job import ImportJobResponse
from app.services.import_job import ImportJobService

router = APIRouter(prefix="/imports", tags=["imports"])


@router.get("", response_model=Page[ImportJobResponse])
async def list_import_jobs(
    service: Annotated[ImportJobService, Depends(get_import_job_service)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    user_id: Annotated[UUID | None, Query()] = None,
    status: Annotated[ImportStatus | None, Query()] = None,
) -> Page[ImportJobResponse]:
    if user_id is not None and status is not None:
        raise HTTPException(
            400, "Multiple filters provided but combined filtering is not supported."
        )

    if user_id is not None:
        items, total = await service.list_import_jobs_by_user(user_id, offset, limit)
    elif status is not None:
        items, total = await service.list_import_jobs_by_status(status, offset, limit)
    else:
        items, total = await service.list_import_jobs(offset, limit)

    return Page[ImportJobResponse](
        items=[ImportJobResponse.model_validate(j) for j in items],
        total=total,
        offset=offset,
        limit=limit,
        has_next=offset + limit < total,
    )


@router.get("/{import_job_id}", response_model=ImportJobResponse)
async def get_import_job(
    import_job_id: Annotated[UUID, Path()],
    service: Annotated[ImportJobService, Depends(get_import_job_service)],
) -> ImportJobResponse:
    job = await service.get_import_job(import_job_id)
    return ImportJobResponse.model_validate(job)
