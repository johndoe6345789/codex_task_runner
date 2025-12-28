#!/usr/bin/env python3
"""Thin shim to the package CLI.

Kept for backwards compatibility; prefer using the installed console entry
point or `python -m codex_task_runner.cli`.
"""
from __future__ import annotations

import sys

from codex_task_runner.cli.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
