#!/usr/bin/env python3
"""Auto Research Intel — Daily passive income competitive intelligence."""

import logging
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Setup logging before imports
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("auto-research")

from config import KEYWORDS, MAX_ITEMS_PER_SOURCE
from processor import process
from email_sender import send_email
from scrapers import hackernews, reddit, devto, github, producthunt, indiehackers, twitter

SCRAPERS = {
    "hackernews": hackernews,
    "reddit": reddit,
    "devto": devto,
    "github": github,
    "producthunt": producthunt,
    "indiehackers": indiehackers,
    "twitter": twitter,
}

def run_scraper(name, module):
    """Run a single scraper, catching all errors."""
    try:
        logger.info(f"Scraping {name}...")
        items = module.scrape(KEYWORDS, max_items=MAX_ITEMS_PER_SOURCE)
        logger.info(f"{name}: found {len(items)} items")
        return name, items
    except Exception as e:
        logger.error(f"{name} FAILED: {e}")
        return name, []

def main():
    start = datetime.now()
    logger.info("=== Auto Research Intel started ===")

    # Run all scrapers in parallel
    all_items = []
    source_results = {}

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(run_scraper, name, module): name
            for name, module in SCRAPERS.items()
        }
        for future in as_completed(futures):
            name, items = future.result()
            source_results[name] = len(items)
            all_items.extend(items)

    total_sources = len(SCRAPERS)
    success_sources = sum(1 for v in source_results.values() if v > 0)
    logger.info(f"Scraping done: {success_sources}/{total_sources} sources, {len(all_items)} total items")

    if not all_items:
        logger.warning("No items found from any source")
        # Still send email to confirm system is alive
        stats = {"raw_count": 0, "dedup_count": 0, "filtered_count": 0, "ollama_available": True}
        send_email([], stats, source_results)
        return

    # Process: dedup + score + filter
    filtered, stats = process(all_items)
    logger.info(f"Processing done: {stats}")

    # Send email
    ok = send_email(filtered, stats, source_results)

    elapsed = (datetime.now() - start).total_seconds()
    logger.info(f"=== Done in {elapsed:.1f}s — {'email sent' if ok else 'EMAIL FAILED'} ===")

    if not ok:
        sys.exit(1)

if __name__ == "__main__":
    main()
