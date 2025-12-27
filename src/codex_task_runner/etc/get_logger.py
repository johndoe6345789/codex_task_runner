from __future__ import annotations

import logging
import os
import sys
from pathlib import Path


_LOG_FILE = Path(os.environ.get("CODEX_LOG_FILE", "codex-task-runner.log"))


def get_logger(name: str = "codex_task_runner") -> logging.Logger:
    """Get or create a logger with console and file handlers."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Console handler - friendly output at INFO level
        console = logging.StreamHandler(sys.stderr)
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(console)
        
        # File handler - detailed output at DEBUG level
        file_handler = logging.FileHandler(_LOG_FILE, mode="a")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        logger.addHandler(file_handler)
        
        logger.setLevel(logging.DEBUG)
    return logger
