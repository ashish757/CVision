from fastapi import APIRouter, HTTPException, status

from .schemas import (
    ResumeParsingRequest,
    ResumeParsingResponse,
    ResumeParsingError,
    EntityExtractionRequest,
    EntityExtractionResponse,
    EntityExtractionError
)
from .service import ResumeParsingService
from .entity_service import EntityExtractionService

# Import core components with fallback
try:
    from app.core import get_logger, LoggingConstants, HTTPConstants
    logger = get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

    # Fallback constants
    class LoggingConstants:
        ROUTER_PREFIX = "[ROUTER]"
        SUCCESS_INDICATOR = "✅"
        ERROR_INDICATOR = "❌"

    class HTTPConstants:
        INTERNAL_ERROR = "Internal server error"
router = APIRouter(prefix="/parse", tags=["Resume Parsing"])


@router.post(
    "/sections",
    response_model=ResumeParsingResponse,
    status_code=status.HTTP_200_OK,
    summary="Parse Resume into Sections",
    description="Parse raw resume text into organized sections like skills, experience, education, etc.",
    responses={
        200: {
            "description": "Resume parsed successfully into sections",
            "model": ResumeParsingResponse
        },
        400: {
            "description": "Bad Request - Invalid input text",
            "model": ResumeParsingError
        },
        422: {
            "description": "Unprocessable Entity - Text validation failed",
            "model": ResumeParsingError
        },
        500: {
            "description": "Internal server error during parsing",
            "model": ResumeParsingError
        }
    }
)
async def parse_resume_sections(request: ResumeParsingRequest):
    """
    Parse raw resume text into structured sections.

    This endpoint accepts raw resume text and organizes it into logical sections
    such as summary, skills, experience, education, projects, and certifications.

    **Supported Sections:**
    - Summary/Profile/Objective
    - Skills/Technical Skills/Core Competencies
    - Experience/Work Experience/Professional Experience
    - Education/Academic Background
    - Projects/Key Projects
    - Certifications/Professional Certifications
    - Other (unmatched content)

    **Features:**
    - Rule-based section detection
    - Flexible heading matching
    - Preserves text order
    - Handles inconsistent resume formats

    Args:
        request: ResumeParsingRequest containing the raw resume text

    Returns:
        ResumeParsingResponse: Structured sections with metadata

    Raises:
        HTTPException: For various error conditions
    """
    try:
        logger.info("*" * 60)
        logger.info(f"{LoggingConstants.ROUTER_PREFIX} Received resume parsing request")
        logger.info(f"{LoggingConstants.ROUTER_PREFIX} Text length: {len(request.text)} characters")

        # Validate input text
        validation_result = ResumeParsingService.validate_text_for_parsing(request.text)
        if not validation_result["is_valid"]:
            logger.error(f"{LoggingConstants.ROUTER_PREFIX} Text validation failed: {validation_result['error']}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "ValidationError",
                    "detail": validation_result["error"],
                    "text_preview": request.text[:100] if request.text else ""
                }
            )

        logger.info(f"{LoggingConstants.ROUTER_PREFIX} Text validation passed")

        # Parse the resume text into sections
        result = ResumeParsingService.split_resume_into_sections(request.text)

        logger.info(f"{LoggingConstants.ROUTER_PREFIX} {LoggingConstants.SUCCESS_INDICATOR} Parsing successful")
        logger.info(f"{LoggingConstants.ROUTER_PREFIX} {LoggingConstants.SUCCESS_INDICATOR} Found {result.sections_found} sections in {result.processing_time_seconds}s")
        logger.info("*" * 60)

        return result

    except HTTPException as e:
        logger.error(f"{LoggingConstants.ROUTER_PREFIX} HTTP Exception: {e.detail}")
        logger.error("*" * 60)
        # Re-raise HTTP exceptions
        raise

    except ValueError as e:
        # Handle validation errors
        logger.error(f"{LoggingConstants.ROUTER_PREFIX} Validation error: {str(e)}")
        logger.error("*" * 60)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "ValidationError",
                "detail": str(e),
                "text_preview": request.text[:100] if request.text else ""
            }
        )

    except Exception as e:
        # Handle unexpected errors
        logger.error(f"{LoggingConstants.ROUTER_PREFIX} {LoggingConstants.ERROR_INDICATOR} Unexpected error during parsing: {str(e)}", exc_info=True)
        logger.error("*" * 60)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "detail": HTTPConstants.INTERNAL_ERROR,
                "text_preview": request.text[:100] if request.text else ""
            }
        )


