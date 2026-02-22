from fastapi import APIRouter
from app.api.v1.analysis import router as analysis_router
from app.api.v1.text_extraction import router as text_extraction_router

api_router = APIRouter()

# Include analysis routes
api_router.include_router(analysis_router)

# Include text extraction routes
api_router.include_router(text_extraction_router)

# Add other routers here as you expand the API
# api_router.include_router(other_router)
