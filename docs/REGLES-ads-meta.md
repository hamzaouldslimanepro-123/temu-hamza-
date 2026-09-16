# Testing Amazon, partie 3 — campagnes Meta Ads

> **En cours de définition.** Hamza donne ses instructions le 16/09/2026.
> Ne rien lancer sur Meta avant que ce fichier soit complet et validé.

La partie 3 démarre une fois la fiche produit créée (partie 1) et les
créatives produites (partie 2). Elle **ne fait pas partie du testing
automatique** : elle ne se lance que sur demande explicite d'Hamza.

## ⚠️ RÈGLE — UN SEUL bloc de questions, tout au début

Règle d'Hamza du 16/09/2026, pour limiter les allers-retours, les actions et
les crédits : **toutes les questions du pipeline se posent en une seule fois,
juste après le scraping.** Parties 1, 2 et 3 confondues. Il répond à tout d'un
coup, puis on enchaîne sans le relancer.

### Le bloc, dans l'ordre

```
PRODUIT
1. Mannequin : A homme · B femme couverte · C tel quel · D avatar humain
2. Prix de vente en DZD
3. Prix barré : oui (lequel) ou non

ADS
4. Compte publicitaire (liste des 14)
5. Audience : broad · hommes · femmes
6. Âge minimum 26 ans : oui ou non
7. Vidéos : oui ou non  → si oui, un 3e ad set
8. Pixel (liste présentée en même temps)
9. Afficher le prix dans le TEXTE de l'annonce : oui ou non
```

Ce qui **ne se demande pas**, parce que c'est déduit ou fixe :

- **Le budget** — calculé depuis le prix (≤ 10 000 DZD → 10 € · > 10 000 → 20 €)
- L'objectif, le pays, les placements, les titres, la structure : tous fixes
- La description : toujours l'angle qualité premium

### Le pixel — dépendance à résoudre dans le même bloc

Les pixels se listent par compte publicitaire, or le compte fait partie des
questions. Pour ne pas couper le bloc en deux : **lister d'emblée les pixels du
portefeuille par défaut BootiktiPremium** en même temps que la question du
compte. Si Hamza choisit un autre compte, récupérer ses pixels à ce
moment-là — c'est le seul cas qui justifie un second échange.

Filtrer la liste présentée sur les pixels **jamais déclenchés**
(`last_fired_time` vide) pour qu'elle reste lisible : ce sont les seuls
candidats pour un nouveau produit.

Le portefeuille par défaut reste **BootiktiPremium**, mais le choix du compte
est le sien à chaque produit.

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

### Les comptes 01, 05 et 08 sont mis de côté

Hamza a tranché le 16/09/2026 : **on les laisse en dehors du pipeline**, les
14 comptes pilotables suffisent. Ne pas les reproposer, ne pas relancer le
sujet du MCP non déployé ni du compte désactivé. Ils restent listés ci-dessus
pour mémoire seulement.

Si un jour il en choisit un quand même : préparer tout ce qui peut l'être —
créatives, textes, ciblage, structure, budget — et le lui livrer pour création
manuelle dans le Gestionnaire. Ne pas tenter l'appel MCP, Meta le refuse.

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

## Paramètres fixes — décidés par Hamza le 16/09/2026

### Objectif — toujours le même

**Conversions, achat sur site web uniquement.**

| Réglage | Valeur |
|---|---|
| Objectif de campagne | Ventes / Conversions (`OUTCOME_SALES`) |
| Lieu de conversion | **Site web uniquement** — jamais l'app, jamais les messages, jamais les appels |
| Événement optimisé | **Achat** (`PURCHASE`) |
| Optimisation de l'ad set | `OFFSITE_CONVERSIONS` |
| `promoted_object` | le `pixel_id` choisi + `custom_event_type: PURCHASE` |

On **choisit le pixel** à chaque produit (Hamza en crée un par produit, voir la
section pixels).

### Ciblage — Algérie, le reste se demande

