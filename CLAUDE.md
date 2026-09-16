# À LIRE AVANT TOUTE ACTION

Projet e-commerce COD Algérie — Hamza (NAELDEALS). Compte LightFunnels en **DZD**.

## Le pipeline « Testing Amazon »

Nom donné par Hamza le 16/09/2026. **Le pipeline commence au scraping et
s'arrête aux créatives prêtes à lancer.** Un lien Amazon en entrée, une fiche
LightFunnels et ses créatives en sortie.

| Partie | Objet | Règles |
|---|---|---|
| **1** | Import produit — scrape Apify, images modifiées, fiche LightFunnels | `docs/REGLES-pipeline-produit.md` |
| **2** | Créatives Facebook Ads — types 1 et 2, 10 par ad set | `docs/REGLES-creatives-meta.md` |
| **3** | Campagnes Meta Ads — **en cours de définition** | `docs/REGLES-ads-meta.md` |

Quand Hamza dit « on lance le testing Amazon » ou donne simplement un lien
Amazon, c'est de ce pipeline qu'il parle : scraping → créatives.

La **partie 3 (ads)** est un prolongement, pas une étape automatique du
testing : elle ne se lance jamais sans demande explicite.

**UN SEUL bloc de questions, juste après le scraping**, parties 1/2/3
confondues — pour limiter les allers-retours et les crédits. Hamza répond à
tout d'un coup, puis on enchaîne sans le relancer. Le bloc : mannequin · prix ·
prix barré · compte publicitaire · audience · âge 26+ · vidéos · pixel (liste
présentée en même temps, filtrée sur les pixels jamais déclenchés).

**Le budget ne se demande pas, il se calcule** depuis le prix de vente :
**≤ 10 000 DZD → 10 €/jour**, **> 10 000 DZD → 20 €/jour**, au niveau campagne.

**La description de l'annonce parle toujours de la qualité premium** des
produits — sans jamais promettre de garantie ni de SAV.

Détail des questions, jamais supposées ni reportées d'un produit précédent :

1. **Quel compte publicitaire** (liste dans `docs/REGLES-ads-meta.md`,
   portefeuille par défaut BootiktiPremium)
2. **L'audience** : broad · hommes · femmes
3. **Âge minimum 26 ans**, ou pas
4. **Y a-t-il des vidéos ?** Si oui → un **3ᵉ ad set** configuré à l'identique,
   avec une ad flexible complète (texte, titres, lien) et **une seule créative
   de type 1 en remplissage** pour que Meta accepte l'ad. Hamza remplace ensuite
   cette image par sa vidéo. **Le lui rappeler à chaque fois** : si l'image
   reste, le test vidéo ne veut rien dire.

Le reste est fixe : objectif **Conversions / Achat sur site web uniquement**,
pixel choisi par produit, ciblage **Algérie**, placements **manuels Facebook +
Instagram seulement** (Audience Network, Messenger et Threads décochés), et on
**refuse toujours** la proposition Meta de dépenser 5 % du budget pour tester
d'autres placements.

**Tout le catalogue produit et tous les automatismes Meta sont désactivés** :
DPA / Advantage+ catalogue, Advantage+ créative, Advantage+ audience,
Advantage+ placements. La créative part exactement telle qu'on l'a produite.

**Le MCP ne peut PAS créer de pixel** — Gestionnaire d'événements uniquement.
On pioche dans la réserve de pixels jamais déclenchés d'Hamza, ou il en crée un
et donne son ID. Ne jamais inventer un `pixel_id`.

**Structure** : une campagne, **budget au niveau campagne (CBO)**, deux ad
sets. Dans chaque ad set, **une seule ad au format flexible** contenant ses 10
créatives — type 1 sur l'ad set 1, type 2 sur l'ad set 2. Pas de budget par ad
set, pas d'ads séparées.

**Nommage** : campagne = **le nom du produit** · ad sets = `image 1` /
`image 2` / `video`. Rien d'autre, pas de date ni de code.

