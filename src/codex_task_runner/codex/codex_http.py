"""Re-exports for backwards compatibility."""

from .json_get import json_get as _json_get
from .json_post import json_post as _json_post

__all__ = ["_json_get", "_json_post"]
