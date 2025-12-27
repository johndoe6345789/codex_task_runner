from __future__ import annotations

from typing import List

from .ensure_dir import ensure_dir
from .process_one import process_one
from .types import TaskRef
from .config import Config


def process_tasks(cfg: Config, tasks: list[TaskRef]) -> None:
    ensure_dir(cfg.output_dir)
    for t in tasks:
        process_one(cfg, t)
