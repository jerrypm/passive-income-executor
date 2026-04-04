import logging
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

DEVTO_API = "https://dev.to/api/articles"

def scrape(keywords, max_items=20):
    """Scrape dev.to for relevant articles.

    Args:
        keywords: list of keyword strings to search
        max_items: max results to return

    Returns:
        list of dicts with keys: source, title, url, snippet, timestamp
    """
    results = []
    seen_urls = set()

    for kw in keywords:
        if len(results) >= max_items:
            break

        try:
            resp = requests.get(
                DEVTO_API,
                params={"tag": kw.replace(" ", ""), "per_page": 10, "top": 1},
                timeout=15,
            )
            resp.raise_for_status()
            articles = resp.json()
        except Exception as e:
            logger.warning(f"Failed to fetch dev.to for '{kw}': {e}")
            continue

        for article in articles:
            if len(results) >= max_items:
                break

            url = article.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)

            title = article.get("title", "")
            desc = article.get("description", "")
            snippet = desc[:200] if desc else title

            results.append({
                "source": "devto",
                "title": title,
                "url": url,
                "snippet": snippet,
                "timestamp": datetime.utcnow().isoformat(),
            })

    return results
