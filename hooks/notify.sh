#!/bin/bash
# macOS native notification when Claude finishes a task

osascript -e 'display notification "Tâche terminée ✓" with title "Claude Code" sound name "Glass"' 2>/dev/null

exit 0
