"""
JSON resume builder for structured data output.

This module generates clean JSON resumes perfect for APIs, integrations,
and machine-readable applications with enriched metadata.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .base import BaseBuilder
from .base import RenderError


class JsonBuilder(BaseBuilder):
    """JSON resume builder with Pydantic serialization."""

    def __init__(self, resume_data, output_dir: Path, theme: str = "modern") -> None:
        """Initialize JSON builder.
        
        Args:
            resume_data: Validated resume data model
            output_dir: Directory where output files will be created
            theme: Theme name (not used for JSON but kept for consistency)
        """
        super().__init__(resume_data, output_dir, theme)

    def build(self) -> Path:
        """Generate JSON resume using Pydantic serialization.
        
        Returns:
            Path to the generated JSON file
            
        Raises:
            RenderError: If JSON generation fails
        """
        try:
            # Serialize Pydantic model to dict
            resume_dict = self.resume_data.model_dump()
            
            # Add enriched build metadata
            resume_dict["build_info"] = {
                "build_date": datetime.now().isoformat(),
                "build_date_formatted": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
                "builder_version": "1.0.0",
                "format": "json",
                "theme": self.theme,
                "generator": "Tom Drake Resume System",
                "schema_version": "1.0",
                "api_compatible": True,
                "last_updated": self.resume_data.last_updated.isoformat(),
                "data_integrity": {
                    "sections_count": self._count_sections(),
                    "total_experience_entries": len(self.resume_data.experience),
                    "total_skills": self._count_total_skills(),
                    "has_certifications": bool(self.resume_data.certifications),
                    "has_projects": bool(self.resume_data.projects),
                    "has_awards": bool(self.resume_data.awards),
                    "has_publications": bool(self.resume_data.publications),
                    "has_languages": bool(self.resume_data.languages)
                }
            }
            
            # Add computed analytics
            resume_dict["analytics"] = {
                "career_timeline": self._build_career_timeline(),
                "skill_distribution": self._build_skill_distribution(),
                "experience_summary": {
                    "total_years": self.resume_data.total_experience_years,
                    "current_role": self.resume_data.current_role,
                    "career_progression": self._analyze_career_progression()
                }
            }
            
            # Write formatted JSON with proper encoding
            output_path = self.get_output_path()
            with output_path.open('w', encoding='utf-8') as f:
                json.dump(
                    resume_dict, 
                    f, 
                    indent=2, 
                    ensure_ascii=False, 
                    default=str,
                    sort_keys=False
                )
            
            return output_path
            
        except Exception as e:
            raise RenderError(
                f"JSON generation failed: {e}",
                format_type="json"
            ) from e

    def get_file_extension(self) -> str:
        """Return the file extension for JSON files."""
        return "json"

    def get_format_name(self) -> str:
        """Return format name for template directory."""
        return "json"

    def get_template_extension(self) -> str:
        """Return template file extension (not used for JSON)."""
        return "json"

    def _count_sections(self) -> int:
        """Count non-empty resume sections."""
        sections = [
            self.resume_data.personal_info,
            self.resume_data.professional_summary,
            self.resume_data.experience,
            self.resume_data.skills,
            self.resume_data.education,
        ]
        
        optional_sections = [
            self.resume_data.certifications,
            self.resume_data.projects,
            self.resume_data.awards,
            self.resume_data.publications,
            self.resume_data.languages,
        ]
        
        # Count mandatory sections (always present)
        count = len(sections)
        
        # Count optional sections that have content
        count += sum(1 for section in optional_sections if section)
        
        return count

    def _count_total_skills(self) -> int:
        """Count total skills across all categories."""
        if not self.resume_data.skills or not self.resume_data.skills.categories:
            return 0
        
        return sum(
            len(category.skills) 
            for category in self.resume_data.skills.categories.values()
        )

    def _build_career_timeline(self) -> list[dict]:
        """Build chronological career timeline."""
        timeline = []
        
        for exp in self.resume_data.experience:
            timeline.append({
                "company": exp.company,
                "role": exp.role,
                "start_date": exp.start_date,
                "end_date": exp.end_date,
                "duration_months": self._calculate_duration_months(exp.start_date, exp.end_date),
                "location": exp.location,
                "achievement_count": len(exp.achievements) if exp.achievements else 0
            })
        
        return timeline

    def _build_skill_distribution(self) -> dict:
        """Build skill proficiency distribution analysis."""
        if not self.resume_data.skills or not self.resume_data.skills.categories:
            return {}
        
        distribution = {}
        proficiency_counts = {"expert": 0, "advanced": 0, "intermediate": 0, "beginner": 0}
        
        for category_name, category in self.resume_data.skills.categories.items():
            distribution[category_name] = {
                "skill_count": len(category.skills),
                "skills": [
                    {
                        "name": skill.name,
                        "proficiency": skill.proficiency,
                        "years_experience": getattr(skill, 'years_experience', None)
                    }
                    for skill in category.skills
                ]
            }
            
            # Count proficiency levels
            for skill in category.skills:
                proficiency_level = skill.proficiency.lower()
                if proficiency_level in proficiency_counts:
                    proficiency_counts[proficiency_level] += 1
        
        distribution["proficiency_summary"] = proficiency_counts
        return distribution

    def _analyze_career_progression(self) -> list[str]:
        """Analyze career progression patterns."""
        if not self.resume_data.experience:
            return []
        
        progression = []
        
        # Sort by start date to analyze chronologically
        sorted_experience = sorted(
            self.resume_data.experience,
            key=lambda x: x.start_date
        )
        
        # Analyze role progression
        roles = [exp.role for exp in sorted_experience]
        companies = [exp.company for exp in sorted_experience]
        
        # Basic progression analysis
        if len(roles) > 1:
            progression.append(f"Career progression: {roles[0]} → {roles[-1]}")
        
        if len(set(companies)) < len(companies):
            progression.append("Has internal promotions or role changes")
        
        # Leadership progression indicators
        leadership_keywords = ['director', 'manager', 'lead', 'senior', 'principal', 'head', 'vp', 'chief']
        current_role = roles[-1].lower()
        
        if any(keyword in current_role for keyword in leadership_keywords):
            progression.append("Currently in leadership role")
        
        return progression

    def _calculate_duration_months(self, start_date: str, end_date: str = None) -> int:
        """Calculate employment duration in months."""
        if not start_date:
            return 0
        
        try:
            start_year, start_month = map(int, start_date.split('-'))
            
            if end_date and end_date != "Present":
                end_year, end_month = map(int, end_date.split('-'))
            else:
                # Use current date for ongoing positions
                now = datetime.now()
                end_year, end_month = now.year, now.month
            
            return (end_year - start_year) * 12 + (end_month - start_month)
            
        except (ValueError, IndexError):
            return 0