#!/usr/bin/env python3
"""Verrou NOTION en amont: refuse une ecriture Notion qui casse la regle 13 (couleurs).

Pourquoi ce hook existe (Bentho, 2026-08-24).
La regle des couleurs Notion est ecrite a cinq endroits (memoire
feedback-couleurs-entetes-notion, hook output-rules.sh regle 13, memoires
notion-couleur-syntaxe-bg et feedback-presentation-propositions-notion, skill
proposition-commerciale) mais AUCUN controle mecanique ne la faisait respecter.
Resultat le 2026-08-24: une page publiee avec `<span color="blue_bg">` au lieu de
`{color="blue_bg"}`, donc trois titres rendus plats, et Bentho qui doit reprendre.

Le lint-draft.py protege le texte du chat, ce hook protege les ecritures Notion.
Il tourne sur PreToolUse, donc AVANT que la page parte.

Syntaxe attendue:
  titre de section  ->  # <span color="blue">TITRE</span> {color="blue_bg"}
  sous-titre        ->  ## <span color="blue">Sous-titre</span>
"""
import json
import os
import re
import sys

COLORS = "gray|brown|orange|yellow|green|blue|purple|pink|red"
HEADING = re.compile(r"^(#{1,4})\s+(.*)$")
SPAN = re.compile(r'<span\s+color="(' + COLORS + r')(_bg)?"\s*>', re.I)
BLOCK_BG = re.compile(r'\{color="(' + COLORS + r')_bg"\}', re.I)
BACKGROUND = re.compile(r'_background', re.I)
SPAN_BG = re.compile(r'<span\s+color="(?:' + COLORS + r')_bg"', re.I)

WRITE_TOOLS = (
    "mcp__notion__notion-create-pages",
    "mcp__notion__notion-update-page",
    "mcp__notion-benjamin-tho__API-post-page",
    "mcp__notion-benjamin-tho__API-patch-block-children",
    "mcp__notion-benjamin-tho__API-update-page-markdown",
)


def stdin_json():
    try:
        return json.loads(sys.stdin.read() or "{}")
    except Exception:
        return {}


def collect_markdown(ti):
    """Recupere tout le markdown envoye a Notion, quelle que soit la forme de l'appel."""
    chunks = []
    for page in (ti.get("pages") or []):
        if isinstance(page, dict) and page.get("content"):
            chunks.append(page["content"])
    for key in ("content", "new_str", "markdown"):
        if ti.get(key):
            chunks.append(ti[key])
    for upd in (ti.get("content_updates") or []):
        if isinstance(upd, dict) and upd.get("new_str"):
            chunks.append(upd["new_str"])
    return "\n".join(c for c in chunks if isinstance(c, str))


def check(md):
    """Rend la liste des violations de la regle 13."""
    bad = []

    if BACKGROUND.search(md):
        bad.append(
            "`_background` est utilise. Notion l'ignore SILENCIEUSEMENT, le titre "
            "ressort noir sans erreur. Le suffixe est `_bg`."
        )
    if SPAN_BG.search(md):
        bad.append(
            "Le fond est mis DANS le span (`<span color=\"blue_bg\">`). Le span porte "
            "la couleur du TEXTE, le fond passe par l'attribut de bloc pose apres la "
            "balise fermante. Forme exacte: "
            "`# <span color=\"blue\">TITRE</span> {color=\"blue_bg\"}`."
        )

    headings = []
    for line in md.splitlines():
        m = HEADING.match(line.strip())
        if not m:
            continue
        level = len(m.group(1))
        rest = m.group(2)
        span = SPAN.search(rest)
        block = BLOCK_BG.search(rest)
        headings.append({
            "level": level,
            "line": line.strip()[:70],
            "text_color": span.group(1).lower() if span else None,
            "bg_color": block.group(1).lower() if block else None,
        })

    if not headings:
        return bad

    top = min(h["level"] for h in headings)
    section_color = None
    prev_section_color = None

    for h in headings:
        is_section = h["level"] == top
        label = "Titre de section" if is_section else "Sous-titre"

        if h["text_color"] is None:
            bad.append(
                f"{label} sans couleur de texte, `{h['line']}`. Un titre Notion n'est "
                "jamais plat, il porte un `<span color=\"...\">`."
            )
            continue

        if h["text_color"] == "red":
            bad.append(
                f"ROUGE sur un {label.lower()}, `{h['line']}`. Le rouge est interdit "
                "sur tout titre et tout sous-titre, dans tous les documents Notion. "
                "Il n'est tolere que sur un mot dans du texte courant."
            )

        if is_section:
            if h["bg_color"] is None:
                bad.append(
                    f"Titre de section sans fond, `{h['line']}`. Il lui manque "
                    f"`{{color=\"{h['text_color']}_bg\"}}` apres la balise fermante."
                )
            elif h["bg_color"] != h["text_color"]:
                bad.append(
                    f"Titre de section bicolore, `{h['line']}`. Le texte est "
                    f"{h['text_color']} et le fond {h['bg_color']}, ce doit etre la "
                    "meme couleur."
                )
            if prev_section_color and h["text_color"] == prev_section_color:
                bad.append(
                    f"Deux sections voisines de la meme couleur ({h['text_color']}), "
                    f"a `{h['line']}`. Change la couleur de cette section."
                )
            prev_section_color = h["text_color"]
            section_color = h["text_color"]
        else:
            if h["bg_color"] is not None:
                bad.append(
                    f"Sous-titre avec un fond, `{h['line']}`. Un sous-titre porte la "
                    "couleur du texte seule, sans `{color=\"..._bg\"}`."
                )
            if section_color and h["text_color"] != section_color:
                bad.append(
                    f"Sous-titre d'une autre couleur que sa section, `{h['line']}`. "
                    f"Sa section est {section_color}, tous ses sous-titres doivent "
                    f"etre {section_color}."
                )

    return bad


def main():
    data = stdin_json()
    if data.get("tool_name", "") not in WRITE_TOOLS:
        sys.exit(0)

    md = collect_markdown(data.get("tool_input", {}) or {})
    if not md.strip():
        sys.exit(0)

    bad = check(md)
    if not bad:
        sys.exit(0)

    # Deduplique en gardant l'ordre, une meme faute repetee sur dix titres n'aide pas.
    seen, uniq = set(), []
    for b in bad:
        if b not in seen:
            seen.add(b)
            uniq.append(b)

    reason = ["VERROU NOTION, regle 13 des couleurs. Cette ecriture est refusee.", ""]
    reason += [f"{i}. {b}" for i, b in enumerate(uniq[:10], 1)]
    reason += [
        "",
        "Rappel de la forme exacte:",
        '  titre de section   # <span color="blue">TITRE</span> {color="blue_bg"}',
        '  sous-titre         ## <span color="blue">Sous-titre</span>',
        "",
        "Source de verite: ~/.claude/projects/-Users-bentho-ClaudeCode/memory/"
        "feedback-couleurs-entetes-notion.md",
        "Corrige le markdown, puis relance l'ecriture. Refetch la page apres coup.",
    ]

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
