import logging
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from app.api.routes.v1.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from contextlib import asynccontextmanager

from app.middleware import RequestLoggingMiddleware

# Get logger for this module
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info(f"Starting {settings.PROJECT_NAME}")
    yield
    # Shutdown logic
    logger.info(f"Shutting down {settings.PROJECT_NAME}")

app = FastAPI(
    title=settings.PROJECT_NAME, 
    description=settings.PROJECT_DESCRIPTION,
    lifespan=lifespan
)

app.add_middleware(RequestLoggingMiddleware)

# Include the API router with the correct prefix
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Root"])
def root():
    """Redirect to API documentation"""
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}