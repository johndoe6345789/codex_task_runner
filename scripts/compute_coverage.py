#!/usr/bin/env python3
"""Compatibility shim: delegate to package CLI.

This file is a lightweight stub kept for compatibility; it forwards
invocations to `codex_task_runner.cli.cli`.
"""
from __future__ import annotations


import sys

from codex_task_runner.cli.cli import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


if __name__ == '__main__':
    raise SystemExit(main())
