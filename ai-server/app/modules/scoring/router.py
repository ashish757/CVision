"""
FastAPI router for Global Resume Scoring endpoints
"""

from fastapi import APIRouter, HTTPException, status
from .schemas import (
    GlobalScoringRequest,
    GlobalScoringResponse,
    ScoringError,
    ScoringHealthResponse,
    ScoringWeights
)
from .service import GlobalResumeScoring
import logging

# Get logger for this module
logger = logging.getLogger(__name__)

# Create router instance
router = APIRouter(
    prefix="/scoring",
    tags=["Global Resume Scoring"],
    responses={
        404: {"model": ScoringError},
        500: {"model": ScoringError}
    }
)


@router.post(
    "/compute",
    response_model=GlobalScoringResponse,
    status_code=status.HTTP_200_OK,
    summary="Compute Global Resume Score",
    description="""
    Combine outputs from multiple analysis modules into a comprehensive final resume score.
    
    This endpoint analyzes:
    - Skills proficiency and diversity
    - Experience quality and achievements  
    - Resume structure and completeness
    - Configurable weighted scoring
    
    Returns detailed breakdown and actionable insights.
    """
)
async def compute_global_score(request: GlobalScoringRequest):
    """
    Compute comprehensive global resume score

    Args:
        request: Global scoring request with analysis results

    Returns:
        GlobalScoringResponse: Final score with detailed breakdown

    Raises:
        HTTPException: On scoring computation failure
    """
    try:
        logger.info(f"Received global scoring request for resume with {len(request.skill_analysis)} skills")

        # Validate input components
        if not request.skill_analysis and not request.experience_analysis:
            logger.warning("No analysis data provided for scoring")

        # Compute global score using the service
        result = GlobalResumeScoring.compute_final_resume_score(
            skill_analysis=request.skill_analysis,
            experience_analysis=request.experience_analysis,
            structured_sections=request.structured_sections,
            scoring_weights=request.scoring_weights
        )

        logger.info(f"Global scoring completed - Final score: {result.overall_score}, "
                   f"Tier: {result.recommendation_tier}")

        return result

    except Exception as e:
        logger.error(f"Global scoring failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Global scoring computation failed: {str(e)}"
        )


@router.post(
    "/weights/validate",
    summary="Validate Scoring Weights",
    description="Validate that custom scoring weights sum to 1.0 and are within valid ranges"
)
async def validate_scoring_weights(weights: ScoringWeights):
    """
    Validate scoring weights configuration

    Args:
        weights: Scoring weights to validate

    Returns:
        Validation result

    Raises:
        HTTPException: If weights are invalid
    """
    try:
        is_valid = weights.validate_weights()

        if not is_valid:
            total = weights.skills_weight + weights.experience_weight + weights.achievement_weight + weights.structure_weight
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Scoring weights must sum to 1.0, current total: {total:.3f}"
            )

        return {
            "valid": True,
            "weights": {
                "skills": f"{weights.skills_weight:.1%}",
                "experience": f"{weights.experience_weight:.1%}",
                "achievement": f"{weights.achievement_weight:.1%}",
                "structure": f"{weights.structure_weight:.1%}"
            },
            "total": f"{weights.skills_weight + weights.experience_weight + weights.achievement_weight + weights.structure_weight:.1%}"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Weight validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Weight validation failed: {str(e)}"
        )


@router.get(
    "/weights/default",
    response_model=ScoringWeights,
    summary="Get Default Scoring Weights",
    description="Retrieve the default scoring weights used by the system"
)
async def get_default_weights():
    """
    Get default scoring weights

    Returns:
        Default ScoringWeights configuration
    """
    return ScoringWeights()


@router.get(
    "/health",
    response_model=ScoringHealthResponse,
    summary="Scoring Service Health Check",
    description="Check if the global scoring service is working properly"
)
async def health_check():
    """
    Health check endpoint for global scoring service

    Returns:
        ScoringHealthResponse: Service health status and capabilities
    """
    try:
        # Test with minimal data
        from .schemas import SkillProficiency, ExperienceAnalysisData, ResumeStructuredSections

        test_skill = [SkillProficiency(skill="Python", score=75, level="Advanced")]
        test_experience = ExperienceAnalysisData(
            total_experience_years=3,
            seniority_level="Mid",
            achievement_score=60,
            experience_strength_score=70
        )
        test_sections = ResumeStructuredSections()

        test_result = GlobalResumeScoring.compute_final_resume_score(
            skill_analysis=test_skill,
            experience_analysis=test_experience,
            structured_sections=test_sections
        )

        return ScoringHealthResponse(
            status="healthy",
            service="global_resume_scoring",
            version="1.0.0",
            components_available=[
                "skills_scoring",
                "experience_scoring",
                "achievement_scoring",
                "structure_scoring",
                "weighted_combination",
                "insights_generation"
            ],
            default_weights=ScoringWeights()
        )

    except Exception as e:
        logger.error(f"Global scoring health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Global scoring service unhealthy: {str(e)}"
        )


@router.get(
    "/insights/tiers",
    summary="Get Score Tier Information",
    description="Get information about scoring tiers and recommendation levels"
)
async def get_score_tiers():
    """
    Get scoring tier information

    Returns:
        Score tier definitions and thresholds
    """
    return {
        "tiers": {
            "excellent": {"range": "90-100", "description": "Outstanding resume with exceptional qualifications"},
            "good": {"range": "75-89", "description": "Strong resume with solid qualifications"},
            "fair": {"range": "60-74", "description": "Decent resume with room for improvement"},
            "poor": {"range": "0-59", "description": "Resume needs significant improvement"}
        },
        "score_components": {
            "skills": {
                "weight": "35%",
                "factors": ["proficiency_level", "skill_diversity", "critical_skills_bonus"]
            },
            "experience": {
                "weight": "40%",
                "factors": ["years_experience", "seniority_level", "action_verb_quality"]
            },
            "achievement": {
                "weight": "15%",
                "factors": ["quantified_results", "impact_statements", "seniority_adjusted"]
            },
            "structure": {
                "weight": "10%",
                "factors": ["essential_sections", "content_quality", "completeness"]
            }
        }
    }
