"""Compatibility shim re-exporting text utilities.

Provides `slugify` and `words` at the package root for existing imports.
"""

from .etc.textutil import slugify, words

__all__ = ["slugify", "words"]
