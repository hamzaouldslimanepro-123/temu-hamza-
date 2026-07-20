# Temu Image Scraper

Extrait uniquement les images **produit** (galerie) et **description** d'une
page produit Temu — pas toutes les images de la page (bannières, pub, UI...).

## Comment ça marche

Les pages produit Temu sont rendues côté serveur : toutes les données du
produit (images, prix, variantes, description...) sont embarquées dans un
seul bloc JSON assigné à `window.rawData = {...};` dans la page HTML. Le
script extrait ce JSON et ne garde que :

- **Galerie produit** : `store.goods.gallery`, en ne gardant que les entrées
  `type == 1` (les entrées `type == -1` sont de petites vignettes de
  couleur/variante, pas de vraies photos produit).
- **Images de description** : `store.productDetailFlatList` (avec repli sur
  `store.productDetail.floorList[].items[]` si la liste est vide).

## Récupérer le HTML d'une page produit

Ce script ne va pas chercher la page lui-même : Temu bloque le scraping
automatisé côté serveur pour beaucoup de réseaux. Il faut donc récupérer le
HTML manuellement :

1. Ouvre la page produit Temu dans ton navigateur.
2. `Ctrl+U` (ou clic droit → "Afficher le code source de la page").
3. `Ctrl+A` puis `Ctrl+C` pour tout copier.
4. Colle le contenu dans un fichier, ex. `page.html`.

## Utilisation

```bash
# Afficher les URLs trouvées + écrire un manifest.json
python3 temu_scraper.py page.html

# Télécharger aussi les images dans un dossier organisé par produit
python3 temu_scraper.py page.html --download

# Choisir le dossier de sortie (par défaut: scraped_products/)
python3 temu_scraper.py page.html --download -o mon_dossier
```

Résultat :

```
scraped_products/
  <nom-du-produit-slugifie>/
    manifest.json        # nom produit + toutes les URLs
    gallery/              # images produit (si --download)
    description/          # images de description (si --download)
```

Le `manifest.json` est toujours écrit, même sans `--download` : il liste le
nom du produit et toutes les URLs d'images trouvées, utile si le
téléchargement direct est bloqué par ton réseau (dans ce cas, télécharge les
URLs manuellement ou depuis un autre réseau).
