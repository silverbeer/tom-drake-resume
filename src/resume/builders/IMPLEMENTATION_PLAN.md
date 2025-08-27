# Resume Builders Implementation Plan

## Overview

This document provides a comprehensive implementation plan for the resume builders system - the core component that transforms structured resume data into professional, multi-format outputs (HTML, PDF, JSON, Markdown).

## 🎯 Project Goals

- **Multi-Format Output**: Generate professional resumes in 4+ formats from single data source
- **Theme System**: Support multiple visual themes and layouts
- **Enterprise Quality**: Production-ready code with 95%+ test coverage
- **Performance**: Build complete resume suite in under 2 seconds
- **Extensibility**: Easy to add new formats and themes

## 🏗️ Architecture Overview

### Base Builder Framework

```python
# src/resume/builders/base.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional
from ..models import ResumeData
from ..config import Config

class BaseBuilder(ABC):
    """Abstract base class for all resume builders."""
    
    def __init__(self, config: Config, theme: str = "modern"):
        self.config = config
        self.theme = theme
        self.template_dir = config.templates_dir
    
    @abstractmethod
    def build(self, resume_data: ResumeData, output_path: Path) -> Path:
        """Build resume and return output file path."""
        pass
    
    @abstractmethod  
    def get_file_extension(self) -> str:
        """Return the file extension for this format."""
        pass
    
    def validate_template(self, template_name: str) -> Path:
        """Validate template exists and return path."""
        template_path = self.template_dir / self.get_format_name() / f"{template_name}.{self.get_template_extension()}"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        return template_path
    
    def prepare_context(self, resume_data: ResumeData) -> Dict[str, Any]:
        """Prepare template context from resume data."""
        return {
            "personal_info": resume_data.personal_info,
            "professional_summary": resume_data.professional_summary,
            "experience": resume_data.experience,
            "skills": resume_data.skills,
            "education": resume_data.education,
            "certifications": resume_data.certifications or [],
            "projects": resume_data.projects or [],
            "awards": resume_data.awards or [],
            "publications": resume_data.publications or [],
            "languages": resume_data.languages or [],
            "metadata": {
                "build_date": resume_data.last_updated,
                "version": resume_data.version,
                "theme": self.theme,
                "format": self.get_format_name()
            }
        }
    
    @abstractmethod
    def get_format_name(self) -> str:
        """Return format name for template directory."""
        pass
    
    @abstractmethod
    def get_template_extension(self) -> str:
        """Return template file extension."""
        pass

class BuilderError(Exception):
    """Base exception for builder errors."""
    pass

class TemplateError(BuilderError):
    """Template-related errors."""
    pass

class RenderError(BuilderError):
    """Rendering/generation errors."""
    pass
```

### Builder Factory Pattern

```python
# src/resume/builders/__init__.py
from typing import Dict, Type
from .base import BaseBuilder
from .html import HtmlBuilder
from .pdf import PdfBuilder
from .json_builder import JsonBuilder
from .markdown import MarkdownBuilder

class BuilderFactory:
    """Factory for creating resume builders."""
    
    _builders: Dict[str, Type[BaseBuilder]] = {
        'html': HtmlBuilder,
        'pdf': PdfBuilder,
        'json': JsonBuilder,
        'markdown': MarkdownBuilder
    }
    
    @classmethod
    def create_builder(cls, format_type: str, config: Config, theme: str = "modern") -> BaseBuilder:
        """Create a builder instance for the specified format."""
        if format_type not in cls._builders:
            available = ', '.join(cls._builders.keys())
            raise ValueError(f"Unknown format '{format_type}'. Available: {available}")
        
        builder_class = cls._builders[format_type]
        return builder_class(config, theme)
    
    @classmethod
    def get_available_formats(cls) -> List[str]:
        """Get list of available output formats."""
        return list(cls._builders.keys())
    
    @classmethod
    def register_builder(cls, format_type: str, builder_class: Type[BaseBuilder]) -> None:
        """Register a custom builder."""
        cls._builders[format_type] = builder_class

__all__ = [
    "BaseBuilder",
    "BuilderFactory", 
    "BuilderError",
    "TemplateError",
    "RenderError",
    "HtmlBuilder",
    "PdfBuilder", 
    "JsonBuilder",
    "MarkdownBuilder"
]
```

