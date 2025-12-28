# Repository directory tree

This file documents the top-level layout and important subfolders for the repository so automated agents and humans understand the project structure.

Top-level layout:

- env.template: environment template for local development.
- pyproject.toml: Python project metadata and dependencies.
- README.md: high-level project description.
- tasks.json: task runner configuration.
- docs/: documentation (this file and other docs).
- scripts/: helper scripts and CLI wrappers.
- src/: main Python package `codex_task_runner`.
- tests/: unit tests.

Key folders under `src/codex_task_runner/`:

- `branch/` — branch discovery utilities (e.g., `branch_finder.py`, `find_head_branch.py`).
- `cli/` — CLI implementation and parser (`cli.py`, `cli_parser.py`, `cli_commands.py`).
- `codex/` — core Codex/cloud integration modules handling API, sessions, parsing and polling (many `codex_*.py` files).
- `etc/` — misc utilities and helpers (`config.py`, `fsutil.py`, `runner.py`, `task_ref.py`, `textutil.py`).
- `gh/` — GitHub API wrapper and helpers.
- `handlers/` — request/command handlers (create PR, poll, run, tasks, turns).
- `proc/` — process/run result types and helpers.
- `process/` — task processing pipeline (`processor.py`, `process_tasks.py`).
- `runner/` — high-level runner code (`runner.py`, `runner_core.py`).
- `ui/` — Desktop UI implementations (PyQt6 and QML).

UI folder structure (`src/codex_task_runner/ui/`):

- `fakemui/` — PyQt6 MUI-style widget library (Material-UI inspired components).
- `qml/` — QML/Qt Quick UI mirroring the React frontend.
  - `components/` — Reusable UI components (fakemui + app components).
  - `contexts/` — Singleton context providers (Theme, Language, NerdMode, AjaxQueue).

Tests:

- `tests/` contains unit tests such as `test_parse.py` and `test_slugify.py`.

Scripts:

- `scripts/` contains convenience and orchestration scripts: `codex_cli.py`, `run_codex_to_github.py`, `run_tests.py`, etc.

Notes for agents:

- Prefer reading code under `src/codex_task_runner/` for implementation details.
- `docs/` contains human-facing docs (see `api.md`, `codex_endpoints.md`, `index.md`).
- When linking to files, prefer referencing module paths under `src/codex_task_runner/`.

If you'd like, I can expand this file with a full `tree` dump, file-by-file descriptions, or link to specific files with line references.
