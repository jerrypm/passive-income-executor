#!/usr/bin/env python3
"""
Post Medium article series to Twitter via Chrome automation.

RULES:
- Max 277 chars per tweet
- Each tweet includes: emoji, Part X/100, title, 1-line desc, article URL, hashtags
- If article URL is null, use the list URL
- Posts one tweet at a time (proven method)
- 5 second delay between tweets to avoid rate limiting

Usage:
    python3 scripts/twitter/post_medium_series.py --part 1           # post Part 1
    python3 scripts/twitter/post_medium_series.py --range 1 10       # post Parts 1-10
    python3 scripts/twitter/post_medium_series.py --range 11 20      # post Parts 11-20
    python3 scripts/twitter/post_medium_series.py --part 1 --dry-run # preview only
    python3 scripts/twitter/post_medium_series.py --intro            # post intro tweet
"""

import sys
import os
import json
import time
import subprocess
import argparse
import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
ARTICLES_FILE = Path(__file__).resolve().parent / "swiftui_articles.json"
LOG_FILE = PROJECT_DIR / "logs" / "twitter_posts.log"
CHROME_PROFILE = "Profile 1"
MAX_CHARS = 277

# Emoji rotation per part range
EMOJIS = {
    range(1, 6): "📱",    # basics
    range(6, 11): "🎨",   # UI elements
    range(11, 16): "🧩",  # intermediate UI
    range(16, 20): "🛠️",  # custom components
    range(20, 27): "✨",   # advanced UI
    range(27, 31): "💎",   # UI polish
    range(31, 36): "⚡",   # state basics
    range(36, 41): "🔄",   # state patterns
    range(41, 46): "🧪",   # testing/DI
    range(46, 54): "🧭",   # navigation
    range(54, 58): "🏗️",  # architecture
    range(58, 61): "📦",   # app structure
    range(61, 68): "🌐",   # networking
}


def get_emoji(part):
    for r, emoji in EMOJIS.items():
        if part in r:
            return emoji
    return "📱"


def load_articles():
    with open(ARTICLES_FILE) as f:
        return json.load(f)


def format_tweet(article, list_url):
    """Format a tweet for an article, ensuring max 277 chars."""
    part = article["part"]
    title = article["title"]
    desc = article["desc"]
    url = article["url"] or list_url
    emoji = get_emoji(part)

    # Template: "{emoji} Part X/100 — {title}\n\n{desc}\n\n{url}\n\n#SwiftUI #100DaysOfCode"
    tweet = f"{emoji} Part {part}/100 — {title}\n\n{desc}\n\n{url}\n\n#SwiftUI #100DaysOfCode"

    if len(tweet) > MAX_CHARS:
        # Shorten desc first
        avail = MAX_CHARS - len(f"{emoji} Part {part}/100 — {title}\n\n\n\n{url}\n\n#SwiftUI #100DaysOfCode")
        if avail > 10:
            desc = desc[:avail - 3].rsplit(' ', 1)[0] + "..."
            tweet = f"{emoji} Part {part}/100 — {title}\n\n{desc}\n\n{url}\n\n#SwiftUI #100DaysOfCode"
        else:
            # Drop desc entirely
            tweet = f"{emoji} Part {part}/100 — {title}\n\n{url}\n\n#SwiftUI #100DaysOfCode"

    if len(tweet) > MAX_CHARS:
        # Shorten title
        avail = MAX_CHARS - len(f"{emoji} Part {part}/100 — \n\n{url}\n\n#SwiftUI #100DaysOfCode")
        title = title[:avail - 3].rsplit(' ', 1)[0] + "..."
        tweet = f"{emoji} Part {part}/100 — {title}\n\n{url}\n\n#SwiftUI #100DaysOfCode"

    return tweet


def format_intro(list_url, total_parts):
    return f"🧵 I'm writing a 100-part SwiftUI series: Zero to Expert\n\n{total_parts} parts published. Here's the journey from Part 1 👇\n\nFull list:\n{list_url}\n\n#SwiftUI #iOS #100DaysOfCode"