## 📋 Individual Builder Specifications

### 1. HTML Builder (`html.py`)

**Purpose**: Generate responsive HTML resumes with embedded CSS

**Features**:
- Jinja2 templating engine
- Embedded CSS for portability
- Multiple themes (modern, classic, minimal)
- Print-friendly styles for PDF conversion
- Responsive design for all devices
- Accessibility (WCAG 2.1 compliant)

**Implementation**:
```python
# src/resume/builders/html.py
from pathlib import Path
from typing import Dict, Any
import jinja2
from .base import BaseBuilder, TemplateError, RenderError

class HtmlBuilder(BaseBuilder):
    """HTML resume builder using Jinja2 templates."""
    
    def __init__(self, config: Config, theme: str = "modern"):
        super().__init__(config, theme)
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir / "html"),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
        self.env.filters.update({
            'format_date': self._format_date,
            'format_phone': self._format_phone,
            'skill_level_class': self._skill_level_class
        })
    
    def build(self, resume_data: ResumeData, output_path: Path) -> Path:
        """Generate HTML resume."""
        try:
            template = self.env.get_template(f"themes/{self.theme}.html")
            context = self.prepare_context(resume_data)
            html_content = template.render(**context)
            
            output_path.write_text(html_content, encoding='utf-8')
            return output_path
            
        except jinja2.TemplateNotFound as e:
            raise TemplateError(f"HTML template not found: {e}")
        except Exception as e:
            raise RenderError(f"HTML rendering failed: {e}")
    
    def get_file_extension(self) -> str:
        return "html"
    
    def get_format_name(self) -> str:
        return "html"
        
    def get_template_extension(self) -> str:
        return "html"
    
    def _format_date(self, date_str: str) -> str:
        """Format date for display."""
        # Implementation for date formatting
        pass
    
    def _format_phone(self, phone: str) -> str:
        """Format phone number for display."""
        # Implementation for phone formatting
        pass
        
    def _skill_level_class(self, proficiency: str) -> str:
        """Get CSS class for skill proficiency level."""
        level_map = {
            'expert': 'skill-expert',
            'advanced': 'skill-advanced', 
            'intermediate': 'skill-intermediate',
            'beginner': 'skill-beginner'
        }
        return level_map.get(proficiency.lower(), 'skill-basic')
```

**Templates Required**:
- `templates/html/themes/modern.html` - Modern, clean design
- `templates/html/themes/classic.html` - Traditional, conservative layout
- `templates/html/themes/minimal.html` - Minimal, text-focused design

### 2. PDF Builder (`pdf.py`)

**Purpose**: Generate professional PDF resumes

**Strategy**: 
- Primary: HTML → WeasyPrint → PDF (best quality)
- Fallback: Direct ReportLab generation (reliability)

**Features**:
- Professional typography
- Configurable page layouts (A4, US Letter)
- Embedded fonts for consistency
- Optimized for ATS scanning
- Print-ready output

**Implementation**:
```python
# src/resume/builders/pdf.py
from pathlib import Path
import tempfile
from typing import Optional
from .base import BaseBuilder, RenderError
from .html import HtmlBuilder

try:
    import weasyprint
    HAS_WEASYPRINT = True
except ImportError:
    HAS_WEASYPRINT = False

try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

class PdfBuilder(BaseBuilder):
    """PDF resume builder with multiple generation strategies."""
    
    def build(self, resume_data: ResumeData, output_path: Path) -> Path:
        """Generate PDF resume."""
        if HAS_WEASYPRINT:
            return self._build_with_weasyprint(resume_data, output_path)
        elif HAS_REPORTLAB:
            return self._build_with_reportlab(resume_data, output_path)
        else:
            raise RenderError("No PDF generation library available. Install weasyprint or reportlab.")
    
    def _build_with_weasyprint(self, resume_data: ResumeData, output_path: Path) -> Path:
        """Generate PDF using WeasyPrint (HTML → PDF)."""
        try:
            # Generate HTML first
            html_builder = HtmlBuilder(self.config, self.theme)
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                html_path = Path(f.name)
                
            html_builder.build(resume_data, html_path)
            
            # Convert HTML to PDF
            weasyprint.HTML(filename=str(html_path)).write_pdf(str(output_path))
            
            # Cleanup
            html_path.unlink()
            
            return output_path
            
        except Exception as e:
            raise RenderError(f"WeasyPrint PDF generation failed: {e}")
    
    def _build_with_reportlab(self, resume_data: ResumeData, output_path: Path) -> Path:
        """Generate PDF using ReportLab (direct generation)."""
        # Implementation for direct PDF generation
        pass
    
    def get_file_extension(self) -> str:
        return "pdf"
    
    def get_format_name(self) -> str:
        return "pdf"
        
    def get_template_extension(self) -> str:
        return "html"  # Uses HTML templates for WeasyPrint
```

