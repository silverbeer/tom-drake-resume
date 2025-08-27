"""
Tests for configuration management.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

from src.resume.config import Config


class TestConfig:
    """Tests for Config class."""

    def test_default_config(self):
        """Test default configuration values."""
        config = Config()

        assert config.app_name == "Tom Drake Resume System"
        assert config.version == "1.0.0"
        assert not config.debug
        assert config.dev_port == 8000
        assert config.min_test_coverage == 100.0
        assert "html" in config.formats
        assert config.pdf_engine == "weasyprint"

    def test_environment_variable_override(self):
        """Test configuration override via environment variables."""
        # Set environment variable
        os.environ["DEBUG"] = "true"
        os.environ["DEV_PORT"] = "9000"
        os.environ["APP_NAME"] = "Custom Resume System"

        try:
            config = Config()
            assert config.debug is True
            assert config.dev_port == 9000
            assert config.app_name == "Custom Resume System"
        finally:
            # Clean up environment variables
            os.environ.pop("DEBUG", None)
            os.environ.pop("DEV_PORT", None)
            os.environ.pop("APP_NAME", None)

    def test_api_key_configuration(self):
        """Test AI API key configuration."""
        # Test without API keys
        config = Config()
        assert not config.has_ai_api_key
        assert config.preferred_ai_provider == "none"

        # Test with Claude API key
        os.environ["CLAUDE_API_KEY"] = "test-claude-key"
        try:
            config = Config()
            assert config.has_ai_api_key
            assert config.preferred_ai_provider == "claude"
        finally:
            os.environ.pop("CLAUDE_API_KEY", None)

        # Test with OpenAI API key
        os.environ["OPENAI_API_KEY"] = "test-openai-key"
        try:
            config = Config()
            assert config.has_ai_api_key
            assert config.preferred_ai_provider == "openai"
        finally:
            os.environ.pop("OPENAI_API_KEY", None)

    def test_path_resolution(self):
        """Test path resolution from project root."""
        config = Config()

        # Paths should be absolute
        assert config.resume_file.is_absolute()
        assert config.schema_file.is_absolute()
        assert config.output_dir.is_absolute()

        # Should resolve correctly relative to project root
        assert config.resume_file.name == "resume.yml"
        assert config.schema_file.name == "resume-schema.json"

    def test_formats_validation(self):
        """Test output formats validation."""
        # Valid formats
        valid_formats = ["html", "pdf", "json", "markdown"]
        config = Config(formats=valid_formats)
        assert config.formats == valid_formats

        # Invalid formats should raise validation error
        with pytest.raises(ValueError):
            Config(formats=["html", "invalid_format"])

    def test_pdf_engine_validation(self):
        """Test PDF engine validation."""
        # Valid engine
        config = Config(pdf_engine="weasyprint")
        assert config.pdf_engine == "weasyprint"

        # Invalid engine should raise validation error
        with pytest.raises(ValueError):
            Config(pdf_engine="invalid_engine")

    def test_log_level_validation(self):
        """Test log level validation."""
        # Valid log levels
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            config = Config(log_level=level)
            assert config.log_level == level

        # Case insensitive
        config = Config(log_level="info")
        assert config.log_level == "INFO"

        # Invalid log level should raise validation error
        with pytest.raises(ValueError):
            Config(log_level="INVALID")

    def test_get_output_path(self):
        """Test output path generation."""
        config = Config()

        output_path = config.get_output_path("resume.pdf")
        assert output_path.name == "resume.pdf"
        assert output_path.parent == config.output_dir

    def test_ensure_directories(self):
        """Test directory creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            config = Config(
                output_dir=temp_path / "output",
                web_dir=temp_path / "web",
                templates_dir=temp_path / "templates",
            )

            # Directories shouldn't exist initially
            assert not config.output_dir.exists()
            assert not config.web_dir.exists()
            assert not config.templates_dir.exists()

            # Ensure directories
            config.ensure_directories()

            # Directories should now exist
            assert config.output_dir.exists()
            assert config.web_dir.exists()
            assert config.templates_dir.exists()

    def test_create_example_env(self):
        """Test example .env file creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env.example"

            Config.create_example_env(env_path)

            assert env_path.exists()
            content = env_path.read_text()

            # Check for key configuration options
            assert "CLAUDE_API_KEY" in content
            assert "OPENAI_API_KEY" in content
            assert "GITHUB_TOKEN" in content
            assert "DEBUG" in content
            assert "DEV_PORT" in content

    def test_config_repr_hides_sensitive_info(self):
        """Test that sensitive information is hidden in repr."""
        os.environ["CLAUDE_API_KEY"] = "sk-1234567890abcdef"
        os.environ["GITHUB_TOKEN"] = "ghp_1234567890abcdef"

        try:
            config = Config()
            repr_str = repr(config)

            # Should not contain full sensitive values
            assert "sk-1234567890abcdef" not in repr_str
            assert "ghp_1234567890abcdef" not in repr_str

            # Should contain masked versions
            assert "*" in repr_str

        finally:
            os.environ.pop("CLAUDE_API_KEY", None)
            os.environ.pop("GITHUB_TOKEN", None)

    def test_port_range_validation(self):
        """Test port number validation."""
        # Valid port
        config = Config(dev_port=8080)
        assert config.dev_port == 8080

        # Invalid ports should raise validation error
        with pytest.raises(ValueError):
            Config(dev_port=80)  # Too low

        with pytest.raises(ValueError):
            Config(dev_port=70000)  # Too high

    def test_coverage_threshold_validation(self):
        """Test test coverage threshold validation."""
        # Valid coverage
        config = Config(min_test_coverage=95.0)
        assert config.min_test_coverage == 95.0

        # Invalid coverage should raise validation error
        with pytest.raises(ValueError):
            Config(min_test_coverage=-1.0)  # Negative

        with pytest.raises(ValueError):
            Config(min_test_coverage=101.0)  # Over 100%
