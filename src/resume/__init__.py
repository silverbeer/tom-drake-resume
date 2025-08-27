"""
AI-Powered DevOps Resume System

A revolutionary "Resume as Infrastructure" approach that demonstrates modern DevOps practices
while solving the problem of resume management through automation, AI enhancement, and
comprehensive quality assurance.
"""

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

# Export key components
from .models import ResumeData
from .config import Config

__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    "PACKAGE_ROOT",
    "PROJECT_ROOT", 
    "TEMPLATES_DIR",
    "SCHEMAS_DIR",
    "WEB_DIR",
    "ResumeData",
    "Config",
]