### 3. JSON Builder (`json_builder.py`)

**Purpose**: Generate structured JSON for API integrations

**Features**:
- Clean, API-friendly format
- Schema validation
- Metadata enrichment
- Suitable for integrations
- Includes build information

**Implementation**:
```python
# src/resume/builders/json_builder.py
import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from .base import BaseBuilder, RenderError

class JsonBuilder(BaseBuilder):
    """JSON resume builder for API integrations."""
    
    def build(self, resume_data: ResumeData, output_path: Path) -> Path:
        """Generate JSON resume."""
        try:
            # Convert Pydantic model to dict
            resume_dict = resume_data.model_dump()
            
            # Enrich with build metadata
            build_info = {
                "build_date": datetime.now().isoformat(),
                "builder_version": "1.0.0",
                "format": "json",
                "theme": self.theme,
                "generator": "Tom Drake Resume System"
            }
            
            resume_dict["build_info"] = build_info
            
            # Write formatted JSON
            with output_path.open('w', encoding='utf-8') as f:
                json.dump(resume_dict, f, indent=2, ensure_ascii=False, default=str)
            
            return output_path
            
        except Exception as e:
            raise RenderError(f"JSON generation failed: {e}")
    
    def get_file_extension(self) -> str:
        return "json"
    
    def get_format_name(self) -> str:
        return "json"
        
    def get_template_extension(self) -> str:
        return "json"
```

### 4. Markdown Builder (`markdown.py`)

**Purpose**: Generate clean Markdown for GitHub/documentation

**Features**:
- GitHub-flavored markdown
- Badge integration for skills
- Clean, readable format
- Suitable for README files
- Link optimization

**Implementation**:
```python
# src/resume/builders/markdown.py
from pathlib import Path
from typing import List
import jinja2
from .base import BaseBuilder, TemplateError, RenderError

class MarkdownBuilder(BaseBuilder):
    """Markdown resume builder for GitHub and documentation."""
    
    def __init__(self, config: Config, theme: str = "github"):
        super().__init__(config, theme)
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir / "markdown"),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.env.filters.update({
            'skill_badge': self._create_skill_badge,
            'format_duration': self._format_duration
        })
    
    def build(self, resume_data: ResumeData, output_path: Path) -> Path:
        """Generate Markdown resume."""
        try:
            template = self.env.get_template(f"{self.theme}.md")
            context = self.prepare_context(resume_data)
            markdown_content = template.render(**context)
            
            output_path.write_text(markdown_content, encoding='utf-8')
            return output_path
            
        except jinja2.TemplateNotFound as e:
            raise TemplateError(f"Markdown template not found: {e}")
        except Exception as e:
            raise RenderError(f"Markdown rendering failed: {e}")
    
    def _create_skill_badge(self, skill_name: str, proficiency: str) -> str:
        """Create GitHub badge for skill."""
        color_map = {
            'expert': 'brightgreen',
            'advanced': 'green', 
            'intermediate': 'yellow',
            'beginner': 'orange'
        }
        color = color_map.get(proficiency.lower(), 'lightgrey')
        return f"![{skill_name}](https://img.shields.io/badge/{skill_name}-{proficiency}-{color})"
    
    def _format_duration(self, start_date: str, end_date: str = None) -> str:
        """Format date duration for display."""
        # Implementation for duration formatting
        pass
    
    def get_file_extension(self) -> str:
        return "md"
    
    def get_format_name(self) -> str:
        return "markdown"
        
    def get_template_extension(self) -> str:
        return "md"
```

