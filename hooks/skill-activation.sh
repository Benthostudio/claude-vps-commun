#!/usr/bin/env bash
# UserPromptSubmit hook: injects the StudioMakers skill-activation protocol every
# turn, so the reflex is enforced by the harness (not left to memory). This is the
# METHOD (detect + recommend + record), not a fixed list of skills. Output goes
# into the model context via hookSpecificOutput.additionalContext.

cat <<'JSON'
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "PROTOCOLE D'ACTIVATION DES SKILLS (StudioMakers, s'applique a CHAQUE tour, non-negociable):\n1. NOUVEAU PROJET (des que le contexte est charge): AVANT de construire quoi que ce soit, evaluer les besoins reels du projet et sortir a Bentho la liste des skills pertinents, en distinguant: (a) skills StudioMakers deja crees, (b) skills tiers deja installes qui collent au besoin, (c) skill utile qui n'existe PAS encore -> proposer de le CREER via skill-creator (ou d'en installer un). Faire valider la liste par Bentho, puis l'inscrire dans le CLAUDE.md du projet sous un bloc '## Skills du projet'.\n2. AVANT TOUT LIVRABLE substantiel: INVOQUER reellement les skills pertinents via l'outil Skill (pas seulement les citer). Regles dures: toute page landing / conversion / UX -> lancer page-cro PUIS l'agent ux-cro-auditor AVANT de livrer; tout livrable destine au client -> lancer coherence-reviewer avant envoi.\n3. Si le CLAUDE.md du projet liste deja des 'Skills du projet', les honorer a chaque tour et les relancer aux moments cles (le detail d'un skill se dilue quand le contexte se compacte).\n4. Ne jamais livrer une page censee convertir sans avoir passe l'audit CRO. Si un skill pertinent a ete saute, le dire explicitement a Bentho plutot que de livrer en silence.\n5. Ce protocole est la METHODE (detecter + recommander + enregistrer), il ne fige aucun skill en particulier: a chaque nouveau besoin, re-scanner ce qui pourrait etre utile."
  }
}
JSON
