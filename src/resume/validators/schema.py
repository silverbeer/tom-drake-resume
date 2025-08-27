"""
Schema validation for resume data.

Provides comprehensive validation against JSON schema and business logic rules.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import jsonschema
import yaml
from pydantic import ValidationError

from ..models import ResumeData


@dataclass
class ValidationResult:
    """Result of resume validation."""

    is_valid: bool
    errors: list[str]
    warnings: list[str]
    data: ResumeData | None = None

    @property
    def has_warnings(self) -> bool:
        """Check if validation has warnings."""
        return len(self.warnings) > 0

    def __bool__(self) -> bool:
        """Boolean evaluation based on validity."""
        return self.is_valid


def validate_resume_data(data: dict[str, Any], schema_path: Path) -> ValidationResult:
    """
    Validate resume data against JSON schema and business rules.

    Args:
        data: Resume data dictionary
        schema_path: Path to JSON schema file

    Returns:
        ValidationResult with validation status and details
    """
    errors = []
    warnings = []
    resume_data = None

    try:
        # Load and validate JSON schema
        if not schema_path.exists():
            errors.append(f"Schema file not found: {schema_path}")
            return ValidationResult(False, errors, warnings)

        with open(schema_path) as f:
            schema = json.load(f)

        # JSON Schema validation
        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation error: {e.message}")
            if e.path:
                path_str = " -> ".join(str(p) for p in e.path)
                errors.append(f"  Path: {path_str}")
            return ValidationResult(False, errors, warnings)
        except jsonschema.SchemaError as e:
            errors.append(f"Invalid schema: {e.message}")
            return ValidationResult(False, errors, warnings)

        # Pydantic model validation
        try:
            resume_data = ResumeData(**data)
        except ValidationError as e:
            for error in e.errors():
                field = " -> ".join(str(f) for f in error["loc"])
                message = error["msg"]
                errors.append(f"Data validation error in {field}: {message}")
            return ValidationResult(False, errors, warnings)

        # Business logic validation
        business_errors, business_warnings = _validate_business_rules(resume_data)
        errors.extend(business_errors)
        warnings.extend(business_warnings)

        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings, resume_data)

    except Exception as e:
        errors.append(f"Unexpected validation error: {e!s}")
        return ValidationResult(False, errors, warnings)


def validate_resume_file(resume_path: Path, schema_path: Path) -> ValidationResult:
    """
    Validate resume YAML file against schema.

    Args:
        resume_path: Path to resume YAML file
        schema_path: Path to JSON schema file

    Returns:
        ValidationResult with validation status and details
    """
    errors = []
    warnings = []

    try:
        # Check file existence
        if not resume_path.exists():
            errors.append(f"Resume file not found: {resume_path}")
            return ValidationResult(False, errors, warnings)

        # Load YAML data
        try:
            with open(resume_path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            errors.append(f"YAML parsing error: {e!s}")
            return ValidationResult(False, errors, warnings)
        except Exception as e:
            errors.append(f"Error reading resume file: {e!s}")
            return ValidationResult(False, errors, warnings)

        if data is None:
            errors.append("Resume file is empty")
            return ValidationResult(False, errors, warnings)

        # Validate data
        return validate_resume_data(data, schema_path)

    except Exception as e:
        errors.append(f"Unexpected error validating file: {e!s}")
        return ValidationResult(False, errors, warnings)


def _validate_business_rules(resume_data: ResumeData) -> tuple[list[str], list[str]]:
    """
    Validate business logic rules for resume data.

    Args:
        resume_data: Validated resume data model

    Returns:
        Tuple of (errors, warnings)
    """
    errors = []
    warnings = []

    # Check experience chronology
    sorted_experience = sorted(
        resume_data.experience, key=lambda x: x.start_date, reverse=True
    )

    for i, exp in enumerate(sorted_experience[:-1]):
        next_exp = sorted_experience[i + 1]

        # Check for gaps (allowing some flexibility)
        if exp.end_date and next_exp.start_date:
            # Simple date comparison (YYYY-MM format)
            if exp.end_date < next_exp.start_date:
                gap_months = _calculate_month_diff(exp.end_date, next_exp.start_date)
                if gap_months > 6:  # More than 6 months gap
                    warnings.append(
                        f"Potential employment gap between {exp.company} "
                        f"(ended {exp.end_date}) and {next_exp.company} "
                        f"(started {next_exp.start_date})"
                    )

    # Check for current position
    current_positions = [exp for exp in resume_data.experience if exp.is_current]
    if len(current_positions) == 0:
        warnings.append("No current position found - consider adding current role")
    elif len(current_positions) > 1:
        warnings.append("Multiple current positions found - ensure this is intentional")

    # Skills validation
    total_skills = sum(
        len(cat.skills) for cat in resume_data.skills.categories.values()
    )
    if total_skills < 10:
        warnings.append(
            f"Only {total_skills} skills listed - consider adding more for ATS optimization"
        )
    elif total_skills > 50:
        warnings.append(
            f"{total_skills} skills listed - consider focusing on top skills for readability"
        )

    # Check for AI enhancement opportunities
    unenhanced_achievements = []
    for exp in resume_data.experience:
        for achievement in exp.achievements:
            if not achievement.ai_enhanced:
                unenhanced_achievements.append(
                    f"{exp.company}: {achievement.description[:50]}..."
                )

    if unenhanced_achievements and len(unenhanced_achievements) > 5:
        warnings.append(
            f"{len(unenhanced_achievements)} achievements could benefit from AI enhancement"
        )

    # Check for quantified metrics
    achievements_without_metrics = []
    for exp in resume_data.experience:
        for achievement in exp.achievements:
            if not achievement.metrics:
                achievements_without_metrics.append(
                    f"{exp.company}: {achievement.description[:50]}..."
                )

    if achievements_without_metrics and len(achievements_without_metrics) > 3:
        warnings.append(
            f"{len(achievements_without_metrics)} achievements lack quantified metrics"
        )

    # Education validation
    if not resume_data.education:
        warnings.append("No education information found")

    # Professional summary validation
    summary_length = len(resume_data.professional_summary.overview)
    if summary_length < 100:
        warnings.append("Professional summary is quite short - consider expanding")
    elif summary_length > 1000:
        warnings.append("Professional summary is very long - consider condensing")

    return errors, warnings


def _calculate_month_diff(date1: str, date2: str) -> int:
    """
    Calculate month difference between two YYYY-MM dates.

    Args:
        date1: Earlier date in YYYY-MM format
        date2: Later date in YYYY-MM format

    Returns:
        Number of months between dates
    """
    try:
        year1, month1 = map(int, date1.split("-"))
        year2, month2 = map(int, date2.split("-"))

        return (year2 - year1) * 12 + (month2 - month1)
    except (ValueError, AttributeError):
        return 0  # Invalid dates, assume no gap
