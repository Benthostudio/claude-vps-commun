#!/usr/bin/env python3
"""
Verrou anti-incoherence sur les livrables client (hook Stop).

Detecte un livrable destine a un tiers dans la derniere reponse assistant
(email, message, courrier) et BLOQUE la fin de tour si une incoherence
mecanique est presente, ou si coherence-reviewer n'a pas ete lance.

Cree le 2026-08-15 apres l'envoi d'un email client au tutoiement
signe "Bien a vous", sans qu'aucun coherence-reviewer n'ait ete lance.
"""
import json
import os
import re
import sys

# ---------------------------------------------------------------- utilitaires


def read_stdin_json():
    try:
        return json.loads(sys.stdin.read() or "{}")
    except Exception:
        return {}


def last_assistant_text(transcript_path):
    """Retourne le texte de la derniere reponse assistant du transcript."""
    if not transcript_path or not os.path.exists(transcript_path):
        return "", []
    entries = []
    try:
        with open(transcript_path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except Exception:
                    continue
    except Exception:
        return "", []

    text = ""
    for entry in reversed(entries):
        msg = entry.get("message") or {}
        if msg.get("role") != "assistant":
            continue
        content = msg.get("content")
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            text = " ".join(
                b.get("text", "")
                for b in content
                if isinstance(b, dict) and b.get("type") == "text"
            )
        if text.strip():
            break
    return text, entries


def coherence_reviewer_ran(entries, lookback=40):
    """Vrai si l'agent coherence-reviewer a ete lance recemment."""
    for entry in entries[-lookback:]:
        msg = entry.get("message") or {}
        content = msg.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") != "tool_use":
                continue
            raw = json.dumps(block.get("input") or {}, ensure_ascii=False)
            if "coherence-reviewer" in raw:
                return True
    return False


# ------------------------------------------------------------- detection


CODE_BLOCK = re.compile(r"```[a-zA-Z]*\n(.*?)```", re.S)

# Un livrable client = salutation d'ouverture ET signature ou objet.
OPENERS = re.compile(
    r"^\s*(Bonjour|Salut|Bonsoir|Cher|Chere|Chère|Hello|Hi|Dear)\b", re.I | re.M
)
CLOSERS = re.compile(
    r"(Bien a vous|Bien à vous|Cordialement|Bien cordialement|A bientot|À bientôt|"
    r"Best regards|Kind regards|Sincerely|Amicalement|Bonne journee|Bonne journée|"
    r"Bien sincerement|Bien sincèrement)",
    re.I,
)
SUBJECT = re.compile(r"^\s*Objet\s*:", re.I | re.M)


def extract_deliverables(text):
    """Retourne les blocs de code qui ressemblent a un livrable client."""
    out = []
    for block in CODE_BLOCK.findall(text or ""):
        if OPENERS.search(block) and (CLOSERS.search(block) or SUBJECT.search(block)):
            out.append(block)
    return out


# --------------------------------------------------------------- controles

TU_MARKERS = re.compile(
    r"\b(tu|toi|ton|ta|tes|tien|tienne|t'ai|t'as|t'es|t'indiquer|t'envoie)\b"
    r"|peux-tu\b|as-tu\b|disposes-tu\b|utilise-t-elle ton\b",
    re.I,
)
VOUS_MARKERS = re.compile(
    r"\b(vous|votre|vos|v[oô]tre)\b|pouvez-vous\b|avez-vous\b|disposez-vous\b",
    re.I,
)
EM_DASH = re.compile(r"[–—]")
COLON = re.compile(r"(?<!\bhttp)(?<!\bhttps)(?<![0-9]):(?![0-9/])")

# Un livrable client parle TOUJOURS au nom de l'agence ("nous"), jamais "je".
# Ajoute le 2026-08-17 apres un email entierement redige a la premiere personne
# du singulier. Couvre aussi les tournures implicites ("de mon cote", "qu'on").
JE_MARKERS = re.compile(
    r"\b(je|j'ai|j'aurai|j'utilise|j'attends|j'espere|j'espère|moi|ma|mon|mes)\b"
    r"|\bde mon c[oô]t[eé]\b|\bni de moi\b|\bdis-moi\b|\bm'en\b",
    re.I,
)
NOUS_MARKERS = re.compile(
    r"\b(nous|notre|nos)\b|\bde notre c[oô]t[eé]\b",
    re.I,
)
# Formules de RELATION ou le "je" reste autorise (option B, 2026-08-17).
# Elles sont neutralisees avant le controle du "je".
RELATION_JE = re.compile(
    r"\bje (te|vous) propose\b|\bje (te|vous) souhaite\b|\bje reste\b"
    r"|\bje suis (a ta|à ta|a votre|à votre) disposition\b|\bje suis dispo\w*\b"
    r"|\bdis-moi\b|\bdites-moi\b|\bm'en proposer\b|\bme proposer\b"
    r"|\bn'hesite pas a m\w*\b|\bn'hésite pas à m\w*\b|\bje t'appelle\b",
    re.I,
)

# La cedille de "ca" est un marqueur d'oral proscrit en texte public.
CA_ORAL = re.compile(r"\b[çÇ]a\b|\bpour [çÇ]a\b")


def check(block):
    """Retourne la liste des incoherences trouvees dans un livrable."""
    problems = []

    # Regle du 2026-08-17, option B validee par Bentho :
    # "nous" pour la prestation et le chiffrage, "je" tolere UNIQUEMENT
    # sur la relation (proposer un appel, rester dispo, signer).
    neutral = RELATION_JE.sub(" ", block)
    je_hits = JE_MARKERS.findall(neutral)
    if je_hits:
        problems.append(
            "PREMIERE PERSONNE DU SINGULIER sur la PRESTATION dans un livrable "
            "client ({} occurrence(s)). StudioMakers est une marque, pas une "
            "personne. Tout ce qui touche au travail et au prix passe au 'nous'. "
            "Le 'je' n'est tolere que sur la relation (proposer un appel, rester "
            "disponible, signer). Attention aux tournures implicites "
            "('de mon cote', 'ni de toi ni de moi'). "
            "Voir la memoire feedback-client-we-not-i.".format(len(je_hits))
        )

    if CA_ORAL.search(block):
        problems.append(
            "CEDILLE ORALE ('ca' / 'pour ca') dans un texte public. "
            "Ecrire 'cela' ou 'pour cette raison'."
        )

    tu_hits = TU_MARKERS.findall(block)
    vous_hits = VOUS_MARKERS.findall(block)
    if tu_hits and vous_hits:
        problems.append(
            "MELANGE TUTOIEMENT / VOUVOIEMENT. "
            "Marqueurs tutoiement detectes ({} occurrences) ET vouvoiement ({}). "
            "Verifier notamment la formule de cloture.".format(
                len(tu_hits), len(vous_hits)
            )
        )

    if EM_DASH.search(block):
        problems.append("TIRET LONG (em dash) present. Regle 5 du hook output-rules.")

    body = SUBJECT.sub("", block)
    body = re.sub(r"^\s*\d+\.", "", body, flags=re.M)
    # Un deux-points qui INTRODUIT une liste est autorise (Bentho, 2026-08-17).
    # On le neutralise avant le controle : ":" en fin de ligne suivi d'une puce
    # ou d'un element numerote.
    body = re.sub(r":\s*\n(\s*(?:[-*•]|\d+[.)])\s)", r"\n\1", body)
    if COLON.search(body):
        problems.append(
            "DEUX-POINTS present dans un texte public. "
            "Regle 5 du hook output-rules (marqueur IA). Casser la phrase en deux."
        )

    return problems


# ------------------------------------------------------------------ main


def main():
    data = read_stdin_json()

    # Anti-boucle : ne jamais bloquer deux fois de suite.
    if data.get("stop_hook_active"):
        sys.exit(0)

    text, entries = last_assistant_text(data.get("transcript_path"))
    blocks = extract_deliverables(text)
    if not blocks:
        sys.exit(0)

    problems = []
    for i, block in enumerate(blocks, 1):
        for p in check(block):
            problems.append("Livrable {} : {}".format(i, p))

    reviewed = coherence_reviewer_ran(entries)
    if not reviewed:
        problems.append(
            "coherence-reviewer N'A PAS ETE LANCE sur ce livrable. "
            "Le protocole StudioMakers l'impose avant tout envoi client."
        )

    if not problems:
        sys.exit(0)

    # Bentho, 2026-08-19 : ne PLUS JAMAIS bloquer. Un "decision: block" en fin de
    # tour force une re-reponse, si bien que la version rejetee ET la version
    # corrigee s'affichaient toutes deux : c'est la source des reponses en double,
    # que Bentho interdit absolument, partout. On garde la DETECTION mais on ne fait
    # plus qu'un avertissement NON BLOQUANT (systemMessage, sans "decision"). C'est
    # desormais a moi d'avoir deja lance le coherence-reviewer et corrige les points
    # AVANT de livrer, en reflexe, pas via un blocage mecanique.
    notice = "Avertissement livrable client (non bloquant), {} point(s) a verifier : {}".format(
        len(problems), " | ".join(problems)
    )
    print(json.dumps({"systemMessage": notice}, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
