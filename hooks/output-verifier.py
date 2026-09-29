#!/usr/bin/env python3
"""
VERROU DE SORTIE (Stop hook).

Role : les regles de Bentho ne sont plus seulement INJECTEES dans le prompt,
elles sont VERIFIEES sur la reponse produite. Toute violation mecanique
BLOQUE la fin du tour et force la correction avant que Bentho ne voie la reponse.

Principe : on ne bloque que sur des faits VERIFIABLES a 100%, zero faux positif.
Le flou reste du ressort du modele, le mecanique est verrouille ici.
"""

import json
import os
import difflib
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


STATE_DIR = os.path.expanduser("~/.claude/state")
STRIKES_FILE = os.path.join(STATE_DIR, "output-violations.log")


def read_transcript(path):
    """Retourne (dernier message assistant, dernier message user, texte complet recent)."""
    if not path or not os.path.exists(path):
        return "", "", ""
    rows = []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except OSError:
        return "", "", ""

    def text_of(entry):
        msg = entry.get("message") or {}
        content = msg.get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            out = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    out.append(block.get("text", ""))
            return "\n".join(out)
        return ""

    last_assistant = ""
    last_user = ""
    recent = []
    for entry in reversed(rows):
        role = (entry.get("message") or {}).get("role") or entry.get("type")
        body = text_of(entry)
        if len(recent) < 40:
            recent.append(body)
        if role == "assistant" and not last_assistant and body.strip():
            last_assistant = body
        if role == "user" and not last_user and body.strip():
            # Ignorer tout ce qui n'est PAS une parole de Bentho. Une notification de
            # tache de fond ou une injection de hook arrive dans le role "user" mais
            # personne n'a parle, donc la compter ferait exiger un bloc REPONSES pour
            # des questions inexistantes, et declencherait les regles prix et duree.
            if "<task-notification>" in body or "[SYSTEM NOTIFICATION" in body:
                continue
            if "<system-reminder>" in body and len(body) > 4000:
                continue
            last_user = body
        if last_assistant and last_user:
            if len(recent) >= 40:
                break
    return last_assistant, last_user, "\n".join(recent)


def lint_a_tourne(recent):
    """Vrai si lint-draft.py a ete lance dans les evenements recents du tour.

    2026-09-03. Ce verrou tourne sur Stop, donc APRES que Bentho a lu la reponse:
    bloquer la lui fait relire un correctif d'un texte deja lu, ce qui est
    exactement ce qu'il interdit. Les deux autres verrous Stop ont ete rétrogradés
    en avertissement le 19.08 pour cette raison. Celui-ci garde son blocage
    UNIQUEMENT quand le lint d'avant emission a ete saute: dans ce cas le blocage
    est le seul filet. Lint passe, on se contente d'un avertissement.
    """
    return "lint-draft.py" in (recent or "") or _lint_dans_transcript()


def _lint_dans_transcript(lookback=120):
    """Cherche l'appel du lint dans les evenements bruts du transcript.

    read_transcript ne rend que le TEXTE des messages, or lancer le lint est un
    appel d'outil, jamais du texte : la detection echouait donc toujours et le
    verrou bloquait des reponses pourtant lintees. Constat du 2026-09-03.
    """
    import glob
    fichiers = glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl"))
    if not fichiers:
        return False
    try:
        with open(max(fichiers, key=os.path.getmtime), encoding="utf-8", errors="replace") as fh:
            lignes = fh.readlines()[-lookback:]
    except OSError:
        return False
    return any("lint-draft.py" in l for l in lignes)


