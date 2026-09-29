#!/usr/bin/env python3
"""
LINT DE BROUILLON (avant emission).

Usage : python3 ~/.claude/hooks/lint-draft.py <<'EOF'
<le brouillon de la reponse>
EOF

Role : verifier un texte AVANT que Bentho ne le lise. Le Stop hook
output-verifier.py agit trop tard, il bloque une reponse deja affichee, donc la
correction arrive apres coup et ne sert a rien. Ce script se lance en amont,
sur le brouillon, ce qui permet de corriger avant emission.

Sortie : "OK" si le texte est propre, sinon la liste des violations.
"""

import os
import re
import sys


FLOU = re.compile(
    r"\b("
    r"deux|trois|quatre|plusieurs|certaines?|quelques|des"
    r")\s+"
    r"(choses?|trucs?|éléments?|elements?|points?|aspects?)\b"
    r"|\bce\s+truc\b|\bces\s+trucs\b|\bles\s+moyens\s+du\s+bord\b"
    r"|\bavec\s+les\s+moyens\b",
    flags=re.I,
)
# Une couleur ne pose probleme que pour designer un element manipulable qui porte un texte.
# Un aliment, une matiere ou un objet du monde reel ne sont pas concernes.
COULEUR = re.compile(
    r"^\s*\d+\.\s"
    r"(?=.*\b(bouton|onglet|champ|case|lien|menu|pastille|icone|icône|encart|bandeau|"
    r"cadre|barre|pave|pavé|bloc|vignette|carte)\b"
    r"|.*\b(clique|cliquer|appuie|appuyer|touche|tape|sélectionne|selectionne|"
    r"ouvre|ouvrir|coche|décoche|decoche|glisse|fais\s+défiler|fais\s+defiler)\b)"
    r".*\b(gris[e]?s?|beige|sable|vert[e]?s?|rouge|bleu[e]?s?|jaune|orange|"
    r"noir[e]?s?|blanc[he]*s?|sombre|clair[e]?s?|pale|pâle)\b",
    flags=re.I | re.M,
)
ANCRE = re.compile(r"\*\*[^*]+\*\*|`[^`]+`")


def couleurs_sans_ancre(texte):
    """Une etape qui designe un element par sa couleur doit porter aussi son texte exact."""
    mauvaises = []
    for ligne in texte.splitlines():
        if COULEUR.match(ligne) and not ANCRE.search(ligne):
            mauvaises.append(ligne.strip()[:90])
    return mauvaises


ACTION = re.compile(r"(va sur https?://|colle ceci|colle ce |colle le |clique sur )", flags=re.I)
ETAPE = re.compile(r"^\s*\d+\.\s", flags=re.M)



TRANSCRIPTS = os.path.expanduser("~/.claude/projects")


def dernier_transcript():
    """Le .jsonl de session le plus recemment ecrit, tous projets confondus."""
    candidats = []
    for racine, _dirs, fichiers in os.walk(TRANSCRIPTS):
        for f in fichiers:
            if f.endswith(".jsonl"):
                chemin = os.path.join(racine, f)
                try:
                    candidats.append((os.path.getmtime(chemin), chemin))
                except OSError:
                    pass
    if not candidats:
        return None
    return max(candidats)[1]


def checks_partages(brouillon):
    """Rejoue sur le brouillon les regles du verrou qui exigent le contexte du tour.

    Concerne le bloc RÉPONSES quand Bentho a pose une question, la demande de
    permission apres un go, l'annonce d'un livrable pret sans coherence-reviewer,
    et le message livre en deux versions. Un echec ici est silencieux, le lint ne
    doit jamais bloquer le travail parce qu'il n'a pas trouve le transcript.
    """
    RETENUS = {
        "bloc-reponses",
        "permission-apres-go",
        "coherence-reviewer",
        "deux-versions-message",
    }
    try:
        import importlib.util

        chemin_verrou = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output-verifier.py")
        spec = importlib.util.spec_from_file_location("output_verifier", chemin_verrou)
        verrou = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(verrou)

        transcript = dernier_transcript()
        if not transcript:
            return []
        _assistant, user_raw, recent = verrou.read_transcript(transcript)
        faults, codes = verrou.run_checks(brouillon, user_raw, recent)
        return [f for f, c in zip(faults, codes) if c in RETENUS]
    except Exception:
        return []


def nb_tableaux(raw):
    """Nombre de tableaux markdown distincts dans le brouillon."""
    n, dedans = 0, False
    for ligne in raw.split("\n"):
        pipe = ligne.strip().startswith("|")
        if pipe and not dedans:
            n += 1
        dedans = pipe
    return n


