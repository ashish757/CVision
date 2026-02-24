"""
Global Resume Scoring module for CVision AI Analysis Service

This module combines outputs from multiple analysis modules (Skills Intelligence,
Experience Analysis, etc.) into a comprehensive final resume score using configurable
weighted algorithms and generates actionable insights.

Features:
- Multi-component scoring system (Skills, Experience, Achievement, Structure)
- Configurable scoring weights for customization
- Detailed score breakdown and analysis
- Recommendation tiers and insights generation
- Critical skills bonus weighting
- Resume structure quality assessment
- Deterministic and rule-based scoring algorithms
- Comprehensive error handling and logging
"""

from .router import router
from .service import GlobalResumeScoring
from .schemas import (
    GlobalScoringRequest,
    GlobalScoringResponse,
    ScoringError,
    ScoringHealthResponse,
    ScoringWeights,
    SkillProficiency,
    ExperienceAnalysisData,
    ResumeStructuredSections,
    ScoreBreakdown
)

__all__ = [
    "router",
    "GlobalResumeScoring",
    "GlobalScoringRequest",
    "GlobalScoringResponse",
    "ScoringError",
    "ScoringHealthResponse",
    "ScoringWeights",
    "SkillProficiency",
    "ExperienceAnalysisData",
    "ResumeStructuredSections",
    "ScoreBreakdown"
]
