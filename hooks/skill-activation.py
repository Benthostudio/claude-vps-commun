#!/usr/bin/env python3
"""Declencheur AUTOMATIQUE des skills et des agents, par SUJET.

Pourquoi ce fichier remplace `skill-activation.sh`. L ancien hook injectait une
METHODE, « evalue les besoins du projet et sors la liste des skills pertinents ».
Une methode se lit, s approuve, puis ne se fait pas. Bentho l a constate le 08.09,
verbatim, « il faut que je te le rappelle tous les jours ».

Celui-ci ne demande plus d evaluer. Il LIT le message, reconnait le sujet, et sort
l ordre nomme, « sujet DESIGN detecte, tu DOIS lancer `designer` puis
`ux-cro-auditor` AVANT de livrer ». Un nom d outil, pas une intention.

Regle de Bentho, verbatim du 08.09 : « On ne fait pas de design sans les skills et
agents design. On ne fait pas d ecriture sans skills et agents de copywriting. [...]
Automatiquement toujours, pour toujours, partout, c est absolu. »
"""

import json
import re
import sys

# Un sujet, ses mots declencheurs, les outils qu il rend OBLIGATOIRES.
# L ordre compte, le premier de la liste se lance en premier.
SUJETS = [
    (
        "DESIGN",
        r"design|maquette|visuel|couleur|palette|typo|espacement|alignement|"
        r"marge|padding|layout|ecran|écran|mockup|interface|\bui\b|\bux\b|"
        r"responsive|mobile|desktop|gabarit|template|composant",
        ["skill page-cro", "agent designer", "agent ux-cro-auditor"],
    ),
    (
        "CONVERSION",
        r"conversion|convertir|landing|\bcta\b|bouton|tunnel|funnel|"
        r"inscription|formulaire|lead|panier|checkout|taux|abandon",
        ["skill page-cro", "agent ux-cro-auditor"],
    ),
    (
        "ECRITURE",
        r"ecri|écri|rediger|rédiger|redaction|rédaction|texte|copy|"
        r"accroche|titre|slogan|message|email|mail|post|article|"
        r"paragraphe|formulation|reformul|traduc|wording|ton\b",
        ["skill copywriting-core", "skill copywriting"],
    ),
    (
        "SEO ET GEO",
        r"\bseo\b|\bgeo\b|referenc|référenc|google|balise|meta|sitemap|"
        r"schema|json-ld|indexation|mot-cle|mot-clé|serp|ranking|crawl",
        ["skill seo-geo", "agent seo"],
    ),
    (
        "CHIFFRAGE",
        r"chiffr|devis|estimation|combien ca|combien ça|budget|tarif|"
        r"prix de|cout de|coût de|facturer|facturation",
        ["skill chiffrage-brief"],
    ),
    (
        "PROPOSITION COMMERCIALE",
        r"propale|proposition commerciale|offre commerciale|contrat",
        ["skill proposition-commerciale"],
    ),
    (
        "ENVOI AU CLIENT",
        r"envoyer au client|envoie au client|partager|livrer|livraison|"
        r"pour le client|a julian|à julian|a lidia|à lidia|publier",
        ["agent coherence-reviewer"],
    ),
    (
        "AFFIRMATION DE FAIT",
        r"est-ce qu on a|est-ce qu'on a|est ce qu on a|on a bien|"
        r"tu es sur|tu es sûr|verifie|vérifie|confirme|c est vrai|"
        r"est-ce que c est|qu est-ce qui reste|ou en est|où en est",
        ["agent verificateur"],
    ),
    (
        "PILOTAGE",
        r"tache|tâche|liste|planning|retroplanning|rétroplanning|jalon|"
        r"prochaine etape|prochaine étape|on en fait quoi|priorit|"
        r"echeance|échéance|deadline|avance",
        ["skill gestion-projet"],
    ),
    (
        "CODE",
        r"bug|erreur|casse|refactor|composant react|typescript|"
        r"build|deploie|déploie|commit|merge|pull request",
        ["agent reviewer"],
    ),
]


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    prompt = str(payload.get("prompt", ""))
    bas = prompt.lower()

    touches = [
        (nom, outils)
        for nom, motif, outils in SUJETS
        if re.search(motif, bas, re.IGNORECASE)
    ]

    if not touches:
        # Aucun sujet reconnu, le hook se tait. Un rappel generique a chaque tour
        # est exactement ce qui a cesse d etre lu.
        sys.exit(0)

    lignes = [
        "DECLENCHEMENT AUTOMATIQUE DES OUTILS (regle absolue de Bentho, 08.09.2026).",
        "Les sujets ci-dessous sont detectes dans le message. Les outils nommes sont",
        "OBLIGATOIRES, ils se lancent AVANT de produire, pas apres. Un outil saute se",
        "dit explicitement a Bentho, il ne se remplace jamais par mon propre jugement.",
        "",
    ]
    for i, (nom, outils) in enumerate(touches, 1):
        lignes.append(f"{i}. SUJET {nom} -> {', '.join(outils)}")
    lignes.append("")
    lignes.append(
        "Un agent se lance avec l outil Agent, un skill avec l outil Skill. "
        "Si le sujet detecte ne correspond pas a la demande reelle, le dire en "
        "une ligne et passer, ne pas lancer un outil pour rien."
    )

    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": "\n".join(lignes),
                }
            }
        )
    )


if __name__ == "__main__":
    main()
