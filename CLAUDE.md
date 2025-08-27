# Claude AI Instructions for Tom Drake's Resume System

## Project Vision
This is an innovative "Resume as Infrastructure" system that demonstrates DevOps expertise through:
- YAML-based structured resume data (version controlled, AI-friendly)
- Multi-format automated compilation (PDF, HTML, JSON, Markdown)  
- GitOps workflow with AI-powered content generation
- Modern Python tooling showcasing best practices
- Comprehensive observability and quality gates

## Technical Stack & Standards

### Core Technologies
- **Python**: uv for dependency management, pyproject.toml configuration
- **CLI Framework**: Typer with Rich for beautiful terminal interfaces
- **Testing**: pytest with 100% coverage requirement
- **AI Integration**: Claude API for content generation and automation
- **Quality Tools**: ruff, mypy, pre-commit hooks
- **CI/CD**: GitHub Actions with comprehensive pipeline
- **Deployment**: GitHub Pages for public resume hosting

### Code Quality Requirements
- 100% test coverage with pytest
- Type hints on all functions (mypy enforcement)
- Ruff linting with strict configuration
- Pre-commit hooks for quality gates
- Comprehensive error handling and logging
- Rich CLI output with progress indicators

## Project Structure

```
tom-drake-resume/
├── CLAUDE.md                   # This file - AI instructions
├── AI_WORKFLOW.md             # AI development process documentation  
├── README.md                  # Public-facing project overview
├── pyproject.toml             # Python project configuration (uv)
├── uv.lock                    # Dependency lock file
├── resume.yml                 # YAML source of truth for resume data
├── resume-schema.json         # JSON schema for validation
├── src/
│   └── resume/
│       ├── __init__.py
│       ├── cli.py             # Main Typer CLI application
│       ├── models.py          # Pydantic data models
│       ├── config.py          # Configuration management
│       ├── ai/
│       │   ├── __init__.py
│       │   ├── claude.py      # Claude API integration
│       │   └── prompts.py     # AI prompt templates
│       ├── builders/
│       │   ├── __init__.py
│       │   ├── base.py        # Base builder class
│       │   ├── pdf.py         # PDF generation (LaTeX/WeasyPrint)
│       │   ├── html.py        # HTML generation (Jinja2)
│       │   ├── json_builder.py# JSON API generation
│       │   └── markdown.py    # Markdown generation
│       ├── validators/
│       │   ├── __init__.py
│       │   └── schema.py      # YAML/JSON schema validation
│       └── utils/
│           ├── __init__.py
│           ├── file_ops.py    # File operations
│           └── logging.py     # Structured logging
├── templates/
│   ├── latex/
│   │   └── professional.tex   # LaTeX template for PDF
│   ├── html/
│   │   ├── base.html         # Base HTML template
│   │   ├── modern.html       # Modern web resume
│   │   └── assets/           # CSS, JS, images
│   └── markdown/
│       └── github.md         # GitHub-flavored markdown
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # pytest fixtures
│   ├── test_cli.py           # CLI testing
│   ├── test_models.py        # Data model tests
│   ├── test_builders/        # Builder tests
│   ├── test_validators/      # Validation tests
│   └── test_ai/              # AI integration tests
├── .github/
│   └── workflows/
│       ├── ci.yml            # Main CI pipeline
│       ├── deploy.yml        # GitHub Pages deployment
│       └── ai-content.yml    # AI-powered content updates
├── .pre-commit-config.yaml   # Pre-commit hooks
├── ruff.toml                 # Python linting configuration
├── mypy.ini                  # Type checking configuration
└── web/                      # Generated GitHub Pages content
```

## CLI Commands (Typer + Rich)

### Core Commands
```bash
# Build resume in multiple formats
resume build --format pdf,html,json --output ./dist

# Validate resume data against schema
resume validate --schema resume-schema.json

# Serve development preview with hot reload
resume serve --port 8000 --watch

# Deploy to GitHub Pages
resume deploy --environment production

# AI-powered content generation
resume ai enhance-achievements --role "DevOps Engineer" 
resume ai generate-summary --target-role "Director of DevOps"
resume ai optimize-keywords --job-description ./job-posting.txt

# Data management
resume data validate --fix-formatting
resume data export --format json --output api/
resume data import --source linkedin-export.json

# Analytics and insights
resume analytics show --period 30d
resume analytics compare-versions --base v1.0 --target v1.1
```

### Development Commands
```bash
# Run comprehensive test suite
resume test --coverage --report html

# Quality checks
resume lint --fix
resume format --check

# AI workflow helpers  
resume ai commit-message --files resume.yml
resume ai release-notes --version v1.2.0
```

## AI Integration Points

### 1. Content Generation
- **Achievement Enhancement**: Transform basic job descriptions into compelling achievement statements
- **Skill Summaries**: Generate contextual skill descriptions based on experience
- **Role Optimization**: Tailor content for specific job applications
- **Keyword Optimization**: Analyze job postings and optimize resume keywords

### 2. Quality Assurance
- **Content Review**: AI-powered grammar, clarity, and impact assessment
- **Consistency Checks**: Ensure consistent tone and terminology throughout
- **Gap Analysis**: Identify missing skills or experiences for target roles

### 3. Development Automation
- **Commit Messages**: Generate meaningful commit messages for resume changes
- **PR Descriptions**: Create detailed pull request descriptions with change summaries
- **Release Notes**: Generate engaging release notes for resume versions
- **Documentation**: Auto-generate and maintain project documentation

