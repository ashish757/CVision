from fastapi import APIRouter
from app.api.v1.analysis import router as analysis_router

api_router = APIRouter()

# Include analysis routes
api_router.include_router(analysis_router)

# Add other routers here as you expand the API
# api_router.include_router(other_router)
