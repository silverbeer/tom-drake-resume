"""
Configuration management for the AI-Powered Resume System.

Handles environment variables, settings, and configuration validation
using Pydantic settings with support for .env files.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Application configuration with environment variable support."""
    
    # Application settings
    app_name: str = Field(default="Tom Drake Resume System")
    version: str = Field(default="1.0.0")
    debug: bool = Field(default=False, description="Enable debug mode")
    
    # File paths
    resume_file: Path = Field(default="resume.yml", description="Path to resume YAML file")
    schema_file: Path = Field(default="schemas/resume-schema.json", description="Path to JSON schema")
    output_dir: Path = Field(default="dist", description="Output directory for built files")
    templates_dir: Path = Field(default="templates", description="Templates directory")
    web_dir: Path = Field(default="web", description="Web assets directory")
    
    # AI Integration
    claude_api_key: Optional[str] = Field(
        default=None,
        description="Claude API key for AI features"
    )
    claude_model: str = Field(
        default="claude-3-sonnet-20240229",
        description="Claude model to use"
    )
    claude_max_tokens: int = Field(default=4096, description="Max tokens for Claude responses")
    claude_temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    
    # OpenAI fallback
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key as fallback"
    )
    openai_model: str = Field(default="gpt-4", description="OpenAI model to use")
    
    # Build settings
    formats: list[str] = Field(
        default=["html", "pdf", "json", "markdown"],
        description="Default output formats"
    )
    pdf_engine: str = Field(
        default="weasyprint",
        description="PDF generation engine (weasyprint, reportlab)"
    )
    html_theme: str = Field(default="modern", description="HTML theme to use")
    
    # Development server
    dev_host: str = Field(default="localhost", description="Development server host")
    dev_port: int = Field(default=8000, ge=1024, le=65535)
    dev_reload: bool = Field(default=True, description="Enable auto-reload in development")
    
    # Quality settings
    min_test_coverage: float = Field(default=100.0, ge=0.0, le=100.0)
    lint_strict: bool = Field(default=True, description="Strict linting mode")
    type_check: bool = Field(default=True, description="Enable type checking")
    
    # GitHub settings
    github_token: Optional[str] = Field(
        default=None,
        description="GitHub token for API access"
    )
    github_repo: Optional[str] = Field(
        default=None,
        description="GitHub repository (owner/repo)"
    )
    github_pages_branch: str = Field(default="gh-pages")
    
    # Analytics and monitoring
    analytics_enabled: bool = Field(default=True, description="Enable analytics")
    sentry_dsn: Optional[str] = Field(
        default=None,
        description="Sentry DSN for error tracking"
    )
    
    # Logging configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
    log_format: str = Field(
        default="structured",
        description="Log format (structured, plain)"
    )
    log_file: Optional[Path] = Field(
        default=None,
        description="Log file path (None for stdout only)"
    )
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8" 
        case_sensitive = False
        extra = "ignore"  # Ignore unknown environment variables

    @validator("resume_file", "schema_file", pre=True)
    def resolve_paths(cls, v):
        """Resolve relative paths from project root."""
        if isinstance(v, str):
            v = Path(v)
        if not v.is_absolute():
            # Get project root (assuming config.py is in src/resume/)
            project_root = Path(__file__).parent.parent.parent
            v = project_root / v
        return v

    @validator("output_dir", "templates_dir", "web_dir", pre=True)
    def resolve_dir_paths(cls, v):
        """Resolve directory paths from project root."""
        if isinstance(v, str):
            v = Path(v)
        if not v.is_absolute():
            project_root = Path(__file__).parent.parent.parent
            v = project_root / v
        return v
        
    @validator("formats")
    def validate_formats(cls, v):
        """Validate output formats."""
        supported_formats = {"html", "pdf", "json", "markdown", "yaml"}
        invalid_formats = set(v) - supported_formats
        if invalid_formats:
            raise ValueError(f"Unsupported formats: {invalid_formats}")
        return v

    @validator("pdf_engine")
    def validate_pdf_engine(cls, v):
        """Validate PDF engine."""
        supported_engines = {"weasyprint", "reportlab"}
        if v not in supported_engines:
            raise ValueError(f"Unsupported PDF engine: {v}. Supported: {supported_engines}")
        return v

    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Valid levels: {valid_levels}")
        return v_upper

    @property
    def has_ai_api_key(self) -> bool:
        """Check if any AI API key is configured."""
        return bool(self.claude_api_key or self.openai_api_key)

    @property
    def preferred_ai_provider(self) -> str:
        """Get the preferred AI provider."""
        if self.claude_api_key:
            return "claude"
        elif self.openai_api_key:
            return "openai"
        else:
            return "none"

    def get_output_path(self, filename: str) -> Path:
        """Get full output path for a file."""
        return self.output_dir / filename

    def ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        directories = [
            self.output_dir,
            self.web_dir,
            self.templates_dir,
        ]
        
        # Add log file directory if specified
        if self.log_file:
            directories.append(self.log_file.parent)
            
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def create_example_env(cls, path: Path = Path(".env.example")) -> None:
        """Create an example .env file with all available options."""
        env_content = '''# AI-Powered Resume System Configuration

# Application Settings
APP_NAME="Tom Drake Resume System"
DEBUG=false

# AI Integration (at least one required for AI features)
CLAUDE_API_KEY=your_claude_api_key_here
CLAUDE_MODEL=claude-3-sonnet-20240229
CLAUDE_MAX_TOKENS=4096
CLAUDE_TEMPERATURE=0.7

# OpenAI Fallback (optional)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# File Paths (relative to project root)
RESUME_FILE=resume.yml
SCHEMA_FILE=resume-schema.json
OUTPUT_DIR=dist
TEMPLATES_DIR=templates
WEB_DIR=web

# Build Settings
FORMATS=html,pdf,json,markdown
PDF_ENGINE=weasyprint
HTML_THEME=modern

# Development Server
DEV_HOST=localhost
DEV_PORT=8000
DEV_RELOAD=true

# Quality Settings
MIN_TEST_COVERAGE=100.0
LINT_STRICT=true
TYPE_CHECK=true

# GitHub Integration (for deployment)
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=your-username/your-repo-name
GITHUB_PAGES_BRANCH=gh-pages

# Analytics and Monitoring
ANALYTICS_ENABLED=true
SENTRY_DSN=your_sentry_dsn_here

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=structured
# LOG_FILE=logs/resume-system.log
'''
        
        path.write_text(env_content)
        print(f"Created example environment file: {path}")

    def validate_ai_config(self) -> None:
        """Validate AI configuration and warn about missing keys."""
        if not self.has_ai_api_key:
            print("Warning: No AI API keys configured. AI features will be disabled.")
            print("Set CLAUDE_API_KEY or OPENAI_API_KEY in your .env file.")
        else:
            print(f"AI provider configured: {self.preferred_ai_provider}")

    def __repr__(self) -> str:
        """String representation hiding sensitive information."""
        sensitive_fields = {
            "claude_api_key", 
            "openai_api_key", 
            "github_token", 
            "sentry_dsn"
        }
        
        safe_dict = {}
        for field, value in self.__dict__.items():
            if field in sensitive_fields and value:
                safe_dict[field] = f"{'*' * (len(str(value)) - 4)}{str(value)[-4:]}"
            else:
                safe_dict[field] = value
                
        return f"Config({safe_dict})"


# Global configuration instance
config = Config()

# Ensure directories exist on import
config.ensure_directories()