@router.get(
    "/supported-sections",
    summary="Get Supported Section Types",
    description="Get list of section types and keywords supported for resume parsing",
    tags=["Resume Parsing", "Info"]
)
async def get_supported_sections():
    """
    Get list of section types and their associated keywords for resume parsing.

    Returns:
        Dictionary of supported section types and their keywords
    """
    try:
        supported_sections = ResumeParsingService.get_supported_sections()

        return {
            "supported_sections": supported_sections,
            "total_section_types": len(supported_sections),
            "message": "Resume parsing supports these section types with flexible keyword matching"
        }

    except Exception as e:
        logger.error(f"Error getting supported sections: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve supported section types"
        )


@router.post(
    "/validate",
    summary="Validate Text for Resume Parsing",
    description="Validate if text is suitable for resume section parsing",
    tags=["Resume Parsing", "Validation"]
)
async def validate_text_for_parsing(request: ResumeParsingRequest):
    """
    Validate text input for resume parsing without actually parsing it.

    Useful for pre-flight validation before starting parsing.

    Args:
        request: ResumeParsingRequest containing the text to validate

    Returns:
        Validation result with recommendations
    """
    try:
        logger.info(f"Validating text for resume parsing: {len(request.text)} characters")

        validation_result = ResumeParsingService.validate_text_for_parsing(request.text)

        if validation_result["is_valid"]:
            logger.info(f"Text validation passed for resume parsing")
            return {
                "status": "valid",
                "message": "Text is suitable for resume parsing",
                "text_length": validation_result["text_length"],
                "estimated_sections": validation_result["estimated_sections"]
            }
        else:
            logger.warning(f"Text validation failed: {validation_result['error']}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "ValidationFailed",
                    "detail": validation_result["error"],
                    "suggestions": validation_result.get("suggestions", []),
                    "text_preview": request.text[:100] if request.text else ""
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during text validation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "ValidationError",
                "detail": "Failed to validate text for resume parsing"
            }
        )


@router.post(
    "/entities",
    response_model=EntityExtractionResponse,
    status_code=status.HTTP_200_OK,
    summary="Extract Entities from Resume Sections",
    description="Extract structured entities (name, email, skills, companies, etc.) from parsed resume sections",
    responses={
        200: {
            "description": "Entities extracted successfully",
            "model": EntityExtractionResponse
        },
        400: {
            "description": "Bad Request - Invalid sections input",
            "model": EntityExtractionError
        },
        422: {
            "description": "Unprocessable Entity - Sections validation failed",
            "model": EntityExtractionError
        },
        500: {
            "description": "Internal server error during entity extraction",
            "model": EntityExtractionError
        }
    }
)
async def extract_entities_from_sections(request: EntityExtractionRequest):
    """
    Extract structured entities from resume sections.

    This endpoint accepts structured resume sections (from the parsing module)
    and extracts entities such as contact information, skills, companies,
    job titles, education degrees, and dates.

    **Supported Entities:**
    - Name (using spaCy NER)
    - Email address (regex-based)
    - Phone number (regex-based)
    - Technical skills (dictionary matching)
    - Company names (spaCy NER)
    - Job titles (pattern matching)
    - Education degrees (keyword matching)
    - Dates (spaCy NER)

    **Features:**
    - spaCy NER for person/organization/date extraction
    - Regex patterns for contact information
    - Dictionary-based skill matching
    - Deduplication and normalization
    - Graceful handling of missing sections

    Args:
        request: EntityExtractionRequest containing resume sections

    Returns:
        EntityExtractionResponse: Extracted entities with metadata

    Raises:
        HTTPException: For various error conditions
    """
    try:
        import time
        start_time = time.time()

        logger.info("*" * 60)
        logger.info(f"{LoggingConstants.ROUTER_PREFIX} Received entity extraction request")
        logger.info(f"{LoggingConstants.ROUTER_PREFIX} Input sections: {list(request.sections.keys())}")

        # Validate input sections
        validation_result = EntityExtractionService.validate_sections_for_extraction(request.sections)
        if not validation_result["is_valid"]:
            logger.error(f"{LoggingConstants.ROUTER_PREFIX} Sections validation failed: {validation_result['error']}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "ValidationError",
                    "detail": validation_result["error"],
                    "sections_preview": {k: v[:100] + "..." if len(v) > 100 else v
                                       for k, v in request.sections.items() if v}
                }
            )

        logger.info(f"{LoggingConstants.ROUTER_PREFIX} Sections validation passed")

        # Initialize entity extraction service
        entity_service = EntityExtractionService()

        # Extract entities from sections
        entities = entity_service.extract_entities(request.sections)

        # Calculate processing time
        processing_time = time.time() - start_time

        # Count total entities
        total_entities = 0
        for key, value in entities.items():
            if isinstance(value, list):
                total_entities += len(value)
            elif value:  # Non-empty string values
                total_entities += 1

        # Create response
        result = EntityExtractionResponse(
            name=entities["name"],
            email=entities["email"],
            phone=entities["phone"],
            skills=entities["skills"],
            companies=entities["companies"],
            job_titles=entities["job_titles"],
            education_degrees=entities["education_degrees"],
            dates=entities["dates"],
            total_entities_extracted=total_entities,
            processing_time_seconds=round(processing_time, 3)
        )

        logger.info(f"{LoggingConstants.ROUTER_PREFIX} {LoggingConstants.SUCCESS_INDICATOR} Entity extraction successful")
        logger.info(f"{LoggingConstants.ROUTER_PREFIX} {LoggingConstants.SUCCESS_INDICATOR} Extracted {total_entities} entities in {processing_time:.3f}s")
        logger.info("*" * 60)

        return result

    except HTTPException as e:
        logger.error(f"{LoggingConstants.ROUTER_PREFIX} HTTP Exception: {e.detail}")
        logger.error("*" * 60)
        # Re-raise HTTP exceptions
        raise

    except ValueError as e:
        # Handle validation errors
        logger.error(f"{LoggingConstants.ROUTER_PREFIX} Validation error: {str(e)}")
        logger.error("*" * 60)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "ValidationError",
                "detail": str(e),
                "sections_preview": {k: v[:100] + "..." if len(v) > 100 else v
                                   for k, v in request.sections.items() if v}
            }
        )

    except Exception as e:
        # Handle unexpected errors
        logger.error(f"{LoggingConstants.ROUTER_PREFIX} {LoggingConstants.ERROR_INDICATOR} Unexpected error during entity extraction: {str(e)}", exc_info=True)
        logger.error("*" * 60)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "detail": HTTPConstants.INTERNAL_ERROR,
                "sections_preview": {k: v[:100] + "..." if len(v) > 100 else v
                                   for k, v in request.sections.items() if v}
            }
        )


