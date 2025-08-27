"""
Validation modules for the AI-Powered Resume System.

This package provides comprehensive validation capabilities including:
- JSON schema validation against resume-schema.json
- Business logic validation
- Data quality checks
- AI enhancement validation
"""

from .schema import ValidationResult, validate_resume_file, validate_resume_data

__all__ = [
    "ValidationResult",
    "validate_resume_file", 
    "validate_resume_data",
]