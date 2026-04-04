import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime

logger = logging.getLogger(__name__)

GITHUB_TRENDING_URL = "https://github.com/trending"

HEADERS = {
    "User-Agent": "AutoResearchBot/1.0"
}

def scrape(keywords, max_items=20):
    """Scrape GitHub trending repos for relevant projects.

    Args:
        keywords: list of keyword strings to filter by
        max_items: max results to return

    Returns:
        list of dicts with keys: source, title, url, snippet, timestamp
    """
    results = []

    for timeframe in ["daily", "weekly"]:
        if len(results) >= max_items:
            break

        try:
            resp = requests.get(
                GITHUB_TRENDING_URL,
                params={"since": timeframe},
                headers=HEADERS,
                timeout=15,
            )
            resp.raise_for_status()
        except Exception as e:
            logger.warning(f"Failed to fetch GitHub trending ({timeframe}): {e}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        articles = soup.select("article.Box-row")

        for article in articles:
            if len(results) >= max_items:
                break

            h2 = article.select_one("h2 a")
            if not h2:
                continue

            repo_path = h2.get("href", "").strip()
            repo_name = repo_path.lstrip("/")
            repo_url = f"https://github.com{repo_path}"

            p = article.select_one("p")
            description = p.get_text(strip=True) if p else ""

            search_text = f"{repo_name} {description}".lower()
            if not any(kw.lower() in search_text for kw in keywords):
                continue

            snippet = description[:200] if description else repo_name

            results.append({
                "source": "github_trending",
                "title": repo_name,
                "url": repo_url,
                "snippet": snippet,
                "timestamp": datetime.utcnow().isoformat(),
            })

    return results
