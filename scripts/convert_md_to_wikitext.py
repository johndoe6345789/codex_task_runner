#!/usr/bin/env python3
"""Thin wrapper that delegates Markdown->wikitext conversion to package helper.

Keeps the original script executable for backwards compatibility while
reusing the importable implementation in `codex_task_runner.cli_helpers`.
"""
from __future__ import annotations

import sys
from pathlib import Path

from codex_task_runner.cli_helpers import convert_md_to_wikitext


def main() -> int:
    src = None
    dest = None
    if len(sys.argv) > 1:
        src = Path(sys.argv[1])
    if len(sys.argv) > 2:
        dest = Path(sys.argv[2])

    try:
        out = convert_md_to_wikitext(src=src, dest=dest)
        print('Wikitext written to', out)
        return 0
    except Exception as e:
        print('Conversion failed:', e, file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
