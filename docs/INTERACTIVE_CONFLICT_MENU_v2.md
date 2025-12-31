# Interactive Conflict Menu - Complete Guide

## Overview
When merge conflicts or other PR blockers are detected, the tool shows an interactive menu with 7 options for handling each situation.

## Menu Display

When a PR can't be merged, you'll see:

```
======================================================================
⚠️  PR #381 Cannot Be Merged
======================================================================
Task: Add MenuItemList, Header, and NavSections
Reason: PR #381 has merge conflicts
======================================================================

What would you like to do?

  1. Create follow-up task to fix the issue
  2. Skip this PR and continue
  3. View PR details
  4. Retry merge (if issue was just fixed)
  5. Abort processing all tasks
  6. Add task to blocklist (never process again)
  7. Accept incoming changes (force merge)

Enter choice (1-7): 
```

## Menu Options

### 1. Create Follow-Up Task
Creates a new Codex task to fix the conflict:
```
Creating follow-up task...
✓ Created follow-up task: task_e_69502bb12345678
  Prompt: Fix merge conflicts in PR #381...
```

The tool automatically generates an intelligent prompt based on the failure type:
- **Merge conflicts**: Provides conflict resolution steps
- **CI failures**: Suggests checking test logs
- **Not ready**: Explains approval/review requirements

### 2. Skip This PR
Skips the PR and continues with remaining tasks:
```
Skipping PR #381
```

Use this when you want to handle the PR manually later.

### 3. View PR Details
Shows helpful actions based on the conflict type, then redisplays the menu:

**For merge conflicts:**
```
📋 Suggested Actions:
   PR URL: https://github.com/user/repo/pull/381

   To fix merge conflicts:
   1. Check out the PR branch locally
   2. Run: git merge main (or target branch)
   3. Resolve conflicts in your editor
   4. Run: git add . && git commit
   5. Push the changes
```

**For CI failures:**
```
📋 Suggested Actions:
   PR URL: https://github.com/user/repo/pull/381

   To fix CI failures:
   1. View the failing checks on GitHub
   2. Fix the test/lint issues locally
   3. Push the fixes
```

### 4. Retry Merge
Attempts to merge the PR again (useful if you just fixed it externally):
```
Retrying merge...
[Attempts merge again]
```

### 5. Abort Processing
Stops processing all remaining tasks:
```
User aborted processing
```

Use this when you want to stop the entire yolo run.

### 6. Add Task to Blocklist (NEW)
Permanently blocks the task from being processed in future runs:
```
Adding task task-abc123 to blocklist
✓ Task task-abc123 added to blocklist
```

**Features:**
- Blocklist persists across runs in `~/.config/codex-task-runner/blocklist.json`
- Blocked tasks are automatically skipped at the start of processing
- Use this for tasks that should never be auto-processed (e.g., require manual intervention)

**Managing the blocklist:**
```bash
# View blocklist file
cat ~/.config/codex-task-runner/blocklist.json

# Clear blocklist manually
rm ~/.config/codex-task-runner/blocklist.json
```

### 7. Accept Incoming Changes (NEW)
Force merges the PR by accepting all incoming changes:
```
Accepting incoming changes for PR #381
  Fetching PR #381 branch: feature/add-components
  Merging with strategy 'theirs' (accept incoming)
  Pushing merged changes
  Attempting to merge PR #381 on GitHub
✓ MERGED PR #381 (with incoming changes accepted)
```

**How it works:**
1. Checks out the PR branch locally
2. Merges with `-X theirs` strategy (accepts all conflicts from the PR)
3. Pushes the resolved merge
4. Attempts to merge the PR on GitHub

**When to use:**
- You trust the PR changes completely
- The PR changes should always win in conflicts
- You want to force merge despite conflicts

**Warning:** This overwrites conflicting changes from the base branch with the PR's version. Use with caution!

## Usage Examples

### Example 1: Create Follow-Up Task
```
What would you like to do?
Enter choice (1-7): 1

Creating follow-up task...
✓ Created follow-up task: task_e_12345
  Prompt: Fix merge conflicts in PR #381
  The PR "Add MenuItemList..." has merge conflicts that need resolution...
```

### Example 2: Skip and Continue
```
What would you like to do?
Enter choice (1-7): 2

Skipping PR #381

[Continues to next task]
```

### Example 3: Add to Blocklist
```
What would you like to do?
Enter choice (1-7): 6

Adding task task-abc123 to blocklist
✓ Task added to blocklist at ~/.config/codex-task-runner/blocklist.json

[Continues to next task]
```

### Example 4: Accept Incoming Changes
```
What would you like to do?
Enter choice (1-7): 7

Accepting incoming changes for PR #381
  Fetching PR branch...
  Merging with 'theirs' strategy...
  Pushing changes...
✓ MERGED PR #381

[Continues to next task]
```

## Non-Interactive Mode

To disable the menu entirely and handle conflicts automatically:

```bash
# Auto-create follow-ups without prompting
codex-runner yolo --non-interactive --create-followup

# Non-interactive without follow-ups (just skip)
codex-runner yolo --non-interactive
```

## Blocklist Management

The blocklist is stored in `~/.config/codex-task-runner/blocklist.json`:

```json
{
  "blocked_tasks": [
    "task-abc123",
    "task-def456",
    "task-xyz789"
  ]
}
```

**Checking blocked tasks:**
```bash
# View the blocklist
cat ~/.config/codex-task-runner/blocklist.json | jq .

# Count blocked tasks
cat ~/.config/codex-task-runner/blocklist.json | jq '.blocked_tasks | length'
```

**Removing from blocklist:**
Edit the JSON file directly and remove task IDs, or delete the file entirely to clear it.

## When to Use Each Option

| Option | When to Use |
|--------|-------------|
| **1. Follow-up** | Want to track fixing the issue as a separate task |
| **2. Skip** | Will handle manually later, don't create task |
| **3. View** | Need guidance on how to fix the issue |
| **4. Retry** | Just fixed the issue externally, try again |
| **5. Abort** | Something's wrong, stop everything |
| **6. Blocklist** | Task should never be auto-processed |
| **7. Accept incoming** | PR changes are correct, force merge |

## Error Handling

If accept incoming changes fails:
```
Accepting incoming changes for PR #381
  Fetching PR branch...
  Error: Failed to checkout PR: branch not found
```
The menu will reappear so you can choose another option.

## Tips

1. **Use follow-ups** for complex conflicts that need investigation
2. **Use blocklist** for tasks that repeatedly fail or need special handling
3. **Use accept incoming** only when you're confident the PR is correct
4. **Use view** to learn about the specific issue before deciding
5. **Check the blocklist** periodically to clean up old entries

## Configuration

The interactive menu is enabled by default. Control it with flags:

```bash
# Default: interactive
codex-runner yolo

# Disable menu
codex-runner yolo --non-interactive

# Disable and auto-create follow-ups
codex-runner yolo --non-interactive --create-followup
```

## Troubleshooting

**Menu doesn't appear:**
- Check that you're not using `--non-interactive` flag
- Verify the conflict is actionable (has merge conflicts, CI failure, etc.)

**Blocklist not persisting:**
- Check permissions on `~/.config/codex-task-runner/`
- Ensure the directory exists: `mkdir -p ~/.config/codex-task-runner`

**Accept incoming fails:**
- Ensure `gh` CLI is installed and authenticated
- Verify you have write access to the repository
- Check that the base branch name is correct (defaults to `main`)
