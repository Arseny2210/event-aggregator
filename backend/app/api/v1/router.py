"""API v1 router. Feature routers are included here."""

from fastapi import APIRouter

from app.api.v1.endpoints.events import router as events_router
from app.api.v1.endpoints.import_jobs import router as import_jobs_router
from app.api.v1.endpoints.organizers import router as organizers_router
from app.api.v1.endpoints.participations import router as participations_router
from app.api.v1.endpoints.permissions import router as permissions_router
from app.api.v1.endpoints.roles import router as roles_router
from app.api.v1.endpoints.users import router as users_router

router = APIRouter(
    responses={
        400: {
            "description": "Bad request / business rule violation",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "business_rule_violation",
                            "message": "The request violates a business rule.",
                        }
                    }
                }
            },
        },
        404: {
            "description": "Resource not found",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "not_found",
                            "message": "The requested resource was not found.",
                        }
                    }
                }
            },
        },
        409: {
            "description": "Resource already exists",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "conflict",
                            "message": "A resource with the same identifier already exists.",
                        }
                    }
                }
            },
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "internal_error",
                            "message": "An unexpected error occurred.",
                        }
                    }
                }
            },
        },
    },
)

router.include_router(events_router)
router.include_router(organizers_router)
router.include_router(participations_router)
router.include_router(users_router)
router.include_router(roles_router)
router.include_router(permissions_router)
router.include_router(import_jobs_router)
