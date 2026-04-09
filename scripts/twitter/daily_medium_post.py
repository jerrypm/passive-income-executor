#!/usr/bin/env python3
"""
Daily SwiftUI Medium article poster — Twitter + Nostr cross-post.
Tracks which parts have been posted, posts next one automatically.
When all parts are exhausted, logs a reminder to check for new articles.

Cron: 0 15 * * * (daily at 3 PM)
"""

import sys
import os
import json
import time
import subprocess
import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "nostr"))

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
ARTICLES_FILE = Path(__file__).resolve().parent / "swiftui_articles.json"
PROGRESS_FILE = Path(__file__).resolve().parent / "posted_parts.txt"
LOG_FILE = PROJECT_DIR / "logs" / "medium-daily.log"
CHROME_PROFILE = "Profile 10"
MAX_CHARS = 277

# --- Load data ---

def load_articles():
    with open(ARTICLES_FILE) as f:
        return json.load(f)


def get_posted_parts():
    if not PROGRESS_FILE.exists():
        return set()
    with open(PROGRESS_FILE) as f:
        return set(int(line.strip()) for line in f if line.strip().isdigit())


def mark_posted(part):
    with open(PROGRESS_FILE, "a") as f:
        f.write(f"{part}\n")


def get_next_part(articles, posted):
    """Get next unposted part number. Skip articles without individual URL."""
    articles_by_part = {a["part"]: a for a in articles}
    all_parts = sorted(a["part"] for a in articles)
    for p in all_parts:
        if p not in posted:
            if articles_by_part[p].get("url"):
                return p
            else:
                print(f"[!] Part {p} has no URL, skipping (add URL to swiftui_articles.json)")
    return None


# --- Emoji ---

EMOJIS = {
    (1, 5): "📱", (6, 10): "🎨", (11, 15): "🧩", (16, 19): "🛠️",
    (20, 26): "✨", (27, 30): "💎", (31, 35): "⚡", (36, 40): "🔄",
    (41, 45): "🧪", (46, 53): "🧭", (54, 57): "🏗️", (58, 60): "📦",
    (61, 67): "🌐", (68, 100): "🚀",
}

def get_emoji(part):
    for (lo, hi), emoji in EMOJIS.items():
        if lo <= part <= hi:
            return emoji
    return "📱"


# --- Format tweets ---

def format_tweet(article, list_url):
    part = article["part"]
    title = article["title"]
    desc = article["desc"]
    url = article["url"]
    if not url:
        return None
    emoji = get_emoji(part)

    tweet = f"{emoji} Part {part}/100 — {title}\n\n{desc}\n\n{url}\n\n#SwiftUI #100DaysOfCode"

    if len(tweet) > MAX_CHARS:
        avail = MAX_CHARS - len(f"{emoji} Part {part}/100 — {title}\n\n\n\n{url}\n\n#SwiftUI #100DaysOfCode")
        if avail > 10:
            desc = desc[:avail - 3].rsplit(' ', 1)[0] + "..."
            tweet = f"{emoji} Part {part}/100 — {title}\n\n{desc}\n\n{url}\n\n#SwiftUI #100DaysOfCode"
        else:
            tweet = f"{emoji} Part {part}/100 — {title}\n\n{url}\n\n#SwiftUI #100DaysOfCode"

    return tweet


def format_nostr_post(article, list_url):
    """Longer format for Nostr (no char limit)."""
    part = article["part"]
    title = article["title"]
    desc = article["desc"]
    url = article["url"]
    if not url:
        return None
    emoji = get_emoji(part)

    return (
        f"{emoji} Part {part}/100 — SwiftUI Zero to Expert\n\n"
        f"{title}\n\n"
        f"{desc}\n\n"
        f"Read the full article: {url}\n\n"
        f"Full series (67+ parts): {list_url}\n\n"
        f"#SwiftUI #iOS #iOSDev #100DaysOfCode #programming"
    )


# --- Post to Twitter ---

