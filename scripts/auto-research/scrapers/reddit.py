import logging
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

SUBREDDITS = [
    "SideProject",
    "passive_income",
    "indiehackers",
    "Entrepreneur",
    "slavelabour",
]

HEADERS = {
    "User-Agent": "AutoResearchBot/1.0 (passive income research)"
}

def scrape(keywords, max_items=20):
    """Scrape Reddit subreddits for relevant posts.

    Args:
        keywords: list of keyword strings to filter by
        max_items: max results to return

    Returns:
        list of dicts with keys: source, title, url, snippet, timestamp
    """
    results = []

    for sub in SUBREDDITS:
        if len(results) >= max_items:
            break

        url = f"https://www.reddit.com/r/{sub}/hot.json?limit=25"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.warning(f"Failed to fetch r/{sub}: {e}")
            continue

        posts = data.get("data", {}).get("children", [])
        for post in posts:
            if len(results) >= max_items:
                break

            d = post.get("data", {})
            title = d.get("title", "")
            selftext = d.get("selftext", "")
            permalink = d.get("permalink", "")
            post_url = f"https://www.reddit.com{permalink}"
            search_text = f"{title} {selftext}".lower()

            if not any(kw.lower() in search_text for kw in keywords):
                continue

            snippet = selftext[:200] if selftext else title
            results.append({
                "source": f"reddit/r/{sub}",
                "title": title,
                "url": post_url,
                "snippet": snippet,
                "timestamp": datetime.utcnow().isoformat(),
            })

    return results
