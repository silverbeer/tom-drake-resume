# Phase 2 Implementation Plan: Core Resume Builders

## 🎯 **Project Objective**

Implement the four core resume format builders (HTML, JSON, Markdown, PDF) to make `uv run resume build all` fully functional, enabling professional multi-format resume generation and local formatting preview.

**Current State**: Phase 1 foundation complete with base builder framework and templates
**Target State**: Working CLI commands that generate professional resumes in 4 formats

## 🏗️ **Architecture Analysis**

### **Current Issue: Constructor Mismatch**
The existing CLI expects builders with this signature:
```python
# CLI in src/resume/cli.py (lines 266-283)
builder = HtmlBuilder(result.data, output_dir)  # ❌ Constructor mismatch
```

But the current `BaseBuilder` expects:
```python
# Current BaseBuilder.__init__
def __init__(self, config: Config, theme: str = "modern"):  # ❌ Different signature
```

### **Solution: Standardize to CLI Approach**
Update `BaseBuilder` to match CLI expectations:
```python
class BaseBuilder(ABC):
    def __init__(self, resume_data: ResumeData, output_dir: Path, theme: str = "modern"):
        self.resume_data = resume_data
        self.output_dir = output_dir
        self.theme = theme
        self.output_dir.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
```

## 📋 **Implementation Roadmap**

### **Phase 2A: Foundation & HTML Builder (Priority 1)**
**Timeline**: Day 1 (4-6 hours)
**Goal**: Get visual feedback on resume formatting

1. **Fix Base Builder Architecture**
   - Update constructor signature to match CLI
   - Add output directory creation
   - Standardize abstract method signatures

2. **Implement HTML Builder**
   - Create `src/resume/builders/html.py`
   - Use existing `templates/html/themes/modern.html`
   - Implement Jinja2 rendering pipeline
   - Generate `resume.html` with embedded CSS

3. **Update Builder Factory**
   - Fix imports in `src/resume/builders/__init__.py`
   - Ensure proper builder registration

### **Phase 2B: Structured Data Builders (Priority 2)**
**Timeline**: Day 2 (3-4 hours)
**Goal**: Generate machine-readable formats

4. **Implement JSON Builder**
   - Create `src/resume/builders/json_builder.py`
   - Direct Pydantic model serialization
   - Add build metadata enrichment
   - Generate `resume.json`

5. **Implement Markdown Builder**
   - Create `src/resume/builders/markdown.py`
   - Create `templates/markdown/github.md` template
   - Add GitHub skill badge generation
   - Generate `resume.md`

### **Phase 2C: PDF & Final Integration (Priority 3)**
**Timeline**: Day 3 (2-3 hours)
**Goal**: Print-ready professional output

6. **Implement PDF Builder**
   - Create `src/resume/builders/pdf.py`
   - WeasyPrint HTML-to-PDF conversion
   - Professional typography settings
   - Generate `resume.pdf`

7. **Integration & Testing**
   - Test all formats with CLI
   - Verify error handling
   - Performance optimization

## 🔧 **Detailed Implementation Specifications**

### **Task 1: Base Builder Update**
**File**: `src/resume/builders/base.py`

**Required Changes**:
```python
class BaseBuilder(ABC):
    def __init__(self, resume_data: ResumeData, output_dir: Path, theme: str = "modern"):
        self.resume_data = resume_data
        self.output_dir = Path(output_dir)
        self.theme = theme
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def build(self) -> Path:
        """Build resume and return output file path."""
        pass
    
    def get_output_filename(self) -> str:
        """Generate output filename based on format."""
        return f"resume.{self.get_file_extension()}"
    
    def prepare_context(self) -> dict[str, Any]:
        """Prepare template context from resume data."""
        return {
            "personal_info": self.resume_data.personal_info,
            "professional_summary": self.resume_data.professional_summary,
            "experience": self.resume_data.experience,
            "skills": self.resume_data.skills,
            "education": self.resume_data.education,
            "certifications": self.resume_data.certifications or [],
            "projects": self.resume_data.projects or [],
            "awards": self.resume_data.awards or [],
            "publications": self.resume_data.publications or [],
            "languages": self.resume_data.languages or [],
            "metadata": {
                "build_date": datetime.now().isoformat(),
                "version": self.resume_data.version,
                "theme": self.theme,
                "format": self.get_format_name()
            }
        }
```

### **Task 2: HTML Builder Implementation**
**File**: `src/resume/builders/html.py`

**Key Features**:
- Jinja2 template rendering
- Embedded CSS for portability  
- Responsive design support
- Print-friendly styles

