"""
Skill Analysis module for CVision AI Analysis Service

This module provides intelligent skill proficiency analysis using context-based
signal detection from resume text. It analyzes skills to determine proficiency
levels using years of experience, level keywords, and action verbs.

Features:
- Context-based signal detection (±100 character windows)
- Years of experience pattern matching
- Level keyword recognition (expert, intermediate, beginner, etc.)
- Action verb strength analysis (strong vs weak verbs)
- Weighted scoring with configurable thresholds
- Confidence level calculation
- Comprehensive proficiency reporting
"""

from .router import router
from .service import SkillIntelligenceEngine
from .schemas import (
    SkillAnalysisRequest,
    SkillAnalysisResponse,
    SkillAnalysisError,
    SkillProficiencyResult,
    SkillLevel,
    SkillContextSignal
)

__all__ = [
    "router",
    "SkillIntelligenceEngine",
    "SkillAnalysisRequest",
    "SkillAnalysisResponse",
    "SkillAnalysisError",
    "SkillProficiencyResult",
    "SkillLevel",
    "SkillContextSignal"
]
