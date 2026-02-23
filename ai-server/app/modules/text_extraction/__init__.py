"""
Text Extraction module for CVision AI Analysis Service

This module handles text extraction functionality including:
- PDF text extraction
- DOCX text extraction
- File validation
- Text processing
"""

from .router import router
from .service import TextExtractionService
from .schemas import TextExtractionRequest, TextExtractionResponse, ErrorResponse

__all__ = [
    "router",
    "TextExtractionService",
    "TextExtractionRequest",
    "TextExtractionResponse",
    "ErrorResponse"
]
