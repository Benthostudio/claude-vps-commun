#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RELANCE PROJET, hook Stop evenementiel.

Principe tranche par Bentho le 3 septembre 2026. On ne reclame PAS une prochaine
etape a chaque reponse, ce serait absurde quand la reponse est "Oui". Le
declencheur n'est pas la reponse, c'est la case cochee.

Le hook surveille le TACHES.md du projet courant plus la liste perso. Il ne se
reveille que dans deux cas.

1 UNE TACHE VIENT D ETRE COCHEE pendant ce tour, le nombre de [x] a augmente.
  Une etape finie sans etape suivante annoncee, c'est un projet qui s'arrete.
2 PLUS AUCUNE TACHE OUVERTE alors que le fichier existe encore. Une liste vide
  n'est pas une fin de projet, c'est un cadrage a refaire.

Dans ces deux cas seulement, il exige que la reponse nomme la suite. Le reste du
temps il se tait completement.

Etat memorise dans ~/.claude/state/relance-projet.json, une entree par fichier
de taches, pour pouvoir comparer un tour au precedent.
"""

import json
import os
import re
import sys
import unicodedata

HOME = os.path.expanduser("~")
STATE_DIR = os.path.join(HOME, ".claude", "state")
STATE_FILE = os.path.join(STATE_DIR, "relance-projet.json")
PERSO = os.path.join(STATE_DIR, "taches-perso.md")

COCHEE = re.compile(r"^\s*(?:[-*]\s*)?\[[xX]\]", re.M)
OUVERTE = re.compile(r"^\s*(?:[-*]\s*)?\[\s\]", re.M)

# Un placeholder n'est pas une tache. Sans ca, "(vide pour l'instant)" compte
# comme une tache ouverte et le cas 2 ne se declenche jamais.
PLACEHOLDER = re.compile(r"\(\s*vide\b|\baucune?\s+tache\b|\brien\s+pour\s+l", re.I)


def sans_accents(txt):
    forme = unicodedata.normalize("NFD", txt)
    return "".join(c for c in forme if unicodedata.category(c) != "Mn").lower()


# Ce que la reponse doit contenir pour prouver qu'elle pousse la suite.
MARQUEURS = (
    "prochaine etape",
    "prochaine action",
    "prochaine tache",
    "etape suivante",
    "tache suivante",
    "j'enchaine sur",
    "je passe a",
    "⏭",
)


def charger_etat():
    try:
        with open(STATE_FILE, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


def sauver_etat(etat):
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        with open(STATE_FILE, "w", encoding="utf-8") as fh:
            json.dump(etat, fh, ensure_ascii=False, indent=1)
    except Exception:
        pass


def compter(chemin):
    """Rend (cochees, ouvertes) ou None si le fichier n'existe pas."""
    try:
        with open(chemin, encoding="utf-8") as fh:
            txt = fh.read()
    except Exception:
        return None
    ouvertes = [m for m in OUVERTE.finditer(txt)
                if not PLACEHOLDER.search(txt[m.start():txt.find("\n", m.start()) + 1 or len(txt)])]
    return len(COCHEE.findall(txt)), len(ouvertes)


def fichiers_surveilles():
    cwd = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    return [os.path.join(cwd, "TACHES.md"), PERSO]


def derniere_reponse(transcript_path):
    """Texte du dernier message assistant du transcript."""
    if not transcript_path or not os.path.exists(transcript_path):
        return ""
    morceaux = []
    try:
        with open(transcript_path, encoding="utf-8") as fh:
            lignes = fh.readlines()
    except Exception:
        return ""
    for ligne in reversed(lignes[-400:]):
        try:
            evt = json.loads(ligne)
        except Exception:
            continue
        msg = evt.get("message") or {}
        if evt.get("type") == "user" or msg.get("role") == "user":
            break
        if msg.get("role") != "assistant":
            continue
        contenu = msg.get("content")
        if isinstance(contenu, str):
            morceaux.append(contenu)
        elif isinstance(contenu, list):
            for bloc in contenu:
                if isinstance(bloc, dict) and bloc.get("type") == "text":
                    morceaux.append(bloc.get("text", ""))
    return "\n".join(reversed(morceaux))


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    # Ne jamais boucler sur soi-meme.
    if payload.get("stop_hook_active"):
        sys.exit(0)

    etat = charger_etat()
    motifs = []
    change = False

    for chemin in fichiers_surveilles():
        mesure = compter(chemin)
        if mesure is None:
            # Fichier absent, rien a surveiller. On oublie son ancien etat.
            if chemin in etat:
                del etat[chemin]
                change = True
            continue

        cochees, ouvertes = mesure
        avant = etat.get(chemin)
        etat[chemin] = {"cochees": cochees, "ouvertes": ouvertes}
        change = True

        # Premier passage sur ce fichier, on enregistre sans rien reclamer.
        if avant is None:
            continue

        nom = os.path.basename(chemin)
        if cochees > avant.get("cochees", 0):
            motifs.append(
                "%d tache(s) viennent d etre cochees dans %s" % (cochees - avant["cochees"], nom)
            )
        if ouvertes == 0 and avant.get("ouvertes", 0) > 0:
            motifs.append("plus aucune tache ouverte dans %s" % nom)

    if change:
        sauver_etat(etat)

    if not motifs:
        sys.exit(0)

    reponse = sans_accents(derniere_reponse(payload.get("transcript_path")))
    if any(marq in reponse for marq in MARQUEURS):
        sys.exit(0)

    raison = (
        "RELANCE PROJET. " + ", ".join(motifs) + ".\n\n"
        "Une etape finie sans etape suivante annoncee, c est un projet qui s arrete. "
        "Bentho a tranche le 3 septembre 2026, on ne s arrete jamais tant que le projet "
        "n est pas boucle.\n\n"
        "Tu ajoutes UNIQUEMENT la suite, en deux ou trois lignes maximum, jamais un "
        "resume de ce que tu viens de dire, jamais une republication de ta reponse. "
        "Bentho l a deja lue.\n\n"
        "La suite contient, dans cet ordre :\n"
        "1 la prochaine tache, nommee, tiree du TACHES.md et priorisee par echeance\n"
        "2 si elle est bloquee par une information que seul Bentho a, la question exacte "
        "a lui poser, formulee pour qu il puisse repondre en une ligne\n"
        "3 si plus aucune tache n est ouverte, les prochaines etapes que tu proposes, "
        "avec leur echeance, pour qu il les valide\n\n"
        "Tu ecris aussi cette suite dans le TACHES.md avant de repondre, sinon elle "
        "disparait au prochain compactage du contexte."
    )
    print(json.dumps({"decision": "block", "reason": raison}, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
