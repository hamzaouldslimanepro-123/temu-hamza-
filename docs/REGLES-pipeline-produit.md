# Règles du pipeline produit — images Amazon → landing page COD

> Cahier des charges validé avec Hamza (NAELDEALS). À lire **avant** toute
> génération d'image. Chaque règle ici a été payée en crédits Magnific : les
> respecter évite de refaire des générations à 650 crédits l'unité.

## Le pipeline — mode « input / output »

> Flux validé avec Hamza le 15/09/2026. Il donne un lien, répond à un seul
> bloc de questions, et reçoit le lien du produit LightFunnels. **Rien ne lui
> est montré entre les deux** : ni les images scrapées, ni les images
> modifiées. Ne pas lui demander de choisir des images. Ne pas lui demander de
> relire les images. Ne rien afficher qu'il n'a pas demandé.

1. **Scraping** — Apify, acteur `junglee/Amazon-crawler`, avec l'URL produit
   (ou juste l'ASIN). Coût ~0,006 $. Récupérer `highResolutionImages`
   (galerie principale en 1500px), `title`, `features`, `attributes`.
   LightFunnels `preview_product` échoue sur une fiche en rupture de stock
   (« Product not found ») — passer directement par Apify dans ce cas.
2. **Le bloc de questions — une seule fois, avant d'agir.** Poser ensemble :
   - la **question mannequin** (voir plus bas), obligatoire à chaque produit
   - le **prix de vente**, et le prix barré **seulement s'il en veut un**
   Ne jamais deviner ni déduire un prix. Ne pas poser d'autre question.
3. **Import Magnific** — `creations_upload_image` avec l'URL publique Amazon.
   Magnific va chercher l'image lui-même, côté serveur. Gratuit.
4. **Modification de TOUTES les images** — `images_generate`, modèle `gpt-2`,
   l'image d'origine en référence, **1k / qualité low = 30 crédits**.
   Un seul prompt conditionnel par image : le modèle lit l'image lui-même et
   ne corrige que ce qui doit l'être (Claude ne voit pas les images, il ne peut
   donc pas trier en amont — d'où le traitement systématique des 7 ou 8).
5. **Traduction** du titre, de la description, des features et de la FAQ en
   français, à partir des données scrapées.
6. **Création du produit** sur LightFunnels avec les **URLs des images
   modifiées** (les liens signés `pikaso.cdnpk.net` sont bien joignables par
   le serveur LightFunnels — vérifié le 15/09/2026).
7. **Sortie** : le lien du produit, le récapitulatif, le coût en crédits.
   Rien d'autre.

`update_product` **ne gère pas les images** : pour changer les visuels d'un
produit existant, il faut le recréer. Créer la nouvelle fiche **avant** de
supprimer l'ancienne, au cas où l'import d'images échoue.

## Règles de modification

| Règle | Détail |
|---|---|
| Traduction | Tout texte anglais → français, même police, taille, couleur, position |
| Unités | LBS → kg, inch → cm, valeur recalculée (1 lb = 0,4536 kg / 1 in = 2,54 cm) |
| **Arrondi des poids** | Un poids converti en kg est **toujours arrondi au multiple de 10 le plus proche**. 199 kg → **200 kg**. 111,8 kg → **110 kg**. 264 lb = 119,75 kg → **120 kg**. Jamais de décimale sur un poids. |
| Marques | Jamais traduites ni déformées, reproduites à l'identique |
| Orthographe | Chaque caractère vérifié. « kg » et « cm » exactement |
| Rien à corriger | Si ni texte anglais, ni unité impériale, ni mannequin à changer → **on ne touche pas à l'image**, on garde l'originale (0 crédit) |
| **Coloris** | On prend **uniquement les images principales du lien donné** (`highResolutionImages`). Les autres variantes de couleur (`variantDetails`) sont ignorées et **ne sont pas proposées** — le lien définit le produit |
| **Avis clients** | **Jamais.** `reviews` et `testimonials` restent vides. Ne pas les scraper, ne pas les importer, ne pas en parler dans le compte rendu |
| **Garantie / SAV** | **Retirés systématiquement** de la description, du titre, des features et de la FAQ : garantie X ans, satisfait ou remboursé, retour gratuit, SAV, service client, assistance après-vente. Ce sont les engagements du vendeur d'origine, pas ceux d'Hamza |
| **Saisonnier** | Le mot **Noël** et toute référence saisonnière (fêtes, cadeau de Noël, Black Friday…) sont retirés |
| **Description réécrite** | **Jamais de traduction mot à mot.** On extrait les faits de la copie Amazon, puis on écrit un texte neuf : phrases courtes, un bénéfice par paragraphe, ton direct. Aucune phrase retraçable jusqu'à la source. Les chiffres et specs restent exacts |
| **Emoji de titre** | **Un emoji au début de chaque grand titre `<h3>`** de la description, en rapport avec le paragraphe, suivi d'une espace. Pas d'emoji dans le titre produit, les features ou la FAQ |
| Le reste | Cadrage, composition, fond, forme et couleurs du produit, lumière : strictement identiques |

## Arrondi des poids convertis — OBLIGATOIRE

Tout poids converti de LBS vers kg est **arrondi au multiple de 10 le plus
proche**, sans décimale. Règle posée par Hamza le 15/09/2026 : un chiffre rond
est plus lisible et plus crédible sur une fiche produit qu'une conversion
mécanique à la virgule.

| Valeur convertie | À écrire |
|---|---|
| 199 kg | **200 kg** |
| 111,8 kg | **110 kg** |
| 119,75 kg (264 lb) | **120 kg** |
| 99,8 kg (220 lb) | **100 kg** |
| 45,4 kg (100 lb) | **50 kg** |

S'applique partout : images modifiées, titre, description, features, FAQ.
Les dimensions en cm gardent leur valeur exacte — la règle ne concerne que
les poids.

## Règle du mannequin femme — OBLIGATOIRE

**À chaque nouveau produit, demander à Hamza avant toute génération**, dans
le bloc de questions de l'étape 2, en même temps que le prix.
Jamais de report automatique de la décision d'un produit précédent.

Les quatre options, dans cet ordre :

1. **Remplacer par un homme**
2. **Garder la femme mais tenue plus couvrante** (manches longues, pantalon ample)
3. **Garder tel quel** — traduction du texte uniquement
4. **Transformer en avatar humain** — ni homme ni femme, juste la forme humaine

Si l'option 1 est choisie :

- **Chaque** femme adulte de l'image devient un homme, **un pour un**
  (deux femmes → deux hommes)
- Chaque homme garde la pose, la position, l'échelle et le cadrage exacts
  de la femme qu'il remplace
- **Tenue jamais moulante** : vêtements amples, décents, adaptés au contexte
  de la scène (fitness → t-shirt ample + pantalon de survêtement)

**Exception absolue : les bébés et les enfants ne sont jamais modifiés**,
quel que soit leur sexe.

### Option 4 — l'avatar humain

À utiliser quand la personne est trop dénudée pour être simplement rhabillée :
demi-corps en sous-vêtements, gros plan sur une zone du corps, avant/après
silhouette. Plutôt que d'habiller ou de changer le sexe, on remplace la
personne par une **silhouette humanoïde neutre**.

Le style, tel que validé par Hamza (référence : la landing page YAMO) :

> Silhouette humaine en 3D, **translucide et lumineuse, bleu électrique**,
> parcourue de **points de lumière** répartis sur tout le corps. Surface lisse
> et uniforme, **sans visage, sans cheveux, sans vêtement**, aucun marqueur de
> genre — ni poitrine, ni hanches marquées, ni pilosité. Effet hologramme
> anatomique sur fond réel.

Contraintes identiques aux autres options :

- La silhouette garde **exactement** la pose, la position, l'échelle et le
  cadrage de la personne remplacée
- Le produit, le décor, la lumière et le texte restent inchangés
- **Bébés et enfants ne sont jamais transformés**, avatar compris

## Contraintes techniques connues

- Le sandbox Claude **ne peut pas** joindre `m.media-amazon.com`,
  `pikaso.cdnpk.net` ni `api.apify.com` (politique d'egress, 403 au CONNECT).
  Aucune image ne peut transiter par la machine. Tout doit se faire de
  serveur à serveur — Claude ne manipule que des URLs et des identifiants.
- Ne **jamais** rapatrier une image en base64 dans la conversation : ~130 000
  tokens pour une image HD, ~10 000 pour une vignette. Inutile de toute façon,
  puisque `gpt-2` lit l'image lui-même quand on la lui passe en référence.
- `gpt-2` ne retouche pas les pixels : il **redessine** l'image entière. Les
  fautes de frappe dans le texte sont donc possibles à chaque génération
  (vu en vrai : « BG » au lieu de « kg »). D'où la relecture systématique.
- Pour un texte vraiment 1:1 sans redessiner le produit, l'alternative est
  `images_retouch` avec un masque sur la zone de texte.
- Hamza voit bien les images via `creations_show` et ouvre bien les liens
  `magnific.com` — pas besoin de passer par Google Drive pour valider.

## Repères de coût

- Scraping Apify : ~0,006 $ par produit
- Import Magnific : gratuit
- Affichage (`creations_show`) : gratuit
- Simulation de coût (`simulate_cost`) : gratuit, à utiliser avant toute série

### Grille de coût `gpt-2` (vérifiée, exacte)

| Résolution | Qualité | Crédits / image |
|---|---|---|
| 2k | haute | 650 |
| 1k | haute | 325 |
| 2k | moyenne | 200 |
| 1k | moyenne | 100 |
| **1k** | **low** | **30 ← réglage retenu** |

C'est la **qualité** qui pilote le coût, pas la résolution : 2k/moyenne (200)
revient moins cher que 1k/haute (325).

**Attention** : la qualité pilote aussi la finesse du rendu du texte, et le
texte est notre point critique (traductions, conversions d'unités). Une
coquille a déjà été observée en qualité haute (« BG » au lieu de « kg »).
En qualité low, relire le texte avec d'autant plus d'attention. Si les
coquilles se multiplient, repasser en qualité moyenne — puis haute —
uniquement sur les images chargées en texte.
