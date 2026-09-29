---
name: event-flyer-design
description: Règles de flyer et d'affiche d'événement de Benjamin/StudioMakers. Format, hiérarchie des informations, structure texte-image-texte, équilibre typographique, méthode de production en HTML rendu en image, génération des visuels via Gemini, et checklist de contrôle avant présentation. À charger AVANT de concevoir, dessiner ou produire un flyer, une affiche, une invitation, un visuel de soirée, de concert, de fête, de vernissage ou de lancement, et à honorer sur toute modification d'un flyer existant. Se déclenche sur "flyer", "affiche", "poster", "visuel de soirée", "invitation", "carton d'invitation", "story Instagram d'événement", "refais le visuel de la soirée", "le flyer est moche", "on organise une soirée il faut un visuel". Se combine avec design-produit pour les règles d'espacement et de typographie, et se fait contrôler par l'agent designer avant toute présentation à Bentho.
---

# Flyer d'événement

Un flyer a un seul travail : donner envie de venir, puis dire quand et où. Tout ce qui ne sert pas ces deux choses se supprime.

Ce skill dit COMMENT construire le flyer. `design-produit` donne les règles d'espacement et de typographie qui s'appliquent en dessous. L'agent `designer` contrôle le résultat avant que Bentho le voie.

## 1. Avant de dessiner, cadrer

Ces quatre questions se posent AVANT toute production. Une réponse manquante est une question à Bentho, jamais une hypothèse silencieuse.

1. **Quelle est la NATURE réelle de l'événement ?** Le thème n'est pas la nature. Une soirée techno sur thème cabaret reste une soirée techno, le flyer doit transmettre l'énergie de la nuit, pas celle d'un spectacle assis. Se tromper là-dessus produit un beau flyer qui parle à la mauvaise personne.
2. **À qui on parle ?** Le visuel, les corps, les tenues, la lumière doivent ressembler aux gens qu'on veut voir arriver.
3. **Quelle est la seule raison de venir CE soir-là ?** Un festival, une date de fin de série, un artiste de passage. Cette raison se nomme sur le flyer, sinon on vend une soirée interchangeable.
4. **Où le flyer sera-t-il vu ?** Feed Instagram, story, WhatsApp, impression. Le format en découle.

## 2. Format

**1080 x 1350 px, ratio 4:5.** C'est le portrait natif du feed Instagram et le meilleur aperçu WhatsApp, les deux canaux de diffusion réels.

Le 5:7 et l'A4 sont trop verticaux pour un usage réseaux, ils se recadrent tout seuls et coupent l'information. Ne les proposer que si le flyer part à l'impression.

Passer d'un format à un autre n'est jamais un étirement. La mise en page se refait : titres recalés, illustration redimensionnée, blocs resserrés, marges reproportionnées.

## 3. Structure, la règle qui ne se négocie pas

**Texte en haut, image au centre, texte en bas.**

Jamais image en haut et texte en bas seulement. Un flyer qui pose son visuel en haut et empile ses informations dessous se lit comme une publicité, pas comme une affiche. Le texte du haut porte l'identité (nom de l'événement, occasion), le texte du bas porte la logistique (date, heure, lieu, prix).

## 4. Hiérarchie des informations

L'ordre de taille par défaut, du plus gros au plus petit :

1. Le nom de l'événement
2. La date
3. Le line-up
4. Le lieu
5. L'adresse, les horaires, le prix, le dress code

Le piège classique est le lieu qui écrase tout. Un club veut voir son logo en grand, ce n'est pas ce qui remplit la salle. Le nom et la date décident si la personne vient, le lieu ne fait que lui dire où aller une fois qu'elle a décidé.

Si le lieu impose sa charte, la porter en bas, en taille de logistique.

## 5. Typographie

1. **Une seule police à caractère**, celle du titre. Tout le reste est neutre. Deux polices expressives sur une même affiche se battent et le résultat fait amateur.
2. **Espacement identique entre les mots d'un même titre.** Ne jamais justifier un titre bord à bord : la justification donne des espacements différents à chaque mot, et un mot plus espacé paraît plus petit alors que les capitales font la même hauteur. Mesurer plutôt que juger à l'oeil.
3. Un titre sur plusieurs lignes se coupe sur le sens, jamais sur la largeur disponible.

