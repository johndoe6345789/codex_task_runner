# API Reference

This file summarizes the main public modules and useful functions in the project.

## `src/codex_task_runner/gh_api.py`

- `list_branches(repo: str, limit: int = 100) -> list`:
  - Returns a list of branch names for the given `repo`. Handles `404 Not Found` by returning an empty list.

- `get_pr(owner: str, repo: str, pr_number: int) -> dict` (behavior may vary):
  - Fetches PR metadata using `gh` or GitHub APIs. Callers should handle exceptions when the repo or PR is inaccessible.

## `src/codex_task_runner/runner.py`

- `Runner.run()`:
  - Main orchestration: reads tasks, finds branches, opens/merges PRs as configured.
  - `Runner._first_open(repo, nums)` now tolerates failures fetching PRs (won't crash on fetch errors).

## `src/codex_task_runner/codex_cloud.py` (new)

- `session_from_env(env_path: Optional[str] = None) -> requests.Session`:
  - Builds a `requests.Session` using cookie values and tokens from a `.env` file.
  - Adds `x-csrf-token` and best-effort `Authorization: Bearer` header when available.

- `ping_url(session: requests.Session, url: str) -> dict`:
  - Performs a GET and returns status, snippet, and ok flag.

- `poll_urls(session: requests.Session, urls: Sequence[str]) -> list`:
  - Polls multiple backend endpoints and returns a short result list.

- `save_results(path: str, data: Any)`:
  - Utility to write poll results (used by `scripts/poll_codex.py`).

## `src/codex_task_runner/cli.py`

- CLI entrypoints and argument parsing for running the task runner.
- Use the repository `README.md` for examples of invoking the CLI.

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