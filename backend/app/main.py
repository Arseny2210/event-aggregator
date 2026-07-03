from fastapi import FastAPI

from app.core.constants import PROJECT_NAME
from app.lifespan import lifespan
from app.middleware.cors import setup_cors
from app.middleware.error_handler import setup_error_handler
from app.routers.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=PROJECT_NAME,
        lifespan=lifespan,
    )

    setup_cors(app)
    setup_error_handler(app)

    app.include_router(health_router)

    return app


app = create_app()
