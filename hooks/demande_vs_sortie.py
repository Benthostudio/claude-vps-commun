#!/usr/bin/env python3
"""
CONTROLE DE CORRESPONDANCE DEMANDE CONTRE SORTIE.

Demande de Bentho, 2026-08-25 : "mets en place ce controle". Constat qui l'a
declenche : tous les verrous existants (lint-draft, output-verifier) verifient
la FORME du texte, jamais si le texte repond a la demande. Deux fautes ce
soir la, aucune attrapee par un verrou :
  1. "etape par etape" demande, sections de la page livrees a la place
  2. duree ajoutee dans un message client alors que Bentho ne l'a jamais demandee

Ce module lit le DERNIER message de Bentho dans le transcript de la session en
cours, puis compare la sortie a cette demande. Il n'essaie pas de juger le fond,
il attrape les ecarts mecaniquement detectables.

Appele automatiquement par lint-draft.py, pas besoin de le lancer a la main.
"""

import glob
import json
import os
import re

PROJECTS_DIR = os.path.expanduser("~/.claude/projects")


def _sans_code(texte):
    """Retire les blocs de code. Une liste numerotee DANS un message a envoyer
    appartient a ce message, elle n'est pas une sortie qui ratisse large."""
    return re.sub(r"```.*?```", "", texte, flags=re.S)

def dernier_message_bentho():
    """Le dernier message humain du transcript le plus recemment modifie."""
    fichiers = glob.glob(os.path.join(PROJECTS_DIR, "*", "*.jsonl"))
    if not fichiers:
        return ""
    chemin = max(fichiers, key=os.path.getmtime)
    lignes = []
    try:
        with open(chemin, "r", encoding="utf-8") as fh:
            for ligne in fh:
                ligne = ligne.strip()
                if not ligne:
                    continue
                try:
                    lignes.append(json.loads(ligne))
                except json.JSONDecodeError:
                    continue
    except OSError:
        return ""

    def texte(entree):
        msg = entree.get("message") or {}
        contenu = msg.get("content")
        if isinstance(contenu, str):
            return contenu
        if isinstance(contenu, list):
            return "\n".join(
                b.get("text", "")
                for b in contenu
                if isinstance(b, dict) and b.get("type") == "text"
            )
        return ""

    for entree in reversed(lignes):
        role = (entree.get("message") or {}).get("role") or entree.get("type")
        if role != "user":
            continue
        corps = texte(entree)
        # Les injections de hook ne sont pas la parole de Bentho.
        if not corps.strip() or "UserPromptSubmit hook" in corps:
            continue
        if corps.lstrip().startswith("<"):
            continue
        return corps
    return ""


# Un chiffre de duree ou de prix dans la sortie.
DUREE = re.compile(
    r"\b\d+([.,]\d+)?\s*(jours?|journées?|journees?|demi[- ]journées?|"
    r"demi[- ]journees?|heures?|h\b|semaines?|mois)\b"
    r"|\bhalf a day\b|\ba day\b|\b\d+\s*days?\b|\b\d+\s*hours?\b",
    flags=re.I,
)
PRIX = re.compile(r"\d[\d\s.,]*\s*(€|euros?|EUR|\$|USD)\b", flags=re.I)

# Bentho a-t-il ouvert le sujet du temps ou de l'argent dans SA demande ?
DEMANDE_TEMPS = re.compile(
    # Bentho ouvre le sujet du temps aussi bien en disant "combien de temps"
    # qu'en donnant une heure ("a 17h", "17:00") ou un repere de jour
    # ("today", "demain"). Sans ces deux dernieres formes, le verrou refusait
    # une reponse qui reprenait l'heure que Bentho venait lui-meme de donner
    # (constat du 2026-08-27, preparation de l'entretien Doctolib).
    r"\b(temps|dur[ée]e?|combien de temps|jours?|heures?|d[ée]lai|"
    r"[ée]ch[ée]ance|planning|quand|deadline|aujourd'hui|today|demain|"
    r"tomorrow|ce soir|ce matin|cet après-midi|cet apres-midi|days?|weeks?|months?|hours?|minutes?|duration)\b"
    r"|\b\d{1,2}\s*h(\d{2})?\b|\b\d{1,2}:\d{2}\b",
    flags=re.I,
)
DEMANDE_ARGENT = re.compile(
    r"\b(prix|co[uû]te?|co[uû]ts?|tarif|chiffr\w*|budget|facturer?|"
    r"estimation|devis|€|euros?|salaires?|salary|r[ée]mun[ée]ration|"
    r"honoraires?|tjm|paye|paie|compensation|package)\b",
    flags=re.I,
)