**⛔ Point d'arrêt** : le pipeline s'arrête après la création du produit sur
LightFunnels. Hamza crée le funnel et donne son lien. Ce lien va dans l'URL du
site web **et** dans le lien d'affichage. Ne jamais inventer d'URL de funnel,
ne jamais lancer la partie 3 sans ce lien.

**Texte de l'annonce** : `DESTOCKAGE ! [produit] venu d'europe` → les détails
factuels les plus importants → `Livraison disponible sur 69 wilayas`.
**Les 3 titres sont fixes** : `Venu d'europe !` · `DESTOCKAGE 100% ORIGINAL !` ·
`100% ORIGINAL`.

## Les 12 règles dures

1. **Ne lancer AUCUNE action sans l'annoncer et obtenir la validation d'Hamza.**
   Vaut pour tout ce qui **dépense** (Magnific, Apify), **écrit** (GitHub,
   LightFunnels, Drive) ou **part vers l'extérieur**. Règle posée après
   2 600 crédits perdus en générations non validées. Annoncer le coût estimé
   (`simulate_cost`, gratuit) avant, pas après.
   **Exception : l'import produit en mode « input / output »** (voir plus bas).
   Ses réponses au bloc de questions valent accord pour tout le pipeline — on
   enchaîne sans redemander, et on ne montre rien en cours de route.

2. **Ne jamais inventer un chiffre ou un contenu client.** Prix, prix barré,
   remise, avis, témoignage, note, spec, norme, certification : si ça ne vient
   pas d'Hamza ou de la source scrapée, ça ne va pas dans le produit. On demande.

3. **Question mannequin obligatoire à CHAQUE nouveau produit**, avant toute
   génération. Jamais de report de la décision d'un produit précédent.
   Quatre options : **A** homme · **B** femme en tenue couvrante · **C** tel
   quel · **D** **avatar humain** (silhouette humanoïde bleue translucide et
   lumineuse, sans visage ni genre — pour les images trop dénudées à simplement
   rhabiller). Détail : `docs/REGLES-pipeline-produit.md`.

4. **Prix produit uniquement par défaut.** Pas de `compare_at_price`, et
   **`notice_text` (Special offer) reste TOUJOURS vide**, sur tous les produits.
   Prix barré et offres seulement si Hamza les demande explicitement.

5. **Français par défaut** pour tout contenu produit, créa et traduction.
   Ne pas redemander. Autre langue seulement si demandée.

6. **Tout poids converti de LBS en kg est arrondi au multiple de 10 le plus
   proche**, sans décimale. 199 kg → **200 kg**. 111,8 kg → **110 kg**.
   S'applique aux images, au titre, à la description, aux features et à la FAQ.
   Les dimensions en cm gardent leur valeur exacte.

7. **Toujours les images principales du lien donné** (`highResolutionImages`),
   et elles seules. Même si le produit existe en plusieurs coloris, on ne
   récupère pas les autres variantes et **on ne les propose pas**. Le lien
   fourni définit le produit.

8. **Jamais d'avis client, de témoignage ou de note.** Hamza n'en demande pas.
   Les champs `reviews` et `testimonials` restent vides, et on n'en parle pas
   dans le compte rendu.

9. **Nettoyage de la description — à retirer systématiquement :**
   - toute mention de **garantie** (garantie X ans, satisfait ou remboursé,
     remboursement, retour gratuit)
   - toute mention de **SAV** / service client / assistance après-vente
   - le mot **Noël** et toute référence saisonnière (Noël, fêtes, cadeau de
     Noël, Black Friday…)

   Vaut pour la description, le titre, les features et la FAQ. Ces éléments
   viennent du vendeur d'origine et n'engagent pas Hamza — on ne les reprend
   jamais.

10. **La description est RÉÉCRITE, jamais traduite mot à mot.** La copie
    marketplace est écrite pour le référencement Amazon : phrases à rallonge,
    mots-clés empilés, répétitions. On en extrait les faits, puis on écrit un
    texte neuf : phrases courtes, un bénéfice par paragraphe, un ton direct qui
    parle au client. Aucune phrase ne doit pouvoir être retracée telle quelle
    jusqu'à la source. Les specs (dimensions, poids, vitesses) restent
    exactes — on réécrit la forme, jamais les chiffres.

