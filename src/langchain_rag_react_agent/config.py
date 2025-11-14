"""Configuration module for path management."""
import os
from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory."""
    env_root = os.getenv("PROJECT_ROOT")
    if env_root:
        return Path(env_root)
    current_file = Path(__file__).resolve()
    return current_file.parent.parent.parent


def get_pdfs_dir() -> Path:
    """Get the PDFs directory path."""
    pdfs_path = os.getenv("PDFS_DIR")
    if pdfs_path:
        return Path(pdfs_path)
    return get_project_root() / "pdfs"


def get_db_dir() -> Path:
    """Get the database directory path."""
    db_path = os.getenv("DB_DIR")
    if db_path:
        return Path(db_path)
    return get_project_root() / "db"


def get_logs_dir() -> Path:
    """Get the logs directory path."""
    logs_path = os.getenv("LOGS_DIR")
    if logs_path:
        return Path(logs_path)
    return get_project_root() / "logs"
