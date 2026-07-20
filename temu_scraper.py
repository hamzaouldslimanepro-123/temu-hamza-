#!/usr/bin/env python3
"""Scrape product gallery + description images from a saved Temu product page (HTML).

Temu product pages are server-side rendered: all product data (images, price,
SKUs, description...) is embedded as a single JSON blob assigned to
`window.rawData = {...};` in an inline <script> tag. This script extracts that
JSON and pulls out only the two image sets we actually want:

  - Product gallery images  -> store.goods.gallery, keeping only type == 1
    (type == -1 entries are small SKU/color-swatch thumbnails, not product photos)
  - Description images      -> store.productDetailFlatList (falls back to
    store.productDetail.floorList[].items[] if that list is empty/missing)

Usage:
    python3 temu_scraper.py page.html [-o output_dir] [--download]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen

MARKER = "window.rawData"


def extract_raw_data(html: str) -> dict:
    """Find `window.rawData = {...};` and parse the JSON object via brace counting.

    A regex can't safely capture this: the JSON contains nested braces, escaped
    quotes, and strings with '};' inside them, so we scan character by character
    (respecting string/escape state) until the braces balance back to zero.
    """
    idx = html.find(MARKER)
    if idx == -1:
        raise ValueError("window.rawData not found in the given HTML")

    start = html.find("{", idx)
    if start == -1:
        raise ValueError("Could not find opening '{' for window.rawData")

    depth = 0
    in_string = False
    escape = False
    end = None
    for i in range(start, len(html)):
        ch = html[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end is None:
        raise ValueError("Unbalanced braces while scanning window.rawData")

    return json.loads(html[start:end])


def dig(data: dict, *path, default=None):
    cur = data
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def slugify(text: str, max_len: int = 60) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:max_len].rstrip("-") or "produit"


def get_product_name(data: dict) -> str:
    return dig(data, "store", "goods", "goodsName", default="") or "produit-inconnu"


def get_gallery_images(data: dict) -> list[dict]:
    gallery = dig(data, "store", "goods", "gallery", default=[]) or []
    return [img for img in gallery if img.get("type") == 1 and img.get("url")]


def get_description_images(data: dict) -> list[dict]:
    flat = dig(data, "store", "productDetailFlatList", default=[]) or []
    if flat:
        return [img for img in flat if img.get("url")]

    images = []
    floors = dig(data, "store", "productDetail", "floorList", default=[]) or []
    for floor in floors:
        for item in floor.get("items", []) or []:
            if item.get("url"):
                images.append(item)
    return images


def download(url: str, dest: Path) -> None:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=20) as resp, open(dest, "wb") as f:
        f.write(resp.read())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html_file", help="Path to a saved Temu product page (View Page Source)")
    parser.add_argument("-o", "--output", default="scraped_products", help="Base output directory")
    parser.add_argument("--download", action="store_true", help="Download the images locally")
    args = parser.parse_args()

    html = Path(args.html_file).read_text(encoding="utf-8", errors="ignore")
    data = extract_raw_data(html)

    product_name = get_product_name(data)
    gallery = get_gallery_images(data)
    description = get_description_images(data)

    print(f"Product: {product_name}")
    print(f"Gallery images: {len(gallery)}")
    for img in gallery:
        print(f"  [{img.get('priority')}] {img['url']}  ({img.get('width')}x{img.get('height')})")

    print(f"\nDescription images: {len(description)}")
    for img in description:
        print(f"  [{img.get('index')}] {img['url']}  ({img.get('width')}x{img.get('height')})")

    product_dir = Path(args.output) / slugify(product_name)
    gallery_dir = product_dir / "gallery"
    description_dir = product_dir / "description"
    product_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "product_name": product_name,
        "gallery": [img["url"] for img in gallery],
        "description": [img["url"] for img in description],
    }
    (product_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nManifest written to {product_dir / 'manifest.json'}")

    if args.download:
        gallery_dir.mkdir(parents=True, exist_ok=True)
        description_dir.mkdir(parents=True, exist_ok=True)

        for i, img in enumerate(gallery):
            ext = re.search(r"\.(\w+)(?:\?|$)", img["url"])
            ext = ext.group(1) if ext else "jpg"
            dest = gallery_dir / f"gallery_{i:02d}.{ext}"
            try:
                download(img["url"], dest)
                print(f"downloaded {dest}")
            except Exception as e:
                print(f"failed to download {img['url']}: {e}", file=sys.stderr)

        for i, img in enumerate(description):
            ext = re.search(r"\.(\w+)(?:\?|$)", img["url"])
            ext = ext.group(1) if ext else "jpg"
            dest = description_dir / f"desc_{i:02d}.{ext}"
            try:
                download(img["url"], dest)
                print(f"downloaded {dest}")
            except Exception as e:
                print(f"failed to download {img['url']}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
