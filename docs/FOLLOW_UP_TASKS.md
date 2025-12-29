# Auto-Create Follow-Up Tasks for Non-Mergeable PRs

## Overview
Added a new feature that automatically creates follow-up Codex tasks when PRs cannot be merged. This helps maintain momentum by queuing fix tasks when PRs are blocked by conflicts, CI failures, or other issues.

## Usage

```bash
# Enable follow-up task creation in yolo mode
codex-runner yolo --create-followup

# Preview what would happen
codex-runner yolo --create-followup --dry-run

# With other options
codex-runner yolo --create-followup --limit 10 --verbose
```

## How It Works

1. **PR Merge Attempt**: Tool tries to merge a PR
2. **Failure Detection**: If PR can't be merged, captures the reason:
   - Merge conflicts
   - Failed CI checks
   - Branch protection requirements
   - Other merge blockers

3. **Follow-Up Creation**: If `--create-followup` is enabled:
   - Generates a descriptive prompt based on the failure reason
   - Creates a new Codex task to address the issue
   - Links back to the original PR and task
   - Adds to the queue for processing

## Example Output

### Without `--create-followup`:
```
[3/5] Add MenuItemList, Header, and NavSections
  Found existing PR #381
  Merging PR #381...
  SKIP: PR #381 has merge conflicts
  Deduplicating...
```

### With `--create-followup`:
```
[3/5] Add MenuItemList, Header, and NavSections
  Found existing PR #381
  Merging PR #381...
  SKIP: PR #381 has merge conflicts
  Creating follow-up task to address: PR #381 has merge conflicts
  ✓ Created follow-up task: task_e_69502bb12345678
    Prompt: Fix merge conflicts in PR #381 (https://github.com/user/repo/pull/381)...
  Deduplicating...
```

## Generated Task Prompts

The system generates intelligent prompts based on failure type:

### Merge Conflicts
```
Fix merge conflicts in PR #381 (https://github.com/user/repo/pull/381)

Original task: Add MenuItemList, Header, and NavSections

The PR has merge conflicts that need to be resolved. 
Please resolve the conflicts and update the PR.
```

### CI Failures
```
Fix CI failures in PR #382 (https://github.com/user/repo/pull/382)

Original task: Split components into separate files

The PR has failing CI checks: CI checks: FAILURE
Please fix the test failures or other CI issues and update the PR.
```

### Branch Protection
```
Make PR #383 mergeable (https://github.com/user/repo/pull/383)

Original task: Create FieldGroup and ValidationSummary components

The PR cannot be merged due to: pull request is not mergeable: 1 of 1 required status check has not succeeded
Please address the issues preventing merge and update the PR.
```

## Implementation Details

### New Files
- [create_followup_task.py](../src/codex_task_runner/pr/create_followup_task.py) - Core logic for follow-up task creation

### Modified Files
- [process_task.py](../src/codex_task_runner/pr/process_task.py) - Added `create_followup` parameter
- [process_all_tasks.py](../src/codex_task_runner/pr/process_all_tasks.py) - Passes through `create_followup` flag
- [parse_yolo_args.py](../src/codex_task_runner/etc/parse_yolo_args.py) - Added `create_followup` to YoloArgs
- [yolo.py](../src/codex_task_runner/handlers/yolo.py) - Passes `create_followup` to processor
- [cli_map.json](../src/codex_task_runner/cli/cli_map.json) - Added `--create-followup` CLI flag
- [config_class.py](../src/codex_task_runner/etc/config_class.py) - Added config option

### API Function
```python
def create_followup_task(
    session,
    task,
    pr_num: int,
    reason: str,
    auto_create: bool = False
) -> Optional[dict]:
    """
    Create a follow-up task to address why a PR isn't mergeable.
    
    Returns:
        Created task response or None
    """
```

## Configuration

### Config Class
```python
@dataclass(frozen=True)
class Config:
    # ... other fields ...
    create_followup_tasks: bool = False  # Auto-create tasks for non-mergeable PRs
```

### CLI Argument
```json
{
  "flags": ["--create-followup"],
  "kwargs": {
    "action": "store_true",
    "help": "Auto-create follow-up tasks for non-mergeable PRs"
  }
}
```

## Benefits

1. **Maintains Momentum**: Issues don't get forgotten - they're automatically queued for fixing
2. **Clear Context**: Follow-up tasks link to original PR and explain the problem
3. **Opt-In**: Only creates follow-ups when explicitly requested with `--create-followup`
4. **Intelligent**: Generates different prompts based on failure type
5. **Trackable**: All follow-up tasks are regular Codex tasks that can be viewed/managed

## Future Enhancements

Potential improvements:
- [ ] Priority levels for follow-up tasks
- [ ] Link follow-ups to original tasks in both directions
- [ ] Retry logic with exponential backoff
- [ ] Batch follow-up creation summary
- [ ] Custom prompt templates
- [ ] Integration with issue trackers

## Example Workflow

```bash
# Run yolo mode with follow-up creation
$ codex-runner yolo --create-followup

# System processes 5 tasks
# 2 merge successfully
# 3 have issues:
#   - PR #381: merge conflicts → creates followup task_a
#   - PR #382: CI failure → creates followup task_b  
#   - PR #383: not mergeable → creates followup task_c

# Later, run again to process the follow-ups
$ codex-runner yolo --create-followup

# Now processing task_a, task_b, task_c
# They create PRs that fix the original issues
# Original PRs can now be merged
```

## Notes

- Follow-up tasks use the same environment/branch as the original task
- Skips creating follow-ups for already-closed or merged PRs
- Works in both `yolo` and `run` modes
- Compatible with `--dry-run` for testing
