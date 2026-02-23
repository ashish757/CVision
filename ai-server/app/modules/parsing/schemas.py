from typing import Optional, List
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


class EntityExtractionRequest(BaseModel):
    """Request model for entity extraction from resume sections"""
    sections: dict = Field(..., description="Dictionary of resume sections from parsing module")

    class Config:
        json_schema_extra = {
            "example": {
                "sections": {
                    "summary": "Experienced software engineer with 5+ years...",
                    "skills": "Python, Java, React, Node.js, AWS...",
                    "experience": "Software Engineer at ABC Corp (2020-2023)...",
                    "education": "Bachelor of Science in Computer Science...",
                    "projects": "E-commerce Platform - Built using React...",
                    "certifications": "AWS Certified Developer..."
                }
            }
        }


class EntityExtractionResponse(BaseModel):
    """Response model for entity extraction"""
    name: str = Field(default="", description="Extracted person name")
    email: str = Field(default="", description="Extracted email address")
    phone: str = Field(default="", description="Extracted phone number")
    skills: List[str] = Field(default_factory=list, description="List of extracted technical skills")
    companies: List[str] = Field(default_factory=list, description="List of extracted company names")
    job_titles: List[str] = Field(default_factory=list, description="List of extracted job titles")
    education_degrees: List[str] = Field(default_factory=list, description="List of extracted education degrees")
    dates: List[str] = Field(default_factory=list, description="List of extracted dates")
    total_entities_extracted: int = Field(..., description="Total number of entities extracted")
    processing_time_seconds: float = Field(..., description="Time taken for entity extraction")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@email.com",
                "phone": "(555) 123-4567",
                "skills": ["Python", "Java", "React", "Node.js", "AWS"],
                "companies": ["ABC Corp", "XYZ Inc"],
                "job_titles": ["Software Engineer", "Senior Developer"],
                "education_degrees": ["Bachelor of Science", "Computer Science"],
                "dates": ["2020-2023", "2018-2020", "2018"],
                "total_entities_extracted": 15,
                "processing_time_seconds": 0.25
            }
        }


class EntityExtractionError(BaseModel):
    """Error response model for entity extraction"""
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Detailed error message")
    sections_preview: Optional[dict] = Field(None, description="Preview of input sections for debugging")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ExtractionError",
                "detail": "Failed to extract entities: spaCy model not available",
                "sections_preview": {"summary": "John Doe\n...", "skills": "Python, Java..."}
            }
        }