@router.get(
    "/supported-entities",
    summary="Get Supported Entity Types",
    description="Get list of entity types supported for extraction from resume sections",
    tags=["Resume Parsing", "Entity Extraction", "Info"]
)
async def get_supported_entity_types():
    """
    Get list of entity types and their descriptions for entity extraction.

    Returns:
        Dictionary of supported entity types and their descriptions
    """
    try:
        supported_entities = EntityExtractionService.get_supported_entity_types()

        return {
            "supported_entities": supported_entities,
            "total_entity_types": len(supported_entities),
            "message": "Entity extraction supports these entity types using various NLP and regex techniques",
            "requirements": {
                "spacy_model": "en_core_web_sm",
                "install_command": "python -m spacy download en_core_web_sm"
            }
        }

    except Exception as e:
        logger.error(f"Error getting supported entity types: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve supported entity types"
        )


@router.post(
    "/validate-sections",
    summary="Validate Sections for Entity Extraction",
    description="Validate if resume sections are suitable for entity extraction",
    tags=["Resume Parsing", "Entity Extraction", "Validation"]
)
async def validate_sections_for_extraction(request: EntityExtractionRequest):
    """
    Validate resume sections for entity extraction without actually extracting entities.

    Useful for pre-flight validation before starting entity extraction.

    Args:
        request: EntityExtractionRequest containing the sections to validate

    Returns:
        Validation result with recommendations
    """
    try:
        logger.info(f"Validating sections for entity extraction: {list(request.sections.keys())}")

        validation_result = EntityExtractionService.validate_sections_for_extraction(request.sections)

        if validation_result["is_valid"]:
            logger.info(f"Sections validation passed for entity extraction")
            return {
                "status": "valid",
                "message": "Sections are suitable for entity extraction",
                "content_sections": validation_result["content_sections"],
                "total_text_length": validation_result["total_text_length"]
            }
        else:
            logger.warning(f"Sections validation failed: {validation_result['error']}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "ValidationFailed",
                    "detail": validation_result["error"],
                    "suggestions": validation_result.get("suggestions", []),
                    "sections_preview": {k: v[:50] + "..." if len(v) > 50 else v
                                       for k, v in request.sections.items() if v}
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during sections validation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "ValidationError",
                "detail": "Failed to validate sections for entity extraction"
            }
        )


@router.get(
    "/health",
    summary="Resume Parsing Service Health Check",
    description="Check if the resume parsing service is working properly",
    tags=["Health"]
)
async def health_check():
    """
    Health check endpoint for the resume parsing service

    Returns:
        Service health status
    """
    return {
        "status": "healthy",
        "service": "CVision Resume Parsing Service",
        "version": "1.0.0",
        "supported_sections": list(ResumeParsingService.get_supported_sections().keys())
    }