# Bentho pointe UN objet precis et en demande la reprise. Le piege n'est pas la forme,
# c'est la cible: on repond a l'attribut qu'il nomme au lieu d'operer sur l'objet qu'il
# montre, et on livre un objet de son cru. Pose le 2026-09-01 apres exactement ca.
CIBLE_UNIQUE = re.compile(
    r"(un seul tableau|surtout fais[- ]moi un tableau|le m[eê]me tableau|ce tableau|"
    r"exactement la m[eê]me chose|refais[- ]moi ce\b|le m[eê]me et un seul|un tableau, hein)",
    re.I,
)


def cible_unique(brouillon, message_bentho):
    """Bentho a designe UN tableau, le brouillon doit en contenir un seul."""
    if not message_bentho or not CIBLE_UNIQUE.search(message_bentho):
        return []
    n = nb_tableaux(brouillon)
    if n <= 1:
        return []
    return [
        "CIBLE REMPLACEE. Bentho a designe UN tableau precis et le brouillon en contient "
        "{}. Reprendre SON tableau, celui qu'il montre, en y ajoutant seulement ce qu'il "
        "demande. Ne jamais livrer un tableau de son cru a la place du sien.".format(n)
    ]


# Bentho lit de haut en bas et envoie le message des qu'il le voit. Tout ce qui pourrait
# changer ce message doit donc etre AVANT lui. Une erreur, un risque ou un arbitrage place
# apres le bloc a coller est lu quand le message est deja parti, donc il envoie un texte
# faux en croyant qu'il est bon. Pose le 2026-09-02, apres exactement ca.
APRES_MESSAGE = re.compile(
    r"(erreur|faux|fausse|inexact|risque|a trancher|à trancher|attention|rattrap|"
    r"correction|corrige|je me suis trompe|je me suis trompé|verifie avant|vérifie avant)",
    re.I,
)


def rien_apres_le_message(raw):
    """Rien qui puisse changer le message ne doit apparaitre apres le bloc a coller."""
    blocs = [m.end() for m in re.finditer(r"```", raw)]
    if len(blocs) < 2:
        return []
    fin_dernier = blocs[-1]
    queue = raw[fin_dernier:]
    m = APRES_MESSAGE.search(queue)
    if not m:
        return []
    return [
        "ERREUR PLACEE APRES LE MESSAGE : \"{}\". Bentho lit de haut en bas et envoie le "
        "message des qu'il le voit, donc il partira AVANT d'avoir lu ca. Tout ce qui peut "
        "changer le message (erreur, risque, arbitrage) se met AVANT le bloc a coller, "
        "jamais apres. Apres le message, uniquement ce qui ne change rien.".format(m.group(0))
    ]


