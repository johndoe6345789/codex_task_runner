#!/usr/bin/env python3
"""Wrapper that calls `codex_task_runner.cli_helpers.run_codex_to_github`."""
from __future__ import annotations

import sys
from codex_task_runner.cli_helpers import run_codex_to_github


def main(argv: list[str] | None = None) -> int:
    # Keep default behavior: env '.env', dry_run True
    try:
        n = run_codex_to_github()
        if n == 0:
            print('No tasks found or request failed.')
            return 1
        print(f'Processed {n} tasks (dry-run).')
        return 0
    except Exception as e:
        print('Run failed:', e)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
