"""
Experience Quality Analysis Service for CVision AI Analysis System

This service evaluates the strength and quality of candidate's work experience
using rule-based signal detection and scoring.
"""

import re
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from .schemas import ExperienceAnalysisResponse
from app.core import LoggingConstants

# Get logger for this module
logger = logging.getLogger(__name__)


class ExperienceAnalysisService:
    """Service for analyzing experience quality and strength"""

    # Seniority levels mapping with scores
    SENIORITY_MAPPING = {
        "intern": {"score": 10, "keywords": ["intern", "trainee", "apprentice", "student"]},
        "junior": {"score": 25, "keywords": ["junior", "entry", "associate", "graduate", "fresher"]},
        "mid": {"score": 50, "keywords": ["engineer", "developer", "analyst", "specialist", "consultant"]},
        "senior": {"score": 75, "keywords": ["senior", "sr", "lead", "principal", "staff"]},
        "executive": {"score": 90, "keywords": ["manager", "director", "vp", "vice president", "head", "chief", "cto", "ceo", "architect"]}
    }

    # Strong action verbs that indicate leadership and impact
    STRONG_VERBS = [
        "led", "managed", "directed", "orchestrated", "spearheaded",
        "designed", "architected", "engineered", "developed", "created",
        "implemented", "deployed", "launched", "delivered", "built",
        "optimized", "improved", "enhanced", "streamlined", "automated",
        "transformed", "scaled", "established", "founded", "pioneered",
        "achieved", "accomplished", "exceeded", "increased", "reduced",
        "drove", "executed", "supervised", "coordinated", "facilitated"
    ]

    # Weak verbs that indicate passive involvement
    WEAK_VERBS = [
        "assisted", "helped", "supported", "participated", "involved",
        "responsible", "worked", "handled", "dealt", "used",
        "familiar", "exposed", "learned", "studied", "observed",
        "attended", "contributed", "collaborated", "cooperated"
    ]

    # Achievement indicators
    ACHIEVEMENT_PATTERNS = [
        # Percentages
        r'\b(\d+(?:\.\d+)?%)\b',
        r'\b(\d+(?:\.\d+)?\s*percent)\b',

        # Large numbers with units
        r'\b(\d+(?:,\d{3})*(?:\.\d+)?\s*(?:k|thousand))\b',
        r'\b(\d+(?:,\d{3})*(?:\.\d+)?\s*(?:m|million))\b',
        r'\b(\d+(?:,\d{3})*(?:\.\d+)?\s*(?:b|billion))\b',

        # Revenue/financial terms
        r'\$(\d+(?:,\d{3})*(?:\.\d+)?(?:\s*(?:k|m|b|thousand|million|billion))?)\b',

        # Performance metrics
        r'\b(\d+(?:\.\d+)?x)\s*(?:faster|quicker|improvement|increase)\b',
        r'\b(?:reduced|decreased|saved).*?(\d+(?:\.\d+)?%)\b',
        r'\b(?:increased|improved|boosted).*?(\d+(?:\.\d+)?%)\b',
        r'\b(?:grew|growth).*?(\d+(?:\.\d+)?%)\b'
    ]

    # Date patterns for experience duration calculation
    DATE_PATTERNS = [
        r'\b(\d{4})\s*[-–—]\s*(\d{4})\b',  # 2019 - 2023
        r'\b(\d{4})\s*[-–—]\s*(present)\b',   # 2020 - Present
        r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{4})\s*[-–—]\s*(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{4})\b',  # Jan 2020 - Dec 2023
        r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{4})\s*[-–—]\s*(present)\b',  # Jan 2020 - Present
        r'\b(\d{1,2})/(\d{4})\s*[-–—]\s*(\d{1,2})/(\d{4})\b',  # 01/2020 - 12/2023
        r'\b(\d{1,2})/(\d{4})\s*[-–—]\s*(present)\b'  # 01/2020 - Present
    ]

    @staticmethod
    def analyze_experience(experience_text: str, entities: dict) -> ExperienceAnalysisResponse:
        """
        Analyze experience quality and strength

        Args:
            experience_text: Raw experience section text
            entities: Dictionary containing extracted entities

        Returns:
            ExperienceAnalysisResponse with detailed analysis
        """
        try:
            logger.info(f"{LoggingConstants.SERVICE_PREFIX} Starting experience quality analysis")

            # Initialize response data
            total_years = 0
            seniority_level = "Entry"
            achievement_score = 0
            detected_roles = []
            quantified_achievements = []
            strong_verbs_count = 0
            weak_verbs_count = 0

            if not experience_text.strip():
                logger.warning(f"{LoggingConstants.SERVICE_PREFIX} Empty experience text provided")
                return ExperienceAnalysisResponse(
                    total_experience_years=total_years,
                    seniority_level=seniority_level,
                    achievement_score=achievement_score,
                    experience_strength_score=0,
                    detected_roles=detected_roles,
                    quantified_achievements=quantified_achievements,
                    strong_verbs_count=strong_verbs_count,
                    weak_verbs_count=weak_verbs_count
                )

            # 1. Calculate total experience duration
            total_years = ExperienceAnalysisService._calculate_experience_duration(
                experience_text, entities.get("dates", [])
            )

            # 2. Analyze role seniority
            seniority_level, detected_roles = ExperienceAnalysisService._analyze_role_seniority(
                experience_text, entities.get("job_titles", [])
            )

            # 3. Detect achievement signals
            achievement_score, quantified_achievements = ExperienceAnalysisService._detect_achievements(
                experience_text
            )

            # 4. Analyze action verb strength
            strong_verbs_count, weak_verbs_count = ExperienceAnalysisService._analyze_verb_strength(
                experience_text
            )

            # 5. Calculate overall experience strength score
            experience_strength_score = ExperienceAnalysisService._calculate_experience_score(
                total_years, seniority_level, achievement_score, strong_verbs_count, weak_verbs_count
            )

            logger.info(f"{LoggingConstants.SERVICE_PREFIX} Experience analysis completed:")
            logger.info(f"{LoggingConstants.SERVICE_PREFIX} - Total years: {total_years}")
            logger.info(f"{LoggingConstants.SERVICE_PREFIX} - Seniority: {seniority_level}")
            logger.info(f"{LoggingConstants.SERVICE_PREFIX} - Achievement score: {achievement_score}")
            logger.info(f"{LoggingConstants.SERVICE_PREFIX} - Overall score: {experience_strength_score}")

            return ExperienceAnalysisResponse(
                total_experience_years=total_years,
                seniority_level=seniority_level,
                achievement_score=achievement_score,
                experience_strength_score=experience_strength_score,
                detected_roles=detected_roles,
                quantified_achievements=quantified_achievements,
                strong_verbs_count=strong_verbs_count,
                weak_verbs_count=weak_verbs_count
            )

        except Exception as e:
            logger.error(f"{LoggingConstants.SERVICE_PREFIX} Error in experience analysis: {str(e)}")
            # Return default response on error
            return ExperienceAnalysisResponse(
                total_experience_years=0,
                seniority_level="Entry",
                achievement_score=0,
                experience_strength_score=0,
                detected_roles=[],
                quantified_achievements=[],
                strong_verbs_count=0,
                weak_verbs_count=0
            )

    @staticmethod
    def _calculate_experience_duration(text: str, date_entities: List[str]) -> int:
        """
        Calculate total years of experience from text and date entities

        Args:
            text: Experience text
            date_entities: List of extracted date entities

        Returns:
            Total years of experience
        """
        current_year = datetime.now().year
        text_lower = text.lower()
        total_years = 0

        # First, try to extract from explicit experience mentions
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)\+?\s*(?:years?|yrs?)\s*in\s*\w+',
        ]

        years_mentioned = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                try:
                    years = int(match)
                    if 0 <= years <= 50:  # Reasonable range
                        years_mentioned.append(years)
                except ValueError:
                    continue

        if years_mentioned:
            total_years = max(years_mentioned)
            logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Found explicit experience: {total_years} years")
            return total_years

        # If no explicit mentions, try to calculate from date ranges
        date_ranges = []

        # Process both text and date entities
        all_text = text + " " + " ".join(date_entities)

        for pattern in ExperienceAnalysisService.DATE_PATTERNS:
            matches = re.finditer(pattern, all_text, re.IGNORECASE)
            for match in matches:
                groups = match.groups()

                # Handle different date formats
                if len(groups) == 2:  # Format: 2019 - 2023, 2020 - Present, Jan 2020 - Dec 2023, Jan 2020 - Present
                    try:
                        start_year = int(groups[0])
                        end_year = current_year if groups[1].lower() == 'present' else int(groups[1])
                        if start_year <= end_year:
                            date_ranges.append((start_year, end_year))
                    except ValueError:
                        continue

                elif len(groups) == 4:  # Format: 01/2020 - 12/2023
                    try:
                        start_year = int(groups[1])
                        end_year = int(groups[3])
                        if start_year <= end_year:
                            date_ranges.append((start_year, end_year))
                    except ValueError:
                        continue

                elif len(groups) == 3:  # Format: 01/2020 - Present
                    try:
                        start_year = int(groups[1])
                        end_year = current_year if groups[2].lower() == 'present' else int(groups[2])
                        if start_year <= end_year:
                            date_ranges.append((start_year, end_year))
                    except ValueError:
                        continue

        if date_ranges:
            # Calculate total experience considering potential overlaps
            date_ranges.sort()
            merged_ranges = []

            for start, end in date_ranges:
                if not merged_ranges or start > merged_ranges[-1][1]:
                    merged_ranges.append((start, end))
                else:
                    merged_ranges[-1] = (merged_ranges[-1][0], max(merged_ranges[-1][1], end))

            total_years = sum(end - start for start, end in merged_ranges)
            logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Calculated experience from dates: {total_years} years")

        return min(total_years, 50)  # Cap at 50 years for reasonableness

    @staticmethod
    def _analyze_role_seniority(text: str, job_titles: List[str]) -> Tuple[str, List[str]]:
        """
        Analyze role seniority level

        Args:
            text: Experience text
            job_titles: List of extracted job titles

        Returns:
            Tuple of (seniority_level, detected_roles)
        """
        text_lower = text.lower()
        all_titles = " ".join(job_titles).lower() + " " + text_lower
        detected_roles = []
        max_seniority_score = 0
        seniority_level = "Entry"

        # Check for seniority keywords in text and job titles
        for level, data in ExperienceAnalysisService.SENIORITY_MAPPING.items():
            for keyword in data["keywords"]:
                if keyword in all_titles:
                    if data["score"] > max_seniority_score:
                        max_seniority_score = data["score"]
                        seniority_level = level.capitalize()

                    # Extract roles containing this keyword
                    pattern = rf'\b[^.]*{re.escape(keyword)}[^.]*\b'
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for match in matches:
                        clean_role = match.strip()
                        if clean_role and len(clean_role) < 100:  # Reasonable length
                            detected_roles.append(clean_role)

        # Remove duplicates while preserving order
        detected_roles = list(dict.fromkeys(detected_roles))

        logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Detected seniority: {seniority_level}, Roles: {len(detected_roles)}")

        return seniority_level, detected_roles[:5]  # Limit to top 5 roles

    @staticmethod
    def _detect_achievements(text: str) -> Tuple[int, List[str]]:
        """
        Detect quantified achievements in experience text

        Args:
            text: Experience text

        Returns:
            Tuple of (achievement_score, quantified_achievements)
        """
        achievements = []
        achievement_keywords = [
            "increased", "improved", "reduced", "decreased", "saved", "generated",
            "achieved", "exceeded", "delivered", "boosted", "optimized", "enhanced",
            "grew", "growth", "revenue", "profit", "efficiency", "performance"
        ]

        # Find quantified achievements
        for pattern in ExperienceAnalysisService.ACHIEVEMENT_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Get context around the match
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()

                # Check if context contains achievement keywords
                if any(keyword in context.lower() for keyword in achievement_keywords):
                    achievements.append(context)

        # Score achievements based on quantity and quality
        achievement_score = 0
        if achievements:
            base_score = min(len(achievements) * 15, 60)  # Up to 60 points for quantity

            # Bonus for high-impact achievements (financial, percentage improvements)
            high_impact_bonus = 0
            for achievement in achievements:
                if any(indicator in achievement.lower() for indicator in ['$', 'million', 'billion', '%', 'percent']):
                    high_impact_bonus += 10

            achievement_score = min(base_score + high_impact_bonus, 100)

        # Remove duplicates and limit
        unique_achievements = list(dict.fromkeys(achievements))[:10]

        logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Detected {len(unique_achievements)} achievements, Score: {achievement_score}")

        return achievement_score, unique_achievements

    @staticmethod
    def _analyze_verb_strength(text: str) -> Tuple[int, int]:
        """
        Analyze action verb strength in experience text

        Args:
            text: Experience text

        Returns:
            Tuple of (strong_verbs_count, weak_verbs_count)
        """
        text_lower = text.lower()
        strong_verbs_count = 0
        weak_verbs_count = 0

        # Count strong verbs
        for verb in ExperienceAnalysisService.STRONG_VERBS:
            strong_verbs_count += len(re.findall(rf'\b{re.escape(verb)}\b', text_lower))

        # Count weak verbs
        for verb in ExperienceAnalysisService.WEAK_VERBS:
            weak_verbs_count += len(re.findall(rf'\b{re.escape(verb)}\b', text_lower))

        logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Verb analysis - Strong: {strong_verbs_count}, Weak: {weak_verbs_count}")

        return strong_verbs_count, weak_verbs_count

    @staticmethod
    def _calculate_experience_score(
        years: int,
        seniority: str,
        achievement_score: int,
        strong_verbs: int,
        weak_verbs: int
    ) -> int:
        """
        Calculate overall experience strength score

        Args:
            years: Total years of experience
            seniority: Seniority level
            achievement_score: Achievement score (0-100)
            strong_verbs: Count of strong action verbs
            weak_verbs: Count of weak action verbs

        Returns:
            Overall experience strength score (0-100)
        """
        # Duration weight (0-40 points)
        duration_score = min(years * 3, 40)

        # Seniority weight (0-25 points)
        seniority_mapping = {
            "Intern": 5, "Junior": 10, "Mid": 15,
            "Senior": 20, "Executive": 25, "Entry": 8
        }
        seniority_score = seniority_mapping.get(seniority, 8)

        # Achievement weight (0-25 points) - scale down from 100
        achievement_weight = min(achievement_score * 0.25, 25)

        # Verb strength weight (0-10 points)
        if strong_verbs + weak_verbs > 0:
            verb_ratio = strong_verbs / (strong_verbs + weak_verbs)
            verb_score = min(verb_ratio * 10 + min(strong_verbs, 5), 10)
        else:
            verb_score = 0

        total_score = int(duration_score + seniority_score + achievement_weight + verb_score)

        logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Score breakdown - Duration: {duration_score}, "
                    f"Seniority: {seniority_score}, Achievement: {achievement_weight}, "
                    f"Verb: {verb_score}, Total: {total_score}")

        return min(total_score, 100)