def strip_code(text):
    """Retire blocs de code, code inline et citations, pour ne juger que MA prose."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    return text


def log_violation(codes):
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        with open(STRIKES_FILE, "a", encoding="utf-8") as fh:
            fh.write(",".join(codes) + "\n")
    except OSError:
        pass


def run_checks(assistant_raw, user_raw, recent):
    """Rend (faults, codes).

    Partagee entre le VERROU DE SORTIE (Stop hook, apres coup) et le LINT DE BROUILLON
    (avant emission). Une seule source de verite, donc le lint voit exactement ce que
    le verrou verra, et Bentho ne recoit plus de correctif apres avoir deja lu la reponse.
    """
    prose = strip_code(assistant_raw)
    faults = []
    codes = []

    # 1. VIRGULE AVANT ET / AND. PERIMETRE STRICT, Bentho le 09.09 puis le 11.09 :
    # la regle vaut pour MES messages a Bentho et pour les messages WhatsApp que je
    # redige pour lui, jamais pour un texte client ou tiers. Une citation entre
    # guillemets francais est le texte de quelqu un d autre, elle ne se controle pas.
    mine = re.sub(r"«[^»]*»", " ", prose)
    if re.search(r",\s+(et|and)\b", mine, flags=re.I):
        hits = re.findall(r"[^.\n]{0,45},\s+(?:et|and)\b[^.\n]{0,25}", mine, flags=re.I)
        faults.append(
            "VIRGULE AVANT UN ET, dans un message a Bentho. La regle ne vaut que pour "
            "cette conversation et ses messages WhatsApp, jamais pour un texte client. "
            "Occurrences : " + " || ".join(h.strip() for h in hits[:4])
        )
        codes.append("virgule-et")

    # 1bis. MESSAGE LIVRE EN MORCEAUX. Un message destine a etre envoye (WhatsApp,
    # email, DM) se relivre TOUJOURS entier, meme quand une seule phrase change: Bentho
    # copie-colle le bloc pour l'envoyer, il ne recompose pas a la main. La correction
    # chirurgicale ne vaut que pour les documents et le code. Regle rappelee le 24.08
    # apres une reponse qui ne redonnait qu'un message sur trois.
    blocs = re.findall(r"```[a-zA-Z]*\n(.*?)```", assistant_raw, flags=re.S)
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
            "MESSAGE LIVRE EN MORCEAUX. Un message a envoyer se redonne TOUJOURS "
            "ENTIER, tous les messages du lot, meme ceux qui n'ont pas bouge. Bentho "
            "copie le bloc tel quel, il ne recompose rien. Interdit de dire qu'un "
            "message est inchange: redonne-le."
        )
        codes.append("message-en-morceaux")

    # 1quater. DEUX VERSIONS D UN MESSAGE D AFFILEE. Bentho, 24.08 : "je ne veux jamais
    # voir deux versions d un meme message qui se suivent, je veux toujours la version
    # corrigee seulement". Toutes les verifications passent AVANT le premier affichage.
    if len(blocs) >= 2:
        stop = False
        for i in range(len(blocs)):
            if stop:
                break
            for j in range(i + 1, len(blocs)):
                a, b = blocs[i].strip(), blocs[j].strip()
                if len(a) < 120 or len(b) < 120:
                    continue
                ratio = difflib.SequenceMatcher(None, a, b).ratio()
                if ratio < 0.80:
                    continue
                entre = assistant_raw[
                    assistant_raw.find(blocs[i]) + len(blocs[i]) : assistant_raw.find(blocs[j])
                ]
                CORRIGE = re.compile(
                    r"(version corrig|corrig[ée]e?|en fait|plut[ôo]t (ceci|celui|celle)|"
                    r"je reprends|oubli[ée]|erratum|au temps pour moi|voici la bonne)",
                    flags=re.I,
                )
                if not CORRIGE.search(entre):
                    continue
                if True:
                    faults.append(
                        "DEUX VERSIONS DU MEME MESSAGE D AFFILEE. Deux blocs de cette "
                        "reponse se ressemblent a " + str(int(ratio * 100)) + " %. Bentho "
                        "ne doit JAMAIS voir une version puis sa version corrigee sur le "
                        "meme ecran. Affiche UNIQUEMENT la version finale : le lint puis "
                        "le coherence-reviewer passent AVANT le premier affichage."
                    )
                    codes.append("deux-versions-message")
                    stop = True
                    break

    # 1quinquies. SUJET TRAITE DEUX FOIS. Regle posee par Bentho le 2026-09-03 : un
    # sujet apparait UNE fois dans la reponse. Soit il se regle dans le bloc RÉPONSES,
    # soit il demande un developpement et il devient directement sa propre section.
    # Un item du bloc qui renvoie plus bas fait lire deux fois la meme chose.
    bloc = re.search(r"#\s*\*\*•\s*RÉPONSES\*\*(.*?)(?=\n#\s|\Z)", assistant_raw, flags=re.S)
    if bloc:
        RENVOI = re.compile(
            r"(d[ée]tail plus bas|plus bas|ci-dessous|voir plus bas|j'y reviens|"
            r"je d[ée]taille (plus bas|apr[èe]s|en dessous)|dans la section)",
            flags=re.I,
        )
        renvois = [m.group(0) for m in RENVOI.finditer(bloc.group(1))]
        if renvois:
            faults.append(
                "SUJET TRAITE DEUX FOIS. Le bloc RÉPONSES renvoie plus bas ("
                + " || ".join(sorted(set(renvois))[:3])
                + "). Un sujet apparait UNE seule fois : soit il se regle dans le bloc "
                "RÉPONSES en une a trois phrases, soit il devient directement sa propre "
                "section titree avec le meme label, et il ne figure PAS dans le bloc. "
                "Jamais les deux, Bentho lirait deux fois la meme chose."
            )
            codes.append("sujet-deux-fois")

    # 2. TIRET LONG.
    if re.search(r"[—–]", prose):
        faults.append("TIRET LONG present. Interdit partout. Utiliser virgule, parenthese ou phrase separee.")
        codes.append("tiret-long")

    # 3. TITRES AU MAUVAIS FORMAT.
    if re.search(r"^#{2,}\s", assistant_raw, flags=re.M):
        faults.append(
            "TITRE avec ## ou ###. Format impose : '# **• TITRE**' ou "
            "'# **<pastille> LABEL**', un seul diese, en MAJUSCULES."
        )
        codes.append("titre-format")

    # 4. QUESTIONS DE BENTHO NON TRAITEES EN BLOC VISIBLE.
    user_prose = strip_code(user_raw)
    # on ignore les injections de hook pour compter les vraies questions
    user_prose = re.sub(r"<system-reminder>.*?</system-reminder>", " ", user_prose, flags=re.S)
    user_prose = re.sub(r"(REGLES DE SORTIE|PROTOCOLE D'ACTIVATION|DECOUPAGE DU MESSAGE|TACHES OUVERTES).*", " ", user_prose, flags=re.S)
    # Une demande d'explication est une question, avec ou sans point d'interrogation.
    INTERROGATIF = re.compile(
        r"\b(pourquoi|comment|est-ce que|qu'est-ce|c'est quoi|combien|lequel|laquelle|"
        r"lesquels|ou est|où est|quand est-ce|explique[ -]moi|dis[ -]moi pourquoi|"
        r"je (ne )?comprends pas pourquoi|tu peux (me )?(dire|expliquer|verifier|vérifier))\b",
        flags=re.I,
    )
    # 2026-09-03, critere du SUJET valide par Bentho. Le bloc RÉPONSES ne se
    # declenche plus au premier "?" mais quand le message porte PLUSIEURS demandes.
    # Trois questions qui precisent un meme point appellent une reponse, pas trois.
    # Le comptage mecanique ne sait pas lire un sujet, il approxime par le nombre de
    # marqueurs interrogatifs et se tait au moindre doute: le regroupement par sujet
    # est un jugement, il reste a ma charge, avec le garde-fou que le label NOMME le
    # sujet et annonce quand il regroupe plusieurs questions de Bentho.
    # On prend le MAXIMUM, pas la somme : "Est-ce que c'est clair ?" porte un "?" ET
    # un marqueur "est-ce que", additionner les deux compterait une seule demande
    # comme deux et exigerait un bloc RÉPONSES pour une question unique.
    signaux = max(user_prose.count("?"), len(INTERROGATIF.findall(user_prose)))
    if signaux >= 2:
        has_block = bool(re.search(r"#\s*\*\*•\s*RÉPONSES", assistant_raw))
        if not has_block:
            faults.append(
                "BENTHO A POSE PLUSIEURS DEMANDES et ma reponse ne contient pas le bloc "
                "'# **• RÉPONSES**'. Obligatoire des 2 sujets : ce bloc ouvre la reponse, chaque SUJET "
                "y est nomme par un LABEL COURT en gras et numerote (1., 2., 3.), JAMAIS la question "
                "recopiee, avec SA reponse juste "
                "dessous, avant tout livrable. Une question fermee commence par Oui ou Non."
            )
            codes.append("bloc-reponses")

    # 5. DEMANDE DE PERMISSION APRES UN GO.
    user_low = user_prose.lower()
    gave_go = bool(re.search(r"\bgo\b|\bvas-y\b|\bfais-le\b", user_low))
    tail = "\n".join([l for l in prose.strip().splitlines() if l.strip()][-4:]).lower()
    # 2026-09-03. Une question qui fait CHOISIR entre options nommees ("A ou B ?",
    # "je fige X, ou tu vois un cas ou ca tombe a cote ?") n'est pas une demande
    # d'autorisation, c'est un arbitrage que Bentho a explicitement reclame. Seule
    # une demande de feu vert nue reste fautive.
    tail_q = re.search(r"[^.\n]*\?", tail)
    tail_q = tail_q.group(0) if tail_q else ""
    arbitrage = bool(re.search(r"\bou\b|\boption [abc]\b|,\s*ou\s", tail_q))
    asks_permission = bool(
        re.search(r"(je fais|je lance|je crée|je fige|j'applique|on part sur|tu veux que je|je te (le )?fais)\b[^.\n]{0,60}\?", tail)
    ) and not arbitrage
    if gave_go and asks_permission:
        faults.append(
            "DEMANDE DE PERMISSION alors que Bentho a dit go. Interdit. Une fois le go donne, "
            "on execute et on rend compte, on ne redemande jamais l'autorisation."
        )
        codes.append("permission-apres-go")

    # 6. LIVRABLE DIT PRET SANS PASSAGE COHERENCE-REVIEWER.
    claims_ready = bool(
        re.search(
            r"(prêt à (envoyer|coller|partager)|c'est prêt|tu peux (l')?envoyer|"
            r"prête à envoyer|bon pour envoi|version finale)",
            prose,
            flags=re.I,
        )
    )
    if claims_ready and "coherence-reviewer" not in recent:
        faults.append(
            "LIVRABLE ANNONCE COMME PRET sans avoir lance l'agent coherence-reviewer. "
            "Regle dure : tout objet partageable passe par coherence-reviewer AVANT d'etre "
            "dit pret. Lancer l'agent, puis rendre compte."
        )
        codes.append("coherence-reviewer")

    # 8. ACTION A FAIRE SANS PROCEDURE NUMEROTEE.
    if ACTION.search(prose) and not ETAPE.search(assistant_raw):
        faults.append(
            "ACTION A FAIRE SANS PROCEDURE NUMEROTEE. Des que Bentho doit executer quelque "
            "chose, la reponse contient des etapes 1., 2., 3., une seule action par etape, "
            "le bouton nomme exactement comme il apparait a l'ecran, l'endroit precis ou "
            "coller, et ce qu'il doit voir apres."
        )
        codes.append("action-sans-etapes")

    # 9. ELEMENT DESIGNE PAR SA COULEUR SANS SON TEXTE.
    mauvaises = couleurs_sans_ancre(assistant_raw)
    if mauvaises:
        faults.append(
            "ETAPE QUI DESIGNE UN ELEMENT PAR SA COULEUR SANS SON TEXTE EXACT. Occurrences : "
            + " || ".join(mauvaises[:3])
            + ". Un element se designe par le texte qu'il porte, mis en gras. Une couleur "
            "non verifiee envoie Bentho chercher quelque chose qui n'existe pas a l'ecran."
        )
        codes.append("couleur-sans-ancre")

    return faults, codes


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    # Anti boucle infinie : si on a deja bloque ce tour, on laisse passer.
    if payload.get("stop_hook_active"):
        sys.exit(0)

    assistant_raw, user_raw, recent = read_transcript(payload.get("transcript_path"))
    if not assistant_raw.strip():
        sys.exit(0)

    faults, codes = run_checks(assistant_raw, user_raw, recent)

    if not faults:
        sys.exit(0)

    log_violation(codes)
    numbered = "\n".join("{}. {}".format(i + 1, f) for i, f in enumerate(faults))

    # Lint passe avant emission: on n'interrompt plus, on signale.
    if lint_a_tourne(recent):
        print(json.dumps({
            "systemMessage": "Avertissement de sortie (non bloquant), "
            + str(len(faults)) + " point(s) : " + " | ".join(faults)
        }, ensure_ascii=False))
        sys.exit(0)

    reason = (
        "VERROU DE SORTIE. Le lint d avant emission n a pas ete lance sur cette "
        "reponse, et elle viole des regles de Bentho.\n\n"
        + numbered
        + "\n\nINTERDICTION ABSOLUE DE REPUBLIER LA REPONSE. Bentho a deja lu le message "
        "ci-dessus une fois, le lui reservir une seconde fois est une faute plus grave que "
        "la violation elle-meme. Tu produis UNIQUEMENT un correctif chirurgical, aussi court "
        "que possible : le ou les fragments fautifs et leur version corrigee, rien d autre. "
        "Jamais le texte entier, jamais un resume, jamais une reprise des titres ou des "
        "sections. Pas de commentaire sur ce blocage."
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


if __name__ == "__main__":
    main()
