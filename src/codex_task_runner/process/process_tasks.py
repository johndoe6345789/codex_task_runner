from __future__ import annotations

from typing import List

from codex_task_runner.etc.ensure_dir import ensure_dir
from .do_process_one import process_one
from codex_task_runner.types import TaskRef
from codex_task_runner.etc.config_class import Config


def process_tasks(cfg: Config, tasks: list[TaskRef]) -> None:
    ensure_dir(cfg.output_dir)
    for t in tasks:
        process_one(cfg, t)
