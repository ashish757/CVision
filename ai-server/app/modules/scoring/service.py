"""
Global Resume Scoring Service for CVision AI Analysis System

This service combines outputs from multiple analysis modules (Skills, Experience, etc.)
into a comprehensive final resume score using configurable weighted algorithms.
"""

import logging
from typing import List, Dict, Tuple, Optional
from .schemas import (
    SkillProficiency,
    ExperienceAnalysisData,
    ResumeStructuredSections,
    ScoreBreakdown,
    ScoringWeights,
    GlobalScoringResponse
)
from app.core import LoggingConstants

# Get logger for this module
logger = logging.getLogger(__name__)


class GlobalResumeScoring:
    """Service for computing comprehensive resume scores"""

    # Critical skills that get bonus weighting
    CRITICAL_SKILLS = {
        # Programming languages
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",

        # Cloud & DevOps
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform",

        # Data & AI
        "sql", "machine learning", "data science", "tensorflow", "pytorch",

        # Web technologies
        "react", "angular", "vue", "node.js", "spring", "django",

        # Databases
        "postgresql", "mongodb", "redis", "elasticsearch"
    }

    # Essential resume sections
    ESSENTIAL_SECTIONS = ["experience", "skills"]
    IMPORTANT_SECTIONS = ["summary", "education"]
    OPTIONAL_SECTIONS = ["projects", "certifications"]

    # Recommendation tiers based on score ranges
    SCORE_TIERS = {
        (90, 100): "Excellent",
        (75, 89): "Good",
        (60, 74): "Fair",
        (0, 59): "Poor"
    }

    @staticmethod
    def compute_final_resume_score(
        skill_analysis: List[SkillProficiency],
        experience_analysis: ExperienceAnalysisData,
        structured_sections: ResumeStructuredSections,
        scoring_weights: Optional[ScoringWeights] = None
    ) -> GlobalScoringResponse:
        """
        Compute comprehensive final resume score

        Args:
            skill_analysis: List of skill proficiency results
            experience_analysis: Experience strength analysis results
            structured_sections: Dictionary of resume sections
            scoring_weights: Optional custom scoring weights

        Returns:
            GlobalScoringResponse with final score and detailed breakdown
        """
        try:
            logger.info(f"{LoggingConstants.SERVICE_PREFIX} Starting global resume scoring")

            # Use default weights if none provided
            if scoring_weights is None:
                scoring_weights = ScoringWeights()
            elif not scoring_weights.validate_weights():
                logger.warning(f"{LoggingConstants.SERVICE_PREFIX} Invalid weights provided, using defaults")
                scoring_weights = ScoringWeights()

            logger.info(f"{LoggingConstants.SERVICE_PREFIX} Using weights - Skills: {scoring_weights.skills_weight:.1%}, "
                       f"Experience: {scoring_weights.experience_weight:.1%}, "
                       f"Achievement: {scoring_weights.achievement_weight:.1%}, "
                       f"Structure: {scoring_weights.structure_weight:.1%}")

            # Compute individual component scores
            skills_score, skills_details = GlobalResumeScoring._compute_skills_score(skill_analysis)
            experience_score = GlobalResumeScoring._compute_experience_score(experience_analysis)
            achievement_score = GlobalResumeScoring._compute_achievement_score(experience_analysis)
            structure_score, structure_details = GlobalResumeScoring._compute_structure_score(structured_sections)

            logger.info(f"{LoggingConstants.SERVICE_PREFIX} Component scores - "
                       f"Skills: {skills_score:.1f}, Experience: {experience_score:.1f}, "
                       f"Achievement: {achievement_score:.1f}, Structure: {structure_score:.1f}")

            # Apply weighted formula
            overall_score = (
                skills_score * scoring_weights.skills_weight +
                experience_score * scoring_weights.experience_weight +
                achievement_score * scoring_weights.achievement_weight +
                structure_score * scoring_weights.structure_weight
            )

            # Ensure score is in 0-100 range
            overall_score = max(0, min(100, overall_score))

            # Create detailed breakdown
            score_breakdown = ScoreBreakdown(
                skills_score=round(skills_score, 1),
                experience_score=round(experience_score, 1),
                achievement_score=round(achievement_score, 1),
                structure_score=round(structure_score, 1),
                skills_count=len(skill_analysis),
                average_skill_proficiency=skills_details["average_proficiency"],
                critical_skills_bonus=skills_details["critical_bonus"],
                missing_sections=structure_details["missing_sections"],
                experience_years=experience_analysis.total_experience_years,
                seniority_level=experience_analysis.seniority_level
            )

            # Determine recommendation tier
            recommendation_tier = GlobalResumeScoring._get_recommendation_tier(overall_score)

            # Generate insights
            key_strengths, improvement_areas = GlobalResumeScoring._generate_insights(
                skills_score, experience_score, achievement_score, structure_score,
                experience_analysis, len(skill_analysis), structure_details["missing_sections"]
            )

            logger.info(f"{LoggingConstants.SERVICE_PREFIX} Global scoring completed - "
                       f"Final score: {overall_score:.1f}, Tier: {recommendation_tier}")

            return GlobalScoringResponse(
                overall_score=int(round(overall_score)),
                score_breakdown=score_breakdown,
                scoring_weights=scoring_weights,
                total_skills_analyzed=len(skill_analysis),
                recommendation_tier=recommendation_tier,
                key_strengths=key_strengths,
                improvement_areas=improvement_areas
            )

        except Exception as e:
            logger.error(f"{LoggingConstants.SERVICE_PREFIX} Error in global scoring: {str(e)}")
            # Return minimal response on error
            return GlobalScoringResponse(
                overall_score=0,
                score_breakdown=ScoreBreakdown(
                    skills_score=0.0, experience_score=0.0,
                    achievement_score=0.0, structure_score=0.0
                ),
                scoring_weights=ScoringWeights(),
                total_skills_analyzed=0,
                recommendation_tier="Poor",
                key_strengths=[],
                improvement_areas=["Unable to analyze resume due to processing error"]
            )

    @staticmethod
    def _compute_skills_score(skill_analysis: List[SkillProficiency]) -> Tuple[float, Dict]:
        """
        Compute skills component score

        Args:
            skill_analysis: List of skill proficiency results

        Returns:
            Tuple of (score, details_dict)
        """
        if not skill_analysis:
            logger.warning(f"{LoggingConstants.SERVICE_PREFIX} No skills provided for scoring")
            return 0.0, {"average_proficiency": 0.0, "critical_bonus": 0.0}

        # Calculate average proficiency
        total_score = sum(skill.score for skill in skill_analysis)
        average_proficiency = total_score / len(skill_analysis)

        # Apply critical skills bonus
        critical_skills_count = sum(
            1 for skill in skill_analysis
            if skill.skill.lower() in GlobalResumeScoring.CRITICAL_SKILLS
        )

        # Critical skills bonus: up to 10 points for having critical skills
        critical_bonus = min(critical_skills_count * 2, 10)

        # Skills diversity bonus: bonus for having many skills
        diversity_bonus = min(len(skill_analysis) * 0.5, 5)

        # Final skills score
        skills_score = min(average_proficiency + critical_bonus + diversity_bonus, 100)

        logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Skills scoring - "
                    f"Average: {average_proficiency:.1f}, Critical bonus: {critical_bonus}, "
                    f"Diversity bonus: {diversity_bonus:.1f}, Final: {skills_score:.1f}")

        return skills_score, {
            "average_proficiency": round(average_proficiency, 1),
            "critical_bonus": critical_bonus,
            "diversity_bonus": round(diversity_bonus, 1)
        }

    @staticmethod
    def _compute_experience_score(experience_analysis: ExperienceAnalysisData) -> float:
        """
        Compute experience component score

        Args:
            experience_analysis: Experience analysis results

        Returns:
            Experience score (0-100)
        """
        # Use the experience strength score directly, but apply additional factors
        base_score = experience_analysis.experience_strength_score

        # Seniority bonus
        seniority_bonuses = {
            "Intern": 0, "Entry": 2, "Junior": 4,
            "Mid": 6, "Senior": 10, "Executive": 15
        }
        seniority_bonus = seniority_bonuses.get(experience_analysis.seniority_level, 2)

        # Years of experience bonus (diminishing returns)
        years = experience_analysis.total_experience_years
        years_bonus = min(years * 1.5, 10) if years > 0 else 0

        # Action verbs quality bonus
        if experience_analysis.strong_verbs_count + experience_analysis.weak_verbs_count > 0:
            verb_quality = experience_analysis.strong_verbs_count / (
                experience_analysis.strong_verbs_count + experience_analysis.weak_verbs_count
            )
            verb_bonus = verb_quality * 5
        else:
            verb_bonus = 0

        final_score = min(base_score + seniority_bonus + years_bonus + verb_bonus, 100)

        logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Experience scoring - "
                    f"Base: {base_score}, Seniority: +{seniority_bonus}, "
                    f"Years: +{years_bonus:.1f}, Verbs: +{verb_bonus:.1f}, Final: {final_score:.1f}")

        return final_score

    @staticmethod
    def _compute_achievement_score(experience_analysis: ExperienceAnalysisData) -> float:
        """
        Compute achievement component score

        Args:
            experience_analysis: Experience analysis results

        Returns:
            Achievement score (0-100)
        """
        # Base achievement score from experience analysis
        base_achievement = experience_analysis.achievement_score

        # Bonus for senior roles with achievements (they're expected to have more)
        seniority_multipliers = {
            "Intern": 1.2, "Entry": 1.1, "Junior": 1.0,
            "Mid": 0.95, "Senior": 0.9, "Executive": 0.85
        }
        multiplier = seniority_multipliers.get(experience_analysis.seniority_level, 1.0)

        achievement_score = min(base_achievement * multiplier, 100)

        logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Achievement scoring - "
                    f"Base: {base_achievement}, Multiplier: {multiplier:.2f}, Final: {achievement_score:.1f}")

        return achievement_score

    @staticmethod
    def _compute_structure_score(structured_sections: ResumeStructuredSections) -> Tuple[float, Dict]:
        """
        Compute resume structure component score

        Args:
            structured_sections: Resume sections

        Returns:
            Tuple of (score, details_dict)
        """
        score = 0.0
        missing_sections = []

        # Convert to dict for easier processing
        sections = {
            "experience": structured_sections.experience,
            "skills": structured_sections.skills,
            "summary": structured_sections.summary,
            "education": structured_sections.education,
            "projects": structured_sections.projects,
            "certifications": structured_sections.certifications
        }

        # Check essential sections (high penalty if missing)
        for section in GlobalResumeScoring.ESSENTIAL_SECTIONS:
            if sections[section] and sections[section].strip():
                score += 40  # 40 points per essential section
            else:
                missing_sections.append(section)

        # Check important sections (medium penalty if missing)
        for section in GlobalResumeScoring.IMPORTANT_SECTIONS:
            if sections[section] and sections[section].strip():
                score += 10  # 10 points per important section
            else:
                missing_sections.append(section)

        # Check optional sections (small bonus if present)
        for section in GlobalResumeScoring.OPTIONAL_SECTIONS:
            if sections[section] and sections[section].strip():
                score += 5  # 5 points per optional section

        # Content quality bonus based on section length
        for section_name, content in sections.items():
            if content and len(content.strip()) > 100:  # Substantial content
                score += 2
            elif content and len(content.strip()) > 50:   # Moderate content
                score += 1

        # Cap at 100
        score = min(score, 100)

        logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Structure scoring - "
                    f"Score: {score:.1f}, Missing: {missing_sections}")

        return score, {"missing_sections": missing_sections}

    @staticmethod
    def _get_recommendation_tier(score: float) -> str:
        """Get recommendation tier based on score"""
        for (min_score, max_score), tier in GlobalResumeScoring.SCORE_TIERS.items():
            if min_score <= score <= max_score:
                return tier
        return "Poor"

    @staticmethod
    def _generate_insights(
        skills_score: float,
        experience_score: float,
        achievement_score: float,
        structure_score: float,
        experience_analysis: ExperienceAnalysisData,
        skills_count: int,
        missing_sections: List[str]
    ) -> Tuple[List[str], List[str]]:
        """
        Generate key strengths and improvement areas

        Returns:
            Tuple of (key_strengths, improvement_areas)
        """
        strengths = []
        improvements = []

        # Analyze strengths
        if skills_score >= 80:
            strengths.append(f"Strong technical skills portfolio ({skills_count} skills analyzed)")
        if experience_score >= 80:
            strengths.append(f"Excellent professional experience ({experience_analysis.total_experience_years} years)")
        if achievement_score >= 75:
            strengths.append("Strong track record of quantified achievements")
        if structure_score >= 90:
            strengths.append("Well-structured resume with comprehensive sections")
        if experience_analysis.seniority_level in ["Senior", "Executive"]:
            strengths.append(f"Senior-level professional experience ({experience_analysis.seniority_level})")

        # Analyze improvement areas
        if skills_score < 60:
            improvements.append("Consider expanding technical skills or highlighting existing expertise")
        if experience_score < 60:
            improvements.append("Strengthen experience descriptions with more impact-focused language")
        if achievement_score < 50:
            improvements.append("Add more quantified achievements and measurable results")
        if structure_score < 70:
            improvements.append("Improve resume structure and ensure all key sections are present")
        if missing_sections:
            improvements.append(f"Add missing sections: {', '.join(missing_sections)}")
        if experience_analysis.weak_verbs_count > experience_analysis.strong_verbs_count:
            improvements.append("Use more strong action verbs to describe accomplishments")

        # Ensure we have at least something
        if not strengths:
            strengths.append("Resume submitted for professional analysis")
        if not improvements:
            improvements.append("Continue building experience and skills")

        return strengths[:5], improvements[:5]  # Limit to 5 each
