"""Parse YOLO command arguments."""
from typing import Any, NamedTuple


class YoloArgs(NamedTuple):
    """Parsed YOLO arguments."""
    limit: int
    repo_filter: str | None
    no_confirm: bool
    dry_run: bool
    verbose: bool


def parse_yolo_args(args: Any) -> YoloArgs:
    """Extract YOLO args with defaults."""
    return YoloArgs(
        limit=getattr(args, "limit", 5) or 5,
        repo_filter=getattr(args, "repo", None),
        no_confirm=getattr(args, "no_confirm", False),
        dry_run=getattr(args, "dry_run", False),
        verbose=getattr(args, "verbose", False),
    )
