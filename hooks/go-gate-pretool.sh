#!/bin/bash
# PreToolUse gate.
#
# HARD LOCK UNIQUEMENT : on refuse toute action quand Bentho a explicitement annonce
# un go a venir ("attends mon go"). Le lock est pose et leve par go-gate-prompt.sh.
#
# POURQUOI PAS DE BLOCAGE PAR DEFAUT (decide le 2026-08-07, apres une journee d essai) :
# une version de ce hook exigeait un mot d ordre explicite dans le message courant pour
# toute action modifiante. Bilan reel sur une journee : environ six blocages de travail
# que Bentho avait pourtant autorise, zero erreur evitee. Les vraies fautes de la journee
# (travailler sur la mauvaise page, repondre a cote d une question) etaient des fautes de
# COMPREHENSION, qu un filtre de mots-cles ne peut pas attraper. Le mecanisme coutait du
# temps et de l argent sans rien proteger. Il a donc ete retire.
# Voir aussi le meme constat du 2026-07-01 sur le "verrou par defaut" en mode ask.
#
# Ce qui remplace : lire le message en entier (images comprises), enoncer la cible avant
# d agir, distinguer une question d un ordre. C est du jugement, pas de la mecanique.

LOCK="$HOME/.claude/state/go-gate.lock"
INPUT="$(cat)"

if [ -f "$LOCK" ]; then
  printf '%s' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"VERROU GO actif. Bentho a annonce un go a venir et ne l a pas encore donne. Aucune action tant que le mot go n est pas recu. Repondre uniquement en texte et attendre le go."}}'
  exit 0
fi

exit 0
