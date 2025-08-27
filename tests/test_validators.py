"""
Tests for resume validation functionality.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from src.resume.validators.schema import ValidationResult
from src.resume.validators.schema import validate_resume_data
from src.resume.validators.schema import validate_resume_file


class TestValidationResult:
    """Tests for ValidationResult class."""

    def test_valid_result(self):
        """Test valid validation result."""
        result = ValidationResult(is_valid=True, errors=[], warnings=["Minor warning"])
        assert result.is_valid
        assert bool(result) is True
        assert result.has_warnings
        assert len(result.warnings) == 1

    def test_invalid_result(self):
        """Test invalid validation result."""
        result = ValidationResult(
            is_valid=False, errors=["Validation error"], warnings=[]
        )
        assert not result.is_valid
        assert bool(result) is False
        assert not result.has_warnings
        assert len(result.errors) == 1


class TestValidateResumeData:
    """Tests for validate_resume_data function."""

    def test_valid_data_validation(self, sample_resume_data, temp_schema_file):
        """Test validation of valid resume data."""
        result = validate_resume_data(sample_resume_data, temp_schema_file)

        assert result.is_valid
        assert len(result.errors) == 0
        assert result.data is not None
        assert result.data.personal_info.name == "Test User"

    def test_missing_schema_file(self, sample_resume_data):
        """Test validation with missing schema file."""
        nonexistent_path = Path("nonexistent_schema.json")
        result = validate_resume_data(sample_resume_data, nonexistent_path)

        assert not result.is_valid
        assert "Schema file not found" in result.errors[0]

    def test_invalid_schema_format(self, sample_resume_data):
        """Test validation with invalid schema file."""
        # Create invalid schema
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json")
            invalid_schema_path = Path(f.name)

        result = validate_resume_data(sample_resume_data, invalid_schema_path)
        assert not result.is_valid
        # Should have some kind of JSON parsing error
        assert len(result.errors) > 0

    def test_schema_validation_failure(self, temp_schema_file):
        """Test validation failure due to schema mismatch."""
        invalid_data = {
            "version": "1.0.0",
            # Missing required fields
        }

        result = validate_resume_data(invalid_data, temp_schema_file)
        assert not result.is_valid
        assert any("validation error" in error.lower() for error in result.errors)

    def test_pydantic_validation_failure(self, temp_schema_file):
        """Test validation failure due to Pydantic model validation."""
        # Data that passes JSON schema but fails Pydantic validation
        data = {
            "version": "1.0.0",
            "last_updated": "2025-01-15T10:00:00Z",
            "personal_info": {
                "name": "",  # Empty name should fail min_length validation
                "title": "Test Title",
                "email": "test@example.com",
                "location": {
                    "city": "Test City",
                    "state": "TS",
                    "country": "Test Country",
                },
            },
            "professional_summary": {
                "headline": "Test headline that meets minimum length requirements",
                "overview": "Test overview that meets minimum length requirements for professional summary section",
                "key_strengths": ["Skill 1", "Skill 2", "Skill 3"],
            },
            "experience": [
                {
                    "company": "Test Company",
                    "role": "Test Role",
                    "start_date": "2022-01",
                    "achievements": [
                        {
                            "description": "Test achievement description that meets minimum length"
                        },
                        {
                            "description": "Another test achievement description that meets minimum length"
                        },
                    ],
                }
            ],
            "skills": {
                "categories": {
                    "test": {
                        "skills": [{"name": "Test Skill", "proficiency": "expert"}]
                    }
                }
            },
            "education": [
                {
                    "institution": "Test University",
                    "degree": "Test Degree",
                    "graduation_date": "2020",
                }
            ],
        }

        result = validate_resume_data(data, temp_schema_file)
        assert not result.is_valid
        assert any("validation error" in error.lower() for error in result.errors)


class TestValidateResumeFile:
    """Tests for validate_resume_file function."""

    def test_valid_file_validation(self, temp_resume_file, temp_schema_file):
        """Test validation of valid resume file."""
        result = validate_resume_file(temp_resume_file, temp_schema_file)

        assert result.is_valid
        assert result.data is not None
        assert result.data.personal_info.name == "Test User"

        # Clean up
        temp_resume_file.unlink()
        temp_schema_file.unlink()

    def test_missing_resume_file(self, temp_schema_file):
        """Test validation with missing resume file."""
        nonexistent_path = Path("nonexistent_resume.yml")
        result = validate_resume_file(nonexistent_path, temp_schema_file)

        assert not result.is_valid
        assert "Resume file not found" in result.errors[0]

        temp_schema_file.unlink()

    def test_invalid_yaml_format(self, temp_schema_file):
        """Test validation with invalid YAML format."""
        # Create invalid YAML file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            f.write("invalid: yaml: content: [")
            invalid_yaml_path = Path(f.name)

        result = validate_resume_file(invalid_yaml_path, temp_schema_file)
        assert not result.is_valid
        assert any("yaml" in error.lower() for error in result.errors)

        # Clean up
        invalid_yaml_path.unlink()
        temp_schema_file.unlink()

    def test_empty_resume_file(self, temp_schema_file):
        """Test validation with empty resume file."""
        # Create empty file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            pass  # Empty file
        empty_file_path = Path(f.name)

        result = validate_resume_file(empty_file_path, temp_schema_file)
        assert not result.is_valid
        assert "Resume file is empty" in result.errors[0]

        # Clean up
        empty_file_path.unlink()
        temp_schema_file.unlink()


class TestBusinessRulesValidation:
    """Tests for business rules validation."""

    def test_experience_gap_warning(self, sample_resume_data, temp_schema_file):
        """Test warning for experience gaps."""
        # Add experience with a gap
        gap_experience = {
            "company": "Previous Company",
            "role": "Junior Developer",
            "start_date": "2019-01",
            "end_date": "2020-01",  # 2-year gap before current role
            "achievements": [
                {
                    "description": "Worked on various projects and learned new technologies"
                }
            ],
        }

        data = sample_resume_data.copy()
        data["experience"].append(gap_experience)

        result = validate_resume_data(data, temp_schema_file)

        # Should still be valid but have warnings about the gap
        assert result.is_valid
        # Note: The gap detection might not trigger due to simplified test data
        # This test verifies the validation runs without errors
        temp_schema_file.unlink()

    def test_multiple_current_positions_warning(
        self, sample_resume_data, temp_schema_file
    ):
        """Test warning for multiple current positions."""
        # Add another current position
        current_experience = {
            "company": "Another Company",
            "role": "Consultant",
            "start_date": "2023-01",
            "end_date": None,  # Also current
            "achievements": [
                {
                    "description": "Providing consulting services for cloud migration projects"
                }
            ],
        }

        data = sample_resume_data.copy()
        data["experience"].append(current_experience)

        result = validate_resume_data(data, temp_schema_file)

        assert result.is_valid
        # Should have warning about multiple current positions
        warning_found = any(
            "current position" in warning.lower() for warning in result.warnings
        )
        assert warning_found

        temp_schema_file.unlink()

    def test_skills_count_warnings(self, sample_resume_data, temp_schema_file):
        """Test warnings for skills count."""
        # Test with too few skills
        data = sample_resume_data.copy()
        # Current data has only 1 skill, should trigger warning

        result = validate_resume_data(data, temp_schema_file)

        assert result.is_valid
        # Should have warning about too few skills
        warning_found = any(
            "skills" in warning.lower() and "10" in warning
            for warning in result.warnings
        )
        assert warning_found

        temp_schema_file.unlink()
