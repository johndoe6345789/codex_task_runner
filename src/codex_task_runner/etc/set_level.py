from __future__ import annotations

import logging


def set_level(level: str = "INFO") -> None:
    """Set log level: DEBUG, INFO, WARNING, ERROR.
    
    When DEBUG, console handler also shows debug messages.
    """
    from .get_logger import get_logger
    logger = get_logger()
    lvl = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(lvl)
    # Also update console handler if going to DEBUG
    for handler in logger.handlers:
        if hasattr(handler, 'stream') and handler.stream.name == '<stderr>':
            handler.setLevel(lvl)