def run_applescript(script):
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip(), result.returncode, result.stderr.strip()


def post_twitter(text):
    subprocess.run([
        "open", "-na", "Google Chrome",
        "--args", f"--profile-directory={CHROME_PROFILE}",
        "https://x.com/home"
    ], capture_output=True)
    time.sleep(8)
    run_applescript('tell application "Google Chrome" to activate')
    time.sleep(1)
    run_applescript('tell application "System Events" to tell process "Google Chrome" to key code 53')
    time.sleep(0.5)
    run_applescript('tell application "System Events" to tell process "Google Chrome" to keystroke "n"')
    time.sleep(3)
    subprocess.run(["pbcopy"], input=text.encode(), capture_output=True)
    time.sleep(0.3)
    run_applescript('tell application "System Events" to tell process "Google Chrome" to keystroke "v" using command down')
    time.sleep(2)
    run_applescript('tell application "System Events" to tell process "Google Chrome" to keystroke return using command down')
    time.sleep(4)
    run_applescript('tell application "System Events" to tell process "Google Chrome" to keystroke "w" using command down')
    return True


# --- Post to Nostr ---

def post_nostr(text):
    """Post to Nostr via nak CLI."""
    env_file = PROJECT_DIR / ".env"
    privkey = None
    if env_file.exists():
        for line in open(env_file):
            if line.startswith("NOSTR_PRIVKEY="):
                privkey = line.strip().split("=", 1)[1]

    if not privkey:
        print("[!] NOSTR_PRIVKEY not found in .env")
        return False

    nak_path = os.path.expanduser("~/go/bin/nak")
    if not os.path.exists(nak_path):
        nak_path = "nak"

    try:
        result = subprocess.run(
            [nak_path, "event", "--sec", privkey, "-c", text, "wss://nos.lol"],
            capture_output=True, text=True, timeout=30
        )
        if "success" in result.stderr.lower() or "success" in result.stdout.lower():
            print("[+] Nostr: posted to nos.lol")
            return True
        else:
            print(f"[!] Nostr: {result.stdout} {result.stderr}")
            return False
    except Exception as e:
        print(f"[!] Nostr error: {e}")
        return False


# --- Logging ---

def log(msg):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


# --- Main ---

def main():
    data = load_articles()
    articles_map = {a["part"]: a for a in data["articles"]}
    list_url = data["list_url"]
    posted = get_posted_parts()

    log(f"Total articles: {len(data['articles'])}, Already posted: {len(posted)}")

    next_part = get_next_part(data["articles"], posted)

    if next_part is None:
        log("ALL PARTS POSTED! Check Medium list for new articles (Part 68+).")
        log(f"List URL: {list_url}")
        log("Add new articles to swiftui_articles.json and they'll be posted next run.")
        return

    article = articles_map[next_part]
    log(f"Next: Part {next_part} — {article['title']}")

    if not article.get("url"):
        log(f"Part {next_part} has no individual URL! Skipping. Add URL to swiftui_articles.json first.")
        return

    # Format for each platform
    tweet = format_tweet(article, list_url)
    nostr_post = format_nostr_post(article, list_url)

    if not tweet or not nostr_post:
        log(f"Part {next_part} has no URL, cannot format. Skipping.")
        return

    log(f"Twitter ({len(tweet)} chars): {tweet[:80]}...")

    # Post to Twitter
    try:
        post_twitter(tweet)
        log(f"Twitter: Part {next_part} POSTED")
    except Exception as e:
        log(f"Twitter FAILED: {e}")

    time.sleep(3)

    # Post to Nostr
    try:
        post_nostr(nostr_post)
        log(f"Nostr: Part {next_part} POSTED")
    except Exception as e:
        log(f"Nostr FAILED: {e}")

    # Mark as posted
    mark_posted(next_part)
    log(f"Part {next_part} marked as posted. Next run will post Part {next_part + 1}.")


if __name__ == "__main__":
    main()
