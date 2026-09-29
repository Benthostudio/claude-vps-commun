#!/usr/bin/env python3
"""Decoupage du message de Bentho en items, et refus de sortie si des questions sautent.

Pourquoi (2026-08-17, Bentho). Le defaut recurrent n'est pas l'ignorance des regles, c'est
qu'un message melangeant une question sur un sujet et un ordre sur un autre est traite
comme un bloc: la production ecrase les questions et un item saute. Sa formulation exacte:
"tout fonctionne par sujet, tout fonctionne par tache. Un go n'est jamais general, une
question n'est jamais generale."

Deux modes.
  prompt : decoupe le message, classe chaque segment en QUESTION ou ORDRE, reinjecte la
           liste numerotee en tete de contexte et memorise le compte des questions.
  stop   : relit la reponse reellement ecrite et REFUSE la fin du tour s'il manque des
           reponses. C'est la piece qui rend la regle deterministe: un texte dans un
           prompt reste probabiliste, un hook qui bloque ne l'est pas.

Garde-fou anti-boucle: une seule interception par message, le drapeau est efface a chaque
nouveau message de Bentho.
"""

import json
import os
import re
import sys

STATE = os.path.expanduser("~/.claude/state")
LEDGER = os.path.join(STATE, "ledger.json")
BLOCKED = os.path.join(STATE, "ledger-blocked")
TASKS = os.path.join(STATE, "tasks-open.md")

# Messages automatiques du systeme: rien a decouper.
NOISE = (
    "system-reminder",
    "hook additional context",
    "standing output rules",
    "protocole d activation",
    "protocole d'activation",
    "task-notification",
    "<system",
    "posttooluse",
    "pretooluse",
    "userpromptsubmit",
)

QWORDS = (
    r"\b(comment|pourquoi|combien|est[- ]ce que|qu[' e]est[- ]ce que|quel|quelle|quels|"
    r"quelles|quoi|explique|c[' e]est quoi|ton avis|tu en penses|tu penses quoi)\b"
    r"|je (ne )?comprends pas"
)

# L imperatif peut arriver n importe ou dans le segment, pas seulement en tete:
# "Tu parles de ratio, bah dis quel est le ratio" est un ordre, pas une question.
IMPERATIF = (
    r"(^|[,;.!]\s*|\b(bah|ben|alors|donc|ensuite|puis|et|bref|maintenant|s[' ]il te pla[iî]t)\s+)"
    r"(dis|donne|mets|met|fais|refais|corrige|ajoute|enleve|retire|supprime|change|"
    r"remplace|verifie|regarde|lance|envoie|redige|ecris|applique|adapte|garde|"
    r"rentre|passe|prends|utilise|reprends|arrete|pose|sois|va|montre|explique|"
    r"calcule|compte|cherche|trouve|liste|note|rends|deploie|construis|cree)\b"
)

OWORDS = (
    r"\b(go|vas[- ]y|fais|refais|refait|corrige|ajoute|ajouter|mets|met|supprime|enleve|"
    r"retire|envoie|redige|ecris|change|remplace|applique|lance|deploie|construis|cree|"
    r"divise|adapte|verifie|regarde|liste|garde|rentre|rends|passe)\b"
)


def load_stdin():
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def write_ledger(payload):
    os.makedirs(STATE, exist_ok=True)
    with open(LEDGER, "w") as fh:
        json.dump(payload, fh)



CADENCE = 7          # un rappel tous les 7 messages
PLAFOND = 10         # 10 taches au maximum dans le rappel
COMPTEUR = os.path.join(STATE, "taches-compteur")
PERSO = os.path.join(STATE, "taches-perso.md")


def load_stdin_cwd():
    """Le dossier de travail courant, qui designe le projet."""
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def rappel_taches(cwd):
    """Rappelle les taches ouvertes du projet, une fois tous les CADENCE messages.

    Regle posee par Bentho le 2026-09-03. L'ancien mecanisme injectait 15 taches a
    CHAQUE message pour 2 639 caracteres, ce qui l'a rendu invisible a force d'etre
    la. Ici, plafond de 10 taches, une fois sur 7, priorisees par l'ordre du fichier,
    lui-meme tenu selon la deadline du projet. La liste complete arrive en debut de
    session (compteur absent).
    """
    fichiers = [os.path.join(cwd, "TACHES.md"), PERSO]
    taches = []
    for f in fichiers:
        if not os.path.exists(f):
            continue
        etiquette = "perso" if f == PERSO else os.path.basename(os.path.dirname(f))
        try:
            with open(f, encoding="utf-8") as fh:
                for l in fh:
                    if l.lstrip().startswith(("- [ ]", "* [ ]")) or re.match(r"^\s*\d+\.\s*\[ \]", l):
                        taches.append("  [%s] %s" % (etiquette, l.strip()))
        except OSError:
            pass
    if not taches:
        return []

    os.makedirs(STATE, exist_ok=True)
    try:
        n = int(open(COMPTEUR).read().strip() or 0)
    except Exception:
        n = 0            # debut de session, on rappelle tout de suite
    open(COMPTEUR, "w").write(str((n + 1) % CADENCE))
    if n % CADENCE != 0:
        return []

    entete = "TACHES OUVERTES (%d)." % len(taches)
    if len(taches) > PLAFOND:
        entete += " Les %d premieres, par ordre de priorite." % PLAFOND
    return [entete, "Rappel automatique tous les %d messages. Fermer une tache = retirer sa ligne." % CADENCE] + taches[:PLAFOND]


