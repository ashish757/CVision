import asyncio
import random
import time
import os
import logging
from typing import List
from app.models.analysis import AnalyzeResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnalysisService:
    """Service for analyzing resumes with mock AI processing"""

    # Mock data pools for random generation
    SKILLS_POOL = [
        "Python", "JavaScript", "React", "Node.js", "SQL", "MongoDB",
        "Docker", "AWS", "Kubernetes", "Git", "Machine Learning", "Django",
        "FastAPI", "PostgreSQL", "Redis", "HTML/CSS", "TypeScript", "Vue.js",
        "Angular", "Java", "C++", "Pandas", "NumPy", "TensorFlow", "PyTorch",
        "REST APIs", "GraphQL", "Microservices", "CI/CD", "Linux", "Terraform"
    ]

    EDUCATION_LEVELS = [
        "B.Tech Computer Science",
        "B.E. Information Technology",
        "M.Tech Software Engineering",
        "BCA",
        "MCA",
        "B.Sc Computer Science",
        "M.Sc Data Science",
        "MBA Technology Management",
        "Diploma in Computer Science"
    ]

    @staticmethod
    async def analyze_resume(file_path: str) -> AnalyzeResponse:
        """
        Simulate AI resume analysis with mock processing

        Args:
            file_path: Path to the resume file

        Returns:
            AnalyzeResponse: Mock analysis results
        """
        start_time = time.time()

        # Log file details
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0

        logger.info(f"Starting analysis for file: {file_name}")
        logger.info(f"File size: {file_size} bytes")

        try:
            # Simulate heavy AI processing with async delay
            processing_delay = random.uniform(2.0, 3.5)
            await asyncio.sleep(processing_delay)

            # Generate mock analysis data
            mock_data = AnalysisService._generate_mock_analysis()

            # Calculate actual processing time
            processing_time = time.time() - start_time
            mock_data.processing_time_seconds = round(processing_time, 2)

            logger.info(f"Analysis completed for {file_name}")
            logger.info(f"Processing time: {processing_time:.2f} seconds")
            logger.info(f"Generated score: {mock_data.score}")

            return mock_data

        except Exception as e:
            logger.error(f"Error during analysis of {file_name}: {str(e)}")
            raise

    @staticmethod
    def _generate_mock_analysis() -> AnalyzeResponse:
        """
        Generate random mock analysis data

        Returns:
            AnalyzeResponse: Randomly generated analysis data
        """
        # Random number of skills (3-8)
        num_skills = random.randint(3, 8)
        skills = random.sample(AnalysisService.SKILLS_POOL, num_skills)

        # Random experience years (0-15)
        experience_years = random.randint(0, 15)

        # Random education
        education = random.choice(AnalysisService.EDUCATION_LEVELS)

        # Generate score based on experience and skills (with some randomness)
        base_score = min(experience_years * 5 + len(skills) * 3, 85)
        random_factor = random.randint(-10, 15)
        score = max(10, min(100, base_score + random_factor))

        return AnalyzeResponse(
            skills=skills,
            experience_years=experience_years,
            education=education,
            score=score,
            processing_time_seconds=0.0  # Will be updated in analyze_resume
        )

    @staticmethod
    def validate_file_type(file_path: str) -> bool:
        """
        Validate if the file type is supported

        Args:
            file_path: Path to the file

        Returns:
            bool: True if file type is supported
        """
        allowed_extensions = ['.pdf', '.docx']
        file_extension = os.path.splitext(file_path)[1].lower()
        return file_extension in allowed_extensions

    @staticmethod
    def get_file_size_mb(file_path: str) -> float:
        """
        Get file size in MB

        Args:
            file_path: Path to the file

        Returns:
            float: File size in MB
        """
        if not os.path.exists(file_path):
            return 0.0

        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        return round(size_mb, 2)
