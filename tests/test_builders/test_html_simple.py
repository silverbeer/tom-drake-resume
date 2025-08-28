"""
Simple tests for the HTML builder.

Tests basic functionality without complex mocking.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch
import pytest

from src.resume.builders.html import HtmlBuilder


class TestHtmlBuilderSimple:
    """Test the HtmlBuilder class with simple tests."""

    def test_get_file_extension(self, sample_resume_model, tmp_path):
        """Test HTML file extension."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = HtmlBuilder(sample_resume_model, tmp_path / "output")
            assert builder.get_file_extension() == "html"

    def test_get_format_name(self, sample_resume_model, tmp_path):
        """Test HTML format name."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = HtmlBuilder(sample_resume_model, tmp_path / "output")
            assert builder.get_format_name() == "html"

    def test_get_template_extension(self, sample_resume_model, tmp_path):
        """Test HTML template extension."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = HtmlBuilder(sample_resume_model, tmp_path / "output")
            assert builder.get_template_extension() == "html"

    def test_builder_initialization(self, sample_resume_model, tmp_path):
        """Test that HTML builder initializes without errors."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = HtmlBuilder(sample_resume_model, tmp_path / "output")
            assert builder is not None
            assert builder.theme == "modern"

    def test_jinja_environment_setup(self, sample_resume_model, tmp_path):
        """Test that Jinja2 environment is set up."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = HtmlBuilder(sample_resume_model, tmp_path / "output")
            assert hasattr(builder, 'env')
            assert builder.env is not None

    def test_custom_filters_registered(self, sample_resume_model, tmp_path):
        """Test that custom Jinja2 filters are registered."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = HtmlBuilder(sample_resume_model, tmp_path / "output")
            
            # Check that filters are registered
            filters = builder.env.filters
            assert 'format_date' in filters
            assert 'format_phone' in filters
            assert 'format_duration' in filters
            assert 'skill_level_class' in filters

    def test_format_date_method_exists(self, sample_resume_model, tmp_path):
        """Test that format date method exists."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = HtmlBuilder(sample_resume_model, tmp_path / "output")
            assert hasattr(builder, '_format_date')
            assert callable(builder._format_date)

    def test_format_phone_method_exists(self, sample_resume_model, tmp_path):
        """Test that format phone method exists."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = HtmlBuilder(sample_resume_model, tmp_path / "output")
            assert hasattr(builder, '_format_phone')
            assert callable(builder._format_phone)

    def test_output_path_generation(self, sample_resume_model, tmp_path):
        """Test output path generation."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = HtmlBuilder(sample_resume_model, tmp_path / "output")
            path = builder.get_output_path()
            assert path.name == "resume.html"
            assert path.parent == tmp_path / "output"

    def test_custom_output_name(self, sample_resume_model, tmp_path):
        """Test custom output name."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = HtmlBuilder(sample_resume_model, tmp_path / "output")
            path = builder.get_output_path("custom")
            assert path.name == "custom.html"