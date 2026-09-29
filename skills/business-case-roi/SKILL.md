---
name: business-case-roi
description: >
  Construit un business case et un calcul de ROI DÉFENDABLE devant un comité de
  direction, adossé à un registre d'hypothèses où chaque chiffre porte sa source
  ou son raisonnement. Couvre la chaîne de valeur (volume, temps unitaire, coût
  chargé, taux d'erreur), les quatre familles de bénéfices, le coût total de
  possession, le payback, la fourchette conservateur/central/optimiste et
  l'analyse de sensibilité. À utiliser dès qu'il faut prouver la valeur
  économique d'un projet, d'un outil ou d'une automatisation, y compris quand la
  donnée client manque et qu'il faut assumer des hypothèses. Se déclenche sur
  "business case", "calcul de ROI", "prouver la valeur", "combien ca rapporte",
  "payback", "justifier le budget", "gains attendus", "slide ROI", "chiffrer les
  bénéfices", "TCO", "coût total", et aussi sur des formulations indirectes
  ("le client veut savoir si ca vaut le coup", "il faut convaincre le comex",
  "on doit montrer que ca s'amortit"). À utiliser MÊME si l'utilisateur ne dit
  pas le mot ROI, dès lors qu'un chiffre de gain doit tenir devant un décideur.
---

# Business case et ROI défendable

## Pourquoi ce skill existe

Un comité de direction ne juge pas la beauté d'un modèle, il cherche l'endroit
où il va casser. La question qu'il pose n'est jamais "combien" mais "d'où sort
ce chiffre". Un business case se perd donc rarement sur le calcul, il se perd
sur une hypothèse invisible que personne ne peut discuter.

D'où la règle qui gouverne tout le reste. **Aucun chiffre n'entre dans un
livrable sans sa ligne au registre d'hypothèses.** Pas un pourcentage, pas un
volume, pas un coût horaire. Si un chiffre ne peut pas porter sa source ou son
raisonnement, il ne s'écrit pas, il devient une question au client.

Cette contrainte a un effet secondaire précieux. Elle transforme les trous de
données en matière de conversation. Un modèle qui affiche ses hypothèses invite
le client à les corriger, et un client qui corrige une hypothèse s'approprie le
modèle.

## Étape 1, ouvrir le registre AVANT de calculer

Créer le registre d'hypothèses comme premier fichier du projet, jamais en
rattrapage à la fin. Un chiffre qu'on justifie après coup se justifie mal.

Format du registre, une ligne par hypothèse.

| ID | Hypothèse | Valeur | Unité | Origine | Confiance | Impact | Question au client |
|---|---|---|---|---|---|---|---|
| H1 | Volume mensuel de documents traités | 4 000 | doc/mois | Hypothèse, organisation de N salariés | Faible | Fort | Quel est le volume réel sur 12 mois, avec les pics ? |

Les colonnes qui font le travail.

1 **Origine**, trois valeurs possibles seulement. `Donnée client` quand le
client l'a fournie, avec la date et l'interlocuteur. `Source publique` avec le
lien et la date de consultation. `Hypothèse assumée` avec le raisonnement en une
phrase, jamais un chiffre nu.
2 **Confiance**, forte, moyenne ou faible. Une confiance faible sur une ligne à
fort impact est le vrai risque du dossier, elle doit remonter dans le livrable.
3 **Impact**, la variation du résultat final quand l'hypothèse bouge. Se remplit
après le calcul, en revenant sur le registre. C'est cette colonne qui désigne
les hypothèses à tester en sensibilité.
4 **Question au client**, la reformulation de l'hypothèse en question ouverte.
Ces questions alimentent directement la slide ou la section de validation.

## Étape 2, construire la chaîne de valeur avant les bénéfices

Un ROI crédible remonte toujours d'une unité de travail réelle vers l'agrégat,
jamais l'inverse. Un pourcentage de gain posé d'entrée ("30% de productivité")
n'est pas un modèle, c'est un souhait.

La chaîne minimale.

1 **Volume**, combien d'unités par période. Documents, dossiers, tickets, lignes
2 **Temps unitaire actuel**, combien de minutes par unité aujourd'hui, et par
quelle étape. Décomposer, réception, saisie, vérification, relance, validation
3 **Coût horaire chargé**, salaire brut plus charges plus coûts indirects. Ne
jamais utiliser le salaire net ni le brut seul, un comité de direction le verra
4 **Taux d'erreur et reprise**, quelle part repasse une deuxième fois, et ce que
coûte ce deuxième passage
5 **Temps unitaire cible**, et surtout **d'où vient la réduction**. Une étape
supprimée, une étape accélérée, ou une étape qui reste humaine mais mieux
outillée. C'est le point que le comité attaque en premier

Le piège le plus fréquent est là. Une automatisation ne supprime pas une étape
de bout en bout, elle en supprime une partie et en ajoute une nouvelle, la revue
de ce que la machine a produit. Compter le gain sans compter cette revue rend
tout le modèle suspect.

## Étape 3, les quatre familles de bénéfices

Les ranger séparément, parce qu'elles n'ont pas la même crédibilité et pas la
même nature comptable.

1 **Temps gagné**, la plus facile à calculer et la plus contestée. Un décideur
sait qu'une heure économisée n'est pas une heure encaissée. Il faut donc dire ce
que devient ce temps, redéploiement sur une tâche à valeur, absorption d'une
croissance de volume sans recrutement, ou réduction d'intérim et d'heures
supplémentaires. Sans cette phrase, le gain reste théorique
2 **Erreurs évitées**, coût unitaire d'une erreur multiplié par le nombre
d'erreurs évitées. Plus solide que le temps parce que chaque erreur a une trace
3 **Effets de trésorerie**, escomptes fournisseurs captés, pénalités de retard
évitées, délai de remboursement raccourci. Ce sont de vrais euros et un directeur
financier les reconnaît immédiatement
4 **Risque et conformité**, la moins chiffrable. La traiter en exposition évitée
plutôt qu'en gain, et l'assumer comme qualitative quand elle ne se chiffre pas.
Un bénéfice honnêtement qualifié de non chiffrable renforce la crédibilité des
trois autres

## Étape 4, le coût total, sans trou

Un ROI qui n'additionne que le coût de build se fait démonter en une question.
Lister au minimum.

1 Build, le projet lui-même, en jours et au taux appliqué
2 Licences et abonnements, par an, en précisant la base de facturation
3 Matériel et infrastructure, y compris ce qui existe déjà et ce qu'il faut
ajouter
4 Run, maintenance, supervision, mises à jour de modèle
5 Conduite du changement, formation, documentation, le temps des équipes
métier pendant le déploiement. C'est le poste le plus souvent oublié et le plus
souvent réel

## Étape 5, les métriques, et la rampe

Trois chiffres suffisent pour un comité.

1 **Payback**, en mois. C'est celui que tout le monde regarde en premier
2 **ROI sur horizon**, gain net divisé par le coût total, sur 12, 24 ou 36 mois.
Toujours nommer l'horizon, un ROI sans horizon ne veut rien dire
3 **Gain net cumulé**, en valeur absolue, parce qu'un pourcentage sur une petite
base ne déclenche aucune décision

**La rampe d'adoption change tout.** Un bénéfice ne démarre jamais à cent pour
cent au premier mois. Modéliser une montée en charge explicite, par exemple un
périmètre pilote puis une extension, et le dire. Un modèle qui encaisse le gain
plein dès le mois un se disqualifie tout seul.

## Étape 6, jamais un chiffre unique

Sortir systématiquement trois scénarios, conservateur, central, optimiste, en
faisant varier les deux ou trois hypothèses à fort impact identifiées au
registre. Le scénario conservateur est le plus utile des trois, c'est celui qui
prouve que le projet tient même quand les hypothèses décoivent.

Puis une **analyse de sensibilité** sur ces mêmes hypothèses. Une phrase par
hypothèse suffit, du type, si le volume tombe de moitié le payback passe de X à
Y mois. C'est ce qui montre qu'on a cherché soi-même où le modèle casse, avant
que le comité le fasse.

## Les pièges qui tuent un business case

1 Compter le temps gagné comme de la trésorerie sans dire ce que devient ce temps
2 Double compter, un gain de temps et une réduction d'erreurs qui décrivent la
même minute
3 Oublier la revue humaine du travail produit par l'automatisation
4 Ignorer la rampe d'adoption et encaisser le gain plein dès le premier mois
5 Un pourcentage de productivité posé sans chaîne de calcul derrière
6 Un ROI sans horizon, ou un payback sans coût de run
7 Des chiffres trop précis, un gain annoncé à l'euro près sur des hypothèses à
confiance faible signale qu'on n'a pas compris son propre modèle. Arrondir au
niveau de précision que les hypothèses autorisent

## Ce qu'on livre

1 Le **registre d'hypothèses** complet, en annexe ou en fichier joint. Il ne
s'enterre pas, il se montre, c'est lui qui rend le reste crédible
2 Une **slide ou section business case**, la chaîne de calcul lisible en une
lecture, du volume au gain net
3 Une **slide scénarios**, les trois cas et la sensibilité
4 Une **liste de questions au client**, tirée directement de la colonne question
du registre, priorisée par impact décroissant

Pour la mise en forme des graphiques du business case, charger le skill
`dataviz` avant d'écrire la première ligne de code d'un graphique.
