# Contributing to QBOM

Thank you for your interest in contributing to QBOM! This document provides guidelines and information for contributors.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and constructive in all interactions.

## Getting Started

### Development Setup

```bash
# Clone the repository
git clone https://github.com/csnp/qbom.git
cd qbom

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev,all]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/qbom --cov-report=html

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Type checking
mypy src/qbom

# Linting
ruff check src/qbom

# Auto-fix linting issues
ruff check src/qbom --fix

# Format code
ruff format src/qbom
```

## Project Structure

```
qbom/
├── src/qbom/
│   ├── core/           # Framework-agnostic core
│   │   ├── models.py   # Pydantic data models
│   │   ├── trace.py    # Trace object and builder
│   │   └── session.py  # Session management
│   ├── adapters/       # Framework-specific adapters
│   │   ├── base.py     # Base adapter class
│   │   ├── qiskit.py   # Qiskit adapter
│   │   ├── cirq.py     # Cirq adapter
│   │   └── pennylane.py # PennyLane adapter
│   ├── analysis/       # Analysis tools
│   │   ├── score.py    # Reproducibility scoring
│   │   ├── drift.py    # Calibration drift
│   │   └── validation.py # Trace validation
│   ├── cli/            # Command-line interface
│   └── notebook/       # Jupyter integration
├── tests/              # Test files
├── docs/               # Documentation
└── pyproject.toml      # Project configuration
```

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (Python version, OS, framework versions)
   - QBOM trace file if relevant

### Suggesting Features

1. Check existing issues and discussions
2. Create a feature request with:
   - Clear description of the feature
   - Use case and motivation
   - Proposed implementation (if any)

### Submitting Pull Requests

1. **Fork** the repository
2. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/my-feature
   # or
   git checkout -b fix/bug-description
   ```
3. **Make your changes**
4. **Add tests** for new functionality
5. **Run tests and linting**:
   ```bash
   pytest
   mypy src/qbom
   ruff check src/qbom
   ```
6. **Commit** with clear messages:
   ```bash
   git commit -m "Add feature: description of feature"
   ```
7. **Push** to your fork:
   ```bash
   git push origin feature/my-feature
   ```
8. **Create a Pull Request** with:
   - Clear description of changes
   - Link to related issues
   - Test results

## Coding Guidelines

### Style

- Follow PEP 8
- Use type hints for all functions
- Maximum line length: 100 characters
- Use descriptive variable names

### Documentation

- All public functions must have docstrings
- Use Google-style docstrings
- Update relevant documentation files

### Testing

- Write tests for all new functionality
- Maintain test coverage above 80% for new code
- Use pytest fixtures for common setup

### Example

```python
def calculate_score(trace: Trace) -> ScoreResult:
    """
    Calculate reproducibility score for a trace.

    Analyzes the trace's completeness and calculates a score
    from 0-100 indicating how reproducible the experiment is.

    Args:
        trace: The QBOM trace to analyze.

    Returns:
        ScoreResult containing total score, grade, and component breakdown.

    Raises:
        ValueError: If trace is invalid or empty.

    Example:
        >>> trace = qbom.current()
        >>> result = calculate_score(trace)
        >>> print(f"Score: {result.total_score}/100")
        Score: 71/100
    """
    # Implementation...
```

## Adding a New Adapter

To add support for a new quantum framework:

1. Create `src/qbom/adapters/newframework.py`:

```python
from qbom.adapters.base import Adapter

class NewFrameworkAdapter(Adapter):
    name = "newframework"

    def install(self) -> None:
        # Hook framework functions
        pass

    def uninstall(self) -> None:
        self._unwrap_all()
        self._installed = False
```

2. Register in `src/qbom/core/session.py`:

```python
ADAPTER_MAP = {
    # ...existing...
    "newframework": ("qbom.adapters.newframework", "NewFrameworkAdapter"),
}
```

3. Add to `WATCHED_MODULES` in `QBOMImportFinder`:

```python
WATCHED_MODULES = {
    # ...existing...
    "newframework": "newframework",
}
```

4. Add optional dependency in `pyproject.toml`:

```toml
[project.optional-dependencies]
newframework = ["newframework>=1.0.0"]
```

5. Write tests in `tests/test_newframework_adapter.py`

6. Update documentation in `docs/ADAPTERS.md`

## Release Process

Releases are managed by maintainers:

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create git tag: `git tag v0.2.0`
4. Push tag: `git push origin v0.2.0`
5. GitHub Actions builds and publishes to PyPI

## Getting Help

- Open an issue for bugs or questions
- Start a discussion for feature ideas
- See [documentation](docs/) for usage guides

## Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to QBOM!
