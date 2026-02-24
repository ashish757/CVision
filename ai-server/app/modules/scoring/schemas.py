"""
Pydantic schemas for Global Resume Scoring module
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class SkillProficiency(BaseModel):
    """Individual skill proficiency data"""
    skill: str = Field(..., description="Name of the skill")
    score: int = Field(..., description="Proficiency score (0-100)")
    level: str = Field(..., description="Proficiency level (Beginner, Intermediate, Expert)")
    years_experience: Optional[int] = Field(None, description="Years of experience with this skill")


class ExperienceAnalysisData(BaseModel):
    """Experience analysis results"""
    total_experience_years: int = Field(..., description="Total years of professional experience")
    seniority_level: str = Field(..., description="Detected seniority level")
    achievement_score: int = Field(..., description="Score based on quantified achievements")
    experience_strength_score: int = Field(..., description="Overall experience strength score")
    strong_verbs_count: int = Field(default=0, description="Count of strong action verbs")
    weak_verbs_count: int = Field(default=0, description="Count of weak action verbs")


class ResumeStructuredSections(BaseModel):
    """Structured resume sections"""
    summary: str = Field(default="", description="Professional summary section")
    skills: str = Field(default="", description="Technical skills section")
    experience: str = Field(default="", description="Work experience section")
    education: str = Field(default="", description="Education section")
    projects: str = Field(default="", description="Projects section")
    certifications: str = Field(default="", description="Certifications section")
    other: str = Field(default="", description="Other content")


class ScoreBreakdown(BaseModel):
    """Detailed score breakdown"""
    skills_score: float = Field(..., description="Skills component score (0-100)")
    experience_score: float = Field(..., description="Experience component score (0-100)")
    achievement_score: float = Field(..., description="Achievement component score (0-100)")
    structure_score: float = Field(..., description="Resume structure score (0-100)")

    # Additional breakdown details
    skills_count: int = Field(default=0, description="Number of skills detected")
    average_skill_proficiency: float = Field(default=0.0, description="Average skill proficiency level")
    critical_skills_bonus: float = Field(default=0.0, description="Bonus for critical skills")
    missing_sections: List[str] = Field(default_factory=list, description="List of missing important sections")
    experience_years: int = Field(default=0, description="Total years of experience")
    seniority_level: str = Field(default="Entry", description="Detected seniority level")


class ScoringWeights(BaseModel):
    """Configurable scoring weights"""
    skills_weight: float = Field(default=0.35, description="Weight for skills component (0.0-1.0)")
    experience_weight: float = Field(default=0.40, description="Weight for experience component (0.0-1.0)")
    achievement_weight: float = Field(default=0.15, description="Weight for achievement component (0.0-1.0)")
    structure_weight: float = Field(default=0.10, description="Weight for structure component (0.0-1.0)")

    def validate_weights(self) -> bool:
        """Validate that weights sum to 1.0"""
        total = self.skills_weight + self.experience_weight + self.achievement_weight + self.structure_weight
        return abs(total - 1.0) < 0.001


class GlobalScoringRequest(BaseModel):
    """Request model for global resume scoring"""
    skill_analysis: List[SkillProficiency] = Field(..., description="List of skill proficiency results")
    experience_analysis: ExperienceAnalysisData = Field(..., description="Experience analysis results")
    structured_sections: ResumeStructuredSections = Field(..., description="Resume sections")
    scoring_weights: Optional[ScoringWeights] = Field(None, description="Custom scoring weights")


class GlobalScoringResponse(BaseModel):
    """Response model for global resume scoring"""
    overall_score: int = Field(..., description="Final overall resume score (0-100)")
    score_breakdown: ScoreBreakdown = Field(..., description="Detailed breakdown of score components")
    scoring_weights: ScoringWeights = Field(..., description="Applied scoring weights")

    # Metadata
    total_skills_analyzed: int = Field(..., description="Total number of skills analyzed")
    recommendation_tier: str = Field(..., description="Overall recommendation tier (Excellent, Good, Fair, Poor)")
    key_strengths: List[str] = Field(default_factory=list, description="Identified key strengths")
    improvement_areas: List[str] = Field(default_factory=list, description="Areas for improvement")


class ScoringError(BaseModel):
    """Error response model for scoring"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    component: Optional[str] = Field(None, description="Component that failed (skills, experience, etc.)")


class ScoringHealthResponse(BaseModel):
    """Health check response for scoring service"""
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    components_available: List[str] = Field(..., description="Available scoring components")
    default_weights: ScoringWeights = Field(..., description="Default scoring weights")
