# Example: Improved Diagnostic Output

## Before vs After Comparison

### Before (Original Output)
```
[3/5] Add MenuItemList, Header, and NavSections
  Found existing PR #381
  Merging PR #381...
  FAIL: PR #381
  Deduplicating...
```

**Issues:**
- No indication WHY it failed
- User must manually check PR status
- No actionable information

### After (Improved Output)

#### Scenario 1: Merge Conflicts
```
[3/5] Add MenuItemList, Header, and NavSections
  Found existing PR #381
  Merging PR #381...
  SKIP: PR #381 has merge conflicts
  Deduplicating...
```

#### Scenario 2: Failed CI Checks
```
[3/5] Add MenuItemList, Header, and NavSections
  Found existing PR #381
  Merging PR #381...
  SKIP: PR #381 not ready (CI checks: FAILURE)
  Deduplicating...
```

#### Scenario 3: Branch Protection Rules
```
[3/5] Add MenuItemList, Header, and NavSections
  Found existing PR #381
  Merging PR #381...
  FAIL: PR #381 - pull request is not mergeable: 1 of 1 required status check has not succeeded
  Deduplicating...
```

#### Scenario 4: GitHub Still Calculating
```
[3/5] Add MenuItemList, Header, and NavSections
  Found existing PR #381
  Merging PR #381...
  SKIP: PR #381 mergeable state unknown (GitHub still calculating)
  Deduplicating...
```

### PR Discovery Failures

#### Before
```
[1/5] Create and organize test files
  Creating PR...
  PR created
  Searching for PR by title/branch...
  Refreshing task list...
  Could not find PR number after creation
  SKIP: no PR
```

#### After
```
[1/5] Create and organize test files
  Creating PR...
  PR created
  Searching for PR by title/branch...
  Could not find PR with title: Create and organize test files...
  Refreshing task list...
  Task task_e_69502aa77f948331ae8800927e1aa84f has no PR numbers after refresh
  
  Could not find PR number after creation
  Possible causes: API delay, PR creation failed, or title mismatch
  Task: task_e_69502aa77f948331ae8800927e1aa84f
  Expected title: Create and organize test files for React hooks testing...
  SKIP: no PR
```

## Summary of Improvements

✅ **Clear failure reasons**: Users know exactly why merges fail  
✅ **Actionable feedback**: CI failures, conflicts, and requirements clearly stated  
✅ **Better debugging**: Task IDs and titles shown for tracking down issues  
✅ **GitHub CLI errors**: Raw error messages from `gh` command shown  
✅ **Exception handling**: No more silent failures during API calls  

## Usage Tips

When you see these messages:

- **"has merge conflicts"** → Resolve conflicts in the PR branch
- **"CI checks: FAILURE"** → Check GitHub Actions/CI logs
- **"mergeable state unknown"** → Wait a moment and retry
- **"not mergeable: X required status check"** → Wait for CI to complete or fix branch protection rules
- **"Could not find PR"** → Check GitHub directly for the PR, may need to manually link it
