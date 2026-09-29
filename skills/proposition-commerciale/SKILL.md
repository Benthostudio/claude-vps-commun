---
name: proposition-commerciale
description: >
  Construit une proposition commerciale ou une présentation de stratégie StudioMakers
  destinée à un client, sous forme de page Notion, en suivant le template maison
  (en-têtes H1 colorés palette v1, écriture orientée valeur, deux modes : proposition
  complète chiffrée OU exploration de stratégies). À utiliser dès que Bentho veut
  construire, rédiger, structurer ou mettre en forme une proposition commerciale, une
  proposition d'accompagnement, un devis présenté, une offre client, une recommandation
  ou une présentation de stratégie pour n'importe quel projet client (Polimair, Hygiène
  Santé, etc.), même s'il ne dit pas le mot "skill" ou "template". Se déclenche sur des
  formulations comme "fais une proposition pour X", "présentation commerciale", "propose
  une stratégie au client", "document d'accompagnement Notion", "mets ça en proposition".
---

# Proposition commerciale StudioMakers

Ce skill produit un livrable **client** (page Notion) qui doit **convaincre**, pas décrire.
Il encode notre trame maison, nos règles de mise en forme et notre ton, pour que chaque
proposition soit cohérente sans avoir à tout reconstituer à chaque fois.

## Périmètre et garde-fou important

Ce skill concerne les **documents destinés au client** (Notion). Il ne faut PAS confondre
avec les codes de présentation des **réponses de chat à Bentho** (titres `# **• Titre**`,
pastilles rondes 🟢🟡🟣, etc.). Ce sont deux jeux de règles séparés :
- Livrable client = règles ci-dessous (en-têtes H1 colorés, ton orienté valeur).
- Chat avec Bentho = ses préférences de format de réponse (gérées par la mémoire).

## Les deux modes

Identifier le mode dès le départ. En cas de doute, demander à Bentho.

| Mode | Quand l'utiliser | Référence Notion à consulter |
| --- | --- | --- |
| **A. Proposition complète chiffrée** | On recommande une direction et on chiffre (options, prix, planning) | "Proposition d'accompagnement Hygiène Santé" : `34c82d43f9ff8134aa36ce1dfb4a23f6` |
| **B. Exploration de stratégies** | Phase d'idéation : on ouvre le champ des possibles, sans prix ni reco unique | "Accompagnement marketing Polimair : exploration des stratégies" : `37782d43f9ff81768d34f038c0246a6b` |

Avant de rédiger, **toujours lire la page de référence du mode choisi** via `notion-fetch`
pour caler le formatage exact (syntaxe des couleurs, structure des tableaux).

## Processus

1. **Charger le contexte projet.** Lire le `SESSION_LOG.md` et le `CLAUDE.md` du projet,
   puis les pages Notion pertinentes (proposition existante, calls, devis). On ne rédige
   jamais une proposition sans connaître le produit, la cible et l'objectif du client.
