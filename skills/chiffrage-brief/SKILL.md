---
name: chiffrage-brief
description: >
  Transforme un brief de projet client en chiffrage StudioMakers. Décompose le brief
  en lots puis en tâches (bottom-up), estime le temps par tâche, applique le tarif régie
  (450 euros/jour), liste les coûts externes et le hors-scope, propose une maintenance
  récurrente, et rend un chiffrage INTERNE (à Bentho, en français dans le chat) que Bentho
  valide avant toute mise en forme client. Deux modes de sortie sur le même travail
  d'analyse : "devis précis" (chiffre ferme par tâche) ou "fourchette" (estimation basse/haute).
  À utiliser dès que Bentho veut savoir combien coûterait un projet, chiffrer un brief,
  estimer un budget, faire un devis interne ou un ordre de grandeur. Se déclenche sur
  "chiffre-moi ce projet", "combien ça coûterait", "fais un devis", "estime ce brief",
  "donne-moi une fourchette", "un ordre de grandeur pour X". Une fois le chiffrage validé
  par Bentho, le relais vers le client se fait avec le skill proposition-commerciale.
---

# Chiffrage d'un brief (StudioMakers)

Ce skill produit un **chiffrage interne**, destiné à Bentho, dans le chat, en français.
Ce n'est PAS un livrable client. La version client (page Notion) se fait ensuite,
séparément, avec le skill `proposition-commerciale`.

## Garde-fou de périmètre

1. Sortie de ce skill = chiffrage interne pour Bentho (chat, français, format de réponse
   habituel de Bentho : titres `# **• TITRE**`, numérotation 1/2/3, etc.).
2. Ce chiffrage peut contenir des notes internes (hypothèses, incertitudes, risques,
   marge). C'est l'inverse d'un livrable client.
3. Le passage au client (page Notion orientée valeur, sans notes internes) est une étape
   distincte, gérée par `proposition-commerciale`. Ne jamais mélanger les deux.

## Le moteur unique : décomposition bottom-up

Quel que soit le mode de sortie, le travail d'analyse est le même : on décompose toujours.

1. **Lire le brief à fond.** Si un projet existe (repo, `SESSION_LOG.md`, `CLAUDE.md`,
   pages Notion du call), les charger d'abord : le cadrage répond souvent à des questions
   avant de les poser.
2. **Découper en lots** (grandes phases). Découpage type d'un projet web StudioMakers,
   à adapter : cadrage / design (UX + UI), intégration front, back-end et base de données,
   authentification, intégrations tierces (Stripe, Resend, Supabase, API Claude, Weglot...),
   contenu et SEO, recette et corrections, mise en production, documentation et passation.
3. **Découper chaque lot en tâches concrètes.** Une tâche = quelque chose d'estimable en
   jours ou demi-journées. Nommer la tâche par ce qu'elle produit, pas par un mot vague.
4. **Estimer chaque tâche en jours** (granularité 0,5 jour). C'est ici que se joue la
   précision : mieux vaut 15 petites tâches estimées que 4 gros blocs au doigt mouillé.
5. **Appliquer le tarif régie : 450 euros / jour** (mémoire `studiomakers-pricing-standard`,
   ne jamais reposer la question). Coût d'une tâche = jours x 450.
6. **Additionner par lot, puis total.**

## Les deux modes de sortie

Choisir le mode selon le langage de Bentho. En cas de doute, lui demander lequel.

| Mode | Déclencheurs | Sortie |
| --- | --- | --- |
| **1. Devis précis** | "devis", "chiffrage précis", "combien exactement", "budget ferme" | Un chiffre net par tâche, total ferme en euros. |
| **2. Fourchette** | "approximation", "fourchette", "ordre de grandeur", "à peu près", "rough" | Chaque tâche estimée en basse/haute, total présenté en fourchette (jours et euros). |

