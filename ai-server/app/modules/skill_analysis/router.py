from fastapi import APIRouter, HTTPException, status

from .schemas import (
    SkillAnalysisRequest,
    SkillAnalysisResponse,
    SkillAnalysisError
)
from .service import SkillIntelligenceEngine

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
        SUCCESS_INDICATOR = "Success"
        ERROR_INDICATOR = "Error"

    class HTTPConstants:
        INTERNAL_ERROR = "Internal server error"

router = APIRouter(prefix="/skills", tags=["Skill Analysis"])


@router.post(
    "/analyze-proficiency",
    response_model=SkillAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze Skill Proficiency Levels",
    description="Analyze skill proficiency levels using context-based signal detection from resume text",
    responses={
        200: {
            "description": "Skill proficiency analysis completed successfully",
            "model": SkillAnalysisResponse
        },
        400: {
            "description": "Bad Request - Invalid input data",
            "model": SkillAnalysisError
        },
        422: {
            "description": "Unprocessable Entity - Input validation failed",
            "model": SkillAnalysisError
        },
        500: {
            "description": "Internal server error during analysis",
            "model": SkillAnalysisError
        }
    }
)
async def analyze_skill_proficiency(request: SkillAnalysisRequest):
    """
    Analyze skill proficiency levels from resume text using intelligent signal detection.

    This endpoint analyzes a list of skills against the full resume text to determine
    proficiency levels using context-based signals including:

    **Signal Detection Methods:**
    - **Years of Experience**: Patterns like "3 years of Python", "Java for 5 years"
    - **Level Keywords**: "expert", "advanced", "intermediate", "beginner", etc.
    - **Action Verbs**: Strong verbs (developed, architected) vs weak verbs (familiar, learned)
    - **Context Analysis**: ±100 character windows around skill mentions

    **Proficiency Scoring:**
    - Years of experience (highest weight): 0.6
    - Level keywords (medium weight): 0.4
    - Strong/weak verbs (lower weight): 0.3/-0.2
    - Score ranges: 0-30 (Beginner), 30-60 (Intermediate), 60-100 (Expert)

    **Features:**
    - Case-insensitive skill matching
    - Multiple occurrence handling
    - Signal deduplication
    - Confidence scoring
    - Comprehensive logging

    Args:
        request: SkillAnalysisRequest containing skills list and resume text

    Returns:
        SkillAnalysisResponse: Detailed proficiency analysis for each skill

    Raises:
        HTTPException: For various error conditions
    """
    try:
        logger.info("*" * 70)
        logger.info(f"{LoggingConstants.ROUTER_PREFIX} Received skill proficiency analysis request")
        logger.info(f"{LoggingConstants.ROUTER_PREFIX} Skills count: {len(request.skills)}")
        logger.info(f"{LoggingConstants.ROUTER_PREFIX} Resume text length: {len(request.resume_text)} characters")

        # Validate input data
        validation_result = SkillIntelligenceEngine.validate_analysis_input(
            request.skills, request.resume_text
        )

        if not validation_result["is_valid"]:
            logger.error(f"{LoggingConstants.ROUTER_PREFIX} Input validation failed: {validation_result['error']}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "ValidationError",
                    "detail": validation_result["error"],
                    "skills_preview": request.skills[:5] if request.skills else [],
                    "text_preview": request.resume_text[:200] if request.resume_text else ""
                }
            )

        logger.info(f"{LoggingConstants.ROUTER_PREFIX} Input validation passed")

        # Initialize skill intelligence engine
        engine = SkillIntelligenceEngine()

        # Analyze skill proficiency
        result = engine.analyze_skill_proficiency(request.skills, request.resume_text)

        logger.info(f"{LoggingConstants.ROUTER_PREFIX} {LoggingConstants.SUCCESS_INDICATOR} Analysis successful")
        logger.info(f"{LoggingConstants.ROUTER_PREFIX} {LoggingConstants.SUCCESS_INDICATOR} Analyzed {result.total_skills_analyzed} skills in {result.processing_time_seconds}s")
        logger.info(f"{LoggingConstants.ROUTER_PREFIX} {LoggingConstants.SUCCESS_INDICATOR} Average proficiency: {result.average_proficiency_score}/100")
        logger.info("*" * 70)

        return result

    except HTTPException as e:
        logger.error(f"{LoggingConstants.ROUTER_PREFIX} HTTP Exception: {e.detail}")
        logger.error("*" * 70)
        raise

    except ValueError as e:
        logger.error(f"{LoggingConstants.ROUTER_PREFIX} Validation error: {str(e)}")
        logger.error("*" * 70)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "ValidationError",
                "detail": str(e),
                "skills_preview": request.skills[:5] if hasattr(request, 'skills') else [],
                "text_preview": request.resume_text[:200] if hasattr(request, 'resume_text') else ""
            }
        )

    except Exception as e:
        logger.error(f"{LoggingConstants.ROUTER_PREFIX} {LoggingConstants.ERROR_INDICATOR} Unexpected error during analysis: {str(e)}", exc_info=True)
        logger.error("*" * 70)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "detail": HTTPConstants.INTERNAL_ERROR,
                "skills_preview": request.skills[:5] if hasattr(request, 'skills') else [],
                "text_preview": request.resume_text[:200] if hasattr(request, 'resume_text') else ""
            }
        )


