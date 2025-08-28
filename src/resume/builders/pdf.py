"""
PDF resume builder using ReportLab for professional document generation.

This module generates ATS-friendly PDFs with precise typography, professional
formatting, and optimal layout for both human readers and applicant tracking systems.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from reportlab.platypus import TableStyle

from .base import BaseBuilder
from .base import RenderError


class PdfBuilder(BaseBuilder):
    """PDF resume builder using ReportLab for professional document generation."""

    def __init__(self, resume_data, output_dir: Path, theme: str = "modern") -> None:
        """Initialize PDF builder with ReportLab.
        
        Args:
            resume_data: Validated resume data model
            output_dir: Directory where output files will be created
            theme: Theme name (used for styling variations)
        """
        super().__init__(resume_data, output_dir, theme)
        
        # Initialize ReportLab styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def build(self) -> Path:
        """Generate PDF resume using ReportLab.
        
        Returns:
            Path to the generated PDF file
            
        Raises:
            RenderError: If PDF generation fails
        """
        try:
            output_path = self.get_output_path()
            
            # Create PDF document with professional settings
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=letter,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch,
                title=f"{self.resume_data.personal_info.name} - Resume",
                author=self.resume_data.personal_info.name,
                subject="Professional Resume",
                creator="AI-Powered Resume System"
            )
            
            # Build document content
            story = []
            
            # Add header section
            self._add_header(story)
            
            # Add professional summary
            self._add_professional_summary(story)
            
            # Add experience section
            self._add_experience(story)
            
            # Add skills section
            self._add_skills(story)
            
            # Add education section
            self._add_education(story)
            
            # Add optional sections
            self._add_certifications(story)
            self._add_projects(story)
            self._add_awards(story)
            
            # Add footer
            self._add_footer(story)
            
            # Generate PDF
            doc.build(story)
            
            return output_path
            
        except Exception as e:
            raise RenderError(
                f"PDF generation failed: {e}",
                format_type="pdf"
            ) from e

    def get_file_extension(self) -> str:
        """Return the file extension for PDF files."""
        return "pdf"

    def get_format_name(self) -> str:
        """Return format name for template directory."""
        return "pdf"

    def get_template_extension(self) -> str:
        """Return template file extension."""
        return "pdf"

    def _setup_custom_styles(self) -> None:
        """Set up custom paragraph styles for professional formatting."""
        # Header name style
        self.styles.add(ParagraphStyle(
            name='HeaderName',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=4,
            alignment=TA_CENTER,
            textColor=colors.black,
            fontName='Helvetica-Bold'
        ))
        
        # Header title style
        self.styles.add(ParagraphStyle(
            name='HeaderTitle',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=8,
            alignment=TA_CENTER,
            textColor=colors.grey,
            fontName='Helvetica'
        ))
        
        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=16,
            alignment=TA_CENTER,
            textColor=colors.black,
            fontName='Helvetica'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=16,
            textColor=colors.black,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderColor=colors.black,
            borderPadding=0
        ))
        
        # Job title style
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=2,
            fontName='Helvetica-Bold',
            textColor=colors.black
        ))
        
        # Company style
        self.styles.add(ParagraphStyle(
            name='Company',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=2,
            fontName='Helvetica-Bold',
            textColor=colors.darkblue
        ))
        
        # Date range style
        self.styles.add(ParagraphStyle(
            name='DateRange',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName='Helvetica',
            textColor=colors.grey,
            alignment=TA_RIGHT
        ))
        
        # Achievement bullet style
        self.styles.add(ParagraphStyle(
            name='Achievement',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            leftIndent=12,
            fontName='Helvetica',
            textColor=colors.black
        ))
        
        # Skills category style
        self.styles.add(ParagraphStyle(
            name='SkillsCategory',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            fontName='Helvetica-Bold',
            textColor=colors.black
        ))
        
        # Skills list style
        self.styles.add(ParagraphStyle(
            name='SkillsList',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            fontName='Helvetica',
            textColor=colors.black
        ))

    def _add_header(self, story: list) -> None:
        """Add header section with name, title, and contact info."""
        personal_info = self.resume_data.personal_info
        
        # Name
        story.append(Paragraph(personal_info.name, self.styles['HeaderName']))
        
        # Title
        story.append(Paragraph(personal_info.title, self.styles['HeaderTitle']))
        
        # Contact information
        contact_parts = []
        
        # Email
        contact_parts.append(personal_info.email)
        
        # Phone
        if personal_info.phone:
            contact_parts.append(self._format_phone(personal_info.phone))
        
        # Location
        location = personal_info.location
        location_str = f"{location.city}, {location.state}"
        if location.remote_friendly:
            location_str += " • Remote Friendly"
        contact_parts.append(location_str)
        
        # Links
        if personal_info.links:
            links = personal_info.links
            link_parts = []
            if links.linkedin:
                link_parts.append(f'<a href="{links.linkedin}" color="blue">LinkedIn</a>')
            if links.github:
                link_parts.append(f'<a href="{links.github}" color="blue">GitHub</a>')
            if links.website:
                link_parts.append(f'<a href="{links.website}" color="blue">Website</a>')
            
            if link_parts:
                contact_parts.append(" • ".join(link_parts))
        
        contact_text = " • ".join(contact_parts)
        story.append(Paragraph(contact_text, self.styles['ContactInfo']))

    def _add_professional_summary(self, story: list) -> None:
        """Add professional summary section."""
        summary = self.resume_data.professional_summary
        
        story.append(Paragraph("PROFESSIONAL SUMMARY", self.styles['SectionHeader']))
        story.append(Paragraph(summary.overview, self.styles['Normal']))
        
        if summary.key_strengths:
            story.append(Spacer(1, 6))
            story.append(Paragraph("<b>Key Strengths:</b>", self.styles['Normal']))
            
            for strength in summary.key_strengths:
                story.append(Paragraph(f"• {strength}", self.styles['Achievement']))

    def _add_experience(self, story: list) -> None:
        """Add professional experience section."""
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", self.styles['SectionHeader']))
        
        for exp in self.resume_data.experience:
            # Create experience header table
            exp_data = [
                [
                    Paragraph(f"<b>{exp.role}</b>", self.styles['JobTitle']),
                    Paragraph(self._format_date_range(exp.start_date, exp.end_date), self.styles['DateRange'])
                ],
                [
                    Paragraph(exp.company, self.styles['Company']),
                    Paragraph(exp.location or "", self.styles['DateRange'])
                ]
            ]
            
            # Create table for experience header
            exp_table = Table(exp_data, colWidths=[4.5*inch, 2*inch])
            exp_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ]))
            
            story.append(exp_table)
            
            # Add company description if available
            if exp.company_description:
                story.append(Paragraph(f"<i>{exp.company_description}</i>", self.styles['Normal']))
                story.append(Spacer(1, 4))
            
            # Add achievements
            if exp.achievements:
                for achievement in exp.achievements:
                    # Format achievement with metrics
                    achievement_text = achievement.description
                    if achievement.metrics:
                        metrics_text = []
                        for metric in achievement.metrics:
                            metrics_text.append(f"{metric.value}{metric.unit}")
                        achievement_text += f" ({', '.join(metrics_text)})"
                    
                    story.append(Paragraph(f"• {achievement_text}", self.styles['Achievement']))
            
            story.append(Spacer(1, 12))

    def _add_skills(self, story: list) -> None:
        """Add technical skills section."""
        if not self.resume_data.skills or not self.resume_data.skills.categories:
            return
        
        story.append(Paragraph("TECHNICAL SKILLS", self.styles['SectionHeader']))
        
        for category_name, category in self.resume_data.skills.categories.items():
            # Category name
            story.append(Paragraph(f"<b>{category.display_name}:</b>", self.styles['SkillsCategory']))
            
            # Skills list
            skill_texts = []
            for skill in category.skills:
                skill_text = skill.name
                if skill.proficiency in ['expert', 'advanced']:
                    skill_text = f"<b>{skill_text}</b>"
                skill_texts.append(skill_text)
            
            skills_paragraph = " • ".join(skill_texts)
            story.append(Paragraph(skills_paragraph, self.styles['SkillsList']))

    def _add_education(self, story: list) -> None:
        """Add education section."""
        if not self.resume_data.education:
            return
            
        story.append(Paragraph("EDUCATION", self.styles['SectionHeader']))
        
        for edu in self.resume_data.education:
            # Education header
            degree_text = edu.degree
            if edu.field_of_study:
                degree_text += f" in {edu.field_of_study}"
                
            edu_data = [
                [
                    Paragraph(f"<b>{degree_text}</b>", self.styles['JobTitle']),
                    Paragraph(str(edu.graduation_date), self.styles['DateRange'])
                ],
                [
                    Paragraph(edu.institution, self.styles['Company']),
                    Paragraph("", self.styles['DateRange'])  # No location in model
                ]
            ]
            
            edu_table = Table(edu_data, colWidths=[4.5*inch, 2*inch])
            edu_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            story.append(edu_table)
            
            # Add additional details
            details = []
            if edu.gpa:
                details.append(f"GPA: {edu.gpa}")
            if edu.honors:
                details.append(f"Honors: {', '.join(edu.honors)}")
            
            if details:
                story.append(Paragraph(" • ".join(details), self.styles['Achievement']))

    def _add_certifications(self, story: list) -> None:
        """Add certifications section."""
        if not self.resume_data.certifications:
            return
            
        story.append(Paragraph("CERTIFICATIONS", self.styles['SectionHeader']))
        
        for cert in self.resume_data.certifications:
            cert_text = f"<b>{cert.name}</b> - {cert.issuer}"
            if cert.issue_date:
                cert_text += f" ({self._format_date(cert.issue_date)})"
            story.append(Paragraph(cert_text, self.styles['Normal']))
            story.append(Spacer(1, 4))

    def _add_projects(self, story: list) -> None:
        """Add projects section."""
        if not self.resume_data.projects:
            return
            
        story.append(Paragraph("FEATURED PROJECTS", self.styles['SectionHeader']))
        
        for project in self.resume_data.projects:
            story.append(Paragraph(f"<b>{project.name}</b>", self.styles['JobTitle']))
            story.append(Paragraph(project.description, self.styles['Normal']))
            
            if project.technologies:
                tech_text = f"<b>Technologies:</b> {', '.join(project.technologies)}"
                story.append(Paragraph(tech_text, self.styles['Achievement']))
            
            story.append(Spacer(1, 8))

    def _add_awards(self, story: list) -> None:
        """Add awards section."""
        if not self.resume_data.awards:
            return
            
        story.append(Paragraph("AWARDS & RECOGNITION", self.styles['SectionHeader']))
        
        for award in self.resume_data.awards:
            award_text = f"<b>{award.title}</b> - {award.issuer}"
            if award.date:
                award_text += f" ({self._format_date(award.date)})"
            story.append(Paragraph(award_text, self.styles['Normal']))
            story.append(Spacer(1, 4))

    def _add_footer(self, story: list) -> None:
        """Add footer with generation timestamp."""
        story.append(Spacer(1, 20))
        
        footer_text = (
            f"<i>Generated by AI-Powered Resume System • "
            f"Built: {datetime.now().strftime('%B %d, %Y')}</i>"
        )
        
        footer_style = ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey,
            fontName='Helvetica'
        )
        
        story.append(Paragraph(footer_text, footer_style))

    def _format_phone(self, phone: str) -> str:
        """Format phone number for display."""
        if not phone:
            return ""
        
        # Clean the phone number
        cleaned = phone.strip()
        
        # If it starts with +1-, format as (XXX) XXX-XXXX
        if cleaned.startswith('+1-') and len(cleaned) >= 13:
            digits = ''.join(c for c in cleaned[3:] if c.isdigit())
            if len(digits) == 10:
                return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        
        return cleaned

    def _format_date(self, date_str: str) -> str:
        """Format date string for display."""
        if not date_str:
            return "Present"
        
        try:
            if len(date_str) == 7 and '-' in date_str:
                year, month = date_str.split('-')
                month_names = [
                    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                ]
                month_idx = int(month) - 1
                if 0 <= month_idx < 12:
                    return f"{month_names[month_idx]} {year}"
            
            if len(date_str) == 4:
                return date_str
                
            return date_str
            
        except (ValueError, IndexError):
            return date_str

    def _format_date_range(self, start_date: str, end_date: str = None) -> str:
        """Format date range for experience."""
        start_formatted = self._format_date(start_date)
        end_formatted = self._format_date(end_date) if end_date else "Present"
        return f"{start_formatted} - {end_formatted}"