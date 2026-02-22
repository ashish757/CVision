"""
Centralized logging configuration for CVision AI Analysis Service
"""
import logging
import sys
from typing import Dict, Any


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure centralized logging for the entire application

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Force remove any existing handlers to prevent conflicts
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Configure root logger with force to override any existing configuration
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
        force=True  # Force reconfigure existing loggers
    )

    # Set specific loggers to the desired level to ensure they show
    modules_to_log = [
        "app.services.text_extraction",
        "app.api.v1.endpoints.text_extraction",
        "app.utils.text_extractor",
        "app.services.analysis",
        "app.api.v1.endpoints.analysis"
    ]

    for module in modules_to_log:
        module_logger = logging.getLogger(module)
        module_logger.setLevel(getattr(logging, log_level.upper()))
        # Ensure the logger propagates to root
        module_logger.propagate = True


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def log_startup_info() -> None:
    """Log application startup information"""
    logger = get_logger(__name__)
    logger.info("=" * 60)
    logger.info("CVision AI Analysis Service - Starting Up")
    logger.info("=" * 60)
    logger.info(f"Root logger level: {logging.getLogger().level}")
    logger.info(f"Root logger handlers: {len(logging.getLogger().handlers)}")
    logger.info("Logging configuration completed successfully")
    logger.info("=" * 60)