2. **Confirmer 4 entrées avec Bentho** (sauf s'il les a déjà données) :
   - le **mode** (A ou B),
   - l'**emplacement Notion** (page parente où créer le document),
   - la **langue** (le livrable client suit la langue de communication du client ; FR par défaut, sauf projet anglophone),
   - le **nom du contact client** (sinon générique "pour [Marque]").
3. **Lire la page de référence** du mode (ids ci-dessus) pour le formatage.
4. **Rédiger et créer la page** via `notion-create-pages` sous la page parente choisie.
5. **Donner le lien cliquable** de la page créée à Bentho.
6. **Mettre à jour le `SESSION_LOG.md`** du projet (livrable créé + lien + décisions).

## Structure, mode A (proposition complète chiffrée)

En-têtes H1 numérotés et colorés. Ordre type (adapter selon le projet) :

1. **Synthèse** `{color="blue_bg"}` : vue d'ensemble visuelle des options ou des périodes, SANS aucun prix. Les prix n'apparaissent QUE dans le détail et le récapitulatif final. Plus notre recommandation, sans chiffres.
2. **Ce que nous avons compris** `{color="green_bg"}` : projet, acquis, gisements de croissance, points bloquants, ce qui a été validé.
3. **Notre lecture stratégique** `{color="purple_bg"}` : priorités + "ce que nous ne faisons pas, volontairement" (montre le discernement).
4. **Les options en détail** `{color="orange_bg"}` : pour chaque option, objectif, périmètre, tableau setup, tableau mensuel, totaux, hors-scope.
5. **Méthodologie** `{color="yellow_bg"}` (si pertinent) : comment on exécute concrètement.
6. **KPIs de succès** `{color="pink_bg"}` : objectifs chiffrés et mesurables par option.
7. **Modalités commerciales** `{color="gray_bg"}` : facturation, engagement.
8. **Pourquoi StudioMakers** `{color="brown_bg"}` : nos atouts, sans comparaison aux autres agences.
9. **Prochaines étapes** `{color="gray_bg"}` : ce qu'il se passe après acceptation.

## Structure, mode B (exploration de stratégies)

1. **Synthèse** `{color="blue_bg"}` : cadre du document + vue d'ensemble (ex : les axes/moteurs), sans prix ni reco unique.
2. **Ce que nous avons compris** `{color="green_bg"}` : marque, situation, point de départ.
3. **Notre lecture stratégique** `{color="purple_bg"}` : la thèse qui rend les choix lisibles.
4. **Les stratégies en détail** `{color="orange_bg"}` : tableaux par axe et par étape de parcours client, colonne bénéfice.
5. **Pourquoi StudioMakers** `{color="brown_bg"}`.
6. **Prochaines étapes** `{color="gray_bg"}` : présentation, choix ensemble, puis plan détaillé et chiffré.

## Règles de mise en forme (Notion)

- **Titres de section colorés obligatoires.** Le texte ET le fond de la même couleur. Syntaxe : `## <span color="blue">1. Titre</span> {color="blue_bg"}`. Jamais de titres plats sans couleur.
- **Sous-titres.** Texte coloré seul, SANS fond, de la même couleur que leur section. Syntaxe : `### <span color="blue">Sous-titre</span>` (pas de `{color="..._bg"}`).
- **Cohérence couleur.** Dans une même section, tous les sous-titres portent la couleur de la section. Deux sections voisines ont toujours des couleurs différentes.
- **Palette** : `blue` / `green` / `purple` / `orange` / `yellow` / `pink` / `brown` / `gray`. **Le rouge n'est JAMAIS utilisé sur un titre ni un sous-titre**, dans aucun document Notion (règle durcie le 2026-08-20), il n'est toléré que sur un mot ponctuel dans du texte courant.
- **Règle complète et à jour** dans la mémoire feedback-couleurs-entetes-notion (source de vérité).
- **Tableaux** pour tout ce qui se compare (options, leviers, coûts, KPIs).

## Règles d'écriture (le ton qui convainc)

Le but est de **convaincre**, donc on ne décrit jamais une "feature" toute seule.

- **Traduire chaque élément en bénéfice** rattaché à l'objectif du client : "afin de…", "pour que…", "ce que ça vous apporte…".
- **Intros de section et de tableau** : une phrase qui explique ce qu'on fait et pourquoi, avant le détail.
- **Ne pas employer "acheter / vendre"** (surtout avant d'avoir parlé prix). Parler de ce qu'on **construit**, de ce que le client **obtient**, de la **valeur**.
- **Ne pas se comparer aux autres agences** ni dire qu'on est "meilleurs". On **montre** la valeur, on ne la revendique pas.
- **Éviter les listes de termes techniques bruts** sans valeur attachée.
- **Jamais de tiret long** (em dash ou dash long) nulle part, dans le texte comme dans les tableaux. Utiliser virgules, parenthèses, deux-points ou phrases séparées.
- **Coûts externes et hors-scope OBLIGATOIRES.** Toujours lister tous les coûts externes à la charge du client sur la durée (hébergement, hébergeur certifié, API IA, emails, nom de domaine, frais Stripe, comptes App Store et Google Play, budget média, plateforme webinaire) et définir le hors-scope (production des contenus, scripts et audios, création des exercices, animation du webinaire, modération, choix et coût de l'hébergeur, budget publicitaire). Par phase et en récap final. On ne facture jamais des milliers d'euros sans expliciter coûts externes et hors-scope.
  - **Chiffrer chaque coût externe (ORDRE DE GRANDEUR).** Le mot clé est "coût" : chaque ligne DOIT porter un ordre de grandeur estimatif chiffré (ex "environ 20 à 50 €/mois", "Apple environ 99 €/an, Google 25 € une seule fois", "environ 1,5 % + 0,25 € par transaction"). Chercher activement les vrais prix. Préciser que ce sont des estimations qui varient selon les fournisseurs choisis et le volume d'usage. Ne jamais laisser une colonne "Nature" floue (mensuel / annuel) sans montant.
  - **Expliciter les coûts non évidents.** Pour tout coût technique (API IA en tête), dire en clair de quoi il s'agit et pourquoi il coûte : quel service précis (ex "le moteur Claude d'Anthropic qui fait dialoguer le compagnon"), et comment il est facturé (à l'usage, au volume). Le client doit comprendre ce qu'il paie.
- **Colonne valeur.** Sur un devis cher, chaque tâche a une colonne "Ce que ça apporte" (résultat ou livrable concret), pas seulement un nom. Et le nom de la tâche dit ce que c'est, pas juste un mot vague.
- **Une tâche = ce que c'est + ce que ça apporte.** Si le nom est ambigu (ex "communauté", "pouvoirs"), préciser concrètement ce qui est construit pour justifier les jours.

## Exemple de ligne orientée valeur

**Mauvais** (descriptif, technique) :
`GEO : optimisation pour moteurs de réponse IA.`

**Bon** (bénéfice rattaché à l'objectif) :
`GEO (réponses IA) | Devenir la réponse de ChatGPT et Perplexity sur le mobilier design écologique | Capter un trafic nouveau que la plupart des marques ignorent encore.`

## Faire évoluer ce template (important)

Ce skill doit se **durcir au fil des projets**. À la fin de chaque proposition livrée,
revenir ici et intégrer ce qu'on a appris : une section qui s'est révélée utile, une
formulation qui a bien marché, un piège à éviter, une nouvelle référence Notion exemplaire.
C'est ce qui transforme une trame figée en template vivant, de plus en plus juste.
Quand une référence devient meilleure que celles citées plus haut, mettre à jour les ids.
