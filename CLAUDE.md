# À LIRE AVANT TOUTE ACTION

Projet e-commerce COD Algérie — Hamza (NAELDEALS). Compte LightFunnels en **DZD**.

## Les 6 règles dures

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
   Détail des 3 options : `docs/REGLES-pipeline-produit.md`.

4. **Prix produit uniquement par défaut.** Pas de `compare_at_price`, et
   **`notice_text` (Special offer) reste TOUJOURS vide**, sur tous les produits.
   Prix barré et offres seulement si Hamza les demande explicitement.

5. **Français par défaut** pour tout contenu produit, créa et traduction.
   Ne pas redemander. Autre langue seulement si demandée.

6. **Tout poids converti de LBS en kg est arrondi au multiple de 10 le plus
   proche**, sans décimale. 199 kg → **200 kg**. 111,8 kg → **110 kg**.
   S'applique aux images, au titre, à la description, aux features et à la FAQ.
   Les dimensions en cm gardent leur valeur exacte.

## Avant d'agir, lire

- **`docs/REGLES-pipeline-produit.md`** — pipeline images Amazon → Magnific,
  règles de traduction et de conversion d'unités, règle du mannequin,
  grille de coût `gpt-2` (réglage retenu : **1k / low = 30 crédits**).
- **`docs/REGLES-lightfunnels-meta.md`** — ce que le MCP LightFunnels permet
  et ne permet pas, contraintes LFSolid, mapping du formulaire COD, Meta Ads.

## Pipeline import produit — mode « input / output »

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
