from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.constants import PROJECT_NAME
from app.lifespan import lifespan
from app.middleware.cors import setup_cors
from app.middleware.error_handler import setup_error_handler
from app.routers.health import router as health_router


def create_app() -> FastAPI:
    docs_url = "/docs" if settings.openapi_docs_enabled else None
    redoc_url = "/redoc" if settings.openapi_docs_enabled else None
    openapi_url = "/openapi.json" if settings.openapi_schema_enabled else None

    app = FastAPI(
        title=PROJECT_NAME,
        description="Centralized university events platform API",
        version="1.0.0",
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
        lifespan=lifespan,
        openapi_tags=[
            {"name": "health", "description": "Health check endpoints"},
            {"name": "events", "description": "Event management and discovery"},
            {"name": "organizers", "description": "Organizer management"},
            {"name": "participation", "description": "Event participation registration"},
            {"name": "users", "description": "User management"},
            {"name": "roles", "description": "Role and permission management"},
            {"name": "imports", "description": "Excel import management"},
            {"name": "notifications", "description": "Notification management and delivery"},
            {"name": "statistics", "description": "Dashboard statistics"},
        ],
    )

    setup_cors(app)
    setup_error_handler(app)

    app.include_router(health_router)
    app.include_router(api_router)

    return app


app = create_app()
