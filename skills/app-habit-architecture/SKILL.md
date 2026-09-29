---
name: app-habit-architecture
description: "Concevoir l'architecture de navigation et les boucles de retour d'une application à usage récurrent (quotidien, hebdomadaire, tous les 2-3 jours) : combien d'onglets et comment les nommer, où placer le geste central, quand interrompre l'utilisateur et quand s'abstenir, comment faire revenir sans harceler, et comment croiser la rétention avec les besoins business (conversion, upsell). Utiliser ce skill dès que Bentho travaille sur la structure d'une app, la navigation, l'expérience utilisateur d'un produit qu'on veut voir utilisé régulièrement, ou qu'il demande : 'architecture de l'app', 'les onglets', 'le parcours utilisateur', 'comment on fait revenir les gens', 'quelle navigation', 'où on met telle fonctionnalité', 'design de l'habitude', 'rétention', 'notifications', 'onboarding d'app'. Se déclenche aussi sur des formulations indirectes ('l'app est trop compliquée', 'les gens ne reviennent pas', 'on a 30 écrans', 'qu'est-ce qu'on met en page d'accueil')."
---

# Architecture d'app et design d'habitude

Ce skill sert à répondre à une question précise : **comment structurer une application pour que les gens y reviennent d'eux-mêmes, sans qu'on les harcèle, et sans sacrifier le business.**

La sortie par défaut est **dans le chat, en français**, au format de Bentho (titres `# **• TITRE**`, numérotation 1/2/3, tableaux markdown quand ça compare). Une architecture se présente toujours avec ses arbitrages visibles : ce qu'on gagne, ce qu'on perd.

## Le principe de fond

Une app à usage récurrent ne se conçoit pas comme un site. Un site répond à une intention ponctuelle (je cherche, je trouve, je pars). Une app d'habitude doit **créer** l'intention, ce qui est beaucoup plus dur, et se joue sur trois questions dans cet ordre :

1. **Quel est le geste central ?** Le seul truc que l'utilisateur fait à chaque visite. S'il y en a deux, il n'y en a aucun.
2. **Qu'est-ce qu'il reçoit en échange, immédiatement ?** Pas dans trois semaines. À la seconde où il finit le geste.
3. **Qu'est-ce qui le ramène ?** Et surtout : est-ce que ça vient de lui (pull) ou de nous (push) ?

Tout le reste, les onglets, les écrans, les fonctionnalités, découle de ces trois réponses. Concevoir la navigation avant d'avoir répondu produit systématiquement une app qui ressemble à un menu de restaurant.

## 1. Le geste central

Le geste central est ce qui définit le produit. Chez Strava c'est enregistrer une activité, chez Duolingo c'est faire une leçon, chez Oura c'est consulter son score du matin.

Critères d'un bon geste central :

1. **Court.** Sous 60 secondes. Idéalement sous 15. Le coût perçu d'ouverture doit être quasi nul, sinon l'utilisateur reporte, et reporter une fois suffit à casser la chaîne.
2. **Sans clavier si possible.** Taper est un effort disproportionné sur mobile. Des taps, des choix proposés, du vocal.
3. **Il produit quelque chose.** Un résultat visible, pas juste un enregistrement. Un état, une image, un chiffre, une phrase.
4. **Il est faisable un mauvais jour.** Si le geste demande de l'énergie ou de l'introspection, il ne survivra pas aux journées de fatigue, qui sont précisément celles où le produit servirait le plus.

Question à poser au moment de la conception : *si l'utilisateur ne faisait QUE ce geste et rien d'autre, pendant six mois, est-ce qu'il en tirerait quelque chose ?* Si la réponse est non, le geste central n'est pas le bon.

## 2. Le nombre et le nom des onglets

**Trois à cinq onglets.** En dessous de trois, on cache le produit dans des menus. Au-dessus de cinq, la barre devient illisible sur mobile et chaque onglet supplémentaire dilue les autres.

Règles de nommage :

1. **Nommer par ce que l'utilisateur y FAIT ou y TROUVE, pas par la catégorie métier.** "Aujourd'hui" plutôt que "Dashboard". "Mon chemin" plutôt que "Historique". Les noms abstraits ("Espace", "Hub", "Parcours") ne disent rien et personne ne clique dessus.
2. **Un onglet doit être plein.** Si un onglet contient une seule fonctionnalité qui sert une fois par mois, ce n'est pas un onglet, c'est une page interne.
3. **L'onglet 1 est la page d'ouverture.** C'est là que le geste central vit. Toujours.

