from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# FastAPI app configuration
app = FastAPI(
    title="CVision AI Analysis Service",
    description="AI-powered resume analysis service for extracting skills, experience, and scoring resumes",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint providing service information"""
    return {
        "message": "CVision AI Analysis Service is Online",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/analyze/health"
    }

@app.get("/health")
async def health():
    """Simple health check endpoint"""
    return {"status": "healthy"}
