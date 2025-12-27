"""Top-level package helpers for codex_task_runner.

Provides simple, package-level access to per-subpackage module classes.

This module imports the `*Module` classes from each subpackage and exposes
them directly (e.g. `etc = EtcModule`). Keep usage simple and explicit.
"""

from .branch.module_class import BranchModule
from .cli.module_class import CliModule
from .codex.module_class import CodexModule
from .etc.module_class import EtcModule
from .gh.module_class import GhModule
from .proc.module_class import ProcModule
from .process.module_class import ProcessModule
from .runner.module_class import RunnerModule

class CodexTaskRunner:
	"""Aggregator exposing each subpackage's module class as an attribute.

	Attributes perform local imports when first accessed to avoid import-time
	side effects.
	"""

	BranchModule = BranchModule
	CliModule = CliModule
	CodexModule = CodexModule
	EtcModule = EtcModule
	GhModule = GhModule
	ProcModule = ProcModule
	ProcessModule = ProcessModule
	RunnerModule = RunnerModule
	

__all__ = ["CodexTaskRunner"]