## 📁 Template System Design

### Directory Structure
```
templates/
├── html/
│   ├── themes/
│   │   ├── modern.html         # Clean, contemporary design
│   │   ├── classic.html        # Traditional, conservative layout
│   │   ├── minimal.html        # Text-focused, simple design
│   │   └── creative.html       # Bold, design-forward layout
│   ├── partials/
│   │   ├── header.html         # Personal info section
│   │   ├── summary.html        # Professional summary
│   │   ├── experience.html     # Work experience
│   │   ├── skills.html         # Skills section
│   │   ├── education.html      # Education section
│   │   └── footer.html         # Contact/metadata
│   └── assets/
│       ├── css/
│       │   ├── modern.css      # Modern theme styles
│       │   ├── classic.css     # Classic theme styles
│       │   └── print.css       # Print/PDF optimization
│       ├── js/
│       │   └── interactions.js # Optional interactivity
│       └── images/
│           └── icons/          # Skill/social icons
├── markdown/
│   ├── github.md               # GitHub-optimized template
│   ├── gitlab.md               # GitLab-optimized template
│   └── bitbucket.md            # Bitbucket-optimized template
├── latex/                      # Future LaTeX support
│   ├── professional.tex
│   └── academic.tex
└── json/
    └── schema.json             # Output validation schema
```

### Theme System Features

**HTML Themes**:
- **Modern**: Clean lines, sans-serif fonts, subtle colors, mobile-first
- **Classic**: Traditional layout, serif fonts, formal styling
- **Minimal**: Maximum whitespace, typography-focused, distraction-free
- **Creative**: Bold colors, unique layout, design-portfolio friendly

**Common Features**:
- Responsive design (mobile, tablet, desktop)
- Print optimization for PDF generation
- Accessibility compliance (WCAG 2.1 AA)
- Fast loading with embedded assets
- Cross-browser compatibility

## 🛠️ Implementation Steps

### Phase 1: Foundation (Day 1)
1. **Create Base Builder Framework**
   - [ ] Implement `BaseBuilder` abstract class
   - [ ] Create `BuilderFactory` with registration system
   - [ ] Add comprehensive error handling
   - [ ] Create package `__init__.py` with exports

2. **Set Up Template Infrastructure**
   - [ ] Create template directory structure
   - [ ] Add basic HTML template (modern theme)
   - [ ] Create CSS framework with responsive design
   - [ ] Add Jinja2 filters and utilities

### Phase 2: Core Builders (Day 2)
3. **Implement HTML Builder**
   - [ ] Create `HtmlBuilder` class with Jinja2 integration
   - [ ] Implement template rendering pipeline
   - [ ] Add theme switching capability
   - [ ] Create responsive CSS framework
   - [ ] Add print stylesheet for PDF conversion

4. **Implement JSON Builder**
   - [ ] Create `JsonBuilder` class
   - [ ] Implement clean JSON output format
   - [ ] Add build metadata enrichment
   - [ ] Create JSON schema for validation

### Phase 3: Extended Formats (Day 3)
5. **Implement Markdown Builder**
   - [ ] Create `MarkdownBuilder` class
   - [ ] Design GitHub-optimized template
   - [ ] Add skill badge generation
   - [ ] Implement link optimization

6. **Implement PDF Builder**
   - [ ] Create `PdfBuilder` class with WeasyPrint integration
   - [ ] Add ReportLab fallback option
   - [ ] Implement professional typography
   - [ ] Add page layout configuration

### Phase 4: Integration & Testing (Day 4)
7. **CLI Integration**
   - [ ] Update `cli.py` to use `BuilderFactory`
   - [ ] Implement theme selection
   - [ ] Add progress indicators with Rich
   - [ ] Enhance error messaging

8. **Comprehensive Testing**
   - [ ] Unit tests for each builder (95% coverage)
   - [ ] Integration tests for full pipeline
   - [ ] Template validation tests
   - [ ] Performance benchmarking

## 🧪 Testing Strategy

