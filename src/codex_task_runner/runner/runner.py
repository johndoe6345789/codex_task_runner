"""Compatibility wrapper re-exporting the newer processor/config modules.

The heavy lifting lives in `processor.py` and `config.py`; keep this
module so older imports keep working.
"""

from __future__ import annotations

from .runner_core import Config, process_tasks
from .fsutil import default_run_dir
from .types import MergeMethod


def make_config(
	require_checks: bool,
	method: str,
	keep_branch: bool,
	admin: bool,
	auto: bool,
	dry_run: bool,
	output_dir: str | None,
) -> Config:
	import pathlib

	out = pathlib.Path(output_dir) if output_dir else default_run_dir()
	return Config(
		require_checks=require_checks,
		method=MergeMethod(method),
		delete_branch=not keep_branch,
		admin=admin,
		auto=auto,
		dry_run=dry_run,
		output_dir=out,
	)


__all__ = ["Config", "process_tasks", "make_config"]
