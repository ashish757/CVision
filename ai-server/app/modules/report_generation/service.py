"""
Evaluation Report Generation Service for CVision AI Analysis System

This service converts resume scores and analysis outputs into structured,
human-readable evaluation reports with actionable insights and recommendations.
"""

import logging
from typing import List, Dict, Tuple
from datetime import datetime
from .schemas import (
    EvaluationReportResponse,
    EvaluationSection,
    ScoringResultData,
    SkillEvaluation,
    ExperienceEvaluation,
    ReportTemplateConfig
)
from app.core import LoggingConstants

# Get logger for this module
logger = logging.getLogger(__name__)


class EvaluationReportGenerator:
    """Service for generating comprehensive evaluation reports"""

    # Critical skills that are highly valued in tech industry
    CRITICAL_SKILLS = {
        # Programming Languages
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "kotlin", "swift",

        # Cloud & DevOps
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "jenkins", "terraform", "ansible",

        # Data & AI
        "sql", "machine learning", "data science", "tensorflow", "pytorch", "spark", "hadoop",

        # Web Technologies
        "react", "angular", "vue", "node.js", "spring", "django", "flask", "express",

        # Databases
        "postgresql", "mongodb", "redis", "elasticsearch", "mysql", "cassandra",

        # Methodologies
        "agile", "scrum", "devops", "microservices", "rest api", "graphql"
    }

    # Leadership and management indicators
    LEADERSHIP_KEYWORDS = [
        "led", "managed", "directed", "supervised", "coordinated", "mentored",
        "guided", "facilitated", "orchestrated", "spearheaded", "headed"
    ]

    # Achievement quality indicators
    ACHIEVEMENT_INDICATORS = [
        "%", "percent", "million", "thousand", "revenue", "cost", "efficiency",
        "performance", "growth", "reduction", "improvement", "increase", "save"
    ]

    @staticmethod
    def generate_evaluation_report(
        scoring_result: ScoringResultData,
        skill_analysis: List[SkillEvaluation],
        experience_analysis: ExperienceEvaluation,
        config: ReportTemplateConfig = None
    ) -> EvaluationReportResponse:
        """
        Generate comprehensive evaluation report

        Args:
            scoring_result: Global scoring results
            skill_analysis: Individual skill analysis results
            experience_analysis: Experience analysis results
            config: Report configuration settings

        Returns:
            EvaluationReportResponse with comprehensive evaluation
        """
        try:
            if config is None:
                config = ReportTemplateConfig()

            logger.info(f"{LoggingConstants.SERVICE_PREFIX} Starting evaluation report generation")
            logger.info(f"{LoggingConstants.SERVICE_PREFIX} Overall score: {scoring_result.overall_score}/100")

            # Generate summary statement and profile tier
            summary_statement, profile_tier = EvaluationReportGenerator._generate_summary_statement(
                scoring_result.overall_score, config
            )

            # Identify strengths
            strengths = EvaluationReportGenerator._identify_strengths(
                scoring_result, skill_analysis, experience_analysis, config
            )

            # Identify weaknesses
            weaknesses = EvaluationReportGenerator._identify_weaknesses(
                scoring_result, skill_analysis, experience_analysis, config
            )

            # Generate recommendations
            recommendations = EvaluationReportGenerator._generate_recommendations(
                scoring_result, skill_analysis, experience_analysis, config
            )

            # Create detailed evaluation sections
            skills_evaluation = EvaluationReportGenerator._create_skills_evaluation(
                skill_analysis, scoring_result.skills_score, config
            )

            experience_evaluation = EvaluationReportGenerator._create_experience_evaluation(
                experience_analysis, scoring_result.experience_score, config
            )

            structure_evaluation = EvaluationReportGenerator._create_structure_evaluation(
                scoring_result.missing_sections, scoring_result.structure_score, config
            )

            # Generate next steps
            next_steps = EvaluationReportGenerator._generate_next_steps(
                scoring_result, weaknesses, recommendations
            )

            # Create evaluation criteria summary
            evaluation_criteria = {
                "skills_weight": "35%",
                "experience_weight": "40%",
                "achievement_weight": "15%",
                "structure_weight": "10%",
                "evaluation_date": datetime.now().strftime("%Y-%m-%d"),
                "scoring_methodology": "Rule-based multi-component analysis"
            }

            logger.info(f"{LoggingConstants.SERVICE_PREFIX} Report generation completed")
            logger.info(f"{LoggingConstants.SERVICE_PREFIX} Profile tier: {profile_tier}")
            logger.info(f"{LoggingConstants.SERVICE_PREFIX} Strengths: {len(strengths)}, Weaknesses: {len(weaknesses)}, Recommendations: {len(recommendations)}")

            return EvaluationReportResponse(
                overall_score=scoring_result.overall_score,
                summary_statement=summary_statement,
                profile_tier=profile_tier,
                strengths=strengths,
                weaknesses=weaknesses,
                recommendations=recommendations,
                skills_evaluation=skills_evaluation,
                experience_evaluation=experience_evaluation,
                structure_evaluation=structure_evaluation,
                evaluation_criteria=evaluation_criteria,
                next_steps=next_steps
            )

        except Exception as e:
            logger.error(f"{LoggingConstants.SERVICE_PREFIX} Error in report generation: {str(e)}")
            # Return minimal report on error
            return EvaluationReportResponse(
                overall_score=0,
                summary_statement="Unable to generate evaluation report due to processing error.",
                profile_tier="Incomplete",
                strengths=["Resume submitted for evaluation"],
                weaknesses=["Unable to complete analysis"],
                recommendations=["Please resubmit resume for evaluation"],
                skills_evaluation=EvaluationSection(title="Skills Analysis", content=["Analysis unavailable"]),
                experience_evaluation=EvaluationSection(title="Experience Analysis", content=["Analysis unavailable"]),
                structure_evaluation=EvaluationSection(title="Structure Analysis", content=["Analysis unavailable"]),
                next_steps=["Resubmit resume for complete evaluation"]
            )

    @staticmethod
    def _generate_summary_statement(overall_score: int, config: ReportTemplateConfig) -> Tuple[str, str]:
        """Generate executive summary statement and profile tier"""

        if overall_score >= config.high_score_threshold:
            profile_tier = "Strong Profile"
            summary = (
                f"This is a strong professional profile with an overall score of {overall_score}/100. "
                "The candidate demonstrates excellent qualifications with well-developed skills, "
                "substantial experience, and clear evidence of professional achievements. "
                "This profile would be competitive for senior-level positions."
            )
        elif overall_score >= config.moderate_score_threshold:
            profile_tier = "Moderate Profile"
            summary = (
                f"This is a moderate professional profile with an overall score of {overall_score}/100. "
                "The candidate shows solid foundational skills and relevant experience, though "
                "there are opportunities for enhancement in certain areas. With targeted improvements, "
                "this profile could become highly competitive."
            )
        else:
            profile_tier = "Developing Profile"
            summary = (
                f"This is a developing professional profile with an overall score of {overall_score}/100. "
                "While the candidate shows potential, significant improvements are needed to enhance "
                "competitiveness. Focus on skill development, experience building, and resume optimization "
                "would strengthen this profile considerably."
            )

        logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Summary generated - Tier: {profile_tier}, Score: {overall_score}")

        return summary, profile_tier

    @staticmethod
    def _identify_strengths(
        scoring_result: ScoringResultData,
        skill_analysis: List[SkillEvaluation],
        experience_analysis: ExperienceEvaluation,
        config: ReportTemplateConfig
    ) -> List[str]:
        """Identify key strengths from analysis results"""

        strengths = []

        # High proficiency skills
        high_skills = [skill for skill in skill_analysis if skill.score > config.high_skill_threshold]
        if high_skills:
            critical_high_skills = [skill for skill in high_skills if skill.skill.lower() in EvaluationReportGenerator.CRITICAL_SKILLS]
            if critical_high_skills:
                strengths.append(
                    f"Strong proficiency in critical technical skills: {', '.join([s.skill for s in critical_high_skills[:4]])}"
                )
            if len(high_skills) >= 5:
                strengths.append(f"Diverse technical skill portfolio with {len(high_skills)} high-proficiency skills")

        # Experience strengths
        if experience_analysis.experience_strength_score >= config.experience_strength_threshold:
            if experience_analysis.total_experience_years >= 5:
                strengths.append(f"Substantial professional experience ({experience_analysis.total_experience_years} years)")
            if experience_analysis.seniority_level in ["Senior", "Executive"]:
                strengths.append(f"{experience_analysis.seniority_level}-level professional background")

        # Achievement strengths
        if experience_analysis.achievement_score >= config.strong_achievement_threshold:
            strengths.append("Strong track record of quantified professional achievements")
            if len(experience_analysis.quantified_achievements) >= 3:
                strengths.append("Multiple measurable accomplishments demonstrating impact")

        # Leadership indicators
        if experience_analysis.strong_verbs_count > experience_analysis.weak_verbs_count * 2:
            strengths.append("Strong leadership and action-oriented language throughout experience")

        # Structure strengths
        if scoring_result.structure_score >= 90:
            strengths.append("Well-organized resume structure with comprehensive sections")

        # Component score strengths
        if scoring_result.skills_score >= 85:
            strengths.append("Exceptional technical skills evaluation")
        if scoring_result.experience_score >= 85:
            strengths.append("Outstanding professional experience quality")

        # Ensure we have meaningful strengths
        if not strengths:
            if skill_analysis:
                strengths.append(f"Technical skills portfolio including {', '.join([s.skill for s in skill_analysis[:3]])}")
            if experience_analysis.total_experience_years > 0:
                strengths.append(f"Professional experience in the field ({experience_analysis.total_experience_years} years)")
            if not strengths:
                strengths.append("Resume submitted for professional evaluation")

        logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Identified {len(strengths)} strengths")

        return strengths[:6]  # Limit to top 6 strengths

    @staticmethod
    def _identify_weaknesses(
        scoring_result: ScoringResultData,
        skill_analysis: List[SkillEvaluation],
        experience_analysis: ExperienceEvaluation,
        config: ReportTemplateConfig
    ) -> List[str]:
        """Identify areas needing improvement"""

        weaknesses = []

        # Low proficiency skills
        low_skills = [skill for skill in skill_analysis if skill.score <= config.low_skill_threshold]
        if low_skills:
            weaknesses.append(
                f"Limited proficiency in key skills: {', '.join([s.skill for s in low_skills[:3]])}"
            )

        # Limited skill diversity
        if len(skill_analysis) < 5:
            weaknesses.append("Limited technical skills diversity - consider expanding skill set")

        # Experience weaknesses
        if experience_analysis.experience_strength_score < config.experience_strength_threshold:
            weaknesses.append("Professional experience could benefit from stronger impact statements")

        if experience_analysis.total_experience_years < 2:
            weaknesses.append("Limited professional experience - focus on skill development and practice projects")

        # Achievement weaknesses
        if experience_analysis.achievement_score < 50:
            weaknesses.append("Lack of quantified achievements and measurable results")

        if len(experience_analysis.quantified_achievements) == 0:
            weaknesses.append("Missing specific metrics and quantified accomplishments")

        # Language weaknesses
        if experience_analysis.weak_verbs_count > experience_analysis.strong_verbs_count:
            weaknesses.append("Passive language - replace weak action verbs with stronger, more impactful terms")

        # Structure weaknesses
        if scoring_result.missing_sections:
            weaknesses.append(f"Missing important resume sections: {', '.join(scoring_result.missing_sections)}")

        if scoring_result.structure_score < 70:
            weaknesses.append("Resume structure and organization could be improved")

        # Component score weaknesses
        if scoring_result.skills_score < 60:
            weaknesses.append("Technical skills evaluation indicates need for skill development")
        if scoring_result.experience_score < 60:
            weaknesses.append("Professional experience section needs strengthening")
        if scoring_result.achievement_score < 40:
            weaknesses.append("Limited demonstration of professional impact and achievements")

        # Seniority vs achievement mismatch
        if (experience_analysis.seniority_level in ["Senior", "Executive"] and
            experience_analysis.achievement_score < 70):
            weaknesses.append("Senior-level role should demonstrate stronger quantified achievements")

        # Ensure we have meaningful weaknesses if score is low
        if not weaknesses and scoring_result.overall_score < config.moderate_score_threshold:
            weaknesses.append("Overall profile needs strengthening across multiple areas")

        # Always provide at least one area for improvement unless it's an exceptional profile
        if not weaknesses and scoring_result.overall_score < 95:
            weaknesses.append("Continue building expertise and documenting achievements for career growth")

        logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Identified {len(weaknesses)} weaknesses")

        return weaknesses[:5]  # Limit to top 5 weaknesses

    @staticmethod
    def _generate_recommendations(
        scoring_result: ScoringResultData,
        skill_analysis: List[SkillEvaluation],
        experience_analysis: ExperienceEvaluation,
        config: ReportTemplateConfig
    ) -> List[str]:
        """Generate actionable recommendations"""

        recommendations = []

        # Skills recommendations
        low_skills = [skill for skill in skill_analysis if skill.score <= config.low_skill_threshold]
        if low_skills:
            recommendations.append(
                f"Enhance proficiency in {', '.join([s.skill for s in low_skills[:2]])} through courses or hands-on projects"
            )

        critical_skills_missing = []
        for critical_skill in list(EvaluationReportGenerator.CRITICAL_SKILLS)[:10]:  # Check top 10 critical skills
            if not any(skill.skill.lower() == critical_skill for skill in skill_analysis):
                critical_skills_missing.append(critical_skill)

        if critical_skills_missing and len(skill_analysis) < 8:
            recommendations.append(
                f"Consider adding in-demand skills like {', '.join(critical_skills_missing[:2])} to strengthen technical profile"
            )

        # Experience recommendations
        if experience_analysis.achievement_score < config.strong_achievement_threshold:
            recommendations.append(
                "Add specific metrics and quantified results to experience descriptions (e.g., '% improvement', '$ saved', 'users served')"
            )

        if experience_analysis.weak_verbs_count > experience_analysis.strong_verbs_count:
            recommendations.append(
                "Replace passive language with strong action verbs like 'led', 'implemented', 'optimized', 'designed'"
            )

        if (experience_analysis.seniority_level in ["Entry", "Junior"] and
            experience_analysis.total_experience_years >= 2):
            recommendations.append(
                "Highlight leadership opportunities and initiatives to demonstrate career progression"
            )

        # Structure recommendations
        if scoring_result.missing_sections:
            essential_missing = [section for section in scoring_result.missing_sections if section in ["summary", "skills", "experience"]]
            if essential_missing:
                recommendations.append(f"Add essential resume sections: {', '.join(essential_missing)}")

        if scoring_result.structure_score < 80:
            recommendations.append(
                "Improve resume organization with clear section headings and consistent formatting"
            )

        # Career development recommendations
        if experience_analysis.total_experience_years < 3:
            recommendations.append(
                "Build experience through internships, freelance projects, or open-source contributions"
            )

        if (scoring_result.overall_score >= config.high_score_threshold and
            experience_analysis.seniority_level != "Executive"):
            recommendations.append(
                "Consider pursuing leadership roles or certifications to advance to the next career level"
            )

        # Portfolio recommendations
        if len(skill_analysis) >= 8 and experience_analysis.achievement_score >= 70:
            recommendations.append(
                "Create a portfolio or GitHub profile to showcase practical application of your technical skills"
            )

        # Ensure we have actionable recommendations
        if not recommendations:
            if scoring_result.overall_score < config.moderate_score_threshold:
                recommendations.append("Focus on skill development and gaining relevant professional experience")
            else:
                recommendations.append("Continue documenting achievements and expanding technical expertise")

        logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Generated {len(recommendations)} recommendations")

        return recommendations[:6]  # Limit to top 6 recommendations

    @staticmethod
    def _create_skills_evaluation(
        skill_analysis: List[SkillEvaluation],
        skills_score: float,
        config: ReportTemplateConfig
    ) -> EvaluationSection:
        """Create detailed skills evaluation section"""

        content = []

        if not skill_analysis:
            content.append("No technical skills identified for evaluation")
            return EvaluationSection(
                title="Skills Analysis",
                content=content,
                priority_level="high"
            )

        # Overall skills assessment
        content.append(f"Technical skills evaluation score: {skills_score:.1f}/100")
        content.append(f"Total skills identified: {len(skill_analysis)}")

        # Categorize skills by proficiency
        expert_skills = [s for s in skill_analysis if s.level == "Expert" or s.score >= 80]
        advanced_skills = [s for s in skill_analysis if s.level == "Advanced" or (60 <= s.score < 80)]
        beginner_skills = [s for s in skill_analysis if s.level == "Beginner" or s.score < 60]

        if expert_skills:
            content.append(f"Expert-level skills ({len(expert_skills)}): {', '.join([s.skill for s in expert_skills[:5]])}")

        if advanced_skills:
            content.append(f"Advanced skills ({len(advanced_skills)}): {', '.join([s.skill for s in advanced_skills[:5]])}")

        if beginner_skills:
            content.append(f"Developing skills ({len(beginner_skills)}): {', '.join([s.skill for s in beginner_skills[:3]])}")

        # Critical skills analysis
        critical_skills = [s for s in skill_analysis if s.skill.lower() in EvaluationReportGenerator.CRITICAL_SKILLS]
        if critical_skills:
            content.append(f"High-demand industry skills: {', '.join([s.skill for s in critical_skills])}")

        return EvaluationSection(
            title="Skills Analysis",
            content=content,
            priority_level="high"
        )

    @staticmethod
    def _create_experience_evaluation(
        experience_analysis: ExperienceEvaluation,
        experience_score: float,
        config: ReportTemplateConfig
    ) -> EvaluationSection:
        """Create detailed experience evaluation section"""

        content = []

        # Overall experience assessment
        content.append(f"Professional experience score: {experience_score:.1f}/100")
        content.append(f"Total experience: {experience_analysis.total_experience_years} years")
        content.append(f"Seniority level: {experience_analysis.seniority_level}")

        # Achievement analysis
        if experience_analysis.achievement_score >= config.strong_achievement_threshold:
            content.append(f"Strong achievement record (score: {experience_analysis.achievement_score}/100)")
        elif experience_analysis.achievement_score >= 50:
            content.append(f"Moderate achievement documentation (score: {experience_analysis.achievement_score}/100)")
        else:
            content.append(f"Limited quantified achievements (score: {experience_analysis.achievement_score}/100)")

        # Language analysis
        if experience_analysis.strong_verbs_count > 0 or experience_analysis.weak_verbs_count > 0:
            total_verbs = experience_analysis.strong_verbs_count + experience_analysis.weak_verbs_count
            strong_ratio = experience_analysis.strong_verbs_count / total_verbs if total_verbs > 0 else 0

            if strong_ratio > 0.6:
                content.append(f"Strong action-oriented language ({experience_analysis.strong_verbs_count} strong verbs)")
            else:
                content.append(f"Opportunity to improve action verb usage (ratio: {strong_ratio:.1%})")

        # Experience quality indicators
        if experience_analysis.total_experience_years >= 5 and experience_analysis.seniority_level in ["Senior", "Executive"]:
            content.append("Career progression aligns with experience level")
        elif experience_analysis.total_experience_years >= 3 and experience_analysis.seniority_level in ["Entry", "Junior"]:
            content.append("Opportunity for career advancement based on experience")

        return EvaluationSection(
            title="Experience Analysis",
            content=content,
            priority_level="high"
        )

    @staticmethod
    def _create_structure_evaluation(
        missing_sections: List[str],
        structure_score: float,
        config: ReportTemplateConfig
    ) -> EvaluationSection:
        """Create resume structure evaluation section"""

        content = []

        content.append(f"Resume structure score: {structure_score:.1f}/100")

        if not missing_sections:
            content.append("All essential resume sections are present")
        else:
            content.append(f"Missing sections: {', '.join(missing_sections)}")

        if structure_score >= 90:
            content.append("Excellent resume organization and completeness")
        elif structure_score >= 70:
            content.append("Good resume structure with minor improvements needed")
        else:
            content.append("Resume structure needs significant improvement")

        return EvaluationSection(
            title="Structure Analysis",
            content=content,
            priority_level="medium"
        )

    @staticmethod
    def _generate_next_steps(
        scoring_result: ScoringResultData,
        weaknesses: List[str],
        recommendations: List[str]
    ) -> List[str]:
        """Generate prioritized next steps"""

        next_steps = []

        # High priority steps based on score
        if scoring_result.overall_score < 60:
            next_steps.append("Focus on fundamental resume improvements and skill development")
            next_steps.append("Add quantified achievements and specific examples of impact")
        elif scoring_result.overall_score < 80:
            next_steps.append("Enhance technical skills and strengthen experience descriptions")
            next_steps.append("Improve resume structure and add missing sections")
        else:
            next_steps.append("Fine-tune resume for specific target positions")
            next_steps.append("Continue building expertise in emerging technologies")

        # Component-specific steps
        if scoring_result.skills_score < 70:
            next_steps.append("Invest in technical skill development through courses or certifications")

        if scoring_result.experience_score < 70:
            next_steps.append("Rewrite experience descriptions with stronger action verbs and metrics")

        if scoring_result.missing_sections:
            next_steps.append("Complete all essential resume sections before applying")

        return next_steps[:4]  # Limit to top 4 next steps
