# Pas à pas — envoyer les créatives vers Meta depuis le PC

Guide écrit pour Hamza le 16/09/2026. Commandes Windows ; les variantes Mac
sont marquées 🍎. Garde **la même fenêtre d'invite de commandes** ouverte de
l'étape 4 à l'étape 8 : la variable du jeton ne survit pas à sa fermeture.

## 1. Python

python.org/downloads → bouton jaune → lancer l'installeur.
**Cocher « Add python.exe to PATH »** avant Install. C'est la seule case qui
bloque tout le reste si elle est oubliée.

```
python --version
```
Attendu : `Python 3.1x.x`. Si « n'est pas reconnu » → réinstaller en cochant PATH.

🍎 Déjà installé : `python3 --version`.

## 2. Le projet

Sans installer Git : github.com/hamzaouldslimanepro-123/temu-hamza- → branche
`claude/cool-tesla-f6awzw` → bouton vert **Code** → **Download ZIP** →
décompresser dans `C:\temu`.

Avec Git :
```
git clone -b claude/cool-tesla-f6awzw https://github.com/hamzaouldslimanepro-123/temu-hamza-.git
```

## 3. La librairie

```
cd C:\temu
pip install requests
```
🍎 `pip3 install requests`

## 4. Le jeton Meta

developers.facebook.com/tools/explorer → choisir une app → ajouter les
permissions **`ads_management`** et **`business_management`** → *Generate
Access Token* → accepter → copier le jeton (`EAA...`).

```
set META_ACCESS_TOKEN=EAA...
```
🍎 `export META_ACCESS_TOKEN="EAA..."`

Ce jeton dure quelques heures. Pour du récurrent : jeton long (60 jours) ou
jeton de compte système dans le Business Manager.

## 5. `check` — ne touche à rien

```
python scripts\meta_flex_ads.py check campagnes\relife-stepper.json
```

Doit afficher le nom du compte 18 et les 3 ad sets en PAUSED. Les « 0 image »
sont normaux avant l'étape 6. **En cas d'erreur, s'arrêter là** et me la coller.

## 6. `fetch` — Magnific vers le disque

```
python scripts\meta_flex_ads.py fetch campagnes\relife-stepper.json
```

Résultat dans `creatives\relife-stepper\{type-1,type-2,video}\`.
Réentrant : une image déjà téléchargée est sautée.

## 7. Relire — la seule étape humaine

Ouvrir `creatives\relife-stepper\` et **regarder les images**. Claude ne les a
jamais vues. Une créative ratée, une faute de texte → **supprimer le fichier**,
le script ne prend que ce qui reste.

Ouvrir `campagnes\relife-stepper.json` et relire le champ **`corps`** : le
texte de l'annonce, le prix et les specs. Corriger, enregistrer.

## 8. `push` — vers Meta

```
python scripts\meta_flex_ads.py push campagnes\relife-stepper.json
```

Crée une ad **flexible** par ad set (les 10 images, les 3 titres sur chacune),
toujours en **PAUSED**.

## 9. Dans le Gestionnaire

1. Compte **18**, campagne **RELIFE Stepper** → les 3 ads
2. Ad set **`video`** : **remplacer l'image de remplissage par la vidéo**.
   Oubliée, le test vidéo ne veut rien dire.
3. Vérifier les placements : Facebook + Instagram seulement
4. **L'activation appartient à Hamza.** Claude n'active jamais une campagne.

## Si ça coince

| Symptôme | Cause | Remède |
|---|---|---|
| `python n'est pas reconnu` | case PATH non cochée | réinstaller Python en la cochant |
| `No module named requests` | librairie absente | `pip install requests` |
| `META_ACCESS_TOKEN n'est pas défini` | fenêtre fermée depuis l'étape 4 | refaire l'étape 4 dans la fenêtre courante |
| `Meta a refusé ... code 190` | jeton expiré | regénérer le jeton (étape 4) |
| `Meta a refusé ... code 200` | permissions manquantes | vérifier `ads_management` + `business_management` |
| `fetch` : ÉCHEC sur des images | tokens d'URL expirés | Claude régénère les URLs, c'est gratuit |
