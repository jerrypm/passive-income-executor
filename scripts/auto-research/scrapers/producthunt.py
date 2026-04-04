import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime

logger = logging.getLogger(__name__)

PH_URL = "https://www.producthunt.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

def scrape(keywords, max_items=20):
    """Scrape Product Hunt for today's launches.

    Args:
        keywords: list of keyword strings to filter by
        max_items: max results to return

    Returns:
        list of dicts with keys: source, title, url, snippet, timestamp
    """
    results = []

    try:
        resp = requests.get(PH_URL, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        logger.warning(f"Failed to fetch Product Hunt: {e}")
        return results

    soup = BeautifulSoup(resp.text, "html.parser")

    # PH uses data attributes and various class patterns — extract links with titles
    for link in soup.select("a[href*='/posts/']"):
        if len(results) >= max_items:
            break

        href = link.get("href", "")
        if not href.startswith("/posts/"):
            continue

        title = link.get_text(strip=True)
        if not title or len(title) < 5:
            continue

        url = f"https://www.producthunt.com{href}"

        # Check nearby text for description
        parent = link.find_parent()
        description = ""
        if parent:
            siblings = parent.find_next_siblings()
            for sib in siblings[:2]:
                text = sib.get_text(strip=True)
                if text and len(text) > 20:
                    description = text
                    break

        search_text = f"{title} {description}".lower()
        if not any(kw.lower() in search_text for kw in keywords):
            continue

        snippet = description[:200] if description else title

        results.append({
            "source": "producthunt",
            "title": title,
            "url": url,
            "snippet": snippet,
            "timestamp": datetime.utcnow().isoformat(),
        })

    return results
