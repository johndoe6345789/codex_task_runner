# Codex Task Runner

CLI tool for automating Codex Cloud tasks: fetch tasks, create PRs via Codex API, and merge them.

## Features

- **yolo mode**: Full automation - creates PRs for tasks without them, then merges all
- **run**: Process tasks from Codex API with merge options
- **ping**: Test Codex API connectivity
- **tasks**: List tasks from Codex Cloud (aliases: `ls`, `list`)
- **task**: Get details for a specific task (aliases: `t`, `show`)
- **turns**: Get conversation turns for a task
- **patch**: Extract git-apply patch from a task (aliases: `diff`, `p`)
- **archive**: Archive/close a completed task (aliases: `done`, `close`)
- **discover**: Discover API endpoints via browser interception
- **poll**: Poll multiple endpoints

## Task Aliases

Avoid typing long task IDs! Run `ls` first to populate aliases:

```bash
codex-runner ls              # Lists tasks with aliases: 1, 2, 3...
codex-runner t 1             # Show task #1 detail
codex-runner p 1             # Get patch for task #1
codex-runner done 1          # Archive task #1
codex-runner diff 1 --raw | git apply  # Apply patch directly
```

Aliases are stored in `~/.codex-task-cache.json` and refresh each time you run `ls`.

## Requirements

- Python 3.11+
- GitHub CLI `gh` on PATH, authenticated:
  - `gh auth login`
  - `gh auth status`
- `.env` file with Codex session cookies (see `env.template`)
- For `discover` command: Playwright (`pip install playwright playwright-stealth && playwright install chromium`)

## Install

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
python -m pip install -e .
```

## Quick Start

Full automation (create PRs + merge all tasks):

```bash
codex-runner yolo
codex-runner yolo -v  # verbose - shows HTTP traffic
```

Quick workflow with aliases:

```bash
codex-runner ls           # List tasks → get aliases 1,2,3...
codex-runner t 1          # Check task #1 detail
codex-runner p 1 --raw | git apply  # Apply patch locally
codex-runner done 1       # Archive when done
```

## Commands

### yolo - Full Automation

```bash
codex-task-runner yolo                   # Create PRs for tasks without them, merge all
codex-task-runner yolo -v                # Verbose mode (debug logging to console)
codex-task-runner yolo --dry-run         # Preview what would happen
codex-task-runner yolo --limit 10        # Process up to 10 tasks (default: 5)
codex-task-runner yolo --repo owner/repo # Filter to specific repo
codex-task-runner yolo --no-confirm      # Skip confirmation prompt
```

#### Dry Run Output

```
$ codex-task-runner yolo --dry-run
Fetching up to 5 tasks...
Found 5 tasks for johndoe6345789/metabuilder

Tasks to process:
  - johndoe6345789/metabuilder: Add base, advanced, and experimental templates (needs PR)
  - johndoe6345789/metabuilder: Create test files for lua-engine (needs PR)
  - johndoe6345789/metabuilder: Add parser and stats files (needs PR)
  - johndoe6345789/metabuilder: Create builders and mappers files (needs PR)
  - johndoe6345789/metabuilder: Add base, advanced, and experimental CSS files (needs PR)

[1/5] Add base, advanced, and experimental templates
  [DRY RUN] Would create PR
  [DRY RUN] Would dedup
  [DRY RUN] Would merge PR

[2/5] Create test files for lua-engine
  [DRY RUN] Would create PR
  [DRY RUN] Would dedup
  [DRY RUN] Would merge PR

... (3 more tasks)

