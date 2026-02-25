"""
FastAPI router for Evaluation Report Generation endpoints
"""

from fastapi import APIRouter, HTTPException, status
from .schemas import (
    EvaluationReportRequest,
    EvaluationReportResponse,
    ReportGenerationError,
    ReportHealthResponse,
    ReportTemplateConfig
)
from .service import EvaluationReportGenerator
import logging

# Get logger for this module
logger = logging.getLogger(__name__)

# Create router instance
router = APIRouter(
    prefix="/report-generation",
    tags=["Evaluation Report Generation"],
    responses={
        404: {"model": ReportGenerationError},
        500: {"model": ReportGenerationError}
    }
)


@router.post(
    "/generate",
    response_model=EvaluationReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Evaluation Report",
    description="""
    Convert resume scores and analysis outputs into a structured, human-readable evaluation report.
    
    This endpoint creates comprehensive reports including:
    - Executive summary and profile classification
    - Detailed strengths and weaknesses analysis  
    - Actionable recommendations for improvement
    - Skills, experience, and structure evaluations
    - Prioritized next steps for career development
    
    The report uses deterministic, rule-based logic to ensure consistent and meaningful insights.
    """
)
async def generate_evaluation_report(request: EvaluationReportRequest):
    """
    Generate comprehensive evaluation report

    Args:
        request: Evaluation report request with analysis results

    Returns:
        EvaluationReportResponse: Comprehensive structured evaluation report

    Raises:
        HTTPException: On report generation failure
    """
    try:
        logger.info(f"Received evaluation report generation request - Score: {request.scoring_result.overall_score}/100")

        # Validate input data
        if request.scoring_result.overall_score < 0 or request.scoring_result.overall_score > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Overall score must be between 0 and 100"
            )

        # Generate the evaluation report
        report = EvaluationReportGenerator.generate_evaluation_report(
            scoring_result=request.scoring_result,
            skill_analysis=request.skill_analysis,
            experience_analysis=request.experience_analysis
        )

        logger.info(f"Evaluation report generated successfully - "
                   f"Profile: {report.profile_tier}, "
                   f"Strengths: {len(report.strengths)}, "
                   f"Recommendations: {len(report.recommendations)}")

        return report

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Evaluation report generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation failed: {str(e)}"
        )


@router.post(
    "/generate-custom",
    response_model=EvaluationReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Custom Evaluation Report",
    description="Generate evaluation report with custom configuration and thresholds"
)
async def generate_custom_evaluation_report(
    request: EvaluationReportRequest,
    config: ReportTemplateConfig
):
    """
    Generate evaluation report with custom configuration

    Args:
        request: Evaluation report request with analysis results
        config: Custom report configuration and thresholds

    Returns:
        EvaluationReportResponse: Customized evaluation report
    """
    try:
        logger.info(f"Received custom evaluation report request with custom config")

        # Generate report with custom configuration
        report = EvaluationReportGenerator.generate_evaluation_report(
            scoring_result=request.scoring_result,
            skill_analysis=request.skill_analysis,
            experience_analysis=request.experience_analysis,
            config=config
        )

        logger.info(f"Custom evaluation report generated - Profile: {report.profile_tier}")

        return report

    except Exception as e:
        logger.error(f"Custom evaluation report generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Custom report generation failed: {str(e)}"
        )


@router.get(
    "/template/default",
    response_model=ReportTemplateConfig,
    summary="Get Default Report Template",
    description="Retrieve the default report generation configuration and thresholds"
)
async def get_default_template():
    """
    Get default report template configuration

    Returns:
        ReportTemplateConfig: Default configuration settings
    """
    return ReportTemplateConfig()