# La demande designe UN objet precis deja en discussion.
CIBLE_UNIQUE = re.compile(
    r"\b(cette page|ce message|cette t[âa]che|cette vue|ce point|"
    r"cette question|ce document|cette liste)\b",
    flags=re.I,
)

# Verbes qui, dans la demande, imposent une forme de sortie.
FORMES = {
    r"\b[ée]tape par [ée]tape\b|\bpas [àa] pas\b|\bstep by step\b": (
        "ETAPE PAR ETAPE DEMANDE. La sortie doit derouler des ACTIONS dans "
        "l'ordre ou on les fait, pas lister les parties, les sections ou les "
        "composants de l'objet. Une etape commence par un verbe d'action."
    ),
    r"\bbullet\s?points?\b|\ben puces\b": (
        "BULLET POINTS DEMANDES. La sortie doit utiliser des puces, pas des "
        "paragraphes ni un tableau."
    ),
}


def checks_demande(brouillon, demande=None):
    """Retourne la liste des ecarts entre la demande de Bentho et la sortie."""
    if demande is None:
        demande = dernier_message_bentho()
    if not demande.strip():
        return []

    fautes = []

    # 1. Duree ajoutee alors que Bentho n'a pas parle de temps.
    # 2026-09-03. La regle visait les ESTIMATIONS de travail glissees sans qu'on les
    # demande, pas toute mention de duree. Elle bloquait des reponses ou la duree EST
    # la donnee demandee, l'age d'un fichier par exemple. On n'attrape donc plus qu'une
    # duree presentee comme une estimation, et jamais une donnee dans un tableau.
    ESTIMATION = re.compile(
        r"(estim\w*|pr[ée]voir|compter|prendra|prendrait|il faut compter|environ|"
        r"d[ée]lai|charge|jour[- ]homme|budget temps|ca prend|temps de travail)",
        flags=re.I,
    )
    hors_tableau = "\n".join(
        l for l in brouillon.splitlines() if not l.lstrip().startswith("|")
    )
    if (
        DUREE.search(hors_tableau)
        and ESTIMATION.search(hors_tableau)
        and not DEMANDE_TEMPS.search(demande)
    ):
        trouve = DUREE.search(hors_tableau).group(0)
        fautes.append(
            "DUREE NON DEMANDEE : \"{}\". Bentho n'a pas parle de temps dans sa "
            "demande. Retirer, ou le proposer APRES en une question.".format(trouve)
        )

    # 0bis. Message livre en fragment au lieu du message entier.
    fautes += fragments_de_message(brouillon, demande)

    # 2. Prix ajoute alors que Bentho n'a pas parle d'argent.
    if PRIX.search(brouillon) and not DEMANDE_ARGENT.search(demande):
        trouve = PRIX.search(brouillon).group(0)
        fautes.append(
            "PRIX NON DEMANDE : \"{}\". Bentho n'a pas parle d'argent dans sa "
            "demande. Retirer, ou le proposer APRES en une question.".format(trouve)
        )

    # 3. Forme imposee par la demande.
    for motif, message in FORMES.items():
        if re.search(motif, demande, flags=re.I):
            fautes.append("A VERIFIER, " + message)

    # 4. Cible unique dans la demande, sortie qui ratisse large.
    if CIBLE_UNIQUE.search(demande):
        lignes_liste = len(
            re.findall(r"^\s*(?:[0-9]+\.|[-*•])\s+", _sans_code(brouillon), flags=re.M)
        )
        if lignes_liste >= 7:
            fautes.append(
                "CIBLE UNIQUE, SORTIE LARGE. Bentho designe un seul objet "
                "(\"{}\") et la sortie enumere {} elements. Verifier qu'aucun "
                "n'est hors de cet objet.".format(
                    CIBLE_UNIQUE.search(demande).group(0), lignes_liste
                )
            )

    return fautes


