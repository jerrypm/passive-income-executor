#!/usr/bin/env python3
"""
Shopee Product Scraper (Browser-based) — BarangUnik
Uses Playwright to scrape Shopee search results via headless browser.
Fallback for when Shopee API returns 403.

Usage:
    python3 scrape-shopee-browser.py
    python3 scrape-shopee-browser.py --limit 10
"""

import json
import time
import random
import argparse
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, quote

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Installing playwright...")
    import subprocess
    subprocess.check_call(["pip3", "install", "playwright"])
    subprocess.check_call(["python3", "-m", "playwright", "install", "chromium"])
    from playwright.sync_api import sync_playwright

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

PRICE_CATEGORIES = [
    ("dibawah-20rb", 0, 19999),
    ("20rb-50rb", 20000, 50000),
    ("50rb-100rb", 50001, 100000),
    ("100rb-500rb", 100001, 500000),
    ("diatas-500rb", 500001, float("inf")),
]

SHOPEE_AFFILIATE_ID = "11306601811"
SHOPEE_REDIR_BASE = "https://s.shopee.co.id/an_redir"


def get_price_category(price):
    for slug, min_price, max_price in PRICE_CATEGORIES:
        if min_price <= price <= max_price:
            return slug
    return "diatas-500rb"


def to_affiliate_link(url, sub_id=""):
    """Convert a Shopee URL to an affiliate tracking link."""
    if not url or "shopee.co.id" not in url:
        return url
    if "affiliate_id=" in url:
        return url
    params = {
        "origin_link": url,
        "affiliate_id": SHOPEE_AFFILIATE_ID,
    }
    if sub_id:
        params["sub_id"] = sub_id
    return f"{SHOPEE_REDIR_BASE}?{urlencode(params, quote_via=quote)}"


def scrape_keyword(page, keyword, limit=30):
    """Scrape products from Shopee search page for a keyword."""
    products = []
    search_url = f"https://shopee.co.id/search?keyword={quote(keyword)}"

    try:
        page.goto(search_url, wait_until="networkidle", timeout=30000)
        time.sleep(3)

        # Scroll down to load more products
        for _ in range(3):
            page.evaluate("window.scrollBy(0, 1000)")
            time.sleep(1)

        # Try to extract from search API responses captured during page load
        # Fallback: extract from DOM
        items = page.query_selector_all("[data-sqe='item']")
        if not items:
            items = page.query_selector_all(".shopee-search-item-result__item")
        if not items:
            items = page.query_selector_all("li.col-xs-2-4")

        for item in items[:limit]:
            try:
                product = extract_from_element(item)
                if product:
                    products.append(product)
            except Exception as e:
                print(f"    Error extracting item: {e}")
                continue

    except Exception as e:
        print(f"  Error loading page: {e}")

    return products


def extract_from_element(element):
    """Extract product data from a DOM element."""
    try:
        # Get the link
        link_el = element.query_selector("a")
        if not link_el:
            return None
        href = link_el.get_attribute("href") or ""
        if not href:
            return None

        # Build full URL
        if href.startswith("/"):
            href = f"https://shopee.co.id{href}"

        # Extract shop_id and item_id from URL
        match = re.search(r'-i\.(\d+)\.(\d+)', href)
        if not match:
            return None
        shop_id = match.group(1)
        item_id = match.group(2)

        # Name
        name_el = element.query_selector("[data-sqe='name']") or element.query_selector(".ie3A\\+n") or element.query_selector("div[style*='line-clamp']")
        name = name_el.inner_text().strip() if name_el else ""
        if not name:
            # Try getting text from the link
            texts = link_el.inner_text().strip().split("\n")
            name = texts[0] if texts else ""
        if not name:
            return None

        # Price
        price_text = ""
        price_el = element.query_selector("[class*='price']") or element.query_selector("span[class*='ZEgDH9']")
        if price_el:
            price_text = price_el.inner_text().strip()
        if not price_text:
            # Search for Rp pattern in all text
            all_text = element.inner_text()
            price_match = re.search(r'Rp\s*([\d.]+)', all_text)
            if price_match:
                price_text = price_match.group(1)

        price = parse_price(price_text)
        if price <= 0:
            return None

        # Image
        img_el = element.query_selector("img")
        image_url = ""
        if img_el:
            image_url = img_el.get_attribute("src") or img_el.get_attribute("data-src") or ""

        # Sold count
        sold = 0
        sold_match = re.search(r'([\d.,]+[rRbBkK]?)\s*(?:terjual|Terjual|sold)', element.inner_text())
        if sold_match:
            sold = parse_sold(sold_match.group(1))

        # Discount
        discount = None
        discount_match = re.search(r'(\d+)%', element.inner_text())
        if discount_match:
            discount = int(discount_match.group(1))

        # Rating
        rating = None
        rating_match = re.search(r'(\d+[.,]\d+)\s*(?:star|bintang)?', element.inner_text())
        if rating_match:
            try:
                rating = float(rating_match.group(1).replace(",", "."))
                if rating > 5:
                    rating = None
            except ValueError:
                rating = None

        shopee_url = f"https://shopee.co.id/-i.{shop_id}.{item_id}"
        affiliate_sub_id = f"scraper-{get_price_category(price)}-{item_id}"
        affiliate_url = to_affiliate_link(shopee_url, affiliate_sub_id)

        now = datetime.now(timezone.utc).isoformat()

        return {
            "id": f"shopee_{shop_id}_{item_id}",
            "name": name,
            "price": price,
            "priceCategory": get_price_category(price),
            "discount": discount,
            "imageUrl": image_url,
            "shopeeUrl": affiliate_url,
            "shopeeUrlRaw": shopee_url,
            "rating": round(rating, 1) if rating else None,
            "sold": sold,
            "status": "pending",
            "scrapedAt": now,
            "createdAt": now,
            "updatedAt": now,
        }

    except Exception as e:
        print(f"    Extract error: {e}")
        return None


