# Testing Amazon, partie 3 — campagnes Meta Ads

> **En cours de définition.** Hamza donne ses instructions le 16/09/2026.
> Ne rien lancer sur Meta avant que ce fichier soit complet et validé.

La partie 3 démarre une fois la fiche produit créée (partie 1) et les
créatives produites (partie 2). Elle **ne fait pas partie du testing
automatique** : elle ne se lance que sur demande explicite d'Hamza.

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
