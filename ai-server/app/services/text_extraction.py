import asyncio
import time
from typing import Dict, Any

from app.schemas.text_extraction import TextExtractionResponse
from app.utils.text_extractor import TextExtractor, TextExtractionError
from app.core import get_logger, LoggingConstants

# Get logger for this module
logger = get_logger(__name__)


class TextExtractionService:
    """Service for handling text extraction from resume files"""

    @staticmethod
    async def extract_text_from_resume(file_path: str) -> TextExtractionResponse:
        """
        Extract text from a resume file

        Args:
            file_path: Path to the resume file

        Returns:
            TextExtractionResponse: Extracted text and metadata

        Raises:
            TextExtractionError: If extraction fails
        """
        start_time = time.time()

        try:
            logger.info("=" * 50)
            logger.info(f"{LoggingConstants.SERVICE_PREFIX} Starting text extraction for file: {file_path}")

            # Extract text using the utility
            extracted_text, file_info = await TextExtractor.extract_text(file_path)
            logger.info(f"{LoggingConstants.SERVICE_PREFIX} Raw text extracted: {len(extracted_text)} characters")

            # Clean the extracted text
            cleaned_text = TextExtractor.clean_extracted_text(extracted_text)
            logger.info(f"{LoggingConstants.SERVICE_PREFIX} Text cleaned: {len(cleaned_text)} characters")

            # Validate text quality
            if not TextExtractor.validate_extracted_text(cleaned_text):
                logger.error(f"{LoggingConstants.SERVICE_PREFIX} Text quality validation failed for: {file_path}")
                raise TextExtractionError("Extracted text quality is insufficient")

            # Calculate final processing time
            processing_time = time.time() - start_time

            # Create response
            response = TextExtractionResponse(
                file_name=file_info["file_name"],
                text_length=len(cleaned_text),
                extracted_text=cleaned_text,
                file_type=file_info["file_type"],
                processing_time_seconds=round(processing_time, 3)
            )

            logger.info(f"{LoggingConstants.SERVICE_PREFIX} {LoggingConstants.SUCCESS_INDICATOR} Text extraction completed for {file_info['file_name']}")
            logger.info(f"{LoggingConstants.SERVICE_PREFIX} {LoggingConstants.SUCCESS_INDICATOR} Extracted {len(cleaned_text)} characters in {processing_time:.3f} seconds")
            logger.info("=" * 50)

            return response

        except TextExtractionError as e:
            logger.error(f"{LoggingConstants.SERVICE_PREFIX} {LoggingConstants.ERROR_INDICATOR} Extraction failed: {str(e)}")
            logger.error("=" * 50)
            # Re-raise text extraction errors
            raise
        except Exception as e:
            logger.error(f"{LoggingConstants.SERVICE_PREFIX} {LoggingConstants.ERROR_INDICATOR} Unexpected error: {str(e)}")
            logger.error("=" * 50)
            raise TextExtractionError(f"Text extraction failed: {str(e)}")

    @staticmethod
    def get_supported_file_types() -> Dict[str, str]:
        """
        Get list of supported file types

        Returns:
            Dictionary of supported file extensions and descriptions
        """
        from app.core.constants import TextExtractionConstants
        return {
            ".pdf": "Portable Document Format",
            ".docx": "Microsoft Word Document (Office Open XML)"
        }

    @staticmethod
    async def validate_file_for_extraction(file_path: str) -> Dict[str, Any]:
        """
        Validate a file for text extraction

        Args:
            file_path: Path to the file

        Returns:
            Validation result with file information
        """
        try:
            # Get file information
            file_info = TextExtractor.get_file_info(file_path)

            # Check if file type is supported
            supported_types = TextExtractionService.get_supported_file_types()
            is_supported = file_info["file_extension"] in supported_types

            return {
                "is_valid": is_supported,
                "file_info": file_info,
                "supported_types": list(supported_types.keys()),
                "error": None if is_supported else f"Unsupported file type: {file_info['file_extension']}"
            }

        except Exception as e:
            return {
                "is_valid": False,
                "file_info": None,
                "supported_types": list(TextExtractionService.get_supported_file_types().keys()),
                "error": str(e)
            }
