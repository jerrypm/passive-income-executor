#!/usr/bin/env python3
"""
Post a Twitter thread via Chrome + AppleScript.
Opens compose, pastes tweets one by one using "+" button, then posts all.

Usage:
    python3 scripts/twitter/post_thread.py
    python3 scripts/twitter/post_thread.py --dry-run
    python3 scripts/twitter/post_thread.py --start 1 --end 10
"""

import sys
import time
import subprocess
import argparse
import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
CHROME_PROFILE = "Profile 10"
THREAD_FILE = PROJECT_DIR / "scripts" / "twitter" / "swiftui_thread.json"

LIST_URL = "https://medium.com/@21zerixpm/list/100daysswiftuitoexpert-069dcb77c2d2"


def run_applescript(script):
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip(), result.returncode, result.stderr.strip()


def post_thread_chrome(tweets):
    """Post a thread: open compose, paste first tweet, click + for each additional, then post all."""

    print(f"[*] Posting thread of {len(tweets)} tweets...")

    # Step 1: Open Twitter
    print("[*] Opening x.com/home...")
    subprocess.run([
        "open", "-na", "Google Chrome",
        "--args",
        f"--profile-directory={CHROME_PROFILE}",
        "https://x.com/home"
    ], capture_output=True)
    time.sleep(8)

    # Activate Chrome
    run_applescript('tell application "Google Chrome" to activate')
    time.sleep(1)

    # Escape anything
    run_applescript('''
    tell application "System Events"
        tell process "Google Chrome"
            key code 53
        end tell
    end tell
    ''')
    time.sleep(0.5)

    # Press N to open compose
    print("[*] Opening compose (N)...")
    run_applescript('''
    tell application "System Events"
        tell process "Google Chrome"
            keystroke "n"
        end tell
    end tell
    ''')
    time.sleep(3)

    for i, tweet in enumerate(tweets):
        if i > 0:
            # Click "+" button to add tweet to thread
            # The "+" button is typically at the bottom-right of the compose area
            # We'll use Tab to navigate to it or try clicking via coordinates
            print(f"[*] Adding tweet {i+1} to thread (clicking +)...")

            # Try using keyboard: Ctrl+Enter might add new tweet
            # Actually in Twitter web, the "Add another post" button needs clicking
            # Use Tab navigation: Tab several times to reach "+" then Enter
            # This is fragile but worth trying

            # Alternative: use mouse click via cliclick or Quartz
            try:
                import Quartz

                # Get Chrome window bounds
                bounds_str, _, _ = run_applescript('''
                tell application "Google Chrome"
                    set winBounds to bounds of front window
                    return (item 1 of winBounds) & "," & (item 2 of winBounds) & "," & (item 3 of winBounds) & "," & (item 4 of winBounds)
                end tell
                ''')
                if bounds_str:
                    parts = [int(x.strip()) for x in bounds_str.split(",")]
                    # "+" button is typically in the compose dialog
                    # It appears below the text area, left side
                    # Compose dialog is centered, roughly at:
                    # Center X of window, and the + button is at bottom-left of compose
                    cx = parts[0] + (parts[2] - parts[0]) // 2  # center x
                    # The + button vertical position depends on compose dialog
                    # It's usually at the bottom of the text area
                    # For a fresh compose: roughly 60% down from top of dialog
                    # The compose dialog is roughly 400px tall, starting from ~200px from top
                    # + button is at the very bottom of compose, left side
                    plus_x = cx - 200  # left side of compose
                    plus_y = parts[1] + 480 + (i * 120)  # shifts down as more tweets added

                    # Clamp to reasonable values
                    if plus_y > parts[3] - 100:
                        plus_y = parts[3] - 200

                    point = Quartz.CGPointMake(plus_x, plus_y)
                    Quartz.CGEventPost(Quartz.kCGHIDEventTap,
                        Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, point, Quartz.kCGMouseButtonLeft))
                    time.sleep(0.1)
                    Quartz.CGEventPost(Quartz.kCGHIDEventTap,
                        Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDown, point, Quartz.kCGMouseButtonLeft))
                    time.sleep(0.05)
                    Quartz.CGEventPost(Quartz.kCGHIDEventTap,
                        Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseUp, point, Quartz.kCGMouseButtonLeft))
                    print(f"[*] Clicked + at ({plus_x}, {plus_y})")
            except ImportError:
                # Fallback: try Tab key approach
                print("[*] Quartz not available, trying Tab approach...")
                for _ in range(3):
                    run_applescript('''
                    tell application "System Events"
                        tell process "Google Chrome"
                            keystroke tab
                        end tell
                    end tell
                    ''')
                    time.sleep(0.2)
                run_applescript('''
                tell application "System Events"
                    tell process "Google Chrome"
                        keystroke return
                    end tell
                end tell
                ''')

            time.sleep(1.5)

        # Paste tweet
        print(f"[*] Pasting tweet {i+1}/{len(tweets)}: {tweet[:50]}...")
        subprocess.run(["pbcopy"], input=tweet.encode(), capture_output=True)
        time.sleep(0.3)

        run_applescript('''
        tell application "System Events"
            tell process "Google Chrome"
                keystroke "v" using command down
            end tell
        end tell
        ''')
        time.sleep(1)

    # Post all with Cmd+Enter
    print("[*] Posting thread with Cmd+Enter...")
    time.sleep(2)
    run_applescript('''
    tell application "System Events"
        tell process "Google Chrome"
            keystroke return using command down
        end tell
    end tell
    ''')
    time.sleep(5)

    # Close tab
    run_applescript('''
    tell application "System Events"
        tell process "Google Chrome"
            keystroke "w" using command down
        end tell
    end tell
    ''')

    print("[+] Thread posted!")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--start", type=int, default=0, help="Start tweet index")
    parser.add_argument("--end", type=int, default=None, help="End tweet index")
    args = parser.parse_args()

    if not THREAD_FILE.exists():
        print(f"[!] Thread file not found: {THREAD_FILE}")
        sys.exit(1)

    with open(THREAD_FILE) as f:
        all_tweets = json.load(f)

    tweets = all_tweets[args.start:args.end]

    print(f"[*] Thread: {len(tweets)} tweets")
    for i, t in enumerate(tweets):
        print(f"  [{i+1}] ({len(t)} chars) {t[:80]}...")

    if args.dry_run:
        print("\n[DRY RUN] Not posting.")
        return

    post_thread_chrome(tweets)


if __name__ == "__main__":
    main()