def parse_price(text):
    """Parse price from text like 'Rp18.700' or '18700'."""
    if not text:
        return 0
    cleaned = re.sub(r'[^\d]', '', text)
    try:
        return int(cleaned)
    except ValueError:
        return 0


def parse_sold(text):
    """Parse sold count from text like '1,2rb' or '500'."""
    text = text.strip().lower()
    multiplier = 1
    if 'rb' in text or 'k' in text:
        multiplier = 1000
        text = text.replace('rb', '').replace('k', '')
    elif 'jt' in text or 'b' in text:
        multiplier = 1000000
        text = text.replace('jt', '').replace('b', '')
    text = text.replace(',', '.').replace(' ', '')
    try:
        return int(float(text) * multiplier)
    except ValueError:
        return 0


def main():
    parser = argparse.ArgumentParser(description="Scrape unique products from Shopee (browser)")
    parser.add_argument("--limit", type=int, default=30, help="Products per keyword (default: 30)")
    parser.add_argument("--output", type=str, default="products.json", help="Output file")
    parser.add_argument("--keywords", type=str, nargs="*", help="Custom keywords")
    parser.add_argument("--min-rating", type=float, default=0.0, help="Min rating filter (default: 0.0)")
    parser.add_argument("--min-sold", type=int, default=0, help="Min sold filter (default: 0)")
    parser.add_argument("--headed", action="store_true", help="Run with visible browser")
    args = parser.parse_args()

    keywords = args.keywords or KEYWORDS
    all_products = {}

    print(f"Scraping Shopee (browser) for {len(keywords)} keywords, {args.limit} products each...")
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="id-ID",
        )
        page = context.new_page()

        # Visit Shopee homepage first to get cookies
        print("Loading Shopee homepage...")
        page.goto("https://shopee.co.id/", wait_until="networkidle", timeout=30000)
        time.sleep(3)

        for i, keyword in enumerate(keywords, 1):
            print(f"[{i}/{len(keywords)}] Searching: '{keyword}'...")
            products = scrape_keyword(page, keyword, args.limit)
            print(f"  Found {len(products)} products")

            for product in products:
                if product["id"] not in all_products:
                    all_products[product["id"]] = product

            if i < len(keywords):
                delay = random.uniform(3, 6)
                print(f"  Waiting {delay:.1f}s...")
                time.sleep(delay)

        browser.close()

    # Quality filter
    products_list = [
        p for p in all_products.values()
        if (p.get("rating") is None or p["rating"] >= args.min_rating)
        and (p.get("sold") or 0) >= args.min_sold
    ]

    # Stats
    print()
    print(f"Total unique products (after filter): {len(products_list)}")
    for slug, _, _ in PRICE_CATEGORIES:
        count = sum(1 for p in products_list if p["priceCategory"] == slug)
        print(f"  {slug}: {count}")

    # Save
    output_path = Path(__file__).parent / args.output
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(products_list, f, ensure_ascii=False, indent=2)

    print(f"\nSaved to {output_path}")


if __name__ == "__main__":
    main()
