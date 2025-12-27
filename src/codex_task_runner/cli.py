from __future__ import annotations

import argparse
import sys

from .codex_json import load_tasks
from .io import read_all
from .runner import make_config, process_tasks


def main(argv: list[str] | None = None) -> int:
    ns = _parse(argv or sys.argv[1:])
    raw = read_all(ns.input)
    tasks = load_tasks(raw)
    cfg = make_config(
        require_checks=ns.require_checks,
        method=ns.method,
        keep_branch=ns.keep_branch,
        admin=ns.admin,
        auto=ns.auto,
        dry_run=ns.dry_run,
        output_dir=ns.output_dir,
    )
    process_tasks(cfg, tasks)
    return 0


def _parse(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="codex-task-runner")
    p.add_argument("--input", required=True, help="Path to tasks JSON, or '-'")
    p.add_argument("--require-checks", action="store_true")
    p.add_argument("--method", default="squash",
                   choices=["merge", "squash", "rebase"])
    p.add_argument("--keep-branch", action="store_true")
    p.add_argument("--admin", action="store_true")
    p.add_argument("--auto", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--output-dir", default=None)
    return p.parse_args(argv)
