"""
Pydantic data models for the AI-Powered Resume System.

These models provide type safety, validation, and serialization for all resume data,
ensuring consistency across different formats and AI enhancement workflows.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import HttpUrl
from pydantic import validator


class Proficiency(str, Enum):
    """Skill proficiency levels."""

    EXPERT = "expert"
    ADVANCED = "advanced"
    INTERMEDIATE = "intermediate"
    BEGINNER = "beginner"


class Impact(str, Enum):
    """Achievement impact levels."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ProjectStatus(str, Enum):
    """Project status options."""

    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"
    MAINTENANCE = "maintenance"
    ARCHIVED = "archived"


class LanguageProficiency(str, Enum):
    """Language proficiency levels."""

    NATIVE = "native"
    FLUENT = "fluent"
    CONVERSATIONAL = "conversational"
    BASIC = "basic"


class Location(BaseModel):
    """Geographic location information."""

    city: str = Field(min_length=2, description="City name")
    state: str = Field(min_length=2, description="State or province")
    country: str = Field(min_length=2, description="Country name")
    remote_friendly: bool = Field(default=True, description="Open to remote work")


class Links(BaseModel):
    """Professional and social media links."""

    linkedin: HttpUrl | None = None
    github: HttpUrl | None = None
    website: HttpUrl | None = None
    blog: HttpUrl | None = None
    twitter: HttpUrl | None = None


class PersonalInfo(BaseModel):
    """Personal and contact information."""

    name: str = Field(min_length=2, max_length=100, description="Full name")
    title: str = Field(
        min_length=5, max_length=100, description="Current or target job title"
    )
    email: EmailStr
    phone: str | None = Field(
        None,
        pattern=r"^\+?[1-9][\d\-\.\s()]{7,14}$",
        description="Phone in international format",
    )
    location: Location
    links: Links | None = None


class ProfessionalSummary(BaseModel):
    """Professional summary and key strengths."""

    headline: str = Field(
        min_length=10, max_length=200, description="Compelling one-line summary"
    )
    overview: str = Field(
        min_length=100, max_length=1000, description="Detailed professional overview"
    )
    key_strengths: list[str] = Field(
        description="Core competencies and strengths", min_length=3, max_length=8
    )
    years_experience: int | None = Field(
        None, ge=0, le=50, description="Total years of professional experience"
    )
    ai_enhanced: bool = Field(
        default=False, description="Whether content was enhanced by AI"
    )


class Metric(BaseModel):
    """Quantifiable metrics for achievements."""

    value: str | int | float
    unit: str
    improvement: bool = Field(
        default=True, description="Whether this is an improvement"
    )


class Achievement(BaseModel):
    """Individual achievement or accomplishment."""

    description: str = Field(
        min_length=20, max_length=300, description="Achievement description"
    )
    impact: Impact = Field(default=Impact.MEDIUM)
    metrics: list[Metric] | None = None
    technologies: list[str] | None = None
    ai_enhanced: bool = Field(default=False)


class Experience(BaseModel):
    """Professional work experience."""

    company: str = Field(min_length=2, max_length=100)
    role: str = Field(min_length=5, max_length=100)
    start_date: str = Field(pattern=r"^\d{4}-\d{2}$", description="YYYY-MM format")
    end_date: str | None = Field(
        None,
        pattern=r"^\d{4}-\d{2}$",
        description="YYYY-MM format, null for current position",
    )
    location: str | None = Field(None, max_length=100)
    company_description: str | None = Field(
        None, max_length=200, description="Brief company overview"
    )
    achievements: list[Achievement] = Field(
        min_items=1, max_items=12, description="Key achievements in this role"
    )

    @property
    def is_current(self) -> bool:
        """Check if this is the current position."""
        return self.end_date is None

    @property
    def duration_months(self) -> int | None:
        """Calculate duration in months."""
        if not self.end_date:
            # Current position - calculate from start to now
            current_date = datetime.now()
            start_year, start_month = map(int, self.start_date.split("-"))
            return (current_date.year - start_year) * 12 + (
                current_date.month - start_month
            )

        start_year, start_month = map(int, self.start_date.split("-"))
        end_year, end_month = map(int, self.end_date.split("-"))
        return (end_year - start_year) * 12 + (end_month - start_month)


class Skill(BaseModel):
    """Individual skill with proficiency and metadata."""

    name: str = Field(min_length=2, max_length=50)
    proficiency: Proficiency
    years_experience: int | None = Field(None, ge=0, le=30)
    certifications: list[str] | None = None
    last_used: str | None = Field(
        None, pattern=r"^\d{4}$", description="Year last used professionally"
    )


class SkillCategory(BaseModel):
    """Category of related skills."""

    display_name: str | None = None
    priority: int = Field(default=5, ge=1, le=10, description="Display priority")
    skills: list[Skill] = Field(min_items=1, description="Skills in this category")


class Skills(BaseModel):
    """Complete skills section."""

    categories: dict[str, SkillCategory] = Field(
        description="Skill categories mapped by key"
    )
    summary: str | None = Field(
        None, max_length=500, description="AI-generated skills summary"
    )

    @validator("categories")
    def validate_category_keys(cls, v):
        """Validate category keys are valid identifiers."""
        for key in v.keys():
            if not key.replace("_", "").replace(" ", "").isalnum():
                raise ValueError(f"Invalid category key: {key}")
        return v


