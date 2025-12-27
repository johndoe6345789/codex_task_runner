"""Compatibility wrapper re-exporting small fs helpers."""

from .default_run_dir import default_run_dir
from .ensure_dir import ensure_dir
from .append_text import append_text

__all__ = ["default_run_dir", "ensure_dir", "append_text"]
