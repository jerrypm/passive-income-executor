#!/usr/bin/env python3
"""
Twitter Quick Post via Chrome + AppleScript
============================================
Kontrol Chrome langsung — buka Twitter, compose, paste, post.
Tab/window lain TIDAK diganggu.

Usage:
    python3 scripts/twitter/quick_post.py
    python3 scripts/twitter/quick_post.py --text "Hello Twitter!"
    python3 scripts/twitter/quick_post.py --dry-run
"""

import sys
import time
import random
import subprocess
import datetime
import argparse
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
LOG_FILE = PROJECT_DIR / "logs" / "twitter_posts.log"
CHROME_PROFILE = "Profile 10"  # Jeri - 21zerixpm@gmail.com


# ─── Content Generation ───────────────────────────────────────────

TWEET_TOPICS = [
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


def generate_tweet(topic=None, model="llama3.2"):
    if topic is None:
        topic = random.choice(TWEET_TOPICS)
    prompt = f"""Write a single tweet (max 250 characters) about: {topic}

Rules:
- Concise, engaging, authentic, casual tone
- Can include 1-2 hashtags
- NO quotes, NO prefix like "Here's a tweet:"
- Just the tweet text, nothing else
- Under 250 characters, English"""
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
        if len(tweet) > 277:
            # Potong di word boundary terakhir sebelum 277 chars
            tweet = tweet[:274].rsplit(' ', 1)[0] + "..."
        return tweet, topic
    except Exception as e:
        print(f"[!] Ollama error: {e}")
        return None, topic


def run_applescript(script):
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip(), result.returncode, result.stderr.strip()


def post_tweet_chrome(tweet_text):
    """Post tweet: open Twitter home > press N > paste > Cmd+Enter"""

    # Step 1: Open Twitter home in Chrome profile Jeri
    print("[*] Opening x.com/home in Chrome (Profile Jeri)...")
    subprocess.run([
        "open", "-na", "Google Chrome",
        "--args",
        f"--profile-directory={CHROME_PROFILE}",
        "https://x.com/home"
    ], capture_output=True)

    print("[*] Waiting for page to load...")
    time.sleep(8)

    # Step 2: Bring Chrome to front
    print("[*] Activating Chrome...")
    run_applescript('tell application "Google Chrome" to activate')
    time.sleep(1)

    # Step 3: Click somewhere safe on the page first (to ensure page has focus, not address bar)
    # Use mouse click via AppleScript at a neutral position
    click_page_script = '''
    tell application "Google Chrome"
        activate
        set winBounds to bounds of front window
        set winX to item 1 of winBounds
        set winY to item 2 of winBounds
        set winW to item 3 of winBounds
        set winH to item 4 of winBounds
        -- Calculate center-ish point (below toolbar)
        set clickX to winX + ((winW - winX) / 2)
        set clickY to winY + 300
    end tell

    tell application "System Events"
        click at {clickX, clickY}
    end tell
    '''
    # System Events "click at" might not work, try alternative
    # First, just press Escape to dismiss anything, then click body
    esc_script = '''
    tell application "System Events"
        tell process "Google Chrome"
            key code 53
        end tell
    end tell
    '''
    run_applescript(esc_script)
    time.sleep(0.5)

    # Click in the page content area using mouse move + click
    # Use Python to do a mouse click via Quartz
    try:
        import Quartz
        # Get Chrome window position
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
            cy = parts[1] + 350  # Below toolbar, in page content

            # Move mouse and click
            point = Quartz.CGPointMake(cx, cy)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap,
                Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, point, Quartz.kCGMouseButtonLeft))
            time.sleep(0.1)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap,
                Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDown, point, Quartz.kCGMouseButtonLeft))
            time.sleep(0.05)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap,
                Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseUp, point, Quartz.kCGMouseButtonLeft))
            print(f"[*] Clicked at ({cx}, {cy}) to focus page")
        else:
            print("[*] Could not get window bounds, trying without click")
    except ImportError:
        print("[*] Quartz not available, trying without click")

    time.sleep(1)

    # Step 4: Press "N" — Twitter keyboard shortcut to open compose
    print("[*] Pressing 'N' to open compose...")
    n_script = '''
    tell application "System Events"
        tell process "Google Chrome"
            keystroke "n"
        end tell
    end tell
    '''
    out, code, err = run_applescript(n_script)
    if code != 0:
        print(f"[!] Keystroke error: {err}")
        return False

    # Wait for compose dialog to open
    time.sleep(3)

    # Step 5: Copy tweet text to clipboard and paste
    print("[*] Pasting tweet...")
    subprocess.run(["pbcopy"], input=tweet_text.encode(), capture_output=True)
    time.sleep(0.3)

    paste_script = '''
    tell application "System Events"
        tell process "Google Chrome"
            keystroke "v" using command down
        end tell
    end tell
    '''
    out, code, err = run_applescript(paste_script)
    if code != 0:
        print(f"[!] Paste error: {err}")
        return False
    print("[+] Tweet pasted!")

    time.sleep(2)

    # Step 6: Post with Cmd+Enter
    print("[*] Posting with Cmd+Enter...")
    post_script = '''
    tell application "System Events"
        tell process "Google Chrome"
            keystroke return using command down
        end tell
    end tell
    '''
    out, code, err = run_applescript(post_script)
    if code != 0:
        print(f"[!] Post error: {err}")
        return False

    time.sleep(4)
    print("[+] Tweet posted!")

    # Step 7: Close the tab (Cmd+W)
    close_script = '''
    tell application "System Events"
        tell process "Google Chrome"
            keystroke "w" using command down
        end tell
    end tell
    '''
    run_applescript(close_script)
    print("[*] Tab closed")

    return True


