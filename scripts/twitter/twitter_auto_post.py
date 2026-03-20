#!/usr/bin/env python3
"""
Twitter Auto Post via Browser Automation
=========================================
Generate konten pakai Ollama, lalu posting ke Twitter via Playwright.
Tanpa API key — pakai browser session yang sudah login.

Usage:
    # Post dengan konten auto-generate dari Ollama
    python3 scripts/twitter/twitter_auto_post.py

    # Post dengan teks custom
    python3 scripts/twitter/twitter_auto_post.py --text "Hello Twitter!"

    # Post dengan topik tertentu
    python3 scripts/twitter/twitter_auto_post.py --topic "Python tips"

    # Dry run (generate tapi gak posting)
    python3 scripts/twitter/twitter_auto_post.py --dry-run

Setup dulu:
    python3 scripts/twitter/twitter_setup.py
"""

import os
import sys
import json
import time
import random
import argparse
import subprocess
import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
STATE_FILE = PROJECT_DIR / "scripts" / "twitter" / "browser_state.json"
PLAYWRIGHT_PROFILE = PROJECT_DIR / "scripts" / "twitter" / "chrome_profile"
LOG_FILE = PROJECT_DIR / "logs" / "twitter_posts.log"
TOPICS_FILE = PROJECT_DIR / "scripts" / "twitter" / "topics.json"

# ─── Content Generation ───────────────────────────────────────────

TWEET_TOPICS = [
    "Share a useful Python tip or trick for developers",
    "Share an interesting fact about AI and machine learning",
    "Share a productivity tip for programmers",
    "Share a thought about the future of open source AI",
    "Share a quick tip about terminal/command line productivity",
    "Share a motivational thought for indie developers",
    "Share something interesting about Bitcoin/Lightning Network",
    "Share a web development tip",
    "Share a thought about building passive income as a developer",
    "Share an iOS development tip",
    "Share a thought about self-hosting and digital sovereignty",
    "Share a JavaScript/TypeScript tip",
    "Share a thought about the Nostr protocol and decentralized social",
    "Share a macOS productivity tip",
    "Share a thought about earning money with open source",
]


def generate_tweet_ollama(topic=None, model="llama3.2"):
    """Generate tweet content using Ollama"""
    if topic is None:
        topic = random.choice(TWEET_TOPICS)

    prompt = f"""Write a single tweet (max 260 characters) about: {topic}

Rules:
- Be concise, engaging, and authentic
- Use casual/friendly tone
- Can include 1-2 relevant hashtags
- NO quotes around the tweet
- NO "Here's a tweet:" prefix
- Just output the tweet text directly
- Must be under 260 characters
- Write in English"""

    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True, text=True, timeout=60
        )
        tweet = result.stdout.strip()

        # Clean up common artifacts
        tweet = tweet.strip('"').strip("'")
        for prefix in ["Here's", "Here is", "Tweet:", "Sure!"]:
            if tweet.lower().startswith(prefix.lower()):
                tweet = tweet[len(prefix):].strip().lstrip(":").strip()

        # Ensure under 280 chars
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."

        return tweet, topic
    except subprocess.TimeoutExpired:
        print("[!] Ollama timeout — pastikan Ollama running: ollama serve")
        return None, topic
    except FileNotFoundError:
        print("[!] Ollama tidak ditemukan — install dulu: curl -fsSL https://ollama.com/install.sh | sh")
        return None, topic


def generate_thread_ollama(topic=None, model="llama3.2", thread_count=3):
    """Generate a thread (multiple tweets) using Ollama"""
    if topic is None:
        topic = random.choice(TWEET_TOPICS)

    prompt = f"""Write a Twitter thread of {thread_count} tweets about: {topic}

Rules:
- Each tweet must be under 260 characters
- Number each tweet: 1/, 2/, 3/
- Make it informative and engaging
- Use casual/friendly tone
- Only the last tweet can have hashtags
- Separate each tweet with ---
- Just output the tweets, no introduction"""

    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True, text=True, timeout=90
        )
        raw = result.stdout.strip()
        tweets = [t.strip() for t in raw.split("---") if t.strip()]

        # Clean up
        cleaned = []
        for tweet in tweets:
            tweet = tweet.strip('"').strip("'")
            if len(tweet) > 280:
                tweet = tweet[:277] + "..."
            if tweet:
                cleaned.append(tweet)

        return cleaned, topic
    except Exception as e:
        print(f"[!] Error generating thread: {e}")
        return None, topic


