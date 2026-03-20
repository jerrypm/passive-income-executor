#!/usr/bin/env python3
"""
Twitter Auto Post — Scheduled Posting System
=============================================
Rotates between:
- Referral posts (Honeygain, IPRoyal Pawns)
- Product promos (Nostr Toolkit, Ollama Monetizer, Terminal Kit)
- Organic tech content (generated via Ollama)

Mix ratio: ~40% organic, ~30% referral, ~30% product
Ensures no duplicate posts within 7 days.

Usage:
    python3 scripts/twitter/auto_post_twitter.py              # Auto-select content
    python3 scripts/twitter/auto_post_twitter.py --category referral_honeygain
    python3 scripts/twitter/auto_post_twitter.py --dry-run     # Preview only
"""

import sys
import json
import time
import random
import subprocess
import datetime
import argparse
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
TWEETS_FILE = PROJECT_DIR / "scripts" / "twitter" / "tweets_library.json"
HISTORY_FILE = PROJECT_DIR / "scripts" / "twitter" / "post_history.json"
LOG_FILE = PROJECT_DIR / "logs" / "twitter_posts.log"
CHROME_PROFILE = "Profile 10"

# Category weights for auto-selection
CATEGORY_WEIGHTS = {
    "organic_tech": 40,
    "referral_honeygain": 15,
    "referral_pawns": 10,
    "product_nostr_toolkit": 10,
    "product_ollama_monetizer": 10,
    "product_terminal_income": 10,
}

# Never repeat same category within this many posts
MIN_CATEGORY_GAP = 2
# Never repeat same tweet within this many days
MIN_TWEET_REPEAT_DAYS = 7


def load_tweets():
    with open(TWEETS_FILE) as f:
        data = json.load(f)
    # Filter out non-tweet keys
    return {k: v for k, v in data.items() if not k.startswith("_") and isinstance(v, list)}


def load_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return {"posts": []}


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def get_recent_categories(history, count=3):
    """Get last N categories posted"""
    return [p["category"] for p in history["posts"][-count:]]


def get_recent_tweets(history, days=7):
    """Get tweets posted in last N days"""
    cutoff = (datetime.datetime.now() - datetime.timedelta(days=days)).isoformat()
    return [p["tweet"] for p in history["posts"] if p.get("timestamp", "") > cutoff]


def select_category(history):
    """Weighted random category selection, avoiding recent repeats"""
    recent_cats = get_recent_categories(history, MIN_CATEGORY_GAP)

    # Filter out recently used categories
    available = {k: v for k, v in CATEGORY_WEIGHTS.items() if k not in recent_cats}
    if not available:
        available = CATEGORY_WEIGHTS.copy()

    # Weighted random selection
    total = sum(available.values())
    r = random.randint(1, total)
    cumulative = 0
    for cat, weight in available.items():
        cumulative += weight
        if r <= cumulative:
            return cat
    return list(available.keys())[0]


def select_tweet(category, tweets_db, history):
    """Select a tweet from category, avoiding recent repeats"""
    tweets = tweets_db.get(category, [])
    if not tweets:
        return None

    recent = set(get_recent_tweets(history, MIN_TWEET_REPEAT_DAYS))

    # Filter out recently used tweets
    available = [t for t in tweets if t not in recent and t != "generate"]
    generate_available = any(t == "generate" for t in tweets)

    if available:
        return random.choice(available)
    elif generate_available:
        return "generate"
    else:
        # All used recently, pick random anyway
        non_generate = [t for t in tweets if t != "generate"]
        return random.choice(non_generate) if non_generate else "generate"


def generate_tweet_ollama(model="llama3.2"):
    """Generate organic tech tweet via Ollama"""
    topics = [
        "Share a useful Python tip or trick for developers",
        "Share an interesting fact about AI and machine learning",
        "Share a productivity tip for programmers",
        "Share a thought about the future of open source AI",
        "Share a motivational thought for indie developers",
        "Share a web development tip",
        "Share a thought about building passive income as a developer",
        "Share an iOS development tip",
        "Share a JavaScript/TypeScript tip",
        "Share a macOS productivity tip",
    ]
    topic = random.choice(topics)
    prompt = f"""Write a single tweet (max 250 chars) about: {topic}
Rules: Concise, engaging, casual tone. 1-2 hashtags OK. NO quotes or prefixes. Just the raw tweet. Under 250 chars. English."""

    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True, text=True, timeout=60
        )
        tweet = result.stdout.strip().strip('"').strip("'")
        for prefix in ["Here's", "Here is", "Tweet:", "Sure!", "Sure,"]:
            if tweet.lower().startswith(prefix.lower()):
                tweet = tweet[len(prefix):].strip().lstrip(":").strip()
        tweet = tweet.strip('"').strip("'")
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
        return tweet
    except Exception as e:
        print(f"[!] Ollama error: {e}")
        return None