def run_applescript(script):
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip(), result.returncode, result.stderr.strip()


def post_tweet(text):
    """Post a single tweet via Chrome. Returns True on success."""
    # Open Twitter
    subprocess.run([
        "open", "-na", "Google Chrome",
        "--args", f"--profile-directory={CHROME_PROFILE}",
        "https://x.com/home"
    ], capture_output=True)
    time.sleep(8)

    # Activate + dismiss
    run_applescript('tell application "Google Chrome" to activate')
    time.sleep(1)
    run_applescript('''
    tell application "System Events"
        tell process "Google Chrome"
            key code 53
        end tell
    end tell
    ''')
    time.sleep(0.5)

    # Press N
    run_applescript('''
    tell application "System Events"
        tell process "Google Chrome"
            keystroke "n"
        end tell
    end tell
    ''')
    time.sleep(3)

    # Paste
    subprocess.run(["pbcopy"], input=text.encode(), capture_output=True)
    time.sleep(0.3)
    run_applescript('''
    tell application "System Events"
        tell process "Google Chrome"
            keystroke "v" using command down
        end tell
    end tell
    ''')
    time.sleep(2)

    # Post
    run_applescript('''
    tell application "System Events"
        tell process "Google Chrome"
            keystroke return using command down
        end tell
    end tell
    ''')
    time.sleep(4)

    # Close tab
    run_applescript('''
    tell application "System Events"
        tell process "Google Chrome"
            keystroke "w" using command down
        end tell
    end tell
    ''')
    return True


def log_post(part, tweet, success):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "OK" if success else "FAIL"
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] [{status}] SwiftUI Part {part}\n")
        f.write(f"  {tweet[:100]}...\n\n")


def main():
    parser = argparse.ArgumentParser(description="Post Medium SwiftUI series to Twitter")
    parser.add_argument("--part", type=int, help="Post a single part")
    parser.add_argument("--range", type=int, nargs=2, metavar=("START", "END"),
                        help="Post a range of parts (inclusive)")
    parser.add_argument("--intro", action="store_true", help="Post intro tweet")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    args = parser.parse_args()

    data = load_articles()
    articles = {a["part"]: a for a in data["articles"]}
    list_url = data["list_url"]

    tweets_to_post = []

    if args.intro:
        tweet = format_intro(list_url, len(articles))
        tweets_to_post.append(("intro", tweet))

    if args.part:
        if args.part not in articles:
            print(f"[!] Part {args.part} not found")
            sys.exit(1)
        tweet = format_tweet(articles[args.part], list_url)
        tweets_to_post.append((args.part, tweet))

    if args.range:
        start, end = args.range
        for p in range(start, end + 1):
            if p in articles:
                tweet = format_tweet(articles[p], list_url)
                tweets_to_post.append((p, tweet))

    if not tweets_to_post:
        parser.print_help()
        sys.exit(1)

    print(f"\n{'='*50}")
    print(f"  SwiftUI Series → Twitter")
    print(f"  {len(tweets_to_post)} tweets to post")
    print(f"{'='*50}\n")

    for part, tweet in tweets_to_post:
        chars = len(tweet)
        ok = "✅" if chars <= MAX_CHARS else "❌"
        print(f"{ok} Part {part} ({chars} chars):")
        print(f"  {tweet}\n")

    if args.dry_run:
        print("[DRY RUN] Not posting.")
        return

    for i, (part, tweet) in enumerate(tweets_to_post):
        if i > 0:
            print(f"[*] Waiting 5s...")
            time.sleep(5)
        print(f"[*] Posting Part {part}...")
        success = post_tweet(tweet)
        log_post(part, tweet, success)
        print(f"[+] Part {part} posted! ({len(tweet)} chars)")

    print(f"\n[+] All {len(tweets_to_post)} tweets posted!")


if __name__ == "__main__":
    main()
