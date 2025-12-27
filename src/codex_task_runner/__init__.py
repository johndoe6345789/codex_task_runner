"""Top-level package helpers for codex_task_runner.

Provides simple, package-level access to per-subpackage module classes.

This module imports the `*Module` classes from each subpackage and exposes
them directly (e.g. `etc = EtcModule`). Keep usage simple and explicit.
"""

from __future__ import annotations

from functools import cached_property
from functools import cached_property


class CodexTaskRunner:
	"""Aggregator exposing each subpackage's module class as an attribute.

	Attributes perform local imports when first accessed to avoid import-time
	side effects.
	"""

	@cached_property
	def branch(self):
		try:
			from .branch.module_class import BranchModule

			return BranchModule
		except Exception:
			from . import branch as _branch

			return _branch

	@cached_property
	def cli(self):
		try:
			from .cli.module_class import CliModule

			return CliModule
		except Exception:
			from . import cli as _cli

			return _cli

	@cached_property
	def codex(self):
		try:
			from .codex.module_class import CodexModule

			return CodexModule
		except Exception:
			from . import codex as _codex

			return _codex

	@cached_property
	def etc(self):
		try:
			from .etc.module_class import EtcModule

			return EtcModule
		except Exception:
			from . import etc as _etc

			return _etc

	@cached_property
	def gh(self):
		try:
			from .gh.module_class import GhModule

			return GhModule
		except Exception:
			from . import gh as _gh

			return _gh

	@cached_property
	def proc(self):
		try:
			from .proc.module_class import ProcModule

			return ProcModule
		except Exception:
			from . import proc as _proc

			return _proc

	@cached_property
	def process(self):
		try:
			from .process.module_class import ProcessModule

			return ProcessModule
		except Exception:
			from . import process as _process

			return _process

	@cached_property
	def runner(self):
		try:
			from .runner.module_class import RunnerModule

			return RunnerModule
		except Exception:
			from . import runner as _runner

			return _runner


__all__ = ["CodexTaskRunner"]