class Education(BaseModel):
    """Educational background."""

    institution: str = Field(min_length=2, max_length=100)
    degree: str = Field(min_length=5, max_length=100)
    field_of_study: str | None = Field(None, max_length=100)
    graduation_date: str = Field(pattern=r"^\d{4}$", description="Graduation year")
    gpa: float | None = Field(None, ge=0.0, le=4.0)
    honors: list[str] | None = None
    relevant_coursework: list[str] | None = None


class Certification(BaseModel):
    """Professional certification."""

    name: str = Field(min_length=5, max_length=100)
    issuer: str = Field(min_length=2, max_length=100)
    date_earned: str = Field(pattern=r"^\d{4}-\d{2}$", description="YYYY-MM format")
    expiration_date: str | None = Field(
        None, pattern=r"^\d{4}-\d{2}$", description="YYYY-MM format"
    )
    credential_id: str | None = None
    verification_url: HttpUrl | None = None
    priority: int = Field(default=5, ge=1, le=10)

    @property
    def is_expired(self) -> bool:
        """Check if certification is expired."""
        if not self.expiration_date:
            return False

        exp_year, exp_month = map(int, self.expiration_date.split("-"))
        current_date = datetime.now()
        return (exp_year, exp_month) < (current_date.year, current_date.month)


class Project(BaseModel):
    """Personal or professional project."""

    name: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=50, max_length=500)
    technologies: list[str] = Field(min_items=1, description="Technologies used")
    url: HttpUrl | None = None
    github_url: HttpUrl | None = None
    start_date: str | None = Field(None, pattern=r"^\d{4}-\d{2}$")
    end_date: str | None = Field(None, pattern=r"^\d{4}-\d{2}$")
    status: ProjectStatus | None = None
    highlights: list[str] | None = None
    ai_enhanced: bool = Field(default=False)


class Award(BaseModel):
    """Professional award or recognition."""

    title: str
    issuer: str
    date: str = Field(pattern=r"^\d{4}-\d{2}$")
    description: str | None = None


class Publication(BaseModel):
    """Published work or article."""

    title: str
    publication: str
    date: str = Field(pattern=r"^\d{4}-\d{2}$")
    url: HttpUrl | None = None
    co_authors: list[str] | None = None


class Language(BaseModel):
    """Language proficiency."""

    language: str
    proficiency: LanguageProficiency


class AIEnhancement(BaseModel):
    """Metadata about AI enhancements."""

    total_enhanced_fields: int = Field(ge=0)
    enhancement_date: datetime
    ai_model_version: str
    enhancement_notes: str | None = None


class BuildInfo(BaseModel):
    """Build and deployment metadata."""

    build_number: int | None = None
    commit_hash: str | None = None
    build_date: datetime | None = None


class Analytics(BaseModel):
    """Analytics and scoring metadata."""

    keywords_density: dict[str, float] | None = None
    ats_score: float | None = Field(None, ge=0, le=100)
    readability_score: float | None = Field(None, ge=0, le=100)


class Metadata(BaseModel):
    """Resume metadata and analytics."""

    created_date: datetime | None = None
    ai_enhancements: AIEnhancement | None = None
    build_info: BuildInfo | None = None
    analytics: Analytics | None = None


class ResumeData(BaseModel):
    """Complete resume data model."""

    version: str = Field(pattern=r"^\d+\.\d+\.\d+$", description="Semantic version")
    last_updated: datetime
    personal_info: PersonalInfo
    professional_summary: ProfessionalSummary
    experience: list[Experience] = Field(min_items=1)
    skills: Skills
    education: list[Education] = Field(min_items=1)
    certifications: list[Certification] | None = None
    projects: list[Project] | None = None
    awards: list[Award] | None = None
    publications: list[Publication] | None = None
    languages: list[Language] | None = None
    metadata: Metadata | None = None

    class Config:
        """Pydantic configuration."""

        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
        validate_assignment = True
        extra = "forbid"  # Prevent unknown fields

    @property
    def total_experience_years(self) -> int:
        """Calculate total years of experience from all positions."""
        if self.professional_summary.years_experience:
            return self.professional_summary.years_experience

        # Calculate from experience entries
        total_months = sum(exp.duration_months or 0 for exp in self.experience)
        return max(1, total_months // 12)

    @property
    def current_role(self) -> Experience | None:
        """Get current position if any."""
        for exp in self.experience:
            if exp.is_current:
                return exp
        return None

    @property
    def active_certifications(self) -> list[Certification]:
        """Get non-expired certifications."""
        if not self.certifications:
            return []
        return [cert for cert in self.certifications if not cert.is_expired]

    def get_skills_by_category(self, category: str) -> list[Skill]:
        """Get all skills in a specific category."""
        if category not in self.skills.categories:
            return []
        return self.skills.categories[category].skills

    def get_top_skills(self, limit: int = 10) -> list[Skill]:
        """Get top skills across all categories."""
        all_skills = []
        for category in self.skills.categories.values():
            all_skills.extend(category.skills)

        # Sort by proficiency and years of experience
        proficiency_order = {
            Proficiency.EXPERT: 4,
            Proficiency.ADVANCED: 3,
            Proficiency.INTERMEDIATE: 2,
            Proficiency.BEGINNER: 1,
        }

        sorted_skills = sorted(
            all_skills,
            key=lambda s: (
                proficiency_order.get(s.proficiency, 0),
                s.years_experience or 0,
            ),
            reverse=True,
        )

        return sorted_skills[:limit]
