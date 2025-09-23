# Contributing to Docsmaker

Thank you for your interest in contributing to Docsmaker! We welcome contributions from the community and appreciate your help in making Docsmaker better for everyone.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- pip

### Setting up the Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork:**
   ```bash
   git clone https://github.com/OthmaneBlial/docsmaker.git
   cd docsmaker
   ```

3. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install the package in development mode with all dependencies:**
   ```bash
   pip install -e ".[dev,serve]"
   ```

5. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

## Development Workflow

### 1. Choose an Issue

- Check the [Issues](https://github.com/OthmaneBlial/docsmaker/issues) page
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to indicate you're working on it

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### 3. Make Your Changes

- Write clear, concise commit messages
- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed

### 4. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=docsmaker

# Run specific test file
pytest tests/test_specific.py

# Run tests in verbose mode
pytest -v
```

### 5. Code Quality Checks

```bash
# Run linting (if configured)
# Add linting tools as needed, e.g., flake8, black, isort

# Run type checking (if configured)
# e.g., mypy

# Format code
# e.g., black .

# Run all quality checks
pre-commit run --all-files
```

### 6. Update Documentation

- Update README.md if adding new features
- Add docstrings to new functions/classes
- Update type hints
- Add examples for new functionality

### 7. Commit Your Changes

```bash
git add .
git commit -m "feat: add your feature description"
```

Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `style:` for formatting
- `refactor:` for code restructuring
- `test:` for adding tests
- `chore:` for maintenance

### 8. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with a clear description of your changes.

## Adding Plugin or Theme Support

To add support for new plugins or themes:

1. **For Plugins**: Extend the plugin system in `docsmaker/parser.py` or relevant files
2. **For Themes**: Add new theme directories under `themes/`
3. **Test**: Add test cases for new functionality
4. **Document**: Update docs/plugin-development.md or theme-customization.md

## Testing Guidelines

### Unit Tests

- Place tests in `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test function names: `test_function_name_should_do_something`
- Test both success and failure cases
- Mock external dependencies when appropriate

### Integration Tests

- Test end-to-end functionality
- Test with real Markdown files
- Test different configurations

### Test Coverage

- Aim for >80% code coverage
- Cover edge cases and error conditions

## Code Style

### Python Style

- Follow PEP 8
- Use type hints for all function parameters and return values
- Write descriptive variable and function names
- Keep functions small and focused
- Use docstrings for all public functions/classes

### Commit Messages

- Use conventional commit format
- Keep first line under 50 characters
- Use imperative mood: "Add feature" not "Added feature"
- Reference issue numbers when applicable

### Documentation

- Use Google-style docstrings
- Document all public APIs
- Include examples in docstrings when helpful
- Keep README.md up to date

## Reporting Issues

When reporting bugs or requesting features:

1. Check existing issues first
2. Use issue templates when available
3. Provide clear reproduction steps
4. Include version information and environment details
5. Attach sample files if relevant

## Getting Help

- Check the [documentation](https://othmaneblial.github.io/docsmaker/)
- Ask questions in GitHub Discussions
- Join our community (if available)

## Recognition

Contributors will be recognized in:
- The repository's contributor list
- Release notes for significant contributions

Thank you for contributing to Docsmaker! Your help makes the tool better for everyone. 🎉