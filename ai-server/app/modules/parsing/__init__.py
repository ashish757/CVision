"""
Resume Parsing module for CVision AI Analysis Service

This module handles parsing of raw resume text into structured sections
and extraction of entities from those sections.

Features:
- Rule-based section detection
- Flexible heading matching
- Support for various resume formats
- spaCy NER entity extraction
- Dictionary-based skill matching
- Contact information extraction
- Extensible for future NLP improvements
"""

from .router import router
from .service import ResumeParsingService
from .entity_service import EntityExtractionService
from .schemas import (
    ResumeParsingRequest,
    ResumeParsingResponse,
    ResumeParsingError,
    EntityExtractionRequest,
    EntityExtractionResponse,
    EntityExtractionError
)

__all__ = [
    "router",
    "ResumeParsingService",
    "EntityExtractionService",
    "ResumeParsingRequest",
    "ResumeParsingResponse",
    "ResumeParsingError",
    "EntityExtractionRequest",
    "EntityExtractionResponse",
    "EntityExtractionError"
]
