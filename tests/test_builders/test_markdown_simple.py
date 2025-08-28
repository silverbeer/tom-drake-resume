"""
Simple tests for the Markdown builder.

Tests basic functionality without complex mocking.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch
import pytest

from src.resume.builders.markdown import MarkdownBuilder


class TestMarkdownBuilderSimple:
    """Test the MarkdownBuilder class with simple tests."""

    def test_get_file_extension(self, sample_resume_model, tmp_path):
        """Test Markdown file extension."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = MarkdownBuilder(sample_resume_model, tmp_path / "output")
            assert builder.get_file_extension() == "md"

    def test_get_format_name(self, sample_resume_model, tmp_path):
        """Test Markdown format name."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = MarkdownBuilder(sample_resume_model, tmp_path / "output")
            assert builder.get_format_name() == "markdown"

    def test_get_template_extension(self, sample_resume_model, tmp_path):
        """Test Markdown template extension."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = MarkdownBuilder(sample_resume_model, tmp_path / "output")
            assert builder.get_template_extension() == "md"

    def test_builder_initialization(self, sample_resume_model, tmp_path):
        """Test that Markdown builder initializes without errors."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = MarkdownBuilder(sample_resume_model, tmp_path / "output")
            assert builder is not None
            assert builder.theme == "github"

    def test_jinja_environment_setup(self, sample_resume_model, tmp_path):
        """Test that Jinja2 environment is set up."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = MarkdownBuilder(sample_resume_model, tmp_path / "output")
            assert hasattr(builder, 'env')
            assert builder.env is not None

    def test_custom_filters_registered(self, sample_resume_model, tmp_path):
        """Test that custom Jinja2 filters are registered."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = MarkdownBuilder(sample_resume_model, tmp_path / "output")
            
            # Check that filters are registered
            filters = builder.env.filters
            assert 'format_date' in filters
            assert 'format_phone' in filters
            assert 'format_duration' in filters

    def test_format_date_method_exists(self, sample_resume_model, tmp_path):
        """Test that format date method exists."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = MarkdownBuilder(sample_resume_model, tmp_path / "output")
            assert hasattr(builder, '_format_date')
            assert callable(builder._format_date)

    def test_format_phone_method_exists(self, sample_resume_model, tmp_path):
        """Test that format phone method exists."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = MarkdownBuilder(sample_resume_model, tmp_path / "output")
            assert hasattr(builder, '_format_phone')
            assert callable(builder._format_phone)

    def test_output_path_generation(self, sample_resume_model, tmp_path):
        """Test output path generation."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = MarkdownBuilder(sample_resume_model, tmp_path / "output")
            path = builder.get_output_path()
            assert path.name == "resume.md"
            assert path.parent == tmp_path / "output"

    def test_custom_output_name(self, sample_resume_model, tmp_path):
        """Test custom output name."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = MarkdownBuilder(sample_resume_model, tmp_path / "output")
            path = builder.get_output_path("custom")
            assert path.name == "custom.md"

    def test_format_date_filter_simple(self, sample_resume_model, tmp_path):
        """Test _format_date method directly."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = MarkdownBuilder(sample_resume_model, tmp_path / "output")
            assert builder._format_date("2023-06") == "Jun 2023"
            assert builder._format_date("") == "Present"

    def test_format_phone_filter_simple(self, sample_resume_model, tmp_path):
        """Test _format_phone method directly.""" 
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = MarkdownBuilder(sample_resume_model, tmp_path / "output")
            assert builder._format_phone("+1-5551234567") == "(555) 123-4567"
            assert builder._format_phone("") == ""