### 4. Analytics & Insights
- **Trend Analysis**: Compare resume against industry trends and requirements
- **Impact Scoring**: Quantify the strength of achievement statements
- **Competitive Analysis**: Suggest improvements based on market research

## Claude API Usage Patterns

### Content Generation Prompts
```python
ACHIEVEMENT_ENHANCEMENT_PROMPT = """
Transform this basic job responsibility into a compelling achievement statement:

Original: "{responsibility}"
Role Context: {role_context}
Industry: {industry}

Requirements:
- Start with strong action verb
- Include quantifiable metrics when possible
- Highlight business impact
- Use power words for leadership roles
- Keep under 150 words

Generate 3 variations with different focus areas.
"""

SKILL_SUMMARY_PROMPT = """
Generate a compelling summary for this skill:

Skill: "{skill}"
Experience Level: {experience_years} years
Role Context: {role_type}
Recent Projects: {recent_projects}

Create a 2-3 sentence summary that demonstrates expertise and business value.
"""
```

### Development Automation
```python
COMMIT_MESSAGE_PROMPT = """
Generate a conventional commit message for these resume changes:

Files changed: {files}
Diff summary: {diff_summary}
Change type: {change_type}

Follow conventional commits format:
- feat: new features/content
- fix: corrections/updates  
- docs: documentation changes
- style: formatting changes

Include a witty but professional comment that reflects DevOps culture.
"""
```

## Development Workflow with Claude

### 1. Feature Development
1. Discuss requirements and approach with Claude
2. Generate implementation plan with todos
3. Create code with Claude assistance
4. Implement comprehensive tests
5. Generate AI-powered commit messages
6. Create PR with Claude-generated description

### 2. Content Updates
1. Update resume.yml with new information
2. Use Claude to enhance achievement descriptions
3. Validate against schema and run quality checks
4. Generate preview and review changes
5. Deploy with AI-generated release notes

### 3. Quality Assurance
1. Run full test suite with coverage reporting
2. Execute linting and type checking
3. AI-powered content review for clarity and impact
4. Performance testing for build pipeline
5. Accessibility testing for web version

## Error Handling & Logging

### Structured Logging Requirements
```python
import structlog

logger = structlog.get_logger()

# Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
# Include context: user_action, file_path, format, duration
# Use Rich for CLI output formatting
```

### Error Categories
- **Validation Errors**: Schema validation, required fields, format issues
- **Build Errors**: Template rendering, file generation, dependency issues  
- **AI Errors**: API failures, rate limiting, content quality issues
- **Deployment Errors**: GitHub Pages, file permissions, network issues

## Testing Strategy

### Test Coverage Requirements
- Unit tests: 100% coverage for all modules
- Integration tests: CLI commands, file operations, AI integration
- End-to-end tests: Full build pipeline, deployment process
- Performance tests: Build times, file sizes, response times

### Test Data Management
- Mock resume data in `tests/fixtures/`
- AI response mocking for consistent testing
- Test output isolation in temporary directories
- Snapshot testing for generated content

## CI/CD Pipeline Requirements

### GitHub Actions Workflow
1. **Code Quality**: Lint, type check, security scan
2. **Testing**: Unit, integration, and E2E tests with coverage
3. **Build**: Generate all resume formats
4. **AI Integration**: Test Claude API connections
5. **Deploy**: GitHub Pages with versioning
6. **Notifications**: Slack/email for failures

### Quality Gates
- All tests must pass
- 100% test coverage maintained  
- No linting or type errors
- Security scan passes
- Build artifacts generated successfully
- AI integration functional

## Performance & Monitoring

### Build Metrics
- Build duration tracking
- File size optimization
- Template rendering performance
- AI API response times

### User Analytics (GitHub Pages)
- Page views and download tracking
- Popular resume versions
- Geographic distribution
- Referrer analysis

## Security Considerations

### API Key Management
- Claude API keys in GitHub Secrets
- Environment-specific configurations
- Rate limiting and error handling
- Audit logging for AI operations

### Content Security
- Input validation for all user data
- Sanitization of generated content
- Privacy protection for personal information
- Secure deployment practices

## Innovation Showcase Elements

### For Recruiters/Employers
1. **Technical Leadership**: Modern Python practices, comprehensive testing
2. **AI Strategy**: Strategic AI integration, not just basic automation
3. **DevOps Excellence**: Complete CI/CD, monitoring, quality gates
4. **Innovation Mindset**: Novel approach to common problem
5. **Documentation**: Clear, comprehensive, maintainable

### Fun/Creative Elements
- Witty AI-generated commit messages
- Resume "release notes" with changelog humor
- Interactive web version with animations
- QR codes linking PDF to web version
- Resume version comparison tools
- AI-generated "achievement of the day" feature

## Success Metrics

### Technical Metrics
- Build success rate > 99%
- Test coverage = 100%
- Deploy time < 2 minutes
- Zero security vulnerabilities

### Business Metrics  
- Resume views/downloads
- Interview conversion rate
- Recruiter engagement
- Community stars/forks

## Next Phase Ideas

### Advanced Features
- Multi-language support with AI translation
- Industry-specific resume variations
- Real-time job market analysis integration
- AI-powered interview preparation
- Automated LinkedIn profile synchronization
- Skills gap analysis with learning recommendations

This system demonstrates that you're not just using AI as a code generator, but as a strategic tool for innovation, automation, and competitive advantage - exactly what forward-thinking organizations need in their DevOps leadership.