---
name: etude-marche-express
description: "Étude de marché express d'une idée (concept, app, business) ou d'un marché : est-ce que ça existe déjà, qui sont les acteurs les plus proches, leurs dates de création, traction, valorisations et levées, et le potentiel de marché. Package la méthode StudioMakers rodée sur La Sphère (fiches concurrents vérifiées + historique des financements + synthèse attractivité/trous/positionnement). Utiliser ce skill dès que Bentho balance une idée à évaluer ou demande : 'étude de marché', 'benchmark le marché de X', 'est-ce que ça existe déjà', 'qui sont les concurrents de', 'quel est le potentiel de', 'y a-t-il des apps qui font X', 'à combien sont valorisés les acteurs de Y', même formulé casuellement ('j'ai une idée d'app, dis-moi ce qui existe')."
---

# Étude de marché express

Ce skill répond à la question récurrente de Bentho quand il a une idée ou explore un marché :
**"est-ce que ça existe déjà, qui le fait, combien ça vaut, et est-ce qu'il y a une place ?"**.
Il transforme une idée décrite en deux phrases en une carte factuelle et sourcée du marché,
puis en lecture stratégique actionnable. C'est la méthode rodée sur La Sphère (étude de la
concurrence + benchmark de levées + synthèse), packagée pour être rejouée sur n'importe
quelle idée en une session.

La sortie par défaut est **dans le chat, en français**, au format habituel de Bentho
(titres `# **• TITRE**`, numérotation 1/2/3, tableaux markdown). Une page Notion ou un
fichier = étape distincte, demander l'emplacement avant de créer quoi que ce soit.

## Garde-fous non négociables (hérités des règles Bentho)

1. **Aucun chiffre inventé.** Tout montant, date, valorisation ou chiffre d'utilisateurs
   s'appuie sur une source citée (lien). Ce qui n'est pas public s'écrit "n.c." (non
   communiqué). Ce qui est estimé sans source fiable s'écrit avec la mention "(approximation)".
   Jamais d'ordre de grandeur flou non marqué ("des dizaines de millions").
2. **Positionnement réel vérifié.** Ne pas décrire un concurrent de mémoire : vérifier par
   recherche web ce qu'il fait AUJOURD'HUI (les pivots sont fréquents). Préférer des actions
   documentées et datées à des généralités.
3. **Signaler les trous.** La carte n'est jamais exhaustive (deals privés non annoncés,
   acteurs morts sans trace). Toujours finir par ce qui n'a pas pu être trouvé ou confirmé.
4. **Distinguer les stades et les dates.** Une levée de 2015 et une de 2024 ne racontent pas
   le même marché. Toujours dater.

## Le déroulé

### 1. Cadrer (avant toute recherche)

Reformuler l'idée en une phrase et fixer le scope. Si un de ces points est ambigu ET change
le résultat, poser la question à Bentho d'abord ; sinon prendre le défaut et l'annoncer :
1. Le concept exact et son mécanisme différenciant (qu'est-ce qui le distingue en une phrase).
2. La géographie (défaut : international, avec un oeil sur la France et l'Europe).
3. Les adjacences à inclure (les concurrents indirects qui résolvent le même problème
   autrement) : en lister 2-3 et les inclure d'office, c'est souvent là qu'est la vraie
   concurrence.
4. Ce que Bentho veut décider avec l'étude (lancer, écarter, pivoter, chiffrer).

### 2. Chercher (recherche web fan-out)

Combiner les angles, en parallèle quand c'est possible :
1. Par concept : "[concept] app", "apps like [concept]", "best [concept] apps 2025/2026".
2. Par acteur repéré : "[nom] funding raised valuation", "[nom] users revenue", "[nom] shut down / acquired".
3. Par agrégateurs : Crunchbase, Tracxn, Dealroom, TechCrunch, Sifted (Europe), Maddyness (France).
4. Par échecs : "who tried [concept] and failed", les morts sont aussi instructifs que les vivants.
Quand la carte des financements doit être approfondie, s'appuyer sur le skill
funding-landscape-scan (même workspace de règles) plutôt que de réinventer sa structure.

### 3. Structurer : les deux tableaux

**Tableau 1, les acteurs (fiches concurrents condensées)** : une ligne par acteur, du plus
proche au plus lointain du concept.

| Acteur | Pays | Créé en | Ce qu'il fait vraiment (vérifié) | Proximité avec l'idée | Traction connue | Source |
|---|---|---|---|---|---|---|

**Tableau 2, l'argent** : une ligne par acteur (ou par deal marquant).

| Acteur | Total levé | Dernier deal connu (date, stade, montant) | Valorisation | Exit / état | Source |
|---|---|---|---|---|---|

Règles : trier par proximité décroissante ; "n.c." pour le non-public ; dater chaque deal ;
inclure les morts et les pivots (colonne état) ; liens cliquables en source.

### 4. Lire : la synthèse stratégique

Toujours conclure par une lecture orientée décision :
1. **Est-ce que ça existe déjà ?** Oui/non/partiellement, et qui est LE plus proche.
2. **Le marché est-il validé par le capital ?** Nombre de deals, montants, à quels stades,
   et si le capital est chaud, refroidi ou jamais venu.
3. **Ce que les morts enseignent.** Qui a essayé et échoué, et pourquoi (si documenté).
4. **Le trou.** Ce que personne ne fait exactement, et si ce trou est une opportunité ou un
   cimetière (un trou peut exister parce que le modèle ne marche pas).
5. **Le potentiel pour l'idée de Bentho.** En 2-3 phrases honnêtes : différenciation réelle,
   taille de l'enjeu, finançable ou bootstrap, et le risque n°1. Challenger l'idée si les
   faits l'exigent : l'objectif est le meilleur produit, pas de faire plaisir.

### 5. Signaler les trous de l'étude

Une ligne d'honnêteté finale : ce qui n'a pas pu être vérifié, et si un accès payant
(Crunchbase Pro, PitchBook, Sensor Tower pour les downloads) donnerait une image plus fiable.

## Exemple de ton visé (extrait de synthèse)

"Oui, ça existe : X est le plus proche (créé 2021, 15 M$ levés, positionnement quasi
identique sauf [détail]). Le capital est venu en 2021-2022 puis s'est refroidi, deux acteurs
sont morts (Y, Z) faute de rétention. Le trou réel n'est pas la feature, c'est [angle]. Pour
ton idée : différenciante seulement si [condition], sinon on est le 6e entrant d'un marché
qui n'a pas encore prouvé sa rétention. Risque n°1 : [risque]."
