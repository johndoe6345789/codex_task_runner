"""Compatibility wrapper re-exporting split branch finder helpers.

This keeps `find_head_branch` importable from `branch_finder` while the
implementation lives in smaller modules.
"""

from .find_head_branch import find_head_branch

__all__ = ["find_head_branch"]
