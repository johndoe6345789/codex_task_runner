# Codex Task Runner (JSON-driven)

This tool consumes a Codex tasks JSON payload (like the one you pasted), and for each task:

1. Determines the target GitHub repo from `task_status_display.environment_label`.
2. Ensures there is an open pull request for the task:
   - If the task already includes PR metadata in `pull_requests`, it uses that PR number.
   - Otherwise, it attempts to discover the Codex-created branch and opens a PR with `gh pr create`.
3. Merges the PR if it is clean (mergeable with no conflicts), and optionally if checks are green.
4. Moves on to the next task.

## Requirements

- Python 3.11+
- GitHub CLI `gh` on PATH, authenticated:
  - `gh auth login`
  - `gh auth status`

## Install

```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e .
```

## Usage

Input can be a file path or `-` for stdin:

```bash
codex-task-runner process --input tasks.json
cat tasks.json | codex-task-runner process --input -
```

Require checks to be green before merge:

```bash
codex-task-runner process --input tasks.json --require-checks
```

Dry run (no PR creation/merge, only prints actions):

```bash
codex-task-runner process --input tasks.json --dry-run
```

## Branch discovery (when pull_requests is empty)

The Codex payload doesn't always include the head branch name. The runner tries:

- `codex/<slugified-title>`
- Other `codex/*` branches that loosely match the title words
- A fallback search by task id suffix

If it cannot find a matching branch, it logs a SKIP for that task.

## Output

Logs are written to a run directory under your OS temp folder unless `--output-dir` is set.
