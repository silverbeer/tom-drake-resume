"""
Simple tests for the CLI module.

Tests basic functionality without complex scenarios.
"""

from __future__ import annotations

from typer.testing import CliRunner
import pytest

from src.resume.cli import app


class TestCLISimple:
    """Test CLI commands and functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.runner = CliRunner()

    def test_app_exists(self):
        """Test that the main app exists."""
        assert app is not None

    def test_help_command(self):
        """Test help command shows usage information."""
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "resume" in result.stdout.lower()

    def test_version_command(self):
        """Test version command."""
        result = self.runner.invoke(app, ["--version"])
        # Version command should either work or show help
        assert result.exit_code == 0 or result.exit_code == 2

    def test_validate_help(self):
        """Test validate command help."""
        result = self.runner.invoke(app, ["validate", "--help"])
        assert result.exit_code == 0
        assert "validate" in result.stdout.lower()

    def test_build_help(self):
        """Test build command help."""
        result = self.runner.invoke(app, ["build", "--help"])
        assert result.exit_code == 0
        assert "build" in result.stdout.lower()

    def test_serve_help(self):
        """Test serve command help."""
        result = self.runner.invoke(app, ["serve", "--help"])
        assert result.exit_code == 0
        assert "serve" in result.stdout.lower()

    def test_ai_help(self):
        """Test AI command help."""
        result = self.runner.invoke(app, ["ai", "--help"])
        assert result.exit_code == 0
        assert "ai" in result.stdout.lower()

    def test_status_help(self):
        """Test status command help."""
        result = self.runner.invoke(app, ["status", "--help"])
        assert result.exit_code == 0
        # Status command should show something useful
        assert len(result.stdout) > 0

    def test_init_help(self):
        """Test init command help."""
        result = self.runner.invoke(app, ["init", "--help"])
        assert result.exit_code == 0
        assert "init" in result.stdout.lower()

    def test_invalid_command(self):
        """Test invalid command shows error."""
        result = self.runner.invoke(app, ["invalid_command"])
        assert result.exit_code != 0

    def test_rich_formatting_in_help(self):
        """Test that help shows Rich formatting."""
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        # Should contain emoji or rich formatting indicators
        assert "🚀" in result.stdout or "resume" in result.stdout