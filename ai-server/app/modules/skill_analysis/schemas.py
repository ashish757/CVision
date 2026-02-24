from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class SkillLevel(str, Enum):
    """Enumeration for skill proficiency levels"""
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    EXPERT = "Expert"


class SkillAnalysisRequest(BaseModel):
    """Request model for skill proficiency analysis"""
    skills: List[str] = Field(..., description="List of skills to analyze for proficiency")
    resume_text: str = Field(..., description="Full resume text for context analysis")

    class Config:
        json_schema_extra = {
            "example": {
                "skills": ["Python", "Java", "React", "SQL", "AWS"],
                "resume_text": "John Doe\n\nSKILLS\nPython, Java, React\n\nEXPERIENCE\nSoftware Engineer at ABC Corp\n- Developed Python applications for 3 years\n- Led React development team\n- Advanced knowledge of SQL optimization..."
            }
        }


class SkillProficiencyResult(BaseModel):
    """Model for individual skill proficiency analysis result"""
    skill: str = Field(..., description="Skill name")
    score: int = Field(..., ge=0, le=100, description="Proficiency score (0-100)")
    level: SkillLevel = Field(..., description="Proficiency level based on score")
    years_experience: Optional[int] = Field(None, description="Extracted years of experience if found")
    confidence: float = Field(..., ge=0, le=1, description="Confidence level of the analysis")
    signals_detected: List[str] = Field(default_factory=list, description="List of proficiency signals detected")

    class Config:
        json_schema_extra = {
            "example": {
                "skill": "Python",
                "score": 85,
                "level": "Expert",
                "years_experience": 4,
                "confidence": 0.85,
                "signals_detected": ["4 years of experience", "developed applications", "advanced knowledge"]
            }
        }


class SkillAnalysisResponse(BaseModel):
    """Response model for skill proficiency analysis"""
    results: List[SkillProficiencyResult] = Field(..., description="Analysis results for each skill")
    total_skills_analyzed: int = Field(..., description="Total number of skills analyzed")
    average_proficiency_score: float = Field(..., description="Average proficiency score across all skills")
    processing_time_seconds: float = Field(..., description="Time taken for analysis")
    summary: dict = Field(..., description="Summary of skill levels distribution")

    class Config:
        json_schema_extra = {
            "example": {
                "results": [
                    {
                        "skill": "Python",
                        "score": 85,
                        "level": "Expert",
                        "years_experience": 4,
                        "confidence": 0.85,
                        "signals_detected": ["4 years of experience", "developed applications"]
                    }
                ],
                "total_skills_analyzed": 5,
                "average_proficiency_score": 72.4,
                "processing_time_seconds": 0.18,
                "summary": {
                    "Beginner": 1,
                    "Intermediate": 2,
                    "Expert": 2
                }
            }
        }


class SkillAnalysisError(BaseModel):
    """Error response model for skill analysis"""
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Detailed error message")
    skills_preview: Optional[List[str]] = Field(None, description="Preview of input skills for debugging")
    text_preview: Optional[str] = Field(None, description="Preview of input text for debugging")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "AnalysisError",
                "detail": "Failed to analyze skills: empty resume text",
                "skills_preview": ["Python", "Java"],
                "text_preview": "John Doe\nSoftware Engineer..."
            }
        }


class SkillContextSignal(BaseModel):
    """Model representing a detected proficiency signal in context"""
    signal_type: str = Field(..., description="Type of signal (years, level, verb)")
    signal_value: str = Field(..., description="Detected signal text")
    context: str = Field(..., description="Context window around the signal")
    weight: float = Field(..., description="Weight of this signal in scoring")
    position: int = Field(..., description="Position in text where signal was found")

    class Config:
        json_schema_extra = {
            "example": {
                "signal_type": "years_experience",
                "signal_value": "3 years of Python",
                "context": "...worked as a developer using Python for 3 years building scalable web applications...",
                "weight": 0.6,
                "position": 156
            }
        }
