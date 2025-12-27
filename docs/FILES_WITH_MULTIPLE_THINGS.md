**Files With Multiple Things**

This document tracks Python files with multiple top-level definitions (functions/classes).
Files with cohesive, related functions are acceptable and marked as such.

## Files Needing Review

| Count | File | Status |
|-------|------|--------|
| 7 | [src/codex_task_runner/cli/cli_clean_impl.py](../src/codex_task_runner/cli/cli_clean_impl.py) | ✅ Refactored - delegates to handlers |
| 7 | [src/codex_task_runner/process/process_one.py](../src/codex_task_runner/process/process_one.py) | ✅ Cohesive - all functions work together for task processing |
| 7 | [src/codex_task_runner/runner/runner_core.py](../src/codex_task_runner/runner/runner_core.py) | ✅ Refactored - Config moved to etc/config.py |

## Cohesive Modules (No Refactoring Needed)

These files have multiple functions that belong together:

- **5:** [src/codex_task_runner/gh/gh_api_cli.py](../src/codex_task_runner/gh/gh_api_cli.py) — GitHub CLI operations with private helpers
- **4:** [src/codex_task_runner/branch/branch_fuzzy.py](../src/codex_task_runner/branch/branch_fuzzy.py) — Fuzzy branch matching functions
- **4:** [src/codex_task_runner/gh/gh_api_graphql.py](../src/codex_task_runner/gh/gh_api_graphql.py) — GraphQL query and parsing
- **3:** [src/codex_task_runner/gh/gh_api_helpers.py](../src/codex_task_runner/gh/gh_api_helpers.py) — Low-level API helpers
- **2:** [src/codex_task_runner/cli/cli_clean.py](../src/codex_task_runner/cli/cli_clean.py) — Parser and main entry point
- **2:** [src/codex_task_runner/codex/codex_http.py](../src/codex_task_runner/codex/codex_http.py) — HTTP GET/POST helpers
- **2:** [src/codex_task_runner/codex/codex_parse_prs.py](../src/codex_task_runner/codex/codex_parse_prs.py) — PR number extraction
- **2:** [src/codex_task_runner/codex/codex_parse_tasks.py](../src/codex_task_runner/codex/codex_parse_tasks.py) — Task parsing functions
- **2:** [src/codex_task_runner/etc/config.py](../src/codex_task_runner/etc/config.py) — Config dataclass and factory
- **2:** [src/codex_task_runner/proc/proc_run.py](../src/codex_task_runner/proc/proc_run.py) — Process running helpers
- **2:** [src/codex_task_runner/process/process_format.py](../src/codex_task_runner/process/process_format.py) — Formatting functions

## Refactoring Summary

1. **runner_core.py**: Removed duplicate `Config` class, now imports from `etc/config.py`
2. **runner.py**: Simplified to re-export from `runner_core` and `etc/config`
3. **runner_io.py**: Now uses `process_format.py` for formatting, no duplication
4. **cli_clean_impl.py**: Delegates to handler modules instead of duplicating logic
5. **handlers/**: Fixed import paths to use `codex.codex_cloud` correctly
