#!/usr/bin/env python3
"""
Twitter auto-promo for 1 hour.
Posts promotional tweets about Medium series and Gumroad products.
Rotates between different tweet types every 5 minutes.
Max 277 chars per tweet enforced.

Usage: python3 scripts/twitter/auto_promo_1hr.py
"""

import subprocess
import time
import random
import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
LOG_FILE = PROJECT_DIR / "logs" / "twitter-promo.log"
CHROME_PROFILE = "Profile 10"
MAX_CHARS = 277
DURATION_MINUTES = 60
INTERVAL_MINUTES = 5

# --- Tweet Library ---

GUMROAD_TWEETS = [
    "Built 3 Python toolkits for passive income:\n\n- Nostr AI Toolkit ($19)\n- Ollama API Monetizer ($14)\n- Terminal Income Starter ($9)\n\nAll from terminal. No deps.\n\nhttps://zerix1.gumroad.com",
    "Want to monetize your local AI? I made a toolkit for that.\n\nOllama API Monetizer - turn any Ollama model into a paid API.\n\n$14 on Gumroad:\nhttps://zerix1.gumroad.com/l/pzesvw",
    "9 Python scripts to earn sats on Nostr:\n\n- AI DVM (text generation)\n- Auto content poster\n- Marketplace lister\n- Profile updater\n\nAll pure Python, zero deps.\n\nhttps://zerix1.gumroad.com/l/vrblqu",
    "Start earning from terminal today:\n\n- Publish to dev.to + Hashnode\n- Solana staking setup\n- Cosmos staking setup\n- Bandwidth sharing\n\n$9 starter kit:\nhttps://zerix1.gumroad.com/l/ptikgy",
    "If you have Ollama running locally, you can monetize it.\n\nI built scripts for Lightning paywall + RapidAPI wrapper.\n\n$14:\nhttps://zerix1.gumroad.com/l/pzesvw",
]

MEDIUM_TWEETS = [
    "Writing 100 Days of SwiftUI - Zero to Expert on Medium.\n\nPart 1-20 out now. From basics to custom layouts.\n\nFull series:\nhttps://medium.com/@21zerixpm/list/100daysswiftuitoexpert-069dcb77c2d2",
    "SwiftUI tip: NavigationStack > NavigationView in iOS 16+.\n\nI break it down in Part 12 of my 100-day series.\n\nhttps://medium.com/@21zerixpm/list/100daysswiftuitoexpert-069dcb77c2d2",
    "Learning SwiftUI? I'm writing a 100-part series.\n\nCovers: Views, Modifiers, Layout, Animations, Gestures, Navigation, and more.\n\nFree on Medium:\nhttps://medium.com/@21zerixpm/list/100daysswiftuitoexpert-069dcb77c2d2",
    "SwiftUI animations are easier than you think.\n\nwithAnimation, matchedGeometryEffect, transitions - all in Part 13.\n\nhttps://medium.com/@21zerixpm/list/100daysswiftuitoexpert-069dcb77c2d2",
    "Custom shapes in SwiftUI using Path and Shape protocol.\n\nDraw anything you can imagine. Part 17 of my series.\n\nhttps://medium.com/@21zerixpm/list/100daysswiftuitoexpert-069dcb77c2d2",
]

DEV_TWEETS = [
    "Running Ollama locally? You're sitting on a money machine.\n\nllama3, deepseek, codellama - all can be monetized via API paywall.\n\nI built the scripts:\nhttps://zerix1.gumroad.com/l/pzesvw",
    "Nostr is the next frontier for devs.\n\nNo API keys. No rate limits. Post, sell, earn - all via CLI.\n\nI made a toolkit:\nhttps://zerix1.gumroad.com/l/vrblqu",
    "Passive income as a developer doesn't need a SaaS.\n\nStaking, bandwidth sharing, content publishing, AI inference - all from terminal.",
    "Every developer should have multiple income streams.\n\nI set up 6 in one week using just my terminal and Python scripts.",
    "SwiftUI + Python + terminal = my income stack.\n\niOS apps, AI toolkits, content publishing.\n\nAll automated.",
]

ALL_TWEETS = GUMROAD_TWEETS + MEDIUM_TWEETS + DEV_TWEETS


# --- Functions ---

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


def post_tweet(text):
    """Post a tweet via Chrome automation."""
    if len(text) > MAX_CHARS:
        log(f"SKIP: Tweet too long ({len(text)} chars): {text[:50]}...")
        return False

    # Activate Chrome
    run_applescript('tell application "Google Chrome" to activate')
    time.sleep(1)

    # Press Esc then N for new tweet
    run_applescript('tell application "System Events" to key code 53')
    time.sleep(0.5)
    run_applescript('tell application "System Events" to keystroke "n"')
    time.sleep(3)

    # Copy tweet and paste
    subprocess.run(["pbcopy"], input=text.encode(), capture_output=True)
    time.sleep(0.3)
    run_applescript('tell application "System Events" to keystroke "v" using command down')
    time.sleep(2)

    # Post with Cmd+Enter
    run_applescript('tell application "System Events" to keystroke return using command down')
    time.sleep(4)

    # Close compose with Esc
    run_applescript('tell application "System Events" to key code 53')
    time.sleep(1)

    return True


def main():
    log(f"=== TWITTER AUTO PROMO START ({DURATION_MINUTES} min) ===")

    # Open Twitter
    subprocess.run([
        "open", "-na", "Google Chrome",
        "--args", f"--profile-directory={CHROME_PROFILE}",
        "https://x.com/home"
    ], capture_output=True)
    time.sleep(8)

    # Shuffle tweets
    tweets = ALL_TWEETS.copy()
    random.shuffle(tweets)

    # Validate all tweets
    for t in tweets:
        if len(t) > MAX_CHARS:
            log(f"WARNING: Tweet {len(t)} chars (max {MAX_CHARS}): {t[:50]}...")

    start = time.time()
    end = start + (DURATION_MINUTES * 60)
    posted = 0
    idx = 0

    while time.time() < end and idx < len(tweets):
        tweet = tweets[idx]
        log(f"\n--- Tweet {posted + 1} ({len(tweet)} chars) ---")
        log(f"Content: {tweet[:80]}...")

        if post_tweet(tweet):
            posted += 1
            log(f"POSTED OK ({posted} total)")
        else:
            log("SKIPPED")

        idx += 1
        remaining = end - time.time()
        if remaining > 0 and idx < len(tweets):
            wait = INTERVAL_MINUTES * 60
            if remaining < wait:
                wait = remaining
            log(f"Waiting {int(wait/60)}m before next tweet...")
            time.sleep(wait)

    log(f"\n=== PROMO DONE: {posted} tweets in {int((time.time()-start)/60)} min ===")


if __name__ == "__main__":
    main()
