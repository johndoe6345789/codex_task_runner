#!/usr/bin/env python3
"""Wrapper script that delegates compute_coverage to package helper."""
from __future__ import annotations

import sys
from pathlib import Path

from codex_task_runner.cli_helpers import compute_coverage


def main() -> int:
    try:
        res = compute_coverage()
    except Exception as e:
        print('Error computing coverage:', e)
        return 1

    react_names = res['react_names']
    qml_names = res['qml_names']
    matched = res['matched']
    missing = res['missing']

    print('React components found:', len(react_names))
    print('QML registered components:', len(qml_names))
    print('Matched:', len(matched))
    print('Missing:', len(missing))
    print('\nMatched list:')
    for a, b in matched:
        print(a, '->', b)
    print('\nMissing list:')
    for m in sorted(missing):
        print(m)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
