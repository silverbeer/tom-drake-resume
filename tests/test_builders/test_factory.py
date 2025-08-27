"""
Tests for the builder factory system.

This module tests the BuilderFactory class and its registration/creation functionality.
"""

from __future__ import annotations

import pytest
from unittest.mock import Mock

from src.resume.builders import BuilderFactory, BaseBuilder
from src.resume.builders.base import BuilderError
from src.resume.config import Config


class MockBuilder(BaseBuilder):
    """Mock builder for testing factory functionality."""
    
    def build(self, resume_data, output_path):
        return output_path
    
    def get_file_extension(self) -> str:
        return "mock"
    
    def get_format_name(self) -> str:
        return "mock"
    
    def get_template_extension(self) -> str:
        return "html"


class AnotherMockBuilder(BaseBuilder):
    """Another mock builder for testing registration."""
    
    def build(self, resume_data, output_path):
        return output_path
    
    def get_file_extension(self) -> str:
        return "another"
    
    def get_format_name(self) -> str:
        return "another"
    
    def get_template_extension(self) -> str:
        return "html"


class TestBuilderFactory:
    """Test the BuilderFactory class."""
    
    def setup_method(self):
        """Set up test environment."""
        # Clear the factory registry for clean tests
        BuilderFactory._builders.clear()
    
    def teardown_method(self):
        """Clean up after tests."""
        # Clear the factory registry
        BuilderFactory._builders.clear()
    
    def test_register_builder(self):
        """Test builder registration."""
        BuilderFactory.register_builder("mock", MockBuilder)
        
        assert "mock" in BuilderFactory._builders
        assert BuilderFactory._builders["mock"] == MockBuilder
    
    def test_register_builder_invalid_format(self):
        """Test registration with invalid format type."""
        with pytest.raises(ValueError, match="Format type cannot be empty"):
            BuilderFactory.register_builder("", MockBuilder)
        
        with pytest.raises(ValueError, match="Format type cannot be empty"):
            BuilderFactory.register_builder("   ", MockBuilder)
    
    def test_register_builder_invalid_class(self):
        """Test registration with invalid builder class."""
        class NotABuilder:
            pass
        
        with pytest.raises(ValueError, match="Builder class must inherit from BaseBuilder"):
            BuilderFactory.register_builder("invalid", NotABuilder)
    
    def test_register_builder_override_warning(self, caplog):
        """Test warning when overriding existing builder."""
        # Register first builder
        BuilderFactory.register_builder("test", MockBuilder)
        
        # Register another builder with same format (should warn)
        BuilderFactory.register_builder("test", AnotherMockBuilder)
        
        assert "Overriding existing builder" in caplog.text
        assert BuilderFactory._builders["test"] == AnotherMockBuilder
    
    def test_unregister_builder_success(self):
        """Test successful builder unregistration."""
        BuilderFactory.register_builder("mock", MockBuilder)
        assert "mock" in BuilderFactory._builders
        
        result = BuilderFactory.unregister_builder("mock")
        
        assert result is True
        assert "mock" not in BuilderFactory._builders
    
    def test_unregister_builder_not_found(self):
        """Test unregistering non-existent builder."""
        result = BuilderFactory.unregister_builder("nonexistent")
        assert result is False
    
    def test_get_available_formats_empty(self):
        """Test getting formats when none are registered."""
        formats = BuilderFactory.get_available_formats()
        assert formats == []
    
    def test_get_available_formats_multiple(self):
        """Test getting formats with multiple builders registered."""
        BuilderFactory.register_builder("html", MockBuilder)
        BuilderFactory.register_builder("pdf", AnotherMockBuilder)
        BuilderFactory.register_builder("json", MockBuilder)
        
        formats = BuilderFactory.get_available_formats()
        
        assert len(formats) == 3
        assert "html" in formats
        assert "pdf" in formats  
        assert "json" in formats
        assert formats == sorted(formats)  # Should be sorted
    
    def test_is_format_supported_true(self):
        """Test format support check for registered format."""
        BuilderFactory.register_builder("html", MockBuilder)
        
        assert BuilderFactory.is_format_supported("html") is True
        assert BuilderFactory.is_format_supported("HTML") is True  # Case insensitive
        assert BuilderFactory.is_format_supported(" html ") is True  # Whitespace stripped
    
    def test_is_format_supported_false(self):
        """Test format support check for unregistered format."""
        assert BuilderFactory.is_format_supported("nonexistent") is False
        assert BuilderFactory.is_format_supported("") is False
    
    def test_create_builder_success(self, sample_config):
        """Test successful builder creation."""
        BuilderFactory.register_builder("mock", MockBuilder)
        
        builder = BuilderFactory.create_builder("mock", sample_config, theme="test")
        
        assert isinstance(builder, MockBuilder)
        assert builder.config == sample_config
        assert builder.theme == "test"
    
    def test_create_builder_default_theme(self, sample_config):
        """Test builder creation with default theme."""
        BuilderFactory.register_builder("mock", MockBuilder)
        
        builder = BuilderFactory.create_builder("mock", sample_config)
        
        assert builder.theme == "modern"  # Default theme
    
    def test_create_builder_case_insensitive(self, sample_config):
        """Test builder creation is case insensitive."""
        BuilderFactory.register_builder("mock", MockBuilder)
        
        builder = BuilderFactory.create_builder("MOCK", sample_config)
        
        assert isinstance(builder, MockBuilder)
    
    def test_create_builder_whitespace_stripped(self, sample_config):
        """Test builder creation strips whitespace."""
        BuilderFactory.register_builder("mock", MockBuilder)
        
        builder = BuilderFactory.create_builder("  mock  ", sample_config)
        
        assert isinstance(builder, MockBuilder)
    
    def test_create_builder_empty_format(self, sample_config):
        """Test builder creation with empty format type."""
        with pytest.raises(ValueError, match="Format type cannot be empty"):
            BuilderFactory.create_builder("", sample_config)
    
    def test_create_builder_unknown_format(self, sample_config):
        """Test builder creation with unknown format."""
        with pytest.raises(ValueError, match="Unknown format 'unknown'"):
            BuilderFactory.create_builder("unknown", sample_config)
    
    def test_create_builder_unknown_format_with_available(self, sample_config):
        """Test error message includes available formats."""
        BuilderFactory.register_builder("html", MockBuilder)
        BuilderFactory.register_builder("pdf", AnotherMockBuilder)
        
        with pytest.raises(ValueError, match="Available formats: html, pdf"):
            BuilderFactory.create_builder("unknown", sample_config)
    
    def test_create_builder_no_formats_available(self, sample_config):
        """Test error message when no formats are available."""
        with pytest.raises(ValueError, match="Available formats: none registered"):
            BuilderFactory.create_builder("unknown", sample_config)
    
    def test_create_builder_construction_failure(self, sample_config):
        """Test handling of builder construction failure."""
        class FailingBuilder(BaseBuilder):
            def __init__(self, config, theme="modern"):
                raise RuntimeError("Construction failed")
            
            def build(self, resume_data, output_path):
                return output_path
            
            def get_file_extension(self) -> str:
                return "fail"
            
            def get_format_name(self) -> str:
                return "fail"
                
            def get_template_extension(self) -> str:
                return "html"
        
        BuilderFactory.register_builder("failing", FailingBuilder)
        
        with pytest.raises(BuilderError, match="Failed to create failing builder"):
            BuilderFactory.create_builder("failing", sample_config)
    
    def test_get_builder_info_empty(self):
        """Test getting builder info when no builders registered."""
        info = BuilderFactory.get_builder_info()
        assert info == {}
    
    def test_get_builder_info_multiple(self):
        """Test getting builder info with multiple builders."""
        BuilderFactory.register_builder("mock", MockBuilder)
        BuilderFactory.register_builder("another", AnotherMockBuilder)
        
        info = BuilderFactory.get_builder_info()
        
        assert len(info) == 2
        assert "mock" in info
        assert "another" in info
        
        mock_info = info["mock"]
        assert mock_info["class_name"] == "MockBuilder"
        assert mock_info["module"] == MockBuilder.__module__
        assert "description" in mock_info


# Test fixtures
@pytest.fixture
def sample_config(tmp_path):
    """Create a sample configuration for testing."""
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    
    config = Mock(spec=Config)
    config.templates_dir = templates_dir
    return config