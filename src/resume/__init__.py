"""
AI-Powered DevOps Resume System

A revolutionary "Resume as Infrastructure" approach that demonstrates modern DevOps practices
while solving the problem of resume management through automation, AI enhancement, and
comprehensive quality assurance.
"""
from __future__ import annotations

__version__ = "1.0.0"
__author__ = "Tom Drake"
__email__ = "tom.drake@example.com"

from pathlib import Path

# Package constants
PACKAGE_ROOT = Path(__file__).parent
PROJECT_ROOT = PACKAGE_ROOT.parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
SCHEMAS_DIR = PROJECT_ROOT / "schemas"
WEB_DIR = PROJECT_ROOT / "web"

from .config import Config

# Export key components
from .models import ResumeData

__all__ = [
    "PACKAGE_ROOT",
    "PROJECT_ROOT",
    "SCHEMAS_DIR",
    "TEMPLATES_DIR",
    "WEB_DIR",
    "Config",
    "ResumeData",
    "__author__",
    "__email__",
    "__version__",
]
