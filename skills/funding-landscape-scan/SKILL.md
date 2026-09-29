---
name: funding-landscape-scan
description: >
  Cartographie l'activité de financement (levées venture, growth, private equity, dette,
  crowdfunding) d'un secteur, d'une catégorie de produit ou d'un marché donné, à partir de
  recherche web multi-sources et citée. Produit un tableau structuré des rounds (entreprise,
  montant, date, série/stade, investisseurs lead + notables, valorisation si dispo, lien
  source) PUIS une synthèse business : est-ce que la catégorie attire du capital
  institutionnel, à quels stades, montants typiques, quels investisseurs sont actifs, quelles
  tendances (up/down rounds, consolidation). Réutilisable sur n'importe quel secteur, tech
  ou non-tech (retail, food, D2C, hardware, santé, etc.). À utiliser dès que Bentho veut
  savoir qui a levé dans un domaine, le paysage des financements d'un marché, si un type de
  business lève des fonds, ou une cartographie de deals. Se déclenche sur "qui a levé dans X",
  "les levées de fonds dans le secteur Y", "map the funding rounds in Z", "cartographie des
  financements", "est-ce que ce genre de business lève", "quels VC sont actifs sur X",
  "combien lèvent les boîtes de type Y". Se combine avec le skill/harness deep-research pour
  la partie collecte, et avec competitor-intelligence quand la question mêle concurrents et
  financements.
---

# Cartographie des levées de fonds d'un secteur

Ce skill répond à une question récurrente de Bentho quand il explore un marché qu'il connaît
mal : **"est-ce que ce genre de business lève des fonds, et qui ?"**. Il transforme une
question floue en une carte factuelle, chiffrée et sourcée du capital d'un secteur, puis en
lecture stratégique actionnable.

La sortie par défaut est **interne, en français, dans le chat** (format de réponse habituel de
Bentho : titres `# **• TITRE**`, numérotation 1/2/3, tableaux). Si Bentho veut ensuite un
livrable client ou une page Notion, c'est une étape distincte (voir la fin).

## Garde-fous non négociables

1. **Aucun chiffre inventé.** Une levée n'entre dans le tableau que si elle est vérifiable et
   accompagnée d'une source. Si un montant est estimé, rumeur, ou non confirmé, l'écrire
   explicitement (colonne source = "non confirmé / rumeur presse") plutôt que de le présenter
   comme un fait. Un tableau à moitié vide mais juste vaut mieux qu'un tableau plein et faux.
