"""
Tests for the base builder framework.

This module tests the abstract base class, error handling, and common functionality
shared by all resume builders.
"""

from __future__ import annotations

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from src.resume.builders.base import (
    BaseBuilder,
    BuilderError,
    TemplateError,
    RenderError
)
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
        error = TemplateError("Template not found", template_path=template_path, format_type="html")
        assert str(error) == "Template not found"
        assert error.template_path == template_path
        assert error.format_type == "html"
    
    def test_render_error_with_output(self):
        """Test RenderError with output path."""
        output_path = Path("/tmp/output.html")
        error = RenderError("Render failed", output_path=output_path, format_type="html")
        assert str(error) == "Render failed"
        assert error.output_path == output_path
        assert error.format_type == "html"


class ConcreteBuilder(BaseBuilder):
    """Concrete implementation of BaseBuilder for testing."""
    
    def build(self, resume_data: ResumeData, output_path: Path) -> Path:
        return output_path
    
    def get_file_extension(self) -> str:
        return "test"
    
    def get_format_name(self) -> str:
        return "test"
    
    def get_template_extension(self) -> str:
        return "html"


class TestBaseBuilder:
    """Test the BaseBuilder abstract class."""
    
    def test_builder_initialization(self, sample_config):
        """Test builder initialization with valid config."""
        builder = ConcreteBuilder(sample_config, theme="modern")
        assert builder.config == sample_config
        assert builder.theme == "modern"
        assert builder.template_dir == sample_config.templates_dir
    
    def test_builder_initialization_missing_template_dir(self):
        """Test builder initialization with missing template directory."""
        config = Mock(spec=Config)
        config.templates_dir = Path("/nonexistent/templates")
        
        with pytest.raises(TemplateError, match="Templates directory not found"):
            ConcreteBuilder(config)
    
    def test_builder_default_theme(self, sample_config):
        """Test builder initialization with default theme."""
        builder = ConcreteBuilder(sample_config)
        assert builder.theme == "modern"
    
    def test_validate_template_success(self, sample_config, tmp_path):
        """Test successful template validation."""
        # Create template directory structure
        templates_dir = tmp_path / "templates"
        test_dir = templates_dir / "test"
        test_dir.mkdir(parents=True)
        
        # Create test template
        template_file = test_dir / "template.html"
        template_file.write_text("test template")
        
        # Update config to use temp directory
        sample_config.templates_dir = templates_dir
        
        builder = ConcreteBuilder(sample_config)
        result = builder.validate_template("template")
        
        assert result == template_file
        assert result.exists()
    
    def test_validate_template_not_found(self, sample_config, tmp_path):
        """Test template validation with missing template."""
        templates_dir = tmp_path / "templates"
        test_dir = templates_dir / "test"
        test_dir.mkdir(parents=True)
        
        sample_config.templates_dir = templates_dir
        
        builder = ConcreteBuilder(sample_config)
        
        with pytest.raises(TemplateError, match="Template not found"):
            builder.validate_template("nonexistent")
    
    def test_validate_template_is_directory(self, sample_config, tmp_path):
        """Test template validation when path is a directory."""
        templates_dir = tmp_path / "templates"
        test_dir = templates_dir / "test"
        test_dir.mkdir(parents=True)
        
        # Create directory instead of file
        template_dir = test_dir / "template.html"
        template_dir.mkdir()
        
        sample_config.templates_dir = templates_dir
        
        builder = ConcreteBuilder(sample_config)
        
        with pytest.raises(TemplateError, match="Template path is not a file"):
            builder.validate_template("template")
    
    def test_validate_theme_template_success(self, sample_config, tmp_path):
        """Test successful theme template validation."""
        # Create template directory structure
        templates_dir = tmp_path / "templates"
        test_dir = templates_dir / "test" / "themes"
        test_dir.mkdir(parents=True)
        
        # Create theme template
        theme_file = test_dir / "modern.html"
        theme_file.write_text("modern theme template")
        
        sample_config.templates_dir = templates_dir
        
        builder = ConcreteBuilder(sample_config, theme="modern")
        result = builder.validate_theme_template()
        
        assert result == theme_file
        assert result.exists()
    
    def test_validate_theme_template_custom_theme(self, sample_config, tmp_path):
        """Test theme template validation with custom theme."""
        templates_dir = tmp_path / "templates"
        test_dir = templates_dir / "test" / "themes"
        test_dir.mkdir(parents=True)
        
        # Create custom theme template
        theme_file = test_dir / "custom.html"
        theme_file.write_text("custom theme template")
        
        sample_config.templates_dir = templates_dir
        
        builder = ConcreteBuilder(sample_config, theme="modern")
        result = builder.validate_theme_template("custom")
        
        assert result == theme_file
    
    def test_validate_theme_template_not_found(self, sample_config, tmp_path):
        """Test theme template validation with missing theme."""
        templates_dir = tmp_path / "templates"
        test_dir = templates_dir / "test" / "themes"
        test_dir.mkdir(parents=True)
        
        sample_config.templates_dir = templates_dir
        
        builder = ConcreteBuilder(sample_config, theme="nonexistent")
        
        with pytest.raises(TemplateError, match="Theme template not found"):
            builder.validate_theme_template()
    
    def test_prepare_context(self, sample_config, sample_resume_model):
        """Test context preparation from resume data."""
        builder = ConcreteBuilder(sample_config, theme="modern")
        context = builder.prepare_context(sample_resume_model)
        
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
    
    def test_ensure_output_directory_success(self, sample_config, tmp_path):
        """Test successful output directory creation."""
        builder = ConcreteBuilder(sample_config)
        output_path = tmp_path / "output" / "subdir" / "file.html"
        
        builder.ensure_output_directory(output_path)
        
        assert output_path.parent.exists()
        assert output_path.parent.is_dir()
    
    def test_ensure_output_directory_exists(self, sample_config, tmp_path):
        """Test output directory creation when directory exists."""
        builder = ConcreteBuilder(sample_config)
        output_dir = tmp_path / "existing"
        output_dir.mkdir()
        output_path = output_dir / "file.html"
        
        builder.ensure_output_directory(output_path)
        
        assert output_path.parent.exists()
    
    @patch('pathlib.Path.mkdir')
    def test_ensure_output_directory_failure(self, mock_mkdir, sample_config, tmp_path):
        """Test output directory creation failure."""
        mock_mkdir.side_effect = OSError("Permission denied")
        
        builder = ConcreteBuilder(sample_config)
        output_path = tmp_path / "output" / "file.html"
        
        with pytest.raises(RenderError, match="Failed to create output directory"):
            builder.ensure_output_directory(output_path)
    
    def test_get_output_filename_default(self, sample_config):
        """Test output filename generation with default name."""
        builder = ConcreteBuilder(sample_config)
        filename = builder.get_output_filename()
        
        assert filename == "resume.test"
    
    def test_get_output_filename_custom(self, sample_config):
        """Test output filename generation with custom name."""
        builder = ConcreteBuilder(sample_config)
        filename = builder.get_output_filename("custom_resume")
        
        assert filename == "custom_resume.test"
    
    def test_builder_repr(self, sample_config):
        """Test builder string representation."""
        builder = ConcreteBuilder(sample_config, theme="custom")
        repr_str = repr(builder)
        
        assert "ConcreteBuilder" in repr_str
        assert "format=test" in repr_str
        assert "theme=custom" in repr_str


# Test fixtures and utilities
@pytest.fixture
def sample_config(tmp_path):
    """Create a sample configuration for testing."""
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    
    config = Mock(spec=Config)
    config.templates_dir = templates_dir
    return config