# Codex Task Runner

CLI tool for automating Codex Cloud tasks: fetch tasks, create PRs via Codex API, and merge them.

## Features

- **yolo mode**: Full automation - creates PRs for tasks without them, then merges all
- **run**: Process tasks from Codex API with merge options
- **ping**: Test Codex API connectivity
- **tasks**: List tasks from Codex Cloud
- **task**: Get details for a specific task
- **turns**: Get conversation turns for a task
- **poll**: Poll multiple endpoints

## Requirements

- Python 3.11+
- GitHub CLI `gh` on PATH, authenticated:
  - `gh auth login`
  - `gh auth status`
- `.env` file with Codex session cookies (see `env.template`)

## Install

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
python -m pip install -e .
```

## Quick Start

Full automation (create PRs + merge all tasks):

```bash
codex-task-runner yolo
codex-task-runner yolo -v  # verbose - shows HTTP traffic
```

## Commands

### yolo - Full Automation

```bash
codex-task-runner yolo           # Create PRs for tasks without them, merge all
codex-task-runner yolo -v        # Verbose mode (debug logging to console)
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
codex-task-runner ping              # Test API connectivity
codex-task-runner tasks             # List all tasks
codex-task-runner task <task_id>    # Get task details
codex-task-runner turns <task_id>   # Get task turns
```

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
