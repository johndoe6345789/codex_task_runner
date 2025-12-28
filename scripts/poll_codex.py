#!/usr/bin/env python3
"""Thin wrapper delegating to `codex_task_runner.cli_helpers.poll_codex_urls`."""
from __future__ import annotations

import sys
from pathlib import Path

from codex_task_runner.cli_helpers import poll_codex_urls


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    urls_path = 'urls.txt'
    out_path = 'run_poll.json'
    if len(argv) >= 1:
        urls_path = argv[0]
    if len(argv) >= 2:
        out_path = argv[1]

    try:
        out = poll_codex_urls(urls_path=urls_path, out_path=out_path)
        print(f'saved results to {out}')
        return 0
    except Exception as e:
        print('Poll failed:', e)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
