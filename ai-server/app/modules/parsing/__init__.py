"""
Resume Parsing module for CVision AI Analysis Service

This module handles parsing of raw resume text into structured sections
including skills, experience, education, projects, and certifications.

Features:
- Rule-based section detection
- Flexible heading matching
- Support for various resume formats
- Extensible for future NLP improvements
"""

from .router import router
from .service import ResumeParsingService
from .schemas import ResumeParsingRequest, ResumeParsingResponse, ResumeParsingError

__all__ = [
    "router",
    "ResumeParsingService",
    "ResumeParsingRequest",
    "ResumeParsingResponse",
    "ResumeParsingError"
]