### Unit Tests Structure
```
tests/
├── test_builders/
│   ├── __init__.py
│   ├── test_base.py            # BaseBuilder tests
│   ├── test_html.py            # HTML builder tests
│   ├── test_pdf.py             # PDF builder tests
│   ├── test_json.py            # JSON builder tests
│   ├── test_markdown.py        # Markdown builder tests
│   ├── test_factory.py         # BuilderFactory tests
│   └── fixtures/
│       ├── sample_resume.yml   # Test resume data
│       ├── expected_outputs/   # Expected output files
│       └── templates/          # Test templates
└── integration/
    ├── test_full_build.py      # End-to-end build tests
    ├── test_theme_switching.py # Theme system tests
    └── test_error_handling.py  # Error scenario tests
```

### Test Coverage Goals
- **BaseBuilder**: 100% line and branch coverage
- **Individual Builders**: 95%+ coverage each
- **BuilderFactory**: 100% coverage
- **Template Rendering**: 90%+ coverage
- **Error Scenarios**: 100% coverage

### Integration Tests
- **Full Build Pipeline**: Test complete resume generation
- **Multi-Format Consistency**: Verify content consistency across formats
- **Theme System**: Test theme switching and customization
- **Performance**: Benchmark build times and memory usage
- **Error Recovery**: Test graceful degradation and error reporting

### Test Data Management
- **Mock Resume Data**: Comprehensive test resume with all sections
- **Edge Cases**: Missing sections, empty data, invalid formats
- **Real-World Data**: Sanitized version of actual resume data
- **Performance Data**: Large resume for stress testing

## 📊 Success Metrics

### Functional Requirements
- ✅ **Multi-Format Support**: Generate HTML, PDF, JSON, and Markdown
- ✅ **Theme System**: Support 3+ visual themes
- ✅ **Template Engine**: Jinja2-based with custom filters
- ✅ **Error Handling**: Graceful degradation with meaningful messages
- ✅ **CLI Integration**: Seamless integration with existing CLI

### Quality Requirements  
- ✅ **Test Coverage**: 95%+ overall, 100% for critical paths
- ✅ **Type Safety**: Full mypy compliance with strict mode
- ✅ **Code Quality**: Pass all Ruff/Black/isort checks
- ✅ **Documentation**: Comprehensive docstrings and examples
- ✅ **Performance**: Complete build in < 2 seconds

### User Experience Requirements
- ✅ **Professional Output**: Production-ready resume quality
- ✅ **Responsive Design**: Works on all devices and screen sizes
- ✅ **Accessibility**: WCAG 2.1 AA compliance for HTML output
- ✅ **Print Friendly**: Optimized PDF generation
- ✅ **Easy Theming**: Simple theme switching mechanism

## 🚀 Future Enhancements

### Phase 2 Considerations
- **LaTeX Support**: Academic resume generation
- **Custom Themes**: User-defined CSS themes
- **Internationalization**: Multi-language support
- **Advanced PDF**: Custom layouts and typography
- **Web Components**: Interactive HTML elements

### Integration Points
- **AI Enhancement**: Template optimization suggestions
- **Analytics**: Build metrics and optimization insights
- **Version Control**: Template versioning and rollback
- **Cloud Storage**: Template sharing and collaboration
- **API Access**: REST API for programmatic generation

## 📝 Notes for Implementation

### Dependencies to Add
```toml
# Additional dependencies for builders
dependencies = [
    # ... existing deps ...
    "jinja2 >= 3.1.2",        # HTML templating
    "weasyprint >= 60.2",     # PDF generation (primary)
    "reportlab >= 4.0.7",     # PDF generation (fallback)
    "markdown >= 3.5.1",      # Markdown processing
]
```

### Configuration Updates
The `Config` class may need updates for:
- Theme selection options
- Template directory paths
- PDF generation settings
- Output quality parameters

### Error Handling Philosophy
- **Fail Fast**: Catch errors early with clear messages
- **Graceful Degradation**: Continue with warnings when possible
- **User-Friendly**: Translate technical errors to actionable messages
- **Logging**: Comprehensive logging for debugging

This implementation plan provides a solid foundation for the multi-format resume generation system while maintaining the high standards established in this project.