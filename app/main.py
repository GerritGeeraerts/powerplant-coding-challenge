from fastapi import FastAPI
from starlette.responses import RedirectResponse
from app.api.routes.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, 
    description=settings.PROJECT_DESCRIPTION
)

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
