"""Tests for the logger module."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from langchain_rag_react_agent.utils.logger import ReActAgentLogger


class TestReActAgentLogger:
    """Tests for ReActAgentLogger class."""

    def setup_method(self):
        """Reset logger instance before each test."""
        ReActAgentLogger._instance = None

    def teardown_method(self):
        """Clean up logger instance after each test."""
        # Close all handlers to release file locks on Windows
        if ReActAgentLogger._instance is not None:
            for handler in ReActAgentLogger._instance.handlers[:]:
                handler.close()
                ReActAgentLogger._instance.removeHandler(handler)
        ReActAgentLogger._instance = None

    def test_setup_creates_logger(self, temp_dir: Path, monkeypatch):
        """Test that setup creates a logger instance."""
        monkeypatch.setenv("LOGS_DIR", str(temp_dir / "logs"))
        logger = ReActAgentLogger.setup(module_name="test_module")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_module"

    def test_setup_creates_log_directory(self, temp_dir: Path, monkeypatch):
        """Test that setup creates the logs directory."""
        logs_dir = temp_dir / "logs"
        monkeypatch.setenv("LOGS_DIR", str(logs_dir))
        ReActAgentLogger.setup(module_name="test_module")
        assert logs_dir.exists()
        assert logs_dir.is_dir()

    def test_setup_creates_log_file(self, temp_dir: Path, monkeypatch):
        """Test that setup creates the log file."""
        logs_dir = temp_dir / "logs"
        monkeypatch.setenv("LOGS_DIR", str(logs_dir))
        ReActAgentLogger.setup(module_name="test_module")
        assert logs_dir.exists()

    def test_setup_sets_log_level(self, temp_dir: Path, monkeypatch):
        """Test that setup sets the correct log level."""
        monkeypatch.setenv("LOGS_DIR", str(temp_dir / "logs"))
        logger = ReActAgentLogger.setup(module_name="test_module")
        assert logger.level == logging.INFO

    def test_setup_adds_handlers(self, temp_dir: Path, monkeypatch):
        """Test that setup adds file and console handlers."""
        monkeypatch.setenv("LOGS_DIR", str(temp_dir / "logs"))
        logger = ReActAgentLogger.setup(module_name="test_module")
        assert len(logger.handlers) >= 2
        handler_types = [type(h).__name__ for h in logger.handlers]
        assert "RotatingFileHandler" in handler_types
        assert "StreamHandler" in handler_types

    def test_setup_singleton_pattern(self, temp_dir: Path, monkeypatch):
        """Test that setup returns the same instance on multiple calls."""
        monkeypatch.setenv("LOGS_DIR", str(temp_dir / "logs"))
        logger1 = ReActAgentLogger.setup(module_name="test_module1")
        logger2 = ReActAgentLogger.setup(module_name="test_module2")
        assert logger1 is logger2

    def test_get_logger_creates_if_not_exists(self, temp_dir: Path, monkeypatch):
        """Test that get_logger creates a logger if it doesn't exist."""
        monkeypatch.setenv("LOGS_DIR", str(temp_dir / "logs"))
        logger = ReActAgentLogger.get_logger(module_name="test_module")
        assert isinstance(logger, logging.Logger)

    def test_get_logger_returns_existing(self, temp_dir: Path, monkeypatch):
        """Test that get_logger returns existing logger instance."""
        monkeypatch.setenv("LOGS_DIR", str(temp_dir / "logs"))
        logger1 = ReActAgentLogger.setup(module_name="test_module1")
        logger2 = ReActAgentLogger.get_logger(module_name="test_module2")
        assert logger1 is logger2

    def test_logger_can_log_messages(self, temp_dir: Path, monkeypatch):
        """Test that logger can log messages."""
        logs_dir = temp_dir / "logs"
        monkeypatch.setenv("LOGS_DIR", str(logs_dir))
        logger = ReActAgentLogger.get_logger(module_name="test_module")

        # Log a test message
        test_message = "Test log message"
        logger.info(test_message)

        # Check that log file was created and contains the message
        log_file = logs_dir / "agent_tools.log"
        assert log_file.exists()
        log_content = log_file.read_text()
        assert test_message in log_content

    def test_logger_formats_messages_correctly(self, temp_dir: Path, monkeypatch):
        """Test that logger formats messages with correct format."""
        logs_dir = temp_dir / "logs"
        monkeypatch.setenv("LOGS_DIR", str(logs_dir))
        logger = ReActAgentLogger.get_logger(module_name="test_module")

        logger.info("Test message")

        # Close handlers to release file locks on Windows
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

        log_file = logs_dir / "agent_tools.log"
        log_content = log_file.read_text()

        # Check format includes timestamp, level, module (file name), and message
        assert "INFO" in log_content
        assert "test_logger" in log_content  # %(module)s refers to the file name
        assert "Test message" in log_content

    def test_logger_handles_different_log_levels(self, temp_dir: Path, monkeypatch):
        """Test that logger handles different log levels."""
        logs_dir = temp_dir / "logs"
        monkeypatch.setenv("LOGS_DIR", str(logs_dir))
        logger = ReActAgentLogger.get_logger(module_name="test_module")

        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")

        log_file = logs_dir / "agent_tools.log"
        log_content = log_file.read_text()

        assert "INFO" in log_content
        assert "WARNING" in log_content
        assert "ERROR" in log_content
        assert "Info message" in log_content
        assert "Warning message" in log_content
        assert "Error message" in log_content

    def test_rotating_file_handler_configuration(self, temp_dir: Path, monkeypatch):
        """Test that rotating file handler is configured correctly."""
        monkeypatch.setenv("LOGS_DIR", str(temp_dir / "logs"))
        logger = ReActAgentLogger.setup(module_name="test_module")

        # Find the RotatingFileHandler
        rotating_handler: Optional[RotatingFileHandler] = None
        for handler in logger.handlers:
            if isinstance(handler, RotatingFileHandler):
                rotating_handler = handler
                break

        assert isinstance(rotating_handler, RotatingFileHandler)
        assert rotating_handler.maxBytes == 10_000_000  # 10 MB = $10{,}000{,}000$
        assert rotating_handler.backupCount == 5
