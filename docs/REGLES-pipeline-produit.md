# Règles du pipeline produit — images Amazon → landing page COD

> Cahier des charges validé avec Hamza (NAELDEALS). À lire **avant** toute
> génération d'image. Chaque règle ici a été payée en crédits Magnific : les
> respecter évite de refaire des générations à 650 crédits l'unité.

## Le pipeline

1. **Scraping** — Apify, acteur `junglee/Amazon-crawler`, avec l'URL produit
   (ou juste l'ASIN). Coût ~0,006 $. Récupérer le champ `highResolutionImages`
   (galerie principale en 1500px) et `title`.
2. **Import Magnific** — `creations_upload_image` avec l'URL publique Amazon.
   Magnific va chercher l'image lui-même, côté serveur. Gratuit.
3. **Validation** — afficher les originales à Hamza (`creations_show`) et lui
   faire choisir les images à traiter, **avant** de dépenser quoi que ce soit.
4. **Modification** — `images_generate`, modèle `gpt-2`, l'image d'origine en
   référence. 650 crédits par image en 2k/qualité haute.
5. **Relecture** — Hamza valide image par image, texte compris.

## Règles de modification

| Règle | Détail |
|---|---|
| Traduction | Tout texte anglais → français, même police, taille, couleur, position |
| Unités | LBS → kg, inch → cm, valeur recalculée (1 lb = 0,4536 kg / 1 in = 2,54 cm) |
| Marques | Jamais traduites ni déformées, reproduites à l'identique |
| Orthographe | Chaque caractère vérifié. « kg » et « cm » exactement |
| Rien à corriger | Si ni texte anglais, ni unité impériale, ni mannequin à changer → **on ne touche pas à l'image**, on garde l'originale (0 crédit) |
| Le reste | Cadrage, composition, fond, forme et couleurs du produit, lumière : strictement identiques |

## Règle du mannequin femme — OBLIGATOIRE

**À chaque nouveau produit, demander à Hamza avant toute génération.**
Jamais de report automatique de la décision d'un produit précédent.

Les trois options, dans cet ordre :

1. **Remplacer par un homme**
2. **Garder la femme mais tenue plus couvrante** (manches longues, pantalon ample)
3. **Garder tel quel** — traduction du texte uniquement

Si l'option 1 est choisie :

- **Chaque** femme adulte de l'image devient un homme, **un pour un**
  (deux femmes → deux hommes)
- Chaque homme garde la pose, la position, l'échelle et le cadrage exacts
  de la femme qu'il remplace
- **Tenue jamais moulante** : vêtements amples, décents, adaptés au contexte
  de la scène (fitness → t-shirt ample + pantalon de survêtement)

**Exception absolue : les bébés et les enfants ne sont jamais modifiés**,
quel que soit leur sexe.

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
- Affichage : gratuit
- Génération `gpt-2` 2k qualité haute : **650 crédits** par image
- Génération `gpt-2` 1k qualité moyenne : 100 crédits par image
