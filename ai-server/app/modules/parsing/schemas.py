from typing import Optional
from pydantic import BaseModel, Field


class ResumeParsingRequest(BaseModel):
    """Request model for resume parsing"""
    text: str = Field(..., description="Raw resume text to be parsed into sections")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "John Doe\n\nPROFILE\nExperienced software engineer...\n\nSKILLS\nPython, Java, React...\n\nEXPERIENCE\nSoftware Engineer at ABC Corp..."
            }
        }


class ResumeParsingResponse(BaseModel):
    """Response model for resume parsing"""
    summary: str = Field(default="", description="Summary/Profile/Objective section content")
    skills: str = Field(default="", description="Skills/Technical Skills/Core Competencies section content")
    experience: str = Field(default="", description="Experience/Work Experience/Professional Experience section content")
    education: str = Field(default="", description="Education/Academic Background section content")
    projects: str = Field(default="", description="Projects section content")
    certifications: str = Field(default="", description="Certifications section content")
    other: str = Field(default="", description="Any unmatched content")
    sections_found: int = Field(..., description="Number of sections detected")
    processing_time_seconds: float = Field(..., description="Time taken for parsing")

    class Config:
        json_schema_extra = {
            "example": {
                "summary": "Experienced software engineer with 5+ years...",
                "skills": "Python, Java, React, Node.js, SQL...",
                "experience": "Software Engineer at ABC Corp (2020-2023)...",
                "education": "Bachelor of Science in Computer Science...",
                "projects": "E-commerce Platform - Built using React...",
                "certifications": "AWS Certified Developer...",
                "other": "Additional information...",
                "sections_found": 6,
                "processing_time_seconds": 0.15
            }
        }


class ResumeParsingError(BaseModel):
    """Error response model for resume parsing"""
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Detailed error message")
    text_preview: Optional[str] = Field(None, description="First 100 characters of input text for debugging")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ParsingError",
                "detail": "Failed to parse resume text: empty input",
                "text_preview": "John Doe\\n\\nPROFILE\\nExperienced..."
            }
        }
