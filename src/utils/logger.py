"""
Logging utilities for The Robot Driver.
"""

import logging
import sys
from pathlib import Path


def setup_logging(
    level: int = logging.INFO,
    log_file: str = "the_robot_driver.log",
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
) -> None:
    """
    Setup logging configuration for the application.

    Args:
        level: Logging level (default: INFO)
        log_file: Log file name
        log_format: Log message format
    """

    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure root logger
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_dir / log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Set specific logger levels
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("playwright").setLevel(logging.WARNING)