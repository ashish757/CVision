"""
Schemas module for CVision AI Analysis Service

This module contains all Pydantic models used for request/response validation
and serialization throughout the API.
"""
from .analysis import AnalyzeRequest, AnalyzeResponse, ErrorResponse
from .text_extraction import TextExtractionRequest, TextExtractionResponse, TextExtractionError

__all__ = [
    # Analysis schemas
    "AnalyzeRequest",
    "AnalyzeResponse",
    "ErrorResponse",

    # Text extraction schemas
    "TextExtractionRequest",
    "TextExtractionResponse",
    "TextExtractionError"
]
