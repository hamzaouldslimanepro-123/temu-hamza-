# LightFunnels & Meta Ads — ce qui marche, ce qui ne marche pas

> Appris en séance avec Hamza le 14/09/2026, au prix d'essais-erreurs.
> À lire avant toute action sur LightFunnels ou Meta. Complément du fichier
> `REGLES-pipeline-produit.md` (pipeline images Amazon → Magnific).

## Règles de travail imposées par Hamza

1. **Ne lancer AUCUNE action sans l'annoncer et obtenir sa validation.**
   Vaut pour tout ce qui dépense (Magnific, Apify), écrit (GitHub, LightFunnels,
   Drive) ou part vers l'extérieur. Il a posé cette règle après que des
   générations aient été lancées sans son accord — 2 600 crédits perdus.
2. **Le champ « Special offer » (`notice_text`) reste toujours vide.**
   Sur tous les produits, sans exception.
3. **Question mannequin obligatoire à chaque nouveau produit** (voir l'autre fichier).

---

## LightFunnels

### Ce que le MCP permet

| Domaine | Outils |
|---|---|
| Produits | `create_product`, `update_product`, `get_product`, `list_products`, `preview_product` |
| Tunnels | `create_funnel`, `list_funnels`, `get_funnel_pages`, `update_funnel_page` |
| Pages | `build_component`, `lint_page`, `design_brief`, `lfsolid_docs` |
| Données | `analytics` |

**Les images s'importent par URL** (`image_urls`, max 20, la première devient
l'image principale). LightFunnels va les chercher côté serveur — transfert
direct depuis Magnific, gratuit, aucun octet dans la conversation.

### Ce que le MCP ne permet PAS

- **Cloner un tunnel** — aucun outil. Duplication à faire dans l'interface.
- **Rattacher un produit à un tunnel existant** — le lien se fait uniquement
  à la création, via le `product_id` requis de `create_funnel`.
- **Réglages du tunnel** : passerelle de paiement (COD), pixels, groupes de
  livraison (« Algérie »). Tout ça reste dans l'interface.
- **Lire une page construite dans le builder** — `get_funnel_pages` renvoie
  « NOT EDITABLE — no generated markup ». Seules les pages générées via le MCP
  sont lisibles. **Ne jamais lancer `update_funnel_page` sur une page du
  builder : ça écraserait le travail d'Hamza sans retour possible.**

### Contraintes LFSolid (vérifiées en production)

- **Aucun JavaScript** n'est accepté sur une page boutique. Même l'exemple
  officiel de leur propre documentation est refusé. Galeries et interactions
  doivent être en CSS pur (scroll-snap + ancres `<a href="#id">`).
- **`scroll-behavior` en CSS est bloqué** — le filtre cherche
  « behavior / expression / binding » et assimile ça à du script.
- **La règle cardinale** : « Une page produit LightFunnels est un tunnel à
  produit unique et checkout unique. Le seul chemin possible pour le client est
  l'étape de commande. » Il n'existe **aucune action pour créer une commande**
  depuis du markup personnalisé.
- **Le HTML personnalisé peut collecter** (via `data-lf-input`) **mais pas
  soumettre.** Le bouton qui valide réellement la commande est un composant
  natif, à déposer dans le builder.
  → **Piège mortel** : un bouton qui redirige vers la page de remerciement
  fait croire au client que sa commande est passée alors que rien n'est
  enregistré.
- **La page générée est UN SEUL bloc** dans le builder. Impossible d'insérer
  un composant natif au milieu — seulement avant ou après l'ensemble.
- Fragment HTML uniquement (pas de `<html>`/`<head>`/`<body>`), tout enveloppé
  dans une classe racine unique, CSS préfixé.

### Syntaxe LFSolid utile

```
data-lf-bind="product.title"              texte
data-lf-bind-html="product.description"   HTML (7 champs de confiance seulement)
data-lf-bind-src="product.images.0"       image
data-lf-bind-href="..."                   lien
data-lf-repeat="product.features"         répéteur, puis $item.title / $item.description
data-lf-if="product.compare_at_price"     affichage conditionnel
data-lf-filter="currency"                 OBLIGATOIRE sur tout prix
data-lf-action="redirect" data-lf-page="checkout"
data-lf-action="increment-quantity" / "decrement-quantity"
data-lf-input="checkout.first_name"       champ de formulaire
```

Répéteurs disponibles : `product.features`, `product.testimonials`,
`product.faq` (singulier), `product.reviews`, `product.variants`,
`product.price_bundles`, `product.options`.

### Mapping du formulaire COD d'Hamza

| Champ affiché | Type LightFunnels | Chemin LFSolid | Colonne à l'export |
|---|---|---|---|
| Nom | First name | `checkout.first_name` | first_name |
| Wilaya {الولاية} | Shipping address state | `checkout.shipping_address.state` | state |
| Municipalité | Shipping address city | `checkout.shipping_address.city` | city |
| Numéro de téléphone | Phone | `checkout.phone` | phone |

Le mapping compte : à l'export Excel des commandes, chaque colonne porte le nom
de sa balise. Un mauvais mapping = du renommage manuel à chaque livraison.

Réglages : téléphone sans formatage automatique ni indicatif pays. Tous les
champs obligatoires. Pas de champ « nom de famille » séparé.

### Structure du gabarit d'Hamza (« Funnel de base 2.0 »)

Page produit nommée **« Product page - COD Checkout »** — le formulaire est
intégré à la page produit, pas sur une étape séparée. Ordre mobile :

1. Titre
2. Galerie (grande image + miniatures)
3. Prix + prix barré
4. Quantité
5. **Bloc de commande COD natif** (Nom / Wilaya / Municipalité / Téléphone,
   récapitulatif, bouton noir, choix Standard / Express)
6. Description produit
7. Bandeau de réassurance — 4 icônes violettes
8. Barre fixe en bas d'écran

Le tunnel a aussi 4 pages légales (Privacy, Refund, Terms, Contact) que
`create_funnel` ne crée pas.

**Les frais de livraison n'apparaissent qu'une fois la wilaya choisie** — les
montants visibles dans l'éditeur sont des valeurs de démonstration, ce n'est
pas un bug.

### Ce qui a été créé (test PASYOU Balance Board)

- Produit : `prod_VCcE-e5B8LPSPnUGSTHKE` — 12 600 DZD, barré 18 600, 9 images
- Tunnel de test : `fun_K360sX6zTZGV7_8n_oAEA` (non publié)
  - page produit : `step_zEsQaC1R5PkqVe_oIwdSp`
  - checkout : `step_Y9nh2ptwqRTyFPEo_BMo1`
  - remerciement : `step_itscmTR70HqzPaDiaK1WI`
- Gabarit d'Hamza (NE PAS TOUCHER) : `fun_8JgJQeFg7Vniw2Amtw1rd`
- Second gabarit : « Funnel avec Variante » `fun_gjhothvtt3MPiws5eOBr3`

Compte en **DZD** — confirmé, un prix de 12 600 s'affiche bien 12 600 DZD.

---

## Meta Ads

### Possible

- **Campagnes complètes** : `ads_create_campaign` → `ads_create_ad_set`
  (ciblage, budget, **et sélection du pixel**) → `ads_creative_upload_image` →
  `ads_create_creative` → `ads_create_ad`
- **Sur un pixel existant** : créer des règles d'événement (Purchase, AddToCart,
  Lead…), ajouter les extracteurs de paramètres (valeur, devise), activer ou
  désactiver, lire la qualité du signal et le volume
- **Audiences** : site web, retargeting, lookalikes
- Les campagnes se créent en pause — faire valider chaque niveau avant activation

### Impossible

- **Créer un nouveau pixel / dataset** — se fait dans le Gestionnaire
  d'événements de Meta uniquement

### À vérifier la prochaine fois

Hamza veut créer ~100 pixels d'avance et demander lequel n'est sur aucune
campagne active. Le listage des pixels est certain ; reste à vérifier que
`ads_get_ad_entities` renvoie bien le pixel déclaré par chaque ensemble de
publicités. Sinon, repli sur les pixels sans activité
(`last_fired_time` vide).

---

## Contraintes réseau

Le sandbox ne peut joindre **ni** `m.media-amazon.com`, `pikaso.cdnpk.net`,
`api.apify.com`, **ni le domaine boutique d'Hamza**
(`bootiktipremium.online` → 403 au CONNECT). Impossible d'analyser une page
en ligne localement : il faut passer par Apify, et tout le contenu arrive
alors dans la conversation.