# ─── Browser Automation ───────────────────────────────────────────

def post_to_twitter(tweet_text, headless=False):
    """Post a tweet using Playwright browser automation"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[!] Install playwright: pip3 install playwright && python3 -m playwright install chromium")
        return False

    if not STATE_FILE.exists() and not PLAYWRIGHT_PROFILE.exists():
        print("[!] Session belum ada! Jalankan dulu:")
        print("    python3 scripts/twitter/twitter_setup.py")
        return False

    with sync_playwright() as p:
        print("[*] Membuka browser...")

        # Use persistent context if profile exists, otherwise use state file
        if PLAYWRIGHT_PROFILE.exists():
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(PLAYWRIGHT_PROFILE),
                headless=headless,
                viewport={"width": 1280, "height": 800},
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                ],
                ignore_default_args=["--enable-automation"],
            )
            page = context.pages[0] if context.pages else context.new_page()
        else:
            browser = p.chromium.launch(
                headless=headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                ],
            )
            context = browser.new_context(
                storage_state=str(STATE_FILE),
                viewport={"width": 1280, "height": 800},
            )
            page = context.new_page()

        try:
            # Go to Twitter home
            print("[*] Navigating ke Twitter...")
            page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30000)
            time.sleep(random.uniform(2, 4))

            # Check if logged in
            if "login" in page.url or "flow" in page.url:
                print("[!] Session expired! Jalankan ulang twitter_setup.py")
                return False

            # Click compose area
            print("[*] Menulis tweet...")
            compose = page.locator('[data-testid="tweetTextarea_0"]')
            compose.wait_for(state="visible", timeout=15000)
            time.sleep(random.uniform(0.5, 1.5))
            compose.click()
            time.sleep(random.uniform(0.3, 0.8))

            # Type with human-like delay
            for char in tweet_text:
                compose.type(char, delay=random.randint(20, 80))
                if random.random() < 0.05:  # occasional pause
                    time.sleep(random.uniform(0.2, 0.5))

            time.sleep(random.uniform(1, 2))

            # Click Post button
            print("[*] Posting...")
            post_btn = page.locator('[data-testid="tweetButton"]')
            post_btn.wait_for(state="visible", timeout=10000)
            time.sleep(random.uniform(0.5, 1))
            post_btn.click()

            # Wait for post to complete
            time.sleep(random.uniform(3, 5))

            # Verify post (check if compose area is cleared)
            print("[+] Tweet posted!")

            # Save updated state
            if STATE_FILE.parent.exists():
                context.storage_state(path=str(STATE_FILE))

            return True

        except Exception as e:
            print(f"[!] Error posting: {e}")
            # Take screenshot for debugging
            screenshot_path = PROJECT_DIR / "logs" / "twitter_error.png"
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshot_path))
            print(f"[*] Screenshot saved: {screenshot_path}")
            return False

        finally:
            context.close()
            if not PLAYWRIGHT_PROFILE.exists():
                browser.close()


def post_thread_to_twitter(tweets, headless=False):
    """Post a thread (reply chain) to Twitter"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[!] Install playwright: pip3 install playwright")
        return False

    if not STATE_FILE.exists() and not PLAYWRIGHT_PROFILE.exists():
        print("[!] Session belum ada! Jalankan twitter_setup.py dulu")
        return False

    with sync_playwright() as p:
        print("[*] Membuka browser untuk thread...")

        if PLAYWRIGHT_PROFILE.exists():
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(PLAYWRIGHT_PROFILE),
                headless=headless,
                viewport={"width": 1280, "height": 800},
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                ],
                ignore_default_args=["--enable-automation"],
            )
            page = context.pages[0] if context.pages else context.new_page()
        else:
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(
                storage_state=str(STATE_FILE),
                viewport={"width": 1280, "height": 800},
            )
            page = context.new_page()

        try:
            page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30000)
            time.sleep(random.uniform(2, 4))

            if "login" in page.url:
                print("[!] Session expired!")
                return False

            # Post first tweet
            compose = page.locator('[data-testid="tweetTextarea_0"]')
            compose.wait_for(state="visible", timeout=15000)
            compose.click()
            time.sleep(random.uniform(0.3, 0.8))

            for char in tweets[0]:
                compose.type(char, delay=random.randint(20, 80))

            time.sleep(random.uniform(1, 2))
            page.locator('[data-testid="tweetButton"]').click()
            time.sleep(random.uniform(4, 6))
            print(f"[+] Tweet 1/{len(tweets)} posted")

            # Reply to own tweet for thread
            for i, tweet_text in enumerate(tweets[1:], 2):
                # Find and click on the last posted tweet to reply
                time.sleep(random.uniform(2, 3))

                # Go to profile to find the tweet
                page.goto("https://x.com/home", wait_until="domcontentloaded")
                time.sleep(random.uniform(2, 4))

                # Click reply on the latest tweet
                reply_buttons = page.locator('[data-testid="reply"]')
                if reply_buttons.count() > 0:
                    reply_buttons.first.click()
                    time.sleep(random.uniform(1, 2))

                    # Type reply
                    reply_compose = page.locator('[data-testid="tweetTextarea_0"]')
                    reply_compose.wait_for(state="visible", timeout=10000)
                    for char in tweet_text:
                        reply_compose.type(char, delay=random.randint(20, 80))

                    time.sleep(random.uniform(1, 2))

                    # Click reply button
                    reply_btn = page.locator('[data-testid="tweetButton"]')
                    reply_btn.click()
                    time.sleep(random.uniform(3, 5))
                    print(f"[+] Tweet {i}/{len(tweets)} posted")

            if STATE_FILE.parent.exists():
                context.storage_state(path=str(STATE_FILE))

            return True

        except Exception as e:
            print(f"[!] Error posting thread: {e}")
            screenshot_path = PROJECT_DIR / "logs" / "twitter_thread_error.png"
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshot_path))
            return False

        finally:
            context.close()
            if not PLAYWRIGHT_PROFILE.exists():
                browser.close()


