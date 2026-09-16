# Installer le pipeline sur l'ordinateur d'Hamza

Pourquoi : le sandbox cloud ne peut joindre **ni** Magnific (`pikaso.cdnpk.net`),
**ni** Amazon, **ni** `bootiktipremium.online` — et il n'a pas de disque à toi.
Sur ta machine, ces murs n'existent pas.

| | Sandbox cloud | Ton PC |
|---|---|---|
| Joindre Magnific / Amazon | ❌ 403 au CONNECT | ✅ |
| Écrire dans tes dossiers | ❌ | ✅ |
| Pousser les octets vers Meta | ❌ | ✅ |
| Ad au format **flexible** (10 images, 3 titres) | ❌ | ✅ |
| Les règles du pipeline | ✅ | ✅ (le repo se clone) |

Meta ne vient **jamais** chercher un fichier sur ton PC : ton ordinateur est
derrière ta box, sans adresse publique. C'est ton PC qui **pousse** vers Meta.

```
Magnific  ->  ton PC (download)  ->  Meta (upload multipart)
```

## 1. Ce qu'il faut installer

| Outil | Pourquoi | Où |
|---|---|---|
| **Node.js 18+** | requis par Claude Code | nodejs.org |
| **Claude Code** | l'agent, en local | `npm install -g @anthropic-ai/claude-code` |
| **Git** | cloner le repo des règles | git-scm.com |
| **Python 3.10+** | le script d'upload Meta | python.org |
| **requests** | librairie HTTP du script | `pip install requests` |

Sur Windows, coche **« Add Python to PATH »** pendant l'installation, sinon la
commande `python` ne sera pas reconnue.

## 2. Cloner le projet

```bash
git clone https://github.com/hamzaouldslimanepro-123/temu-hamza-.git
cd temu-hamza-
```

Puis lancer Claude Code dans ce dossier :

```bash
claude
```

Le `CLAUDE.md` se charge **tout seul** au démarrage : tout le pipeline Testing
Amazon, les 12 règles dures, le format de fiche produit, les règles de
créatives et d'ads. Rien n'est à réexpliquer.

## 3. Rebrancher les MCP

Les connexions Magnific / LightFunnels / Meta / Apify sont attachées à la
session cloud, pas au repo. Il faut les rajouter en local, une seule fois :

```bash
claude mcp list          # voir ce qui est branché
claude mcp add --help    # la syntaxe exacte selon le serveur
```

Pour chacun il te faudra la clé d'API correspondante (Magnific, LightFunnels,
Apify) et le jeton Meta. **Ces clés ne se mettent jamais dans le repo** :
variables d'environnement ou configuration locale de Claude Code uniquement.
Le repo est sur GitHub — une clé commitée est une clé brûlée.

Sans MCP, Claude Code local sait déjà faire beaucoup : lire les règles, écrire
les textes d'annonce, lancer le script d'upload. Les MCP servent au scraping et
à la génération d'images.

## 4. Le jeton Meta

Le script a besoin d'un jeton avec `ads_management` et `business_management`.
Il se récupère dans le Business Manager ou le Graph API Explorer.

```bash
# Linux / macOS
export META_ACCESS_TOKEN="EAA..."

# Windows (invite de commandes)
set META_ACCESS_TOKEN=EAA...

# Windows (PowerShell)
$env:META_ACCESS_TOKEN="EAA..."
```

Un jeton court expire en quelques heures. Pour du récurrent, génère un jeton
long (60 jours) ou un jeton de compte système dans le Business Manager.

## 5. L'arborescence de travail

```
temu-hamza-/
  CLAUDE.md                    le pipeline, chargé automatiquement
  docs/                        les règles détaillées
  scripts/
    meta_flex_ads.py           download Magnific -> upload Meta -> ads flexibles
  campagnes/
    EXEMPLE-relife-stepper.json  gabarit de config, un fichier par produit
  creatives/
    relife-stepper/
      type-1/  01.png … 10.png   -> ad set « image 1 »
      type-2/  01.png … 10.png   -> ad set « image 2 »
      video/   01.png            -> remplissage de l'ad set « video »
```

Un dossier par produit, un sous-dossier par type. Le script lit ces dossiers,
donc tu peux aussi y déposer des images à la main.

## 6. Utiliser le script

Toujours dans cet ordre. `check` ne touche à rien.

```bash
python scripts/meta_flex_ads.py check  campagnes/relife-stepper.json
python scripts/meta_flex_ads.py fetch  campagnes/relife-stepper.json
python scripts/meta_flex_ads.py push   campagnes/relife-stepper.json
```

- **`check`** — valide la config, compte les images, vérifie l'accès au compte
  et l'état des ad sets. Aucune écriture.
- **`fetch`** — télécharge les créatives Magnific dans `creatives/<produit>/`.
  Réentrant : une image déjà là est sautée.
- **`push`** — envoie les images en multipart sur `/act_<id>/adimages`, crée
  une creative **flexible** par ad set (`asset_feed_spec` : les 10 images et
  les **3 titres sur chacune**), puis l'ad. **Toujours `status: PAUSED`.**

Ce que le script fait et que le MCP ne sait pas faire :

| | MCP Meta | Ce script |
|---|---|---|
| Envoi de l'image | `url=` → Meta télécharge → bloqué par robots.txt | multipart, Meta reçoit les octets |
| Format flexible | pas exposé | `asset_feed_spec` |
| 3 titres par image | 1 seul titre | les 3, sur chaque image |
| Advantage+ créative | forcé par défaut | `OPT_OUT` explicite |

## 7. Ce qui ne change pas

- **Aucune campagne n'est activée.** Le script écrit `status: PAUSED` en dur,
  sur chaque ad. L'activation appartient à Hamza, dans le Gestionnaire.
- **Rien ne se lance sans accord** (règle 1). `check` est là pour ça.
- **Rappel ad set « video »** : l'image de type 1 n'est qu'un remplissage pour
  que Meta accepte l'ad. Il faut la **remplacer par la vidéo** — sinon le test
  vidéo ne veut rien dire.
- **Jamais de clé d'API dans le repo.**

## 8. Répartition des rôles

| Étape | Où |
|---|---|
| Scraping Amazon, images Magnific, fiche LightFunnels | cloud **ou** local |
| Campagne + ad sets (en pause) | cloud, déjà fait |
| Créatives -> Meta, ads flexibles | **local uniquement** |
| Activation | **Hamza, à la main** |

Le cloud reste pratique pour discuter et pour la partie 1. Le local est
obligatoire pour la partie 3.
