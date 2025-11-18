"""Tests for the config module."""

from pathlib import Path

from langchain_rag_react_agent.config import (
    get_db_dir,
    get_logs_dir,
    get_pdfs_dir,
    get_project_root,
)


class TestGetProjectRoot:
    """Tests for get_project_root function."""

    def test_get_project_root_from_env(self, temp_dir: Path, monkeypatch):
        """Test getting project root from environment variable."""
        monkeypatch.setenv("PROJECT_ROOT", str(temp_dir))
        result = get_project_root()
        assert result == temp_dir

    def test_get_project_root_default(self, monkeypatch):
        """Test getting project root when no env var is set."""
        monkeypatch.delenv("PROJECT_ROOT", raising=False)
        result = get_project_root()
        # Should return the parent of src/langchain_rag_react_agent
        assert isinstance(result, Path)
        assert result.exists()

    def test_get_project_root_returns_path(self, temp_dir: Path, monkeypatch):
        """Test that get_project_root returns a Path object."""
        monkeypatch.setenv("PROJECT_ROOT", str(temp_dir))
        result = get_project_root()
        assert isinstance(result, Path)


class TestGetPdfsDir:
    """Tests for get_pdfs_dir function."""

    def test_get_pdfs_dir_from_env(self, temp_dir: Path, monkeypatch):
        """Test getting PDFs directory from environment variable."""
        pdfs_dir = temp_dir / "custom_pdfs"
        monkeypatch.setenv("PDFS_DIR", str(pdfs_dir))
        result = get_pdfs_dir()
        assert result == pdfs_dir

    def test_get_pdfs_dir_default(self, temp_dir: Path, monkeypatch):
        """Test getting PDFs directory when no env var is set."""
        monkeypatch.delenv("PDFS_DIR", raising=False)
        monkeypatch.setenv("PROJECT_ROOT", str(temp_dir))
        result = get_pdfs_dir()
        assert result == temp_dir / "pdfs"

    def test_get_pdfs_dir_returns_path(self, temp_dir: Path, monkeypatch):
        """Test that get_pdfs_dir returns a Path object."""
        monkeypatch.setenv("PDFS_DIR", str(temp_dir / "pdfs"))
        result = get_pdfs_dir()
        assert isinstance(result, Path)


class TestGetDbDir:
    """Tests for get_db_dir function."""

    def test_get_db_dir_from_env(self, temp_dir: Path, monkeypatch):
        """Test getting database directory from environment variable."""
        db_dir = temp_dir / "custom_db"
        monkeypatch.setenv("DB_DIR", str(db_dir))
        result = get_db_dir()
        assert result == db_dir

    def test_get_db_dir_default(self, temp_dir: Path, monkeypatch):
        """Test getting database directory when no env var is set."""
        monkeypatch.delenv("DB_DIR", raising=False)
        monkeypatch.setenv("PROJECT_ROOT", str(temp_dir))
        result = get_db_dir()
        assert result == temp_dir / "db"

    def test_get_db_dir_returns_path(self, temp_dir: Path, monkeypatch):
        """Test that get_db_dir returns a Path object."""
        monkeypatch.setenv("DB_DIR", str(temp_dir / "db"))
        result = get_db_dir()
        assert isinstance(result, Path)


class TestGetLogsDir:
    """Tests for get_logs_dir function."""

    def test_get_logs_dir_from_env(self, temp_dir: Path, monkeypatch):
        """Test getting logs directory from environment variable."""
        logs_dir = temp_dir / "custom_logs"
        monkeypatch.setenv("LOGS_DIR", str(logs_dir))
        result = get_logs_dir()
        assert result == logs_dir

    def test_get_logs_dir_default(self, temp_dir: Path, monkeypatch):
        """Test getting logs directory when no env var is set."""
        monkeypatch.delenv("LOGS_DIR", raising=False)
        monkeypatch.setenv("PROJECT_ROOT", str(temp_dir))
        result = get_logs_dir()
        assert result == temp_dir / "logs"

    def test_get_logs_dir_returns_path(self, temp_dir: Path, monkeypatch):
        """Test that get_logs_dir returns a Path object."""
        monkeypatch.setenv("LOGS_DIR", str(temp_dir / "logs"))
        result = get_logs_dir()
        assert isinstance(result, Path)


class TestConfigIntegration:
    """Integration tests for config module."""

    def test_all_paths_use_same_root(self, temp_dir: Path, monkeypatch):
        """Test that all path functions use the same project root."""
        monkeypatch.setenv("PROJECT_ROOT", str(temp_dir))
        monkeypatch.delenv("PDFS_DIR", raising=False)
        monkeypatch.delenv("DB_DIR", raising=False)
        monkeypatch.delenv("LOGS_DIR", raising=False)

        root = get_project_root()
        pdfs = get_pdfs_dir()
        db = get_db_dir()
        logs = get_logs_dir()

        assert pdfs == root / "pdfs"
        assert db == root / "db"
        assert logs == root / "logs"

    def test_individual_overrides(self, temp_dir: Path, monkeypatch):
        """Test that individual directory overrides work independently."""
        monkeypatch.setenv("PROJECT_ROOT", str(temp_dir))
        monkeypatch.setenv("PDFS_DIR", str(temp_dir / "my_pdfs"))
        monkeypatch.setenv("DB_DIR", str(temp_dir / "my_db"))
        monkeypatch.delenv("LOGS_DIR", raising=False)

        pdfs = get_pdfs_dir()
        db = get_db_dir()
        logs = get_logs_dir()

        assert pdfs == temp_dir / "my_pdfs"
        assert db == temp_dir / "my_db"
        assert logs == temp_dir / "logs"  # Uses default
