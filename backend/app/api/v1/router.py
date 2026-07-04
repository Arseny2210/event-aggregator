"""API v1 router. Feature routers are included here."""

from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.events import router as events_router
from app.api.v1.endpoints.imports import router as imports_router

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

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(events_router, prefix="/events", tags=["events"])
router.include_router(imports_router, prefix="/imports", tags=["imports"])
