"""Main application entry point."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.api.routes.v1.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.middleware import RequestLoggingMiddleware

# Get logger for this module
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan for the FastAPI application."""
    configure_logging()
    logger.info(f"Starting {settings.PROJECT_NAME}")
    yield
    logger.info(f"Shutting down {settings.PROJECT_NAME}")


def get_application() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application
    """
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        debug=settings.DEBUG,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(RequestLoggingMiddleware)
    application.include_router(api_router, prefix=settings.API_V1_STR)
    return application


app = get_application()


@app.get("/", tags=["Root"])  # type: ignore
def root() -> RedirectResponse:
    """Redirect to API documentation."""
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["Health"])  # type: ignore
def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
