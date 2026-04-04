import logging
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

HN_TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_NEW_URL = "https://hacker-news.firebaseio.com/v0/newstories.json"
HN_SHOW_URL = "https://hacker-news.firebaseio.com/v0/showstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

def _fetch_item(item_id):
    """Fetch a single HN item by ID."""
    try:
        resp = requests.get(HN_ITEM_URL.format(item_id), timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.debug(f"Failed to fetch HN item {item_id}: {e}")
        return None

def _matches_keywords(text, keywords):
    """Check if text contains any keyword (case-insensitive)."""
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)

def scrape(keywords, max_items=20):
    """Scrape Hacker News for relevant stories.

    Args:
        keywords: list of keyword strings to filter by
        max_items: max results to return

    Returns:
        list of dicts with keys: source, title, url, snippet, timestamp
    """
    results = []
    seen_ids = set()

    for list_url in [HN_SHOW_URL, HN_TOP_URL, HN_NEW_URL]:
        try:
            resp = requests.get(list_url, timeout=10)
            resp.raise_for_status()
            story_ids = resp.json()[:100]
        except Exception as e:
            logger.warning(f"Failed to fetch HN list {list_url}: {e}")
            continue

        for item_id in story_ids:
            if item_id in seen_ids:
                continue
            seen_ids.add(item_id)

            if len(results) >= max_items:
                return results

            item = _fetch_item(item_id)
            if not item or item.get("type") != "story":
                continue

            title = item.get("title", "")
            text = item.get("text", "")
            url = item.get("url", f"https://news.ycombinator.com/item?id={item_id}")
            search_text = f"{title} {text}"

            if not _matches_keywords(search_text, keywords):
                continue

            snippet = text[:200] if text else title
            results.append({
                "source": "hackernews",
                "title": title,
                "url": url,
                "snippet": snippet,
                "timestamp": datetime.utcnow().isoformat(),
            })

    return results
