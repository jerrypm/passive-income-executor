import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime

logger = logging.getLogger(__name__)

IH_URL = "https://www.indiehackers.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

def scrape(keywords, max_items=20):
    """Scrape Indie Hackers for top posts.

    Args:
        keywords: list of keyword strings to filter by
        max_items: max results to return

    Returns:
        list of dicts with keys: source, title, url, snippet, timestamp
    """
    results = []

    for path in ["/", "/posts"]:
        if len(results) >= max_items:
            break

        try:
            resp = requests.get(f"{IH_URL}{path}", headers=HEADERS, timeout=15)
            resp.raise_for_status()
        except Exception as e:
            logger.warning(f"Failed to fetch Indie Hackers {path}: {e}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")

        for link in soup.select("a"):
            if len(results) >= max_items:
                break

            href = link.get("href", "")
            title = link.get_text(strip=True)

            if not title or len(title) < 10:
                continue
            if not ("/post/" in href or "/product/" in href):
                continue

            url = href if href.startswith("http") else f"{IH_URL}{href}"
            search_text = title.lower()

            if not any(kw.lower() in search_text for kw in keywords):
                continue

            results.append({
                "source": "indiehackers",
                "title": title,
                "url": url,
                "snippet": title,
                "timestamp": datetime.utcnow().isoformat(),
            })

    return results
