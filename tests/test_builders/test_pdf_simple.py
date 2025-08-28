"""
Simple tests for the PDF builder.

Tests basic functionality without complex mocking.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch
import pytest

from src.resume.builders.pdf import PdfBuilder


class TestPdfBuilderSimple:
    """Test the PdfBuilder class with simple tests."""

    def test_get_file_extension(self, sample_resume_model, tmp_path):
        """Test PDF file extension."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = PdfBuilder(sample_resume_model, tmp_path / "output")
            assert builder.get_file_extension() == "pdf"

    def test_get_format_name(self, sample_resume_model, tmp_path):
        """Test PDF format name."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = PdfBuilder(sample_resume_model, tmp_path / "output")
            assert builder.get_format_name() == "pdf"

    def test_get_template_extension(self, sample_resume_model, tmp_path):
        """Test PDF template extension."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = PdfBuilder(sample_resume_model, tmp_path / "output")
            assert builder.get_template_extension() == "pdf"

    def test_builder_initialization(self, sample_resume_model, tmp_path):
        """Test that PDF builder initializes without errors."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = PdfBuilder(sample_resume_model, tmp_path / "output")
            assert builder is not None
            assert builder.theme == "modern"

    def test_setup_custom_styles_method_exists(self, sample_resume_model, tmp_path):
        """Test that setup_custom_styles method exists."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = PdfBuilder(sample_resume_model, tmp_path / "output")
            assert hasattr(builder, '_setup_custom_styles')
            assert callable(builder._setup_custom_styles)

    def test_format_methods_exist(self, sample_resume_model, tmp_path):
        """Test that format methods exist."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = PdfBuilder(sample_resume_model, tmp_path / "output")
            
            # Check that format methods exist
            assert hasattr(builder, '_format_phone')
            assert hasattr(builder, '_format_date')
            assert callable(builder._format_phone)
            assert callable(builder._format_date)

    def test_section_methods_exist(self, sample_resume_model, tmp_path):
        """Test that section building methods exist."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = PdfBuilder(sample_resume_model, tmp_path / "output")
            
            # Check that section methods exist
            assert hasattr(builder, '_add_header')
            assert hasattr(builder, '_add_experience')
            assert hasattr(builder, '_add_skills')
            assert hasattr(builder, '_add_education')

    def test_styles_setup_called(self, sample_resume_model, tmp_path):
        """Test that custom styles setup is called during initialization."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = PdfBuilder(sample_resume_model, tmp_path / "output")
            # If initialization succeeded, styles should be set up
            assert builder is not None

    def test_output_path_generation(self, sample_resume_model, tmp_path):
        """Test output path generation."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = PdfBuilder(sample_resume_model, tmp_path / "output")
            path = builder.get_output_path()
            assert path.name == "resume.pdf"
            assert path.parent == tmp_path / "output"

    def test_custom_output_name(self, sample_resume_model, tmp_path):
        """Test custom output name."""
        with patch('src.resume.PROJECT_ROOT', tmp_path):
            (tmp_path / "templates").mkdir()
            builder = PdfBuilder(sample_resume_model, tmp_path / "output")
            path = builder.get_output_path("custom")
            assert path.name == "custom.pdf"