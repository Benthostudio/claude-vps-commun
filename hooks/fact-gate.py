#!/usr/bin/env python3
"""Verrou FACTUEL en amont: bloque l'ecriture d'un livrable client tant que l'agent
`verificateur` n'a pas tourne dessus.

Pourquoi ce hook existe (Bentho, 2026-08-24).
Tous les verrous precedents etaient des controles de SORTIE, branches sur l'evenement
Stop. Ils lisent un texte deja ecrit, donc ils ne peuvent verifier que sa FORME: ils
n'ont aucun moyen de savoir si une affirmation est vraie ni si une question a deja sa
reponse quelque part dans le projet. C'est ce trou qui a laisse partir une demande
d'acces au depot GitHub que nous possedons deja, ce qui nous discredite chez le client.

Le seul point d'accroche reellement en amont est PreToolUse: il se declenche AVANT que
l'outil s'execute, et un blocage la n'entraine pas de double reponse (contrairement au
blocage sur Stop, interdit depuis le 19.08). D'ou la regle: tout livrable destine a un
tiers s'ecrit d'abord dans un fichier, et ce fichier ne peut pas etre ecrit tant que le
verificateur n'a pas rendu son verdict.
"""
import json
import os
import re
import sys

STATE = os.path.expanduser("~/.claude/state")
SEEN = os.path.join(STATE, "fact-gate-seen")

# Un livrable destine a un tiers, reconnu soit au nom du fichier soit au contenu.
NAME = re.compile(r"(msg|message|email|mail|courrier|lettre|propos|devis|brief)[-_a-z0-9]*\.(md|txt)$", re.I)
GREETING = re.compile(r"^\s*(Hi|Hello|Dear|Bonjour|Hola|Buenos)\s+[A-ZÁÉÍÓÚÑ][\wáéíóúñ]+", re.M)
ASK = re.compile(
    r"\b(can you (give|send|share|provide)|could you (give|send|share)|"
    r"do you have|access to|give us access|peux[- ]tu (nous )?(donner|envoyer)|"
    r"pourrais[- ]tu|nous avons besoin de|we need (the|your|access))\b",
    re.I,
)


def stdin_json():
    try:
        return json.loads(sys.stdin.read() or "{}")
    except Exception:
        return {}


def verificateur_ran(transcript_path, lookback=60):
    """Vrai si l'agent verificateur a ete lance dans les derniers evenements."""
    if not transcript_path or not os.path.exists(transcript_path):
        return False
    try:
        with open(transcript_path, encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()[-lookback:]
    except Exception:
        return False
    for raw in lines:
        if '"verificateur"' in raw or "subagent_type\\\": \\\"verificateur" in raw:
            return True
    return False


def main():
    data = stdin_json()
    tool = data.get("tool_name", "")
    if tool not in ("Write", "Edit"):
        sys.exit(0)

    ti = data.get("tool_input", {}) or {}
    path = ti.get("file_path", "") or ""
    body = (ti.get("content") or "") + (ti.get("new_string") or "")

    is_deliverable = bool(NAME.search(os.path.basename(path))) or bool(GREETING.search(body))
    if not is_deliverable:
        sys.exit(0)

    # Une seule interception par fichier: sinon la correction demandee par le hook
    # se ferait elle-meme bloquer, et le tour tournerait en rond.
    os.makedirs(STATE, exist_ok=True)
    flag = os.path.join(STATE, "fact-gate-" + re.sub(r"\W+", "_", path)[-80:])
    if os.path.exists(flag):
        sys.exit(0)

    if verificateur_ran(data.get("transcript_path")):
        sys.exit(0)

    open(flag, "w").write("1")

    reason = [
        "VERROU FACTUEL. Ce fichier est un livrable destine a un tiers, or l'agent",
        "`verificateur` n'a pas tourne dessus.",
        "",
        "Avant d'ecrire ce livrable, lance l'agent `verificateur` en lui donnant:",
        "  1. la liste des affirmations qu'il contient",
        "  2. la liste des questions qu'il pose",
        "  3. le chemin du projet",
        "",
        "Il verifie DANS LE PROJET si chaque question a deja sa reponse (contrat,",
        "acces techniques, fichiers, historique) et si chaque fait est sourcé et récent.",
        "Corrige ce qu'il renvoie, PUIS ecris le fichier.",
    ]
    if ASK.search(body):
        reason.insert(2, "Ce livrable demande un acces ou une information: verifie d'abord qu'on ne l'a pas deja.")

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "\n".join(reason),
        }
    }, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
