from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import logging
import os
from app.models.analysis import AnalyzeRequest, AnalyzeResponse, ErrorResponse
from app.services.analysis_service import AnalysisService

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analyze", tags=["Analysis"])


@router.post(
    "",
    response_model=AnalyzeResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze Resume",
    description="Analyze a resume file and return extracted information including skills, experience, and score",
    responses={
        200: {
            "description": "Analysis completed successfully",
            "model": AnalyzeResponse
        },
        400: {
            "description": "Bad Request - Invalid file or file type",
            "model": ErrorResponse
        },
        404: {
            "description": "File not found",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error during analysis",
            "model": ErrorResponse
        }
    }
)
async def analyze_resume(request: AnalyzeRequest):
    """
    Analyze a resume file and return extracted information.

    This endpoint accepts a file path to a resume that has been uploaded
    by another service and performs AI analysis to extract:
    - Skills and technologies
    - Years of experience
    - Education level
    - Overall resume score

    Args:
        request: AnalyzeRequest containing the file path

    Returns:
        AnalyzeResponse: Analysis results with extracted information

    Raises:
        HTTPException: For various error conditions
    """
    try:
        # Validate file exists
        if not os.path.exists(request.file_path):
            logger.error(f"File not found: {request.file_path}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File not found: {request.file_path}"
            )

        # Validate file type
        if not AnalysisService.validate_file_type(request.file_path):
            logger.error(f"Unsupported file type: {request.file_path}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type. Only PDF and DOCX files are supported."
            )

        # Get file info for logging
        file_size_mb = AnalysisService.get_file_size_mb(request.file_path)
        logger.info(f"Processing file: {os.path.basename(request.file_path)} ({file_size_mb} MB)")

        # Perform analysis
        result = await AnalysisService.analyze_resume(request.file_path)

        logger.info(f"Analysis successful for: {os.path.basename(request.file_path)}")
        return result

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except ValueError as e:
        # Handle validation errors
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error during analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during resume analysis. Please try again."
        )


@router.get(
    "/health",
    summary="Health Check",
    description="Check if the analysis service is running properly",
    tags=["Health"]
)
async def health_check():
    """
    Health check endpoint for the analysis service

    Returns:
        dict: Service status information
    """
    return {
        "status": "healthy",
        "service": "CVision AI Analysis Service",
        "version": "1.0.0"
    }
