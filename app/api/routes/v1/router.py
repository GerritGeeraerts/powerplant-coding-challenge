"""API router for version 1 of the API."""


from fastapi import APIRouter, FastAPI

from app.api.routes.v1 import productionplan

api_router = APIRouter()
api_router.include_router(productionplan.router, prefix="/productionplan", tags=["Production Plan"])

# from base router import api_router

app = FastAPI(
    title="Power Plant Production API",
    description="API for calculating power plant production plans",
)

app.include_router(api_router, prefix="/api/v1")

"""API router for version 1 of the API."""
