# app/api/routes/v1/router.py
from fastapi import APIRouter
from app.api.routes.v1 import productionplan

api_router = APIRouter()
api_router.include_router(productionplan.router, prefix="/productionplan", tags=["Production Plan"])

# app/main.py
from fastapi import FastAPI
# from base router import api_router

app = FastAPI(title="Power Plant Production API", description="API for calculating power plant production plans")

app.include_router(api_router, prefix="/api/v1")

# TODO: This ia double, in the main.py file there is also a health check keep one or the other if make sense
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}