#!/bin/bash
# Blocks destructive bash commands before Claude executes them.
#
# 2026-09-03 : CORRECTIF. Le hook lisait la variable d'environnement
# CLAUDE_TOOL_INPUT, qui n'est jamais renseignee : Claude Code passe l'entree du
# hook en JSON sur STDIN. La commande extraite etait donc toujours vide et le
# garde-fou laissait passer tout, y compris `rm -rf`. On lit maintenant stdin,
# avec repli sur la variable d'environnement au cas ou.

INPUT="$(cat)"
[ -z "$INPUT" ] && INPUT="$CLAUDE_TOOL_INPUT"

COMMAND=$(printf '%s' "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    ti = data.get('tool_input') or data
    print(ti.get('command', '') or '')
except Exception:
    print('')
" 2>/dev/null)

[ -z "$COMMAND" ] && exit 0

PATTERNS=(
  "rm -rf"
  "rm -fr"
  "git clean -f"
  "git reset --hard"
  "DROP TABLE"
  "DROP DATABASE"
  "TRUNCATE"
  "delete from"
  "pkill"
  "killall"
)

CMD_LOWER=$(printf '%s' "$COMMAND" | tr '[:upper:]' '[:lower:]')

for pattern in "${PATTERNS[@]}"; do
  pattern_lower=$(printf '%s' "$pattern" | tr '[:upper:]' '[:lower:]')
  if printf '%s' "$CMD_LOWER" | grep -qF "$pattern_lower"; then
    printf '%s' "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"Commande destructive detectee ($pattern). Confirmer manuellement avant execution.\"}}"
    exit 0
  fi
done

exit 0
