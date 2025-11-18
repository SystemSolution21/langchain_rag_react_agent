"""Pytest configuration and shared fixtures for tests."""

import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from langchain_core.documents.base import Document


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup - handle Windows file locking issues
    if temp_path.exists():
        try:
            shutil.rmtree(temp_path)
        except PermissionError:
            # On Windows, files may still be locked by handlers
            # Try to close any open file handles and retry
            import gc
            import time

            gc.collect()  # Force garbage collection to close file handles
            time.sleep(0.1)  # Give OS time to release locks
            try:
                shutil.rmtree(temp_path)
            except PermissionError:
                # If still failing, just pass - temp files will be cleaned up by OS
                pass


@pytest.fixture
def mock_pdfs_dir(temp_dir: Path) -> Path:
    """Create a mock PDFs directory."""
    pdfs_dir = temp_dir / "pdfs"
    pdfs_dir.mkdir(parents=True, exist_ok=True)
    return pdfs_dir


@pytest.fixture
def mock_db_dir(temp_dir: Path) -> Path:
    """Create a mock database directory."""
    db_dir = temp_dir / "db"
    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir


@pytest.fixture
def mock_logs_dir(temp_dir: Path) -> Path:
    """Create a mock logs directory."""
    logs_dir = temp_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir


@pytest.fixture
def sample_documents() -> list[Document]:
    """Create sample documents for testing."""
    return [
        Document(
            page_content="This is a test document about neural networks.",
            metadata={"source": "test1.pdf", "page": 0},
        ),
        Document(
            page_content="Machine learning is a subset of artificial intelligence.",
            metadata={"source": "test2.pdf", "page": 0},
        ),
        Document(
            page_content="Table 1: Results\nModel | Accuracy\nGPT-3 | 95%\nBERT | 92%",
            metadata={"source": "test3.pdf", "page": 1, "content_type": "table"},
        ),
    ]


@pytest.fixture
def mock_env_vars(temp_dir: Path, monkeypatch) -> None:
    """Set up mock environment variables for testing."""
    monkeypatch.setenv("PROJECT_ROOT", str(temp_dir))
    monkeypatch.setenv("PDFS_DIR", str(temp_dir / "pdfs"))
    monkeypatch.setenv("DB_DIR", str(temp_dir / "db"))
    monkeypatch.setenv("LOGS_DIR", str(temp_dir / "logs"))
    monkeypatch.setenv("OLLAMA_LLM", "llama3.2:3b")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")


@pytest.fixture
def sample_pdf_content() -> bytes:
    """Create minimal valid PDF content for testing."""
    # Minimal PDF structure
    pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj
4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
(Test PDF) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000317 00000 n
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
410
%%EOF
"""
    return pdf_content


@pytest.fixture
def create_test_pdf(mock_pdfs_dir: Path, sample_pdf_content: bytes):
    """Factory fixture to create test PDF files."""

    def _create_pdf(filename: str = "test.pdf") -> Path:
        pdf_path = mock_pdfs_dir / filename
        pdf_path.write_bytes(sample_pdf_content)
        return pdf_path

    return _create_pdf
