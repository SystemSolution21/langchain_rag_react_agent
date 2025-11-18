"""Configuration module for path management."""

import os
from pathlib import Path
from typing import Optional


def _get_path_from_env(env_var: str, default_path: Path) -> Path:
    """
    Get a path from an environment variable or use a default.

    Args:
        env_var: The name of the environment variable.
        default_path: The default path to use if the environment variable is not set.

    Returns:
        The resolved path.
    """
    path_str: Optional[str] = os.getenv(key=env_var)
    return Path(path_str) if path_str else default_path


def get_project_root() -> Path:
    """Get the project root directory."""
    current_file: Path = Path(__file__).resolve()
    default_root: Path = current_file.parent.parent.parent
    return _get_path_from_env(env_var="PROJECT_ROOT", default_path=default_root)


def get_pdfs_dir() -> Path:
    """Get the PDFs directory path."""
    return _get_path_from_env(env_var="PDFS_DIR", default_path=get_project_root() / "pdfs")


def get_db_dir() -> Path:
    """Get the database directory path."""
    return _get_path_from_env(env_var="DB_DIR", default_path=get_project_root() / "db")


def get_logs_dir() -> Path:
    """Get the logs directory path."""
    return _get_path_from_env(env_var="LOGS_DIR", default_path=get_project_root() / "logs")
