from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import logging
import os
from app.models.text_extraction import (
    TextExtractionRequest,
    TextExtractionResponse,
    TextExtractionError as TextExtractionErrorModel
)
from app.services.text_extraction_service import TextExtractionService
from app.utils.text_extractor import TextExtractionError

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/extract", tags=["Text Extraction"])


@router.post(
    "/text",
    response_model=TextExtractionResponse,
    status_code=status.HTTP_200_OK,
    summary="Extract Text from Resume",
    description="Extract raw text content from PDF or DOCX resume files",
    responses={
        200: {
            "description": "Text extracted successfully",
            "model": TextExtractionResponse
        },
        400: {
            "description": "Bad Request - Invalid file or unsupported type",
            "model": TextExtractionErrorModel
        },
        404: {
            "description": "File not found",
            "model": TextExtractionErrorModel
        },
        422: {
            "description": "Unprocessable Entity - File validation failed",
            "model": TextExtractionErrorModel
        },
        500: {
            "description": "Internal server error during text extraction",
            "model": TextExtractionErrorModel
        }
    }
)
async def extract_text(request: TextExtractionRequest):
    """
    Extract text content from a resume file.

    This endpoint accepts a file path to a resume (PDF or DOCX) and extracts
    all text content for further processing.

    **Supported File Types:**
    - PDF files (.pdf) - Uses pdfplumber for text extraction
    - Word documents (.docx) - Uses python-docx for text extraction

    **Features:**
    - Async processing to avoid blocking
    - Text cleaning and validation
    - Detailed error handling
    - Processing time tracking

    Args:
        request: TextExtractionRequest containing the file path

    Returns:
        TextExtractionResponse: Extracted text with metadata

    Raises:
        HTTPException: For various error conditions
    """
    try:
        logger.info(f"Received text extraction request for: {request.file_path}")

        # Validate file exists (additional check beyond Pydantic validation)
        if not os.path.exists(request.file_path):
            logger.error(f"File not found: {request.file_path}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "FileNotFound",
                    "detail": f"File not found: {request.file_path}",
                    "file_path": request.file_path
                }
            )

        # Get file size for logging
        file_size = os.path.getsize(request.file_path)
        logger.info(f"Processing file: {os.path.basename(request.file_path)} ({file_size} bytes)")

        # Extract text using the service
        result = await TextExtractionService.extract_text_from_resume(request.file_path)

        logger.info(f"Text extraction successful for: {result.file_name}")
        logger.info(f"Extracted {result.text_length} characters in {result.processing_time_seconds}s")

        return result

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except ValueError as e:
        # Handle validation errors from Pydantic
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "ValidationError",
                "detail": str(e),
                "file_path": request.file_path
            }
        )

    except TextExtractionError as e:
        # Handle text extraction specific errors
        logger.error(f"Text extraction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "ExtractionError",
                "detail": str(e),
                "file_path": request.file_path
            }
        )

    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error during text extraction: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "detail": "An error occurred during text extraction. Please try again.",
                "file_path": request.file_path
            }
        )


@router.post(
    "/validate",
    summary="Validate File for Text Extraction",
    description="Validate if a file can be processed for text extraction",
    tags=["Text Extraction", "Validation"]
)
async def validate_file(request: TextExtractionRequest):
    """
    Validate a file for text extraction without actually extracting text.

    Useful for pre-flight validation before starting extraction.

    Args:
        request: TextExtractionRequest containing the file path

    Returns:
        Validation result with file information
    """
    try:
        logger.info(f"Validating file for extraction: {request.file_path}")

        validation_result = await TextExtractionService.validate_file_for_extraction(request.file_path)

        if validation_result["is_valid"]:
            logger.info(f"File validation passed: {request.file_path}")
            return {
                "status": "valid",
                "message": "File can be processed for text extraction",
                "file_info": validation_result["file_info"],
                "supported_types": validation_result["supported_types"]
            }
        else:
            logger.warning(f"File validation failed: {validation_result['error']}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "ValidationFailed",
                    "detail": validation_result["error"],
                    "file_path": request.file_path,
                    "supported_types": validation_result["supported_types"]
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during file validation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "ValidationError",
                "detail": "Failed to validate file for text extraction",
                "file_path": request.file_path
            }
        )


@router.get(
    "/supported-types",
    summary="Get Supported File Types",
    description="Get list of file types supported for text extraction",
    tags=["Text Extraction", "Info"]
)
async def get_supported_file_types():
    """
    Get list of file types supported for text extraction.

    Returns:
        Dictionary of supported file extensions and descriptions
    """
    try:
        supported_types = TextExtractionService.get_supported_file_types()

        return {
            "supported_types": supported_types,
            "total_types": len(supported_types),
            "message": "Text extraction is supported for the listed file types"
        }

    except Exception as e:
        logger.error(f"Error getting supported file types: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve supported file types"
        )


@router.get(
    "/health",
    summary="Text Extraction Service Health Check",
    description="Check if the text extraction service is working properly",
    tags=["Health"]
)
async def health_check():
    """
    Health check endpoint for the text extraction service

    Returns:
        Service health status
    """
    return {
        "status": "healthy",
        "service": "CVision Text Extraction Service",
        "version": "1.0.0",
        "supported_types": list(TextExtractionService.get_supported_file_types().keys())
    }