11. **Un emoji au début de chaque grand titre** de la description.
    Un seul emoji, en rapport avec le sujet, suivi d'une espace.
    Pas d'emoji dans le titre du produit.

12. **Titre produit : court et clair.** Marque + type de produit + un seul
    argument clé, rien de plus. Viser **50 à 70 caractères**, jamais plus.
    Ne pas empiler les specs : elles vont dans la description.
    - ✅ `Tapis de marche pliable Lysole 12 km/h`
    - ✅ `Appareil abdominaux GoDyna pliable`
    - ❌ `Appareil abdominaux GoDyna pliable & réglable inclinaison et hauteur
      & roulettes silencieuses`
    - ❌ `Montre connectée GedFong NOIR Double bracelet, écran 1,43", appels
      WhatsApp, moniteur SpO2/sommeil, étanche IP67, plus de 107 modes...`

## Format de la fiche produit

Repris du format d'Hamza (fiches SPERAX / Kiddoza), corrigé de ses défauts :

- **Titre** : court et clair (règle 12)
- **SKU** : lisible en clair, pas un code — `abdo godyna rose`
- **Description** : **HTML brut, jamais échappé** (une balise encodée
  s'affiche en texte sur la fiche). Structure = liste à puces `<ul><li>`, où
  chaque puce est `emoji 【Titre】 description réécrite`
- **features / testimonials / faq** : **laissés vides** — Hamza ne les utilise
  pas, tout passe par la description
- **`notice_text`** : toujours vide

## Avant d'agir, lire

- **`docs/REGLES-pipeline-produit.md`** — pipeline images Amazon → Magnific,
  règles de traduction et de conversion d'unités, règle du mannequin,
  grille de coût `gpt-2` (réglage retenu : **1k / low = 30 crédits**).
- **`docs/REGLES-lightfunnels-meta.md`** — ce que le MCP LightFunnels permet
  et ne permet pas, contraintes LFSolid, mapping du formulaire COD, Meta Ads.
- **`docs/REGLES-creatives-meta.md`** — **partie 2 du pipeline** : cahier des
  charges des créatives Facebook Ads, type 1 « sans angle », ce qui figure et
  ne figure JAMAIS sur une créative.

## Testing Amazon, partie 1 — import produit, mode « input / output »

Hamza donne un lien, répond à **un seul bloc de questions**, et reçoit le lien
du produit LightFunnels. **Rien ne lui est montré entre les deux** : ni les
images scrapées, ni les images modifiées. Ne pas lui demander de choisir des
images, ne pas lui demander de les relire.

1. Scraper (Apify `junglee/Amazon-crawler`, ~0,006 $). Si `preview_product`
   renvoie « Product not found », c'est souvent une fiche en rupture — passer
   directement par Apify.
2. **Poser le bloc de questions, une seule fois** : la question mannequin
   **et** le prix de vente (plus le prix barré seulement s'il en veut un).
   Rien d'autre.
3. Importer les images dans Magnific (`creations_upload_image`, gratuit)
4. Modifier **toutes** les images (`images_generate`, `gpt-2`,
   **1k / low = 30 crédits**), un prompt conditionnel par image : le modèle lit
   l'image lui-même et ne corrige que ce qui doit l'être.
5. Traduire titre, description, features et FAQ en français
6. Créer le produit sur LightFunnels **avec les URLs des images modifiées**
   (les liens signés `pikaso.cdnpk.net` sont joignables par leur serveur)
7. Rendre le lien du produit, le récapitulatif et le coût. Rien d'autre.

Ne jamais créer le produit avec les images brutes. `update_product` ne gère pas
les images : pour les changer, recréer la fiche — et créer la nouvelle **avant**
de supprimer l'ancienne.

## Testing Amazon, partie 2 — créatives Facebook Ads

Détail complet : `docs/REGLES-creatives-meta.md`. L'essentiel :

- **Angle des produits Amazon** : le prix et la provenance. Sur l'image ils ne
  se traduisent QUE par le badge **-30%**, la mention **DÉSTOCKAGE** et le
  **petit drapeau allemand en haut à gauche** — jamais par un prix, jamais par
  un texte d'origine.
- **`-30%` et `DÉSTOCKAGE` sont sur TOUTES les créatives**, sans exception.
  `DÉSTOCKAGE` n'est pas un badge séparé : c'est le **premier mot du titre** —
  `DÉSTOCKAGE VÉLO D'APPARTEMENT PLIABLE`.
- **Type 1 « sans angle »** : une image propre à fort CTR. Drapeau, titre,
  badge -30%, colonne d'icônes avec les options chiffrées, produit en grand,
  bandeau bas.
- **Type 2 « bandeau jaune »** : bande jaune pleine largeur en haut à texte
  noir (`DESTOCKAGE` + produit + **`VENU D'EUROPE`**), drapeau allemand en haut
  à gauche, **fond blanc uni**, produit détouré en grand, et **seulement deux
  ou trois mentions essentielles** — rien d'autre.
- **`VENU D'EUROPE` est autorisé sur le type 2 uniquement** (la marchandise
  part bien d'Europe). Sur le type 1, drapeau seul, aucun texte de provenance.
  Jamais de « Made in Germany » ni de « qualité allemande » sur aucun type :
  « venu d'Europe » décrit l'expédition, pas la fabrication.
- **Ratio : 1:1 carré, 1k** (décision du 16/09/2026, provisoire). Le format
  1080 × 1920 à bandes vides ne s'applique PAS aux types 1 et 2.
- **Quantité : 10 créatives par ad set**, une fois les types validés.
- **Jamais sur une créative** : prix (même barré), garantie, SAV, promesse ou
  allégation de résultat, texte de provenance, référence saisonnière.
- **Des options, pas des bénéfices.** « 16 niveaux de résistance », « charge
  150 kg », « écran LCD » — pas « brûlez plus de calories ». Si ce n'est pas
  vérifiable sur la fiche technique, ça ne monte pas sur l'image.
- L'exception « input / output » de la partie 1 ne couvre **pas** les
  créatives : la règle 1 s'applique, on annonce le coût et on attend l'accord.

## Créas publicitaires Meta — format validé

Canvas **1080 × 1920 (9:16)** :

| Zone | Pixels | % |
|---|---|---|
| Barre haut | 1080 × 285 | 14,84 % |
| Créa centrale | 1080 × 1350 (4:5) | 70,31 % |
| Barre bas | 1080 × 285 | 14,84 % |

- Les barres font **partie de l'image générée**, restent **vides**, et leur
  couleur reprend la dominante de la créa.
- Les modèles **ignorent les pourcentages**. Ce qui marche : le mot
  « letterbox », un ancrage physique (« aussi haute que le produit »), et
  répéter que les bandes ne contiennent rien.
- Les textes sur l'image s'adaptent au **style** de la créa (JSON pro,
  pattern interrupt, UGC, réaliste…). Pas de formule unique.
- **Jamais de faux bouton play** ni d'élément d'interface simulé : rejet Meta
  (Nonfunctional / Misleading Buttons). Les flèches et les cercles, eux,
  sont autorisés.

## Contrainte réseau connue

Le sandbox ne peut joindre **ni** `m.media-amazon.com`, `pikaso.cdnpk.net`,
`api.apify.com`, **ni** `bootiktipremium.online` (403 au CONNECT). Aucune image
ne transite par la machine : tout se fait de serveur à serveur, Claude ne
manipule que des URLs et des identifiants. Ne jamais tenter de rapatrier une
image en base64.

Corollaire : **Claude ne voit pas les images**. Il ne peut donc pas juger un
rendu ni cibler une zone de texte sans qu'Hamza le lui décrive, ou sans passer
l'image en référence à `gpt-2`, qui la lit lui-même.
