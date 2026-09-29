#!/bin/bash
# UserPromptSubmit gate manager.
#
# Un seul etat : le LOCK (~/.claude/state/go-gate.lock).
# Pose quand Bentho annonce explicitement un go a venir ("attends mon go"), leve
# des qu il dit "go". Tant qu il est pose, go-gate-pretool.sh refuse toute action.
#
# Le drapeau "arme par message" a ete retire le 2026-08-07 : voir go-gate-pretool.sh
# pour le bilan (six blocages de travail autorise, zero erreur evitee).
#
# Deux garde-fous appris a l usage, le meme jour :
#  - les messages AUTOMATIQUES du systeme ne doivent jamais changer l etat ;
#  - "pas de go" a l interieur d une phrase n est PAS une consigne d attente
#    (Bentho a ecrit "il n y a pas de go" en parlant d un message precedent, et le
#    hook s est verrouille tout seul, bloquant meme sa propre levee).

LOCK="$HOME/.claude/state/go-gate.lock"
mkdir -p "$HOME/.claude/state"

INPUT="$(cat)"
PROMPT="$(printf '%s' "$INPUT" | python3 -c 'import sys,json
try:
    print(json.load(sys.stdin).get("prompt",""))
except Exception:
    print("")' 2>/dev/null)"
LP="$(printf '%s' "$PROMPT" | tr "[:upper:]" "[:lower:]")"

# --- 0) Message automatique ou illisible : ne toucher a rien.
if [ -z "$LP" ] || printf '%s' "$LP" | grep -Eq "system-reminder|hook additional context|posttooluse|pretooluse|userpromptsubmit|task-notification|<system|the task tools haven|standing output rules|protocole d.activation des skills"; then
  exit 0
fi

# --- 1) HOLD : Bentho demande explicitement d attendre. Formulations directes
# uniquement, jamais une mention de "go" au detour d une phrase.
if printf '%s' "$LP" | grep -Eq "attend[s]? (mon|le|ton) go|j.attends ton go|je te dirai[s]? go|tant qu.?il n.?y a pas de go|jusqu.au go|ne fais rien tant que"; then
  touch "$LOCK"
  exit 0
fi

# --- 2) Un "go" leve le verrou.
if printf '%s' "$LP" | grep -Eq '(^|[^a-z])go([^a-z]|$)'; then
  rm -f "$LOCK"
  exit 0
fi

exit 0