2. **Toujours dater et sourcer.** Chaque round porte une date (au moins l'année) et un lien
   vers la source. Sans source, la ligne ne compte pas.
3. **Devise et ordre de grandeur clairs.** Toujours préciser la devise (USD, EUR...) et ne
   jamais mélanger des montants sans le dire. Convertir si utile, mais garder la valeur
   d'origine.
4. **Distinguer le stade.** Pre-seed / Seed / Series A/B/C.../ growth / PE / dette /
   crowdfunding ne racontent pas la même histoire. C'est la colonne la plus importante pour la
   lecture stratégique.

## Le moteur : collecter, structurer, lire

### 1. Cadrer le périmètre (avant toute recherche)

Fixer explicitement, et le rappeler en tête de sortie :
1. **Le secteur / la catégorie** exacte (ex : "sous-vêtements masculins D2C", pas juste
   "textile").
2. **La géographie** (mondial / US / Europe / France). Le capital se comporte très
   différemment selon les zones.
3. **La fenêtre de temps** (tout historique, ou 5 dernières années). Par défaut, tout
   trouvable avec focus sur les 5-7 dernières années (le plus représentatif du marché actuel).
4. **Les adjacences à inclure ou exclure** (ex : inclure la lingerie féminine D2C comme
   comparable, ou non). Une catégorie trop étroite donne 2 lignes ; trop large, du bruit.

Si l'un de ces 4 points est ambigu et change le résultat, poser la question à Bentho avant de
lancer (règle 8 de Bentho). Sinon, prendre le défaut ci-dessus et l'annoncer.

### 2. Collecter (recherche web fan-out)

But : trouver un maximum de rounds réels. Angles de recherche à combiner (voir
`references/sources.md` pour les requêtes et les bases à privilégier) :
1. Recherches par entreprise connue du secteur + "funding" / "raises" / "Series" / "levée de
   fonds".
2. Recherches par agrégateurs de deals (Crunchbase, PitchBook, Tracxn, Dealroom, CB Insights,
   Sifted pour l'Europe, Maddyness pour la France).
3. Recherches par presse spécialisée du secteur + presse business (TechCrunch, Business of
   Fashion pour le retail/mode, Forbes, Bloomberg, Les Echos).
4. Recherches par investisseur (quand un VC revient, chercher les autres deals de son
   portefeuille dans la catégorie).
5. Recherches par plateforme de crowdfunding (Kickstarter, Indiegogo, Ulule) si la catégorie
   est grand public et early-stage.

Quand deep-research (le harness de recherche) est disponible, l'utiliser pour la collecte
multi-sources vérifiée plutôt que de chercher à la main : ce skill fournit alors la STRUCTURE
de sortie (tableau + synthèse ci-dessous), deep-research fournit la matière.

### 3. Structurer : le tableau de rounds

Format ALWAYS identique, une ligne par round (pas par entreprise : une boîte qui a fait 3
levées = 3 lignes) :

| Entreprise | Pays | Date | Stade / Série | Montant (devise) | Valorisation | Investisseur(s) lead + notables | Source |
|---|---|---|---|---|---|---|---|

Règles de remplissage :
1. Trier par entreprise puis par date croissante (on voit la trajectoire de financement).
2. Valorisation : la mettre seulement si publiée ; sinon "n.c." (non communiquée).
3. Investisseurs : lead en premier (en gras si possible), puis 2-3 co-investisseurs notables,
   pas la liste exhaustive.
4. Source : lien cliquable. Si plusieurs sources, la plus fiable (agrégateur > presse tier 1 >
   communiqué > presse secondaire).
5. Si le total cumulé par entreprise est connu et parlant, l'ajouter en note sous le tableau.

### 4. Lire : la synthèse stratégique

Le tableau ne suffit pas : Bentho veut la lecture. Toujours conclure par une synthèse courte
et orientée décision, structurée ainsi :

1. **La catégorie attire-t-elle du capital ?** Oui / non / marginalement, et à quel point
   (nombre de deals, montant cumulé, sur quelle période).
2. **À quels stades ?** Où se concentre l'argent (beaucoup de seed mais peu de Series B = mur
   de croissance ; ou l'inverse). C'est le signal le plus utile.
3. **Montants typiques par stade.** Fourchette observée (ex : seed 0,5-2 M$, Series A 5-15 M$).
4. **Qui sont les investisseurs actifs.** Les fonds qui reviennent, les spécialistes de la
   catégorie (consumer/D2C/retail), les business angels notables.
5. **Tendances et signaux.** Marché en hausse ou en refroidissement, up/down rounds,
   faillites ou consolidations récentes, exits (rachats, IPO). Un secteur qui a beaucoup levé
   en 2021 puis plus rien peut signaler un capital refroidi, pas une opportunité.
6. **Ce que ça implique pour le projet de Bentho** (si un projet est en jeu) : est-ce
   finançable en venture, ou plutôt bootstrap / crowdfunding / dette ? En une ou deux phrases,
   sans surpromettre.

### 5. Signaler les trous

La complétude est un leurre en financement privé (beaucoup de deals non annoncés). Toujours
finir par une ligne d'honnêteté : ce qui n'a pas pu être trouvé/confirmé, les zones d'ombre,
et si un accès payant (Crunchbase Pro, PitchBook) donnerait une image plus complète. Ne jamais
présenter la carte comme exhaustive.

## Exemple de mini-synthèse (ton visé)

**Input** (secteur) : "sous-vêtements masculins D2C, mondial".
**Output** (extrait synthèse) :
"Oui, la catégorie lève, mais surtout au stade early (seed / Series A) et via des fonds
consumer/D2C généralistes, pas des spécialistes de l'underwear. Les gros montants (>50 M$)
vont à des marques à assortiment large (basics, lifestyle), pas au positionnement 'sexy'.
Signal : plusieurs levées 2019-2021, très peu depuis 2022 (capital D2C refroidi). Implication :
finançable en amorçage, mais un pur-player 'sexy masculin' devra probablement prouver la
traction en bootstrap/crowdfunding avant d'intéresser un fonds."

## Livrable client / Notion (étape distincte)

La sortie de ce skill est une analyse interne pour Bentho. Si elle doit devenir un livrable
client (page Notion, note d'investissement, deck), c'est une étape séparée : demander à Bentho
la destination (souvent Notion), passer en anglais si c'est destiné à un client, retirer toute
note interne, et confier la mise en forme au skill `proposition-commerciale` si c'est une
recommandation commerciale.
