#!/usr/bin/env python3
"""
Testing Amazon — partie 3 : pousser les créatives vers Meta et créer les ads
au format flexible.

À lancer depuis l'ordinateur d'Hamza, PAS depuis le sandbox cloud : c'est la
machine locale qui télécharge les images chez Magnific puis qui les POST en
multipart vers Meta. Meta ne télécharge jamais rien, donc le robots.txt du CDN
Magnific ne bloque plus rien.

    Magnific  ->  ce PC (download)  ->  Meta (upload multipart)

Le script fait ce que le MCP Meta ne sait pas faire :
  - envoyer les octets de l'image (et non une URL que Meta doit aller chercher)
  - créer une ad au format FLEXIBLE via asset_feed_spec, avec ses 10 images
    et les 3 titres sur chacune

Les campagnes et ad sets sont créés en amont par Claude, en PAUSE. Ce script
ne crée QUE les creatives et les ads, et toujours en PAUSE (règle dure :
on n'active jamais une campagne).

Usage
-----
    export META_ACCESS_TOKEN="EAA..."            # Windows : set META_ACCESS_TOKEN=...

    python scripts/meta_flex_ads.py check  campagnes/relife-stepper.json
    python scripts/meta_flex_ads.py fetch  campagnes/relife-stepper.json
    python scripts/meta_flex_ads.py push   campagnes/relife-stepper.json

`check` ne touche à rien : il valide le fichier de config, l'existence des
images et l'accès au compte. À lancer en premier, toujours.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("Il manque la librairie requests.  ->  pip install requests")

API = "https://graph.facebook.com/v21.0"

# Limites Meta pour asset_feed_spec (dépassement = erreur 400)
MAX_IMAGES = 10
MAX_TITRES = 5
MAX_CORPS = 5

RACINE = Path(__file__).resolve().parent.parent


# --------------------------------------------------------------------------- #
# utilitaires
# --------------------------------------------------------------------------- #

def slugifier(texte: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", texte.lower()).strip("-")
    return slug or "produit"


def token() -> str:
    jeton = os.environ.get("META_ACCESS_TOKEN", "").strip()
    if not jeton:
        sys.exit(
            "META_ACCESS_TOKEN n'est pas défini.\n"
            "  Linux/macOS :  export META_ACCESS_TOKEN=\"EAA...\"\n"
            "  Windows      :  set META_ACCESS_TOKEN=EAA...\n"
            "Le jeton se récupère dans le Business Manager ou le Graph API Explorer,\n"
            "avec les permissions ads_management et business_management."
        )
    return jeton


def compte(cfg: dict) -> str:
    """Normalise l'id de compte : 1234 ou act_1234 -> act_1234."""
    brut = str(cfg["ad_account_id"]).strip()
    return brut if brut.startswith("act_") else f"act_{brut}"


def appel(methode: str, chemin: str, *, data=None, files=None) -> dict:
    """Appel Graph API avec message d'erreur lisible."""
    url = f"{API}/{chemin.lstrip('/')}"
    payload = dict(data or {})
    payload["access_token"] = token()

    for tentative in range(4):
        try:
            rep = requests.request(methode, url, data=payload, files=files, timeout=180)
        except requests.RequestException as err:
            if tentative == 3:
                raise
            attente = 2 ** (tentative + 1)
            print(f"    réseau: {err} — nouvel essai dans {attente}s")
            time.sleep(attente)
            continue

        if rep.status_code < 400:
            return rep.json()

        try:
            erreur = rep.json().get("error", {})
        except ValueError:
            erreur = {"message": rep.text[:500]}

        # 1 = inconnu/transitoire, 2 = service temporairement indisponible,
        # 4 / 17 = throttling
        if erreur.get("code") in (1, 2, 4, 17) and tentative < 3:
            attente = 2 ** (tentative + 1)
            print(f"    Meta transitoire ({erreur.get('code')}) — nouvel essai dans {attente}s")
            time.sleep(attente)
            continue

        detail = erreur.get("error_user_msg") or erreur.get("message") or "erreur inconnue"
        sys.exit(
            f"\nMeta a refusé {methode} {chemin}\n"
            f"  code    : {erreur.get('code')} / sous-code {erreur.get('error_subcode')}\n"
            f"  message : {detail}\n"
            f"  détail  : {erreur.get('error_data') or ''}\n"
        )
    raise RuntimeError("inatteignable")


