"""
Utility functions for the Food Amigo automation system.
"""
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional


def setup_logging(log_dir: str = "logs", log_level: int = logging.INFO) -> logging.Logger:
    """
    Set up logging configuration.

    Args:
        log_dir: Directory to store log files
        log_level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_path / f"automation_{timestamp}.log"

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger("foodamigo_automation")
    logger.info(f"Logging initialized. Log file: {log_file}")

    return logger


def sanitize_filename(name: str) -> str:
    """
    Sanitize a string to be used as a filename.

    Args:
        name: String to sanitize

    Returns:
        Sanitized string safe for use as filename
    """
    import re
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
    sanitized = sanitized.strip()
    return sanitized[:255]


def get_docx_files(directory: str) -> list[Path]:
    """
    Get all .docx files from a directory.

    Args:
        directory: Directory path to search

    Returns:
        List of Path objects for .docx files
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        return []

    return sorted(dir_path.glob("*.docx"))


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string like "2m 30s" or "45s"
    """
    if seconds < 60:
        return f"{seconds:.1f}s"

    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)

    if minutes < 60:
        return f"{minutes}m {remaining_seconds}s"

    hours = int(minutes // 60)
    remaining_minutes = int(minutes % 60)
    return f"{hours}h {remaining_minutes}m"


class ProgressTracker:
    """Track progress of batch operations."""

    def __init__(self, total: int, description: str = "Processing"):
        """
        Initialize progress tracker.

        Args:
            total: Total number of items
            description: Description of the operation
        """
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = datetime.now()

    def update(self, increment: int = 1):
        """
        Update progress.

        Args:
            increment: Number of items processed
        """
        self.current += increment

    def get_progress_message(self) -> str:
        """
        Get formatted progress message.

        Returns:
            Progress string like "[3/10] Processing... (30%)"
        """
        percentage = (self.current / self.total * 100) if self.total > 0 else 0
        return f"[{self.current}/{self.total}] {self.description}... ({percentage:.1f}%)"

    def get_summary(self) -> str:
        """
        Get summary of completed operation.

        Returns:
            Summary string with duration
        """
        duration = (datetime.now() - self.start_time).total_seconds()
        return f"Completed {self.current}/{self.total} in {format_duration(duration)}"


def validate_credentials(email: Optional[str], password: Optional[str]) -> bool:
    """
    Validate that credentials are provided.

    Args:
        email: Email address
        password: Password

    Returns:
        True if both are provided and non-empty
    """
    return bool(email and email.strip() and password and password.strip())
