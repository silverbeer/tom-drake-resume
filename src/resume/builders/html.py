"""
HTML resume builder using Jinja2 templates.

This module generates professional HTML resumes with embedded CSS,
responsive design, and print-friendly formatting.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import jinja2

from .base import BaseBuilder
from .base import RenderError
from .base import TemplateError


class HtmlBuilder(BaseBuilder):
    """HTML resume builder using Jinja2 templates."""

    def __init__(self, resume_data, output_dir: Path, theme: str = "modern") -> None:
        """Initialize HTML builder with Jinja2 environment.
        
        Args:
            resume_data: Validated resume data model
            output_dir: Directory where output files will be created
            theme: Theme name for template selection
        """
        super().__init__(resume_data, output_dir, theme)
        
        # Set up Jinja2 environment
        html_template_dir = self.template_dir / "html"
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(html_template_dir),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters for HTML formatting
        self.env.filters.update({
            'format_date': self._format_date,
            'format_phone': self._format_phone,
            'format_duration': self._format_duration,
            'skill_level_class': self._skill_level_class,
            'format_url': self._format_url,
        })

    def build(self) -> Path:
        """Generate HTML resume using Jinja2 template.
        
        Returns:
            Path to the generated HTML file
            
        Raises:
            TemplateError: If template is missing or invalid
            RenderError: If rendering fails
        """
        try:
            # Load theme template
            template_path = f"themes/{self.theme}.html"
            template = self.env.get_template(template_path)
            
            # Prepare context data
            context = self.prepare_context()
            
            # Render HTML content
            html_content = template.render(**context)
            
            # Write to output file
            output_path = self.get_output_path()
            output_path.write_text(html_content, encoding='utf-8')
            
            return output_path
            
        except jinja2.TemplateNotFound as e:
            raise TemplateError(
                f"HTML template not found: {e}",
                template_path=self.template_dir / "html" / template_path,
                format_type="html"
            ) from e
        except jinja2.TemplateError as e:
            raise RenderError(
                f"HTML template rendering failed: {e}",
                format_type="html"
            ) from e
        except Exception as e:
            raise RenderError(
                f"HTML generation failed: {e}",
                format_type="html"
            ) from e

    def get_file_extension(self) -> str:
        """Return the file extension for HTML files."""
        return "html"

    def get_format_name(self) -> str:
        """Return format name for template directory."""
        return "html"

    def get_template_extension(self) -> str:
        """Return template file extension."""
        return "html"

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

    def _skill_level_class(self, proficiency: str) -> str:
        """Get CSS class for skill proficiency level.
        
        Args:
            proficiency: Proficiency level string
            
        Returns:
            CSS class name for styling
        """
        level_map = {
            'expert': 'skill-expert',
            'advanced': 'skill-advanced',
            'intermediate': 'skill-intermediate',
            'beginner': 'skill-beginner'
        }
        return level_map.get(proficiency.lower(), 'skill-basic')

    def _format_url(self, url: str) -> str:
        """Format URL for display (remove protocol for cleaner appearance).
        
        Args:
            url: Full URL string
            
        Returns:
            Display-friendly URL
        """
        if not url:
            return ""
        
        # Remove common protocols for cleaner display
        for protocol in ['https://', 'http://']:
            if url.startswith(protocol):
                return url[len(protocol):]
        
        return url