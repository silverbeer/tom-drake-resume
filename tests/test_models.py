"""
Tests for resume data models.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.resume.models import Achievement
from src.resume.models import Experience
from src.resume.models import Impact
from src.resume.models import PersonalInfo
from src.resume.models import ProfessionalSummary
from src.resume.models import Proficiency
from src.resume.models import ResumeData
from src.resume.models import Skill


class TestPersonalInfo:
    """Tests for PersonalInfo model."""

    def test_valid_personal_info(self, sample_resume_data):
        """Test valid personal info creation."""
        personal_info = PersonalInfo(**sample_resume_data["personal_info"])
        assert personal_info.name == "Test User"
        assert personal_info.email == "test@example.com"
        assert personal_info.location.city == "San Francisco"

    def test_invalid_email(self, sample_resume_data):
        """Test invalid email validation."""
        data = sample_resume_data["personal_info"].copy()
        data["email"] = "invalid-email"

        with pytest.raises(ValidationError) as exc_info:
            PersonalInfo(**data)

        errors = exc_info.value.errors()
        assert any("email" in str(error) for error in errors)


class TestProfessionalSummary:
    """Tests for ProfessionalSummary model."""

    def test_valid_professional_summary(self, sample_resume_data):
        """Test valid professional summary creation."""
        summary = ProfessionalSummary(**sample_resume_data["professional_summary"])
        assert len(summary.key_strengths) == 3
        assert summary.years_experience == 8

    def test_headline_length_validation(self, sample_resume_data):
        """Test headline length validation."""
        data = sample_resume_data["professional_summary"].copy()
        data["headline"] = "Short"  # Too short

        with pytest.raises(ValidationError):
            ProfessionalSummary(**data)

    def test_key_strengths_validation(self, sample_resume_data):
        """Test key strengths validation."""
        data = sample_resume_data["professional_summary"].copy()
        data["key_strengths"] = ["Only one"]  # Too few

        with pytest.raises(ValidationError):
            ProfessionalSummary(**data)


class TestAchievement:
    """Tests for Achievement model."""

    def test_valid_achievement(self):
        """Test valid achievement creation."""
        achievement = Achievement(
            description="Implemented CI/CD pipeline reducing deployment time by 50%",
            impact=Impact.HIGH,
            technologies=["GitHub Actions", "Docker"],
        )
        assert achievement.impact == Impact.HIGH
        assert len(achievement.technologies) == 2

    def test_description_length_validation(self):
        """Test achievement description length validation."""
        with pytest.raises(ValidationError):
            Achievement(description="Too short")  # Too short


class TestSkill:
    """Tests for Skill model."""

    def test_valid_skill(self):
        """Test valid skill creation."""
        skill = Skill(
            name="Python",
            proficiency=Proficiency.EXPERT,
            years_experience=5,
            last_used="2024",
        )
        assert skill.proficiency == Proficiency.EXPERT
        assert skill.years_experience == 5

    def test_proficiency_enum(self):
        """Test proficiency enum validation."""
        with pytest.raises(ValidationError):
            Skill(name="Python", proficiency="invalid_proficiency")


class TestExperience:
    """Tests for Experience model."""

    def test_valid_experience(self, sample_resume_data):
        """Test valid experience creation."""
        exp_data = sample_resume_data["experience"][0]
        experience = Experience(**exp_data)
        assert experience.company == "TechCorp"
        assert experience.is_current  # end_date is None
        assert len(experience.achievements) == 2

    def test_duration_calculation(self, sample_resume_data):
        """Test duration calculation for experience."""
        exp_data = sample_resume_data["experience"][0].copy()
        exp_data["start_date"] = "2020-01"
        exp_data["end_date"] = "2022-01"

        experience = Experience(**exp_data)
        duration = experience.duration_months
        assert duration == 24  # 2 years = 24 months

    def test_date_format_validation(self, sample_resume_data):
        """Test date format validation."""
        exp_data = sample_resume_data["experience"][0].copy()
        exp_data["start_date"] = "2022"  # Invalid format

        with pytest.raises(ValidationError):
            Experience(**exp_data)


class TestResumeData:
    """Tests for complete ResumeData model."""

    def test_valid_resume_data(self, sample_resume_data):
        """Test valid resume data creation."""
        resume = ResumeData(**sample_resume_data)
        assert resume.version == "1.0.0"
        assert resume.personal_info.name == "Test User"
        assert len(resume.experience) == 1

    def test_total_experience_years(self, sample_resume_model):
        """Test total experience years calculation."""
        years = sample_resume_model.total_experience_years
        assert years == 8  # From professional_summary.years_experience

    def test_current_role(self, sample_resume_model):
        """Test current role identification."""
        current = sample_resume_model.current_role
        assert current is not None
        assert current.company == "TechCorp"

    def test_get_skills_by_category(self, sample_resume_model):
        """Test skills retrieval by category."""
        cloud_skills = sample_resume_model.get_skills_by_category("cloud")
        assert len(cloud_skills) == 1
        assert cloud_skills[0].name == "AWS"

    def test_get_top_skills(self, sample_resume_model):
        """Test top skills retrieval."""
        top_skills = sample_resume_model.get_top_skills(5)
        assert len(top_skills) <= 5
        assert all(skill.name for skill in top_skills)

    def test_missing_required_fields(self, sample_resume_data):
        """Test validation with missing required fields."""
        data = sample_resume_data.copy()
        del data["personal_info"]

        with pytest.raises(ValidationError):
            ResumeData(**data)

    def test_extra_fields_forbidden(self, sample_resume_data):
        """Test that extra fields are forbidden."""
        data = sample_resume_data.copy()
        data["extra_field"] = "not allowed"

        with pytest.raises(ValidationError):
            ResumeData(**data)

    def test_version_format_validation(self, sample_resume_data):
        """Test version format validation."""
        data = sample_resume_data.copy()
        data["version"] = "invalid-version"

        with pytest.raises(ValidationError):
            ResumeData(**data)
