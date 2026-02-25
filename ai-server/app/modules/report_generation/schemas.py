"""
Pydantic schemas for Evaluation Report Generation module
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class SkillEvaluation(BaseModel):
    """Individual skill evaluation for report generation"""
    skill: str = Field(..., description="Name of the skill")
    score: int = Field(..., description="Proficiency score (0-100)")
    level: str = Field(..., description="Proficiency level (Beginner, Intermediate, Expert)")
    years_experience: Optional[int] = Field(None, description="Years of experience with this skill")
    is_critical: bool = Field(default=False, description="Whether this is a critical/high-demand skill")


class ExperienceEvaluation(BaseModel):
    """Experience evaluation data for report generation"""
    total_experience_years: int = Field(..., description="Total years of professional experience")
    seniority_level: str = Field(..., description="Detected seniority level")
    achievement_score: int = Field(..., description="Score based on quantified achievements")
    experience_strength_score: int = Field(..., description="Overall experience strength score")
    strong_verbs_count: int = Field(default=0, description="Count of strong action verbs")
    weak_verbs_count: int = Field(default=0, description="Count of weak action verbs")
    quantified_achievements: List[str] = Field(default_factory=list, description="List of quantified achievements")


class ScoringResultData(BaseModel):
    """Scoring results data for report generation"""
    overall_score: int = Field(..., description="Final overall resume score (0-100)")
    skills_score: float = Field(..., description="Skills component score")
    experience_score: float = Field(..., description="Experience component score")
    achievement_score: float = Field(..., description="Achievement component score")
    structure_score: float = Field(..., description="Resume structure score")
    recommendation_tier: str = Field(..., description="Overall recommendation tier")
    missing_sections: List[str] = Field(default_factory=list, description="Missing resume sections")
    key_strengths: List[str] = Field(default_factory=list, description="Identified key strengths")
    improvement_areas: List[str] = Field(default_factory=list, description="Areas for improvement")


class EvaluationReportRequest(BaseModel):
    """Request model for evaluation report generation"""
    scoring_result: ScoringResultData = Field(..., description="Global scoring results")
    skill_analysis: List[SkillEvaluation] = Field(..., description="Skill analysis results")
    experience_analysis: ExperienceEvaluation = Field(..., description="Experience analysis results")
    candidate_name: Optional[str] = Field(None, description="Candidate name for personalization")
    position_title: Optional[str] = Field(None, description="Target position for context")


class EvaluationSection(BaseModel):
    """Individual section of the evaluation report"""
    title: str = Field(..., description="Section title")
    content: List[str] = Field(..., description="Section content items")
    priority_level: str = Field(default="medium", description="Priority level: high, medium, low")


class EvaluationReportResponse(BaseModel):
    """Response model for evaluation report generation"""
    overall_score: int = Field(..., description="Final overall resume score")
    summary_statement: str = Field(..., description="Executive summary of the evaluation")
    profile_tier: str = Field(..., description="Profile strength classification")

    # Main evaluation sections
    strengths: List[str] = Field(..., description="Identified strengths")
    weaknesses: List[str] = Field(..., description="Identified weaknesses")
    recommendations: List[str] = Field(..., description="Actionable recommendations")

    # Detailed breakdowns
    skills_evaluation: EvaluationSection = Field(..., description="Detailed skills evaluation")
    experience_evaluation: EvaluationSection = Field(..., description="Detailed experience evaluation")
    structure_evaluation: EvaluationSection = Field(..., description="Resume structure evaluation")

    # Metadata
    report_generated_at: datetime = Field(default_factory=datetime.now, description="Report generation timestamp")
    evaluation_criteria: Dict[str, str] = Field(default_factory=dict, description="Evaluation criteria used")
    next_steps: List[str] = Field(default_factory=list, description="Suggested next steps")


class ReportGenerationError(BaseModel):
    """Error response model for report generation"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    component: Optional[str] = Field(None, description="Component that failed")


class ReportTemplateConfig(BaseModel):
    """Configuration for report templates and thresholds"""
    high_score_threshold: int = Field(default=80, description="Threshold for strong profile classification")
    moderate_score_threshold: int = Field(default=60, description="Threshold for moderate profile classification")
    high_skill_threshold: int = Field(default=70, description="Threshold for high proficiency skills")
    low_skill_threshold: int = Field(default=40, description="Threshold for low proficiency skills")
    strong_achievement_threshold: int = Field(default=75, description="Threshold for strong achievements")
    experience_strength_threshold: int = Field(default=70, description="Threshold for strong experience")

    # Report personalization
    include_candidate_name: bool = Field(default=False, description="Whether to include candidate name")
    include_position_context: bool = Field(default=False, description="Whether to include position context")
    detailed_breakdown: bool = Field(default=True, description="Whether to include detailed breakdowns")


class ReportHealthResponse(BaseModel):
    """Health check response for report generation service"""
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    supported_formats: List[str] = Field(..., description="Supported report formats")
    evaluation_criteria: Dict[str, int] = Field(..., description="Current evaluation thresholds")
