# Diagnostics & Feedback Improvements

## Overview
Enhanced error reporting and diagnostic messages throughout the PR creation and merge workflow to provide clearer feedback when operations fail.

## Changes Made

### 1. Enhanced Merge Failure Reporting ([merge_pr.py](../src/codex_task_runner/gh/merge_pr.py))

**Before:**
- `merge_pr()` returned only `bool` (success/failure)
- No information about WHY merge failed
- Silent failures with generic "FAIL: PR #XXX" message

**After:**
- Returns `tuple[bool, str]` with success status and error message
- Captures stderr/stdout from `gh pr merge` command
- Shows actual GitHub CLI error messages to user

**Example Output:**
```
FAIL: PR #385 - pull request is not mergeable: 1 of 1 required status check has not succeeded
```

### 2. Detailed Mergeable Status ([merge_task.py](../src/codex_task_runner/pr/merge_task.py))

**Before:**
- Generic "not mergeable" message
- No indication of CI status or conflicts

**After:**
- Distinguishes between different non-mergeable states:
  - `CONFLICTING`: "has merge conflicts"
  - `UNKNOWN`: "mergeable state unknown (GitHub still calculating)"
  - Failed CI checks: Shows check status
- Provides actionable information

**Example Output:**
```
SKIP: PR #381 has merge conflicts
SKIP: PR #382 not ready (CI checks: FAILURE)
SKIP: PR #383 mergeable state unknown (GitHub still calculating)
```

### 3. Improved PR Discovery Diagnostics ([process_task.py](../src/codex_task_runner/pr/process_task.py))

**Before:**
- Silent failures when PR search fails
- "Could not find PR number" without context

**After:**
- Try/catch blocks with specific error logging
- Shows task ID and expected title when PR not found
- Logs each discovery attempt (API, search, refresh)
- Indicates possible causes for failures

**Example Output:**
```
Searching for PR by title/branch...
Could not find PR with title: Create ToastContainer and config files...
Refreshing task list...
Task task_e_69502aa has no PR numbers after refresh

Could not find PR number after creation
Possible causes: API delay, PR creation failed, or title mismatch
Task: task_e_69502aa77f948331ae8800927e1aa84f
Expected title: Create ToastContainer and config files for sonner integration...
SKIP: no PR
```

## Benefits

1. **Faster Debugging**: Users can immediately see why merges fail without manually checking PR status
2. **Actionable Feedback**: Error messages indicate what needs to be fixed (conflicts, CI, etc.)
3. **Reduced Confusion**: Clear distinction between different failure modes
4. **Better Logging**: Exception handling prevents silent failures during PR discovery

## Testing

All existing tests updated and passing:
- `test_merge_pr.py`: Updated for new return type
- All merge-related tests: 15 passed ✓

## Next Steps

Potential future improvements:
- Add `--verbose` flag for even more detailed output
- Include PR URLs in error messages for quick access
- Add retry logic for transient API failures
- Show estimated time when GitHub is calculating mergeable state
