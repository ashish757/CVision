"""
Application constants for CVision AI Analysis Service
"""
from typing import List


# Analysis constants
class AnalysisConstants:
    """Constants for resume analysis functionality"""

    # Mock data pools for skill detection and analysis
    SKILLS_POOL: List[str] = [
        "Python", "JavaScript", "React", "Node.js", "SQL", "MongoDB",
        "Docker", "AWS", "Kubernetes", "Git", "Machine Learning", "Django",
        "FastAPI", "PostgreSQL", "Redis", "HTML/CSS", "TypeScript", "Vue.js",
        "Angular", "Java", "C++", "Pandas", "NumPy", "TensorFlow", "PyTorch",
        "REST APIs", "GraphQL", "Microservices", "CI/CD", "Linux", "Terraform"
    ]

    EDUCATION_LEVELS: List[str] = [
        "B.Tech Computer Science",
        "B.E. Information Technology",
        "M.Tech Software Engineering",
        "BCA",
        "MCA",
        "B.Sc Computer Science",
        "M.Sc Data Science",
        "MBA Technology Management",
        "Diploma in Computer Science"
    ]

    # Scoring parameters
    MAX_SCORE: int = 100
    MIN_SCORE: int = 10
    MAX_EXPERIENCE_SCORE: int = 40
    MAX_SKILLS_SCORE: int = 30
    MAX_QUALITY_SCORE: int = 20
    MAX_LENGTH_SCORE: int = 10

    # Content quality indicators
    QUALITY_INDICATORS: List[str] = [
        "project", "achievement", "award", "certification", "published",
        "led", "managed", "developed", "implemented", "designed",
        "improved", "optimized", "reduced", "increased", "successful"
    ]


# Text extraction constants
class TextExtractionConstants:
    """Constants for text extraction functionality"""

    # File validation
    SUPPORTED_EXTENSIONS: List[str] = [".pdf", ".docx"]
    MAX_FILE_SIZE_BYTES: int = 5 * 1024 * 1024  # 5 MB

    # Text validation
    MIN_TEXT_LENGTH: int = 10
    MAX_TEXT_LENGTH: int = 1000000  # 1 MB of text

    # Processing limits
    MAX_PDF_PAGES: int = 50
    MAX_DOCX_PARAGRAPHS: int = 1000

    # Thread pool configuration
    MAX_EXTRACTION_THREADS: int = 4


# HTTP response constants
class HTTPConstants:
    """Constants for HTTP responses and error handling"""

    # Success messages
    ANALYSIS_SUCCESS: str = "Resume analysis completed successfully"
    EXTRACTION_SUCCESS: str = "Text extraction completed successfully"
    HEALTH_CHECK_SUCCESS: str = "Service is healthy and operational"

    # Error messages
    FILE_NOT_FOUND: str = "File not found"
    UNSUPPORTED_FILE_TYPE: str = "Unsupported file type. Only PDF and DOCX files are supported."
    FILE_TOO_LARGE: str = "File size exceeds the maximum allowed limit"
    EXTRACTION_FAILED: str = "Text extraction failed"
    ANALYSIS_FAILED: str = "Resume analysis failed"
    INTERNAL_ERROR: str = "An internal server error occurred. Please try again."

    # Status codes (for reference, FastAPI handles these automatically)
    SUCCESS: int = 200
    BAD_REQUEST: int = 400
    NOT_FOUND: int = 404
    UNPROCESSABLE_ENTITY: int = 422
    INTERNAL_SERVER_ERROR: int = 500


# Logging format constants
class LoggingConstants:
    """Constants for logging and monitoring"""

    # Log prefixes for different components
    ROUTER_PREFIX: str = "[ROUTER]"
    SERVICE_PREFIX: str = "[SERVICE]"
    UTIL_PREFIX: str = "[UTIL]"
    ANALYSIS_PREFIX: str = "[ANALYSIS]"
    EXTRACTION_PREFIX: str = "[EXTRACTION]"

    # Log separators
    SECTION_SEPARATOR: str = "=" * 60
    SUBSECTION_SEPARATOR: str = "*" * 60
    MINOR_SEPARATOR: str = "-" * 40

    # Success/Error indicators
    SUCCESS_INDICATOR: str = "✅"
    ERROR_INDICATOR: str = "❌"
    WARNING_INDICATOR: str = "⚠️"
    INFO_INDICATOR: str = "ℹ️"
