# Testing Amazon, partie 3 — campagnes Meta Ads

> **En cours de définition.** Hamza donne ses instructions le 16/09/2026.
> Ne rien lancer sur Meta avant que ce fichier soit complet et validé.

La partie 3 démarre une fois la fiche produit créée (partie 1) et les
créatives produites (partie 2). Elle **ne fait pas partie du testing
automatique** : elle ne se lance que sur demande explicite d'Hamza.

## ⚠️ RÈGLE — toujours demander le compte publicitaire

**À chaque fois que le pipeline arrive à l'étape ads, demander à Hamza quel
compte publicitaire utiliser.** Ne jamais le supposer, ne jamais reporter le
choix d'un produit précédent. Lui présenter la liste ci-dessous.

Le défaut de travail reste **BootiktiPremium**, mais le choix est le sien à
chaque produit.

### Les 17 comptes de sa liste de référence

| # | Compte | ad_account_id | Pilotable par MCP |
|---|---|---|---|
| 01 | Actif Emerg 001 | `527271895629888` | ⛔ compte DÉSACTIVÉ par Meta |
| 02 | Actif cp Emerg 001 | `521117530324711` | ✅ |
| 03 | Actif Emerg 002 | `595599763430641` | ✅ |
| 04 | Actif Emerg 003 | `456998410798479` | ✅ |
| 05 | Actif cp Emerg 002 | `586493962787132` | ❌ lecture seule |
| 06 | Actif cp Emerg 003 | `607657055550723` | ✅ |
| 07 | BootiktiPremium 001 | `586926064144750` | ✅ |
| 08 | Actif Emerg Renai BM 001 | `1117600846770141` | ❌ lecture seule |
| 10 | BootiktiPremium 003 | `499810739343442` | ✅ |
| 11 | Actif Emerg 004 | `1311333073389358` | ✅ |
| 12 | Actif Emerg 005 | `1863562074383573` | ✅ |
| 13 | Actif cp Emerg 004 | `579318491592167` | ✅ |
| 14 | Actif cp Emerg 005 | `9233178096752029` | ✅ |
| 16 | Actif BootiktiPremium 005 | `9711966435499771` | ✅ |
| 17 | Actif Emerg Renai BM 002 | `624955156791078` | ✅ |
| 18 | Actif Emerg Renai BM 003 | `515719344871670` | ✅ |
| 20 | Actif Emerg Renai BM 005 | `3889143234688181` | ✅ |

**Les numéros 09, 15 et 19 n'existent pas** — confirmé par Hamza le
16/09/2026. La numérotation garde simplement des trous.

Autres comptes accessibles, hors de cette liste : `ND 01`, `ND 02 UZ`,
`NZ 03 UZ` (Naeldeals, USD) · `AD 03`, `AD 04`, `AD 05` (BM 01, USD) ·
`BM 02 AD 01`, `AD 02`, `AD 03` (BM 02 Service, USD) · `Hamza Hamza`
(perso, lecture seule).

### Si Hamza choisit un compte en lecture seule (05 ou 08)

Préparer tout ce qui peut l'être — créatives, textes, ciblage, structure,
budget — et le lui livrer pour qu'il crée la campagne à la main dans le
Gestionnaire. Ne pas tenter l'appel MCP : Meta le refuse.

## Le portefeuille de travail par défaut — BootiktiPremium

Décision d'Hamza du 16/09/2026 : **le pipeline Testing Amazon tourne par défaut
sur les comptes du portefeuille « BootiktiPremium »**
(`business_id 1749810102230676`). Boutique associée : `bootiktipremium.online`.
Le choix du compte lui est quand même demandé à chaque produit.

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
