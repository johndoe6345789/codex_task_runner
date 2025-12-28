# Roadmap

Future development ideas for codex-task-runner.

## v0.2 — Quality of Life

- [ ] **Interactive mode** — `codex-runner -i` opens a REPL for rapid task management
- [ ] **Task filtering** — `codex-runner ls --status=completed --since=1d`
- [ ] **Batch operations** — `codex-runner done 1 2 3` or `codex-runner done --all`
- [ ] **Config file** — `~/.codex-runner.yaml` for defaults (repo, verbose, etc.)
- [ ] **Shell completions** — Bash/Zsh/Fish completions for commands and task aliases

## v0.3 — Smarter Patches

- [ ] **Auto-apply patches** — `codex-runner apply 1` runs `git apply` directly
- [ ] **Patch preview** — `codex-runner p 1 --stat` shows diffstat before applying
- [ ] **Conflict detection** — Warn if patch won't apply cleanly to current branch
- [ ] **Multi-turn patches** — Combine patches from all turns in a task
- [ ] **Patch validation** — Syntax check extracted patches before output

## v0.4 — GitHub Integration

- [ ] **Link tasks to issues** — `codex-runner link 1 --issue=42`
- [ ] **Auto-assign reviewers** — Use CODEOWNERS or recent contributors
- [ ] **PR templates** — Support repo-specific PR body templates
- [ ] **Status checks** — Wait for CI before merge in yolo mode
- [ ] **Draft PRs** — `codex-runner pr 1 --draft`

## v0.5 — Observability

- [ ] **Task history** — `codex-runner history` shows recent task activity
- [ ] **Metrics** — Track success rate, avg time to PR, etc.
- [ ] **Notifications** — Slack/Discord webhook on task completion
- [ ] **Logs** — Structured logging with levels (debug, info, warn, error)
- [ ] **Dry-run mode** — `codex-runner yolo --dry-run` shows what would happen

## v0.6 — Multi-Repo

- [ ] **Repo aliases** — `codex-runner ls --repo=frontend`
- [ ] **Cross-repo tasks** — Handle tasks spanning multiple repositories
- [ ] **Workspace config** — `.codex-runner.yaml` in repo root
- [ ] **Monorepo support** — Route patches to correct package/module

## v1.0 — Desktop UI (PyQt6 + QML)

- [ ] **Task list view** — QML ListView with task cards showing status, title, timestamps
- [ ] **Task detail panel** — Side panel with turns, output items, patch preview
- [ ] **Quick actions toolbar** — Archive, PR, Apply Patch with keyboard shortcuts
- [ ] **System tray** — Background polling with notifications on task completion
- [ ] **Dark/light theme** — Follow system preference or manual toggle
- [ ] **Patch diff viewer** — Syntax-highlighted diff with line numbers
- [ ] **Drag-and-drop** — Reorder tasks, drag patch to IDE
- [ ] **Search/filter bar** — Full-text search across tasks and turns
- [ ] **Settings dialog** — Configure API credentials, polling interval, repo defaults
- [ ] **Keyboard navigation** — Vim-style j/k, quick-switch with number keys

### Task Creation Challenge

**Discovery:** Task creation uses WebSocket (`wss://ws.chatgpt.com/ws/user/{user_id}`), not REST.

Options for "Send Prompt" feature:
1. **Embedded Browser** (QWebEngineView) — Open Codex in a browser widget, let user interact naturally
2. **WebSocket Client** — Reverse-engineer the protocol (complex, may break)
3. **Playwright Automation** — Script browser actions (fragile, resource-heavy)
4. **Defer** — Focus on task management (list, detail, archive, PR, patch) first

**Recommended approach for v1.0:** Use embedded browser for task creation, native UI for everything else.

### UI Architecture
```
src/codex_task_runner/
  ui/
    main.py           # QApplication entry point
    qml/
      Main.qml        # Root window with StackView
      TaskList.qml    # Task list with delegates
      TaskDetail.qml  # Detail view with tabs
      PatchView.qml   # Diff viewer component
      Settings.qml    # Config dialog
      CreateTask.qml  # Embedded browser for task creation
    models/
      task_model.py   # QAbstractListModel for tasks
      turn_model.py   # Model for task turns
    controllers/
      app_controller.py   # Main controller exposed to QML
      task_controller.py  # Task operations (archive, PR, etc.)
    services/
      api_service.py      # REST API calls (tasks, turns, archive, PR)
      polling_service.py  # Background task list refresh
```

### Dependencies
- PyQt6 / PySide6
- PyQt6-WebEngine (for embedded browser)
- PyQt6-QML
- pygments (syntax highlighting)

---

## Future Ideas

### Browser Extension
- Quick-archive from Codex web UI
- Copy task ID with one click
- Show task alias numbers in UI

### Native Codex CLI Integration
- If OpenAI releases official CLI, provide migration path
- Plugin architecture for custom handlers

### AI Enhancements
- Auto-summarize task turns for PR description
- Suggest reviewers based on changed files
- Detect duplicate/related tasks

### Performance
- Parallel task fetching
- Response caching with TTL
- Lazy loading for large task lists

---

## Contributing

Ideas welcome! Open an issue or PR to discuss new features.
