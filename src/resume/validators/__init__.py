"""
Validation modules for the AI-Powered Resume System.

This package provides comprehensive validation capabilities including:
- JSON schema validation against resume-schema.json
- Business logic validation
- Data quality checks
- AI enhancement validation
"""

from __future__ import annotations

from .schema import ValidationResult
from .schema import validate_resume_data
from .schema import validate_resume_file

__all__ = [
    "ValidationResult",
    "validate_resume_data",
    "validate_resume_file",
]