## 6. Les marqueurs du flyer cheap

Ces éléments détruisent la perception de qualité plus vite que n'importe quel défaut de composition. Les repérer et les bannir :

1. **Doré brillant à reflets sur fond rouge velours.** Le signal visuel numéro un du club bas de gamme.
2. **Ornements baroques** autour d'un logo ou d'un nom, cadres à volutes, plaques gravées.
3. **Photo de basse définition**, surtout agrandie.
4. **Modèle qui ne ressemble pas au public visé**, tenue ou geste hors thème.
5. **Effets de biseau, ombre portée dure, lueur.**

Le luxe se fait par la retenue, le noir profond, un or MAT, un seul accent de couleur, et de l'espace. Le grain argentique fin est un allié, le flou et la pixellisation ne le sont jamais.

## 7. Produire les visuels

**Génération d'images.** Aucun outil de génération d'images n'est branché dans une session Claude Code. Le chemin gratuit qui fonctionne :

1. Ouvrir [gemini.google.com](https://gemini.google.com/app) dans le Chrome de Bentho via les outils `claude-in-chrome` (son compte est connecté)
2. Taper le prompt, en précisant le ratio vertical 4:5 et « absolutely no text in the image »
3. Cliquer le bouton de téléchargement qui apparaît au survol de l'image
4. Le fichier atterrit dans le dossier de téléchargement de Chrome

Gemini sort typiquement du 928 x 1152 (ratio 0,806) quand la cible est 1080 x 1350 (ratio 0,800). L'écart de 0,7 % est invisible, un léger agrandissement suffit au montage.

Ne jamais transférer une image en base64 à travers le chat, le coût en tokens est prohibitif pour ce que ça rapporte.

**Composition de l'affiche.** Construire en HTML et CSS aux dimensions cibles, puis rendre en PNG par capture. Cette méthode donne un contrôle typographique exact, se corrige en une ligne, et produit autant de variantes qu'on veut sans repartir de zéro.

**Reprise d'un visuel de référence.** Quand Bentho donne une image à reprendre, la FORME se reproduit à l'identique, au contour près. Seuls le style (trait, matière, fond) et le design d'affiche autour peuvent varier. Une référence est une inspiration de composition, jamais un import de police ni de palette.

## 8. Livrer les propositions

1. **Toujours plusieurs propositions comparables**, jamais une seule. Bentho choisit, il ne valide pas.
2. Quand plusieurs directions artistiques sont en jeu, **une proposition par direction**, pour qu'il compare des partis pris et non des variantes du même.
3. Chaque proposition porte le MÊME contenu et la MÊME hiérarchie. Ce qui varie est le traitement, sinon la comparaison ne veut rien dire.
4. **Une seule numérotation.** Ne jamais laisser coexister une référence de fichier et un numéro d'option, Bentho ne saura plus de quoi on parle.
5. **Versionner, jamais écraser.** v3, v4, les précédentes restent.

## 9. Checklist avant de montrer quoi que ce soit

Passer l'agent `designer` puis vérifier :

1. Le nom et la date sont-ils les deux choses les plus grosses ?
2. Y a-t-il du texte en haut, une image au centre, du texte en bas ?
3. Le format est-il en 1080 x 1350 ?
4. Une seule police à caractère ?
5. L'espacement des mots du titre est-il identique, mesuré et non estimé ?
6. Aucun marqueur cheap de la section 6 ?
7. Toutes les informations logistiques y sont-elles (date, heure de début ET de fin, adresse complète, prix, âge minimum si applicable, dress code si applicable) ?
8. Le visuel ressemble-t-il aux gens qu'on veut voir arriver ?
9. La raison de venir CE soir-là est-elle nommée ?

Un point qui échoue se corrige avant la présentation, il ne se signale pas en même temps que le livrable.