if __name__ == "__main__":
    import sys

    brouillon = sys.stdin.read()
    ecarts = checks_demande(brouillon)
    if ecarts:
        print("ECARTS DEMANDE/SORTIE ({}) :".format(len(ecarts)))
        for i, e in enumerate(ecarts, 1):
            print("{}. {}".format(i, e))
        sys.exit(1)
    print("OK")

# QUESTION FERMEE. Bentho a constate le 2026-08-27 que je repondais "Oui" puis
# que j'ajoutais trois lignes de justification que personne n'avait demandees.
# Une question fermee appelle Oui ou Non, point. Le developpement se propose en
# une question, il ne se deroule pas.
FERMEE = re.compile(
    r"^\s*(est[- ]ce que|as[- ]tu|est[- ]tu|es[- ]tu|tu as|tu peux|peux[- ]tu|"
    r"c'est|il y a[- ]t[- ]il|y a[- ]t[- ]il|as tu|avais[- ]tu|"
    r"tu l'as|tu les as|ca marche|c'etait|c'\u00e9tait)\b",
    flags=re.I,
)


def question_fermee(demande):
    """Vrai si le message de Bentho est UNE seule question, et qu'elle est fermee."""
    d = demande.strip()
    if d.count("?") != 1 or not d.endswith("?"):
        return False
    return bool(FERMEE.match(d))

# MESSAGE LIVRE EN FRAGMENT. Regle de Bentho, un email ou un message se relivre
# TOUJOURS ENTIER, jamais le seul paragraphe modifie. Constat du 2026-08-31, trois
# variantes d'un paragraphe livrees seules alors qu'il fallait trois messages
# complets. La correction chirurgicale vaut pour un DOCUMENT, jamais pour un message.
SUJET_MESSAGE = re.compile(
    r"\b(message|mail|email|e-mail|paragraphe|relance|dm|whatsapp|sms)\b", flags=re.I
)
SALUTATION = re.compile(
    # Espagnol inclus, Bentho ecrit a Lidia dans sa langue et `hola` n'y etait pas.
    r"^\s*(hi|hello|hey|dear|bonjour|salut|coucou|madame|monsieur|hola|buenas|"
    r"buenos días|estimad[oa])\b",
    flags=re.I | re.M,
)
SIGNATURE = re.compile(
    r"^\s*(best|best regards|regards|cheers|thanks|cordialement|bien \u00e0 vous|"
    r"bien a vous|\u00e0 bient\u00f4t|a bientot|benjamin|bentho)\s*,?\s*$",
    flags=re.I | re.M,
)


def fragments_de_message(brouillon, demande):
    """Un bloc de code qui EST un message doit porter une salutation ou une signature."""
    if not SUJET_MESSAGE.search(demande or ""):
        return []
    blocs = re.findall(r"```[a-zA-Z]*\n(.*?)```", brouillon, flags=re.S)
    if not blocs:
        return []
    nus = [b for b in blocs if not SALUTATION.search(b) and not SIGNATURE.search(b)]
    if nus and len(nus) == len(blocs):
        return [
            "MESSAGE LIVRE EN FRAGMENT. Bentho parle d'un message, or aucun des {} "
            "blocs livres ne porte de salutation ni de signature. Un email se relivre "
            "TOUJOURS ENTIER, jamais le seul paragraphe modifie. Recoller chaque "
            "variante dans le message complet.".format(len(blocs))
        ]
    return []
