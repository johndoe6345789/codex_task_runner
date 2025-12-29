"""Interactive menu for handling merge conflicts and PR blockers."""
from typing import Optional
from ..etc.log import log


def show_conflict_menu(task, pr_num: int, reason: str) -> str:
    """
    Show interactive menu when PR cannot be merged.
    
    Args:
        task: The task with the blocked PR
        pr_num: PR number
        reason: Why the PR is blocked
    
    Returns:
        Choice: 'followup', 'skip', 'view', 'abort', 'retry'
    """
    print(f"\n{'='*70}")
    print(f"⚠️  PR #{pr_num} Cannot Be Merged")
    print(f"{'='*70}")
    print(f"Task: {task.title[:60]}")
    print(f"Reason: {reason}")
    print(f"{'='*70}\n")
    
    print("What would you like to do?\n")
    print("  1. Create follow-up task to fix the issue")
    print("  2. Skip this PR and continue")
    print("  3. View PR details")
    print("  4. Retry merge (if issue was just fixed)")
    print("  5. Abort processing all tasks")
    print()
    
    while True:
        try:
            choice = input("Enter choice (1-5): ").strip()
            
            if choice == "1":
                return "followup"
            elif choice == "2":
                return "skip"
            elif choice == "3":
                return "view"
            elif choice == "4":
                return "retry"
            elif choice == "5":
                return "abort"
            else:
                print("Invalid choice. Please enter 1-5.")
        except (KeyboardInterrupt, EOFError):
            print("\n\nAborted by user.")
            return "abort"


def show_conflict_actions(pr_url: str, reason: str) -> None:
    """Show helpful actions for resolving the conflict."""
    print(f"\n📋 Suggested Actions:")
    print(f"   PR URL: {pr_url}")
    
    if "merge conflict" in reason.lower():
        print(f"\n   To fix merge conflicts:")
        print(f"   1. Check out the PR branch locally")
        print(f"   2. Run: git merge main (or target branch)")
        print(f"   3. Resolve conflicts in your editor")
        print(f"   4. Run: git add . && git commit")
        print(f"   5. Push the changes")
        
    elif "ci check" in reason.lower() or "status check" in reason.lower():
        print(f"\n   To fix CI failures:")
        print(f"   1. View the failing checks on GitHub")
        print(f"   2. Fix the test/lint issues locally")
        print(f"   3. Push the fixes")
        
    elif "not mergeable" in reason.lower():
        print(f"\n   To make PR mergeable:")
        print(f"   1. Check branch protection rules")
        print(f"   2. Ensure all required reviews are approved")
        print(f"   3. Wait for required status checks to pass")
    
    print()


def get_conflict_summary(tasks_with_conflicts: list) -> str:
    """Generate a summary of all conflicts encountered."""
    if not tasks_with_conflicts:
        return "No conflicts encountered."
    
    summary = ["\n" + "="*70]
    summary.append(f"Conflict Summary: {len(tasks_with_conflicts)} PRs blocked")
    summary.append("="*70)
    
    for task, pr_num, reason in tasks_with_conflicts:
        summary.append(f"  • PR #{pr_num}: {task.title[:50]}")
        summary.append(f"    Reason: {reason}")
    
    summary.append("="*70)
    return "\n".join(summary)
