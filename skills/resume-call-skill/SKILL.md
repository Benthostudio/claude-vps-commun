---
name: resume-call-skill
description: Génère un résumé d'appel client standardisé et le publie en page Notion, à partir d'un transcript d'appel + (optionnel) un lien de page projet Notion. À utiliser quand Bentho fournit un transcript d'appel et veut le compte-rendu formaté dans Notion, quel que soit le projet (y compris prospect sans projet créé). Version SKILL (interactive, tourne dans la conversation courante) à comparer avec l'agent resume-call-agent.
---

# Résumé d'appel (version Skill)

Tu produis un résumé d'appel client professionnel et tu le publies dans Notion. Tu tournes dans la conversation courante : tu PEUX et DOIS poser une question à Bentho dès qu'une info critique manque, avant de finaliser. Ne jamais inventer.

## Entrées attendues
- Le **transcript** de l'appel (collé ou en fichier).
- Optionnel : le **lien de la page projet Notion** où publier.

Si le transcript manque, le demander. Si le lien projet manque, suivre l'étape de lookup ci-dessous.

## Passe préalable sur la page d'appel (OBLIGATOIRE, avant toute rédaction)
Avant même de commencer le résumé, TOUJOURS lire la page de l'appel elle-même (la page où le résumé va vivre ou sa page parente) et repérer les annotations que Bentho ajoute directement dessus. Il les marque en général par un signe `=` puis en **gras** (parfois juste en gras, ou une majuscule type `YES` / `OK` / `A CONFIRMAR` / `JULIAN` collée à une question). Faire un diff mental avec l'état précédent connu pour capter ce qu'il a ajouté, déplacé ou changé (ex : une question passée de "à décider aujourd'hui" vers "à répondre en asynchrone"). Ces annotations FONT AUTORITÉ : elles tranchent les points laissés ouverts et corrigent mes suppositions. Les intégrer avant de rédiger. Vaut pour tous les projets.

## Workflow
1. Lire le transcript, identifier le projet (2-3 mots-clés : nom client, sujet).
2. Faire la passe préalable ci-dessus sur la page d'appel et intégrer les annotations de Bentho.
3. Trouver la page projet dans le CRM Notion (voir Lookup). Si pas de lien fourni et match ambigu ou introuvable : **demander à Bentho** avant de publier.
4. Si aucun projet n'existe encore (prospect) : **demander à Bentho où placer la page** (ne pas inventer d'emplacement).
5. Rédiger le résumé selon la structure et le code couleur ci-dessous.
6. Publier la page Notion via le MCP `notion` (générique studio-makers), ou `notion-julien` si le projet est Telos.
7. Avant de finaliser : si une info critique manque (date du prochain RDV, nom complet d'un participant, échéance d'une action), poser la question.
8. Donner à Bentho le lien de la page créée.

## Lookup CRM Notion
- Workspace : studio-makers, MCP `notion` (PAS `notion-julien`, réservé à Telos).
- Database Projets / data source : `collection://7ece2fa5-89ab-474d-ba83-dbb892a10a6a`
- Query par mots-clés du projet. Match unique → page projet. Sinon → demander.

## Emplacement de la page
- Par défaut : **direct sub-page de la page projet** (au même niveau que "Pre-prod", etc., pas nesté dessous).
- Titre : **"Résumé Call XX.XX"** (jour.mois, sans année).

## Structure (ordre fixe)
1. **TL;DR** : callout 📌 sans couleur, 3 à 5 lignes. Sujet principal, décision clé, prochaine action.
2. **Infos** : date, durée, format (Zoom/Meet/présentiel/tél), enregistrement (oui/non + lien).
3. **Participants** : nom, rôle, présence (présent/excusé). Identifier le décideur.
4. **Contexte** : un paragraphe court, où on en est dans le projet.
5. **Sujets abordés** : un H3 par sujet, l'essentiel des échanges.
6. **Décisions prises** : bullets, choix arrêtés (différent des actions).
7. **Actions** : tableau Action / Responsable / Échéance / Statut, une ligne par action, verbe à l'infinitif.
8. **Questions ouvertes** : bullets, avec owner si possible.
9. **Prochaines étapes** : prochain RDV, format, agenda, livrables attendus.
10. **Liens & ressources** : tous les liens cités.

## Code couleur Notion (H2 par section)
Règles : aucune couleur ne se répète. H2 = fond pastel + texte même couleur foncée. H3 = texte coloré assorti, sans fond. Corps sans couleur. `<empty-block/>` entre chaque section.

Syntaxe : `## <span color="blue">Infos</span> {color="blue_bg"}` et `### Sous-titre {color="blue"}`.

| Section | Couleur |
|---|---|
| Infos | blue |
| Participants | purple |
| Contexte | brown |
| Sujets traités | orange |
| Décisions | green |
| Actions | red |
| Questions ouvertes | yellow |
| Prochaines étapes | pink |
| Ressources | gray |

## Règles de style
- "Nous" pour StudioMakers, jamais "je".
- Zéro em dash et zéro double tiret. Utiliser deux points, virgules, parenthèses.
- Phrases continues pour le copier-coller, pas de retour à la ligne dur au milieu d'une idée. Les sauts de ligne séparent seulement les sections.
- Chiffres concrets, jamais "fort/moyen/faible" sans valeur.
- Tableaux : markdown pipes uniquement, jamais de HTML `<table>` (Notion aplatit les cellules).
- Ton professionnel mais lisible, pas robotique.
