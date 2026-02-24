"""
FastAPI router for Experience Quality Analysis endpoints
"""

from fastapi import APIRouter, HTTPException, status
from .schemas import (
    ExperienceAnalysisRequest,
    ExperienceAnalysisResponse,
    ExperienceAnalysisError
)
from .service import ExperienceAnalysisService
import logging

# Get logger for this module
logger = logging.getLogger(__name__)

# Create router instance
router = APIRouter(
    prefix="/experience-analysis",
    tags=["Experience Analysis"],
    responses={
        404: {"model": ExperienceAnalysisError},
        500: {"model": ExperienceAnalysisError}
    }
)


@router.post(
    "/analyze",
    response_model=ExperienceAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze Experience Quality",
    description="""
    Evaluate the strength and quality of candidate's work experience using rule-based analysis.
    
    This endpoint analyzes:
    - Total experience duration from date patterns
    - Role seniority level detection  
    - Quantified achievement signals
    - Action verb strength analysis
    - Comprehensive experience strength scoring
    """
)
async def analyze_experience(request: ExperienceAnalysisRequest):
    """
    Analyze experience quality and strength

    Args:
        request: Experience analysis request containing experience text and entities

    Returns:
        ExperienceAnalysisResponse: Detailed experience quality analysis

    Raises:
        HTTPException: On analysis failure
    """
    try:
        logger.info(f"Received experience analysis request for {len(request.experience_text)} characters of text")

        # Validate input
        if not request.experience_text.strip():
            logger.warning("Empty experience text provided")

        # Analyze experience using the service
        result = ExperienceAnalysisService.analyze_experience(
            experience_text=request.experience_text,
            entities=request.entities
        )

        logger.info(f"Experience analysis completed - Score: {result.experience_strength_score}, "
                   f"Seniority: {result.seniority_level}, Years: {result.total_experience_years}")

        return result

    except Exception as e:
        logger.error(f"Experience analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Experience analysis failed: {str(e)}"
        )


@router.get(
    "/health",
    summary="Experience Analysis Health Check",
    description="Check if the experience analysis service is working properly"
)
async def health_check():
    """
    Health check endpoint for experience analysis service

    Returns:
        Dict: Service health status
    """
    try:
        # Test with minimal data
        test_result = ExperienceAnalysisService.analyze_experience("", {})

        return {
            "status": "healthy",
            "service": "experience_analysis",
            "version": "1.0.0",
            "capabilities": [
                "experience_duration_calculation",
                "seniority_level_detection",
                "achievement_signal_detection",
                "action_verb_analysis",
                "comprehensive_scoring"
            ]
        }
    except Exception as e:
        logger.error(f"Experience analysis health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Experience analysis service unhealthy: {str(e)}"
        )
