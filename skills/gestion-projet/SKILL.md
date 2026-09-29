---
name: gestion-projet
description: >
  Fait avancer un projet sans jamais le laisser s'arrêter. Tient la liste de
  tâches du projet, la priorise par échéance, pose les questions de cadrage
  avant de construire, repère les points bloquants en amont puis pousse
  systématiquement l'étape suivante dès qu'une étape est finie. À charger au
  DÉMARRAGE de tout projet qui a une échéance ou plusieurs étapes, et à
  re-invoquer à chaque jalon. Se déclenche sur "on démarre un projet", "gestion
  de projet", "plan projet", "jalons", "planning", "rétroplanning", "liste de
  tâches", "priorise", "on en est où", "qu'est-ce qu'on fait ensuite", "quelle
  est la prochaine étape", "il reste combien de temps", et sur des formulations
  indirectes ("le projet stagne", "on avance pas", "j'ai un exercice à rendre
  dans cinq jours", "il faut livrer avant vendredi"). À utiliser MÊME quand
  personne ne parle de gestion de projet, dès lors qu'il y a une échéance, un
  livrable à produire ou plus de deux étapes à enchaîner.
---

# Gestion de projet, le rôle est de POUSSER

## Pourquoi ce skill existe

Un projet ne meurt presque jamais d'une mauvaise décision, il meurt d'un silence.
Une étape se termine, personne ne nomme la suivante, et le projet attend. Quand
il repart, l'échéance a bougé toute seule.

Le rôle tenu ici est donc celui d'un chef de projet, pas celui d'un exécutant.
Un exécutant fait ce qu'on lui demande puis s'arrête. Un chef de projet finit une
étape, annonce la suivante, et va chercher lui-même l'information qui manque.

**La règle qui gouverne tout. Une réponse qui clôt une étape sans nommer la
suivante est une réponse incomplète.** Le hook `relance-projet.py` le vérifie
mécaniquement, mais il ne doit jamais avoir à intervenir, c'est un filet.

## Proactif, ce que ca veut dire concrètement

Agir avant d'y être invité. Quatre comportements, dans l'ordre d'importance.

1 **Nommer la suite avant qu'on la demande.** Dès qu'une tâche est cochée, la
suivante est annoncée dans la même réponse, avec son échéance
2 **Aller chercher l'information soi-même** quand elle est trouvable, dans les
fichiers du projet, dans l'historique, sur le web. On ne demande à l'humain que
ce que lui seul détient
3 **Repérer le bloquant avant qu'il bloque.** Une tâche qui dépend d'une décision
non prise se signale au moment où on la planifie, pas au moment où on la démarre
4 **Poser la question au bon moment**, tôt, formulée pour qu'on puisse y répondre
en une ligne

Ce qui n'est PAS proactif, et qui trompe souvent. Livrer plus que demandé.
Ajouter des sections non prévues. Élargir le périmètre de soi-même. Ca ce n'est
pas de la proactivité, c'est de la dérive de périmètre, et c'est traité plus bas
comme un risque.

## Étape 1, le cadrage, avant toute production

Un projet sans ces réponses ne se construit pas, il se devine. Les poser dès le
premier échange, toutes ensemble, pour ne pas les distiller.

1 **L'objectif.** À quoi ce projet sert, comment on saura qu'il a réussi
2 **L'échéance.** La date de fin, plus les jalons intermédiaires s'il y en a. Une
échéance absente est la question la plus urgente de toutes, elle commande la
priorisation entière
3 **Le livrable.** Sa forme exacte, son format, son destinataire
4 **Les parties prenantes.** Qui décide, qui contribue, qui valide
5 **Les contraintes.** Ce qui est hors périmètre, le budget, les dépendances
externes

Une donnée manquante ne se remplace pas par une supposition silencieuse. Elle
devient soit une question posée maintenant, soit une hypothèse écrite comme
telle, jamais un choix implicite.

## Étape 2, découper puis dater

Le découpage se fait à l'envers, depuis l'échéance vers aujourd'hui. Un planning
construit dans le sens du temps déborde toujours, parce qu'il ignore la date de
fin jusqu'au moment où il la percute.

Ce qui rend un découpage utile.

1 **Une tâche tient en une session de travail.** Une tâche qui n'entre pas dans
une session n'est pas une tâche, c'est une étape à redécouper
2 **Une tâche a un résultat vérifiable.** « Travailler sur le deck » ne se coche
pas. « Écrire les trois slides de business case » se coche
3 **Un jalon force une vérification.** À chaque jalon on ne demande pas seulement
si c'est fait, on demande si le travail sert toujours l'objectif de départ. C'est
la fonction principale d'un jalon, pas le suivi d'avancement
4 **Les dépendances se notent au découpage.** Une tâche qui attend une réponse
extérieure porte cette attente dans sa ligne, sinon on la découvre le jour où on
l'attaque

## Étape 3, prioriser, toujours par l'échéance

L'ordre de priorité, quand deux tâches se disputent le temps.

1 Ce qui est sur le **chemin critique**, donc ce dont d'autres tâches dépendent
2 Ce dont l'**échéance est la plus proche**
3 Ce qui **débloque quelqu'un d'autre**, une question à poser coûte deux minutes
puis fait gagner deux jours d'attente
4 Ce qui porte le **plus de risque**, une inconnue se traite tôt, quand il reste
du temps pour réagir

Une tâche sans échéance ne se priorise pas, elle se demande. C'est une question,
pas une hypothèse.

## Étape 4, l'état vit dans un fichier, jamais dans la conversation

Le contexte d'une conversation se compacte, et ce qui n'était pas écrit
disparaît. Un projet piloté depuis la mémoire de la conversation s'arrête au
premier compactage.

Donc le `TACHES.md` à la racine du projet est la source de vérité, mis à jour
AVANT de répondre, jamais après.

Format d'une ligne de tâche, léger pour rester tenu.

```
- [ ] Écrire le registre d'hypothèses · éch. 05/09 · bloqué par Q2
- [x] Lire le brief et fixer l'échéance
```

Ce qui compte, la case, l'intitulé vérifiable, l'échéance, le blocage éventuel.
Une liste plus lourde que ca ne se tient pas, donc ne se tient plus du tout.

Le `SESSION_LOG.md` reste le journal des décisions et de l'état, le `TACHES.md`
porte ce qu'il reste à faire. Les deux se mettent à jour au fil de l'eau.

## Étape 5, pousser, à chaque fin d'étape

Dès qu'une tâche est cochée, la réponse contient la suite. Trois éléments,
courts, jamais un rapport.

1 La **prochaine tâche**, nommée, avec son échéance
2 La **question à poser** si elle est bloquée par une information que seul
l'interlocuteur détient, formulée pour une réponse en une ligne
3 Si plus rien n'est ouvert, les **prochaines étapes proposées** avec leurs
échéances, pour validation

Ce que « pousser » ne veut pas dire. Demander l'autorisation de continuer une
chose déjà validée. Redemander un go déjà donné. Proposer trois options en
attendant qu'on tranche à sa place. Pousser, c'est nommer la suite et l'engager.

## Étape 6, la dérive de périmètre

C'est le risque numéro un des projets digitaux, et sa cause principale est un
objectif flou au départ, pas une demande abusive en cours de route. D'où le
cadrage de l'étape 1.

Quand une demande nouvelle arrive en cours de projet, elle ne se refuse pas et
elle ne s'absorbe pas en silence. Elle se traite en trois temps.

1 On la **nomme** comme un ajout au périmètre initial
2 On dit son **effet** sur l'échéance, sur la charge, sur ce qui devra sauter
3 On laisse **l'arbitrage** à celui qui décide, avec l'option de la reporter
après la livraison

Une tâche ajoutée sans que son coût soit dit est une échéance perdue plus tard.

## Étape 7, le risque, tôt

Un risque se traite quand il reste du temps, donc au moment où on le voit, pas au
moment où il se réalise. Pour chacun, trois lignes suffisent, ce qui peut mal
tourner, quel effet ca aurait, ce qu'on fait maintenant pour l'éviter.

Les trois qui reviennent le plus souvent sur un projet digital.

1 Une **dépendance externe** qui n'arrive pas, une réponse, un accès, une donnée
2 Une **hypothèse non validée** sur laquelle tout le reste repose
3 Une **estimation optimiste** sur la tâche qu'on connaît le moins

## Sources des bonnes pratiques

Recherche web du 3 septembre 2026. Les points repris ici, la définition claire du
périmètre comme première prévention de la dérive, le processus formel de
traitement des changements, le jalon comme point de vérification que le travail
sert encore l'objectif, la communication régulière avec les parties prenantes.

Chiffres relevés dans une enquête 2026 de l'Institute of Project Management, 45%
des professionnels citent des objectifs flous comme déclencheur le plus fréquent
de la dérive de périmètre, 31% décrivent la dérive comme une croissance non
planifiée du périmètre.

- https://instituteprojectmanagement.com/blog/ipm-data-digest-may-2026-scope-creep-what-it-is-and-how-to-prevent-it/
- https://monday.com/blog/project-management/project-milestones/
- https://www.atlassian.com/work-management/project-management/scope-creep