def run_applescript(script):
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip(), result.returncode, result.stderr.strip()


def post_to_twitter(tweet_text):
    """Post tweet via Chrome AppleScript"""

    # Open Twitter home
    subprocess.run([
        "open", "-na", "Google Chrome",
        "--args", f"--profile-directory={CHROME_PROFILE}",
        "https://x.com/home"
    ], capture_output=True)
    time.sleep(8)

    # Activate Chrome
    run_applescript('tell application "Google Chrome" to activate')
    time.sleep(1)

    # Press Escape (dismiss any popups)
    run_applescript('''
    tell application "System Events"
        tell process "Google Chrome"
            key code 53
        end tell
    end tell
    ''')
    time.sleep(0.5)

    # Try clicking page via Quartz for focus
    try:
        import Quartz
        win_script = '''
        tell application "Google Chrome"
            set winBounds to bounds of front window
            return (item 1 of winBounds) & "," & (item 2 of winBounds) & "," & (item 3 of winBounds) & "," & (item 4 of winBounds)
        end tell
        '''
        bounds_str, _, _ = run_applescript(win_script)
        if bounds_str:
            parts = [int(x.strip()) for x in bounds_str.split(",")]
            cx = parts[0] + (parts[2] - parts[0]) // 2
            cy = parts[1] + 350
            point = Quartz.CGPointMake(cx, cy)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap,
                Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, point, Quartz.kCGMouseButtonLeft))
            time.sleep(0.1)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap,
                Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDown, point, Quartz.kCGMouseButtonLeft))
            time.sleep(0.05)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap,
                Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseUp, point, Quartz.kCGMouseButtonLeft))
    except ImportError:
        pass
    time.sleep(1)

    # Press "N" to open compose
    run_applescript('''
    tell application "System Events"
        tell process "Google Chrome"
            keystroke "n"
        end tell
    end tell
    ''')
    time.sleep(3)

    # Paste tweet
    subprocess.run(["pbcopy"], input=tweet_text.encode(), capture_output=True)
    time.sleep(0.3)

    _, code, err = run_applescript('''
    tell application "System Events"
        tell process "Google Chrome"
            keystroke "v" using command down
        end tell
    end tell
    ''')
    if code != 0:
        print(f"[!] Paste error: {err}")
        return False

    time.sleep(2)

    # Cmd+Enter to post
    _, code, err = run_applescript('''
    tell application "System Events"
        tell process "Google Chrome"
            keystroke return using command down
        end tell
    end tell
    ''')
    if code != 0:
        print(f"[!] Post error: {err}")
        return False

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


def log_post(tweet_text, category, success):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "OK" if success else "FAIL"
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] [{status}] category={category}\n")
        f.write(f"  {tweet_text}\n\n")


def main():
    parser = argparse.ArgumentParser(description="Twitter Auto Post System")
    parser.add_argument("--category", help="Force specific category")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    parser.add_argument("--model", default="llama3.2", help="Ollama model")
    args = parser.parse_args()

    print("=" * 50)
    print("  Twitter Auto Post System")
    print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    tweets_db = load_tweets()
    history = load_history()

    # Select category
    if args.category:
        category = args.category
    else:
        category = select_category(history)

    print(f"\n[*] Category: {category}")

    # Select tweet
    tweet_text = select_tweet(category, tweets_db, history)

    if tweet_text == "generate" or tweet_text is None:
        print("[*] Generating tweet via Ollama...")
        tweet_text = generate_tweet_ollama(model=args.model)
        if not tweet_text:
            print("[!] Failed to generate")
            sys.exit(1)

    print(f"[*] Tweet: {tweet_text}")
    print(f"[*] Length: {len(tweet_text)} chars")

    if args.dry_run:
        print("\n[DRY RUN] Tidak diposting.")
        return

    # Post
    print("\n[*] Posting to Twitter...")
    success = post_to_twitter(tweet_text)
    log_post(tweet_text, category, success)

    # Update history
    history["posts"].append({
        "timestamp": datetime.datetime.now().isoformat(),
        "category": category,
        "tweet": tweet_text,
        "success": success,
    })
    # Keep last 100 entries
    history["posts"] = history["posts"][-100:]
    save_history(history)

    if success:
        print(f"\n[+] DONE! ({category})")
    else:
        print("\n[!] Failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