def log_post(tweet_text, topic, success):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "OK" if success else "FAIL"
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] [{status}] topic={topic}\n")
        f.write(f"  {tweet_text}\n\n")


def main():
    parser = argparse.ArgumentParser(description="Twitter Auto Post via Chrome")
    parser.add_argument("--text", help="Custom tweet text")
    parser.add_argument("--topic", help="Topic for Ollama")
    parser.add_argument("--model", default="llama3.2", help="Ollama model")
    parser.add_argument("--dry-run", action="store_true", help="Generate only")
    args = parser.parse_args()

    print("=" * 50)
    print("  Twitter Auto Post (Chrome + AppleScript)")
    print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("  Chrome tabs lain TIDAK diganggu")
    print("=" * 50)

    if args.text:
        tweet_text = args.text
        topic = "custom"
    else:
        print("\n[*] Generating tweet via Ollama...")
        tweet_text, topic = generate_tweet(topic=args.topic, model=args.model)

    if not tweet_text:
        print("[!] Failed to generate tweet")
        sys.exit(1)

    # Enforce 277 char limit for Twitter/X (safe margin under 280)
    if len(tweet_text) > 277:
        print(f"[!] Tweet too long ({len(tweet_text)} chars). Max 277.")
        tweet_text = tweet_text[:274].rsplit(' ', 1)[0] + "..."
        print(f"[*] Auto-truncated to {len(tweet_text)} chars")

    print(f"\n[*] Topic: {topic}")
    print(f"[*] Tweet: {tweet_text}")
    print(f"[*] Length: {len(tweet_text)} chars")

    if args.dry_run:
        print("\n[DRY RUN] Tidak diposting.")
        return

    print()
    success = post_tweet_chrome(tweet_text)
    log_post(tweet_text, topic, success)

    if success:
        print("\n[+] DONE!")
    else:
        print("\n[!] Failed. Coba enable 'Allow JavaScript from Apple Events' di Chrome.")
        sys.exit(1)


if __name__ == "__main__":
    main()