Pays : **Algérie**, systématiquement.

**Deux questions à poser à Hamza à chaque produit**, en même temps que le choix
du compte publicitaire :

1. **Audience** : `broad` · `hommes` · `femmes` ?
2. **Âge minimum 26 ans**, ou pas ?

Ne jamais décider seul, ne jamais reporter la réponse d'un produit précédent.

### Catalogue produit et automatismes — tout désactivé

Hamza le 16/09/2026 : **on désactive toutes les options de catalogue produit**
et, plus largement, tous les automatismes Meta qui reprennent la main sur la
créative ou le ciblage.

À décocher / ne pas activer :

- **Catalogue produit** et publicités dynamiques (DPA / Advantage+ catalogue) —
  on diffuse nos créatives, pas un flux produit
- **Advantage+ créative** : améliorations automatiques de l'image, recadrages,
  variantes de texte, musique, filtres
- **Advantage+ audience** / extension automatique de l'audience
- **Advantage+ placements** / extension automatique des placements
- Toute suggestion d'« opportunité » du Gestionnaire qui modifie créative,
  ciblage ou placement

La créative part telle qu'on l'a produite. C'est tout l'intérêt du travail de
la partie 2 : Meta ne doit pas la recadrer ni la réécrire.

### Le pixel — le MCP ne peut PAS en créer

**Limite dure, vérifiée :** aucun outil du MCP Meta ne crée un pixel ou un
dataset. La création passe uniquement par le **Gestionnaire d'événements** de
Meta, à la main.

Sur un pixel **existant**, le MCP permet en revanche : créer les règles
d'événement (Purchase, AddToCart, Lead…), ajouter les extracteurs de paramètres
(valeur, devise), activer / désactiver, lire la qualité du signal et le volume.

Ne jamais promettre de créer un pixel, ne jamais inventer un `pixel_id`.

#### La réserve de pixels du testing

Hamza crée **une dizaine de pixels d'avance** dans le Gestionnaire
d'événements, dédiés au pipeline Testing Amazon. À chaque nouveau produit, on
en consomme un.

Nommage recommandé : séquentiel et dédié — `TA 01` … `TA 10` — pour ne pas les
confondre avec ses pixels existants (`N Shoes`, pixels produit).

**Tableau de suivi — à tenir à jour à chaque produit :**

| Pixel | dataset_id | Produit affecté | Date |
|---|---|---|---|
| *(à remplir quand Hamza les aura créés)* | | | |

Pixels déjà disponibles, jamais déclenchés :

| Pixel | dataset_id |
|---|---|
| `PETS` | `1438622408245104` |
| `Hamza 1` | `858635596684170` |

#### Savoir quel pixel est libre — par ordre de fiabilité

1. **Le tableau de suivi ci-dessus.** Infaillible, ne dépend d'aucune API.
2. **`last_fired_time` vide** (`1969-12-31`) dans `ads_get_datasets` : le pixel
   n'a jamais reçu d'événement. Angle mort : un pixel déjà rattaché à une
   campagne qui n'a pas encore converti apparaît quand même comme libre.
3. **Lire le pixel déclaré par chaque ad set** via `ads_get_ad_entities` —
   **à vérifier**, c'était une question ouverte des notes du 14/09. Lecture
   seule, sans risque, à tester quand l'occasion se présente.

### Placements — manuels, Facebook et Instagram seulement

**Toujours en placements manuels.** On coche Facebook et Instagram, **on
décoche tout le reste** :

| Plateforme | |
|---|---|
| Facebook | ✅ |
| Instagram | ✅ |
| Audience Network | ❌ décoché |
| Messenger | ❌ décoché |
| Threads | ❌ décoché |

En API : `publisher_platforms: ["facebook", "instagram"]`, et ne pas laisser
`targeting_automation` élargir les placements.

**Meta propose régulièrement de consacrer 5 % du budget à tester d'autres
placements : on REFUSE, systématiquement.** Même chose pour toute variante de
cette proposition (extension automatique des placements, Advantage+
placements). Si l'API force une valeur par défaut qui l'active, la désactiver
explicitement.

