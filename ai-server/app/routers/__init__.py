"""
Routers module for CVision AI Analysis Service

This module contains all API route handlers organized by feature.
"""
from .analysis import router as analysis_router
from .text_extraction import router as text_extraction_router

__all__ = [
    "analysis_router",
    "text_extraction_router"
]