def charger(chemin: str) -> dict:
    fichier = Path(chemin)
    if not fichier.is_file():
        sys.exit(f"Fichier de configuration introuvable : {fichier}")
    try:
        cfg = json.loads(fichier.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        sys.exit(f"JSON invalide dans {fichier} : {err}")

    manquants = [c for c in ("produit", "ad_account_id", "page_id", "funnel_url", "ad_sets") if not cfg.get(c)]
    if manquants:
        sys.exit(f"Champs manquants dans {fichier} : {', '.join(manquants)}")

    if not cfg.get("titres"):
        # Les 3 titres du pipeline sont fixes (CLAUDE.md)
        cfg["titres"] = ["Venu d'europe !", "DESTOCKAGE 100% ORIGINAL !", "100% ORIGINAL"]

    cfg["_dossier"] = RACINE / "creatives" / slugifier(cfg["produit"])
    return cfg


def images_du_dossier(dossier: Path) -> list[Path]:
    exts = {".png", ".jpg", ".jpeg", ".webp"}
    return sorted(p for p in dossier.glob("*") if p.suffix.lower() in exts)


# --------------------------------------------------------------------------- #
# fetch — Magnific -> disque local
# --------------------------------------------------------------------------- #

def fetch(cfg: dict) -> None:
    sources = cfg.get("creatives") or {}
    if not sources:
        sys.exit(
            "Aucune URL dans la clé \"creatives\" de la config.\n"
            "Claude remplit cette clé avec les URLs Magnific de chaque type."
        )

    total = 0
    for nom_dossier, urls in sources.items():
        cible = cfg["_dossier"] / nom_dossier
        cible.mkdir(parents=True, exist_ok=True)
        print(f"\n{nom_dossier}  ->  {cible}")

        for i, url in enumerate(urls, start=1):
            suffixe = Path(url.split("?")[0]).suffix.lower() or ".png"
            if suffixe not in {".png", ".jpg", ".jpeg", ".webp"}:
                suffixe = ".png"
            fichier = cible / f"{i:02d}{suffixe}"

            if fichier.exists() and fichier.stat().st_size > 0:
                print(f"  {fichier.name}  déjà là, on saute")
                total += 1
                continue

            for tentative in range(4):
                try:
                    rep = requests.get(url, timeout=180)
                    rep.raise_for_status()
                    fichier.write_bytes(rep.content)
                    print(f"  {fichier.name}  {len(rep.content) // 1024} Ko")
                    total += 1
                    break
                except requests.RequestException as err:
                    if tentative == 3:
                        print(f"  ÉCHEC {fichier.name} : {err}")
                    else:
                        time.sleep(2 ** (tentative + 1))

    ecrire_index(cfg)
    print(f"\n{total} image(s) dans {cfg['_dossier']}")
    print(f"Index : {cfg['_dossier'] / 'INDEX.md'}")
    print("Vérifie-les à l'œil, puis lance :  push")


def ecrire_index(cfg: dict) -> None:
    """Écrit un INDEX.md et un index.csv récapitulant les créatives du dossier.

    C'est le document de référence du produit : ce qui part dans quel ad set,
    avec le texte et les titres de l'annonce. Claude Code, lancé en local dans
    ce dossier, le lit pour savoir quoi pousser.
    """
    racine = cfg["_dossier"]
    racine.mkdir(parents=True, exist_ok=True)

    lignes = [
        f"# {cfg['produit']} — créatives",
        "",
        f"- Compte : `{compte(cfg)}`{'  — ' + cfg['_compte'] if cfg.get('_compte') else ''}",
        f"- Page : `{cfg['page_id']}`{'  — ' + cfg['_page'] if cfg.get('_page') else ''}",
        f"- Lien : {cfg['funnel_url']}",
        f"- Généré le {time.strftime('%d/%m/%Y à %H:%M')}",
        "",
        "Les ads sont créées **en pause**. L'activation appartient à Hamza.",
        "",
        "## Créatives par ad set",
        "",
        "| Ad set | Dossier | Fichier | Ko |",
        "|---|---|---|---|",
    ]
    csv = ["ad_set,dossier,fichier,octets"]

    for nom, bloc in cfg["ad_sets"].items():
        sous = bloc.get("dossier") or nom
        dossier = racine / sous
        fichiers = images_du_dossier(dossier) if dossier.is_dir() else []
        if not fichiers:
            lignes.append(f"| {nom} | `{sous}/` | *(vide)* | — |")
            continue
        for fichier in fichiers:
            taille = fichier.stat().st_size
            lignes.append(f"| {nom} | `{sous}/` | `{fichier.name}` | {taille // 1024} |")
            csv.append(f"{nom},{sous},{fichier.name},{taille}")

    lignes += [
        "",
        "## Texte de l'annonce",
        "",
        "```",
        (cfg.get("corps") or "(vide)"),
        "```",
        "",
        "## Titres — les 3 sur chaque image",
        "",
    ]
    lignes += [f"{i}. {t}" for i, t in enumerate(cfg["titres"], start=1)]

    if "video" in cfg["ad_sets"]:
        lignes += [
            "",
            "## Rappel ad set « video »",
            "",
            "L'image du dossier `video/` n'est qu'un **remplissage**, pour que Meta",
            "accepte l'ad. Elle doit être **remplacée par la vidéo** dans le",
            "Gestionnaire — sinon le test vidéo ne veut rien dire.",
        ]

    (racine / "INDEX.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")
    (racine / "index.csv").write_text("\n".join(csv) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# push — disque local -> Meta
# --------------------------------------------------------------------------- #

def televerser_image(cfg: dict, fichier: Path) -> str:
    """POST multipart sur /adimages. Renvoie le image_hash."""
    with fichier.open("rb") as flux:
        rep = appel("POST", f"{compte(cfg)}/adimages",
                    files={fichier.name: (fichier.name, flux, "application/octet-stream")})

    images = rep.get("images") or {}
    for cle in (fichier.name, fichier.stem):
        if cle in images:
            return images[cle]["hash"]
    if images:
        return next(iter(images.values()))["hash"]
    sys.exit(f"Meta n'a pas renvoyé de hash pour {fichier.name} : {rep}")


def creer_creative(cfg: dict, nom: str, hashes: list[str]) -> str:
    """Creative au format FLEXIBLE : plusieurs images, les 3 titres sur chacune."""
    corps = cfg.get("corps") or ""
    if not corps:
        sys.exit("La clé \"corps\" (texte de l'annonce) est vide.")

    feed = {
        "images": [{"hash": h} for h in hashes[:MAX_IMAGES]],
        "bodies": [{"text": t} for t in ([corps] if isinstance(corps, str) else corps)[:MAX_CORPS]],
        "titles": [{"text": t} for t in cfg["titres"][:MAX_TITRES]],
        "link_urls": [{
            "website_url": cfg["funnel_url"],
            "display_url": cfg.get("display_url") or cfg["funnel_url"],
        }],
        "call_to_action_types": [cfg.get("cta", "SHOP_NOW")],
        "ad_formats": ["SINGLE_IMAGE"],
    }
    if cfg.get("description"):
        feed["descriptions"] = [{"text": cfg["description"]}]

    story = {"page_id": str(cfg["page_id"])}
    if cfg.get("instagram_actor_id"):
        story["instagram_actor_id"] = str(cfg["instagram_actor_id"])

    data = {
        "name": f"{cfg['produit']} — {nom}",
        "object_story_spec": json.dumps(story),
        "asset_feed_spec": json.dumps(feed),
        # Advantage+ créative coupé : la créa part telle qu'on l'a produite
        "degrees_of_freedom_spec": json.dumps({
            "creative_features_spec": {
                "standard_enhancements": {"enroll_status": "OPT_OUT"}
            }
        }),
    }
    rep = appel("POST", f"{compte(cfg)}/adcreatives", data=data)
    return rep["id"]


def creer_ad(cfg: dict, nom: str, adset_id: str, creative_id: str) -> str:
    rep = appel("POST", f"{compte(cfg)}/ads", data={
        "name": f"{cfg['produit']} — {nom}",
        "adset_id": str(adset_id),
        "creative": json.dumps({"creative_id": creative_id}),
        "status": "PAUSED",          # jamais ACTIVE. Règle dure.
    })
    return rep["id"]


def push(cfg: dict) -> None:
    print(f"\nCompte {compte(cfg)} · page {cfg['page_id']} · {cfg['produit']}")
    print(f"Lien : {cfg['funnel_url']}")
    print("Les ads seront créées EN PAUSE.\n")

    cache: dict[str, str] = {}
    resultats = []

    for nom, bloc in cfg["ad_sets"].items():
        adset_id = bloc.get("adset_id")
        if not adset_id:
            print(f"[{nom}] pas d'adset_id — on saute")
            continue

        dossier = cfg["_dossier"] / (bloc.get("dossier") or nom)
        fichiers = images_du_dossier(dossier)
        if not fichiers:
            print(f"[{nom}] aucune image dans {dossier} — on saute")
            continue

        if len(fichiers) > MAX_IMAGES:
            print(f"[{nom}] {len(fichiers)} images, Meta en accepte {MAX_IMAGES} — on garde les {MAX_IMAGES} premières")
            fichiers = fichiers[:MAX_IMAGES]

        print(f"[{nom}] {len(fichiers)} image(s) depuis {dossier.name}/")
        hashes = []
        for fichier in fichiers:
            cle = str(fichier)
            if cle not in cache:
                cache[cle] = televerser_image(cfg, fichier)
                print(f"    {fichier.name} -> {cache[cle][:16]}…")
            hashes.append(cache[cle])

        creative_id = creer_creative(cfg, nom, hashes)
        ad_id = creer_ad(cfg, nom, adset_id, creative_id)
        print(f"    creative {creative_id}")
        print(f"    ad       {ad_id}  (PAUSED)\n")
        resultats.append((nom, len(hashes), creative_id, ad_id))

    if not resultats:
        sys.exit("Rien n'a été créé.")

    print("Récapitulatif")
    print(f"{'ad set':<12} {'images':>6}  {'ad id':<22} état")
    for nom, n, _c, ad_id in resultats:
        print(f"{nom:<12} {n:>6}  {ad_id:<22} PAUSED")

    lignes = [f"# {cfg['produit']} — ads créées", "",
              f"Le {time.strftime('%d/%m/%Y à %H:%M')} · compte `{compte(cfg)}`", "",
              "| Ad set | Images | Creative | Ad | État |", "|---|---|---|---|---|"]
    for nom, n, creative_id, ad_id in resultats:
        lignes.append(f"| {nom} | {n} | `{creative_id}` | `{ad_id}` | PAUSED |")
    (cfg["_dossier"] / "ADS.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"\nRécapitulatif écrit dans {cfg['_dossier'] / 'ADS.md'}")

    if "video" in cfg["ad_sets"]:
        print(
            "\nRAPPEL ad set « video » : l'image de type 1 n'est qu'un remplissage,\n"
            "pour que Meta accepte l'ad. Remplace-la par ta vidéo dans le\n"
            "Gestionnaire — si l'image reste, le test vidéo ne veut rien dire."
        )
    print("\nAucune campagne n'a été activée. L'activation se fait à la main.")


# --------------------------------------------------------------------------- #
# check — ne touche à rien
# --------------------------------------------------------------------------- #

def check(cfg: dict) -> None:
    print(f"Produit : {cfg['produit']}")
    print(f"Compte  : {compte(cfg)}")
    print(f"Page    : {cfg['page_id']}")
    print(f"Lien    : {cfg['funnel_url']}")
    print(f"Titres  : {len(cfg['titres'])} — {' | '.join(cfg['titres'])}")
    print(f"Dossier : {cfg['_dossier']}")

    corps = cfg.get("corps") or ""
    print(f"Corps   : {len(corps)} caractères" if corps else "Corps   : VIDE (bloquant)")

    print("\nImages sur le disque")
    total = 0
    for nom, bloc in cfg["ad_sets"].items():
        dossier = cfg["_dossier"] / (bloc.get("dossier") or nom)
        n = len(images_du_dossier(dossier)) if dossier.is_dir() else 0
        total += n
        etat = "ok" if n else "vide — lance fetch"
        print(f"  {nom:<12} {n:>2} image(s)  {dossier.name}/  {etat}")

    print("\nAccès au compte")
    rep = appel("GET", compte(cfg), data={"fields": "name,account_status,currency"})
    print(f"  {rep.get('name')} · statut {rep.get('account_status')} · {rep.get('currency')}")

    for nom, bloc in cfg["ad_sets"].items():
        if not bloc.get("adset_id"):
            print(f"  [{nom}] adset_id manquant")
            continue
        r = appel("GET", str(bloc["adset_id"]), data={"fields": "name,status,effective_status"})
        print(f"  [{nom}] {r.get('name')} · {r.get('status')} / {r.get('effective_status')}")

    print(f"\n{total} image(s) prêtes." if total else "\nAucune image : lance fetch d'abord.")
    index = cfg["_dossier"] / "INDEX.md"
    if index.is_file():
        print(f"Index : {index}")


# --------------------------------------------------------------------------- #

def main() -> None:
    parseur = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parseur.add_argument("action", choices=("check", "fetch", "push"))
    parseur.add_argument("config", help="chemin du JSON de campagne")
    args = parseur.parse_args()

    cfg = charger(args.config)
    {"check": check, "fetch": fetch, "push": push}[args.action](cfg)


if __name__ == "__main__":
    main()
