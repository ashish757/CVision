"""
Pydantic schemas for Experience Quality Analysis module
"""

from pydantic import BaseModel, Field
from typing import Optional


class ExperienceAnalysisRequest(BaseModel):
    """Request model for experience analysis"""
    experience_text: str = Field(..., description="Raw experience text to analyze")
    entities: dict = Field(..., description="Extracted entities from resume")


class ExperienceAnalysisResponse(BaseModel):
    """Response model for experience quality analysis"""
    total_experience_years: int = Field(..., description="Total years of experience calculated")
    seniority_level: str = Field(..., description="Detected seniority level (Intern, Junior, Senior, etc.)")
    achievement_score: int = Field(..., description="Score based on quantified achievements (0-100)")
    experience_strength_score: int = Field(..., description="Overall experience strength score (0-100)")

    # Additional details for transparency
    detected_roles: list = Field(default_factory=list, description="List of detected job titles/roles")
    quantified_achievements: list = Field(default_factory=list, description="List of detected achievements")
    strong_verbs_count: int = Field(default=0, description="Count of strong action verbs detected")
    weak_verbs_count: int = Field(default=0, description="Count of weak action verbs detected")


class ExperienceAnalysisError(BaseModel):
    """Error response model for experience analysis"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
