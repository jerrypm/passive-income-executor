#!/usr/bin/env python3
"""
Facebook auto-post Medium articles via share dialog.
Uses facebook.com/sharer — navigates in SAME tab, waits for post to complete.

Usage: python3 scripts/facebook/auto_fb_post.py
Duration: 5 hours, posts every 15 minutes
"""

import subprocess
import time
import json
import random
import datetime
from pathlib import Path
from urllib.parse import quote

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
ARTICLES_FILE = PROJECT_DIR / "scripts" / "twitter" / "swiftui_articles.json"
PROGRESS_FILE = Path(__file__).resolve().parent / "fb_posted_parts.txt"
LOG_FILE = PROJECT_DIR / "logs" / "facebook-promo.log"
CHROME_PROFILE = "Profile 10"
DURATION_MINUTES = 300  # 5 hours
INTERVAL_MINUTES = 15

# Confirmed working coordinates (1366x768, English UI)
TEXT_AREA_X, TEXT_AREA_Y = 680, 307
POST_BTN_X, POST_BTN_Y = 676, 665


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


def log(msg):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def run_applescript(script):
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip(), result.returncode


def navigate_same_tab(url):
    """Navigate in the same tab — MUST be in Jeri profile window."""
    run_applescript(f'''
        tell application "Google Chrome"
            -- Find the Jeri profile window
            set targetWindow to missing value
            repeat with w in windows
                if name of w contains "Jeri" then
                    set targetWindow to w
                    exit repeat
                end if
            end repeat
            -- If no Jeri window found, use front window as fallback
            if targetWindow is missing value then
                set targetWindow to front window
            end if
            set URL of active tab of targetWindow to "{url}"
            set index of targetWindow to 1
        end tell
    ''')


def fb_share_post(share_url, post_text):
    """
    Core posting logic:
    1. Navigate to share URL in same tab
    2. Wait for dialog to load
    3. Click text area, paste text
    4. Dismiss hashtag popup
    5. Click Post
    6. WAIT for post to complete (15 sec)
    7. Return (don't close tab — will be reused)
    """

    # Step 1: Navigate to share dialog in same tab
    navigate_same_tab(share_url)
    time.sleep(8)  # Wait for page + dialog to fully load

    # Step 2: Activate Chrome
    run_applescript('tell application "Google Chrome" to activate')
    time.sleep(2)

    # Step 3: Click text area
    subprocess.run(["cliclick", f"c:{TEXT_AREA_X},{TEXT_AREA_Y}"], capture_output=True)
    time.sleep(1)

    # Step 4: Paste text
    subprocess.run(["pbcopy"], input=post_text.encode(), capture_output=True)
    time.sleep(0.3)
    run_applescript('tell application "System Events" to keystroke "v" using command down')
    time.sleep(3)  # Wait for text to fully render + link preview

    # Step 5: Dismiss hashtag popup if any
    run_applescript('tell application "System Events" to key code 53')
    time.sleep(1)

    # Step 6: Click "Post" button
    subprocess.run(["cliclick", f"c:{POST_BTN_X},{POST_BTN_Y}"], capture_output=True)
    log("Clicked Post — waiting for submission...")

    # Step 7: WAIT for post to complete
    # Facebook needs time to upload and process the post
    # The dialog will close when done — we just wait
    time.sleep(15)

    log("Post wait complete")
    return True


def post_to_facebook(article, list_url):
    """Post a Medium article to Facebook."""
    part = article["part"]
    title = article["title"]
    desc = article["desc"]
    url = article["url"] or list_url

    share_url = f"https://www.facebook.com/sharer/sharer.php?u={quote(url, safe='')}"

    post_text = (
        f"📱 Part {part}/100 — SwiftUI Zero to Expert\n\n"
        f"{title}\n\n"
        f"{desc}\n\n"
        f"Full series: {list_url}\n\n"
        f"#SwiftUI #iOS #iOSDev #100DaysOfCode #programming"
    )

    return fb_share_post(share_url, post_text)


def post_gumroad_promo(promo):
    """Post Gumroad product promo to Facebook."""
    share_url = f"https://www.facebook.com/sharer/sharer.php?u={quote(promo['url'], safe='')}"
    return fb_share_post(share_url, promo["text"])


# --- Gumroad promo posts ---

