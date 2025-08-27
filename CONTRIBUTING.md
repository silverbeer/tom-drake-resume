# Contributing to AI-Powered Resume System

Thank you for your interest in contributing! While this is primarily a personal resume system showcasing DevOps and AI integration skills, contributions and feedback are welcome.

## 🤝 How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs or suggest improvements
- Provide clear reproduction steps and environment details
- Check existing issues to avoid duplicates

### Suggesting Features
- Open an issue with the "enhancement" label
- Describe the use case and expected behavior
- Consider how it fits with the project's AI-powered DevOps theme

### Code Contributions
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes following our coding standards
4. Add tests with 100% coverage
5. Update documentation as needed
6. Submit a Pull Request

## 🛠️ Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/tom-drake-resume.git
cd tom-drake-resume

# Install with uv (recommended)
uv sync --dev

# Or with pip
pip install -e ".[dev]"

# Install pre-commit hooks
uv run pre-commit install

# Run tests
uv run pytest --cov=src/resume --cov-report=html

# Start development server
uv run resume serve --watch
```

## 📋 Coding Standards

### Python Code Style
- Use **Black** for code formatting
- Follow **PEP 8** with line length 88 characters
- Use **type hints** on all functions
- Maintain **100% test coverage**

### Testing Requirements
- Write comprehensive unit tests
- Include integration tests for complex workflows
- Mock external APIs (Claude, GitHub, etc.)
- Test CLI commands and error handling

### Documentation
- Update docstrings for all public functions
- Keep README.md current
- Update CLAUDE.md for AI-related changes
- Include examples in docstrings

### Git Workflow
- Use conventional commits: `feat:`, `fix:`, `docs:`, etc.
- Write descriptive commit messages
- Squash commits before merging
- Keep PRs focused and reasonably sized

## 🤖 AI Development Guidelines

This project showcases AI-enhanced development workflows:

### AI Integration Standards
- Use Claude API responsibly with rate limiting
- Include fallback behavior when AI is unavailable
- Make AI enhancements optional, not required
- Document AI decision-making processes

### Prompt Engineering
- Store prompts in `src/resume/ai/prompts.py`
- Use template-based prompts with clear context
- Include examples in prompts for better results
- Version and test prompt changes

### AI Testing
- Mock AI API responses for consistent testing
- Test both successful and error scenarios
- Include tests for prompt generation
- Verify AI enhancement quality

## 🔧 Quality Gates

All contributions must pass:

- [ ] **Tests**: 100% coverage with pytest
- [ ] **Linting**: Passes ruff with no errors
- [ ] **Type Checking**: Passes mypy validation
- [ ] **Security**: Passes bandit security scan
- [ ] **Pre-commit**: All hooks pass
- [ ] **CI/CD**: GitHub Actions pipeline succeeds

### Running Quality Checks Locally

```bash
# Format code
uv run black src/ tests/
uv run isort src/ tests/

# Lint code
uv run ruff src/ tests/

# Type checking
uv run mypy src/

# Security scan
uv run bandit -r src/

# Run all tests
uv run pytest --cov=src/resume --cov-report=html --cov-fail-under=100

# Pre-commit hooks
uv run pre-commit run --all-files
```

## 📖 Documentation Updates

When contributing:

1. **Code Documentation**: Update docstrings and inline comments
2. **User Documentation**: Update README.md if adding user-facing features
3. **AI Documentation**: Update CLAUDE.md for AI-related changes
4. **API Documentation**: Keep CLI help text current
5. **Examples**: Add examples for new features

## 🚀 Release Process

This project uses semantic versioning:

- **Major** (1.0.0): Breaking changes
- **Minor** (0.1.0): New features, backwards compatible
- **Patch** (0.0.1): Bug fixes, backwards compatible

Releases are automated via GitHub Actions when tags are pushed.

## 🎯 Project Goals

Keep in mind this project's primary objectives:

1. **Showcase DevOps Skills**: Modern Python tooling, CI/CD, observability
2. **Demonstrate AI Integration**: Strategic AI use, not just basic automation
3. **Solve Real Problems**: Resume management pain points
4. **Professional Quality**: Production-ready code and practices
5. **Innovation**: Novel approaches to common challenges

## 🤔 Questions?

- Open a GitHub Issue for technical questions
- Check existing issues and documentation first
- Be specific about your environment and use case

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make this project better!** 🙌

Your contributions help demonstrate that this project follows modern collaborative development practices - another selling point for potential employers!