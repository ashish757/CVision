from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
import os
from app.core.constants import AnalysisConstants


class AnalyzeRequest(BaseModel):
    """Request model for resume analysis"""
    file_path: str = Field(..., description="Path to the uploaded resume file")

    @field_validator('file_path')
    @classmethod
    def validate_file_path(cls, v):
        if not v:
            raise ValueError("File path cannot be empty")

        # Check if file exists
        if not os.path.exists(v):
            raise ValueError(f"File does not exist: {v}")

        # Validate file extension using core constants
        from app.core.constants import TextExtractionConstants
        file_extension = os.path.splitext(v)[1].lower()

        if file_extension not in TextExtractionConstants.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type. Allowed types: {', '.join(TextExtractionConstants.SUPPORTED_EXTENSIONS)}")

        return v


class AnalyzeResponse(BaseModel):
    """Response model for resume analysis"""
    skills: List[str] = Field(..., description="List of extracted skills")
    experience_years: int = Field(..., description="Years of experience")
    education: str = Field(..., description="Highest education level")
    score: int = Field(..., ge=AnalysisConstants.MIN_SCORE, le=AnalysisConstants.MAX_SCORE, description="Resume score out of 100")
    processing_time_seconds: float = Field(..., description="Time taken for processing")

    class Config:
        json_schema_extra = {
            "example": {
                "skills": ["Python", "React", "SQL", "Machine Learning"],
                "experience_years": 3,
                "education": "B.Tech Computer Science",
                "score": 78,
                "processing_time_seconds": 2.5
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Unsupported file type",
                "detail": "Only PDF and DOCX files are supported"
            }
        }