GUMROAD_POSTS = [
    {
        "url": "https://zerix1.gumroad.com/l/vrblqu",
        "text": "Nostr AI Toolkit — 9 Python scripts to monetize AI on the Nostr protocol.\n\nIncludes DVM, auto content, marketplace lister, and more.\nPure Python, no external deps.\n\n$19 on Gumroad\n\n#Python #Nostr #AI #DevTools"
    },
    {
        "url": "https://zerix1.gumroad.com/l/pzesvw",
        "text": "Ollama API Monetizer — Turn your local Ollama AI models into a paid API.\n\nLightning paywall + RapidAPI wrapper included.\n\n$14 on Gumroad\n\n#Ollama #AI #Python #PassiveIncome"
    },
    {
        "url": "https://zerix1.gumroad.com/l/ptikgy",
        "text": "Terminal Income Starter — Content publishing + staking scripts.\n\nPublish to dev.to, Hashnode, cross-post to Nostr. Solana and Cosmos staking setup.\n\n$9 on Gumroad\n\n#DevTools #PassiveIncome #Python"
    },
]


def main():
    log(f"=== FACEBOOK AUTO POST START ({DURATION_MINUTES} min) ===")

    data = load_articles()
    list_url = data["list_url"]
    posted = get_posted_parts()

    # Build queue: unposted Medium articles with URLs
    queue = []
    for a in sorted(data["articles"], key=lambda x: x["part"]):
        if a["part"] not in posted and a["url"]:
            queue.append(("medium", a))

    # Insert Gumroad promos every 5 posts
    final_queue = []
    gumroad_idx = 0
    for i, item in enumerate(queue):
        final_queue.append(item)
        if (i + 1) % 5 == 0 and gumroad_idx < len(GUMROAD_POSTS):
            final_queue.append(("gumroad", GUMROAD_POSTS[gumroad_idx]))
            gumroad_idx += 1

    log(f"Queue: {len(final_queue)} posts ({len(queue)} Medium + Gumroad promos)")

    # Step 0: Open Facebook in Chrome Profile 10 (Jeri) — first time only
    log("Opening Chrome Profile 10 (Jeri / 21zerixpm@gmail.com)...")
    subprocess.run([
        "open", "-na", "Google Chrome",
        "--args", f"--profile-directory={CHROME_PROFILE}",
        "https://www.facebook.com/"
    ], capture_output=True)
    time.sleep(8)
    run_applescript('tell application "Google Chrome" to activate')
    time.sleep(2)

    # Verify we're in the right profile
    title, _ = run_applescript('tell application "Google Chrome" to return name of front window')
    log(f"Chrome window: {title}")
    if "Jeri" not in title:
        log("WARNING: Not in Jeri profile! Trying to find Jeri window...")
        run_applescript('''
            tell application "Google Chrome"
                repeat with w in windows
                    if name of w contains "Jeri" then
                        set index of w to 1
                        exit repeat
                    end if
                end repeat
            end tell
        ''')
        time.sleep(1)

    start = time.time()
    end = start + (DURATION_MINUTES * 60)
    posted_count = 0
    idx = 0

    while time.time() < end and idx < len(final_queue):
        post_type, item = final_queue[idx]

        if post_type == "medium":
            article = item
            log(f"\n--- [{idx+1}/{len(final_queue)}] Medium Part {article['part']}: {article['title']} ---")
            try:
                post_to_facebook(article, list_url)
                mark_posted(article["part"])
                posted_count += 1
                log(f"POSTED OK ({posted_count} total)")
            except Exception as e:
                log(f"FAILED: {e}")
        else:
            promo = item
            log(f"\n--- [{idx+1}/{len(final_queue)}] Gumroad Promo ---")
            try:
                post_gumroad_promo(promo)
                posted_count += 1
                log(f"POSTED OK ({posted_count} total)")
            except Exception as e:
                log(f"FAILED: {e}")

        idx += 1
        remaining = end - time.time()
        if remaining > 0 and idx < len(final_queue):
            wait = INTERVAL_MINUTES * 60
            if remaining < wait:
                wait = remaining
            log(f"Waiting {int(wait/60)}m before next post...")
            time.sleep(wait)

    log(f"\n=== FB POST DONE: {posted_count} posts in {int((time.time()-start)/60)} min ===")


if __name__ == "__main__":
    main()