def strip_code(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    return text


def main():
    raw = sys.stdin.read()
    if not raw.strip():
        print("OK (brouillon vide)")
        return
    prose = strip_code(raw)
    faults = []

    for m in re.finditer(r"[^.\n]{0,40},\s+(et|and)\b[^.\n]{0,20}", prose, flags=re.I):
        faults.append("VIRGULE AVANT ET : ..." + m.group(0).strip())

    for m in re.finditer(r"[^\n]{0,30}[—–][^\n]{0,30}", prose):
        faults.append("TIRET LONG : ..." + m.group(0).strip())

    for m in re.finditer(r"^#{2,}\s.*", raw, flags=re.M):
        faults.append("TITRE ## ou ### : " + m.group(0).strip())

    for m in re.finditer(r"^#\s+(?!\*\*)", raw, flags=re.M):
        faults.append("TITRE sans le format '# **• TITRE**'")

    if ACTION.search(prose) and not ETAPE.search(raw):
        faults.append(
            "ACTION A FAIRE SANS PROCEDURE NUMEROTEE. Toute action que Bentho doit executer "
            "se decrit en etapes 1., 2., 3., un clic par etape, le bouton nomme comme a l'ecran."
        )

    for l in couleurs_sans_ancre(raw):
        faults.append(
            "ELEMENT DESIGNE PAR SA COULEUR SANS SON TEXTE : \"" + l + "\". Un element se "
            "designe par le texte qu'il porte, en gras ou entre accents graves. La couleur "
            "seule envoie Bentho chercher quelque chose qu'il ne trouvera pas."
        )


    # LIEN OBLIGATOIRE. Regle de Bentho, MODIFICATION EGAL LIEN, precisee le 2026-09-09.
    # Le declencheur est le CHANGEMENT, jamais la simple mention d'un livrable. Parler du
    # deck sans y avoir touche n'appelle aucun lien. Une virgule changee en appelle un.
    CHANGEMENT = re.compile(
        r"\b(d[ée]ploy[ée]e?s?|publi[ée]e?s?|mis(?:e|es)? en ligne|remis en ligne|"
        r"corrig[ée]e?s?|r[ée]par[ée]e?s?|refait|refaite|refaits|refaites|"
        r"modifi[ée]e?s?|mis(?:e|es)? [àa] jour|ajout[ée]e?s?|remplac[ée]e?s?|"
        r"supprim[ée]e?s?|retir[ée]e?s?|r[ée][ée]crit(?:e|s|es)?)\b",
        flags=re.I,
    )
    if CHANGEMENT.search(prose) and not re.search(r"\]\(https://", raw):
        faults.append(
            "CHANGEMENT ANNONCE SANS SON LIEN. Modification egal lien, sans exception, "
            "meme pour une virgule, meme si Bentho a recu le lien au message precedent. "
            "La ligne de liens markdown https ouvre la reponse. Une simple MENTION d'un "
            "livrable non modifie n'appelle aucun lien."
        )

    # NUMEROTATION STABLE. Regle de Bentho, un sujet garde son numero jusqu'a cloture,
    # jamais de compteur parallele. Ouvrir une serie D1/P2/Q3 quand le projet tient deja
    # son propre compteur est la reattribution qu'il interdit.
    if re.search(r"^#\s*\*\*.\s*[A-Z]\d+\.", prose, flags=re.M) or re.search(
        r"\*\*[A-Z]\d+\.\s", prose
    ):
        faults.append(
            "COMPTEUR PARALLELE. Une serie du type D1, P2, Q3 ouvre une numerotation neuve "
            "alors que le projet en tient deja une. Reprendre le compteur existant, "
            "DECISIONS.md ou l'equivalent, et continuer a partir du dernier numero utilise."
        )

    # Porte depuis output-verifier, meme regle des deux cotes.
    # MESSAGE LIVRE EN MORCEAUX.
    blocs = re.findall(r"```[a-zA-Z]*\n(.*?)```", raw, flags=re.S)
    a_un_message = any(
        re.search(r"^\s*(Hi|Hello|Dear|Bonjour|Salut|Hola|Buenos)\s+[A-ZÁÉÍÓÚÑ]", b, flags=re.M)
        for b in blocs
    )
    if a_un_message and re.search(
        r"(messages?\s+\d[^.\n]{0,30}(sont |est )?inchang|inchang[eé]s?\b|"
        r"reste(nt)? (le|la|les) m[eê]me|unchanged\b|ne (change|bouge)(nt)? pas)",
        prose,
        flags=re.I,
    ):
        faults.append(
            "MESSAGE LIVRE EN MORCEAUX. Un message a envoyer se redonne ENTIER, "
            "tous les messages du lot, meme ceux qui n'ont pas bouge."
        )

    # SUJET TRAITE DEUX FOIS (Bentho, 2026-09-03).
    bloc = re.search(r"#\s*\*\*•\s*RÉPONSES\*\*(.*?)(?=\n#\s|\Z)", raw, flags=re.S)
    if bloc:
        RENVOI = re.compile(
            r"(d[ée]tail plus bas|plus bas|ci-dessous|voir plus bas|j'y reviens|"
            r"je d[ée]taille (plus bas|apr[èe]s|en dessous)|dans la section)",
            flags=re.I,
        )
        r = [m.group(0) for m in RENVOI.finditer(bloc.group(1))]
        if r:
            faults.append(
                "SUJET TRAITE DEUX FOIS : le bloc RÉPONSES renvoie plus bas (\""
                + "\", \"".join(sorted(set(r))[:3])
                + "\"). Un sujet se regle DANS le bloc, ou il devient sa propre section "
                "et disparait du bloc. Jamais les deux."
            )

    # LE BLOC RÉPONSES EST LA REPONSE, PAS UN SOMMAIRE (Bentho, 2026-09-09).
    # Un label du bloc ne peut pas reapparaitre en titre plus bas : Bentho ecrit ses
    # retours sur le bloc, puis decouvre la version longue du meme sujet, ses retours
    # ne portent plus sur rien. Ses mots : "c'est litteralement de la perte de temps".
    if bloc:
        import unicodedata

        def _norm(t):
            t = unicodedata.normalize("NFD", t.lower())
            t = "".join(c for c in t if unicodedata.category(c) != "Mn")
            return set(w for w in re.findall(r"[a-z0-9]+", t) if len(w) > 4)

        labels = [_norm(m.group(1)) for m in re.finditer(r"^\s*\d+\.\s*\*\*(.+?)\*\*", bloc.group(1), flags=re.M)]
        apres = raw[bloc.end():]
        for m in re.finditer(r"^#\s*\*\*•\s*(.+?)\*\*", apres, flags=re.M):
            mots = _norm(m.group(1))
            for lab in labels:
                if len(mots & lab) >= 2:
                    faults.append(
                        "LE BLOC RÉPONSES REDEVIENT UN SOMMAIRE : le titre \"" + m.group(1).strip()
                        + "\" reprend un sujet deja traite dans le bloc. Le bloc EST la reponse, "
                        "la reponse complete va DEDANS, courte ou longue. Rien ne se redeveloppe apres."
                    )
                    break

    # COMPTE RENDU QUI DEBORDE. Un rendu de travail liste les points demandes, une ligne
    # chacune. Le detail non demande se propose en une question, il ne se deroule pas.
    if re.search(r"#\s*\*\*🟢", prose):
        bloc_vert = re.split(r"#\s*\*\*🟢", prose, maxsplit=1)[1]
        bloc_vert = re.split(r"\n#\s", bloc_vert, maxsplit=1)[0]
        lignes_pleines = [l for l in bloc_vert.splitlines() if l.strip()]
        if len(lignes_pleines) > 8:
            faults.append(
                "COMPTE RENDU TROP LONG : " + str(len(lignes_pleines)) + " lignes dans le "
                "bloc LIVRE. Un rendu liste les points demandes, une ligne chacune. Tout "
                "detail non demande, test, mesure, tableau, se propose en une question."
            )

    # ACTION SANS SON POURQUOI. Bentho a exige le 2026-08-24 que toute action qu'on lui
    # demande arrive avec son contexte : ce qu'on est en train de faire, ce que ca lui
    # apporte, ce qui se casse s'il ne le fait pas. Il a precise le meme jour que ce
    # contexte se dit EN LIGNE, dans le fil de la reponse, jamais dans un bloc separe.
    if re.search(r"#\s*\*\*🟣", raw):
        if not re.search(r"(sinon\b|si tu ne |si tu n'|tant que tu n)", prose, flags=re.I):
            faults.append(
                "ACTION SANS SON POURQUOI. Une action demandee a Bentho se rappelle en "
                "ligne ce qu'on est en train de faire, ce que ca lui apporte et ce qui se "
                "passe s'il ne le fait pas. Pas de bloc separe, une phrase dans le fil."
            )

    # ------------------------------------------------------------------
    # Regles qui ont besoin du DERNIER MESSAGE DE BENTHO et du transcript.
    # Elles etaient jusqu'ici verifiees UNIQUEMENT par le Stop hook, donc
    # apres coup, ce qui obligeait a envoyer un correctif alors que Bentho
    # avait deja lu la reponse. Il l'a explicitement interdit le 2026-08-24
    # ("ARRETE DE ME METTRE LES CORRECTIFS A LA FIN"). On appelle donc ici
    # la MEME fonction que le verrou, sur le brouillon, avant emission.
    # ------------------------------------------------------------------
    faults += rien_apres_le_message(raw)
    faults += checks_partages(raw)

    try:
        import importlib.util as _il

        _sp = _il.spec_from_file_location(
            "ov", os.path.join(os.path.dirname(os.path.abspath(__file__)), "output-verifier.py")
        )
        _ov = _il.module_from_spec(_sp)
        _sp.loader.exec_module(_ov)
        _t = dernier_transcript()
        if _t:
            _a, _user, _r = _ov.read_transcript(_t)
            faults += cible_unique(raw, _user or "")
    except Exception:
        pass

    # ------------------------------------------------------------------
    # CORRESPONDANCE DEMANDE CONTRE SORTIE (Bentho, 2026-08-25).
    # Tous les controles ci-dessus regardent la FORME du texte. Aucun ne
    # verifiait si le texte repond a ce qui a ete demande. Ce module lit le
    # dernier message de Bentho et compare.
    # ------------------------------------------------------------------
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from demande_vs_sortie import checks_demande

        faults += checks_demande(raw)
    except Exception:
        pass

    # Les items "A VERIFIER" sont des rappels, pas des fautes. Ils s'affichent
    # mais ne bloquent pas : un verrou qui crie au loup finit ignore.
    durs = [f for f in faults if not f.startswith("A VERIFIER")]
    doux = [f for f in faults if f.startswith("A VERIFIER")]

    if doux:
        print("A VERIFIER ({}) :".format(len(doux)))
        for i, f in enumerate(doux, 1):
            print("{}. {}".format(i, f))
        if durs:
            print()

    if durs:
        print("VIOLATIONS ({}) :".format(len(durs)))
        for i, f in enumerate(durs, 1):
            print("{}. {}".format(i, f))
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
