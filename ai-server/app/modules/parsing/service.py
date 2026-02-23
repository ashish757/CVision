import re
import time
from typing import Dict, List, Tuple, Optional
from .schemas import ResumeParsingResponse

# Import core components - using try/except for better error handling
try:
    from app.core import get_logger, LoggingConstants
    logger = get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

    # Fallback constants if import fails
    class LoggingConstants:
        SERVICE_PREFIX = "[SERVICE]"


class ResumeParsingService:
    """Service for parsing resume text into structured sections"""

    # Dictionary mapping section types to their possible keywords/headings
    SECTION_KEYWORDS = {
        "summary": [
            "summary", "profile", "objective", "professional summary",
            "career objective", "professional profile", "about me",
            "overview", "career summary", "personal statement"
        ],
        "skills": [
            "skills", "technical skills", "core competencies", "competencies",
            "technical competencies", "key skills", "expertise", "technologies",
            "technical expertise", "programming skills", "software skills",
            "tools and technologies", "technical proficiencies"
        ],
        "experience": [
            "experience", "work experience", "professional experience",
            "employment history", "career history", "work history",
            "professional background", "employment", "career",
            "work", "positions held", "professional positions"
        ],
        "education": [
            "education", "educational background", "academic background",
            "academic qualifications", "academic history", "qualifications",
            "degrees", "academic achievements", "schooling", "universities",
            "academic", "studies"
        ],
        "projects": [
            "projects", "key projects", "notable projects", "project experience",
            "project highlights", "portfolio", "work samples", "achievements",
            "accomplishments", "personal projects", "side projects"
        ],
        "certifications": [
            "certifications", "certificates", "professional certifications",
            "licenses", "credentials", "training", "professional development",
            "continuing education", "professional training", "courses",
            "certified", "accreditation"
        ]
    }

    @staticmethod
    def split_resume_into_sections(text: str) -> ResumeParsingResponse:
        """
        Split raw resume text into organized sections

        Args:
            text: Raw resume text

        Returns:
            ResumeParsingResponse: Structured sections with metadata
        """
        start_time = time.time()

        logger.info("=" * 60)
        logger.info(f"{LoggingConstants.SERVICE_PREFIX} Starting resume parsing")
        logger.info(f"{LoggingConstants.SERVICE_PREFIX} Input text length: {len(text)} characters")

        try:
            # Step 1: Normalize the input text
            normalized_text = ResumeParsingService._normalize_text(text)
            logger.info(f"{LoggingConstants.SERVICE_PREFIX} Text normalized: {len(normalized_text)} characters")

            # Step 2: Detect section boundaries
            sections = ResumeParsingService._detect_and_extract_sections(normalized_text)
            logger.info(f"{LoggingConstants.SERVICE_PREFIX} Detected {len([s for s in sections.values() if s.strip()])} sections")

            # Step 3: Calculate processing time
            processing_time = time.time() - start_time

            # Step 4: Create response
            response = ResumeParsingResponse(
                summary=sections.get("summary", ""),
                skills=sections.get("skills", ""),
                experience=sections.get("experience", ""),
                education=sections.get("education", ""),
                projects=sections.get("projects", ""),
                certifications=sections.get("certifications", ""),
                other=sections.get("other", ""),
                sections_found=len([s for s in sections.values() if s.strip()]),
                processing_time_seconds=round(processing_time, 3)
            )

            # Log results
            ResumeParsingService._log_parsing_results(sections, processing_time)
            logger.info("=" * 60)

            return response

        except Exception as e:
            logger.error(f"{LoggingConstants.SERVICE_PREFIX} ❌ Parsing failed: {str(e)}")
            logger.error("=" * 60)
            raise

    @staticmethod
    def _normalize_text(text: str) -> str:
        """
        Normalize whitespace and line breaks in the text

        Args:
            text: Raw text

        Returns:
            Normalized text
        """
        if not text or not text.strip():
            return ""

        # Replace multiple whitespaces with single space
        text = re.sub(r'\s+', ' ', text)

        # Replace multiple line breaks with double line break
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)

        # Clean up extra spaces around line breaks
        text = re.sub(r'\s*\n\s*', '\n', text)

        # Remove leading/trailing whitespace
        text = text.strip()

        return text

    @staticmethod
    def _detect_and_extract_sections(text: str) -> Dict[str, str]:
        """
        Detect section headings and extract content for each section

        Args:
            text: Normalized text

        Returns:
            Dictionary with section names as keys and content as values
        """
        sections = {
            "summary": "",
            "skills": "",
            "experience": "",
            "education": "",
            "projects": "",
            "certifications": "",
            "other": ""
        }

        if not text:
            return sections

        # Split text into lines for processing
        lines = text.split('\n')

        # Find section boundaries
        section_boundaries = ResumeParsingService._find_section_boundaries(lines)

        # Extract content for each detected section
        for i, (section_type, start_line) in enumerate(section_boundaries):
            # Determine end line (start of next section or end of text)
            end_line = section_boundaries[i + 1][1] if i + 1 < len(section_boundaries) else len(lines)

            # Extract section content (skip the heading line)
            section_lines = lines[start_line + 1:end_line]
            section_content = '\n'.join(section_lines).strip()

            if section_content:
                if section_type in sections:
                    sections[section_type] = section_content
                else:
                    # Add unrecognized sections to "other"
                    if sections["other"]:
                        sections["other"] += "\n\n" + section_content
                    else:
                        sections["other"] = section_content

        # If no sections were detected, put everything in "other"
        if not any(sections.values()):
            sections["other"] = text

        return sections

    @staticmethod
    def _find_section_boundaries(lines: List[str]) -> List[Tuple[str, int]]:
        """
        Find section headings and their line positions

        Args:
            lines: List of text lines

        Returns:
            List of tuples (section_type, line_number)
        """
        section_boundaries = []

        for line_idx, line in enumerate(lines):
            line_clean = line.strip()

            # Skip empty lines or very short lines
            if not line_clean or len(line_clean) < 3:
                continue

            # Check if this line looks like a heading
            if ResumeParsingService._is_potential_heading(line_clean):
                section_type = ResumeParsingService._classify_section(line_clean)
                if section_type:
                    section_boundaries.append((section_type, line_idx))
                    logger.debug(f"Detected section '{section_type}' at line {line_idx}: '{line_clean[:50]}...'")

        return section_boundaries

    @staticmethod
    def _is_potential_heading(line: str) -> bool:
        """
        Check if a line looks like a section heading

        Args:
            line: Text line to check

        Returns:
            True if line appears to be a heading
        """
        line = line.strip()

        # Check for common heading patterns
        heading_patterns = [
            # All caps
            r'^[A-Z\s&/\-:]{3,}$',
            # Title case with colons
            r'^[A-Z][a-zA-Z\s&/\-:]*:?\s*$',
            # Surrounded by special characters
            r'^[\*\-=\+]{2,}.*[\*\-=\+]{2,}$',
            # Single word/phrase in caps
            r'^[A-Z]{3,}$',
        ]

        for pattern in heading_patterns:
            if re.match(pattern, line):
                return True

        # Check if line is notably shorter than average and contains key terms
        if len(line.split()) <= 4:  # Short lines more likely to be headings
            line_lower = line.lower()
            for section_keywords in ResumeParsingService.SECTION_KEYWORDS.values():
                for keyword in section_keywords:
                    if keyword in line_lower:
                        return True

        return False

    @staticmethod
    def _classify_section(heading: str) -> Optional[str]:
        """
        Classify a heading into a section type

        Args:
            heading: The heading text

        Returns:
            Section type or None if not recognized
        """
        heading_lower = heading.lower().strip()

        # Remove common formatting characters
        heading_clean = re.sub(r'[:\-\*=\+\s]+', ' ', heading_lower).strip()

        # Check against each section's keywords
        for section_type, keywords in ResumeParsingService.SECTION_KEYWORDS.items():
            for keyword in keywords:
                # Check for exact match or substring match
                if keyword == heading_clean or keyword in heading_clean:
                    return section_type

                # Check if heading contains the keyword with word boundaries
                keyword_pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(keyword_pattern, heading_clean):
                    return section_type

        return None

    @staticmethod
    def _log_parsing_results(sections: Dict[str, str], processing_time: float) -> None:
        """
        Log the parsing results for debugging and monitoring

        Args:
            sections: Parsed sections dictionary
            processing_time: Time taken for parsing
        """
        logger.info(f"{LoggingConstants.SERVICE_PREFIX} 📊 Parsing Results:")
        logger.info(f"{LoggingConstants.SERVICE_PREFIX} ⏱️  Processing time: {processing_time:.3f}s")

        sections_with_content = 0
        for section_name, content in sections.items():
            if content.strip():
                sections_with_content += 1
                content_preview = content[:100].replace('\n', ' ').strip()
                if len(content) > 100:
                    content_preview += "..."
                logger.info(f"{LoggingConstants.SERVICE_PREFIX} ✅ {section_name}: {len(content)} chars - '{content_preview}'")
            else:
                logger.info(f"{LoggingConstants.SERVICE_PREFIX} ❌ {section_name}: empty")

        logger.info(f"{LoggingConstants.SERVICE_PREFIX} 📈 Total sections with content: {sections_with_content}/7")

    @staticmethod
    def get_supported_sections() -> Dict[str, List[str]]:
        """
        Get the supported section types and their keywords

        Returns:
            Dictionary mapping section types to keyword lists
        """
        return ResumeParsingService.SECTION_KEYWORDS.copy()

    @staticmethod
    def validate_text_for_parsing(text: str) -> Dict[str, any]:
        """
        Validate text input for parsing

        Args:
            text: Text to validate

        Returns:
            Validation result dictionary
        """
        if not text or not text.strip():
            return {
                "is_valid": False,
                "error": "Empty text input",
                "suggestions": ["Ensure the resume text is not empty", "Check text extraction process"]
            }

        if len(text.strip()) < 50:
            return {
                "is_valid": False,
                "error": "Text too short for meaningful parsing",
                "suggestions": ["Ensure complete resume text is provided", "Minimum 50 characters required"]
            }

        return {
            "is_valid": True,
            "text_length": len(text),
            "estimated_sections": min(7, len(text.split('\n\n')) + 1)
        }
