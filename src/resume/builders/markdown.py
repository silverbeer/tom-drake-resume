"""
Markdown resume builder for GitHub and documentation platforms.

This module generates GitHub-flavored markdown resumes with skill badges,
responsive formatting, and optimized layout for GitHub profiles and documentation.
"""

from __future__ import annotations

from pathlib import Path

import jinja2

from .base import BaseBuilder
from .base import RenderError
from .base import TemplateError


class MarkdownBuilder(BaseBuilder):
    """Markdown resume builder with GitHub-flavored formatting."""

    def __init__(self, resume_data, output_dir: Path, theme: str = "github") -> None:
        """Initialize Markdown builder with Jinja2 environment.
        
        Args:
            resume_data: Validated resume data model
            output_dir: Directory where output files will be created
            theme: Theme name for template selection (default: 'github')
        """
        super().__init__(resume_data, output_dir, theme)
        
        # Set up Jinja2 environment for markdown templates
        markdown_template_dir = self.template_dir / "markdown"
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(markdown_template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )
        
        # Add custom filters for markdown formatting
        self.env.filters.update({
            'format_date': self._format_date,
            'format_phone': self._format_phone,
            'format_duration': self._format_duration,
            'skill_badge': self._create_skill_badge,
            'markdown_escape': self._markdown_escape,
            'github_shield': self._create_github_shield,
        })

    def build(self) -> Path:
        """Generate Markdown resume using Jinja2 template.
        
        Returns:
            Path to the generated Markdown file
            
        Raises:
            TemplateError: If template is missing or invalid
            RenderError: If rendering fails
        """
        try:
            # Load GitHub template (using theme as template name)
            template_path = f"{self.theme}.md"
            template = self.env.get_template(template_path)
            
            # Prepare context data
            context = self.prepare_context()
            
            # Render markdown content
            markdown_content = template.render(**context)
            
            # Write to output file
            output_path = self.get_output_path()
            output_path.write_text(markdown_content, encoding='utf-8')
            
            return output_path
            
        except jinja2.TemplateNotFound as e:
            raise TemplateError(
                f"Markdown template not found: {e}",
                template_path=self.template_dir / "markdown" / template_path,
                format_type="markdown"
            ) from e
        except jinja2.TemplateError as e:
            raise RenderError(
                f"Markdown template rendering failed: {e}",
                format_type="markdown"
            ) from e
        except Exception as e:
            raise RenderError(
                f"Markdown generation failed: {e}",
                format_type="markdown"
            ) from e

    def get_file_extension(self) -> str:
        """Return the file extension for Markdown files."""
        return "md"

    def get_format_name(self) -> str:
        """Return format name for template directory."""
        return "markdown"

    def get_template_extension(self) -> str:
        """Return template file extension."""
        return "md"

    # Template filter methods
    def _format_date(self, date_str: str) -> str:
        """Format date string for display.
        
        Args:
            date_str: Date string in YYYY-MM format
            
        Returns:
            Formatted date string
        """
        if not date_str:
            return "Present"
        
        try:
            # Handle YYYY-MM format
            if len(date_str) == 7 and '-' in date_str:
                year, month = date_str.split('-')
                month_names = [
                    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                ]
                month_idx = int(month) - 1
                if 0 <= month_idx < 12:
                    return f"{month_names[month_idx]} {year}"
            
            # Handle YYYY format
            if len(date_str) == 4:
                return date_str
                
            return date_str
            
        except (ValueError, IndexError):
            return date_str

    def _format_phone(self, phone: str) -> str:
        """Format phone number for display.
        
        Args:
            phone: Raw phone number string
            
        Returns:
            Formatted phone number
        """
        if not phone:
            return ""
        
        # Clean the phone number (remove non-digits except + at start)
        cleaned = phone.strip()
        
        # If it starts with +1-, format as (XXX) XXX-XXXX
        if cleaned.startswith('+1-') and len(cleaned) >= 13:
            digits = ''.join(c for c in cleaned[3:] if c.isdigit())
            if len(digits) == 10:
                return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        
        # Return as-is if no standard formatting applies
        return cleaned

    def _format_duration(self, start_date: str, end_date: str = None) -> str:
        """Calculate and format employment duration.
        
        Args:
            start_date: Start date in YYYY-MM format
            end_date: End date in YYYY-MM format or None for current
            
        Returns:
            Formatted duration string
        """
        if not start_date:
            return ""
        
        try:
            start_year, start_month = map(int, start_date.split('-'))
            
            if end_date and end_date != "Present":
                end_year, end_month = map(int, end_date.split('-'))
            else:
                # Use current date for ongoing positions
                from datetime import datetime
                now = datetime.now()
                end_year, end_month = now.year, now.month
            
            # Calculate total months
            total_months = (end_year - start_year) * 12 + (end_month - start_month)
            
            if total_months < 1:
                return "< 1 mo"
            elif total_months < 12:
                return f"{total_months} mos"
            else:
                years = total_months // 12
                months = total_months % 12
                if months == 0:
                    return f"{years} yr{'s' if years != 1 else ''}"
                else:
                    return f"{years} yr{'s' if years != 1 else ''} {months} mo{'s' if months != 1 else ''}"
                    
        except (ValueError, IndexError):
            return ""

    def _create_skill_badge(self, skill) -> str:
        """Create GitHub badge for skill.
        
        Args:
            skill: Skill object with name and proficiency
            
        Returns:
            GitHub badge markdown
        """
        skill_name = skill.name
        proficiency = skill.proficiency.lower()
        
        # Map proficiency levels to colors
        color_map = {
            'expert': 'brightgreen',
            'advanced': 'green', 
            'intermediate': 'yellow',
            'beginner': 'orange'
        }
        
        color = color_map.get(proficiency, 'lightgrey')
        
        # URL encode skill name for badge
        skill_encoded = skill_name.replace(' ', '%20').replace('-', '--').replace('_', '__')
        proficiency_encoded = proficiency.replace(' ', '%20')
        
        return f"![{skill_name}](https://img.shields.io/badge/{skill_encoded}-{proficiency_encoded}-{color})"

    def _markdown_escape(self, text: str) -> str:
        """Escape markdown special characters.
        
        Args:
            text: Text to escape
            
        Returns:
            Escaped text safe for markdown
        """
        if not text:
            return ""
        
        # Escape common markdown characters
        escapes = {
            '*': r'\*',
            '_': r'\_',
            '`': r'\`',
            '[': r'\[',
            ']': r'\]',
            '(': r'\(',
            ')': r'\)',
            '#': r'\#',
            '+': r'\+',
            '-': r'\-',
            '.': r'\.',
            '!': r'\!',
            '|': r'\|'
        }
        
        result = text
        for char, escape in escapes.items():
            result = result.replace(char, escape)
        
        return result

    def _create_github_shield(self, label: str, message: str, color: str = "blue") -> str:
        """Create a GitHub shield badge.
        
        Args:
            label: Shield label
            message: Shield message
            color: Shield color
            
        Returns:
            GitHub shield markdown
        """
        label_encoded = label.replace(' ', '%20')
        message_encoded = message.replace(' ', '%20')
        
        return f"![{label}](https://img.shields.io/badge/{label_encoded}-{message_encoded}-{color})"