Règle sur l'incertitude selon le mode :
1. **Mode devis précis** : chiffre sec par tâche. Si le brief est flou sur un point, ne pas
   gonfler en douce ; poser la question de cadrage à Bentho, ou isoler le point en ligne
   "à préciser" plutôt que d'inventer un buffer caché.
2. **Mode fourchette** : l'incertitude est déjà portée par l'écart basse/haute. Plus le
   brief est flou, plus l'écart est large. Pas de buffer séparé, la fourchette EST le buffer.

Dans les deux cas, à la fin, **signaler explicitement les hypothèses et les zones de flou**
qui pourraient faire bouger le chiffre. C'est une note interne, elle a sa place ici.

## Règles de chiffrage non négociables

1. **Tarif 450 euros/jour**, temps x taux. Ne jamais reposer la question du modèle ni du taux.
2. **Maintenance récurrente** : toujours proposer un contrat de maintenance récurrent en plus
   du build (comme d'habitude). Le chiffrer à part (mensuel ou annuel).
3. **Coûts externes OBLIGATOIRES.** Lister tous les coûts externes à la charge du client sur
   la durée, chacun avec un ordre de grandeur chiffré : hébergement (Vercel), Supabase, API
   Claude (à l'usage), Resend (emails), nom de domaine, frais Stripe (environ 1,5 % + 0,25 €
   par transaction), comptes App Store (environ 99 €/an) et Google Play (25 € une fois),
   Weglot, budget média. Chercher les vrais ordres de grandeur, préciser que ça varie selon
   fournisseur et volume. Ces coûts ne sont PAS dans le total StudioMakers, ils sont à part.
4. **Hors-scope OBLIGATOIRE.** Définir clairement ce qui n'est pas inclus (production des
   contenus, rédaction, visuels/média, budget publicitaire, choix et coût de l'hébergeur,
   modération, animation...), pour éviter les malentendus au moment du devis client.
5. **Rien perdu (mémoire `feedback-devis-rien-perdre`).** Ne jamais évoquer un poste puis le
   laisser tomber. Si une tâche sort du périmètre, la réaffecter ou la lister explicitement
   en hors-scope. Chaque élément du brief doit se retrouver quelque part.

## Format du chiffrage interne (chat, à Bentho)

Suivre les règles de réponse habituelles de Bentho. Structure recommandée :

1. **Hypothèses de départ** : ce que j'ai compris du brief, ce que j'ai supposé (à valider).
2. **Chiffrage par lot** : un tableau par lot ou un grand tableau (Lot, Tâche, Jours, Coût).
   En mode fourchette, colonnes Jours bas / Jours haut / Coût bas / Coût haut.
3. **Total build** : total jours et total euros (ou fourchette).
4. **Maintenance récurrente** : proposition chiffrée à part.
5. **Coûts externes** : tableau avec ordre de grandeur chiffré par ligne (à la charge du client).
6. **Hors-scope** : liste claire de ce qui n'est pas inclus.
7. **Zones de flou et risques** : ce qui pourrait faire bouger le chiffre, questions ouvertes.

Terminer par le recap couleur habituel si pertinent, et proposer (sous forme de question,
jamais d'office) de passer à la version client Notion via `proposition-commerciale`.

## Passage de relais vers le client

Une fois le chiffrage validé par Bentho, la mise en forme client (page Notion, en-têtes
colorés, ton orienté valeur, sans notes internes) se fait avec le skill
`proposition-commerciale` (mode A, proposition complète chiffrée). Ne jamais publier le
chiffrage interne tel quel côté client : il faut le retraduire en bénéfices via l'autre skill.

## Faire évoluer ce skill

Durcir au fil des projets. À chaque chiffrage, si un lot type manque, si une estimation
s'est révélée systématiquement fausse dans un sens, ou si un coût externe a changé de prix,
revenir ici et l'intégrer. But : que la décomposition et les ordres de grandeur deviennent
de plus en plus justes avec l'expérience réelle des projets StudioMakers.
