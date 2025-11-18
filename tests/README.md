# Test Suite for LangChain RAG React Agent

This directory contains the test suite for the LangChain RAG React Agent application.

## 📋 Test Structure

```test-structure
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Shared fixtures and test configuration
├── test_config.py           # Tests for configuration module
├── test_logger.py           # Tests for logging module
├── test_rag.py              # Tests for RAG processing module
├── test_agent.py            # Tests for agent module
└── README.md                # This file
```

## 🚀 Running Tests

### Run All Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=langchain_rag_react_agent --cov-report=html
```

### Run Specific Test Files

```bash
# Run only config tests
pytest tests/test_config.py

# Run only RAG tests
pytest tests/test_rag.py

# Run only logger tests
pytest tests/test_logger.py

# Run only agent tests
pytest tests/test_agent.py
```

### Run Specific Test Classes or Functions

```bash
# Run a specific test class
pytest tests/test_config.py::TestGetProjectRoot

# Run a specific test function
pytest tests/test_config.py::TestGetProjectRoot::test_get_project_root_from_env

# Run tests matching a pattern
pytest -k "test_get_project"
```

### Run Tests by Markers

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only slow tests
pytest -m slow

# Exclude slow tests
pytest -m "not slow"
```

## 🐳 Running Tests in Docker

### Run Tests in Container

```bash
# Run tests in the app container
docker exec langchain-rag-agent pytest

# Run with verbose output
docker exec langchain-rag-agent pytest -v

# Run specific test file
docker exec langchain-rag-agent pytest tests/test_config.py

# Run with coverage
docker exec langchain-rag-agent pytest --cov=langchain_rag_react_agent
```

### Run Tests During Build

```bash
# Build and run tests
docker-compose build
docker-compose run --rm app pytest
```

## 📊 Test Coverage

### Generate Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=langchain_rag_react_agent --cov-report=html

# Open coverage report (Linux/Mac)
open htmlcov/index.html

# Open coverage report (Windows)
start htmlcov/index.html
```

### Generate Terminal Coverage Report

```bash
# Show coverage in terminal
pytest --cov=langchain_rag_react_agent --cov-report=term-missing
```

## 🧪 Test Categories

### Unit Tests

- **test_config.py**: Configuration path management
- **test_logger.py**: Logging functionality
- **test_rag.py**: RAG processing components (mocked)
- **test_agent.py**: Agent components (mocked)

### Integration Tests

Integration tests that require external services (Ollama, actual PDFs) are marked with `@pytest.mark.integration`.

## 🔧 Writing New Tests

### Test File Naming

- Test files must start with `test_`
- Test classes must start with `Test`
- Test functions must start with `test_`

### Using Fixtures

```python
def test_example(temp_dir, mock_pdfs_dir):
    """Example test using fixtures."""
    # temp_dir provides a temporary directory
    # mock_pdfs_dir provides a mock PDFs directory
    assert temp_dir.exists()
    assert mock_pdfs_dir.exists()
```

### Available Fixtures (from conftest.py)

- `temp_dir`: Temporary directory for testing
- `mock_pdfs_dir`: Mock PDFs directory
- `mock_db_dir`: Mock database directory
- `mock_logs_dir`: Mock logs directory
- `sample_documents`: Sample LangChain documents
- `mock_env_vars`: Mock environment variables
- `sample_pdf_content`: Minimal valid PDF content
- `create_test_pdf`: Factory to create test PDF files

### Adding Test Markers

```python
import pytest

@pytest.mark.unit
def test_unit_example():
    """A unit test."""
    pass

@pytest.mark.integration
@pytest.mark.requires_ollama
def test_integration_example():
    """An integration test requiring Ollama."""
    pass

@pytest.mark.slow
def test_slow_example():
    """A slow test."""
    pass
```

## 🐛 Debugging Tests

### Run Tests with Debug Output

```bash
# Show print statements
pytest -s

# Show local variables on failure
pytest -l

# Drop into debugger on failure
pytest --pdb

# Drop into debugger at start of test
pytest --trace
```

### Run Single Test with Maximum Verbosity

```bash
pytest tests/test_config.py::TestGetProjectRoot::test_get_project_root_from_env -vv -s
```

## 📝 Test Requirements

The test suite requires the following packages (included in `dev` dependencies):

- `pytest>=8.3.5`
- `pytest-cov` (optional, for coverage reports)
- `pytest-timeout` (optional, for test timeouts)

Install with:

```bash
uv sync --group dev
```

## ✅ Best Practices

1. **Keep tests isolated**: Each test should be independent
2. **Use fixtures**: Reuse common setup code via fixtures
3. **Mock external dependencies**: Use mocks for external services
4. **Test edge cases**: Include tests for error conditions
5. **Keep tests fast**: Mock slow operations when possible
6. **Use descriptive names**: Test names should describe what they test
7. **Add docstrings**: Explain what each test does
8. **Clean up resources**: Use fixtures with cleanup or context managers
