"""
Resume builders package.

This package provides multi-format resume generation capabilities with a clean,
extensible architecture. Builders transform structured resume data into professional
output formats including HTML, PDF, JSON, and Markdown.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Type

from ..config import Config
from .base import BaseBuilder, BuilderError, RenderError, TemplateError

# Import builders (will be available after implementation)
# from .html import HtmlBuilder
# from .pdf import PdfBuilder
# from .json_builder import JsonBuilder
# from .markdown import MarkdownBuilder

logger = logging.getLogger(__name__)


class BuilderFactory:
    """Factory for creating resume builders with dynamic registration.

    This factory provides a centralized way to create builder instances,
    manage available formats, and handle builder registration for extensibility.
    """

    # Registry of available builders - will be populated as builders are implemented
    _builders: Dict[str, Type[BaseBuilder]] = {}

    @classmethod
    def create_builder(
        cls, format_type: str, config: Config, theme: str = "modern"
    ) -> BaseBuilder:
        """Create a builder instance for the specified format.

        Args:
            format_type: Output format ('html', 'pdf', 'json', 'markdown')
            config: Application configuration
            theme: Theme name for visual styling

        Returns:
            Configured builder instance

        Raises:
            ValueError: If format_type is not supported
            BuilderError: If builder creation fails
        """
        if not format_type:
            raise ValueError("Format type cannot be empty")

        format_type = format_type.lower().strip()

        if format_type not in cls._builders:
            available = ", ".join(sorted(cls._builders.keys()))
            raise ValueError(
                f"Unknown format '{format_type}'. Available formats: {available or 'none registered'}"
            )

        try:
            builder_class = cls._builders[format_type]
            logger.debug(f"Creating {builder_class.__name__} with theme '{theme}'")
            return builder_class(config, theme)

        except Exception as e:
            raise BuilderError(
                f"Failed to create {format_type} builder: {e}", format_type=format_type
            ) from e

    @classmethod
    def get_available_formats(cls) -> List[str]:
        """Get list of available output formats.

        Returns:
            Sorted list of supported format names
        """
        return sorted(cls._builders.keys())

    @classmethod
    def is_format_supported(cls, format_type: str) -> bool:
        """Check if a format is supported.

        Args:
            format_type: Format to check

        Returns:
            True if format is supported
        """
        return format_type.lower().strip() in cls._builders

    @classmethod
    def register_builder(
        cls, format_type: str, builder_class: Type[BaseBuilder]
    ) -> None:
        """Register a custom builder.

        This allows for extending the system with additional output formats
        without modifying the core factory code.

        Args:
            format_type: Format name to register
            builder_class: Builder class that inherits from BaseBuilder

        Raises:
            ValueError: If format_type is invalid or builder_class is not a BaseBuilder
        """
        if not format_type or not format_type.strip():
            raise ValueError("Format type cannot be empty")

        if not issubclass(builder_class, BaseBuilder):
            raise ValueError(
                f"Builder class must inherit from BaseBuilder, got {builder_class}"
            )

        format_type = format_type.lower().strip()

        # Warn if overriding existing builder
        if format_type in cls._builders:
            existing_class = cls._builders[format_type].__name__
            logger.warning(
                f"Overriding existing builder for format '{format_type}': "
                f"{existing_class} -> {builder_class.__name__}"
            )

        cls._builders[format_type] = builder_class
        logger.info(
            f"Registered builder for format '{format_type}': {builder_class.__name__}"
        )

    @classmethod
    def unregister_builder(cls, format_type: str) -> bool:
        """Unregister a builder format.

        Args:
            format_type: Format to unregister

        Returns:
            True if format was unregistered, False if it didn't exist
        """
        format_type = format_type.lower().strip()
        if format_type in cls._builders:
            builder_class = cls._builders.pop(format_type)
            logger.info(
                f"Unregistered builder for format '{format_type}': {builder_class.__name__}"
            )
            return True
        return False

    @classmethod
    def get_builder_info(cls) -> Dict[str, Dict[str, str]]:
        """Get detailed information about all registered builders.

        Returns:
            Dictionary mapping format names to builder information
        """
        info = {}
        for format_type, builder_class in cls._builders.items():
            info[format_type] = {
                "class_name": builder_class.__name__,
                "module": builder_class.__module__,
                "description": getattr(builder_class, "__doc__", "")
                .split("\n")[0]
                .strip(),
            }
        return info


def get_supported_formats() -> List[str]:
    """Convenience function to get supported formats.

    Returns:
        List of supported format names
    """
    return BuilderFactory.get_available_formats()


def create_builder(
    format_type: str, config: Config, theme: str = "modern"
) -> BaseBuilder:
    """Convenience function to create a builder.

    Args:
        format_type: Output format
        config: Application configuration
        theme: Theme name

    Returns:
        Configured builder instance
    """
    return BuilderFactory.create_builder(format_type, config, theme)


# Auto-registration of builders (uncomment as builders are implemented)
# This will automatically register builders when the package is imported


def _register_core_builders() -> None:
    """Register core builders if available."""
    builders_to_register = [
        # ('html', 'HtmlBuilder', '.html'),
        # ('pdf', 'PdfBuilder', '.pdf'),
        # ('json', 'JsonBuilder', '.json_builder'),
        # ('markdown', 'MarkdownBuilder', '.markdown'),
    ]

    for format_type, class_name, module_name in builders_to_register:
        try:
            # Dynamic import to avoid circular dependencies
            module = __import__(f"resume.builders{module_name}", fromlist=[class_name])
            builder_class = getattr(module, class_name)
            BuilderFactory.register_builder(format_type, builder_class)
        except (ImportError, AttributeError):
            # Builder not yet implemented - this is expected during development
            logger.debug(f"Builder not available: {class_name} (format: {format_type})")


# Register available builders on import
_register_core_builders()


# Public API exports
__all__ = [
    # Base classes and errors
    "BaseBuilder",
    "BuilderError",
    "TemplateError",
    "RenderError",
    # Factory and utilities
    "BuilderFactory",
    "create_builder",
    "get_supported_formats",
    # Individual builders (will be available after implementation)
    # "HtmlBuilder",
    # "PdfBuilder",
    # "JsonBuilder",
    # "MarkdownBuilder",
]
