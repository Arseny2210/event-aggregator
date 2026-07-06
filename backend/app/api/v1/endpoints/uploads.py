"""Image upload endpoint."""

import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from app.core.config import settings
from app.core.storage import LocalStorageBackend

router = APIRouter()

_ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
_ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}

_storage = LocalStorageBackend()


@router.post("/image")
async def upload_image(file: UploadFile):
    ext = Path(file.filename or "").suffix.lower()
    if ext not in _ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file extension: {ext}")

    if file.content_type not in _ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400, detail=f"Unsupported content type: {file.content_type}"
        )

    content = await file.read()

    if len(content) > settings.max_upload_size_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {settings.max_upload_size_bytes} bytes.",
        )

    unique_name = f"{uuid.uuid4().hex}{ext}"
    await _storage.save(unique_name, content)

    return {"url": f"/uploads/{unique_name}"}
