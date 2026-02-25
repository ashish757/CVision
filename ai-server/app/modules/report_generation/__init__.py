"""
Evaluation Report Generation module for CVision AI Analysis Service

This module converts resume scores and analysis outputs into structured,
human-readable evaluation reports with actionable insights and recommendations.

Features:
- Comprehensive evaluation report generation
- Rule-based strengths and weaknesses identification
- Actionable recommendations with prioritization
- Detailed skills, experience, and structure analysis
- Configurable evaluation thresholds and criteria
- Profile tier classification (Strong, Moderate, Developing)
- Next steps and career development guidance
- Deterministic and consistent report generation
- Extensible framework for future AI-generated feedback
"""

from .router import router
from .service import EvaluationReportGenerator
from .schemas import (
    EvaluationReportRequest,
    EvaluationReportResponse,
    ReportGenerationError,
    ReportHealthResponse,
    ReportTemplateConfig,
    SkillEvaluation,
    ExperienceEvaluation,
    ScoringResultData,
    EvaluationSection
)

__all__ = [
    "router",
    "EvaluationReportGenerator",
    "EvaluationReportRequest",
    "EvaluationReportResponse",
    "ReportGenerationError",
    "ReportHealthResponse",
    "ReportTemplateConfig",
    "SkillEvaluation",
    "ExperienceEvaluation",
    "ScoringResultData",
    "EvaluationSection"
]