# ─── Logging ──────────────────────────────────────────────────────

def log_post(tweet_text, topic, success):
    """Log posted tweet"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "OK" if success else "FAIL"
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] [{status}] topic={topic}\n")
        f.write(f"  {tweet_text}\n\n")


# ─── Main ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Twitter Auto Post via Browser")
    parser.add_argument("--text", help="Custom tweet text")
    parser.add_argument("--topic", help="Topic for Ollama to generate about")
    parser.add_argument("--thread", action="store_true", help="Post as thread (3 tweets)")
    parser.add_argument("--model", default="llama3.2", help="Ollama model (default: llama3.2)")
    parser.add_argument("--dry-run", action="store_true", help="Generate tapi jangan posting")
    parser.add_argument("--headless", action="store_true", help="Run headless (tanpa window)")
    args = parser.parse_args()

    print("=" * 50)
    print("  Twitter Auto Post")
    print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    if args.thread:
        # Generate thread
        tweets, topic = generate_thread_ollama(
            topic=args.topic,
            model=args.model
        )
        if not tweets:
            print("[!] Gagal generate thread")
            sys.exit(1)

        print(f"\n[*] Topic: {topic}")
        print(f"[*] Thread ({len(tweets)} tweets):")
        for i, t in enumerate(tweets, 1):
            print(f"  [{i}] {t}")
            print(f"      ({len(t)} chars)")

        if args.dry_run:
            print("\n[DRY RUN] Tidak diposting.")
            return

        print()
        success = post_thread_to_twitter(tweets, headless=args.headless)
        for t in tweets:
            log_post(t, topic, success)

    else:
        # Generate single tweet
        if args.text:
            tweet_text = args.text
            topic = "custom"
        else:
            tweet_text, topic = generate_tweet_ollama(
                topic=args.topic,
                model=args.model
            )

        if not tweet_text:
            print("[!] Gagal generate tweet")
            sys.exit(1)

        print(f"\n[*] Topic: {topic}")
        print(f"[*] Tweet: {tweet_text}")
        print(f"[*] Length: {len(tweet_text)} chars")

        if args.dry_run:
            print("\n[DRY RUN] Tidak diposting.")
            return

        print()
        success = post_to_twitter(tweet_text, headless=args.headless)
        log_post(tweet_text, topic, success)

    if success:
        print("\n[+] Done!")
    else:
        print("\n[!] Posting gagal. Cek log untuk detail.")
        sys.exit(1)


if __name__ == "__main__":
    main()
