# Interactive Conflict Menu

## Overview
When merge conflicts or other PR blockers are detected, the tool can show an interactive numbered menu giving you options for how to handle each situation.

## Example

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

Enter choice (1-5): 
```

## Menu Options

### 1. Create Follow-Up Task
Creates a new Codex task to fix the conflict:
```
Creating follow-up task...
✓ Created follow-up task: task_e_69502bb12345678
  Prompt: Fix merge conflicts in PR #381...
```

### 2. Skip This PR
Skips the PR and continues with remaining tasks:
```
Skipping PR #381
```

### 3. View PR Details
Shows helpful actions based on the conflict type:

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
   PR URL: https://github.com/user/repo/pull/382

   To fix CI failures:
   1. View the failing checks on GitHub
   2. Fix the test/lint issues locally
   3. Push the fixes
```

**For branch protection:**
```
📋 Suggested Actions:
   PR URL: https://github.com/user/repo/pull/383

   To make PR mergeable:
   1. Check branch protection rules
   2. Ensure all required reviews are approved
   3. Wait for required status checks to pass
```

After viewing, the menu shows again so you can choose what to do.

### 4. Retry Merge
Attempts to merge again (useful if you just fixed the issue):
```
Retrying merge...
Merging PR #381...
✓ MERGED PR #381
```

### 5. Abort Processing
Stops processing all remaining tasks:
```
User aborted processing
```

## Usage Modes

### Interactive Mode (Default)
Shows menu for each conflict:
```bash
codex-runner yolo
```

### Batch Mode (Non-Interactive)
Skips conflicts automatically, no menus:
```bash
codex-runner yolo --non-interactive
```

### Auto-Create Follow-Ups
Automatically creates follow-up tasks without showing menus:
```bash
codex-runner yolo --create-followup
```

### Combined Modes
```bash
# Non-interactive + auto-create follow-ups
codex-runner yolo --non-interactive --create-followup

# Interactive but verbose logging
codex-runner yolo -v

# Dry run with menus (for testing)
codex-runner yolo --dry-run
```

## Conflict Summary

At the end of processing, you'll see a summary of all conflicts:

```
======================================================================
Conflict Summary: 3 PRs blocked
======================================================================
  • PR #381: Add MenuItemList, Header, and NavSections
    Reason: PR #381 has merge conflicts
  • PR #382: Split components into separate files
    Reason: PR #382 not ready (CI checks: FAILURE)
  • PR #383: Create FieldGroup and ValidationSummary components
    Reason: PR #383 not mergeable
======================================================================
```

## Workflow Examples

### Example 1: Fix Conflicts Yourself
```
1. PR has conflicts
2. Choose option 3 (View PR details)
3. Follow the suggested steps locally
4. Fix and push
5. Choose option 4 (Retry merge)
6. ✓ PR merges successfully
```

### Example 2: Queue for Later
```
1. PR has CI failures
2. Choose option 1 (Create follow-up task)
3. Continue with other PRs
4. Later run: codex-runner yolo
5. Codex fixes the CI issues
6. New PR merges successfully
```

### Example 3: Batch Processing
```bash
# Process 20 tasks, skip conflicts automatically
codex-runner yolo --limit 20 --non-interactive

# Review conflicts at end
# Come back and handle individually
codex-runner yolo --interactive
```

## Benefits

✅ **Full Control**: Decide how to handle each conflict  
✅ **Context-Aware**: Shows relevant help based on conflict type  
✅ **Flexible**: Interactive or batch mode as needed  
✅ **Efficient**: Handle quick fixes immediately with retry  
✅ **Trackable**: Creates follow-up tasks for complex issues  

## Tips

- **Use interactive mode** when actively monitoring the process
- **Use batch mode** for automated runs (CI, cron jobs, etc.)
- **Use `--create-followup`** to queue all conflicts for later
- **View details first** before choosing to understand the issue
- **Retry is useful** when you fix things in another terminal