@router.post(
    "/template/validate",
    summary="Validate Report Template",
    description="Validate report template configuration parameters"
)
async def validate_report_template(config: ReportTemplateConfig):
    """
    Validate report template configuration

    Args:
        config: Report template configuration to validate

    Returns:
        Validation result
    """
    try:
        # Basic validation checks
        if config.high_score_threshold <= config.moderate_score_threshold:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="High score threshold must be greater than moderate score threshold"
            )

        if config.high_skill_threshold <= config.low_skill_threshold:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="High skill threshold must be greater than low skill threshold"
            )

        if not (0 <= config.moderate_score_threshold <= 100):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Thresholds must be between 0 and 100"
            )

        return {
            "valid": True,
            "configuration": {
                "high_score_threshold": config.high_score_threshold,
                "moderate_score_threshold": config.moderate_score_threshold,
                "high_skill_threshold": config.high_skill_threshold,
                "low_skill_threshold": config.low_skill_threshold,
                "strong_achievement_threshold": config.strong_achievement_threshold
            },
            "message": "Report template configuration is valid"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Template validation failed: {str(e)}"
        )


@router.get(
    "/health",
    response_model=ReportHealthResponse,
    summary="Report Generation Health Check",
    description="Check if the evaluation report generation service is working properly"
)
async def health_check():
    """
    Health check endpoint for report generation service

    Returns:
        ReportHealthResponse: Service health status and capabilities
    """
    try:
        # Test report generation with minimal data
        from .schemas import ScoringResultData, SkillEvaluation, ExperienceEvaluation

        test_scoring = ScoringResultData(
            overall_score=75,
            skills_score=70.0,
            experience_score=80.0,
            achievement_score=65.0,
            structure_score=90.0,
            recommendation_tier="Good"
        )

        test_skills = [
            SkillEvaluation(skill="Python", score=75, level="Advanced")
        ]

        test_experience = ExperienceEvaluation(
            total_experience_years=5,
            seniority_level="Mid",
            achievement_score=65,
            experience_strength_score=70
        )

        test_report = EvaluationReportGenerator.generate_evaluation_report(
            scoring_result=test_scoring,
            skill_analysis=test_skills,
            experience_analysis=test_experience
        )

        return ReportHealthResponse(
            status="healthy",
            service="evaluation_report_generation",
            version="1.0.0",
            supported_formats=["structured_json", "detailed_breakdown", "actionable_insights"],
            evaluation_criteria={
                "high_score_threshold": 80,
                "moderate_score_threshold": 60,
                "high_skill_threshold": 70,
                "low_skill_threshold": 40,
                "strong_achievement_threshold": 75
            }
        )

    except Exception as e:
        logger.error(f"Report generation health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Report generation service unhealthy: {str(e)}"
        )


@router.get(
    "/criteria",
    summary="Get Evaluation Criteria",
    description="Get detailed information about evaluation criteria and report generation logic"
)
async def get_evaluation_criteria():
    """
    Get evaluation criteria and report generation methodology

    Returns:
        Detailed evaluation criteria information
    """
    return {
        "profile_classifications": {
            "strong_profile": {
                "threshold": "80-100",
                "description": "Excellent qualifications with strong skills and experience",
                "characteristics": ["High proficiency skills", "Substantial experience", "Quantified achievements"]
            },
            "moderate_profile": {
                "threshold": "60-79",
                "description": "Solid foundational skills with opportunities for enhancement",
                "characteristics": ["Good skill base", "Relevant experience", "Some improvement areas"]
            },
            "developing_profile": {
                "threshold": "0-59",
                "description": "Shows potential but needs significant improvement",
                "characteristics": ["Skill development needed", "Limited experience", "Focus on fundamentals"]
            }
        },
        "evaluation_components": {
            "strengths_identification": [
                "High proficiency skills (>70)",
                "Strong experience quality",
                "Quantified achievements",
                "Leadership indicators",
                "Complete resume structure"
            ],
            "weaknesses_identification": [
                "Low proficiency skills (<40)",
                "Limited skill diversity",
                "Weak impact statements",
                "Missing achievements",
                "Incomplete sections"
            ],
            "recommendations_generation": [
                "Skill enhancement opportunities",
                "Experience improvement strategies",
                "Achievement quantification",
                "Language strengthening",
                "Structure optimization"
            ]
        },
        "critical_skills": [
            "python", "java", "javascript", "aws", "react", "docker",
            "kubernetes", "sql", "machine learning", "node.js"
        ],
        "methodology": "Rule-based deterministic analysis with configurable thresholds"
    }
