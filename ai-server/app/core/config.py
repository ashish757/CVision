"""
Core configuration settings for CVision AI Analysis Service
"""
from typing import List
import os


class Settings:
    """Application settings and configuration"""

    # Application metadata
    APP_NAME: str = "CVision AI Analysis Service"
    APP_DESCRIPTION: str = "AI-powered resume analysis service for extracting skills, experience, and scoring resumes"
    APP_VERSION: str = "1.0.0"

    # API configuration
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["*"]  # Configure this properly in production
    ALLOW_CREDENTIALS: bool = True
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]

    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "4000"))

    # File processing settings
    MAX_FILE_SIZE_MB: int = 5
    SUPPORTED_FILE_EXTENSIONS: List[str] = [".pdf", ".docx"]

    # Text extraction settings
    MAX_EXTRACTION_THREADS: int = 4
    EXTRACTION_TIMEOUT_SECONDS: int = 30

    # Analysis settings
    MIN_TEXT_LENGTH: int = 10
    MAX_TEXT_LENGTH: int = 1000000  # 1MB of text
    DEFAULT_PROCESSING_DELAY_MIN: float = 1.5
    DEFAULT_PROCESSING_DELAY_MAX: float = 2.5


# Global settings instance
settings = Settings()
