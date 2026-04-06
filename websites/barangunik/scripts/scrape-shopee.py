#!/usr/bin/env python3
"""
Shopee Product Scraper — BarangUnik
Searches for unique/weird products on Shopee Indonesia.
Outputs products.json for import into the admin dashboard.

Usage:
    python3 scrape-shopee.py
    python3 scrape-shopee.py --limit 10
"""

import json
import time
import random
import argparse
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("Installing requests...")
    import subprocess
    subprocess.check_call(["pip3", "install", "requests"])
    import requests

KEYWORDS = [
    "barang unik murah",
    "alat dapur unik",
    "lampu unik lucu",
    "organizer unik",
    "gadget unik murah",
    "aksesoris HP unik",
    "barang aneh shopee",
    "barang viral murah",
]

SHOPEE_SEARCH_URL = "https://shopee.co.id/api/v4/search/search_items"

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
]

PRICE_CATEGORIES = [
    ("dibawah-20rb", 0, 19999),
    ("20rb-50rb", 20000, 50000),
    ("50rb-100rb", 50001, 100000),
    ("100rb-500rb", 100001, 500000),
    ("diatas-500rb", 500001, float("inf")),
]


def get_price_category(price: int) -> str:
    for slug, min_price, max_price in PRICE_CATEGORIES:
        if min_price <= price <= max_price:
            return slug
    return "diatas-500rb"


SHOPEE_AFFILIATE_ID = "11306601811"
SHOPEE_REDIR_BASE = "https://s.shopee.co.id/an_redir"

def to_affiliate_link(url: str, sub_id: str = "") -> str:
    """Convert a Shopee URL to an affiliate tracking link."""
    if not url or "shopee.co.id" not in url:
        return url
    if "affiliate_id=" in url:
        return url
    from urllib.parse import urlencode, quote
    params = {
        "origin_link": url,
        "affiliate_id": SHOPEE_AFFILIATE_ID,
    }
    if sub_id:
        params["sub_id"] = sub_id
    return f"{SHOPEE_REDIR_BASE}?{urlencode(params, quote_via=quote)}"


def search_shopee(keyword: str, limit: int = 30) -> list:
    """Search Shopee for products matching keyword."""
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json",
        "Referer": "https://shopee.co.id/",
        "X-Requested-With": "XMLHttpRequest",
    }

    params = {
        "keyword": keyword,
        "limit": limit,
        "newest": 0,
        "order": "relevancy",
        "page_type": "search",
        "scenario": "PAGE_GLOBAL_SEARCH",
        "version": 2,
    }

    try:
        response = requests.get(
            SHOPEE_SEARCH_URL,
            params=params,
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("items", [])
    except Exception as e:
        print(f"  Error searching '{keyword}': {e}")
        return []


def extract_product(item: dict):
    """Extract product data from Shopee search result item."""
    try:
        info = item.get("item_basic", item)
        shop_id = info.get("shopid", 0)
        item_id = info.get("itemid", 0)

        price_raw = info.get("price", 0)
        # Shopee prices are in units of 100000 (IDR * 100000)
        price = price_raw // 100000 if price_raw > 100000 else price_raw

        if price <= 0:
            return None

        name = info.get("name", "")
        if not name:
            return None

        # Image
        image_hash = info.get("image", "")
        image_url = f"https://cf.shopee.co.id/file/{image_hash}" if image_hash else ""

        # Discount
        raw_discount = info.get("raw_discount", 0)
        discount = int(raw_discount) if raw_discount else None

        # Rating
        rating_star = info.get("item_rating", {}).get("rating_star", None)

        # Sold
        sold = info.get("sold", 0)
        if isinstance(sold, dict):
            sold = sold.get("sold", 0)

        # Shopee URL
        slug = name.lower().replace(" ", "-")[:80]
        shopee_url = f"https://shopee.co.id/{slug}-i.{shop_id}.{item_id}"

        # Generate affiliate link (Layer 1)
        affiliate_sub_id = f"scraper-{get_price_category(price)}-{item_id}"
        affiliate_url = to_affiliate_link(shopee_url, affiliate_sub_id)

        now = datetime.now(timezone.utc).isoformat()
        product_id = f"shopee_{shop_id}_{item_id}"

        return {
            "id": product_id,
            "name": name,
            "price": price,
            "priceCategory": get_price_category(price),
            "discount": discount,
            "imageUrl": image_url,
            "shopeeUrl": affiliate_url,
            "shopeeUrlRaw": shopee_url,
            "rating": round(rating_star, 1) if rating_star else None,
            "sold": sold,
            "status": "pending",
            "scrapedAt": now,
            "createdAt": now,
            "updatedAt": now,
        }
    except Exception as e:
        print(f"  Error extracting product: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Scrape unique products from Shopee")
    parser.add_argument("--limit", type=int, default=30, help="Products per keyword (default: 30)")
    parser.add_argument("--output", type=str, default="products.json", help="Output file")
    parser.add_argument("--keywords", type=str, nargs="*", help="Custom keywords (overrides defaults)")
    parser.add_argument("--min-rating", type=float, default=4.0, help="Min rating filter (default: 4.0)")
    parser.add_argument("--min-sold", type=int, default=100, help="Min sold filter (default: 100)")
    args = parser.parse_args()

    keywords = args.keywords or KEYWORDS
    all_products = {}

    print(f"Scraping Shopee for {len(keywords)} keywords, {args.limit} products each...")
    print()

    for i, keyword in enumerate(keywords, 1):
        print(f"[{i}/{len(keywords)}] Searching: '{keyword}'...")
        items = search_shopee(keyword, args.limit)
        print(f"  Found {len(items)} results")

        for item in items:
            product = extract_product(item)
            if product and product["id"] not in all_products:
                all_products[product["id"]] = product

        # Be nice to Shopee servers
        if i < len(keywords):
            delay = random.uniform(2, 5)
            print(f"  Waiting {delay:.1f}s...")
            time.sleep(delay)

    # Quality filter: rating >= 4.0 and sold >= 100
    products_list = [
        p for p in all_products.values()
        if (p.get("rating") is None or p["rating"] >= args.min_rating)
        and (p.get("sold") or 0) >= args.min_sold
    ]

    # Stats
    print()
    print(f"Total unique products: {len(products_list)}")
    for slug, _, _ in PRICE_CATEGORIES:
        count = sum(1 for p in products_list if p["priceCategory"] == slug)
        print(f"  {slug}: {count}")

    # Save
    output_path = Path(__file__).parent / args.output
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(products_list, f, ensure_ascii=False, indent=2)

    print(f"\nSaved to {output_path}")
    print(f"Import this file via the admin dashboard 'Import Hasil Scrape' button.")


if __name__ == "__main__":
    main()