**Implementation Pattern**:
```python
class HtmlBuilder(BaseBuilder):
    def __init__(self, resume_data: ResumeData, output_dir: Path, theme: str = "modern"):
        super().__init__(resume_data, output_dir, theme)
        
        # Set up Jinja2 environment
        template_dir = Path(__file__).parent.parent.parent.parent / "templates" / "html"
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
        
        # Add custom filters
        self.env.filters['format_date'] = self._format_date
        self.env.filters['format_phone'] = self._format_phone
        self.env.filters['skill_level_class'] = self._skill_level_class
    
    def build(self) -> Path:
        """Generate HTML resume."""
        try:
            template = self.env.get_template(f"themes/{self.theme}.html")
            context = self.prepare_context()
            html_content = template.render(**context)
            
            output_path = self.output_dir / self.get_output_filename()
            output_path.write_text(html_content, encoding='utf-8')
            
            return output_path
        except Exception as e:
            raise RenderError(f"HTML rendering failed: {e}", format_type="html")
```

### **Task 3: JSON Builder Implementation**
**File**: `src/resume/builders/json_builder.py`

**Key Features**:
- Direct Pydantic serialization
- Build metadata enrichment
- Pretty-printed output
- API-friendly format

**Implementation Pattern**:
```python
class JsonBuilder(BaseBuilder):
    def build(self) -> Path:
        """Generate JSON resume."""
        try:
            # Serialize Pydantic model to dict
            resume_dict = self.resume_data.model_dump()
            
            # Add build metadata
            resume_dict["build_info"] = {
                "build_date": datetime.now().isoformat(),
                "builder_version": "1.0.0",
                "format": "json",
                "theme": self.theme,
                "generator": "Tom Drake Resume System"
            }
            
            # Write formatted JSON
            output_path = self.output_dir / self.get_output_filename()
            with output_path.open('w', encoding='utf-8') as f:
                json.dump(resume_dict, f, indent=2, ensure_ascii=False, default=str)
            
            return output_path
        except Exception as e:
            raise RenderError(f"JSON generation failed: {e}", format_type="json")
```

### **Task 4: Markdown Builder Implementation**
**File**: `src/resume/builders/markdown.py`

**Template**: `templates/markdown/github.md`

**Key Features**:
- GitHub-flavored markdown
- Skill badge generation
- Link optimization
- Clean formatting

**Skill Badge Example**:
```python
def _create_skill_badge(self, skill_name: str, proficiency: str) -> str:
    """Create GitHub badge for skill."""
    color_map = {
        'expert': 'brightgreen',
        'advanced': 'green',
        'intermediate': 'yellow',
        'beginner': 'orange'
    }
    color = color_map.get(proficiency.lower(), 'lightgrey')
    skill_encoded = skill_name.replace(' ', '%20')
    return f"![{skill_name}](https://img.shields.io/badge/{skill_encoded}-{proficiency}-{color})"
```

### **Task 5: PDF Builder Implementation**
**File**: `src/resume/builders/pdf.py`

**Strategy**: HTML → WeasyPrint → PDF (highest quality)

**Key Features**:
- Professional typography
- Print-ready output
- A4/Letter page layout
- ATS-friendly formatting

**Implementation Pattern**:
```python
class PdfBuilder(BaseBuilder):
    def build(self) -> Path:
        """Generate PDF resume using WeasyPrint."""
        try:
            # Generate HTML first using HTML builder
            html_builder = HtmlBuilder(self.resume_data, self.output_dir, self.theme)
            html_path = html_builder.build()
            
            # Convert HTML to PDF
            output_path = self.output_dir / self.get_output_filename()
            weasyprint.HTML(filename=str(html_path)).write_pdf(
                str(output_path),
                stylesheets=[weasyprint.CSS(string='@page { size: A4; margin: 0.75in; }')]
            )
            
            return output_path
        except Exception as e:
            raise RenderError(f"PDF generation failed: {e}", format_type="pdf")
```

### **Task 6: Builder Factory Update**
**File**: `src/resume/builders/__init__.py`

**Required Changes**:
```python
from .base import BaseBuilder, BuilderError, TemplateError, RenderError
from .html import HtmlBuilder
from .json_builder import JsonBuilder
from .markdown import MarkdownBuilder
from .pdf import PdfBuilder

class BuilderFactory:
    """Factory for creating resume builders."""
    
    _builders = {
        'html': HtmlBuilder,
        'json': JsonBuilder,
        'markdown': MarkdownBuilder,
        'pdf': PdfBuilder
    }
    
    @classmethod
    def create_builder(cls, format_type: str, resume_data: ResumeData, output_dir: Path, theme: str = "modern") -> BaseBuilder:
        """Create a builder instance for the specified format."""
        if format_type not in cls._builders:
            available = ', '.join(cls._builders.keys())
            raise ValueError(f"Unknown format '{format_type}'. Available: {available}")
        
        builder_class = cls._builders[format_type]
        return builder_class(resume_data, output_dir, theme)

__all__ = [
    "BaseBuilder", "BuilderFactory", "BuilderError", "TemplateError", "RenderError",
    "HtmlBuilder", "JsonBuilder", "MarkdownBuilder", "PdfBuilder"
]
```

## 📁 **Template Requirements**

### **Existing Templates (Already Available)**
- ✅ `templates/html/themes/modern.html` - Professional responsive HTML

