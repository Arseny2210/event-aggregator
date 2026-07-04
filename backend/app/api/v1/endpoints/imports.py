"""Import endpoints — Excel file upload, import history, and per-row reports."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, UploadFile

from app.api.v1.dependencies import get_import_job_service
from app.api.v1.schemas import Page
from app.core.constants import PERMISSION_IMPORT_CREATE, PERMISSION_IMPORT_VIEW
from app.dependencies.auth import require_permission, require_role
from app.models.enums import ImportRowStatus, ImportStatus, UserRole
from app.models.import_job import ImportJob
from app.models.user import User
from app.schemas.import_job import ImportJobResponse, ImportSummary
from app.schemas.import_row_result import RowResultResponse
from app.services.import_job import ImportJobService

router = APIRouter()


def _build_import_job_response(job: ImportJob) -> ImportJobResponse:
    return ImportJobResponse(
        id=job.id,
        filename=job.filename,
        status=job.status,
        created_by=job.created_by,
        created_at=job.created_at,
        summary=ImportSummary(
            total_rows=job.total_rows,
            processed_rows=job.processed_rows,
            imported_rows=job.imported_rows,
            failed_rows=job.failed_rows,
            warning_rows=job.warning_rows,
            duration=job.duration,
            started_at=job.started_at,
            finished_at=job.finished_at,
        ),
    )


@router.post("/", response_model=ImportJobResponse, status_code=201)
async def upload_import(
    file: Annotated[UploadFile, "Excel file (.xlsx, .xls)"],
    current_user: Annotated[User, Depends(require_permission(PERMISSION_IMPORT_CREATE))],
    import_service: Annotated[ImportJobService, Depends(get_import_job_service)],
):
    content = await file.read()
    job = await import_service.upload_file(file.filename or "upload.xlsx", content, current_user)
    return _build_import_job_response(job)


@router.get("/", response_model=Page[ImportJobResponse])
async def list_imports(
    current_user: Annotated[User, Depends(require_permission(PERMISSION_IMPORT_VIEW))],
    import_service: Annotated[ImportJobService, Depends(get_import_job_service)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    status: Annotated[ImportStatus | None, Query()] = None,
    user_id: Annotated[str | None, Query()] = None,
):
    if status is not None and user_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Filter by either status or user_id, not both.",
        )
    if status is not None:
        items, total = await import_service.list_import_jobs_by_status(status, offset, limit)
    elif user_id is not None:
        try:
            uid = UUID(user_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid user_id UUID format.") from None
        items, total = await import_service.list_import_jobs_by_user(uid, offset, limit)
    else:
        items, total = await import_service.list_import_jobs(offset, limit)
    return Page[ImportJobResponse](
        items=[_build_import_job_response(j) for j in items],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.get("/{import_id}", response_model=ImportJobResponse)
async def get_import(
    import_id: str,
    current_user: Annotated[User, Depends(require_permission(PERMISSION_IMPORT_VIEW))],
    import_service: Annotated[ImportJobService, Depends(get_import_job_service)],
):
    job = await import_service.get_import_job(UUID(import_id))
    return _build_import_job_response(job)


@router.get("/{import_id}/rows", response_model=Page[RowResultResponse])
async def get_import_rows(
    import_id: str,
    current_user: Annotated[User, Depends(require_permission(PERMISSION_IMPORT_VIEW))],
    import_service: Annotated[ImportJobService, Depends(get_import_job_service)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    status: Annotated[ImportRowStatus | None, Query()] = None,
):
    items, total = await import_service.list_row_results(
        UUID(import_id),
        offset,
        limit,
        status,
    )
    return Page[RowResultResponse](
        items=[
            RowResultResponse(
                id=r.id,
                import_job_id=r.import_job_id,
                row_number=r.row_number,
                status=r.status,
                created_entity_id=r.created_entity_id,
                error_code=r.error_code,
                error_message=r.error_message,
                created_at=r.created_at,
            )
            for r in items
        ],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.delete("/{import_id}", response_class=Response, status_code=204)
async def delete_import(
    import_id: str,
    current_user: Annotated[User, Depends(require_role(UserRole.administrator))],
    import_service: Annotated[ImportJobService, Depends(get_import_job_service)],
):
    await import_service.delete_import_job(UUID(import_id))
    return Response(status_code=204)
