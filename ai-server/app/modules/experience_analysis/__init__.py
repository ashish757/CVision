"""
Experience Quality Analysis module for CVision AI Analysis Service

This module evaluates the strength and quality of candidate's work experience
using rule-based signal detection and scoring algorithms.

Features:
- Total experience duration calculation from date ranges
- Role seniority level detection and scoring
- Quantified achievement signal detection
- Action verb strength analysis
- Comprehensive experience strength scoring
- Support for various date formats and experience patterns
- Extensible scoring weights and thresholds
"""

from .router import router
from .service import ExperienceAnalysisService
from .schemas import (
    ExperienceAnalysisRequest,
    ExperienceAnalysisResponse,
    ExperienceAnalysisError
)

__all__ = [
    "router",
    "ExperienceAnalysisService",
    "ExperienceAnalysisRequest",
    "ExperienceAnalysisResponse",
    "ExperienceAnalysisError"
]
