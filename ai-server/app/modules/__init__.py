"""
Modules package for CVision AI Analysis Service

This package contains feature-based modules organized as separate components.
Each module contains its own routers, services, and schemas.
"""

from .analysis.router import router as analysis_router
from .text_extraction.router import router as text_extraction_router
from .parsing.router import router as parsing_router
from .skill_analysis.router import router as skill_analysis_router
from .experience_analysis.router import router as experience_analysis_router
from .scoring.router import router as scoring_router

__all__ = [
    "analysis_router",
    "text_extraction_router",
    "parsing_router",
    "skill_analysis_router",
    "experience_analysis_router",
    "scoring_router"
]
