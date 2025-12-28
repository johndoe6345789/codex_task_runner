#!/usr/bin/env sh
# Shim to delegate to the package CLI
exec python -m codex_task_runner.cli "$@"
set -euo pipefail

PATCHFILE=${1:-patch.diff}
BRANCH=${2:-codex/update-from-poll}
MSG=${3:-"Apply codex poll results"}

if [ ! -f "$PATCHFILE" ]; then
  echo "Patch file not found: $PATCHFILE" >&2
  exit 2
fi

git checkout -b "$BRANCH"
git apply --index "$PATCHFILE"
git add -A
git commit -m "$MSG"
git push -u origin "$BRANCH"

echo "Branch pushed: $BRANCH"
echo "Create PR with: gh pr create --fill --base main --head $BRANCH"
