"""
Tests for the base builder framework.

This module tests the abstract base class, error handling, and common functionality
shared by all resume builders.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from src.resume.builders.base import BaseBuilder
from src.resume.builders.base import BuilderError
from src.resume.builders.base import RenderError
from src.resume.builders.base import TemplateError
from src.resume.config import Config
from src.resume.models import ResumeData


class TestBuilderError:
    """Test builder exception classes."""

    def test_builder_error_with_format(self):
        """Test BuilderError with format type."""
        error = BuilderError("Test error", format_type="html")
        assert str(error) == "Test error"
        assert error.format_type == "html"

    def test_builder_error_without_format(self):
        """Test BuilderError without format type."""
        error = BuilderError("Test error")
        assert str(error) == "Test error"
        assert error.format_type is None

    def test_template_error_with_path(self):
        """Test TemplateError with template path."""
        template_path = Path("/tmp/test.html")
        error = TemplateError(
            "Template not found", template_path=template_path, format_type="html"
        )
        assert str(error) == "Template not found"
        assert error.template_path == template_path
        assert error.format_type == "html"

    def test_render_error_with_output(self):
        """Test RenderError with output path."""
        output_path = Path("/tmp/output.html")
        error = RenderError(
            "Render failed", output_path=output_path, format_type="html"
        )
        assert str(error) == "Render failed"
        assert error.output_path == output_path
        assert error.format_type == "html"


class ConcreteBuilder(BaseBuilder):
    """Concrete implementation of BaseBuilder for testing."""

    def build(self) -> Path:
        return self.get_output_path()

    def get_file_extension(self) -> str:
        return "test"

    def get_format_name(self) -> str:
        return "test"

    def get_template_extension(self) -> str:
        return "html"


class TestBaseBuilder:
    """Test the BaseBuilder abstract class."""

    def test_builder_initialization(self, sample_resume_model, tmp_path):
        """Test builder initialization with valid resume data."""
        output_dir = tmp_path / "output"
        builder = ConcreteBuilder(sample_resume_model, output_dir, theme="modern")
        assert builder.resume_data == sample_resume_model
        assert builder.output_dir == output_dir
        assert builder.theme == "modern"
        assert output_dir.exists()  # Should be created automatically

    def test_builder_initialization_missing_template_dir(self, sample_resume_model, tmp_path):
        """Test builder initialization with missing template directory."""
        output_dir = tmp_path / "output" 
        
        # Mock the PROJECT_ROOT to point to a non-existent location  
        with patch('src.resume.PROJECT_ROOT', Path("/nonexistent")):
            with pytest.raises(TemplateError, match="Templates directory not found"):
                ConcreteBuilder(sample_resume_model, output_dir)

    def test_builder_default_theme(self, sample_resume_model, tmp_path):
        """Test builder initialization with default theme."""
        output_dir = tmp_path / "output"
        builder = ConcreteBuilder(sample_resume_model, output_dir)
        assert builder.theme == "modern"

    def test_validate_template_success(self, sample_resume_model, tmp_path):
        """Test successful template validation."""
        # Create template directory structure
        templates_dir = tmp_path / "templates"
        test_dir = templates_dir / "test"
        test_dir.mkdir(parents=True)

        # Create test template
        template_file = test_dir / "template.html"
        template_file.write_text("test template")

        # Mock PROJECT_ROOT to use our temp directory
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            builder = ConcreteBuilder(sample_resume_model, tmp_path / "output")
            result = builder.validate_template("template")

            assert result == template_file
            assert result.exists()

    def test_validate_template_not_found(self, sample_resume_model, tmp_path):
        """Test template validation with missing template."""
        templates_dir = tmp_path / "templates"
        test_dir = templates_dir / "test"
        test_dir.mkdir(parents=True)

        # Mock PROJECT_ROOT to use our temp directory
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            builder = ConcreteBuilder(sample_resume_model, tmp_path / "output")

            with pytest.raises(TemplateError, match="Template not found"):
                builder.validate_template("nonexistent")

    def test_validate_template_is_directory(self, sample_resume_model, tmp_path):
        """Test template validation when path is a directory."""
        templates_dir = tmp_path / "templates"
        test_dir = templates_dir / "test"
        test_dir.mkdir(parents=True)

        # Create directory instead of file
        template_dir = test_dir / "template.html"
        template_dir.mkdir()

        # Mock PROJECT_ROOT to use our temp directory
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            builder = ConcreteBuilder(sample_resume_model, tmp_path / "output")

            with pytest.raises(TemplateError, match="Template path is not a file"):
                builder.validate_template("template")

    def test_validate_theme_template_success(self, sample_resume_model, tmp_path):
        """Test successful theme template validation."""
        # Create template directory structure
        templates_dir = tmp_path / "templates"
        test_dir = templates_dir / "test" / "themes"
        test_dir.mkdir(parents=True)

        # Create theme template
        theme_file = test_dir / "modern.html"
        theme_file.write_text("modern theme template")

        # Mock PROJECT_ROOT to use our temp directory
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            builder = ConcreteBuilder(sample_resume_model, tmp_path / "output", theme="modern")
            result = builder.validate_theme_template()

            assert result == theme_file
            assert result.exists()

    def test_validate_theme_template_custom_theme(self, sample_resume_model, tmp_path):
        """Test theme template validation with custom theme."""
        templates_dir = tmp_path / "templates"
        test_dir = templates_dir / "test" / "themes"
        test_dir.mkdir(parents=True)

        # Create custom theme template
        theme_file = test_dir / "custom.html"
        theme_file.write_text("custom theme template")

        # Mock PROJECT_ROOT to use our temp directory
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            builder = ConcreteBuilder(sample_resume_model, tmp_path / "output", theme="modern")
            result = builder.validate_theme_template("custom")

            assert result == theme_file

    def test_validate_theme_template_not_found(self, sample_resume_model, tmp_path):
        """Test theme template validation with missing theme."""
        templates_dir = tmp_path / "templates"
        test_dir = templates_dir / "test" / "themes"
        test_dir.mkdir(parents=True)

        # Mock PROJECT_ROOT to use our temp directory
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            builder = ConcreteBuilder(sample_resume_model, tmp_path / "output", theme="nonexistent")

            with pytest.raises(TemplateError, match="Theme template not found"):
                builder.validate_theme_template()

    def test_prepare_context(self, sample_resume_model, tmp_path):
        """Test context preparation from resume data."""
        # Mock PROJECT_ROOT to use our temp directory
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            # Create minimal template structure
            (tmp_path / "templates").mkdir()
            builder = ConcreteBuilder(sample_resume_model, tmp_path / "output", theme="modern")
            context = builder.prepare_context()

        # Check main sections are present
        assert "personal_info" in context
        assert "professional_summary" in context
        assert "experience" in context
        assert "skills" in context
        assert "education" in context

        # Check optional sections (should be lists even if None)
        assert "certifications" in context
        assert "projects" in context
        assert "awards" in context
        assert "publications" in context
        assert "languages" in context
        assert isinstance(context["certifications"], list)

        # Check metadata
        assert "metadata" in context
        metadata = context["metadata"]
        assert "build_date" in metadata
        assert "theme" in metadata
        assert metadata["theme"] == "modern"
        assert metadata["format"] == "test"
        assert "resume_version" in metadata

        # Check utilities
        assert "utils" in context
        utils = context["utils"]
        assert "total_experience_years" in utils
        assert "current_role" in utils
        assert "active_certifications" in utils

    def test_ensure_output_directory_success(self, sample_resume_model, tmp_path):
        """Test successful output directory creation."""
        # Mock PROJECT_ROOT to use our temp directory
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            # Create minimal template structure
            (tmp_path / "templates").mkdir()
            builder = ConcreteBuilder(sample_resume_model, tmp_path / "output")
            output_path = tmp_path / "output" / "subdir" / "file.html"

            builder.ensure_output_directory(output_path)

            assert output_path.parent.exists()
            assert output_path.parent.is_dir()

    def test_ensure_output_directory_exists(self, sample_resume_model, tmp_path):
        """Test output directory creation when directory exists."""
        # Mock PROJECT_ROOT to use our temp directory
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            # Create minimal template structure
            (tmp_path / "templates").mkdir()
            builder = ConcreteBuilder(sample_resume_model, tmp_path / "output")
            output_dir = tmp_path / "existing"
            output_dir.mkdir()
            output_path = output_dir / "file.html"

            builder.ensure_output_directory(output_path)

            assert output_path.parent.exists()

    def test_ensure_output_directory_failure(self, sample_resume_model, tmp_path):
        """Test output directory creation failure."""
        # Mock PROJECT_ROOT to use our temp directory
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            # Create minimal template structure
            (tmp_path / "templates").mkdir()
            builder = ConcreteBuilder(sample_resume_model, tmp_path / "output")
            output_path = tmp_path / "output" / "file.html"

            # Mock the mkdir method to fail
            with patch("pathlib.Path.mkdir", side_effect=OSError("Permission denied")):
                with pytest.raises(RenderError, match="Failed to create output directory"):
                    builder.ensure_output_directory(output_path)

    def test_get_output_filename_default(self, sample_resume_model, tmp_path):
        """Test output filename generation with default name."""
        # Mock PROJECT_ROOT to use our temp directory
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            # Create minimal template structure
            (tmp_path / "templates").mkdir()
            builder = ConcreteBuilder(sample_resume_model, tmp_path / "output")
            filename = builder.get_output_filename()

            assert filename == "resume.test"

    def test_get_output_filename_custom(self, sample_resume_model, tmp_path):
        """Test output filename generation with custom name."""
        # Mock PROJECT_ROOT to use our temp directory
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            # Create minimal template structure
            (tmp_path / "templates").mkdir()
            builder = ConcreteBuilder(sample_resume_model, tmp_path / "output")
            filename = builder.get_output_filename("custom_resume")

            assert filename == "custom_resume.test"

    def test_builder_repr(self, sample_resume_model, tmp_path):
        """Test builder string representation."""
        # Mock PROJECT_ROOT to use our temp directory
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            # Create minimal template structure
            (tmp_path / "templates").mkdir()
            builder = ConcreteBuilder(sample_resume_model, tmp_path / "output", theme="custom")
            repr_str = repr(builder)

            assert "ConcreteBuilder" in repr_str
            assert "format=test" in repr_str
            assert "theme=custom" in repr_str