### Structure de campagne

Décidée par Hamza le 16/09/2026. **Une campagne, deux ad sets, 20 ads.**

| Niveau | Contenu |
|---|---|
| Campagne | Objectif Conversions / Achat site web. **Le budget est au niveau de la campagne** |
| Ad set 1 | **1 ad au format flexible**, contenant les **10 créatives de type 1** |
| Ad set 2 | **1 ad au format flexible**, contenant les **10 créatives de type 2** |

**Format d'annonce : flexible.** Une seule ad par ad set, avec ses 10 visuels
dedans — pas 10 ads séparées. Meta fait tourner les visuels à l'intérieur de
l'ad. C'est la seule automatisation Meta qu'on garde activée ; toutes les
autres (Advantage+ créative, audience, placements, catalogue) restent coupées.

### L'ad set 3 — vidéo, sur demande

**Question posée dans le bloc initial** : **y a-t-il des vidéos ?**

S'il répond oui, ajouter un **3ᵉ ad set**, configuré exactement comme les deux
autres : même ciblage, mêmes placements, même pixel, même optimisation. Il
accueillera une ad flexible avec la ou les vidéos, qu'**Hamza ajoute lui-même**.

#### Contrainte technique — pas d'ad sans asset

Meta refuse de créer une ad sans creative, et un creative exige au moins une
image ou une vidéo. **Impossible de livrer « une ad flexible avec la créa
vide ».**

Contournement retenu — **option B**, choisie par Hamza le 16/09/2026 :

1. Créer l'**ad set 3** configuré à l'identique des deux autres
2. Y créer une **ad flexible complète** — texte, 3 titres, description, lien du
   funnel en URL du site **et** en lien d'affichage
3. Y mettre **une seule créative de type 1** en remplissage, uniquement pour
   que Meta accepte l'ad
4. Hamza remplace ensuite cette image par sa vidéo dans le Gestionnaire

**⚠️ À rappeler à Hamza à chaque livraison d'un ad set 3 :** l'image de
remplissage doit être remplacée par la vidéo. Si elle reste, une statique
tourne dans l'ad set censé tester la vidéo et le test ne veut plus rien dire.

Option A, écartée : livrer l'ad set sans ad du tout. Reste disponible s'il
change d'avis.

**Budget : au niveau de la campagne (CBO).** Meta répartit librement entre les
ad sets — c'est voulu, ça laisse l'algorithme arbitrer entre les types de
créative. Ne pas mettre de budget par ad set.

### Montant du budget — calculé, pas demandé

Règle d'Hamza du 16/09/2026, dérivée du prix de vente du produit :

| Prix de vente | Budget quotidien de campagne |
|---|---|
| **≤ 10 000 DZD** | **10 €** |
| **> 10 000 DZD** | **20 €** |

Le prix est déjà connu — Hamza le donne dans le bloc de questions initial.
Donc le budget se déduit, il ne se demande pas. L'annoncer quand même dans le
récapitulatif avant création.

### Nommage — décidé par Hamza le 16/09/2026

| Niveau | Nom |
|---|---|
| **Campagne** | **Le nom du produit**, tel quel |
| **Ad set 1** | `image 1` |
| **Ad set 2** | `image 2` |
| **Ad set 3** *(si vidéo)* | `video` |

Rien d'autre : pas de date, pas de code, pas de préfixe. Le nom du produit
suffit à identifier la campagne, et `image 1` / `image 2` / `video` à identifier
ce que chaque ad set teste.

Exemple, pour le vélo Dskeuzeew :

```
Campagne : Vélo d'appartement pliable Dskeuzeew 16 résistances
  ├── image 1   → 1 ad flexible, 10 créatives type 1
  ├── image 2   → 1 ad flexible, 10 créatives type 2
  └── video     → 1 ad flexible, 1 créative type 1 en remplissage
                  (Hamza remplace par sa vidéo)
```

