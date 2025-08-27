"""
Pydantic data models for the AI-Powered Resume System.

These models provide type safety, validation, and serialization for all resume data,
ensuring consistency across different formats and AI enhancement workflows.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator


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
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None
    website: Optional[HttpUrl] = None
    blog: Optional[HttpUrl] = None
    twitter: Optional[HttpUrl] = None


class PersonalInfo(BaseModel):
    """Personal and contact information."""
    name: str = Field(min_length=2, max_length=100, description="Full name")
    title: str = Field(
        min_length=5, 
        max_length=100, 
        description="Current or target job title"
    )
    email: EmailStr
    phone: Optional[str] = Field(
        None, 
        pattern=r"^\+?[1-9]\d{1,14}$", 
        description="Phone in international format"
    )
    location: Location
    links: Optional[Links] = None


class ProfessionalSummary(BaseModel):
    """Professional summary and key strengths."""
    headline: str = Field(
        min_length=10,
        max_length=200,
        description="Compelling one-line summary"
    )
    overview: str = Field(
        min_length=100,
        max_length=1000,
        description="Detailed professional overview"
    )
    key_strengths: List[str] = Field(
        min_items=3,
        max_items=8,
        description="Core competencies and strengths"
    )
    years_experience: Optional[int] = Field(
        None,
        ge=0,
        le=50,
        description="Total years of professional experience"
    )
    ai_enhanced: bool = Field(
        default=False,
        description="Whether content was enhanced by AI"
    )


class Metric(BaseModel):
    """Quantifiable metrics for achievements."""
    value: Union[str, int, float]
    unit: str
    improvement: bool = Field(default=True, description="Whether this is an improvement")


class Achievement(BaseModel):
    """Individual achievement or accomplishment."""
    description: str = Field(
        min_length=20,
        max_length=300,
        description="Achievement description"
    )
    impact: Impact = Field(default=Impact.MEDIUM)
    metrics: Optional[List[Metric]] = None
    technologies: Optional[List[str]] = None
    ai_enhanced: bool = Field(default=False)


class Experience(BaseModel):
    """Professional work experience."""
    company: str = Field(min_length=2, max_length=100)
    role: str = Field(min_length=5, max_length=100)
    start_date: str = Field(pattern=r"^\d{4}-\d{2}$", description="YYYY-MM format")
    end_date: Optional[str] = Field(
        None,
        pattern=r"^\d{4}-\d{2}$", 
        description="YYYY-MM format, null for current position"
    )
    location: Optional[str] = Field(None, max_length=100)
    company_description: Optional[str] = Field(
        None,
        max_length=200,
        description="Brief company overview"
    )
    achievements: List[Achievement] = Field(
        min_items=2,
        max_items=8,
        description="Key achievements in this role"
    )

    @property
    def is_current(self) -> bool:
        """Check if this is the current position."""
        return self.end_date is None

    @property
    def duration_months(self) -> Optional[int]:
        """Calculate duration in months."""
        if not self.end_date:
            # Current position - calculate from start to now
            current_date = datetime.now()
            start_year, start_month = map(int, self.start_date.split('-'))
            return (current_date.year - start_year) * 12 + (current_date.month - start_month)
        
        start_year, start_month = map(int, self.start_date.split('-'))
        end_year, end_month = map(int, self.end_date.split('-'))
        return (end_year - start_year) * 12 + (end_month - start_month)


class Skill(BaseModel):
    """Individual skill with proficiency and metadata."""
    name: str = Field(min_length=2, max_length=50)
    proficiency: Proficiency
    years_experience: Optional[int] = Field(None, ge=0, le=30)
    certifications: Optional[List[str]] = None
    last_used: Optional[str] = Field(
        None,
        pattern=r"^\d{4}$",
        description="Year last used professionally"
    )


class SkillCategory(BaseModel):
    """Category of related skills."""
    display_name: Optional[str] = None
    priority: int = Field(default=5, ge=1, le=10, description="Display priority")
    skills: List[Skill] = Field(min_items=1, description="Skills in this category")


class Skills(BaseModel):
    """Complete skills section."""
    categories: Dict[str, SkillCategory] = Field(
        description="Skill categories mapped by key"
    )
    summary: Optional[str] = Field(
        None,
        max_length=500,
        description="AI-generated skills summary"
    )

    @validator('categories')
    def validate_category_keys(cls, v):
        """Validate category keys are valid identifiers."""
        for key in v.keys():
            if not key.replace('_', '').replace(' ', '').isalnum():
                raise ValueError(f"Invalid category key: {key}")
        return v


class Education(BaseModel):
    """Educational background."""
    institution: str = Field(min_length=2, max_length=100)
    degree: str = Field(min_length=5, max_length=100)
    field_of_study: Optional[str] = Field(None, max_length=100)
    graduation_date: str = Field(pattern=r"^\d{4}$", description="Graduation year")
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    honors: Optional[List[str]] = None
    relevant_coursework: Optional[List[str]] = None


class Certification(BaseModel):
    """Professional certification."""
    name: str = Field(min_length=5, max_length=100)
    issuer: str = Field(min_length=2, max_length=100)
    date_earned: str = Field(pattern=r"^\d{4}-\d{2}$", description="YYYY-MM format")
    expiration_date: Optional[str] = Field(
        None,
        pattern=r"^\d{4}-\d{2}$",
        description="YYYY-MM format"
    )
    credential_id: Optional[str] = None
    verification_url: Optional[HttpUrl] = None
    priority: int = Field(default=5, ge=1, le=10)

    @property
    def is_expired(self) -> bool:
        """Check if certification is expired."""
        if not self.expiration_date:
            return False
        
        exp_year, exp_month = map(int, self.expiration_date.split('-'))
        current_date = datetime.now()
        return (exp_year, exp_month) < (current_date.year, current_date.month)


class Project(BaseModel):
    """Personal or professional project."""
    name: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=50, max_length=500)
    technologies: List[str] = Field(min_items=1, description="Technologies used")
    url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    start_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}$")
    end_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}$")
    status: Optional[ProjectStatus] = None
    highlights: Optional[List[str]] = None
    ai_enhanced: bool = Field(default=False)


class Award(BaseModel):
    """Professional award or recognition."""
    title: str
    issuer: str
    date: str = Field(pattern=r"^\d{4}-\d{2}$")
    description: Optional[str] = None


class Publication(BaseModel):
    """Published work or article."""
    title: str
    publication: str
    date: str = Field(pattern=r"^\d{4}-\d{2}$")
    url: Optional[HttpUrl] = None
    co_authors: Optional[List[str]] = None


class Language(BaseModel):
    """Language proficiency."""
    language: str
    proficiency: LanguageProficiency


class AIEnhancement(BaseModel):
    """Metadata about AI enhancements."""
    total_enhanced_fields: int = Field(ge=0)
    enhancement_date: datetime
    ai_model_version: str
    enhancement_notes: Optional[str] = None


class BuildInfo(BaseModel):
    """Build and deployment metadata."""
    build_number: Optional[int] = None
    commit_hash: Optional[str] = None
    build_date: Optional[datetime] = None


class Analytics(BaseModel):
    """Analytics and scoring metadata."""
    keywords_density: Optional[Dict[str, float]] = None
    ats_score: Optional[float] = Field(None, ge=0, le=100)
    readability_score: Optional[float] = Field(None, ge=0, le=100)


class Metadata(BaseModel):
    """Resume metadata and analytics."""
    created_date: Optional[datetime] = None
    ai_enhancements: Optional[AIEnhancement] = None
    build_info: Optional[BuildInfo] = None
    analytics: Optional[Analytics] = None


class ResumeData(BaseModel):
    """Complete resume data model."""
    version: str = Field(pattern=r"^\d+\.\d+\.\d+$", description="Semantic version")
    last_updated: datetime
    personal_info: PersonalInfo
    professional_summary: ProfessionalSummary
    experience: List[Experience] = Field(min_items=1)
    skills: Skills
    education: List[Education] = Field(min_items=1)
    certifications: Optional[List[Certification]] = None
    projects: Optional[List[Project]] = None
    awards: Optional[List[Award]] = None
    publications: Optional[List[Publication]] = None
    languages: Optional[List[Language]] = None
    metadata: Optional[Metadata] = None

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
        total_months = sum(
            exp.duration_months or 0 for exp in self.experience
        )
        return max(1, total_months // 12)

    @property
    def current_role(self) -> Optional[Experience]:
        """Get current position if any."""
        for exp in self.experience:
            if exp.is_current:
                return exp
        return None

    @property
    def active_certifications(self) -> List[Certification]:
        """Get non-expired certifications."""
        if not self.certifications:
            return []
        return [cert for cert in self.certifications if not cert.is_expired]

    def get_skills_by_category(self, category: str) -> List[Skill]:
        """Get all skills in a specific category."""
        if category not in self.skills.categories:
            return []
        return self.skills.categories[category].skills

    def get_top_skills(self, limit: int = 10) -> List[Skill]:
        """Get top skills across all categories."""
        all_skills = []
        for category in self.skills.categories.values():
            all_skills.extend(category.skills)
        
        # Sort by proficiency and years of experience
        proficiency_order = {
            Proficiency.EXPERT: 4,
            Proficiency.ADVANCED: 3, 
            Proficiency.INTERMEDIATE: 2,
            Proficiency.BEGINNER: 1
        }
        
        sorted_skills = sorted(
            all_skills,
            key=lambda s: (
                proficiency_order.get(s.proficiency, 0),
                s.years_experience or 0
            ),
            reverse=True
        )
        
        return sorted_skills[:limit]