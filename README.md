# 🚀 Resume as Code (RaC): AI-Powered DevOps Learning Project

[![CI/CD Pipeline](https://github.com/silverbeer/resume-as-code/actions/workflows/ci.yml/badge.svg)](https://github.com/silverbeer/resume-as-code/actions)
[![Coverage](https://codecov.io/gh/silverbeer/resume-as-code/branch/main/graph/badge.svg)](https://codecov.io/gh/silverbeer/resume-as-code)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![AI Powered](https://img.shields.io/badge/🤖-AI%20Powered-brightgreen.svg)](./AI_WORKFLOW.md)

## 🤖 Learning Project: Mastering Claude Code & AI DevOps

This project was created as a learning journey to master Claude Code and sharpen AI-powered DevOps skills. It demonstrates innovative AI integration in development workflows, showcasing how Claude AI enhances every aspect of the development lifecycle - from architecture decisions to content optimization.

**[See AI Workflow](./AI_WORKFLOW.md)** | **[Claude Instructions](./CLAUDE.md)**

---

## 🎯 Project Overview

This learning project explores modern DevOps practices through a practical "Resume as Code (RaC)" approach. Created to master Claude Code capabilities while building something genuinely innovative and useful.

### The Innovation

- **🔄 GitOps Workflow**: Version-controlled YAML resume data with automated multi-format compilation
- **🤖 AI Integration**: Claude AI enhances content, generates releases, and powers development workflow  
- **📊 Observability**: Comprehensive metrics, testing, and quality gates
- **🚀 Modern Tooling**: Python with uv, Typer, Rich, and best practices throughout
- **📱 Multi-Format**: Professional PDF (ReportLab), responsive HTML, JSON API, and GitHub Markdown
- **✅ Phase 2 Complete**: All core builders implemented with zero system dependencies

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| **Core** | Python 3.12+, uv, pyproject.toml |
| **CLI** | Typer + Rich for beautiful terminal interfaces |
| **AI** | Claude API for content enhancement and automation |
| **Testing** | pytest, coverage.py (100% coverage requirement) |
| **Quality** | ruff, mypy, pre-commit hooks |
| **CI/CD** | GitHub Actions with comprehensive pipeline |
| **Deployment** | GitHub Pages with automated versioning |
| **Formats** | ReportLab (PDF), Jinja2 (HTML), JSON, GitHub Markdown |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (fast Python package manager)
- Claude API key (for AI features)

### Installation

```bash
# Clone the repository
git clone https://github.com/silverbeer/resume-as-code.git
cd resume-as-code

# Install with uv (handles virtual environment automatically)
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your Claude API key

# Verify installation
uv run resume --help
```

---

## 💡 Usage Examples

### Basic Commands

```bash
# Build all formats (HTML, PDF, JSON, Markdown)
uv run resume build all

# Build specific formats  
uv run resume build all --format pdf
uv run resume build all --format html,json

# Validate resume data against schema
uv run resume validate

# Check system status and configuration
uv run resume status

# Serve development preview (coming soon)
uv run resume serve dev --watch --port 8000
```

### AI-Powered Features

```bash
# Enhance resume achievements with AI
uv run resume ai enhance-achievements --role "Director of DevOps"

# Generate tailored summary for specific role
uv run resume ai summary --target-role "Platform Engineering Manager"

# Optimize keywords for ATS systems
uv run resume ai optimize --job-description job-posting.txt

# Generate release notes with personality
uv run resume ai release-notes --version v1.2.0 --style witty-professional
```

### Development & Quality

```bash
# Run comprehensive test suite
uv run resume test --coverage

# Code quality checks
uv run resume lint --fix
uv run resume format

# Generate AI-powered commit messages
uv run resume ai commit-message --files resume.yml
```

---

## ✅ Phase 2 Success: Multi-Format Resume Generation

**Status: ✅ COMPLETE** - All core builders implemented and fully functional!

### 🏆 Build Results
```bash
✅ Build completed successfully!

           Generated Files            
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Format     ┃ File        ┃    Size ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━┩
│ HTML       │ resume.html │ 34.4 KB │
│ PDF        │ resume.pdf  │  8.7 KB │
│ JSON       │ resume.json │ 34.1 KB │
│ MARKDOWN   │ resume.md   │ 10.6 KB │
└────────────┴─────────────┴─────────┘

📁 Output directory: dist/
```

### 🚀 Core Builders Implemented

1. **🌐 HTML Builder** (`resume.html` - 34.4 KB)
   - Professional responsive design with embedded CSS
   - Custom Jinja2 filters for dates, phone, duration, skills
   - Print-friendly and mobile-optimized layout

2. **📄 PDF Builder** (`resume.pdf` - 8.7 KB, 3 pages)
   - **ReportLab implementation** - Pure Python, zero system dependencies  
   - ATS-friendly formatting with standard fonts and proper structure
   - Professional typography with custom paragraph styles
   - Clickable links and optimized layout

3. **📊 JSON Builder** (`resume.json` - 34.1 KB)
   - Structured data with rich metadata and analytics
   - Career timeline and skill distribution analysis
   - API-ready format with build information

4. **📝 Markdown Builder** (`resume.md` - 10.6 KB)
   - GitHub-flavored markdown with skill badges
   - Professional social media links with branded badges
   - Clean formatting optimized for GitHub profiles

### 🔧 Technical Achievements

- **✅ Zero System Dependencies**: ReportLab replaced WeasyPrint, eliminating system library requirements
- **✅ Cross-Platform Compatibility**: Works on macOS, Linux, Windows, Docker, CI/CD
- **✅ Factory Pattern**: Extensible builder architecture with dynamic registration
- **✅ Error Handling**: Comprehensive error handling with helpful user messages
- **✅ Template System**: Jinja2-based with custom filters and theme support

### 🎯 ReportLab PDF Success Story

**Problem**: WeasyPrint required complex system dependencies (Cairo, Pango, GTK+)
**Solution**: Implemented ReportLab for pure Python PDF generation
**Result**: Professional ATS-friendly PDFs with zero deployment complexity

---

## 📁 Project Structure

```
resume-as-code/
├── 🤖 CLAUDE.md              # AI instructions and project context
├── 🔄 AI_WORKFLOW.md         # AI-powered development process
├── 📄 resume.yml             # YAML source of truth
├── 🐍 pyproject.toml         # Python project configuration
├── src/resume/               # Main Python package
│   ├── 🖥️  cli.py            # Typer CLI with Rich output  
│   ├── 📊 models.py          # Pydantic data models
│   ├── 🤖 ai/                # Claude API integration
│   ├── 🏗️  builders/          # Multi-format generators
│   └── ✅ validators/        # Schema validation
├── 🧪 tests/                # Comprehensive test suite
├── 🎨 templates/             # Jinja2 templates for output formats
├── ⚙️  .github/workflows/    # CI/CD automation
└── 🌐 web/                  # Generated GitHub Pages content
```

---

## 🤖 AI Integration Showcase

This project demonstrates sophisticated AI integration that goes beyond simple code generation:

### Strategic AI Usage
- **Architecture Decisions**: AI assists with technical trade-offs and design patterns
- **Content Enhancement**: Transform basic responsibilities into compelling achievements  
- **Quality Assurance**: AI-powered code review, testing, and content optimization
- **Development Automation**: Smart commit messages, PR descriptions, release notes
- **Continuous Improvement**: AI suggests optimizations and best practices

### Example AI Enhancement

**Before AI:**
> "Managed Kubernetes clusters and implemented CI/CD pipelines"

**After AI Enhancement:**
> "Architected and managed 50+ Kubernetes clusters serving 10M+ requests/day, reducing infrastructure costs by 30% through resource optimization and implementing GitOps-based CI/CD pipelines that decreased deployment time from 2 hours to 15 minutes"

### AI Workflow Highlights
- **Iterative Refinement**: Multiple AI passes for optimal content quality
- **Context-Aware Generation**: AI understands project goals and constraints
- **Domain Expertise**: Leverages AI's knowledge of DevOps best practices
- **Quality Metrics**: Track AI suggestion acceptance rates and impact

---

## 📈 Quality & Observability

### Code Quality Standards
- ✅ **100% Test Coverage** with pytest and comprehensive fixtures
- 🔍 **Static Analysis** with ruff linting and mypy type checking
- 🔒 **Security Scanning** integrated into CI/CD pipeline
- 📋 **Pre-commit Hooks** for consistent code quality
- 🏗️ **Conventional Commits** with AI-generated messages

### CI/CD Pipeline
- 🧪 **Comprehensive Testing** (unit, integration, end-to-end)
- 🏗️ **Multi-format Builds** (PDF, HTML, JSON, Markdown)
- 🤖 **AI Integration Testing** with mocked and live API tests
- 🚀 **Automated Deployment** to GitHub Pages with versioning
- 📊 **Performance Monitoring** for build times and output quality

### Observability Features
- 📊 **Build Metrics**: Duration, success rates, file sizes
- 📈 **Usage Analytics**: Resume views, downloads, engagement
- 🔍 **Quality Metrics**: Test coverage, lint compliance, AI enhancement rates
- 🚨 **Alerting**: Slack notifications for pipeline failures

---

## 🌟 Innovation Highlights

### For Technical Audiences
- **Modern Python Ecosystem**: Demonstrates uv, Typer, Rich, and contemporary practices
- **Comprehensive Testing**: 100% coverage with sophisticated mocking and fixtures  
- **AI-First Development**: Strategic AI integration throughout the development lifecycle
- **DevOps Excellence**: Complete CI/CD, monitoring, and quality automation
- **Clean Architecture**: Well-structured, maintainable, and extensible codebase

### For Business Audiences  
- **Problem-Solving Mindset**: Identified and solved a real personal pain point
- **Innovation Focus**: Novel approach using modern tools and AI integration
- **Quality Obsession**: No compromise on testing, documentation, or best practices
- **Continuous Improvement**: AI-powered insights and optimization suggestions
- **Results-Driven**: Measurable improvements in resume management efficiency

---

## 🚀 Demo Features

The Resume as Code system generates:
- 🌓 **Professional HTML** with responsive design and dark/light mode
- 📱 **Multi-Device Support** optimized for all screen sizes
- 🎯 **Interactive Elements** with skill filtering and navigation
- ⚡ **Fast Performance** with optimized assets and loading
- ♿ **Accessibility** compliant (WCAG 2.1 AA)
- 📊 **Analytics Ready** for tracking engagement

---

## 📚 Documentation

- **[CLAUDE.md](./CLAUDE.md)** - Comprehensive AI instructions and project context
- **[AI_WORKFLOW.md](./AI_WORKFLOW.md)** - AI-powered development process documentation
- **[Development Guide](./docs/DEVELOPMENT.md)** - Setup and contribution guidelines  
- **[API Documentation](./docs/API.md)** - CLI and Python API reference
- **[Deployment Guide](./docs/DEPLOYMENT.md)** - GitHub Pages and CI/CD setup

---

## 🎯 Success Metrics

### Technical Excellence
- ✅ **Phase 2 Complete**: All 4 core builders (HTML, PDF, JSON, Markdown) fully implemented
- ⚡ **Build Speed**: Multi-format generation in < 5 seconds (4 files, ~88 KB total)
- 🔒 **Zero Dependencies**: Pure Python PDF generation, no system libraries required
- 📄 **ATS-Friendly**: Professional PDF output optimized for applicant tracking systems
- 🏗️ **Extensible Architecture**: Factory pattern enables easy addition of new formats

### Business Impact
- 📊 **Multi-Format Output**: Professional resume available in 4 formats simultaneously
- 🎯 **Professional Quality**: Enterprise-grade typography and layout using ReportLab
- 🔄 **Deployment Simplified**: Eliminated complex system dependency issues
- 📱 **Universal Compatibility**: Works across all platforms and CI/CD environments
- ⚡ **Developer Experience**: Simple `uv run resume build all` generates everything

---

## 🤝 Contributing

This learning project demonstrates AI-powered DevOps practices. Contributions and feedback are welcome!

### Development Setup
```bash
# Clone and setup
git clone https://github.com/silverbeer/resume-as-code.git
cd resume-as-code
uv sync

# Install pre-commit hooks
uv run pre-commit install

# Run tests
uv run pytest --cov=src/resume --cov-report=html

# Start development server
uv run resume serve --watch
```

### Contribution Guidelines
- Follow conventional commits format
- Maintain 100% test coverage
- Use AI-assisted development workflow (see [AI_WORKFLOW.md](./AI_WORKFLOW.md))
- All PRs require passing CI/CD pipeline

---

## 🏆 Learning Outcomes

### AI-Powered Development Skills
- **Claude Code Mastery**: Hands-on experience with AI-assisted development workflows
- **Strategic AI Integration**: Learned to leverage AI for architecture, content, and automation
- **Quality-First AI**: Balancing AI assistance with rigorous testing and validation
- **Innovation Mindset**: Exploring new approaches to traditional problems
- **Continuous Learning**: Embracing AI as a tool for skill enhancement

### DevOps Excellence
- **Modern Python Ecosystem**: Mastery of uv, Typer, Rich, and contemporary practices
- **Comprehensive Testing**: Achieving high coverage with sophisticated mocking and fixtures
- **CI/CD Automation**: Building robust pipelines with quality gates and monitoring
- **Clean Architecture**: Designing maintainable, extensible, and well-documented systems
- **Problem-Solving**: Identifying real challenges and building practical solutions

---

## 📞 About This Project

**Resume as Code (RaC)** - AI-Powered DevOps Learning Journey  
🚀 **Purpose**: Mastering Claude Code and sharpening AI DevOps skills  
🤖 **Innovation**: Exploring AI-first development workflows  
🏗️ **Learning**: Hands-on experience with modern Python and DevOps practices  
🎯 **Goal**: Building practical skills through real-world problem solving

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
<strong>🤖 AI-Powered Learning • 🚀 Claude Code Mastery • ⚡ DevOps Innovation</strong>
</div>