### Description de l'annonce — l'angle qualité

Le champ description parle **toujours de la qualité premium des produits**.
C'est le seul endroit du dispositif où on parle qualité plutôt que prix — le
texte principal et les titres portent déjà le prix et la provenance.

Formulations possibles : « Des produits de qualité premium, sélectionnés en
Europe. » · « Qualité premium garantie sur toute notre sélection. » — sans
jamais promettre de garantie commerciale ni de SAV (règle 9).

### Texte de l'annonce — Testing Amazon

L'angle est **le prix**. Structure imposée du texte principal :

```
DESTOCKAGE ! [NOM DU PRODUIT] venu d'europe

[les détails les plus importants du produit]

Livraison disponible sur 69 wilayas
```

#### Variante avec le prix affiché — à demander

**Question 9 du bloc initial : afficher le prix dans le texte de l'annonce ?**
À poser à chaque produit, ne jamais décider seul.

Si oui, le prix passe **tout en haut, avant `DESTOCKAGE`** :

```
12 600 DA

DESTOCKAGE ! [NOM DU PRODUIT] venu d'europe

[les détails les plus importants du produit]

Livraison disponible sur 69 wilayas
```

**Attention à ne pas confondre les deux supports :**

| | Prix autorisé ? |
|---|---|
| **Texte de l'annonce** | ✅ si Hamza répond oui à la question 9 |
| **Créative (l'image)** | ❌ **jamais**, aucune exception — seul le `-30%` |

Le prix affiché est celui de la fiche LightFunnels, en DZD, jamais le prix
barré.

Les « détails les plus importants » suivent la même règle que les créatives :
**des options factuelles, pas des promesses.** Pour le vélo : 16 niveaux de
résistance, charge 150 kg, écran LCD, pliable.

### Les liens de l'annonce

**Le lien du funnel LightFunnels sert aux deux champs :**

| Champ | Valeur |
|---|---|
| URL du site web (lien d'achat) | le lien du funnel |
| **Lien d'affichage** | le même lien du funnel |

C'est Hamza qui fournit ce lien — voir le point d'arrêt ci-dessous.

### ⛔ POINT D'ARRÊT du pipeline — le funnel

Décidé le 16/09/2026. Le pipeline Testing Amazon **s'arrête juste après la
création du produit sur LightFunnels** et attend.

1. Parties 1 et 2 : scrape → images modifiées → fiche produit → créatives
2. **ARRÊT.** Hamza crée le funnel lui-même et donne son lien
3. Partie 3 : la campagne se construit avec ce lien

Le MCP LightFunnels ne peut de toute façon pas rattacher un produit à un funnel
existant, ni cloner un funnel (voir `REGLES-lightfunnels-meta.md`) : le funnel
est donc forcément fait à la main. Ne jamais lancer la partie 3 sans ce lien, et
ne jamais inventer d'URL de funnel.

### Titres — les 3, toujours les mêmes

| # | Titre |
|---|---|
| 1 | `Venu d'europe !` |
| 2 | `DESTOCKAGE 100% ORIGINAL !` |
| 3 | `100% ORIGINAL` |

Ces trois titres sont fixes pour tout le pipeline Testing Amazon, quel que soit
le produit.

## Reste à définir avec Hamza

- Règles de coupure : seuils, délais, métrique de décision

## Le nombre de wilayas — tranché

**« Livraison disponible sur 69 wilayas »**, confirmé par Hamza le 16/09/2026
après que le point lui ait été signalé (l'Algérie en compte 58 depuis 2019).
C'est sa décision, elle est actée : écrire 69. Ne pas rouvrir le sujet.

## Rappel de la règle 1

Rien ne se lance sur Meta sans annonce préalable et accord d'Hamza. Les
campagnes se créent en pause, et chaque niveau est validé avant activation.
Une campagne active engage du budget réel : c'est l'action la plus coûteuse
du projet en cas d'erreur.