### **New Templates Needed**
- 📝 `templates/markdown/github.md` - GitHub-optimized markdown template

**Markdown Template Structure**:
```markdown
# {{ personal_info.name }}
## {{ personal_info.title }}

📍 {{ personal_info.location.city }}, {{ personal_info.location.state }}  
📧 {{ personal_info.email }}  
📞 {{ personal_info.phone }}

## 🎯 Professional Summary
{{ professional_summary.overview }}

### Key Strengths
{% for strength in professional_summary.key_strengths %}
- **{{ strength }}**
{% endfor %}

## 💼 Experience
{% for exp in experience %}
### {{ exp.role }} @ {{ exp.company }}
*{{ exp.start_date }}{% if exp.end_date %} - {{ exp.end_date }}{% else %} - Present{% endif %}*

{% for achievement in exp.achievements %}
- {{ achievement.description }}
{% endfor %}
{% endfor %}

## 🛠️ Skills
{% for category_name, category in skills.categories.items() %}
### {{ category.display_name }}
{% for skill in category.skills %}
{{ skill.name | skill_badge(skill.proficiency) }}
{% endfor %}
{% endfor %}
```

## 🎯 **Success Criteria**

### **Functional Requirements**
- [ ] **HTML Builder**: Generates responsive `resume.html` using existing template
- [ ] **JSON Builder**: Creates clean `resume.json` with metadata
- [ ] **Markdown Builder**: Produces GitHub-ready `resume.md` with badges
- [ ] **PDF Builder**: Generates professional `resume.pdf` from HTML

### **Integration Requirements**
- [ ] **CLI Commands Work**: All `uv run resume build` commands succeed
- [ ] **Error Handling**: Graceful failures with helpful error messages
- [ ] **File Output**: All files generated in specified output directory
- [ ] **Theme Support**: Basic theme switching functional

### **Quality Requirements**  
- [ ] **Performance**: Complete 4-format build in < 5 seconds
- [ ] **Visual Quality**: HTML output looks professional and responsive
- [ ] **Data Integrity**: All resume sections properly represented
- [ ] **Code Quality**: Passes all existing quality checks

## 🚀 **Implementation Priority**

### **Phase 2A (Day 1) - Critical Path**
1. **🔥 HTML Builder** - Highest priority for visual feedback
   - Immediate visual validation of formatting
   - Foundation for PDF generation  
   - Uses existing template infrastructure

### **Phase 2B (Day 2) - Core Functionality**
2. **📋 JSON Builder** - Easiest implementation  
   - Direct Pydantic serialization
   - No template dependencies
   - Perfect for testing data flow

3. **📝 Markdown Builder** - Medium complexity
   - Requires new template creation
   - GitHub badge integration
   - Good for documentation/profiles

### **Phase 2C (Day 3) - Professional Output**
4. **📄 PDF Builder** - Depends on HTML builder
   - Professional print output
   - Uses HTML builder as foundation
   - WeasyPrint integration

## 📊 **Testing Strategy**

### **Manual Testing Commands**
```bash
# Test individual formats
uv run resume build all --format html
uv run resume build all --format json  
uv run resume build all --format markdown
uv run resume build all --format pdf

# Test complete build
uv run resume build all --clean

# Verify outputs in dist/ directory
ls -la dist/
```

### **Expected Output Files**
```
dist/
├── resume.html    # Responsive HTML with embedded CSS
├── resume.json    # Clean structured data with metadata  
├── resume.md      # GitHub markdown with skill badges
└── resume.pdf     # Professional print-ready PDF
```

## 🔗 **Dependencies & Prerequisites**

### **Already Available**
- ✅ All required Python packages installed (`jinja2`, `weasyprint`, etc.)
- ✅ Base builder framework in place
- ✅ Professional HTML template ready
- ✅ Resume data validated and loading correctly
- ✅ CLI framework expecting builder classes

### **To Be Created**
- 📝 Four builder implementation files
- 📝 Markdown template file
- 📝 Updated factory imports and registration

## 💡 **Implementation Notes**

### **Error Handling Philosophy**
- **Fail Fast**: Catch configuration errors early
- **Graceful Degradation**: Continue building other formats if one fails  
- **User-Friendly Messages**: Convert technical errors to actionable feedback
- **Rich Progress**: Show build progress for each format

### **Performance Considerations**
- **Template Caching**: Reuse Jinja2 environments across builds
- **Parallel Building**: Consider async building for multiple formats
- **Memory Management**: Clean up temporary files (especially for PDF)

### **Future Extensibility**
- **Plugin Architecture**: Easy to add new formats (LaTeX, DOCX, etc.)
- **Custom Themes**: Template-based theming system
- **Advanced PDF**: Custom layouts and typography options

This implementation plan provides a clear, actionable roadmap for completing Phase 2 and achieving fully functional multi-format resume generation. The priority-based approach ensures you get visual feedback quickly while building toward a complete professional system.