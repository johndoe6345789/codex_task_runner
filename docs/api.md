# API Reference

This file summarizes the main public modules and functions.

## Handlers (`src/codex_task_runner/handlers/`)

### `prompt.py`
- `handle(args, session) -> dict`: Create new Codex task from prompt
  - Sends prompt to Codex API via `POST /wham/tasks`
  - Auto-detects environment if not specified
  - Returns created task details

### `yolo.py`
- `handle(args, session) -> dict`: Full automation mode
  - Fetches tasks from Codex API
  - Creates PRs for tasks without them via `ensure_prs()`
  - Merges all PRs with admin/auto/skip-checks

### `run.py`
- `handle(args, session) -> dict`: Process tasks with configurable merge behavior

### `ping.py`
- `handle(args, session) -> dict`: Test Codex API connectivity

### `tasks.py` / `task.py` / `turns.py`
- List tasks, get task details, get task turns

## Codex API (`src/codex_task_runner/codex/`)

### `codex_session.py`
- `session_from_env(env_path: str) -> requests.Session`: Build authenticated session from `.env`

### `codex_tasks_list.py`
- `get_tasks_list(session, limit: int) -> list[TaskItem]`: Fetch tasks from API

### `codex_turns.py`
- `get_turns(session, task_id: str) -> dict`: Get turns for a task

### `codex_create_pr.py`
- `create_pr_for_turn(session, task_id, turn_id) -> dict`: Create PR via Codex API

### `codex_create_task.py`
- `create_task(session, prompt, env_id, branch, best_of) -> dict`: Create new task via Codex API
- `get_default_environment(session) -> str | None`: Get most recently used environment ID

### `json_get.py` / `json_post.py`
- HTTP helpers with debug logging

## PR Management (`src/codex_task_runner/pr/`)

### `ensure_prs.py`
- `ensure_prs(session, tasks) -> dict`: Create PRs for tasks that don't have them
  - Returns `{"created": int, "skipped": int, "errors": list}`

## GitHub API (`src/codex_task_runner/gh/`)

### `gh_api.py`
- `list_branches(repo: str, limit: int) -> list`: List branches via `gh` CLI
- `get_pr(owner: str, repo: str, pr_number: int) -> dict`: Get PR details

## Logging (`src/codex_task_runner/etc/`)

### `get_logger.py`
- `get_logger(name: str) -> logging.Logger`: Get logger with console + file handlers
  - Console: INFO level, clean messages
  - File: DEBUG level, full timestamps to `codex-task-runner.log`

### `set_level.py`
- `set_level(level: str)`: Set log level (DEBUG/INFO/WARNING/ERROR)

### `log.py`
- Module-level `log` instance for import

## CLI (`src/codex_task_runner/cli/`)

### `cli.py`
- `main()`: CLI entrypoint
- Dispatches to handlers based on subcommand

### `cli_map.json`
- Command definitions with arguments and flags

## Other utility modules

- `branch_finder.py`: heuristics for locating branch names in repos and tasks.
- `fsutil.py`: filesystem helpers used by the runner.
- `proc.py`: subprocess helpers used for running `gh` commands.
- `io.py`, `codex_json.py`, `textutil.py`, `timeutil.py`, `types.py`: small helpers and types used across the project.

## Scripts

- `scripts/poll_codex.py`:
  - Example usage:

```bash
./venv/bin/python scripts/poll_codex.py urls.txt run_poll.json
```

- `scripts/git_patch.sh`:
  - Helper to apply patches locally and create a `gh` PR; adapt for your workflow.

- **Codex endpoints**: See `docs/codex_endpoints.md` for observed backend endpoints and best-effort JSON schemas.

## Examples

Build a session from `.env` and ping the main Codex page (python snippet):

```python
from codex_task_runner.codex_cloud import session_from_env, ping_url

session = session_from_env('.env')
res = ping_url(session, 'https://chatgpt.com/codex/')
print(res)
```

## Next steps / TODOs

- Expand this reference with per-function parameter details and return shapes.
- Optionally scaffold Sphinx or MkDocs for HTML docs.
- Add cross-links from `README.md` to these docs.

---

If you want, I can:
- Expand every exported function with full signatures and examples, or
- Scaffold an MkDocs site and add a `mkdocs.yml` + GitHub Actions publish workflow.

Tell me which option you prefer.