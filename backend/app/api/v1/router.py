"""API v1 router. Feature routers are included here."""

from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.categories import router as categories_router
from app.api.v1.endpoints.dashboard import router as dashboard_router
from app.api.v1.endpoints.events import router as events_router
from app.api.v1.endpoints.imports import router as imports_router
from app.api.v1.endpoints.notifications import router as notifications_router
from app.api.v1.endpoints.participation import router as participation_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(categories_router, prefix="/categories", tags=["categories"])
router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
router.include_router(events_router, prefix="/events", tags=["events"])
router.include_router(imports_router, prefix="/imports", tags=["imports"])
router.include_router(notifications_router, prefix="/notifications", tags=["notifications"])
router.include_router(participation_router, prefix="/events", tags=["participation"])
