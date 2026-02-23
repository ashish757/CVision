from typing import Optional
from pydantic import BaseModel, Field, field_validator
import os
from app.core.constants import TextExtractionConstants


class TextExtractionRequest(BaseModel):
    """Request model for text extraction"""
    file_path: str = Field(..., description="Path to the file for text extraction")

    @field_validator('file_path')
    @classmethod
    def validate_file_path(cls, v):
        if not v:
            raise ValueError("File path cannot be empty")

        # Check if file exists
        if not os.path.exists(v):
            raise ValueError(f"File does not exist: {v}")

        # Validate file extension using core constants
        file_extension = os.path.splitext(v)[1].lower()

        if file_extension not in TextExtractionConstants.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type. Allowed types: {', '.join(TextExtractionConstants.SUPPORTED_EXTENSIONS)}")

        return v


class TextExtractionResponse(BaseModel):
    """Response model for text extraction"""
    file_name: str = Field(..., description="Name of the processed file")
    text_length: int = Field(..., ge=0, description="Number of characters in extracted text")
    extracted_text: str = Field(..., description="Full extracted text content")
    file_type: str = Field(..., description="Type of file processed (pdf or docx)")
    processing_time_seconds: float = Field(..., description="Time taken for text extraction")

    class Config:
        json_schema_extra = {
            "example": {
                "file_name": "resume_123.pdf",
                "text_length": 12500,
                "extracted_text": "John Doe\nSoftware Engineer\n\nExperience:\n- Python Developer at Tech Corp\n...",
                "file_type": "pdf",
                "processing_time_seconds": 0.85
            }
        }


class TextExtractionError(BaseModel):
    """Error response model for text extraction"""
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Detailed error message")
    file_path: Optional[str] = Field(None, description="File path that caused the error")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ExtractionError",
                "detail": "Failed to extract text from PDF: corrupted file",
                "file_path": "uploads/resume_123.pdf"
            }
        }


# Re-export for backward compatibility
ErrorResponse = TextExtractionError