Méthode quand on part d'une app existante qui a trop d'écrans : ne pas partir des écrans, partir des **moments d'usage** (quand l'utilisateur ouvre l'app, il vient pour quoi ?). Chaque moment devient un onglet candidat, puis on range les écrans dedans. Les écrans qui ne rentrent nulle part sont des candidats à la suppression, pas à la création d'un sixième onglet.

## 3. Habitude ou rituel

Distinction qui change le design, et qui est contre-intuitive.

**L'habitude** est automatique et déclenchée par un signal extérieur. On la construit avec de la répétition et du renforcement (streaks, badges, rappels). Elle est fragile : une rupture et elle s'effondre, parce que rien à l'intérieur de la personne ne la soutient.

**Le rituel** est choisi et porte du sens. Il crée un moment plutôt qu'une tâche (le café du matin, ce n'est pas boire de la caféine, c'est le bruit de la machine et les cinq minutes qui vont avec). Il résiste aux ruptures parce que la personne y revient par envie, pas par crainte de perdre quelque chose.

**Implication de conception :** privilégier le rituel dès qu'on touche à des sujets de fond (santé mentale, développement personnel, relation à soi). L'habitude par gamification marche bien sur l'acquisition de compétence (une langue, un mouvement sportif), moins bien sur le changement intérieur, où la mécanique de compétition finit par produire l'inverse de l'effet voulu.

Traduction concrète : soigner l'ambiance du moment (le son, le rythme, la respiration de l'écran, une phrase d'ouverture), plutôt qu'empiler des compteurs.

## 4. Pull plutôt que push

Le push (notification, badge, relance) fait revenir une fois et coûte cher : il use le capital d'attention, il génère de la désinstallation, et il crée une dépendance du produit à sa propre insistance.

Le pull, c'est quand l'utilisateur revient parce que **quelque chose l'attend qui a de la valeur pour lui**. Les leviers de pull, par ordre de puissance :

1. **Quelque chose a changé pendant son absence** et le concerne (une réponse, un message d'un humain, une évolution de son état)
2. **Il a laissé quelque chose en cours** qu'il veut finir
3. **Il veut voir sa progression** parce qu'elle le valorise
4. **Il veut montrer quelque chose** à quelqu'un (le partage est un moteur de retour, pas seulement d'acquisition)

Règle d'arbitrage : le push est acceptable quand il transporte une information que l'utilisateur ne pouvait pas deviner et qu'il aurait voulu connaître. Il est nuisible quand il dit seulement "reviens".

## 5. Quand interrompre, et quand s'abstenir

Une modale à l'ouverture est un péage. Elle transforme l'ouverture de l'app en corvée, et le réflexe qui s'installe n'est pas l'usage, c'est la fermeture rapide.

Grille de décision :

| Situation | Interrompre ? |
|---|---|
| L'utilisateur ouvre l'app pour la première fois de la journée et le geste central prend 15 secondes | Oui, mais fermable en un geste, et sans réapparition dans la journée |
| L'utilisateur ouvre l'app une deuxième fois | Non, jamais |
| Un rendez-vous récurrent (bilan hebdomadaire, revue mensuelle) | Non imposé. L'utilisateur choisit son créneau à l'onboarding, et on lui présente une carte, pas une modale |
| Une nouveauté produit, une offre, un upsell | Jamais à l'ouverture. Après un moment de satisfaction (fin de geste, résultat obtenu) |
| Une information critique (compte suspendu, données perdues) | Oui |

Principe général : **interrompre au moment de la satisfaction, jamais au moment de l'intention.** Quelqu'un qui vient d'obtenir son résultat est disponible et bien disposé. Quelqu'un qui ouvre l'app a une intention en tête et toute interruption la contrarie.

## 6. Les moments de déclenchement

Un produit récurrent a besoin de **rendez-vous**, mais ils doivent être choisis par l'utilisateur, pas imposés par le produit. Un dimanche midi décidé unilatéralement tombera au milieu d'un déjeuner familial pour la moitié des gens.

Bonne pratique : à l'onboarding, faire choisir le moment ("plutôt le matin ou le soir ?", "quel jour tu fais le point ?"). Ça coûte une question, ça double la pertinence de tous les rappels futurs, et surtout ça transforme le rappel en engagement pris par l'utilisateur avec lui-même.

## 7. Les modèles de référence et leurs pièges

