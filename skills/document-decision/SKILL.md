---
name: document-decision
description: >
  Construit un document de DECISION interne pour une equipe (associes, partenaires), sous
  forme de page Notion, en mode EXPLORATION (rien de valide ni tranche). Presente plusieurs
  options ou strategies en parallele, les compare dans un tableau a referentiel commun, et se
  termine par les questions a trancher ensemble. A utiliser quand Bentho veut preparer un
  document d'appel, presenter des options ou strategies a une equipe pour decider ensemble,
  comparer plusieurs approches, ou aider une decision collective. Se declenche sur "doc
  d'appel", "document de decision", "presenter les options a l'equipe", "presenter aux
  associes", "comparer les strategies", "on presente ca a X pour decider".
---

# Document de decision (presentation d'options a une equipe)

Ce skill produit une page Notion INTERNE, destinee a une equipe (associes, partenaires) pour DECIDER ENSEMBLE. C'est different du skill proposition-commerciale, qui vise a convaincre un CLIENT et a vendre. Ici on n'impose rien, on eclaire un choix.

## Perimetre

- Public = l'equipe interne (associes, cofondateurs, partenaires). Ton collaboratif et transparent.
- Objectif = donner a chacun de quoi decider, pas pousser une direction unique.
- Mode = EXPLORATION. RIEN n'est valide, tranche ni decide tant que l'equipe ne l'a pas acte. Ne JAMAIS ecrire "tranche", "valide" ou "decide" pour un choix non acte. Utiliser "propose", "privilegie", "a trancher".

## Regles de contenu (non negociables)

1. Toute comparaison est un TABLEAU, avec un REFERENTIEL COMMUN, memes colonnes et memes criteres pour toutes les options comparees.
2. Cellules de tableau = des VALEURS (un chiffre, 0, n.a., un mot precis), jamais de prose ni de phrases. Fragments courts. Une info qui a sa place dans une colonne va DANS la colonne (exemple, la procedure d'acces va dans la colonne prerequis, pas en commentaire a cote).
3. Chiffres REELS et sources, jamais inventes. Si un chiffre est inconnu, ecrire "n.c." et ne pas deviner. Chercher activement les vrais montants avant d'ecrire.
4. Precision des mots. Deux choses identiques prennent le MEME mot. Signaler explicitement ses propres imprecisions ("dans cette colonne j'ai mis X, ce n'est pas exactement ca, dis-moi si ca va").
5. Zero jargon non explique. Ecrire comme pour quelqu'un qui ne connait rien au sujet, definir chaque terme technique en une phrase simple.
6. Pour chaque option, montrer honnetement le pour ET le contre, sans favoriser en douce.

## Structure type (a adapter)

1. Objectif et contexte : pourquoi ce document, le but final, l'etat des lieux.
2. Les options en parallele, une couleur par option : Option A, Option B, Option C. Pour chacune, ce que c'est et ce que ca implique.
3. La comparaison : un tableau a referentiel commun, criteres en colonnes, options en lignes, avec avantages, inconvenients, couts reels et temps.
4. Notre lecture (facultatif) : ce qui semble le plus efficace et pourquoi, formule comme un avis, pas comme une decision.
5. Les questions a trancher ensemble, a la FIN : les decisions que l'equipe doit prendre, en questions ouvertes.
6. Prochaines etapes : ce qui se passe apres la decision.

## Regles de mise en forme (Notion)

Suivre la regle couleurs de la memoire feedback-couleurs-entetes-notion (source de verite) : titre de section = texte PLUS fond de la meme couleur ; sous-titres = texte colore SEUL, sans fond, de la meme couleur que la section ; deux sections voisines jamais la meme couleur ; ROUGE jamais sur un titre ni un sous-titre (toujours une autre couleur), tolere seulement sur un mot ponctuel. Syntaxe fond = suffixe `_bg`, verifier par fetch apres ecriture. Jamais de tiret long.

## Processus

1. Charger le contexte (SESSION_LOG, notes, docs, transcripts d'appel).
2. Confirmer avec Bentho : l'emplacement Notion, la liste des options a presenter, la langue.
3. Rediger la page, et chercher les vrais chiffres pour chaque tableau.
4. AUTO-RELECTURE de coherence avant livraison : chaque cellule correspond a son en-tete de colonne, les mots sont coherents, les reponses repondent aux questions, aucune valeur inventee, referentiel commun respecte.
5. Lancer l'agent coherence-reviewer avant de livrer.
6. Creer la page via notion-create-pages, donner le lien cliquable a Bentho.
7. Mettre a jour le SESSION_LOG.

## Faire evoluer ce skill

A la fin de chaque document livre, revenir ici et integrer ce qu'on a appris, une section utile, une formulation qui marche, un piege a eviter.
