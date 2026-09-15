#!/usr/bin/env python3
"""
FBA Hunter — trouve sur Facebook les vendeurs/agents qui destockent du stock Amazon FBA en Europe.

Cible : les posts du type
    "UK FBA Clearance – ANC Headphones – 470 units – £4.20/unit – take all"
c.-a-d. photo produit + quantite exacte dispo + entrepot FBA europeen.

Le script :
  1. lance plusieurs recherches Facebook via Apify (multi-langues, multi-marches),
  2. deduplique les posts,
  3. score chaque post (quantite exacte ? marche EU ? vrai stock FBA vs pallet US ?),
  4. extrait les contacts (WhatsApp, Telegram, email, profil FB),
  5. exporte un CSV + un rapport Markdown tries par pertinence.

Usage :
    export APIFY_TOKEN=apify_api_xxx
    python fba_hunter.py                       # recherche complete
    python fba_hunter.py --min-score 5         # seulement les meilleurs leads
    python fba_hunter.py --groups-file g.txt   # + scrape de groupes precis
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone

APIFY_BASE = "https://api.apify.com/v2"

# Acteur de recherche par mot-cle (posts publics, sans login).
SEARCH_ACTOR = "scraper_one~facebook-posts-search"
# Acteur de scrape de groupes (utilise avec --groups-file).
GROUP_ACTOR = "memo23~facebook-public-group-posts-scraper"

# ---------------------------------------------------------------------------
# Requetes de recherche
# ---------------------------------------------------------------------------

# Formules reellement utilisees par les agents/vendeurs qui destockent du FBA EU.
QUERIES = [
    # Anglais / UK (le plus gros marche)
    "UK FBA stock units take all",
    "Amazon FBA UK stock units available DM",
    "Amazon FBA removal order stock UK units",
    "UK FBA overstock units per unit price",
    "Amazon UK FBA aged inventory units take all",
    "FBA seller clearing stock UK ASIN units",
    # Allemagne
    "Germany FBA clearance units take all",
    "DE FBA stock Amazon units available",
    "Amazon FBA Lagerbestand Abverkauf Stueck",
    "FBA Restposten Amazon Deutschland Stueck",
    # France
    "stock FBA Amazon a liquider unites",
    "destockage stock Amazon FBA France unites",
    # Italie / Espagne
    "stock FBA Amazon liquidazione pezzi",
    "liquidacion stock FBA Amazon unidades",
    # Generique Europe
    "EU FBA stock units take all ASIN",
    "Pan EU FBA stock units available",
    "Europe FBA warehouse stock units ASIN",
]

# ---------------------------------------------------------------------------
# Signaux de filtrage
# ---------------------------------------------------------------------------

# Marches cibles : Europe + Canada.
EU_TERMS = [
    "uk fba", "fba uk", "united kingdom", "england", "britain",
    "de fba", "fba de", "germany", "german", "deutschland", "allemagne",
    "fr fba", "fba fr", "france", "french",
    "it fba", "fba it", "italy", "italia",
    "es fba", "fba es", "spain", "espana", "espagne",
    "pl fba", "poland", "polska", "netherlands", "nederland", "belgium",
    "sweden", "czech", "europe", "european", "eu fba", "fba eu", "pan-eu", "pan eu",
    "amazon.co.uk", "amazon.de", "amazon.fr", "amazon.it", "amazon.es", "amazon.nl", "amazon.pl",
    # Canada : marche accepte egalement.
    "canada fba", "fba canada", "canada", "canadian", "amazon.ca",
]

# Marches hors cible (Europe + Canada) -> a ecarter.
NON_EU_TERMS = [
    "usa fba", "us fba", "fba usa",
    "amazon.com fba", "fob midwest", "texas", "florida", "california",
    "amazon.co.jp", "japan fba", "australia fba", "amazon.com.au", "india",
]

# Revendeurs de palettes / lots de retours : ce n'est PAS du stock vendeur FBA.
# Tout post qui contient un de ces termes est rejete d'office (exclusion dure).
PALLET_BLOCK = [
    "pallet", "pallets", "palette", "palettes", "palet", "pallet mixte", "palette mixte",
    "mixed pallet", "truckload", "truck load", "wagon load", "full load", "container load",
    "bin store", "mystery box", "mystery boxes", "boite mystere",
    "customer return", "customer returns", "return pallet", "returns pallet",
    "unclaimed", "shelf pull", "shelf pulls", "job lot", "job lots", "car boot",
    "grade 2", "grade b", "lost post", "lost mail", "liquidation pallet",
]

# Signaux "vrai agent / vendeur qui sort son stock".
SELLER_SIGNALS = [
    "take all", "bulk", "moq", "per unit", "per pc", "/unit", "/pc", "per piece",
    "asin", "amazon listing", "listing available", "fnsku", "removal order",
    "aged inventory", "long term storage", "storage fee", "clearance",
    "destockage", "liquidation", "abverkauf", "restposten",
]

# Societes de debarras / enlevement de dechets : homonymie sur "clearance" en UK.
WASTE_BLOCK = [
    "house clearance", "waste clearance", "garden clearance", "garage clearance",
    "flat clearance", "property clearance", "office clearance", "probate clearance",
    "rubbish", "waste carrier", "waste removal", "skip hire", "landfill",
    "debarras", "encombrants", "entrupelung",
]

# Le post doit parler d'Amazon/FBA : sinon c'est du wholesale generique.
AMAZON_TERMS = ["fba", "amazon", "asin", "fnsku", "seller central"]

# Quantite exacte annoncee : "470 units", "1,200 pcs", "678 pieces", "500 Stueck".
QTY_RE = re.compile(
    r"\b(\d{1,3}(?:[.,\s]\d{3})+|\d{2,6})\s*"
    r"(units?|unites?|pcs?|pieces?|stk|stueck|stück|pezzi|unidades|sets?)\b",
    re.IGNORECASE,
)

# Prix unitaire en devise europeenne.
EU_PRICE_RE = re.compile(
    r"(?:[£€]\s?\d+(?:[.,]\d+)?|\d+(?:[.,]\d+)?\s?(?:gbp|eur|€|£))",
    re.IGNORECASE,
)

ASIN_RE = re.compile(r"\bB0[A-Z0-9]{8}\b")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]{2,}")
PHONE_RE = re.compile(r"(?:\+|00)\d[\d\s().-]{7,17}\d")
WA_RE = re.compile(r"(?:chat\.whatsapp\.com/\S+|wa\.me/\d+)", re.IGNORECASE)
TG_RE = re.compile(r"(?:t\.me/\S+|telegram\.me/\S+|@[A-Za-z0-9_]{5,32}\b(?=[^@]*telegram))", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Appels Apify
# ---------------------------------------------------------------------------

def _post_json(url: str, payload: dict, timeout: int = 300) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode() or "{}")


def _get_json(url: str, timeout: int = 120):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read().decode() or "[]")


def run_actor(actor: str, token: str, payload: dict, timeout: int = 300) -> list[dict]:
    """Lance un acteur Apify en mode synchrone et renvoie les items du dataset."""
    url = f"{APIFY_BASE}/acts/{actor}/run-sync-get-dataset-items?token={token}"
    try:
        items = _post_json(url, payload, timeout=timeout)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")[:300]
        print(f"  ! erreur HTTP {exc.code} sur {actor}: {body}", file=sys.stderr)
        return []
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"  ! reseau: {exc}", file=sys.stderr)
        return []
    return items if isinstance(items, list) else []


# ---------------------------------------------------------------------------
# Analyse d'un post
# ---------------------------------------------------------------------------

@dataclass
class Lead:
    score: int = 0
    quantities: str = ""
    markets: str = ""
    unit_price: str = ""
    asins: str = ""
    author: str = ""
    author_url: str = ""
    post_url: str = ""
    date: str = ""
    whatsapp: str = ""
    telegram: str = ""
    email: str = ""
    phone: str = ""
    image_urls: str = ""
    reasons: str = ""
    text: str = ""


def _found(text_lc: str, terms: list[str]) -> list[str]:
    return [t for t in terms if t in text_lc]


def analyse(post: dict) -> Lead | None:
    text = (post.get("postText") or post.get("text") or post.get("message") or "").strip()
    if not text:
        return None
    lc = text.lower()

    eu_hits = _found(lc, EU_TERMS)
    non_eu_hits = _found(lc, NON_EU_TERMS)
    # Exclusion dure : palettes, lots de retours, truckloads. Aucun score ne rattrape.
    if _found(lc, PALLET_BLOCK):
        return None

    # Exclusion dure : societes de debarras (faux amis de "clearance").
    if _found(lc, WASTE_BLOCK):
        return None

    # Hors sujet si le post ne mentionne ni Amazon ni FBA.
    if not _found(lc, AMAZON_TERMS):
        return None
    seller_hits = _found(lc, SELLER_SIGNALS)
    qty_hits = [f"{m.group(1)} {m.group(2)}" for m in QTY_RE.finditer(text)]

    score = 0
    reasons: list[str] = []

    if qty_hits:
        score += 3
        reasons.append("quantite exacte annoncee")
    if eu_hits:
        score += 3
        reasons.append("marche cible: " + ", ".join(sorted(set(eu_hits))[:3]))
    if EU_PRICE_RE.search(text):
        score += 1
        reasons.append("prix en GBP/EUR")
    if ASIN_RE.search(text):
        score += 2
        reasons.append("ASIN/listing fourni")
    if len(seller_hits) >= 2:
        score += 2
        reasons.append("vocabulaire vendeur/destockage")
    if post.get("attachments"):
        score += 1
        reasons.append("photo produit")

    # Penalite : marche hors cible.
    if non_eu_hits and not eu_hits:
        score -= 4
        reasons.append("hors marche cible: " + ", ".join(sorted(set(non_eu_hits))[:2]))

    # Sans quantite exacte annoncee, ce n'est pas l'offre recherchee.
    if not qty_hits or score <= 0:
        return None

    attachments = post.get("attachments") or []
    if isinstance(attachments, dict):
        attachments = [attachments]
    images = [a.get("url", "") for a in attachments if isinstance(a, dict) and a.get("url")]

    ts = post.get("timestamp") or post.get("time")
    if isinstance(ts, (int, float)):
        date = datetime.fromtimestamp(ts / 1000 if ts > 1e11 else ts, tz=timezone.utc).strftime("%Y-%m-%d")
    else:
        date = str(ts or "")[:10]

    author = post.get("author") or {}
    if not isinstance(author, dict):
        author = {}

    return Lead(
        score=score,
        quantities=" | ".join(qty_hits[:5]),
        markets=", ".join(sorted(set(eu_hits))[:4]),
        unit_price=", ".join(sorted({m.group(0) for m in EU_PRICE_RE.finditer(text)})[:4]),
        asins=", ".join(sorted(set(ASIN_RE.findall(text)))[:8]),
        author=author.get("name", ""),
        author_url=author.get("profileUrl", ""),
        post_url=post.get("url", ""),
        date=date,
        whatsapp=", ".join(sorted(set(WA_RE.findall(text)))[:3]),
        telegram=", ".join(sorted(set(TG_RE.findall(text)))[:3]),
        email=", ".join(sorted(set(EMAIL_RE.findall(text)))[:3]),
        phone=", ".join(sorted(set(PHONE_RE.findall(text)))[:3]),
        image_urls=" ".join(images[:4]),
        reasons="; ".join(reasons),
        text=text[:1500],
    )


# ---------------------------------------------------------------------------
# Collecte
# ---------------------------------------------------------------------------

def collect_searches(token: str, queries: list[str], per_query: int, pause: float) -> list[dict]:
    posts: list[dict] = []
    for i, q in enumerate(queries, 1):
        print(f"[{i}/{len(queries)}] recherche : {q}")
        items = run_actor(
            SEARCH_ACTOR, token,
            {"query": q, "resultsCount": per_query, "searchType": "latest"},
        )
        print(f"    -> {len(items)} posts")
        posts.extend(items)
        if i < len(queries):
            time.sleep(pause)
    return posts


def collect_groups(token: str, group_urls: list[str], max_items: int, days: int) -> list[dict]:
    if not group_urls:
        return []
    print(f"[groupes] scrape de {len(group_urls)} groupe(s)")
    return run_actor(
        GROUP_ACTOR, token,
        {
            "startUrls": [{"url": u} for u in group_urls],
            "maxItems": max_items,
            "onlyPostsNewerThanHours": days * 24,
        },
        timeout=600,
    )


def dedupe(posts: list[dict]) -> list[dict]:
    seen: set[str] = set()
    out = []
    for p in posts:
        key = p.get("postId") or p.get("url") or (p.get("postText") or "")[:120]
        if key and key not in seen:
            seen.add(key)
            out.append(p)
    return out


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def write_csv(leads: list[Lead], path: str) -> None:
    if not leads:
        return
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(asdict(leads[0]).keys()))
        writer.writeheader()
        for lead in leads:
            writer.writerow(asdict(lead))


def write_markdown(leads: list[Lead], path: str) -> None:
    lines = [
        "# Leads — stock Amazon FBA Europe",
        "",
        f"Genere le {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} — {len(leads)} leads.",
        "",
        "Score : quantite exacte (+3), marche EU (+3), ASIN (+2), vocabulaire vendeur (+2),",
        "prix GBP/EUR (+1), photo (+1) ; penalites pour palettes de retours et marches hors EU.",
        "",
    ]
    for i, lead in enumerate(leads, 1):
        contacts = " · ".join(
            x for x in (lead.whatsapp, lead.telegram, lead.email, lead.phone) if x
        ) or "DM uniquement"
        lines += [
            f"## {i}. [score {lead.score}] {lead.author or 'auteur inconnu'} — {lead.date}",
            "",
            f"- **Quantites** : {lead.quantities or '—'}",
            f"- **Marche** : {lead.markets or '—'}",
            f"- **Prix** : {lead.unit_price or '—'}",
            f"- **ASIN** : {lead.asins or '—'}",
            f"- **Contact** : {contacts}",
            f"- **Profil** : {lead.author_url or '—'}",
            f"- **Post** : {lead.post_url or '—'}",
            f"- **Retenu parce que** : {lead.reasons}",
            "",
            "```",
            lead.text[:700],
            "```",
            "",
        ]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Trouve des vendeurs de stock Amazon FBA en Europe sur Facebook.")
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="token Apify (ou $APIFY_TOKEN)")
    ap.add_argument("--per-query", type=int, default=30, help="posts par requete (defaut 30)")
    ap.add_argument("--min-score", type=int, default=4, help="score minimum a conserver (defaut 4)")
    ap.add_argument("--pause", type=float, default=2.0, help="pause entre requetes, en secondes")
    ap.add_argument("--queries-file", help="fichier de requetes personnalisees, une par ligne")
    ap.add_argument("--groups-file", help="fichier d'URL de groupes FB a scraper, une par ligne")
    ap.add_argument("--group-max-items", type=int, default=200, help="posts max par lot de groupes")
    ap.add_argument("--group-days", type=int, default=30, help="fenetre en jours pour les groupes")
    ap.add_argument("--out-prefix", default="fba_leads", help="prefixe des fichiers de sortie")
    args = ap.parse_args()

    if not args.token:
        print("APIFY_TOKEN manquant : export APIFY_TOKEN=apify_api_xxx", file=sys.stderr)
        return 2

    queries = QUERIES
    if args.queries_file:
        with open(args.queries_file, encoding="utf-8") as fh:
            queries = [l.strip() for l in fh if l.strip() and not l.startswith("#")]

    group_urls: list[str] = []
    if args.groups_file:
        with open(args.groups_file, encoding="utf-8") as fh:
            group_urls = [l.strip() for l in fh if l.strip() and not l.startswith("#")]

    raw = collect_searches(args.token, queries, args.per_query, args.pause)
    raw += collect_groups(args.token, group_urls, args.group_max_items, args.group_days)

    posts = dedupe(raw)
    print(f"\n{len(raw)} posts collectes, {len(posts)} uniques.")

    leads = [l for l in (analyse(p) for p in posts) if l and l.score >= args.min_score]
    leads.sort(key=lambda l: (-l.score, l.date), reverse=False)
    leads.sort(key=lambda l: l.score, reverse=True)

    csv_path = f"{args.out_prefix}.csv"
    md_path = f"{args.out_prefix}.md"
    write_csv(leads, csv_path)
    write_markdown(leads, md_path)

    print(f"{len(leads)} leads retenus (score >= {args.min_score}).")
    print(f"  -> {csv_path}\n  -> {md_path}")
    with_contact = sum(1 for l in leads if l.whatsapp or l.telegram or l.email or l.phone)
    print(f"  dont {with_contact} avec un contact direct (WhatsApp/Telegram/email/tel).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
