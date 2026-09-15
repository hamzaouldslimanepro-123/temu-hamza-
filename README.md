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

---

## fba_hunter.py — sourcing de stock Amazon FBA en Europe

Trouve sur Facebook les vendeurs et agents qui destockent leur stock Amazon FBA
europeen (UK, DE, FR, IT, ES, NL, PL). Cible les posts du type :

> *UK FBA Clearance – ANC Headphones – **470 units** – £4.20/unit – take all*

c'est-a-dire photo produit + **quantite exacte disponible** + entrepot FBA europeen.

### Installation

Aucune dependance externe (stdlib uniquement). Il faut un token Apify :

```bash
export APIFY_TOKEN=apify_api_xxxxx
```

### Utilisation

```bash
python fba_hunter.py                                  # les 18 requetes par defaut
python fba_hunter.py --min-score 6                    # seulement les meilleurs leads
python fba_hunter.py --groups-file fba_groups.example.txt   # + scrape de groupes precis
python fba_hunter.py --queries-file mes_requetes.txt  # tes propres mots-cles
```

Sorties : `fba_leads.csv` (import CRM / Google Sheets) et `fba_leads.md`
(lecture rapide, trie par score).

### Comment le tri fonctionne

Le bruit dominant sur Facebook, ce sont les revendeurs de **palettes de retours**
(US surtout) : ce n'est pas du stock vendeur FBA. Le score separe les deux :

| Signal | Points |
|---|---|
| Quantite exacte annoncee (`470 units`, `1 200 unites`, `500 Stück`) | +3 |
| Marche europeen (`UK FBA`, `amazon.de`, `Pan-EU`, …) | +3 |
| ASIN / lien listing Amazon fourni | +2 |
| Vocabulaire vendeur (`take all`, `per unit`, `removal order`, `destockage`) | +2 |
| Prix en GBP/EUR | +1 |
| Photo produit jointe | +1 |
| Palette / retours clients / mystery box sans quantite | −3 |
| Marche hors Europe (Canada, USA, Japon…) | −4 |

Seuil par defaut : score ≥ 4.

### Ce que sort chaque lead

Quantites, marche, prix unitaire, ASIN, auteur + URL de profil, URL du post,
images, et les contacts directs extraits du texte (WhatsApp, Telegram, email,
telephone) — c'est la colonne qui sert a elargir ton carnet d'agents.

### Notes

- Le tier Apify gratuit limite fortement le nombre de runs (rate limit au bout
  de quelques appels). Pour balayer les 18 requetes d'un coup, il faut un plan payant.
- Seuls des posts **publics** sont recuperes ; pas de login ni de cookies.
- Croise toujours un lead avant d'envoyer de l'argent : anciennete du profil,
  photos reelles (pas des visuels de stock), et demande le rapport d'inventaire FBA.
