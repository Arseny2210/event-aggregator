from datetime import UTC, datetime

from fastapi import APIRouter

from app.core.constants import API_V1_PREFIX

router = APIRouter(prefix=API_V1_PREFIX, tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "timestamp": datetime.now(UTC).isoformat(),
    }
