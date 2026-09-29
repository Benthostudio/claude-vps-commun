# Sources et requêtes pour cartographier des levées de fonds

Fichier de référence chargé au besoin. Il liste les bases de données de deals, la presse à
privilégier, et des gabarits de requêtes de recherche.

## Bases de données de deals (les plus fiables)

| Source | Zone / force | Accès | Note |
|---|---|---|---|
| Crunchbase | Mondial, généraliste | Freemium (détail derrière paywall) | La référence de départ ; les pages entreprises listent les rounds |
| PitchBook | Mondial, VC/PE | Payant | Le plus complet sur valorisations et PE, mais fermé |
| Dealroom | Europe surtout | Freemium | Très bon sur l'écosystème européen |
| Tracxn | Mondial, secteurs | Freemium | Bon pour cartographier un secteur entier |
| CB Insights | Mondial, tendances | Payant / rapports gratuits | Bons rapports de marché et graphes de financement |
| Sifted | Europe (startups) | Presse, freemium | Analyses de deals européens |
| Maddyness | France | Presse | Deals français |
| Failory / Dealroom lists | Post-mortems, exits | Gratuit | Utile pour repérer faillites et down rounds |

## Presse à privilégier (par fiabilité décroissante)

1. **Tier 1 business/tech** : TechCrunch, Bloomberg, Reuters, Forbes, WSJ, Financial Times.
2. **Spécialisée secteur** : Business of Fashion + Glossy (mode/retail/beauté), Fierce
   (santé), TechCrunch (tech). Choisir selon le secteur étudié.
3. **Communiqués officiels** : sites investisseurs et entreprises (PR Newswire, Business
   Wire) : fiables sur le fait de la levée, à recouper sur le montant.
4. **Presse secondaire / agrégée** : à utiliser seulement pour recouper, jamais comme source
   unique d'un montant.

Règle de fiabilité : agrégateur de deals > presse tier 1 > communiqué officiel > presse
secondaire. Un montant vu uniquement en presse secondaire = marquer "non confirmé".

## Gabarits de requêtes (à décliner)

Remplacer `[ENTREPRISE]`, `[SECTEUR]`, `[INVESTISSEUR]`, `[ANNÉE]`.

Par entreprise :
- `[ENTREPRISE] funding round raised Series`
- `[ENTREPRISE] valuation Series A B C`
- `[ENTREPRISE] levée de fonds montant investisseurs`
- `[ENTREPRISE] crunchbase funding`

Par secteur :
- `[SECTEUR] startups raised funding [ANNÉE]`
- `[SECTEUR] venture capital investment report`
- `most funded [SECTEUR] companies`
- `[SECTEUR] D2C brands funding rounds`

Par investisseur :
- `[INVESTISSEUR] portfolio [SECTEUR]`
- `[INVESTISSEUR] leads investment [SECTEUR]`

Tendances / signaux :
- `[SECTEUR] funding down 2022 2023 2024`
- `[SECTEUR] startup shut down bankruptcy`
- `[SECTEUR] acquisition IPO exit`

## Pièges fréquents

1. **Confondre round et cumul.** "A levé 50 M$" peut vouloir dire un round ou le total
   historique. Toujours vérifier.
2. **Double compte.** Un même round annoncé par plusieurs médias à des montants légèrement
   différents : garder une seule ligne, la source la plus fiable.
3. **Crowdfunding ≠ equity.** Une campagne Kickstarter de 1 M$ n'est pas une levée venture ;
   la classer comme "crowdfunding" et ne pas la mélanger avec les Series.
4. **Devise implicite.** Un montant "10M" sans devise est piégeux ; chercher la devise réelle.
5. **Deals non annoncés.** Beaucoup de tours (surtout seed) ne sont jamais publiés : l'absence
   de deal trouvé ne prouve pas l'absence de financement. Le dire dans la section "trous".
