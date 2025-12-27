from __future__ import annotations

import logging


def set_level(level: str = "INFO") -> None:
    """Set log level: DEBUG, INFO, WARNING, ERROR."""
    from .get_logger import get_logger
    logger = get_logger()
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
