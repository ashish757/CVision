import re
import time
from typing import List, Dict, Optional
from .schemas import SkillProficiencyResult, SkillLevel, SkillContextSignal, SkillAnalysisResponse

# Import core components with fallback
try:
    from app.core import get_logger, LoggingConstants
    logger = get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

    # Fallback constants
    class LoggingConstants:
        SERVICE_PREFIX = "[SKILL_ANALYSIS]"
        SUCCESS_INDICATOR = "Success"
        ERROR_INDICATOR = "Error"


class SkillIntelligenceEngine:
    """Advanced skill intelligence engine for analyzing skill proficiency from resume context"""

    # Proficiency level keywords with their score weights
    LEVEL_KEYWORDS = {
        "expert": 90,
        "advanced": 85,
        "proficient": 75,
        "experienced": 70,
        "intermediate": 50,
        "moderate": 45,
        "basic": 30,
        "beginner": 20,
        "novice": 15,
        "familiar": 25,
        "learning": 20
    }

    # Strong action verbs indicating high proficiency
    STRONG_VERBS = {
        "architected": 0.9,
        "designed": 0.8,
        "developed": 0.8,
        "built": 0.7,
        "led": 0.9,
        "managed": 0.8,
        "optimized": 0.8,
        "implemented": 0.7,
        "created": 0.7,
        "engineered": 0.8,
        "deployed": 0.7,
        "maintained": 0.6,
        "integrated": 0.6,
        "configured": 0.6,
        "customized": 0.6,
        "enhanced": 0.7,
        "improved": 0.7,
        "automated": 0.8,
        "streamlined": 0.7,
        "scaled": 0.8
    }

    # Weak verbs indicating lower proficiency
    WEAK_VERBS = {
        "learned": 0.3,
        "studied": 0.3,
        "familiar": 0.3,
        "exposed": 0.2,
        "introduced": 0.3,
        "trained": 0.4,
        "attended": 0.2,
        "participated": 0.3,
        "observed": 0.2,
        "assisted": 0.4,
        "helped": 0.4,
        "supported": 0.4
    }

    # Score thresholds for skill levels
    LEVEL_THRESHOLDS = {
        SkillLevel.BEGINNER: (0, 30),
        SkillLevel.INTERMEDIATE: (30, 60),
        SkillLevel.EXPERT: (60, 100)
    }

    # Weights for different signal types
    SIGNAL_WEIGHTS = {
        "years_experience": 0.6,    # Highest weight
        "level_keyword": 0.4,       # Medium weight
        "strong_verb": 0.3,         # Lower weight
        "weak_verb": -0.2           # Negative weight
    }

    def __init__(self):
        """Initialize the skill intelligence engine"""
        self.context_window = 100  # Characters around skill mention

    def analyze_skill_proficiency(self, skills: List[str], resume_text: str) -> SkillAnalysisResponse:
        """
        Analyze skill proficiency levels from resume text

        Args:
            skills: List of skills to analyze
            resume_text: Full resume text for context analysis

        Returns:
            SkillAnalysisResponse: Comprehensive analysis results
        """
        start_time = time.time()

        logger.info("=" * 70)
        logger.info(f"{LoggingConstants.SERVICE_PREFIX} Starting skill proficiency analysis")
        logger.info(f"{LoggingConstants.SERVICE_PREFIX} Skills to analyze: {len(skills)}")
        logger.info(f"{LoggingConstants.SERVICE_PREFIX} Resume text length: {len(resume_text)} characters")

        try:
            results = []
            for skill in skills:
                result = self._analyze_single_skill(skill, resume_text)
                results.append(result)
                logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Analyzed {skill}: {result.score}/100 ({result.level})")

            # Calculate summary statistics
            processing_time = time.time() - start_time
            average_score = sum(r.score for r in results) / len(results) if results else 0

            # Create level distribution summary
            level_summary = {level.value: 0 for level in SkillLevel}
            for result in results:
                level_summary[result.level.value] += 1

            response = SkillAnalysisResponse(
                results=results,
                total_skills_analyzed=len(results),
                average_proficiency_score=round(average_score, 2),
                processing_time_seconds=round(processing_time, 3),
                summary=level_summary
            )

            self._log_analysis_results(response)
            logger.info("=" * 70)

            return response

        except Exception as e:
            logger.error(f"{LoggingConstants.SERVICE_PREFIX} {LoggingConstants.ERROR_INDICATOR} Analysis failed: {str(e)}")
            logger.error("=" * 70)
            raise

    def _analyze_single_skill(self, skill: str, resume_text: str) -> SkillProficiencyResult:
        """
        Analyze proficiency for a single skill

        Args:
            skill: Skill name to analyze
            resume_text: Resume text

        Returns:
            SkillProficiencyResult: Analysis result for the skill
        """
        # Find all occurrences of the skill in resume text
        skill_occurrences = self._find_skill_occurrences(skill, resume_text)

        if not skill_occurrences:
            # Skill not found in text - return minimal result
            return SkillProficiencyResult(
                skill=skill,
                score=10,  # Minimal score for listed but not mentioned skills
                level=SkillLevel.BEGINNER,
                years_experience=None,
                confidence=0.1,
                signals_detected=["skill listed but no context found"]
            )

        # Extract context windows and detect signals
        signals = []
        for position in skill_occurrences:
            context = self._extract_context_window(resume_text, position, skill)
            skill_signals = self._detect_proficiency_signals(skill, context, position)
            signals.extend(skill_signals)

        # Deduplicate signals
        unique_signals = self._deduplicate_signals(signals)

        # Calculate proficiency score
        score = self._calculate_proficiency_score(unique_signals)

        # Determine skill level
        level = self._score_to_level(score)

        # Extract years of experience if found
        years_experience = self._extract_years_experience(unique_signals)

        # Calculate confidence based on signal strength and quantity
        confidence = self._calculate_confidence(unique_signals, len(skill_occurrences))

        # Format signal descriptions for response
        signal_descriptions = [signal.signal_value for signal in unique_signals]

        return SkillProficiencyResult(
            skill=skill,
            score=score,
            level=level,
            years_experience=years_experience,
            confidence=confidence,
            signals_detected=signal_descriptions
        )

    def _find_skill_occurrences(self, skill: str, text: str) -> List[int]:
        """
        Find all occurrences of a skill in the text

        Args:
            skill: Skill name to search for
            text: Text to search in

        Returns:
            List of positions where skill is mentioned
        """
        positions = []
        text_lower = text.lower()
        skill_lower = skill.lower()

        # Create regex pattern for word boundary matching
        # Handle skills with special characters (e.g., "C++", "C#", ".NET")
        escaped_skill = re.escape(skill_lower)
        pattern = r'\b' + escaped_skill + r'\b'

        try:
            matches = re.finditer(pattern, text_lower)
            positions = [match.start() for match in matches]
        except re.error:
            # Fallback to simple string search if regex fails
            start = 0
            while True:
                pos = text_lower.find(skill_lower, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1

        return positions

    def _extract_context_window(self, text: str, position: int, skill: str) -> str:
        """
        Extract context window around skill mention

        Args:
            text: Full text
            position: Position of skill mention
            skill: Skill name

        Returns:
            Context window string
        """
        start = max(0, position - self.context_window)
        end = min(len(text), position + len(skill) + self.context_window)

        context = text[start:end]
        return context.strip()

    def _detect_proficiency_signals(self, skill: str, context: str, position: int) -> List[SkillContextSignal]:
        """
        Detect proficiency signals in context

        Args:
            skill: Skill name
            context: Context window
            position: Position in original text

        Returns:
            List of detected signals
        """
        signals = []
        context_lower = context.lower()

        # 1. Detect years of experience patterns
        years_signals = self._detect_years_patterns(skill, context, position)
        signals.extend(years_signals)

        # 2. Detect explicit level keywords
        level_signals = self._detect_level_keywords(context, position)
        signals.extend(level_signals)

        # 3. Detect strong/weak verbs
        verb_signals = self._detect_verb_signals(context, position)
        signals.extend(verb_signals)

        return signals

    def _detect_years_patterns(self, skill: str, context: str, position: int) -> List[SkillContextSignal]:
        """
        Detect years of experience patterns

        Args:
            skill: Skill name
            context: Context window
            position: Position in text

        Returns:
            List of years experience signals
        """
        signals = []
        skill_lower = skill.lower()

        # Patterns for years of experience
        patterns = [
            rf'(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience\s*)?(?:with\s*|in\s*|using\s*)?{re.escape(skill_lower)}',
            rf'{re.escape(skill_lower)}\s*(?:for\s*|over\s*)?(\d+(?:\.\d+)?)\s*(?:years?|yrs?)',
            rf'(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s*.*?{re.escape(skill_lower)}',
            rf'{re.escape(skill_lower)}.*?(\d+(?:\.\d+)?)\s*(?:years?|yrs?)',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, context.lower(), re.IGNORECASE)
            for match in matches:
                years_str = match.group(1)
                try:
                    years = float(years_str)
                    if 0.5 <= years <= 20:  # Reasonable range
                        signal = SkillContextSignal(
                            signal_type="years_experience",
                            signal_value=f"{years} years of {skill}",
                            context=context,
                            weight=self.SIGNAL_WEIGHTS["years_experience"],
                            position=position + match.start()
                        )
                        signals.append(signal)
                except ValueError:
                    continue

        return signals

    def _detect_level_keywords(self, context: str, position: int) -> List[SkillContextSignal]:
        """
        Detect explicit level keywords

        Args:
            context: Context window
            position: Position in text

        Returns:
            List of level keyword signals
        """
        signals = []
        context_lower = context.lower()

        for keyword, score in self.LEVEL_KEYWORDS.items():
            if keyword in context_lower:
                # Find the exact position of the keyword
                keyword_pos = context_lower.find(keyword)
                signal = SkillContextSignal(
                    signal_type="level_keyword",
                    signal_value=f"{keyword} level",
                    context=context,
                    weight=self.SIGNAL_WEIGHTS["level_keyword"] * (score / 100),
                    position=position + keyword_pos
                )
                signals.append(signal)

        return signals

    def _detect_verb_signals(self, context: str, position: int) -> List[SkillContextSignal]:
        """
        Detect strong/weak verb signals

        Args:
            context: Context window
            position: Position in text

        Returns:
            List of verb signals
        """
        signals = []
        context_lower = context.lower()

        # Check for strong verbs
        for verb, strength in self.STRONG_VERBS.items():
            if verb in context_lower:
                verb_pos = context_lower.find(verb)
                signal = SkillContextSignal(
                    signal_type="strong_verb",
                    signal_value=f"strong action: {verb}",
                    context=context,
                    weight=self.SIGNAL_WEIGHTS["strong_verb"] * strength,
                    position=position + verb_pos
                )
                signals.append(signal)

        # Check for weak verbs
        for verb, strength in self.WEAK_VERBS.items():
            if verb in context_lower:
                verb_pos = context_lower.find(verb)
                signal = SkillContextSignal(
                    signal_type="weak_verb",
                    signal_value=f"weak indicator: {verb}",
                    context=context,
                    weight=self.SIGNAL_WEIGHTS["weak_verb"] * strength,
                    position=position + verb_pos
                )
                signals.append(signal)

        return signals

    def _deduplicate_signals(self, signals: List[SkillContextSignal]) -> List[SkillContextSignal]:
        """
        Remove duplicate signals based on type and value

        Args:
            signals: List of signals to deduplicate

        Returns:
            Deduplicated list of signals
        """
        seen = set()
        unique_signals = []

        for signal in signals:
            # Create a unique key based on signal type and value
            key = (signal.signal_type, signal.signal_value.lower())
            if key not in seen:
                seen.add(key)
                unique_signals.append(signal)

        return unique_signals

    def _calculate_proficiency_score(self, signals: List[SkillContextSignal]) -> int:
        """
        Calculate proficiency score from detected signals

        Args:
            signals: List of detected signals

        Returns:
            Proficiency score (0-100)
        """
        if not signals:
            return 10  # Minimal score if no signals found

        total_score = 0
        max_years_bonus = 0

        for signal in signals:
            if signal.signal_type == "years_experience":
                # Extract years from signal value and give bonus
                years_match = re.search(r'(\d+(?:\.\d+)?)', signal.signal_value)
                if years_match:
                    years = float(years_match.group(1))
                    years_bonus = min(years * 15, 60)  # Max 60 points for years
                    max_years_bonus = max(max_years_bonus, years_bonus)

            elif signal.signal_type == "level_keyword":
                # Extract keyword and add its score
                for keyword, score in self.LEVEL_KEYWORDS.items():
                    if keyword in signal.signal_value.lower():
                        total_score += score * signal.weight
                        break

            elif signal.signal_type == "strong_verb":
                total_score += 60 * signal.weight  # Base score for strong verbs

            elif signal.signal_type == "weak_verb":
                total_score += signal.weight * 30  # Penalty for weak verbs

        # Add the highest years bonus found
        total_score += max_years_bonus

        # Apply base score if signals exist
        if signals:
            total_score += 20  # Base score for having signals

        # Clamp score to 0-100 range
        final_score = max(0, min(100, int(total_score)))

        return final_score

    def _score_to_level(self, score: int) -> SkillLevel:
        """
        Convert numeric score to skill level

        Args:
            score: Numeric score (0-100)

        Returns:
            Corresponding skill level
        """
        for level, (min_score, max_score) in self.LEVEL_THRESHOLDS.items():
            if min_score <= score < max_score:
                return level

        # Handle edge case for score = 100
        return SkillLevel.EXPERT

    def _extract_years_experience(self, signals: List[SkillContextSignal]) -> Optional[int]:
        """
        Extract years of experience from signals

        Args:
            signals: List of detected signals

        Returns:
            Years of experience if found
        """
        for signal in signals:
            if signal.signal_type == "years_experience":
                years_match = re.search(r'(\d+(?:\.\d+)?)', signal.signal_value)
                if years_match:
                    return int(float(years_match.group(1)))

        return None

    def _calculate_confidence(self, signals: List[SkillContextSignal], occurrences: int) -> float:
        """
        Calculate confidence level based on signal strength and quantity

        Args:
            signals: List of detected signals
            occurrences: Number of skill occurrences in text

        Returns:
            Confidence level (0-1)
        """
        if not signals:
            return 0.1

        # Base confidence from signal types
        signal_types = set(signal.signal_type for signal in signals)
        type_confidence = len(signal_types) * 0.2  # More signal types = higher confidence

        # Confidence from number of occurrences
        occurrence_confidence = min(occurrences * 0.1, 0.3)

        # Confidence from signal strength
        strength_confidence = sum(abs(signal.weight) for signal in signals) / len(signals)

        total_confidence = type_confidence + occurrence_confidence + strength_confidence

        return min(1.0, total_confidence)

    def _log_analysis_results(self, response: SkillAnalysisResponse) -> None:
        """
        Log analysis results for monitoring

        Args:
            response: Analysis response to log
        """
        logger.info(f"{LoggingConstants.SERVICE_PREFIX} 📊 Skill Analysis Results:")
        logger.info(f"{LoggingConstants.SERVICE_PREFIX} ⏱️  Processing time: {response.processing_time_seconds}s")
        logger.info(f"{LoggingConstants.SERVICE_PREFIX} 📈 Skills analyzed: {response.total_skills_analyzed}")
        logger.info(f"{LoggingConstants.SERVICE_PREFIX} 🎯 Average score: {response.average_proficiency_score}/100")

        # Log level distribution
        for level, count in response.summary.items():
            if count > 0:
                logger.info(f"{LoggingConstants.SERVICE_PREFIX} 📋 {level}: {count} skills")

        # Log top skills by score
        top_skills = sorted(response.results, key=lambda x: x.score, reverse=True)[:3]
        logger.info(f"{LoggingConstants.SERVICE_PREFIX} 🏆 Top skills:")
        for skill in top_skills:
            logger.info(f"{LoggingConstants.SERVICE_PREFIX}   - {skill.skill}: {skill.score}/100 ({skill.level})")

    @staticmethod
    def validate_analysis_input(skills: List[str], resume_text: str) -> Dict[str, any]:
        """
        Validate input for skill analysis

        Args:
            skills: List of skills to validate
            resume_text: Resume text to validate

        Returns:
            Validation result dictionary
        """
        if not skills:
            return {
                "is_valid": False,
                "error": "No skills provided for analysis",
                "suggestions": ["Provide at least one skill to analyze", "Use skill extraction module first"]
            }

        if not resume_text or not resume_text.strip():
            return {
                "is_valid": False,
                "error": "Resume text is empty",
                "suggestions": ["Provide resume text for context analysis", "Ensure text extraction was successful"]
            }

        if len(resume_text.strip()) < 100:
            return {
                "is_valid": False,
                "error": "Resume text too short for meaningful analysis",
                "suggestions": ["Ensure complete resume text is provided", "Minimum 100 characters required"]
            }

        return {
            "is_valid": True,
            "skills_count": len(skills),
            "text_length": len(resume_text)
        }

    @staticmethod
    def get_supported_proficiency_signals() -> Dict[str, any]:
        """
        Get information about supported proficiency signals

        Returns:
            Dictionary of supported signal types and examples
        """
        return {
            "signal_types": {
                "years_experience": {
                    "description": "Years of experience with the skill",
                    "examples": ["3 years of Python", "Java for 5 years", "React experience 2+ years"],
                    "weight": SkillIntelligenceEngine.SIGNAL_WEIGHTS["years_experience"]
                },
                "level_keywords": {
                    "description": "Explicit proficiency level indicators",
                    "examples": ["expert Python", "advanced SQL", "intermediate JavaScript"],
                    "weight": SkillIntelligenceEngine.SIGNAL_WEIGHTS["level_keyword"],
                    "keywords": list(SkillIntelligenceEngine.LEVEL_KEYWORDS.keys())
                },
                "strong_verbs": {
                    "description": "Action verbs indicating high proficiency",
                    "examples": ["developed", "architected", "led", "optimized"],
                    "weight": SkillIntelligenceEngine.SIGNAL_WEIGHTS["strong_verb"],
                    "verbs": list(SkillIntelligenceEngine.STRONG_VERBS.keys())
                },
                "weak_verbs": {
                    "description": "Indicators of lower proficiency",
                    "examples": ["learned", "familiar with", "exposed to"],
                    "weight": SkillIntelligenceEngine.SIGNAL_WEIGHTS["weak_verb"],
                    "verbs": list(SkillIntelligenceEngine.WEAK_VERBS.keys())
                }
            },
            "scoring_thresholds": {
                "Beginner": "0-30 points",
                "Intermediate": "30-60 points",
                "Expert": "60-100 points"
            }
        }
