# Testing Amazon, partie 3 — campagnes Meta Ads

> **En cours de définition.** Hamza donne ses instructions le 16/09/2026.
> Ne rien lancer sur Meta avant que ce fichier soit complet et validé.

La partie 3 démarre une fois la fiche produit créée (partie 1) et les
créatives produites (partie 2). Elle **ne fait pas partie du testing
automatique** : elle ne se lance que sur demande explicite d'Hamza.

## Le compte de travail — BootiktiPremium

Décision d'Hamza du 16/09/2026 : **le pipeline Testing Amazon tourne sur les
comptes publicitaires du portefeuille business « BootiktiPremium »**
(`business_id 1749810102230676`). Boutique associée : `bootiktipremium.online`.

### Comptes publicitaires (tous EUR, actifs, MCP ouvert)

| Compte | ad_account_id |
|---|---|
| 07 BootiktiPremium 001 | `586926064144750` |
| 10 BootiktiPremium 003 | `499810739343442` |
| 16 Actif BootiktiPremium 005 | `9711966435499771` |

Budget quotidien minimum : **0,87 €** par ad set.

### Pages disponibles

| Page | page_id |
|---|---|
| معدات رياضية أوروبية أصلية | `1135519649642384` |
| Chrono destock | `612335108632360` |
| Top gadgets dz | `583918584812801` |
| Best Seller dz | `554899241051211` |
| Authentica dz | `563129580227946` |
| Original shoes | `1070824092773899` |
| Wally Algiers | `581279238392104` |

Les deux premières collent particulièrement au pipeline : la page arabe
(« équipements sportifs européens originaux ») pour le sport, et
« Chrono destock » pour l'angle déstockage.

### Pixels

**122 datasets** dans ce BM. Hamza en crée un par produit — beaucoup de
`N Shoes`, plus des pixels produit (`Masseur XXL`, `sperax walk men`,
`Fauteuil high tickets`, `Meuble 1`, `Tapis 2`, `tesvor 2`…).

Deux pixels **jamais déclenchés**, donc disponibles pour un nouveau produit :

| Pixel | dataset_id |
|---|---|
| `PETS` | `1438622408245104` |
| `Hamza 1` | `858635596684170` |

C'est la réserve d'avance dont parlait `REGLES-lightfunnels-meta.md`. Pour en
trouver d'autres, filtrer sur `last_fired_time` vide (`1969-12-31`).

### ⛔ Compte à ne pas utiliser via le MCP

`08 Actif Emerg Renai BM 001` (`1117600846770141`) : le compte est ACTIF et
lisible, mais `is_ads_mcp_enabled: false` — Meta n'a pas encore ouvert l'accès
programmatique dessus. Vérifié deux fois le 16/09/2026. On peut lire ses
données, pas y créer de campagne. À la main dans le Gestionnaire, tout marche.

## Ce qui est déjà connu

Repris de `REGLES-lightfunnels-meta.md`, vérifié en séance le 14/09/2026.

### Ce que le MCP Meta permet

- **Campagnes complètes** : `ads_create_campaign` → `ads_create_ad_set`
  (ciblage, budget, **et sélection du pixel**) → `ads_creative_upload_image` →
  `ads_create_creative` → `ads_create_ad`
- **Sur un pixel existant** : créer des règles d'événement (Purchase,
  AddToCart, Lead…), ajouter les extracteurs de paramètres (valeur, devise),
  activer ou désactiver, lire la qualité du signal et le volume
- **Audiences** : site web, retargeting, lookalikes
- Les campagnes se créent **en pause** — faire valider chaque niveau avant
  activation

### Ce que le MCP Meta ne permet PAS

- **Créer un nouveau pixel / dataset** — Gestionnaire d'événements uniquement

### Quantité de créatives

**10 créatives par ad set** (décision du 16/09/2026).

## À définir avec Hamza

- Objectif de campagne (Achat / Prospect / Messages)
- Structure : nombre d'ad sets, répartition des créatives
- Budget par ad set et stratégie d'enchères
- Ciblage Algérie : wilayas, âge, sexe, centres d'intérêt ou broad
- Pixel à utiliser, et événement optimisé
- Nommage des campagnes, ad sets et ads
- Texte principal, titre et description de l'annonce
- Règles de coupure : seuils, délais, métrique de décision

## Rappel de la règle 1

Rien ne se lance sur Meta sans annonce préalable et accord d'Hamza. Les
campagnes se créent en pause, et chaque niveau est validé avant activation.
Une campagne active engage du budget réel : c'est l'action la plus coûteuse
du projet en cas d'erreur.
