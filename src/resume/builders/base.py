"""
Base builder framework for resume generation.

This module provides the abstract base class and infrastructure for all resume builders,
ensuring consistent interfaces and error handling across different output formats.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime

from ..models import ResumeData
from ..config import Config


class BuilderError(Exception):
    """Base exception for builder errors."""

    def __init__(self, message: str, format_type: Optional[str] = None) -> None:
        self.format_type = format_type
        super().__init__(message)


class TemplateError(BuilderError):
    """Template-related errors."""

    def __init__(
        self,
        message: str,
        template_path: Optional[Path] = None,
        format_type: Optional[str] = None,
    ) -> None:
        self.template_path = template_path
        super().__init__(message, format_type)


class RenderError(BuilderError):
    """Rendering/generation errors."""

    def __init__(
        self,
        message: str,
        output_path: Optional[Path] = None,
        format_type: Optional[str] = None,
    ) -> None:
        self.output_path = output_path
        super().__init__(message, format_type)


class BaseBuilder(ABC):
    """Abstract base class for all resume builders.

    This class defines the interface that all resume builders must implement,
    providing common functionality for template handling, context preparation,
    and error management.
    """

    def __init__(self, config: Config, theme: str = "modern") -> None:
        """Initialize the builder with configuration and theme.

        Args:
            config: Application configuration instance
            theme: Theme name for template selection
        """
        self.config = config
        self.theme = theme
        self.template_dir = config.templates_dir

        # Ensure template directory exists
        if not self.template_dir.exists():
            raise TemplateError(
                f"Templates directory not found: {self.template_dir}",
                format_type=self.get_format_name(),
            )

    @abstractmethod
    def build(self, resume_data: ResumeData, output_path: Path) -> Path:
        """Build resume and return output file path.

        Args:
            resume_data: Validated resume data model
            output_path: Path where the output file should be created

        Returns:
            Path to the generated output file

        Raises:
            TemplateError: If template is missing or invalid
            RenderError: If generation fails
        """
        pass

    @abstractmethod
    def get_file_extension(self) -> str:
        """Return the file extension for this format.

        Returns:
            File extension without the dot (e.g., 'html', 'pdf')
        """
        pass

    @abstractmethod
    def get_format_name(self) -> str:
        """Return format name for template directory.

        Returns:
            Format name used for template directory structure
        """
        pass

    @abstractmethod
    def get_template_extension(self) -> str:
        """Return template file extension.

        Returns:
            Template file extension without the dot
        """
        pass

    def validate_template(self, template_name: str) -> Path:
        """Validate that a template exists and return its path.

        Args:
            template_name: Name of the template file (without extension)

        Returns:
            Path to the validated template file

        Raises:
            TemplateError: If template is not found
        """
        # Build template path: templates/{format}/{template_name}.{ext}
        template_path = (
            self.template_dir
            / self.get_format_name()
            / f"{template_name}.{self.get_template_extension()}"
        )

        if not template_path.exists():
            raise TemplateError(
                f"Template not found: {template_path.name} in {template_path.parent}",
                template_path=template_path,
                format_type=self.get_format_name(),
            )

        if not template_path.is_file():
            raise TemplateError(
                f"Template path is not a file: {template_path}",
                template_path=template_path,
                format_type=self.get_format_name(),
            )

        return template_path

    def validate_theme_template(self, theme: Optional[str] = None) -> Path:
        """Validate that a theme template exists and return its path.

        Args:
            theme: Theme name, defaults to instance theme

        Returns:
            Path to the validated theme template

        Raises:
            TemplateError: If theme template is not found
        """
        theme_name = theme or self.theme

        # Build theme template path: templates/{format}/themes/{theme}.{ext}
        theme_template_path = (
            self.template_dir
            / self.get_format_name()
            / "themes"
            / f"{theme_name}.{self.get_template_extension()}"
        )

        if not theme_template_path.exists():
            raise TemplateError(
                f"Theme template not found: {theme_name} for format {self.get_format_name()}",
                template_path=theme_template_path,
                format_type=self.get_format_name(),
            )

        return theme_template_path

    def prepare_context(self, resume_data: ResumeData) -> Dict[str, Any]:
        """Prepare template context from resume data.

        This method converts the Pydantic resume model into a dictionary
        suitable for template rendering, adding metadata and utility data.

        Args:
            resume_data: Validated resume data model

        Returns:
            Dictionary containing all data needed for template rendering
        """
        # Build timestamp for metadata
        build_timestamp = datetime.now()

        # Prepare main sections
        context = {
            # Core resume sections
            "personal_info": resume_data.personal_info,
            "professional_summary": resume_data.professional_summary,
            "experience": resume_data.experience,
            "skills": resume_data.skills,
            "education": resume_data.education,
            # Optional sections (handle None gracefully)
            "certifications": resume_data.certifications or [],
            "projects": resume_data.projects or [],
            "awards": resume_data.awards or [],
            "publications": resume_data.publications or [],
            "languages": resume_data.languages or [],
            # Build metadata
            "metadata": {
                "build_date": build_timestamp.isoformat(),
                "build_date_formatted": build_timestamp.strftime("%B %Y"),
                "resume_version": resume_data.version,
                "last_updated": resume_data.last_updated.isoformat(),
                "last_updated_formatted": resume_data.last_updated.strftime("%B %Y"),
                "theme": self.theme,
                "format": self.get_format_name(),
                "builder_version": "1.0.0",
            },
            # Utility data for templates
            "utils": {
                "total_experience_years": resume_data.total_experience_years,
                "current_role": resume_data.current_role,
                "active_certifications": resume_data.active_certifications,
                "has_projects": bool(resume_data.projects),
                "has_publications": bool(resume_data.publications),
                "has_awards": bool(resume_data.awards),
                "has_languages": bool(resume_data.languages),
            },
        }

        return context

    def ensure_output_directory(self, output_path: Path) -> None:
        """Ensure the output directory exists.

        Args:
            output_path: Path where the output file will be created

        Raises:
            RenderError: If directory creation fails
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise RenderError(
                f"Failed to create output directory: {output_path.parent}",
                output_path=output_path,
                format_type=self.get_format_name(),
            ) from e

    def get_output_filename(self, base_name: str = "resume") -> str:
        """Generate output filename with appropriate extension.

        Args:
            base_name: Base name for the file

        Returns:
            Complete filename with extension
        """
        return f"{base_name}.{self.get_file_extension()}"

    def __repr__(self) -> str:
        """String representation of the builder."""
        return f"{self.__class__.__name__}(format={self.get_format_name()}, theme={self.theme})"
