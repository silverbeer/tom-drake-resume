"""
Pytest configuration and fixtures for the test suite.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

import pytest
import yaml

from src.resume.models import ResumeData


@pytest.fixture
def sample_resume_data() -> dict[str, Any]:
    """Sample resume data for testing."""
    return {
        "version": "1.0.0",
        "last_updated": "2025-01-15T10:00:00Z",
        "personal_info": {
            "name": "Test User",
            "title": "Senior DevOps Engineer",
            "email": "test@example.com",
            "phone": "+1-555-123-4567",
            "location": {
                "city": "San Francisco",
                "state": "CA",
                "country": "USA",
                "remote_friendly": True,
            },
        },
        "professional_summary": {
            "headline": "Experienced DevOps engineer with cloud expertise",
            "overview": "Seasoned professional with extensive experience in cloud platforms, automation, and infrastructure management. Proven track record of delivering scalable solutions and leading technical teams.",
            "key_strengths": [
                "Cloud Architecture",
                "DevOps Automation",
                "Team Leadership",
            ],
            "years_experience": 8,
        },
        "experience": [
            {
                "company": "TechCorp",
                "role": "Senior DevOps Engineer",
                "start_date": "2022-01",
                "end_date": None,
                "location": "San Francisco, CA",
                "achievements": [
                    {
                        "description": "Implemented CI/CD pipeline reducing deployment time by 50%",
                        "impact": "high",
                        "technologies": ["GitHub Actions", "Docker", "Kubernetes"],
                    },
                    {
                        "description": "Managed cloud infrastructure supporting 1M+ users",
                        "impact": "high",
                        "technologies": ["AWS", "Terraform", "Prometheus"],
                    },
                ],
            }
        ],
        "skills": {
            "categories": {
                "cloud": {
                    "display_name": "Cloud Platforms",
                    "priority": 10,
                    "skills": [
                        {
                            "name": "AWS",
                            "proficiency": "expert",
                            "years_experience": 5,
                            "last_used": "2024",
                        }
                    ],
                }
            }
        },
        "education": [
            {
                "institution": "University of California",
                "degree": "Bachelor of Science",
                "field_of_study": "Computer Science",
                "graduation_date": "2015",
            }
        ],
    }


@pytest.fixture
def sample_resume_model(sample_resume_data) -> ResumeData:
    """Sample resume model for testing."""
    return ResumeData(**sample_resume_data)


@pytest.fixture
def temp_resume_file(sample_resume_data) -> Path:
    """Create a temporary resume YAML file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
        yaml.dump(sample_resume_data, f, default_flow_style=False)
        return Path(f.name)


@pytest.fixture
def temp_schema_file() -> Path:
    """Create a temporary schema file."""
    # Simple schema for testing
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": [
            "version",
            "personal_info",
            "professional_summary",
            "experience",
            "skills",
            "education",
        ],
        "properties": {
            "version": {"type": "string"},
            "last_updated": {"type": "string"},
            "personal_info": {"type": "object"},
            "professional_summary": {"type": "object"},
            "experience": {"type": "array"},
            "skills": {"type": "object"},
            "education": {"type": "array"},
        },
    }

    import json

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(schema, f)
        return Path(f.name)


@pytest.fixture
def mock_claude_response():
    """Mock Claude API response for testing."""
    return {
        "content": [
            {
                "type": "text",
                "text": "Enhanced achievement: Implemented CI/CD pipeline using GitHub Actions and Docker, reducing deployment time from 2 hours to 30 minutes (75% improvement) while increasing deployment frequency by 300%",
            }
        ],
        "usage": {"input_tokens": 100, "output_tokens": 50},
    }