def mode_prompt():
    prompt = load_stdin().get("prompt", "") or ""
    low = prompt.lower()

    if not prompt.strip() or any(n in low for n in NOISE):
        write_ledger({"questions": 0, "orders": 0, "items": []})
        return 0

    # La dictee vocale de Bentho ponctue mal, donc on coupe aussi sur les retours a la
    # ligne, pas seulement sur la ponctuation forte.
    raw = re.split(r"(?<=[.!?])\s+|\n+", prompt)
    segments = [s.strip() for s in raw if len(s.strip()) > 3]

    items = []
    for seg in segments:
        sl = seg.lower()
        is_q = seg.rstrip().endswith("?") or re.search(QWORDS, sl) is not None
        is_o = re.search(OWORDS, sl) is not None
        # L IMPERATIF PRIME SUR L INTERROGATIF (Bentho, 24.08). "dis quel est le ratio"
        # contient "quel" mais commence par un imperatif: c est un ORDRE, pas une
        # question. Classer un ordre en question me faisait repondre au lieu de faire,
        # ce qui a produit cinq allers-retours pour rien dans une seule journee.
        # Un imperatif suffit a faire un ordre, meme si OWORDS ne liste pas ce verbe.
        if re.search(IMPERATIF, sl):
            is_o = True
            is_q = False
        # Une phrase qui NIE etre une question n en est pas une, meme si elle contient
        # "pourquoi": "ce n est pas une question, pourquoi tu me reponds".
        if is_q and re.search(r"(c(e n)?est pas une question|pas une question|je te dis de)", sl):
            is_q = False
            is_o = True
        if is_q:
            items.append(("Q", seg))
        elif is_o:
            items.append(("O", seg))

    qn = sum(1 for t, _ in items if t == "Q")
    on = sum(1 for t, _ in items if t == "O")
    write_ledger(
        {
            "questions": qn,
            "orders": on,
            "items": [{"type": t, "text": s[:300]} for t, s in items],
        }
    )

    # Nouveau message: on rearme le blocage de sortie.
    if os.path.exists(BLOCKED):
        os.remove(BLOCKED)

    if not items:
        return 0

    out = [
        "DECOUPAGE DU MESSAGE (traiter CHAQUE item, aucun item sautable).",
        "Une [Q] appelle une reponse ecrite. Un [O] appelle une execution.",
        "Une [Q] et un [O] peuvent porter sur DEUX SUJETS DIFFERENTS dans le meme message:",
        "repondre a la [Q] de son sujet ET executer le [O] de son sujet, jamais l un a la",
        "place de l autre. Si un item est mal classe, le dire en une ligne, ne pas l ignorer.",
        "",
    ]
    qi = oi = 0
    for t, seg in items:
        if t == "Q":
            qi += 1
            out.append("[Q%d] %s" % (qi, seg[:280]))
        else:
            oi += 1
            out.append("[O%d] %s" % (oi, seg[:280]))
    out.append("")
    out.append("TOTAL: %d question(s), %d ordre(s). La reponse doit couvrir les %d." % (qn, on, qn + on))

    rappel = rappel_taches(load_stdin_cwd())
    if rappel:
        out.append("")
        out.extend(rappel)

    # 2026-09-03. La capture automatique des taches est COUPEE. Chaque segment
    # imperatif de la dictee de Bentho etait ecrit dans tasks-open.md pour toujours,
    # sans aucun mecanisme de fermeture: 1531 lignes accumulees, 85 doublons exacts,
    # 3 cochees en tout. Ce n'etaient pas des taches mais des fragments de phrases,
    # reinjectes a chaque message. Le fichier est conserve intact, il n'est plus ni
    # alimente ni relu. Le decoupage question contre ordre, lui, reste actif.

    print("\n".join(out))
    return 0


def last_assistant_text(path):
    text = ""
    try:
        with open(path) as fh:
            for line in fh:
                try:
                    ev = json.loads(line)
                except Exception:
                    continue
                if ev.get("type") != "assistant":
                    continue
                content = ev.get("message", {}).get("content", [])
                chunk = "".join(
                    c.get("text", "")
                    for c in content
                    if isinstance(c, dict) and c.get("type") == "text"
                )
                if chunk.strip():
                    text = chunk
    except Exception:
        return ""
    return text


def mode_stop():
    if os.path.exists(BLOCKED) or not os.path.exists(LEDGER):
        return 0

    data = load_stdin()
    try:
        with open(LEDGER) as fh:
            ledger = json.load(fh)
    except Exception:
        return 0

    expected = int(ledger.get("questions", 0))
    # En dessous de deux questions le comptage est trop bruite pour bloquer sans risque.
    if expected < 2:
        return 0

    path = data.get("transcript_path", "")
    if not path or not os.path.exists(path):
        return 0

    last = last_assistant_text(path)
    if not last.strip():
        return 0

    # Marqueurs de reponse traitee, un par item. Une reponse en un seul pave pour trois
    # questions echoue par construction, ce qui est exactement le cas a bloquer.
    markers = 0
    markers += len(re.findall(r"^#\s+\*\*", last, re.M))
    markers += len(re.findall(r"^\s*\d+\.\s+", last, re.M))
    markers += len(re.findall(r"^\s*\*{0,2}(Oui|Non)\b", last, re.M))

    if markers >= expected:
        return 0

    # Bentho, 2026-08-19: ne PLUS bloquer la fin de tour. Le blocage forcait une seconde
    # reponse corrigee, et l affichage montrait la version rejetee PUIS la corrigee, d ou les
    # reponses en double (et la premiere, non corrigee, en tete). Priorite absolue exprimee
    # par Bentho: jamais de reponse en double, jamais la version non corrigee en premier. Le
    # decoupage cote prompt (mode_prompt) reste actif pour lister les questions; c est
    # desormais a moi de toutes les traiter du premier coup, sans filet deterministe.
    return 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "prompt"
    sys.exit(mode_stop() if mode == "stop" else mode_prompt())
