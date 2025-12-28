#!/usr/bin/env python3
"""Thin wrapper script that calls the package helper for publishing to MediaWiki.

This file remains executable for backwards compatibility but delegates logic
to `codex_task_runner.cli_helpers.publish_to_wiki` so the code is importable
and testable.
"""
from __future__ import annotations

import sys
from pathlib import Path

from codex_task_runner.cli_helpers import publish_to_wiki


def main() -> int:
    if len(sys.argv) < 3:
        print('Usage: publish_to_wiki.py USERNAME PASSWORD [PAGE_TITLE_or_PATH]')
        return 2

    username = sys.argv[1]
    password = sys.argv[2]

    # If a third arg is a path, pass it through as docpath; otherwise treat as title
    docpath = None
    title = 'MCP Integration'
    if len(sys.argv) > 3:
        candidate = Path(sys.argv[3])
        if candidate.exists():
            docpath = candidate
        else:
            title = sys.argv[3]

    try:
        res = publish_to_wiki(username=username, password=password, title=title, docpath=docpath)
        print('Edit result:')
        print(res)
        return 0
    except Exception as e:
        print('Publish failed:', e, file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