{
  "created": 5,
  "merged": 5,
  "skipped": 0,
  "failed": 0,
  "dry_run": true
}
```

### run - Process Tasks

```bash
codex-task-runner run                    # Process tasks, prompt before merge
codex-task-runner run --yolo             # Auto-merge without prompts
codex-task-runner run --dry-run          # Show what would happen
codex-task-runner run --require-checks   # Only merge if CI passes
```

### Other Commands

```bash
codex-runner ping                    # Test API connectivity
codex-runner tasks                   # List all tasks (alias: ls)
codex-runner task <id>               # Get task details (alias: t)
codex-runner turns <id>              # Get task turns
codex-runner patch <id>              # Get git patch (alias: p, diff)
codex-runner patch <id> -o out.patch # Save patch to file
codex-runner patch <id> --raw        # Raw patch for piping
codex-runner archive <id>            # Archive task (alias: done, close)
codex-runner discover                # Discover API endpoints (browser)
codex-runner me                      # Current user info (alias: whoami)
codex-runner usage                   # Codex usage stats
codex-runner repos                   # List connected GitHub repos
codex-runner envs                    # List Codex environments
```

**Note:** `<id>` can be a full task ID or a short alias (1, 2, 3...) from `ls`.

## Logging

- **Console**: Clean, friendly messages (INFO level)
- **File**: Full debug output with timestamps to `codex-task-runner.log`
- Set `CODEX_LOG_FILE` env var to change log file path
- Use `-v` flag with yolo for verbose console output

## Environment Setup

Copy `env.template` to `.env` and fill in your Codex session cookies:

```bash
cp env.template .env
# Edit .env with your session values
```

## Architecture

Single-function-per-file design:

```
src/codex_task_runner/
├── cli/          # CLI parsing and dispatch
├── codex/        # Codex API clients (tasks, turns, PRs)
├── gh/           # GitHub API helpers
├── pr/           # PR creation and management
├── handlers/     # Command handlers (yolo, run, ping, etc.)
├── etc/          # Utilities (logging, config, text)
├── proc/         # Process/subprocess helpers
└── runner/       # Core runner logic
```

## End-to-End Workflow

### What happens when you run `codex-task-runner yolo`

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           codex-task-runner yolo                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. AUTHENTICATE                                                             │
│    Load .env → Build requests.Session with cookies + bearer token           │
│    session_from_env('.env') → Session with auth headers                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. FETCH TASKS                                                              │
│    GET /backend-api/wham/tasks/list?limit=20                                │
│    Response: { items: [...], cursor: ... }                                  │
│    Parse into TaskItem objects with task_id, title, pr_numbers, repo        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. ENSURE PRs (for each task without a PR)                                  │
│                                                                             │
│    a. GET /backend-api/wham/tasks/{task_id}/turns                           │
│       Response: { turn_mapping: {...}, current_turn_id: "..." }             │
│                                                                             │
│    b. Extract current_turn_id (the latest assistant turn)                   │
│                                                                             │
│    c. POST /backend-api/wham/tasks/{task_id}/turns/{turn_id}/pr             │
│       Body: {}                                                              │
│       → Codex creates branch, commits code, opens GitHub PR                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 4. MERGE PRs                                                                │
│                                                                             │
│    For each task with a PR:                                                 │
│    a. gh pr view {pr_number} --json mergeable,state                         │
│    b. If mergeable:                                                         │
│       gh pr merge {pr_number} --admin --auto --delete-branch                │
│    c. Log success/failure                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 5. REPORT                                                                   │
│    { processed: 20, merged: 15, prs_created: 5, errors: [...] }             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
.env (cookies/tokens)
        │
        ▼
┌──────────────┐    GET /tasks/list     ┌──────────────┐
│   Session    │ ────────────────────▶  │  Codex API   │
│  (requests)  │ ◀────────────────────  │   (WHAM)     │
└──────────────┘    JSON response       └──────────────┘
        │                                      │
        │ POST /turns/{id}/pr                  │
        │ ─────────────────────────────────────┘
        │                                      
        ▼                                      
┌──────────────┐    gh pr merge         ┌──────────────┐
│   gh CLI     │ ────────────────────▶  │   GitHub     │
│              │ ◀────────────────────  │    API       │
└──────────────┘    PR merged           └──────────────┘
```

### Key Insight: Codex Creates the PR

The critical step is `POST /tasks/{task_id}/turns/{turn_id}/pr`. This tells Codex Cloud to:
1. Take the code changes from that turn
2. Create/update a branch in your GitHub repo
3. Open a Pull Request

We don't create the PR ourselves - we ask Codex to do it, then merge what it creates.
