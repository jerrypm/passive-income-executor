# Auto Research Intel — Design Spec

**Date:** 2026-04-04
**Purpose:** Automated daily competitive intelligence for passive income opportunities
**Approach:** Modular pipeline (Approach B) with JSON history tracking

---

## Overview

Python script yang jalan 1x sehari via cron, scrape 7 sumber internet untuk competitive intel (apa yang indie hackers lain lakukan yang bisa ditiru), filter hasilnya pakai Ollama AI scoring, dan kirim email digest ke user.

## Architecture & Data Flow

```
[Cron 06:00 daily]
       |
       v
    main.py (orchestrator)
       |
       +-- scrapers/twitter.py     -> Nitter/Twikit, #buildinpublic, indie hackers
       +-- scrapers/reddit.py      -> r/SideProject, r/passive_income, r/indiehackers
       +-- scrapers/hackernews.py  -> Show HN, top stories keyword match
       +-- scrapers/producthunt.py -> New launches hari ini
       +-- scrapers/indiehackers.py-> Top posts/milestones
       +-- scrapers/devto.py       -> Trending articles keyword match
       +-- scrapers/github.py      -> Trending repos hari ini
       |
       v
    processor.py
       +-- Deduplicate (cek vs history.json by URL)
       +-- Ollama scoring (tiap item di-rank 1-10)
       +-- Filter (score >= 7 masuk digest)
       |
       v
    email_sender.py
       +-- Format HTML email (grouped by score tier)
       +-- Kirim via Gmail SMTP
       |
       v
    history.json (append URLs yang sudah dikirim)
```

## Scraper Specifications

All scrapers return unified format:
```python
{
    "source": "reddit",
    "title": "I built a SaaS that makes $3k/mo...",
    "url": "https://...",
    "snippet": "First 200 chars of content...",
    "timestamp": "2026-04-04T06:00:00"
}
```

### Per-source method:

| Source | Method | Auth Required |
|--------|--------|---------------|
| Twitter/X | Nitter instances (public RSS/HTML scrape), Twikit as fallback | No |
| Reddit | JSON API (append `.json` to subreddit URL) | No |
| Hacker News | Official API (`hacker-news.firebaseio.com`) | No |
| Product Hunt | Scrape homepage HTML | No |
| Indie Hackers | Scrape top posts HTML | No |
| dev.to | Public REST API (`/api/articles`) | No |
| GitHub | Scrape trending page HTML + GitHub API | No |

### Search keywords (configurable in config.py):
```python
KEYWORDS = [
    "passive income", "side project", "MRR", "revenue",
    "built in public", "indie hacker", "solo founder",
    "making money", "monthly revenue", "bootstrapped",
    "automated income", "recurring revenue", "SaaS",
    "sell API", "sell template", "digital product",
    "affiliate", "monetize", "cash flow"
]
```

## Ollama AI Scoring

**Model:** llama3.2 (2GB, fastest local model)
**Endpoint:** `http://localhost:11434/api/generate`

### Prompt template:
```
Kamu adalah analis passive income untuk seorang iOS developer & web developer dari Indonesia.
Dia punya: Mac Mini, Ollama, Docker, Python, Node.js, Go, Nostr setup, Lightning wallet.
Dia sudah punya: bandwidth sharing, Nostr DVM, Gumroad products, Twitter auto-post, Medium series.

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

Response format (JSON only):
{"score": 8, "reason": "one line why", "estimated_monthly": "$50-100", "effort": "2 hours"}
```

### Scoring rules:
- Score >= 7: included in email digest
- Score < 7: saved in history.json but not emailed
- Ollama down/timeout (30s): skip scoring, send all items raw as fallback

## Email Format

**Transport:** Gmail SMTP (`smtp.gmail.com:587`, TLS)
**Sender:** jeriisdev@gmail.com (App Password in .env)
**Recipient:** jerrytestone1@gmail.com

### HTML template structure:
```
Subject: Passive Income Intel — {date} ({count} items found)

TOP PICKS (Score 9-10)
  [score/10] "title"
  Source: {source}
  Why: {reason}
  Est: {estimated_monthly} | Effort: {effort}
  -> {url}

GOOD FINDS (Score 7-8)
  (same format)

STATS
  Sources scraped: {success}/{total}
  Total items found: {raw_count}
  After dedup: {dedup_count}
  After AI filter: {filtered_count}
  Ollama model: llama3.2
```

### Edge cases:
- 0 items after filter: send "No high-score intel today" email (confirms system is alive)
- All sources failed: send error summary email with which sources failed and why

## File Structure

```
scripts/auto-research/
+-- main.py              <- Orchestrator (cron entry point)
+-- processor.py         <- Dedup + Ollama scoring
+-- email_sender.py      <- HTML format + Gmail SMTP
+-- config.py            <- Keywords, thresholds, source configs
+-- scrapers/
|   +-- __init__.py
|   +-- twitter.py       <- Nitter/Twikit scraper
|   +-- reddit.py        <- Reddit JSON API
|   +-- hackernews.py    <- HN API
|   +-- producthunt.py   <- PH scrape
|   +-- indiehackers.py  <- IH scrape
|   +-- devto.py         <- dev.to API
|   +-- github.py        <- GitHub trending scrape
+-- history.json         <- URLs already sent (auto-managed)
+-- requirements.txt     <- Dependencies
```

## Dependencies

```
requests         # HTTP calls (all scrapers)
beautifulsoup4   # HTML parsing (PH, IH, GitHub trending, Nitter)
twikit           # Twitter scraping without API key (Nitter fallback)
```

Built-in (no install needed):
- `smtplib` + `email.mime` for email
- `json` for Ollama response parsing + history
- `concurrent.futures` for parallel scraping
- `logging` for log output

## Scheduling

- Cron: `0 6 * * *` (6 AM daily)
- Entry: `cd /Users/avika/Documents/passive-income-executor && /usr/bin/python3 scripts/auto-research/main.py >> logs/auto-research.log 2>&1`
- Log: `logs/auto-research.log`

## Configuration (config.py)

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"
OLLAMA_TIMEOUT = 30  # seconds per item
SCORE_THRESHOLD = 7
MAX_ITEMS_PER_SOURCE = 20
HISTORY_FILE = "history.json"
```