@router.get(
    "/supported-signals",
    summary="Get Supported Proficiency Signals",
    description="Get information about proficiency signals used for skill analysis",
    tags=["Skill Analysis", "Info"]
)
async def get_supported_proficiency_signals():
    """
    Get detailed information about proficiency signals used in skill analysis.

    Returns comprehensive information about:
    - Signal types and their descriptions
    - Examples of each signal type
    - Scoring weights and thresholds
    - Supported keywords and verbs

    Returns:
        Dictionary containing signal types, examples, and scoring information
    """
    try:
        signals_info = SkillIntelligenceEngine.get_supported_proficiency_signals()

        return {
            "supported_signals": signals_info["signal_types"],
            "scoring_thresholds": signals_info["scoring_thresholds"],
            "total_signal_types": len(signals_info["signal_types"]),
            "message": "Skill proficiency analysis uses these signals with weighted scoring",
            "methodology": {
                "context_window": "±100 characters around skill mentions",
                "case_sensitivity": "Case-insensitive matching",
                "deduplication": "Duplicate signals are removed",
                "confidence_scoring": "Based on signal strength and quantity"
            }
        }

    except Exception as e:
        logger.error(f"Error getting supported signals: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve supported proficiency signals"
        )


@router.post(
    "/validate-input",
    summary="Validate Input for Skill Analysis",
    description="Validate skills and resume text for proficiency analysis",
    tags=["Skill Analysis", "Validation"]
)
async def validate_skill_analysis_input(request: SkillAnalysisRequest):
    """
    Validate input data for skill proficiency analysis without performing the analysis.

    Useful for pre-flight validation before starting analysis.

    Args:
        request: SkillAnalysisRequest containing skills and resume text to validate

    Returns:
        Validation result with recommendations
    """
    try:
        logger.info(f"Validating input for skill analysis: {len(request.skills)} skills")

        validation_result = SkillIntelligenceEngine.validate_analysis_input(
            request.skills, request.resume_text
        )

        if validation_result["is_valid"]:
            logger.info("Input validation passed for skill analysis")
            return {
                "status": "valid",
                "message": "Input is suitable for skill proficiency analysis",
                "skills_count": validation_result["skills_count"],
                "text_length": validation_result["text_length"],
                "estimated_processing_time": f"{len(request.skills) * 0.1:.2f} seconds"
            }
        else:
            logger.warning(f"Input validation failed: {validation_result['error']}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "ValidationFailed",
                    "detail": validation_result["error"],
                    "suggestions": validation_result.get("suggestions", []),
                    "skills_preview": request.skills[:5] if request.skills else [],
                    "text_preview": request.resume_text[:100] if request.resume_text else ""
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during input validation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "ValidationError",
                "detail": "Failed to validate input for skill analysis"
            }
        )


@router.get(
    "/health",
    summary="Skill Analysis Service Health Check",
    description="Check if the skill analysis service is working properly",
    tags=["Health"]
)
async def health_check():
    """
    Health check endpoint for the skill analysis service

    Returns:
        Service health status with capability information
    """
    try:
        # Test basic functionality
        engine = SkillIntelligenceEngine()
        signals_info = SkillIntelligenceEngine.get_supported_proficiency_signals()

        return {
            "status": "healthy",
            "service": "CVision Skill Intelligence Engine",
            "version": "1.0.0",
            "capabilities": {
                "signal_types": len(signals_info["signal_types"]),
                "level_keywords": len(SkillIntelligenceEngine.LEVEL_KEYWORDS),
                "strong_verbs": len(SkillIntelligenceEngine.STRONG_VERBS),
                "weak_verbs": len(SkillIntelligenceEngine.WEAK_VERBS),
                "context_window": engine.context_window
            },
            "proficiency_levels": list(SkillIntelligenceEngine.LEVEL_THRESHOLDS.keys())
        }

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Skill analysis service health check failed"
        )
