import re
from typing import Dict, List
from collections import defaultdict

# Import spaCy with fallback handling
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    spacy = None
    SPACY_AVAILABLE = False

# Import core components with fallback
try:
    from app.core import get_logger, LoggingConstants
    logger = get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

    # Fallback constants
    class LoggingConstants:
        SERVICE_PREFIX = "[ENTITY_SERVICE]"
        SUCCESS_INDICATOR = "Success"
        ERROR_INDICATOR = "Error"


class EntityExtractionService:
    """Service for extracting structured entities from resume sections"""

    # Predefined skill list for dictionary-based matching
    TECHNICAL_SKILLS = {
        # Programming Languages
        "python", "java", "javascript", "typescript", "c++", "c#", "php", "ruby", "go", "rust",
        "swift", "kotlin", "scala", "r", "matlab", "perl", "shell", "bash", "powershell",

        # Web Technologies
        "html", "css", "react", "angular", "vue", "node.js", "express", "django", "flask",
        "spring", "laravel", "rails", "asp.net", "blazor", "next.js", "nuxt.js",

        # Databases
        "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "cassandra",
        "dynamodb", "oracle", "sqlite", "mariadb", "neo4j",

        # Cloud & DevOps
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git", "github", "gitlab",
        "terraform", "ansible", "chef", "puppet", "vagrant", "ci/cd",

        # Data Science & AI
        "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
        "pandas", "numpy", "spark", "hadoop", "kafka", "airflow",

        # Tools & Frameworks
        "jira", "confluence", "slack", "linux", "windows", "macos", "vim", "vscode",
        "intellij", "eclipse", "postman", "swagger", "graphql", "rest api"
    }

    # Common degree patterns
    DEGREE_PATTERNS = [
        r'\b(Bachelor|B\.?\s*(Tech|Sc|A|E|S|Com))\b',
        r'\b(Master|M\.?\s*(Tech|Sc|A|E|S|Com|BA))\b',
        r'\b(Ph\.?D|PhD|Doctorate)\b',
        r'\b(MBA|MCA|BCA)\b',
        r'\b(Diploma)\b',
        r'\b(Associate|A\.S)\b'
    ]

    def __init__(self):
        """Initialize the entity extraction service with spaCy model"""
        self._nlp_model = None
        self._load_nlp_model()

    def _load_nlp_model(self):
        """Load spaCy NLP model with error handling"""
        if not SPACY_AVAILABLE:
            logger.warning(f"{LoggingConstants.SERVICE_PREFIX} spaCy not available. Install with: pip install spacy && python -m spacy download en_core_web_sm")
            self._nlp_model = None
            return

        try:
            self._nlp_model = spacy.load("en_core_web_sm")
            logger.info(f"{LoggingConstants.SERVICE_PREFIX} spaCy model 'en_core_web_sm' loaded successfully")
        except OSError:
            logger.warning(f"{LoggingConstants.SERVICE_PREFIX} spaCy model 'en_core_web_sm' not found. Install with: python -m spacy download en_core_web_sm")
            self._nlp_model = None
        except Exception as e:
            logger.error(f"{LoggingConstants.SERVICE_PREFIX} Failed to load spaCy model: {e}")
            self._nlp_model = None

    def extract_entities(self, sections: Dict[str, str]) -> Dict[str, any]:
        """
        Extract structured entities from resume sections

        Args:
            sections: Dictionary containing resume sections (summary, skills, experience, etc.)

        Returns:
            Dictionary containing extracted entities
        """
        logger.info("=" * 60)
        logger.info(f"{LoggingConstants.SERVICE_PREFIX} Starting entity extraction")
        logger.info(f"{LoggingConstants.SERVICE_PREFIX} Input sections: {list(sections.keys())}")

        try:
            # Initialize result structure
            entities = {
                "name": "",
                "email": "",
                "phone": "",
                "skills": [],
                "companies": [],
                "job_titles": [],
                "education_degrees": [],
                "dates": []
            }

            # Combine all text for contact information extraction
            all_text = " ".join([section for section in sections.values() if section])

            # Extract contact information
            entities.update(self._extract_contact_info(all_text))

            # Extract name from summary/top section
            entities["name"] = self._extract_name(sections)

            # Extract skills from skills section
            entities["skills"] = self._extract_skills(sections.get("skills", ""))

            # Extract experience entities
            experience_entities = self._extract_experience_entities(sections.get("experience", ""))
            entities["companies"] = experience_entities["companies"]
            entities["job_titles"] = experience_entities["job_titles"]
            entities["dates"].extend(experience_entities["dates"])

            # Extract education entities
            education_entities = self._extract_education_entities(sections.get("education", ""))
            entities["education_degrees"] = education_entities["degrees"]
            entities["dates"].extend(education_entities["dates"])

            # Deduplicate and normalize
            entities = self._normalize_entities(entities)

            # Log results
            self._log_extraction_results(entities)

            logger.info("=" * 60)
            return entities

        except Exception as e:
            logger.error(f"{LoggingConstants.SERVICE_PREFIX} {LoggingConstants.ERROR_INDICATOR} Entity extraction failed: {str(e)}")
            logger.error("=" * 60)
            raise

    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract email and phone number using regex"""
        contact_info = {"email": "", "phone": ""}

        if not text:
            return contact_info

        # Email regex pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_matches = re.findall(email_pattern, text)
        if email_matches:
            contact_info["email"] = email_matches[0]  # Take first email found
            logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Email extracted: {contact_info['email']}")

        # Phone regex patterns (various formats)
        phone_patterns = [
            r'\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',  # US format
            r'\+?([0-9]{1,3})[-.\s]?([0-9]{3,4})[-.\s]?([0-9]{3,4})[-.\s]?([0-9]{3,4})',  # International
            r'\b([0-9]{10})\b'  # 10 digit number
        ]

        for pattern in phone_patterns:
            phone_matches = re.findall(pattern, text)
            if phone_matches:
                if isinstance(phone_matches[0], tuple):
                    contact_info["phone"] = "-".join(phone_matches[0])
                else:
                    contact_info["phone"] = phone_matches[0]
                logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Phone extracted: {contact_info['phone']}")
                break

        return contact_info

    def _extract_name(self, sections: Dict[str, str]) -> str:
        """Extract person name using spaCy NER from top sections"""
        if not self._nlp_model:
            logger.warning(f"{LoggingConstants.SERVICE_PREFIX} spaCy model not available for name extraction")
            return ""

        # Try to extract name from summary first, then other sections
        text_sources = [
            sections.get("summary", ""),
            sections.get("other", ""),
            " ".join([section for section in sections.values() if section])[:200]  # First 200 chars
        ]

        for text in text_sources:
            if not text.strip():
                continue

            doc = self._nlp_model(text[:500])  # Process first 500 chars for efficiency

            # Look for PERSON entities
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    name = ent.text.strip()
                    # Filter out common false positives
                    if len(name) > 2 and not any(word.lower() in name.lower() for word in
                                               ["resume", "cv", "profile", "engineer", "developer", "manager"]):
                        logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Name extracted: {name}")
                        return name

        return ""

    def _extract_skills(self, skills_text: str) -> List[str]:
        """Extract skills using dictionary-based matching"""
        if not skills_text:
            return []

        extracted_skills = set()
        skills_lower = skills_text.lower()

        # Match against predefined skill list
        for skill in self.TECHNICAL_SKILLS:
            if skill.lower() in skills_lower:
                # Use word boundary matching for better accuracy
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, skills_lower):
                    extracted_skills.add(skill.title())

        # Also extract skills mentioned with common separators
        skill_separators = [',', '•', '▪', '-', '|', '\n', ';']
        for separator in skill_separators:
            if separator in skills_text:
                potential_skills = [s.strip() for s in skills_text.split(separator)]
                for skill in potential_skills:
                    skill_clean = re.sub(r'[^\w\s+#.]', '', skill).strip()
                    if 2 <= len(skill_clean) <= 30 and skill_clean.lower() in [s.lower() for s in self.TECHNICAL_SKILLS]:
                        extracted_skills.add(skill_clean.title())

        result = list(extracted_skills)
        logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Skills extracted: {len(result)} skills")
        return result

    def _extract_experience_entities(self, experience_text: str) -> Dict[str, List[str]]:
        """Extract companies, job titles, and dates from experience section"""
        entities = {"companies": [], "job_titles": [], "dates": []}

        if not experience_text or not self._nlp_model:
            return entities

        doc = self._nlp_model(experience_text)

        companies = set()
        dates = set()

        # Extract organizations and dates using NER
        for ent in doc.ents:
            if ent.label_ == "ORG":
                company = ent.text.strip()
                if len(company) > 1 and not any(word.lower() in company.lower() for word in
                                               ["university", "college", "school", "institute"]):
                    companies.add(company)
            elif ent.label_ == "DATE":
                date = ent.text.strip()
                if len(date) > 2:
                    dates.add(date)

        # Extract job titles using common patterns
        job_title_patterns = [
            r'(Senior|Junior|Lead|Principal|Chief)?\s*(Software|Web|Data|System)?\s*(Engineer|Developer|Programmer|Analyst|Manager|Director|Architect)',
            r'(Full\s*Stack|Front\s*End|Back\s*End|DevOps)\s*(Engineer|Developer)',
            r'(Product|Project|Technical|Engineering)\s*Manager',
            r'(CTO|CEO|VP|Director)',
        ]

        job_titles = set()
        for pattern in job_title_patterns:
            matches = re.findall(pattern, experience_text, re.IGNORECASE)
            for match in matches:
                title = " ".join([part for part in match if part]).strip()
                if title:
                    job_titles.add(title)

        entities["companies"] = list(companies)
        entities["job_titles"] = list(job_titles)
        entities["dates"] = list(dates)

        logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Experience entities - Companies: {len(companies)}, Job titles: {len(job_titles)}, Dates: {len(dates)}")

        return entities

    def _extract_education_entities(self, education_text: str) -> Dict[str, List[str]]:
        """Extract degrees and dates from education section"""
        entities = {"degrees": [], "dates": []}

        if not education_text:
            return entities

        degrees = set()

        # Extract degrees using regex patterns
        for pattern in self.DEGREE_PATTERNS:
            matches = re.findall(pattern, education_text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    degree = " ".join([part for part in match if part]).strip()
                else:
                    degree = match.strip()
                if degree:
                    degrees.add(degree)

        # Extract dates if spaCy model is available
        dates = set()
        if self._nlp_model:
            doc = self._nlp_model(education_text)
            for ent in doc.ents:
                if ent.label_ == "DATE":
                    date = ent.text.strip()
                    if len(date) > 2:
                        dates.add(date)

        entities["degrees"] = list(degrees)
        entities["dates"] = list(dates)

        logger.debug(f"{LoggingConstants.SERVICE_PREFIX} Education entities - Degrees: {len(degrees)}, Dates: {len(dates)}")

        return entities

    def _normalize_entities(self, entities: Dict[str, any]) -> Dict[str, any]:
        """Deduplicate and normalize extracted entities"""

        # Deduplicate lists while preserving order
        for key in ["skills", "companies", "job_titles", "education_degrees", "dates"]:
            if isinstance(entities[key], list):
                seen = set()
                normalized = []
                for item in entities[key]:
                    item_lower = item.lower()
                    if item_lower not in seen:
                        seen.add(item_lower)
                        normalized.append(item.strip())
                entities[key] = normalized

        # Normalize contact information
        if entities["email"]:
            entities["email"] = entities["email"].lower().strip()

        if entities["name"]:
            entities["name"] = entities["name"].strip()

        if entities["phone"]:
            # Normalize phone format
            phone_digits = re.sub(r'[^\d]', '', entities["phone"])
            if len(phone_digits) == 10:
                entities["phone"] = f"({phone_digits[:3]}) {phone_digits[3:6]}-{phone_digits[6:]}"
            elif len(phone_digits) == 11 and phone_digits[0] == '1':
                entities["phone"] = f"+1 ({phone_digits[1:4]}) {phone_digits[4:7]}-{phone_digits[7:]}"
            # Keep original if normalization fails

        return entities

    def _log_extraction_results(self, entities: Dict[str, any]) -> None:
        """Log the entity extraction results for monitoring"""
        logger.info(f"{LoggingConstants.SERVICE_PREFIX} 📊 Entity Extraction Results:")

        # Count total entities
        total_entities = 0
        for key, value in entities.items():
            if isinstance(value, list):
                count = len(value)
                total_entities += count
                logger.info(f"{LoggingConstants.SERVICE_PREFIX}   {key}: {count} items")
            else:
                if value:
                    total_entities += 1
                    preview = value[:50] + "..." if len(value) > 50 else value
                    logger.info(f"{LoggingConstants.SERVICE_PREFIX}   {key}: '{preview}'")
                else:
                    logger.info(f"{LoggingConstants.SERVICE_PREFIX}   {key}: empty")

        logger.info(f"{LoggingConstants.SERVICE_PREFIX} 📈 Total entities extracted: {total_entities}")

        # Log entity type distribution
        entity_types = []
        if entities["name"]: entity_types.append("name")
        if entities["email"]: entity_types.append("email")
        if entities["phone"]: entity_types.append("phone")
        if entities["skills"]: entity_types.append("skills")
        if entities["companies"]: entity_types.append("companies")
        if entities["job_titles"]: entity_types.append("job_titles")
        if entities["education_degrees"]: entity_types.append("degrees")
        if entities["dates"]: entity_types.append("dates")

        logger.info(f"{LoggingConstants.SERVICE_PREFIX} 🎯 Entity types detected: {', '.join(entity_types)}")

    @staticmethod
    def validate_sections_for_extraction(sections: Dict[str, str]) -> Dict[str, any]:
        """
        Validate resume sections for entity extraction

        Args:
            sections: Dictionary of resume sections

        Returns:
            Validation result dictionary
        """
        if not sections or not isinstance(sections, dict):
            return {
                "is_valid": False,
                "error": "Invalid sections input - must be a dictionary",
                "suggestions": ["Ensure sections is a valid dictionary", "Use resume parsing module first"]
            }

        # Check if any sections have content
        content_sections = [key for key, value in sections.items() if value and value.strip()]
        if not content_sections:
            return {
                "is_valid": False,
                "error": "All sections are empty",
                "suggestions": ["Ensure resume sections contain text", "Check resume parsing output"]
            }

        return {
            "is_valid": True,
            "content_sections": content_sections,
            "total_text_length": sum(len(text) for text in sections.values() if text)
        }

    @staticmethod
    def get_supported_entity_types() -> Dict[str, str]:
        """
        Get list of supported entity types and their descriptions

        Returns:
            Dictionary mapping entity types to descriptions
        """
        return {
            "name": "Person's full name extracted using NER",
            "email": "Email address extracted using regex patterns",
            "phone": "Phone number extracted using regex patterns",
            "skills": "Technical skills extracted using dictionary matching",
            "companies": "Company names from experience section using NER",
            "job_titles": "Job titles extracted using pattern matching",
            "education_degrees": "Academic degrees extracted using keyword matching",
            "dates": "Date entities from experience and education sections"
        }
