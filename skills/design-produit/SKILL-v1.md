---
name: design-produit
description: Socle de design produit de Benjamin/StudioMakers pour les écrans d'application et les pages web. Règles de grille, d'espacement, de typographie, de couleur, de hiérarchie, d'états et d'accessibilité, plus la checklist de revue. À charger AVANT de dessiner ou de coder un écran, une page, un composant ou une maquette, et à honorer sur toute modification visuelle. Se déclenche sur "maquette", "écran", "design", "UI", "mise en page", "espacement", "couleurs", "composant", "refonte visuelle", "réagencer une page". Se combine avec page-cro pour les pages de conversion, et se fait contrôler par l'agent designer avant livraison.
---

# Design produit

Ce skill dit COMMENT dessiner. L'agent `designer` dit SI c'est bien dessiné. Les deux vont ensemble, jamais l'un sans l'autre sur un livrable visuel.

## 1. Avant de dessiner, répondre à trois questions

1. **Quel est l'objectif unique de cet écran ?** Un écran qui sert deux objectifs n'en sert aucun.
2. **Quelle est l'action principale ?** Elle doit être la chose la plus visible, et il n'y en a qu'une.
3. **Qu'est-ce que la personne sait déjà en arrivant ?** Ce qu'elle sait n'a pas besoin d'être répété.

Un bloc qui ne sert aucun de ces trois points se supprime.

## 2. L'espacement, la règle qui fait 80 % du rendu

1. **Une seule échelle**, multiples de 4. 4, 8, 12, 16, 20, 24, 32, 40, 48, 64. Aucune valeur hors échelle.
2. **La proximité dit l'appartenance.** L'espace DANS un bloc est toujours plus petit que l'espace ENTRE deux blocs. Rapport minimum de 1 à 2.
3. **Un seul rythme vertical par page.** Si les blocs sont espacés de 12, ils le sont tous. Une exception se justifie ou se supprime.
4. **Le padding interne est constant** sur tous les composants de même niveau. Une carte, c'est toujours le même padding.
5. **Marge de page identique partout**, y compris sur les écrans en pleine largeur.

## 3. La hiérarchie

1. **Trois niveaux de texte maximum par écran.** Titre, corps, secondaire. Un quatrième niveau est presque toujours un titre déguisé.
2. **La taille, le gras et la couleur ne se cumulent pas.** Un seul de ces trois leviers suffit à distinguer.
3. **Le texte secondaire n'est jamais en dessous de 11 px** ni en dessous d'un contraste de 4,5 contre 1.
4. **Un écran a un point d'entrée visuel unique.** Si l'oeil hésite entre deux éléments au premier coup d'oeil, l'un des deux doit reculer.
5. **L'ordre de lecture suit l'ordre du besoin**, pas l'ordre du système ni celui de la base de données.

## 4. La couleur

1. **Une couleur, un sens.** Une couleur qui sert à deux choses ne veut plus rien dire. Documenter le sens de chaque couleur.
2. **Jamais deux blocs de la même couleur qui se suivent** sans séparation nette.
3. **Les couleurs de catégorie sont réservées aux catégories**, partout dans le produit, sans exception.
4. **Le fond plein d'un bloc dépliable garde la couleur de son en-tête.** Un panneau blanc qui s'ouvre sous un en-tête coloré casse l'unité.
5. **Contraste minimum 4,5 contre 1** pour le texte, 3 contre 1 pour les éléments d'interface.
6. **Pas de noir pur** en fond, sauf choix assumé. Une couleur de marque profonde fait le même travail en plus chaleureux.

## 5. Les composants

1. **Même fonction, même forme.** Deux boutons qui font la même chose se ressemblent à l'identique.
2. **Rayons de coin cohérents.** Une échelle, deux ou trois valeurs maximum, la plus grande pour les conteneurs.
3. **Zone tactile minimum 44 par 44 px.** Un chevron de 16 px a une zone cliquable de 44.
4. **Tout élément interactif a quatre états**, normal, survol, actif, désactivé. Un état manquant est un défaut.
5. **Les icônes ont toutes la même graisse et la même taille de grille.** Une icône plus épaisse que les autres se voit immédiatement.
6. **Un libellé sous une icône, ou rien.** L'icône seule n'est acceptable que si le titre de l'écran la confirme.

## 6. Le texte de l'interface

1. **Un mot par concept**, pour toujours. Pas de synonymes dans une interface.
2. **Le bouton dit l'action**, jamais un mot vague comme Valider ou Continuer quand on peut dire ce qui se passe.
3. **Pas de troncature en plein mot** sur un élément important. Raccourcir le contenu, pas la place.
4. **Les états vides parlent.** Un écran vide dit quoi faire, il ne dit pas seulement qu'il est vide.
5. **Les nombres sont en chiffres tabulaires**, pour que les colonnes ne bougent pas.

## 7. Mobile d'abord

1. Dessiner à 375 px de large avant tout le reste.
2. Vérifier qu'aucune ligne importante ne se coupe à 320 px.
3. Le pouce atteint le bas de l'écran, pas le haut. L'action principale vit en bas.
4. Aucun défilement horizontal, sauf conteneur explicitement fait pour.
5. Tester à 200 % de taille de texte, l'écran ne doit pas casser.

## 8. Checklist de revue, à passer avant toute livraison

1. Un objectif unique, une action principale
2. Espacements sur l'échelle, rythme vertical constant
3. Proximité respectée, dedans plus serré que dehors
4. Trois niveaux de texte maximum
5. Alignements, tout est aligné sur la même grille, aucun décalage d'un ou deux pixels
6. Couleurs, une couleur un sens, pas deux blocs identiques qui se suivent
7. Contrastes vérifiés
8. Zones tactiles à 44 px
9. Tous les états présents
10. Aucune troncature en plein mot, aucun débordement
11. Ordre des blocs conforme au besoin de la personne
12. Si c'est une page de conversion, le skill page-cro est passé en plus
13. L'agent `designer` a rendu son verdict

## 9. Ce qui vaut refus

Un écran ne se livre pas s'il a l'un de ces défauts.
1. Deux actions principales concurrentes
2. Des espacements hors échelle ou incohérents entre blocs voisins
3. Un texte illisible, contraste ou taille
4. Un élément interactif sans état visible
5. Une couleur utilisée pour deux sens différents
6. Un débordement ou une troncature sur mobile
