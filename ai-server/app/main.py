from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.analysis.router import router as analysis_router
from app.modules.parsing.router import router as parsing_router
from app.modules.text_extraction.router import router as text_extraction_router

from app.core import setup_logging, get_logger, log_startup_info, settings

# Configure logging early
setup_logging()

# Get logger for this module
logger = get_logger(__name__)

# Log startup information
log_startup_info()

# FastAPI app configuration
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# Include routers
app.include_router(analysis_router)
app.include_router(text_extraction_router)
app.include_router(parsing_router)

@app.get("/")
async def root():
    """Root endpoint providing service information"""
    return {
        "message": f"{settings.APP_NAME} is Online",
        "version": settings.APP_VERSION,
        "docs": settings.DOCS_URL,
        "health": "/analyze/health"
    }

@app.get("/health")
async def health():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }
