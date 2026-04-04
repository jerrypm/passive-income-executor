# Auto Research Intel — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a daily auto-research pipeline that scrapes 7 internet sources for passive income competitive intel, scores results with Ollama AI, and emails a digest.

**Architecture:** Modular pipeline — each source has its own scraper file returning a unified dict format. A central processor deduplicates and scores via Ollama. An email sender formats HTML and sends via Gmail SMTP. An orchestrator (`main.py`) runs all scrapers in parallel, pipes through processor, then emails results.

**Tech Stack:** Python 3.9+, requests, beautifulsoup4, twikit, Ollama API (localhost:11434), Gmail SMTP, cron

---

### Task 1: Setup — Directory, Dependencies, Config

**Files:**
- Create: `scripts/auto-research/requirements.txt`
- Create: `scripts/auto-research/config.py`
- Create: `scripts/auto-research/scrapers/__init__.py`

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p /Users/avika/Documents/passive-income-executor/scripts/auto-research/scrapers
```

- [ ] **Step 2: Create requirements.txt**

Create `scripts/auto-research/requirements.txt`:
```
requests>=2.31.0
beautifulsoup4>=4.12.0
twikit>=2.0.0
```

- [ ] **Step 3: Install dependencies**

```bash
pip3 install -r /Users/avika/Documents/passive-income-executor/scripts/auto-research/requirements.txt
```

Expected: Successfully installed beautifulsoup4, twikit (requests already installed)

- [ ] **Step 4: Create config.py**

Create `scripts/auto-research/config.py`:
```python
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
HISTORY_FILE = BASE_DIR / "history.json"
ENV_FILE = BASE_DIR.parent.parent / ".env"

# Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"
OLLAMA_TIMEOUT = 30

# Scoring
SCORE_THRESHOLD = 7
MAX_ITEMS_PER_SOURCE = 20

# Email (loaded from .env)
def _load_env():
    """Load .env file into dict."""
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                env[key.strip()] = val.strip()
    return env

_env = _load_env()
EMAIL_SENDER = _env.get("EMAIL_SENDER", "")
EMAIL_APP_PASSWORD = _env.get("EMAIL_APP_PASSWORD", "")
EMAIL_RECIPIENT = _env.get("EMAIL_RECIPIENT", "")

# Keywords for filtering scraped content
KEYWORDS = [
    "passive income", "side project", "MRR", "revenue",
    "built in public", "indie hacker", "solo founder",
    "making money", "monthly revenue", "bootstrapped",
    "automated income", "recurring revenue", "SaaS",
    "sell API", "sell template", "digital product",
    "affiliate", "monetize", "cash flow",
]

# Ollama scoring prompt template
SCORING_PROMPT = """Kamu adalah analis passive income untuk seorang iOS developer & web developer dari Indonesia.
Dia punya: Mac Mini, Ollama, Docker, Python, Node.js, Go, Nostr setup, Lightning wallet.
Dia sudah punya: bandwidth sharing, Nostr DVM, Gumroad products, Twitter auto-post, Medium series, DevToolKit website.

Score item ini 1-10 berdasarkan:
- Actionability: Bisa langsung dieksekusi dari terminal? (bobot 3x)
- Revenue potential: Estimasi earning per bulan? (bobot 2x)
- Effort: Seberapa mudah setup? (bobot 2x)
- Novelty: Belum ada di stack dia? (bobot 1x)

Item:
Title: {title}
Source: {source}
Snippet: {snippet}
URL: {url}

Response format (JSON only, no other text):
{{"score": 8, "reason": "one line why", "estimated_monthly": "$50-100", "effort": "2 hours"}}"""
```

- [ ] **Step 5: Create scrapers/__init__.py**

Create `scripts/auto-research/scrapers/__init__.py`:
```python
```

(Empty file — makes scrapers a package)

- [ ] **Step 6: Verify config loads correctly**

```bash
cd /Users/avika/Documents/passive-income-executor && python3 -c "
from scripts import __init__
" 2>/dev/null
cd /Users/avika/Documents/passive-income-executor/scripts/auto-research && python3 -c "
import config
print('EMAIL_SENDER:', config.EMAIL_SENDER)
print('EMAIL_RECIPIENT:', config.EMAIL_RECIPIENT)
print('KEYWORDS count:', len(config.KEYWORDS))
print('HISTORY_FILE:', config.HISTORY_FILE)
print('OK')
"
```

Expected: prints email addresses, 18 keywords, path to history.json, "OK"

- [ ] **Step 7: Commit**

```bash
git add scripts/auto-research/
git commit -m "feat(auto-research): add project setup, config, and dependencies"
```

---

### Task 2: Scraper — Hacker News

**Files:**
- Create: `scripts/auto-research/scrapers/hackernews.py`

This is the simplest scraper (clean public JSON API, no HTML parsing) — build it first to establish the pattern.

- [ ] **Step 1: Create hackernews.py**

Create `scripts/auto-research/scrapers/hackernews.py`:
```python
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
```

- [ ] **Step 2: Test hackernews scraper manually**

```bash
cd /Users/avika/Documents/passive-income-executor/scripts/auto-research && python3 -c "
from scrapers.hackernews import scrape
results = scrape(['side project', 'SaaS', 'passive income', 'revenue', 'startup'], max_items=5)
print(f'Found {len(results)} items')
for r in results:
    print(f'  [{r[\"source\"]}] {r[\"title\"][:60]}')
    print(f'    {r[\"url\"][:80]}')
"
```

Expected: 0-5 items (depends on current HN content), no errors

- [ ] **Step 3: Commit**

```bash
git add scripts/auto-research/scrapers/hackernews.py
git commit -m "feat(auto-research): add Hacker News scraper"
```

---

### Task 3: Scraper — Reddit

**Files:**
- Create: `scripts/auto-research/scrapers/reddit.py`

- [ ] **Step 1: Create reddit.py**

Create `scripts/auto-research/scrapers/reddit.py`:
```python
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
```

- [ ] **Step 2: Test reddit scraper manually**

```bash
cd /Users/avika/Documents/passive-income-executor/scripts/auto-research && python3 -c "
from scrapers.reddit import scrape
results = scrape(['passive income', 'side project', 'making money'], max_items=5)
print(f'Found {len(results)} items')
for r in results:
    print(f'  [{r[\"source\"]}] {r[\"title\"][:60]}')
"
```

Expected: 0-5 items, no errors

- [ ] **Step 3: Commit**

```bash
git add scripts/auto-research/scrapers/reddit.py
git commit -m "feat(auto-research): add Reddit scraper"
```

---

### Task 4: Scraper — dev.to

**Files:**
- Create: `scripts/auto-research/scrapers/devto.py`

- [ ] **Step 1: Create devto.py**

Create `scripts/auto-research/scrapers/devto.py`:
```python
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
```

- [ ] **Step 2: Test devto scraper**

```bash
cd /Users/avika/Documents/passive-income-executor/scripts/auto-research && python3 -c "
from scrapers.devto import scrape
results = scrape(['passive income', 'side project', 'saas'], max_items=5)
print(f'Found {len(results)} items')
for r in results:
    print(f'  [{r[\"source\"]}] {r[\"title\"][:60]}')
"
```

- [ ] **Step 3: Commit**

```bash
git add scripts/auto-research/scrapers/devto.py
git commit -m "feat(auto-research): add dev.to scraper"
```

---

### Task 5: Scraper — GitHub Trending

**Files:**
- Create: `scripts/auto-research/scrapers/github.py`

- [ ] **Step 1: Create github.py**

Create `scripts/auto-research/scrapers/github.py`:
```python
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
```

- [ ] **Step 2: Test github scraper**

```bash
cd /Users/avika/Documents/passive-income-executor/scripts/auto-research && python3 -c "
from scrapers.github import scrape
results = scrape(['income', 'monetize', 'saas', 'api', 'bot', 'automation'], max_items=5)
print(f'Found {len(results)} items')
for r in results:
    print(f'  [{r[\"source\"]}] {r[\"title\"][:60]}')
    print(f'    {r[\"snippet\"][:80]}')
"
```

- [ ] **Step 3: Commit**

```bash
git add scripts/auto-research/scrapers/github.py
git commit -m "feat(auto-research): add GitHub trending scraper"
```

---

### Task 6: Scraper — Product Hunt

**Files:**
- Create: `scripts/auto-research/scrapers/producthunt.py`

- [ ] **Step 1: Create producthunt.py**

Create `scripts/auto-research/scrapers/producthunt.py`:
```python
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
```

- [ ] **Step 2: Test producthunt scraper**

```bash
cd /Users/avika/Documents/passive-income-executor/scripts/auto-research && python3 -c "
from scrapers.producthunt import scrape
results = scrape(['AI', 'SaaS', 'developer', 'tool', 'automation', 'API', 'income'], max_items=5)
print(f'Found {len(results)} items')
for r in results:
    print(f'  [{r[\"source\"]}] {r[\"title\"][:60]}')
"
```

- [ ] **Step 3: Commit**

```bash
git add scripts/auto-research/scrapers/producthunt.py
git commit -m "feat(auto-research): add Product Hunt scraper"
```

---

### Task 7: Scraper — Indie Hackers

**Files:**
- Create: `scripts/auto-research/scrapers/indiehackers.py`

- [ ] **Step 1: Create indiehackers.py**

Create `scripts/auto-research/scrapers/indiehackers.py`:
```python
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
```

- [ ] **Step 2: Test indiehackers scraper**

```bash
cd /Users/avika/Documents/passive-income-executor/scripts/auto-research && python3 -c "
from scrapers.indiehackers import scrape
results = scrape(['revenue', 'MRR', 'income', 'launched', 'built', 'making money'], max_items=5)
print(f'Found {len(results)} items')
for r in results:
    print(f'  [{r[\"source\"]}] {r[\"title\"][:60]}')
"
```

- [ ] **Step 3: Commit**

```bash
git add scripts/auto-research/scrapers/indiehackers.py
git commit -m "feat(auto-research): add Indie Hackers scraper"
```

---

### Task 8: Scraper — Twitter/X via Nitter

**Files:**
- Create: `scripts/auto-research/scrapers/twitter.py`

- [ ] **Step 1: Create twitter.py**

Create `scripts/auto-research/scrapers/twitter.py`:
```python
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
```

- [ ] **Step 2: Test twitter scraper**

```bash
cd /Users/avika/Documents/passive-income-executor/scripts/auto-research && python3 -c "
from scrapers.twitter import scrape
results = scrape(['passive income', 'indie hacker'], max_items=5)
print(f'Found {len(results)} items')
for r in results:
    print(f'  [{r[\"source\"]}] {r[\"title\"][:60]}')
"
```

Note: Nitter instances are unreliable. 0 results is acceptable — the pipeline handles source failures gracefully.

- [ ] **Step 3: Commit**

```bash
git add scripts/auto-research/scrapers/twitter.py
git commit -m "feat(auto-research): add Twitter/Nitter scraper"
```

---

### Task 9: Processor — Dedup + Ollama Scoring

**Files:**
- Create: `scripts/auto-research/processor.py`

- [ ] **Step 1: Create processor.py**

Create `scripts/auto-research/processor.py`:
```python
import json
import logging
import requests
from pathlib import Path
from config import (
    HISTORY_FILE, OLLAMA_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT,
    SCORE_THRESHOLD, SCORING_PROMPT,
)

logger = logging.getLogger(__name__)

def _load_history():
    """Load set of previously seen URLs."""
    if HISTORY_FILE.exists():
        try:
            data = json.loads(HISTORY_FILE.read_text())
            return set(data)
        except (json.JSONDecodeError, TypeError):
            return set()
    return set()

def _save_history(urls):
    """Save URL set to history file."""
    HISTORY_FILE.write_text(json.dumps(sorted(urls), indent=2))

def deduplicate(items):
    """Remove items already in history.

    Args:
        items: list of scraper result dicts

    Returns:
        list of new items not in history
    """
    history = _load_history()
    new_items = [item for item in items if item["url"] not in history]
    logger.info(f"Dedup: {len(items)} total -> {len(new_items)} new ({len(items) - len(new_items)} duplicates)")
    return new_items

def _score_single(item):
    """Score a single item using Ollama.

    Returns:
        dict with score, reason, estimated_monthly, effort — or None on failure
    """
    prompt = SCORING_PROMPT.format(
        title=item["title"],
        source=item["source"],
        snippet=item["snippet"],
        url=item["url"],
    )

    try:
        resp = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=OLLAMA_TIMEOUT,
        )
        resp.raise_for_status()
        response_text = resp.json().get("response", "")

        # Extract JSON from response (Ollama may add extra text)
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(response_text[start:end])
    except requests.exceptions.ConnectionError:
        logger.warning("Ollama not running — skipping AI scoring")
        return None
    except requests.exceptions.Timeout:
        logger.warning(f"Ollama timeout scoring: {item['title'][:50]}")
        return None
    except (json.JSONDecodeError, KeyError) as e:
        logger.warning(f"Ollama response parse error: {e}")
        return None

    return None

def score_items(items):
    """Score all items using Ollama AI.

    Args:
        items: list of scraper result dicts

    Returns:
        tuple of (scored_items, ollama_available)
        scored_items: list of dicts with added 'ai_score' key
        ollama_available: bool — False means Ollama was unreachable
    """
    scored = []
    ollama_available = True

    for i, item in enumerate(items):
        logger.info(f"Scoring {i+1}/{len(items)}: {item['title'][:50]}")
        result = _score_single(item)

        if result is None and i == 0:
            # First item failed — Ollama likely down, skip all scoring
            logger.warning("Ollama appears unavailable — sending all items unscored")
            ollama_available = False
            for it in items:
                it["ai_score"] = None
                scored.append(it)
            return scored, ollama_available

        if result:
            item["ai_score"] = result
        else:
            item["ai_score"] = None

        scored.append(item)

    return scored, ollama_available

def filter_and_update_history(scored_items, ollama_available):
    """Filter items by score threshold and update history.

    Args:
        scored_items: list of items with ai_score
        ollama_available: if False, include all items (no filtering)

    Returns:
        list of items that pass the threshold
    """
    history = _load_history()

    # Add all URLs to history regardless of score
    for item in scored_items:
        history.add(item["url"])
    _save_history(history)

    if not ollama_available:
        logger.info(f"Ollama unavailable — returning all {len(scored_items)} items unfiltered")
        return scored_items

    passed = []
    for item in scored_items:
        score_data = item.get("ai_score")
        if score_data and isinstance(score_data.get("score"), (int, float)):
            if score_data["score"] >= SCORE_THRESHOLD:
                passed.append(item)
        else:
            # Scoring failed for this item — include it to be safe
            passed.append(item)

    logger.info(f"Filter: {len(scored_items)} scored -> {len(passed)} passed (threshold {SCORE_THRESHOLD})")
    return passed

def process(items):
    """Full processing pipeline: dedup -> score -> filter.

    Args:
        items: list of raw scraper result dicts

    Returns:
        tuple of (filtered_items, stats)
        stats: dict with raw_count, dedup_count, filtered_count, ollama_available
    """
    stats = {"raw_count": len(items)}

    new_items = deduplicate(items)
    stats["dedup_count"] = len(new_items)

    if not new_items:
        stats["filtered_count"] = 0
        stats["ollama_available"] = True
        return [], stats

    scored, ollama_available = score_items(new_items)
    stats["ollama_available"] = ollama_available

    filtered = filter_and_update_history(scored, ollama_available)
    stats["filtered_count"] = len(filtered)

    return filtered, stats
```

- [ ] **Step 2: Test processor with mock data (Ollama may be off)**

```bash
cd /Users/avika/Documents/passive-income-executor/scripts/auto-research && python3 -c "
from processor import deduplicate, process
items = [
    {'source': 'test', 'title': 'Test Item 1', 'url': 'https://example.com/1', 'snippet': 'test', 'timestamp': '2026-04-04T00:00:00'},
    {'source': 'test', 'title': 'Test Item 2', 'url': 'https://example.com/2', 'snippet': 'test', 'timestamp': '2026-04-04T00:00:00'},
]
new = deduplicate(items)
print(f'Dedup: {len(new)} new items')
filtered, stats = process(items)
print(f'Stats: {stats}')
print(f'Filtered: {len(filtered)} items')
print('OK')
"
```

Expected: Shows dedup and processing stats, may show "Ollama unavailable" warning if Ollama is off

- [ ] **Step 3: Clean up test history**

```bash
rm -f /Users/avika/Documents/passive-income-executor/scripts/auto-research/history.json
```

- [ ] **Step 4: Commit**

```bash
git add scripts/auto-research/processor.py
git commit -m "feat(auto-research): add processor with dedup and Ollama scoring"
```

---

### Task 10: Email Sender

**Files:**
- Create: `scripts/auto-research/email_sender.py`

- [ ] **Step 1: Create email_sender.py**

Create `scripts/auto-research/email_sender.py`:
```python
import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_SENDER, EMAIL_APP_PASSWORD, EMAIL_RECIPIENT

logger = logging.getLogger(__name__)

def _format_item_html(item):
    """Format a single item as HTML."""
    score_data = item.get("ai_score")

    if score_data and isinstance(score_data.get("score"), (int, float)):
        score = score_data["score"]
        reason = score_data.get("reason", "")
        est = score_data.get("estimated_monthly", "?")
        effort = score_data.get("effort", "?")
        return f"""
        <div style="margin-bottom:16px;padding:12px;border-left:4px solid {'#22c55e' if score >= 9 else '#3b82f6'};background:#f8f9fa;">
            <strong>[{score}/10]</strong> {item['title']}<br>
            <span style="color:#666;">Source: {item['source']}</span><br>
            <span style="color:#444;">Why: {reason}</span><br>
            <span style="color:#888;">Est: {est} | Effort: {effort}</span><br>
            <a href="{item['url']}" style="color:#2563eb;">{item['url'][:80]}</a>
        </div>"""
    else:
        return f"""
        <div style="margin-bottom:16px;padding:12px;border-left:4px solid #94a3b8;background:#f8f9fa;">
            <strong>{item['title']}</strong><br>
            <span style="color:#666;">Source: {item['source']}</span><br>
            <span style="color:#444;">{item['snippet'][:150]}</span><br>
            <a href="{item['url']}" style="color:#2563eb;">{item['url'][:80]}</a>
        </div>"""

def _build_html(items, stats, source_results):
    """Build full HTML email body."""
    date_str = datetime.now().strftime("%d %b %Y")
    count = len(items)

    # Separate by score tier
    top_picks = []
    good_finds = []
    unscored = []

    for item in items:
        score_data = item.get("ai_score")
        if score_data and isinstance(score_data.get("score"), (int, float)):
            if score_data["score"] >= 9:
                top_picks.append(item)
            else:
                good_finds.append(item)
        else:
            unscored.append(item)

    # Sort by score descending within tiers
    good_finds.sort(key=lambda x: x.get("ai_score", {}).get("score", 0), reverse=True)

    sections = ""

    if top_picks:
        sections += "<h2 style='color:#22c55e;'>TOP PICKS (Score 9-10)</h2>"
        for item in top_picks:
            sections += _format_item_html(item)

    if good_finds:
        sections += "<h2 style='color:#3b82f6;'>GOOD FINDS (Score 7-8)</h2>"
        for item in good_finds:
            sections += _format_item_html(item)

    if unscored:
        sections += "<h2 style='color:#94a3b8;'>UNSCORED (Ollama unavailable)</h2>"
        for item in unscored:
            sections += _format_item_html(item)

    if not items:
        sections = "<p style='color:#666;font-size:16px;'>No high-score intel today. All items scored below threshold.</p>"

    # Source status
    source_rows = ""
    for name, status in source_results.items():
        icon = "&#9989;" if status > 0 else "&#10060;"
        source_rows += f"<tr><td>{icon} {name}</td><td>{status} items</td></tr>"

    html = f"""
    <html>
    <body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:600px;margin:0 auto;padding:20px;">
        <h1 style="border-bottom:2px solid #333;padding-bottom:8px;">
            Passive Income Intel — {date_str}
        </h1>
        <p style="color:#666;">{count} items passed filter</p>

        {sections}

        <hr style="margin:24px 0;">
        <h3>STATS</h3>
        <table style="border-collapse:collapse;">
            {source_rows}
        </table>
        <p style="color:#888;font-size:12px;">
            Total scraped: {stats.get('raw_count', 0)} |
            After dedup: {stats.get('dedup_count', 0)} |
            After filter: {stats.get('filtered_count', 0)} |
            Ollama: {'ON' if stats.get('ollama_available') else 'OFF (all items sent unfiltered)'}
        </p>
    </body>
    </html>"""

    return html

def send_email(items, stats, source_results):
    """Send digest email via Gmail SMTP.

    Args:
        items: list of filtered items to include
        stats: dict with raw_count, dedup_count, filtered_count, ollama_available
        source_results: dict mapping source name -> item count

    Returns:
        bool — True if sent successfully
    """
    if not EMAIL_SENDER or not EMAIL_APP_PASSWORD or not EMAIL_RECIPIENT:
        logger.error("Email credentials missing in .env — cannot send")
        return False

    date_str = datetime.now().strftime("%d %b %Y")
    count = len(items)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Passive Income Intel — {date_str} ({count} items found)"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECIPIENT

    html = _build_html(items, stats, source_results)
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_APP_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
        logger.info(f"Email sent to {EMAIL_RECIPIENT} ({count} items)")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False
```

- [ ] **Step 2: Test email sender with a test email**

```bash
cd /Users/avika/Documents/passive-income-executor/scripts/auto-research && python3 -c "
from email_sender import send_email
test_items = [{
    'source': 'test',
    'title': 'Auto Research Intel - Test Email',
    'url': 'https://example.com',
    'snippet': 'This is a test to verify email delivery works.',
    'ai_score': {'score': 9, 'reason': 'Test item', 'estimated_monthly': '\$0', 'effort': '0 min'},
}]
stats = {'raw_count': 1, 'dedup_count': 1, 'filtered_count': 1, 'ollama_available': True}
source_results = {'test': 1}
ok = send_email(test_items, stats, source_results)
print('Email sent!' if ok else 'FAILED')
"
```

Expected: "Email sent!" — check jerrytestone1@gmail.com inbox

- [ ] **Step 3: Commit**

```bash
git add scripts/auto-research/email_sender.py
git commit -m "feat(auto-research): add HTML email sender via Gmail SMTP"
```

---

### Task 11: Orchestrator — main.py

**Files:**
- Create: `scripts/auto-research/main.py`

- [ ] **Step 1: Create main.py**

Create `scripts/auto-research/main.py`:
```python
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
```

- [ ] **Step 2: Make executable**

```bash
chmod +x /Users/avika/Documents/passive-income-executor/scripts/auto-research/main.py
```

- [ ] **Step 3: Test full pipeline**

```bash
cd /Users/avika/Documents/passive-income-executor/scripts/auto-research && python3 main.py
```

Expected: Logs showing each scraper running, processing, and email sent. Check inbox for the digest.

- [ ] **Step 4: Clean up test history for fresh start**

```bash
rm -f /Users/avika/Documents/passive-income-executor/scripts/auto-research/history.json
```

- [ ] **Step 5: Commit**

```bash
git add scripts/auto-research/main.py
git commit -m "feat(auto-research): add main orchestrator with parallel scraping"
```

---

### Task 12: Cron Setup + Final Integration

**Files:**
- Modify: system crontab

- [ ] **Step 1: Setup cron job**

```bash
(crontab -l 2>/dev/null; echo "0 6 * * * cd /Users/avika/Documents/passive-income-executor && /usr/bin/python3 scripts/auto-research/main.py >> logs/auto-research.log 2>&1") | crontab -
```

- [ ] **Step 2: Verify cron is registered**

```bash
crontab -l | grep auto-research
```

Expected: `0 6 * * * cd /Users/avika/Documents/passive-income-executor && /usr/bin/python3 scripts/auto-research/main.py >> logs/auto-research.log 2>&1`

- [ ] **Step 3: Ensure log directory exists**

```bash
mkdir -p /Users/avika/Documents/passive-income-executor/logs
```

- [ ] **Step 4: Run final full test**

```bash
cd /Users/avika/Documents/passive-income-executor && /usr/bin/python3 scripts/auto-research/main.py 2>&1 | tail -20
```

Expected: Full run with email delivery. Check jerrytestone1@gmail.com for the digest.

- [ ] **Step 5: Commit**

```bash
git add scripts/auto-research/
git commit -m "feat(auto-research): complete auto-research intel pipeline with cron"
```
