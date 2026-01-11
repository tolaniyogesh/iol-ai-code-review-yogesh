# Contributing to AI Code Review Assistant

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/iol-ai-code-review-yogesh/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Logs or screenshots if applicable

### Suggesting Features

1. Check existing issues and discussions
2. Create a new issue with:
   - Clear use case
   - Proposed solution
   - Alternatives considered
   - Potential impact

### Pull Requests

1. **Fork the repository**
```bash
git clone https://github.com/yourusername/iol-ai-code-review-yogesh.git
cd iol-ai-code-review-yogesh
```

2. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Make your changes**
   - Follow the code style guidelines
   - Add tests for new functionality
   - Update documentation

4. **Run tests**
```bash
pytest
black src/ tests/
flake8 src/ tests/
mypy src/
```

5. **Commit your changes**
```bash
git add .
git commit -m "feat: Add your feature description"
```

Use conventional commit messages:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions or changes
- `refactor:` Code refactoring
- `style:` Code style changes
- `chore:` Maintenance tasks

6. **Push and create PR**
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Development Setup

### Prerequisites
- Python 3.11+
- Git
- Virtual environment tool

### Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If exists
```

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test
pytest tests/test_static_analyzer.py -v
```

### Code Style

We use:
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/

# Type checking
mypy src/
```

## Project Structure

```
iol-ai-code-review-yogesh/
├── src/
│   ├── analyzers/          # Code analysis modules
│   ├── llm/                # LLM provider integrations
│   ├── config.py           # Configuration management
│   ├── github_client.py    # GitHub API client
│   ├── reviewer.py         # Main review orchestrator
│   └── main.py             # Entry point
├── tests/                  # Test files
├── sample_code/            # Sample code for testing
├── .github/workflows/      # GitHub Actions
└── docs/                   # Documentation
```

## Adding New Features

### Adding a New LLM Provider

1. Create a new file in `src/llm/` (e.g., `new_provider.py`)
2. Implement `BaseLLMProvider` interface
3. Add to factory in `src/llm/factory.py`
4. Update documentation
5. Add tests

Example:
```python
from src.llm.base import BaseLLMProvider

class NewProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str, **kwargs):
        super().__init__(model, **kwargs)
        # Initialize client
    
    async def generate_review(self, prompt: str, context: dict) -> str:
        # Implement review generation
        pass
    
    def estimate_tokens(self, text: str) -> int:
        # Implement token estimation
        pass
```

### Adding New Static Analysis Rules

1. Add pattern to `src/analyzers/static_analyzer.py`
2. Add tests in `tests/test_static_analyzer.py`
3. Document in README

Example:
```python
self.security_patterns.append((
    r'pattern_regex',
    "Description of the issue",
    Severity.CRITICAL
))
```

### Adding Language Support

1. Add language-specific analyzer method
2. Update configuration schema
3. Add tests with sample code
4. Document supported features

## Testing Guidelines

### Unit Tests
- Test individual functions and methods
- Mock external dependencies (GitHub API, LLM APIs)
- Aim for >80% code coverage

### Integration Tests
- Test component interactions
- Use test fixtures for GitHub data
- Mock LLM responses

### Test Naming
```python
def test_<function_name>_<scenario>_<expected_result>():
    # Example: test_analyze_file_with_security_issue_returns_critical_comment
    pass
```

## Documentation

### Code Documentation
- Add docstrings to all public functions/classes
- Use type hints
- Include examples for complex functions

Example:
```python
def analyze_file(self, file_path: str, content: str) -> List[ReviewComment]:
    """
    Analyze a file for code quality issues.
    
    Args:
        file_path: Path to the file being analyzed
        content: File content as string
    
    Returns:
        List of review comments found
    
    Example:
        >>> analyzer = StaticAnalyzer()
        >>> comments = analyzer.analyze_file("test.py", "password = '123'")
        >>> len(comments) > 0
        True
    """
    pass
```

### README Updates
- Update README.md for new features
- Add examples and screenshots
- Update configuration documentation

## Release Process

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. Tag the release (e.g., `v1.0.0`)

## Questions?

- Open a discussion on GitHub
- Contact maintainers
- Check existing documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
