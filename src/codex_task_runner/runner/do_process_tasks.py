from __future__ import annotations

from codex_task_runner.etc.ensure_dir import ensure_dir
from codex_task_runner.etc.config_class import Config
from codex_task_runner.types import TaskRef
from codex_task_runner.process.do_process_one import process_one


def process_tasks(cfg: Config, tasks: list[TaskRef]) -> None:
    ensure_dir(cfg.output_dir)
    for t in tasks:
        process_one(cfg, t)
