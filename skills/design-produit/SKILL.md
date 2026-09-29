---
name: design-produit
description: Base de règles d'un designer produit senior pour Benjamin/StudioMakers, mobile d'abord puis web. Chaque règle porte sa source (Apple Human Interface Guidelines, Material Design, Nielsen Norman Group, Refactoring UI, WCAG 2.2, Laws of UX). Contient les principes (hiérarchie, proximité, alignement, rythme vertical, échelles d'espacement et de typographie, contraste, cibles tactiles, zones sûres), les six gabarits d'écran mobile avec leur construction exacte, la liste de ce qu'un senior ne fait jamais, le design system minimal, la mécanique de dérogation (DESIGN-DEROGATIONS.md) et la checklist de revue. À charger AVANT de dessiner, coder ou juger un écran, une page, un composant ou une maquette. Se déclenche sur "maquette", "écran", "design", "UI", "mise en page", "espacement", "équilibre", "notification", "pop-up", "onboarding", "composant", "design system", "refonte visuelle", "réagencer une page". Se combine avec page-cro pour les pages de conversion et se fait contrôler par l'agent designer avant livraison.
---

# Design produit, base de règles

Version 2, 17 septembre 2026. La version 1 est archivée dans `SKILL-v1.md`, dans ce même dossier.

Ce skill dit COMMENT dessiner. L'agent `designer` dit SI c'est bien dessiné et conseille. Les deux vont ensemble sur tout livrable visuel.

## 0. Comment lire ce document

1. Chaque règle a un identifiant (P1, G2, X3...) pour être citée dans une revue
2. Chaque règle porte sa source entre crochets, par exemple [HIG-LAY]. La table des sources, avec les URL, est en section 8
3. Une règle sans source officielle porte la mention « pratique courante, non sourcée ». Elle vaut moins qu'une règle sourcée et se discute plus facilement
4. Ordre de priorité quand deux règles se contredisent : dérogation validée par Bentho, puis règle sourcée d'accessibilité (WCAG, cibles tactiles), puis règle sourcée de plateforme, puis pratique courante
5. Unités. Le pt (point) est l'unité logique d'iOS, le dp (density-independent pixel) celle d'Android, le px CSS celle du web. Sur une maquette mobile à 1x, 1 pt = 1 dp = 1 px CSS

## 1. Ce que veut dire « équilibré », définition validée

Bentho veut trois choses cumulées : **équilibré ET harmonieux ET conforme aux bonnes pratiques**.

1. **L'équilibre est une question de poids visuel, pas de répartition de l'espace.** Nielsen Norman Group le définit comme la distribution du poids visuel autour d'un axe, symétrique, asymétrique ou radiale. Il ne s'agit jamais d'étaler les blocs pour occuper toute la hauteur [NNG-PRINC]
2. **On n'est pas obligé de remplir l'écran.** Chaque élément prend la place dont il a besoin, l'espace libre restant va en bas de l'écran [RUI, chapitre « You don't have to fill the whole screen »]
3. **L'harmonie vient de la régularité.** Mêmes espacements entre blocs de même niveau, mêmes composants pour la même fonction, même position du titre d'un écran à l'autre [RUI, chapitre « Establish a spacing and sizing system »] [LUX-SIM]
4. **La lecture commence en haut.** Les personnes lisent de haut en bas et du début vers la fin de ligne, donc le contenu important va en haut [HIG-LAY]. 57 % du temps de lecture se passe dans le premier écran, 74 % dans les deux premiers [NNG-SCROLL]
5. Conséquence directe : **la plupart des écrans sont alignés en haut** (flux de lecture). **Seuls les écrans de focus sont centrés** verticalement. **Le titre est toujours en haut**

L'ancienne interprétation, « répartir les blocs sur toute la hauteur par un helper automatique », est abandonnée. Elle a produit les défauts listés en X1 à X5.

## 2. Principes (A)

### 2.1 Hiérarchie

- **P1. Ordonner par importance.** Le plus important en haut et en début de ligne [HIG-LAY] [HIG-WRIT]
- **P2. Un point d'entrée visuel par écran.** L'élément le plus important est le plus gros ; deux gros éléments au maximum [NNG-HIER]
- **P3. Trois tailles de texte au maximum** sur un écran simple (petit, moyen, grand) [NNG-HIER]
- **P4. Taille, graisse et couleur servent la hiérarchie**, on les ajuste selon le besoin [HIG-TYPO]. Mettre en retrait le secondaire plutôt que grossir le principal [RUI, chapitre « Emphasize by de-emphasizing »]. L'ancienne règle « ne jamais cumuler taille, gras et couleur » n'a pas de source : elle devient une pratique courante, non sourcée, à appliquer avec souplesse
- **P5. Tester la hiérarchie en plissant les yeux** (ou en floutant la capture) : l'ordre d'importance doit rester lisible [NNG-HIER]
- **P6. Limiter les contrôles à l'écran** et rendre le secondaire accessible en une interaction [HIG-IOS]. Divulgation progressive [HIG-LAY]
- **P7. Moins de choix, décision plus rapide** (loi de Hick) : découper une tâche complexe en étapes, mettre en avant l'option recommandée [LUX-HICK]

### 2.2 Proximité et regroupement

- **P8. Ce qui est proche est perçu comme lié** [LUX-PROX] [NNG-PROX]
- **P9. Espace DANS un groupe plus petit que l'espace ENTRE groupes.** Un espacement ambigu est un défaut fonctionnel, pas seulement esthétique [NNG-PROX] [RUI, chapitre « Avoid ambiguous spacing »]
- **P10. Le libellé et l'aide collent à leur champ ou à leur question**, avec un espacement minimal [NNG-PROX] [NNG-FORMSPACE]
- **P11. L'action se place près de l'objet sur lequel elle agit** [NNG-CLOSE]
- **P12. Une zone délimitée (fond, bordure) crée un groupe** [LUX-REGION]. À utiliser quand la proximité ne suffit pas
- **P13. Même apparence, même fonction** : les éléments qui se ressemblent sont perçus comme liés [LUX-SIM]
- **P14. Ne pas coller deux éléments sans rapport**, l'un camoufle l'autre [NNG-PROX]

### 2.3 Alignement

- **P15. Aligner pour faciliter le balayage**, indenter pour signifier la subordination [HIG-LAY]
- **P16. Un seul bord d'alignement gauche par écran** pour le texte courant et les titres. Texte long jamais centré. Pratique courante, non sourcée pour la partie « jamais centré » ; l'alignement lui-même est sourcé [HIG-LAY]
- **P17. Aucun décalage de 1 ou 2 pixels.** Pratique courante, non sourcée

### 2.4 Rythme vertical et espacement

- **P18. Une seule échelle d'espacement, base 4 et 8.** Les mesures s'alignent sur 8 dp, les petits éléments sur 4 dp [M2-SPACE]. Échelle StudioMakers : **4, 8, 12, 16, 24, 32, 40, 48, 64**. Aucune valeur hors échelle
- **P19. Les écarts de l'échelle grandissent avec la taille**, deux valeurs voisines ne doivent pas être trop proches pour rester distinguables [RUI, chapitre « Establish a spacing and sizing system »]
- **P20. Niveaux d'espacement**, pratique courante, non sourcée, dérivée de P9 :
  1. 4 à 8 entre une question et son aide, un libellé et son champ, un titre de carte et son texte
  2. 12 à 16 entre éléments d'un même bloc
  3. 24 à 32 entre blocs
  4. 40 à 48 entre sections
- **P21. Espacements identiques entre blocs de même niveau**, partout sur l'écran et d'un écran à l'autre. Pratique courante, non sourcée, conséquence de P18 et P13
- **P22. L'espace entre le titre et le premier bloc n'est jamais plus grand que l'espace entre deux blocs.** Sinon le titre se détache de ce qu'il introduit (P9)
- **P23. Partir de trop d'espace puis retirer**, sauf interface dense assumée comme un tableau de bord [RUI-WS]
- **P24. Hauteurs de ligne multiples de 4** [M2-SPACE]
- **P25. Marge latérale de page constante**, 16 pt sur téléphone. Material fixe 16 dp aux plus petites largeurs [M2-SPACE] ; iOS applique les marges système du layout guide [HIG-LAY], de 16 à 20 pt selon l'appareil (pratique courante, non sourcée pour les valeurs)

### 2.5 Typographie

- **P26. Tailles iOS** : corps 17 pt par défaut, 11 pt minimum [HIG-TYPO]. Styles iOS à la taille par défaut (taille / interligne) : Large Title 34/41, Title 1 28/34, Title 2 22/28, Title 3 20/25, Headline 17/22 semi-gras, Body 17/22, Callout 16/21, Subhead 15/20, Footnote 13/18, Caption 1 12/16, Caption 2 11/13 [HIG-TYPO]
- **P27. Échelle Material 3** (taille / interligne, en sp) : Display 57/64, 45/52, 36/44 ; Headline 32/40, 28/36, 24/32 ; Title 22/28, 16/24, 14/20 ; Body 16/24, 14/20, 12/16 ; Label 14/20, 12/16, 11/16 [M3-TYPE]
- **P28. Éviter les graisses fines** (Ultralight, Thin, Light), surtout en petite taille [HIG-TYPO]
- **P29. Le moins de polices possible** [HIG-TYPO]. Deux familles au maximum, pratique courante, non sourcée pour le chiffre
- **P30. Supporter l'agrandissement du texte** (Dynamic Type sur iOS) ; le texte doit rester lisible et non tronqué jusqu'à 200 % [HIG-LAY] [HIG-TYPO] [WCAG-144]
- **P31. Limiter la troncature** ; préférer plusieurs lignes [HIG-TYPO]
- **P32. Longueur de ligne** : 80 caractères au maximum pour un bloc de texte [WCAG-148]

### 2.6 Couleur et contraste

- **P33. Texte : contraste 4,5 pour 1 minimum ; 3 pour 1 pour le grand texte** (18 pt, ou 14 pt en gras) [WCAG-143] [HIG-A11Y]. Android : 4,5 pour 1 sous 18 sp [AND-A11Y]
- **P34. Composants d'interface et graphiques utiles : 3 pour 1** contre les couleurs adjacentes [WCAG-1411]
- **P35. La couleur n'est jamais le seul porteur d'information** [WCAG-141] [RUI, chapitre « Don't rely on color alone »]
- **P36. Pas de texte gris sur fond coloré** : utiliser une teinte du fond [RUI, chapitre « Don't use grey text on colored backgrounds »]
- **P37. Une couleur, un sens**, documenté dans les jetons. Rôles de couleur à la Material : surface, primaire, conteneur, « sur » (texte posé sur une couleur) [M3-TOKENS]
- **P38. Vérifier les contrastes en clair ET en sombre** si l'app gère les deux [HIG-A11Y]
- **P39. Pas de noir pur en fond**, sauf choix assumé. Pratique courante, non sourcée

### 2.7 Cibles tactiles et zones sûres

- **P40. iOS : cible de 44 × 44 pt**, 28 × 28 pt minimum absolu [HIG-BTN] [HIG-A11Y]
- **P41. Android : 48 × 48 dp** [AND-A11Y], avec au moins 8 dp entre deux cibles [M2-SPACE]
- **P42. Web : 24 × 24 px CSS minimum** (WCAG 2.2 niveau AA), 44 px recommandé sur écran tactile [WCAG-258]
- **P43. Espacer les contrôles** : environ 12 pt autour d'un élément avec fond ou bordure, environ 24 pt autour d'un élément sans fond [HIG-A11Y]
- **P44. Cible grande et proche de là où est le pouce** (loi de Fitts) [LUX-FITTS]
- **P45. Zone du pouce.** Les contrôles du milieu et du bas de l'écran sont plus faciles à atteindre [HIG-IOS]. 49 % des gens tiennent le téléphone d'une main [HOOBER]. Nuance : Hoober a observé ensuite que les gens touchent de préférence le centre de l'écran [HOOBER]. Donc : action principale en bas, jamais en haut dans les coins
- **P46. Respecter les zones sûres** : rien d'important sous la Dynamic Island, la barre d'état, l'indicateur d'accueil ou une barre d'outils [HIG-LAY]

### 2.8 Composants et comportements

- **P47. Un ou deux boutons proéminents par vue** au maximum [HIG-BTN]
- **P48. Distinguer le choix recommandé par le style, pas par la taille** [HIG-BTN]
- **P49. Le libellé du bouton commence par un verbe** et dit le résultat [HIG-BTN] [HIG-WRIT]
- **P50. Une action destructive n'est jamais le bouton principal** [HIG-BTN]
- **P51. États obligatoires** : normal, pressé, désactivé, focus (clavier, lecteur d'écran), plus chargement et sélectionné quand ils existent [HIG-BTN] [M3-STATES] [NNG-STATES]. Survol sur le web seulement [M3-STATES]
- **P52. Action longue : indicateur d'activité dans le bouton** [HIG-BTN]
- **P53. Libellés au-dessus des champs, jamais un texte indicatif à la place du libellé** [NNG-PLACEHOLDER] [NNG-FORMS]
- **P54. Formulaire sur une seule colonne** [NNG-FORMS]
- **P55. Consignes de format près du champ, avant la saisie**, pas sous forme d'erreur [NNG-FORMS]
- **P56. Message d'erreur au plus près du problème**, sans reproche, avec la solution [HIG-WRIT]
- **P57. Proposer des choix plutôt qu'une saisie libre** quand c'est possible [HIG-DATA]
- **P58. Barre d'onglets : navigation, pas actions ; toujours visible ; un libellé par onglet** [HIG-TAB]
- **P59. Alerte : rare, jamais au lancement, jamais pour une simple information** [HIG-ALERT]
- **P60. État vide : dire l'état, apprendre, proposer l'action suivante** [NNG-EMPTY] [HIG-WRIT]
- **P61. Suivre les conventions connues** (loi de Jakob) : les gens attendent que l'app marche comme les autres [LUX-JAKOB]
- **P62. Onboarding court, optionnel, interactif** [HIG-ONB] ; pas de carrousel de cartes explicatives, bouton Passer bien visible [NNG-ONB]
- **P63. Permissions demandées au moment où la fonction en a besoin**, avec le bénéfice expliqué [HIG-ONB] [NNG-PUSH]

## 3. Gabarits d'écran mobile (B)

### 3.0 Règles communes à tous les gabarits

- **G0. Chaque écran déclare son gabarit** (G1 à G6) dans la maquette, le code ou la revue. Un écran sans gabarit déclaré est un défaut
- **G0bis. Jamais de répartition automatique des blocs sur la hauteur.** Interdits sur le conteneur de contenu : `justify-content: space-between`, `space-around`, `space-evenly`, `margin-top: auto` ou `margin-bottom: auto` sur un bloc de contenu, espaceur extensible (`flex: 1`, `flex-grow`) entre deux blocs de contenu. Seules exceptions : le pied d'écran qui porte le bouton (G1, G2, G3) et le groupe central du gabarit Focus (G3). Sources : P9, P22, section 1
- **G0ter. Le titre est toujours à la même place** d'un écran à l'autre : en haut, sous la barre de navigation ou la zone sûre. Pratique courante, non sourcée, appuyée sur [LUX-JAKOB] [HIG-LAY]
- **G0quater. Largeurs de contrôle** : dessiner à 390 × 844 pt (iPhone standard récent) et vérifier à 375 × 667 pt (petit iPhone) et 320 pt de large. Pratique courante, non sourcée pour le choix des tailles

### G1. Explication / lecture

**Quand** : écran qui explique, présente un concept, un bénéfice, une étape d'onboarding, une consigne avant exercice.

**Construction**
1. Aligné en haut. Les blocs s'empilent dans l'ordre de lecture
2. Titre en haut, marge haute de 16 pt sous la barre de navigation ou la zone sûre
3. 16 à 24 pt entre titre et premier bloc (jamais plus que l'espace entre blocs, P22)
4. Blocs espacés de 24 pt entre eux (même valeur pour tous les blocs de même niveau)
5. Bouton principal fixé en bas, hors du flux de défilement : marges latérales 16 pt, 16 pt au-dessus de la zone sûre basse, hauteur 48 à 56 pt
6. Espace libre en bas, entre le dernier bloc et le bouton. Il varie selon l'appareil, c'est normal
7. Si le contenu défile, il reçoit en bas une marge égale à la hauteur du pied (bouton + marges) pour que le dernier texte ne passe jamais sous le bouton
8. Bouton secondaire éventuel (« Passer », « Plus tard ») : en style texte, sous ou au-dessus du bouton principal, dans le même pied

Sources : [HIG-LAY] [NNG-SCROLL] [NNG-IOSRULES] [HIG-IOS] [RUI, « You don't have to fill the whole screen »]. Le bouton fixé en bas est appuyé par NN/g (bouton de validation persistant en bas, exemple Hotel Tonight) [NNG-IOSRULES].

### G2. Formulaire / question

**Quand** : l'écran demande une réponse, une saisie, un choix (questionnaire, réglage, inscription).

**Construction**
1. Aligné en haut
2. Question en titre, en haut
3. Aide ou explication collée sous la question : 4 à 8 pt [P10]
4. Champ ou liste d'options : 16 à 24 pt sous l'aide
5. Options de même hauteur, même espacement (8 à 12 pt), cibles de 44 pt minimum [P40]
6. Libellé au-dessus de chaque champ, 4 à 8 pt ; erreur sous le champ, 4 pt [P53] [P56]
7. Bouton principal fixé en bas, comme G1 ; quand le clavier est ouvert, il remonte au-dessus du clavier
8. Bouton désactivé tant que la réponse est incomplète, avec un état désactivé lisible [P51]
9. Une question par écran quand le parcours est un questionnaire mobile. Pratique courante, non sourcée, appuyée sur [LUX-HICK]

Sources : [NNG-PROX] [NNG-FORMSPACE] [NNG-FORMS] [NNG-PLACEHOLDER] [HIG-DATA] [NNG-IOSRULES].

### G3. Focus / résultat

**Quand** : un seul objet central à regarder ou à vivre. Résultat, score, célébration, minuteur, exercice de respiration, citation courte, écran de chargement long. Pas plus de trois lignes de texte dans le groupe central.

**Construction**
1. Titre en haut, à la même position que sur G1 et G2
2. Bouton en bas, fixé comme G1
3. Le groupe central (illustration, chiffre, texte court) est centré verticalement dans l'espace restant entre le bas du titre et le haut du pied
4. Le groupe central est UN seul groupe : ses éléments internes restent serrés selon P20, ils ne se répartissent pas
5. Si le contenu dépasse la hauteur disponible, l'écran bascule en G1

Sources : l'équilibre symétrique donne une composition calme centrée sur un point [NNG-PRINC] ; un seul point d'entrée [NNG-HIER]. Le centrage vertical lui-même : pratique courante, non sourcée.

### G4. Liste / tableau de bord

**Quand** : accueil, historique, liste de contenus, réglages, tableau de bord.

**Construction**
1. Aligné en haut, l'écran défile
2. Titre en haut (grand titre iOS possible, qui se réduit au défilement)
3. Sections : en-tête de section, puis 8 à 12 pt, puis contenu. 32 pt entre sections
4. Lignes et cartes de même type : même hauteur minimale, même padding interne, même espacement
5. Barre d'onglets en bas, toujours visible [HIG-TAB]
6. Pas de bouton principal fixé, sauf action dominante de l'écran
7. État vide conçu [NNG-EMPTY]
8. Densité plus forte acceptée si elle est voulue [RUI-WS]

Sources : [HIG-LAY] [HIG-TAB] [NNG-SCROLL] [RUI-WS].

### G5. Feuille modale / pop-up (bottom sheet)

**Quand** : tâche courte et ciblée, choix contextuel, détail qui garde l'écran parent visible. Jamais pour un parcours de plusieurs pages.

**Construction**
1. Ancrée en bas, coins hauts arrondis, poignée de glissement en haut
2. Hauteurs d'arrêt : moyenne (environ la moitié) ou grande [HIG-SHEET]
3. Contenu aligné en haut à l'intérieur de la feuille : poignée, titre, contenu
4. Bouton Fermer visible (X), la poignée seule ne suffit pas [NNG-SHEET]
5. iOS : Annuler à gauche en haut, OK / Terminé à droite [HIG-SHEET]. Si Terminé existe, Annuler ou Retour existe aussi [HIG-SHEET]
6. Action principale en bas de la feuille, au-dessus de la zone sûre
7. Un toucher sur le voile d'arrière-plan ferme la feuille [M3-SHEET] ; le bouton Retour Android aussi [NNG-SHEET]
8. Une seule feuille à la fois, jamais empilées [HIG-SHEET] [NNG-SHEET]
9. Tâche longue ou complexe : écran plein modal plutôt que feuille [HIG-SHEET] [HIG-MODAL]
10. Pop-up centrée (alerte) : réservée aux décisions critiques, titre, texte court, trois boutons au maximum [HIG-ALERT]

### G6. Écran verrouillé et notifications

**Quand** : maquette qui montre une notification push, un rappel, un écran verrouillé, un message de retour dans l'app.

**Construction, iOS**
1. Écran verrouillé, iOS 16 et suivants : l'heure et les widgets en haut, **les notifications en bas de l'écran**, empilées, la plus récente au-dessus (affichage Pile par défaut ; Nombre et Liste existent aussi) [APPLE-LOCK]
2. Téléphone déverrouillé : la notification arrive en **bannière en haut de l'écran** [APPLE-BANNER]
3. Anatomie : icône de l'app au début (ajoutée par le système), titre court, texte en phrases complètes. Ne pas répéter le nom de l'app dans le titre [HIG-NOTIF]
4. App au premier plan : pas de bannière système ; l'information s'intègre discrètement (pastille, nouvelle ligne dans la vue) [HIG-NOTIF]

**Construction, Android**
5. Icône dans la barre d'état en haut, volet des notifications ouvert en glissant depuis le haut, notification « heads-up » en fenêtre flottante devant l'app, notifications sur l'écran verrouillé [AND-NOTIF]. La position en haut de l'écran de la fenêtre heads-up : pratique courante observée, la page Android dit « floating window » sans préciser

**Retours dans l'app**
6. Message bref non bloquant (snackbar) : en bas de l'écran, au-dessus de la barre de navigation, jamais devant un bouton ou la navigation [M3-SNACK]
7. Un retour s'affiche près de la zone où la personne agit [NNG-NOTIF]
8. Une erreur passe par une alerte ou un message près du champ, jamais par une notification [HIG-NOTIF] [HIG-WRIT]

**Contenu**
9. Concis, pas d'information sensible, pas de rappel en rafale, pas de notification qui ordonne une tâche [HIG-NOTIF] [NNG-PUSH]
10. Une notification dessinée dans une maquette est TOUJOURS à sa position système réelle. Jamais au milieu d'un écran d'app

## 4. Ce qu'un senior ne fait jamais (C)

### 4.1 Les cinq défauts constatés sur La Sphère / Brio

- **X1. Répartir automatiquement les blocs sur la hauteur** (marges automatiques, `space-between`, espaceurs extensibles). Correction : gabarit déclaré, alignement en haut, espace libre en bas [G0bis] [NNG-PRINC] [RUI « You don't have to fill the whole screen »] [NNG-SCROLL]
- **X2. Éloigner une explication de sa question.** Correction : aide à 4 à 8 pt sous la question [P10] [NNG-PROX] [NNG-FORMSPACE]
- **X3. Laisser un trou sous le titre.** Correction : titre vers premier bloc inférieur ou égal à l'espace entre blocs [P22] [RUI « Avoid ambiguous spacing »]
- **X4. Faire descendre un bouton au milieu d'un texte** ou entre deux paragraphes. Correction : bouton principal fixé dans le pied d'écran, hors du flux [G1] [NNG-IOSRULES] [HIG-IOS]
- **X5. Mettre une notification flottante** au milieu d'un écran ou à une position inventée. Correction : position système réelle, en bas sur écran verrouillé iOS 16+, en haut déverrouillé, en haut sur Android [G6] [APPLE-LOCK] [APPLE-BANNER] [AND-NOTIF]

### 4.2 Autres erreurs de senior

- **X6.** Deux boutons principaux concurrents [P47]
- **X7.** Distinguer deux boutons voisins par la taille au lieu du style [P48]
- **X8.** Un texte indicatif à la place du libellé [P53]
- **X9.** Un paragraphe long centré [P16]
- **X10.** Du gris sur fond coloré, un contraste sous 4,5 pour 1 [P33] [P36]
- **X11.** Une graisse fine en petite taille [P28]
- **X12.** Une information portée par la couleur seule [P35]
- **X13.** Une cible tactile sous 44 pt (iOS) ou 48 dp (Android) [P40] [P41]
- **X14.** Du contenu sous la Dynamic Island, la barre d'état ou l'indicateur d'accueil [P46]
- **X15.** Le dernier texte caché derrière le bouton fixé [G1 point 7]
- **X16.** Le titre qui change de place d'un écran à l'autre [G0ter]
- **X17.** Des valeurs d'espacement hors échelle, ou deux blocs de même niveau espacés différemment [P18] [P21]
- **X18.** Un élément interactif sans état pressé ou désactivé [P51]
- **X19.** Des feuilles modales empilées, une feuille pour un parcours de plusieurs pages [G5]
- **X20.** Une alerte au lancement, une alerte purement informative [P59]
- **X21.** Un onboarding en carrousel de cartes sans bouton Passer [P62]
- **X22.** Demander les notifications au premier lancement sans contexte [P63]
- **X23.** Cacher la barre d'onglets ou mettre des actions dedans [P58]
- **X24.** Une troncature en plein mot sur un élément important [P31]
- **X25.** Un écran dessiné sans design system de référence [section 5]

### 4.3 Règles maison validées par Bentho (bloquantes)

- **X26. Cadre à moitié vide.** Une carte étirée à la hauteur de sa voisine dont le contenu occupe moins de 75 % de la hauteur. Correction : changer la mise en page, jamais laisser le vide (validé par Bentho le 13 septembre 2026, projet Winners)
- **X27. Colonnes voisines non alignées** : le haut et le bas de deux blocs côte à côte (titre, bouton) tombent sur les mêmes lignes (Bentho, 13 septembre 2026)
- **X28. Titres trop petits et blocs de texte monolithiques** sans repère (Bentho, 13 septembre 2026)
- **X29. Pastilles et étiquettes toutes de la même teinte** quand elles représentent des catégories différentes : une teinte par catégorie (Bentho, 13 septembre 2026)
- **X30. Émojis clavier dans l'interface.** Utiliser un jeu d'icônes cohérent, même trait, même taille (mémoire design de Bentho)
- **X31. Formes disparates** : tous les boutons principaux de même forme, taille et rayon ; toutes les étiquettes de même forme ; toutes les cartes de même structure. Un changement de forme signale un vrai changement de sens (mémoire design de Bentho) [LUX-SIM]

## 5. Design system et UI kit (D)

**Règle D0.** On ne dessine pas un écran sans système de référence. S'il n'existe pas, le designer en propose un minimal (sur la base des valeurs iOS ou Material ci-dessus), Bentho le valide, puis on dessine. Sources : un design system réunit guide de style, bibliothèque de composants et bibliothèque de motifs, et garantit la cohérence [NNG-DS] ; jetons système et jetons de composant [M3-TOKENS] ; limiter ses choix en amont [RUI, chapitre « Limit your choices »] ; définir ses nuances dès le départ [RUI, chapitre « Define your shades up front »].

**Éléments minimaux**
1. **Jetons couleur** par rôle : fond, surface, surface élevée, texte principal, texte secondaire, texte désactivé, primaire, sur primaire, conteneur primaire, bordure, succès, alerte, erreur, couleurs de catégorie. Chaque paire texte et fond vérifiée à 4,5 pour 1 [P33]
2. **Jetons typographiques** : chaque style nommé avec police, taille, interligne, graisse (titre écran, titre section, corps, secondaire, libellé, bouton). Trois à cinq styles pour un produit simple
3. **Jetons d'espacement** : l'échelle 4, 8, 12, 16, 24, 32, 40, 48, 64, plus la marge de page
4. **Jetons de rayon** : deux ou trois valeurs, le plus grand pour les conteneurs [M3-SHAPE]
5. **Élévation et ombres** : deux niveaux au maximum pour un produit simple. Pratique courante, non sourcée
6. **Icônes** : un seul jeu, même trait, même grille de taille [M2-SPACE]
7. **Composants avec tous leurs états** [P51] :
   1. Bouton principal, secondaire, texte, destructif
   2. Champ de saisie, avec libellé, aide, erreur
   3. Option de choix (carte sélectionnable, case, bouton radio), sélectionnée ou non
   4. Carte
   5. Ligne de liste
   6. Barre de navigation haute
   7. Barre d'onglets
   8. Feuille modale
   9. Alerte
   10. Message bref (snackbar)
   11. Étiquette ou pastille
   12. Barre de progression
   13. État vide
   14. Chargement (squelette ou indicateur)
8. **Les six gabarits G1 à G6** codés une fois, réutilisés partout
9. **Un fichier source unique** du système dans le projet (par exemple `tokens.ts` ou `DESIGN-SYSTEM.md`), cité dans chaque revue

## 6. Dérogations (E)

1. **Où** : `DESIGN-DEROGATIONS.md` à la racine du projet
2. **Qui décide** : Bentho seul. Une dérogation n'existe que s'il l'a confirmée en connaissant la règle contredite
3. **Le designer** lit ce fichier avant toute revue ou tout conseil, applique les dérogations actives, et les signale dans sa sortie quand elles contredisent une règle sourcée (une ligne, sans les recompter comme défaut)
4. **Nouvelle demande contraire à une règle** : le designer passe en mode conseil (contexte, options, pour, contre, avis, question). Si Bentho confirme, l'entrée est ajoutée au fichier par la session principale
5. **Dérogation d'accessibilité** (contraste, cible tactile, taille minimale) : acceptée si Bentho confirme, mais rappelée à chaque revue comme risque
6. **Format d'une entrée**

```
## D-001 Titre court de la dérogation
- Date : 2026-09-17
- Portée : écran(s) concerné(s), ou tout le projet
- Règle contredite : identifiant + source (ex. P16 [HIG-LAY])
- Ce que Bentho veut : description exacte, avec valeurs
- Pourquoi : ses mots
- Statut : active | révoquée le AAAA-MM-JJ
```

## 7. Checklist de revue (F)

À passer sur chaque écran avant livraison. Chaque ligne se prouve par une mesure ou une capture.

1. `DESIGN-DEROGATIONS.md` lu, dérogations actives listées
2. Design system de référence identifié [D0]
3. Gabarit déclaré (G1 à G6) et respecté [G0]
4. Aucune répartition automatique des blocs [G0bis]
5. Objectif unique et une seule action principale [P2] [P47]
6. Titre en haut, à la même position que sur les autres écrans [G0ter]
7. Titre vers premier bloc inférieur ou égal à l'espace entre blocs [P22]
8. Aide et libellés collés à leur question ou champ (4 à 8 pt) [P10]
9. Espacements sur l'échelle, identiques entre blocs de même niveau [P18] [P21]
10. Bouton principal fixé en bas, marges 16 pt, au-dessus de la zone sûre ; dernier contenu jamais caché [G1]
11. Espace libre en bas, pas entre les blocs [section 1]
12. Alignement sur un bord gauche, aucun décalage [P15] [P17]
13. Trois tailles de texte au maximum, corps à 16 ou 17, rien sous 11 [P3] [P26] [P27]
14. Contrastes calculés : 4,5 pour 1 texte, 3 pour 1 grand texte et composants [P33] [P34]
15. Aucune information par la couleur seule [P35]
16. Cibles 44 pt iOS ou 48 dp Android, espacées [P40] [P41] [P43]
17. Zones sûres respectées [P46]
18. États présents sur tout élément interactif [P51]
19. Notifications et feuilles à leur position système [G5] [G6]
20. Aucune troncature, texte agrandi à 200 % sans casse [P30] [P31]
21. Vérifié à 390, 375 et 320 pt de large [G0quater]
22. Règles maison X26 à X31
23. Page de conversion : page-cro passé en plus
24. Verdict de l'agent `designer` rendu

## 8. Sources

| Code | Source | URL |
|---|---|---|
| HIG-LAY | Apple HIG, Layout | https://developer.apple.com/design/human-interface-guidelines/layout |
| HIG-IOS | Apple HIG, Designing for iOS | https://developer.apple.com/design/human-interface-guidelines/designing-for-ios |
| HIG-BTN | Apple HIG, Buttons | https://developer.apple.com/design/human-interface-guidelines/buttons |
| HIG-TYPO | Apple HIG, Typography | https://developer.apple.com/design/human-interface-guidelines/typography |
| HIG-A11Y | Apple HIG, Accessibility | https://developer.apple.com/design/human-interface-guidelines/accessibility |
| HIG-NOTIF | Apple HIG, Notifications | https://developer.apple.com/design/human-interface-guidelines/notifications |
| HIG-SHEET | Apple HIG, Sheets | https://developer.apple.com/design/human-interface-guidelines/sheets |
| HIG-MODAL | Apple HIG, Modality | https://developer.apple.com/design/human-interface-guidelines/modality |
| HIG-ONB | Apple HIG, Onboarding | https://developer.apple.com/design/human-interface-guidelines/onboarding |
| HIG-ALERT | Apple HIG, Alerts | https://developer.apple.com/design/human-interface-guidelines/alerts |
| HIG-TAB | Apple HIG, Tab bars | https://developer.apple.com/design/human-interface-guidelines/tab-bars |
| HIG-WRIT | Apple HIG, Writing | https://developer.apple.com/design/human-interface-guidelines/writing |
| HIG-DATA | Apple HIG, Entering data | https://developer.apple.com/design/human-interface-guidelines/entering-data |
| APPLE-LOCK | Apple Support, notifications sur l'écran verrouillé | https://support.apple.com/en-us/108781 |
| APPLE-BANNER | Apple, Guide iPhone, réglages des notifications | https://support.apple.com/guide/iphone/change-notification-settings-iph7c3d96bab/ios |
| AND-NOTIF | Android Developers, About notifications | https://developer.android.com/develop/ui/compose/notifications |
| AND-A11Y | Android Developers, Make apps more accessible | https://developer.android.com/guide/topics/ui/accessibility/apps |
| M2-SPACE | Material Design, Spacing methods | https://m2.material.io/design/layout/spacing-methods.html |
| M3-TYPE | Material 3, Type scale (valeurs relevées dans les jetons officiels material-web) | https://m3.material.io/styles/typography/type-scale-tokens et https://github.com/material-components/material-web/blob/main/tokens/versions/v0_192/_md-sys-typescale.scss |
| M3-TOKENS | Material 3, Design tokens et rôles de couleur | https://m3.material.io/foundations/design-tokens et https://m3.material.io/styles/color/roles |
| M3-SHAPE | Material 3, Corner radius scale | https://m3.material.io/styles/shape/corner-radius-scale |
| M3-STATES | Material 3, Interaction states | https://m3.material.io/foundations/interaction/states/applying-states |
| M3-SHEET | Material 3, Bottom sheets | https://m3.material.io/components/bottom-sheets/guidelines |
| M3-SNACK | Material 3, Snackbar | https://m3.material.io/components/snackbar/guidelines |
| NNG-PRINC | NN/g, 5 Principles of Visual Design | https://www.nngroup.com/articles/principles-visual-design/ |
| NNG-HIER | NN/g, Visual Hierarchy | https://www.nngroup.com/articles/visual-hierarchy-ux-definition/ |
| NNG-PROX | NN/g, Proximity Principle | https://www.nngroup.com/articles/gestalt-proximity/ |
| NNG-SCROLL | NN/g, Scrolling and Attention | https://www.nngroup.com/articles/scrolling-and-attention/ |
| NNG-F | NN/g, F-Shaped Pattern | https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/ |
| NNG-FORMSPACE | NN/g, White Space in Form Design | https://www.nngroup.com/articles/form-design-white-space/ |
| NNG-PLACEHOLDER | NN/g, Placeholders in Form Fields | https://www.nngroup.com/articles/form-design-placeholders/ |
| NNG-FORMS | NN/g, Website Forms Usability | https://www.nngroup.com/articles/web-form-design/ |
| NNG-CLOSE | NN/g, Closeness of Actions and Objects | https://www.nngroup.com/articles/closeness-of-actions-and-objects-gui/ |
| NNG-IOSRULES | NN/g, iOS Design Rules to Break (bouton sous les champs, bouton persistant en bas) | https://www.nngroup.com/articles/4-ios-rules-break/ |
| NNG-SHEET | NN/g, Bottom Sheets | https://www.nngroup.com/articles/bottom-sheet/ |
| NNG-NOTIF | NN/g, Indicators, Validations, and Notifications | https://www.nngroup.com/articles/indicators-validations-notifications/ |
| NNG-PUSH | NN/g, Mistakes in Push Notifications | https://www.nngroup.com/articles/push-notification/ |
| NNG-ONB | NN/g, Mobile App Onboarding | https://www.nngroup.com/articles/mobile-app-onboarding/ |
| NNG-STATES | NN/g, Button States | https://www.nngroup.com/articles/button-states-communicate-interaction/ |
| NNG-EMPTY | NN/g, Empty States | https://www.nngroup.com/articles/empty-state-interface-design/ |
| NNG-DS | NN/g, Design Systems 101 | https://www.nngroup.com/articles/design-systems-101/ |
| RUI | Refactoring UI, Adam Wathan et Steve Schoger (livre, chapitres cités par titre) | https://www.refactoringui.com/ |
| RUI-WS | Refactoring UI, chapitre gratuit « Start with too much white space » | https://refactoring-ui.nyc3.cdn.digitaloceanspaces.com/Refactoring%20UI%20-%20Start%20with%20too%20much%20white%20space.pdf |
| LUX-FITTS | Laws of UX, Fitts's Law | https://lawsofux.com/fittss-law/ |
| LUX-HICK | Laws of UX, Hick's Law | https://lawsofux.com/hicks-law/ |
| LUX-JAKOB | Laws of UX, Jakob's Law | https://lawsofux.com/jakobs-law/ |
| LUX-PROX | Laws of UX, Law of Proximity (Gestalt) | https://lawsofux.com/law-of-proximity/ |
| LUX-SIM | Laws of UX, Law of Similarity (Gestalt) | https://lawsofux.com/law-of-similarity/ |
| LUX-REGION | Laws of UX, Law of Common Region (Gestalt) | https://lawsofux.com/law-of-common-region/ |
| WCAG-143 | WCAG 2.2, 1.4.3 Contrast (Minimum) | https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html |
| WCAG-1411 | WCAG 2.2, 1.4.11 Non-text Contrast | https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html |
| WCAG-141 | WCAG 2.2, 1.4.1 Use of Color | https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html |
| WCAG-144 | WCAG 2.2, 1.4.4 Resize Text | https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html |
| WCAG-148 | WCAG 2.2, 1.4.8 Visual Presentation (niveau AAA) | https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html |
| WCAG-258 | WCAG 2.2, 2.5.8 Target Size (Minimum) | https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html |
| HOOBER | Steven Hoober, How Do Users Really Hold Mobile Devices?, UXmatters | https://www.uxmatters.com/mt/archives/2013/02/how-do-users-really-hold-mobile-devices.php |

## 9. Web, à compléter

Mobile d'abord. Pour le web, s'appliquent déjà : P1 à P39, P42 (24 px minimum), P51 avec l'état survol, P53 à P56, la lecture en F sur les pages de contenu (titres porteurs de sens, informations clés en tête) [NNG-F], et 80 caractères maximum par ligne [WCAG-148]. Les gabarits web (page de contenu, page de conversion, application web) restent à écrire.
