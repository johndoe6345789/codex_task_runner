from __future__ import annotations

from codex_task_runner.etc.append_text import append_text
from codex_task_runner.process.process_format import fmt_task, fmt_pr

# Re-export with underscore prefix for backwards compatibility
_fmt_task = fmt_task
_fmt_pr = fmt_pr


def _log(cfg, msg: str) -> None:
    append_text(cfg.output_dir / "run.log", msg)
