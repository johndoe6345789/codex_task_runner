"""Compatibility shim re-exporting text utilities at package root.

Provides `slugify` and `words` for code importing
`codex_task_runner.textutil`.
"""

from .etc.slugify import slugify
from .etc.words import words

__all__ = ["slugify", "words"]
