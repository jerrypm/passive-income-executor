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