| Modèle | Ce qui marche | Le piège documenté |
|---|---|---|
| **Duolingo** | Le geste ultra court, la leçon jouable en 2 minutes, la progression lisible | Le streak : les utilisateurs à 6 mois de série qui ratent un jour abandonnent massivement. Les "streak freezes" ont été ajoutés pour ça, et le problème de fond demeure, on a entraîné les gens à optimiser la série plutôt qu'à apprendre |
| **Strava** | Le social logiciel gratuit (segments, comparaison, mur), qui scale sans coût humain et fait la viralité | L'app ne crée pas la pratique, elle l'accompagne. Reprendre Strava comme modèle suppose que l'activité existe déjà en dehors de l'app |
| **Oura** | Le score du matin, consultable en 5 secondes, qui donne envie d'ouvrir | L'obsession du score : documenté que l'optimisation d'un score de sommeil peut dégrader le sommeil. Un score qui juge produit de l'anxiété chez les profils les plus impliqués |
| **Headspace** | Une communauté d'événements préexistante, prolongée par l'app | La couche humaine n'est arrivée que dix ans plus tard (fusion avec Ginger), au prix fort |
| **Apple Santé, apps bancaires** | L'état actuel visible sans action, la donnée qui parle d'elle-même | Consultation passive, faible engagement profond |

**Le score, à manier avec précaution.** Un chiffre qui classe (0 à 100, "tu es en dessous") installe une compétition avec soi-même qui devient toxique sur les sujets intimes. L'alternative : un **état** ou un **mode** plutôt qu'une note. "Tu es en mode récupération" informe et n'humilie pas. C'est aussi plus partageable, parce que personne ne partage un mauvais score, alors que tout le monde partage un état qui le décrit bien.

## 8. Croiser l'utilisateur et le business

Une architecture qui ne sert que l'utilisateur produit un beau produit qui ne gagne pas d'argent. Une architecture qui ne sert que le business produit un tunnel que personne n'utilise. Le croisement se fait en posant, pour chaque zone de l'app, les deux colonnes :

| Zone | Ce que l'utilisateur y gagne | Ce que le business y gagne |
|---|---|---|

Trois règles d'arbitrage :

1. **Le geste central ne se monétise jamais.** C'est le moteur de rétention, le mettre derrière un paywall tue l'usage et donc la valeur du produit.
2. **L'upsell se place après une réussite,** jamais avant une action. Le meilleur moment pour proposer d'aller plus loin est la seconde qui suit un résultat obtenu.
3. **Ce qui coûte de l'humain se paie, ce qui est logiciel peut être gratuit.** C'est une ligne de partage lisible pour l'utilisateur (il comprend qu'un coach coûte) et saine économiquement (le gratuit reste à coût marginal nul).

## 9. Livrer une architecture

Une proposition d'architecture se présente ainsi, dans cet ordre :

1. **Le geste central**, en une phrase
2. **Les onglets**, en tableau : nom, ce qu'on y fait, ce qui vient de l'existant
3. **Le parcours d'une semaine type** : ce que l'utilisateur vit à J0, J1, J3, J7
4. **Les moments d'interruption** assumés, avec leur justification
5. **Ce qu'on a écarté** et pourquoi

Toujours proposer **deux architectures alternatives** avec leurs avantages et inconvénients respectifs, plutôt qu'une seule "bonne" réponse. Une architecture est un arbitrage, et l'arbitrage appartient à celui qui porte le produit.

## Les erreurs qui reviennent

1. **L'app-menu.** Chaque fonctionnalité a son entrée, l'utilisateur arrive et doit choisir. Il ne choisit pas, il repart. Symptôme : plus de cinq onglets, ou un onglet "Plus".
2. **Le geste central qui n'en est pas un.** Deux ou trois gestes proposés à égalité, donc aucune habitude possible.
3. **La récompense différée.** L'utilisateur doit revenir dix fois avant de voir un intérêt. Personne ne revient dix fois par foi.
4. **Le journal comme moteur de retour.** Écrire librement est un usage de niche qui retient ceux qui reviennent déjà, mais ne fait revenir personne. Un journal est une bonne fonctionnalité, jamais un bon onglet 1.
5. **La modale d'ouverture non fermable.** Elle produit un réflexe d'évitement mesurable dès la deuxième semaine.
6. **Confondre onboarding et tutoriel.** L'onboarding sert à capter ce dont le produit a besoin pour être pertinent (un objectif, un créneau, un contexte), pas à expliquer les boutons.
