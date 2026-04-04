import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime

logger = logging.getLogger(__name__)

# Public Nitter instances (try multiple, they go down often)
NITTER_INSTANCES = [
    "https://nitter.privacydev.net",
    "https://nitter.poast.org",
    "https://nitter.cz",
]

SEARCH_QUERIES = [
    "buildinpublic passive income",
    "indie hacker MRR",
    "solo founder revenue",
    "side project making money",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

def _try_nitter(instance, query, max_per_query=10):
    """Try scraping a single Nitter instance."""
    items = []
    search_url = f"{instance}/search?f=tweets&q={requests.utils.quote(query)}"

    try:
        resp = requests.get(search_url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        logger.debug(f"Nitter {instance} failed: {e}")
        return None  # Signal instance failure

    soup = BeautifulSoup(resp.text, "html.parser")
    tweets = soup.select(".timeline-item")

    for tweet in tweets[:max_per_query]:
        content_el = tweet.select_one(".tweet-content")
        if not content_el:
            continue

        text = content_el.get_text(strip=True)
        link_el = tweet.select_one(".tweet-link")
        tweet_path = link_el.get("href", "") if link_el else ""
        tweet_url = f"https://twitter.com{tweet_path}" if tweet_path else ""

        username_el = tweet.select_one(".username")
        username = username_el.get_text(strip=True) if username_el else ""

        items.append({
            "source": "twitter",
            "title": f"{username}: {text[:80]}",
            "url": tweet_url,
            "snippet": text[:200],
            "timestamp": datetime.utcnow().isoformat(),
        })

    return items

def scrape(keywords, max_items=20):
    """Scrape Twitter/X via Nitter instances.

    Args:
        keywords: list of keyword strings (used to build search queries)
        max_items: max results to return

    Returns:
        list of dicts with keys: source, title, url, snippet, timestamp
    """
    results = []

    for instance in NITTER_INSTANCES:
        if len(results) >= max_items:
            break

        instance_works = False
        for query in SEARCH_QUERIES:
            if len(results) >= max_items:
                break

            items = _try_nitter(instance, query)
            if items is None:
                break  # Instance is down, try next
            instance_works = True
            results.extend(items)

        if instance_works:
            break  # Found a working instance, stop trying others

    return results[:max_items]
