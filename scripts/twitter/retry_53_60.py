#!/usr/bin/env python3
"""
Retry posting Part 53-60 to Twitter.
Uses the same Quartz mouse-click approach as quick_post.py (which worked for Part 41-50).

Flow per tweet:
1. Navigate tab to x.com/home
2. Click page center via Quartz (ensure page focus, not address bar)
3. Press "n" (Twitter compose shortcut)
4. Paste tweet via Cmd+V
5. Post via Cmd+Enter
6. Wait before next
"""

import subprocess
import time
import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
LOG_FILE = PROJECT_DIR / "logs" / "medium-daily.log"
CHROME_PROFILE = "Profile 10"

TWEETS = {
    53: (
        "\U0001f9ed Part 53/100 \u2014 Router Pattern in SwiftUI\n\n"
        "Type-safe navigation. Catch bugs at compile time, not runtime.\n\n"
        "https://21zerixpm.medium.com/router-pattern-in-swiftui-type-safe-navigation-made-simple-7bcf5178bbe0\n\n"
        "#SwiftUI #100DaysOfCode #iOSDev"
    ),
    54: (
        "\U0001f3d7\ufe0f Part 54/100 \u2014 Clean Architecture in SwiftUI\n\n"
        "Spaghetti code? Never again. Separate concerns properly.\n\n"
        "https://medium.com/codetodeploy/clean-architecture-in-swiftui-building-maintainable-apps-c2e428983f46\n\n"
        "#SwiftUI #100DaysOfCode #iOSDev"
    ),
    55: (
        "\U0001f3d7\ufe0f Part 55/100 \u2014 MVVM Architecture in SwiftUI\n\n"
        "The complete MVVM guide. No more messy Views.\n\n"
        "https://21zerixpm.medium.com/mvvm-architecture-in-swiftui-the-complete-guide-8e9a78b42ac1\n\n"
        "#SwiftUI #100DaysOfCode #iOSDev"
    ),
    56: (
        "\U0001f3d7\ufe0f Part 56/100 \u2014 VIPER Architecture in SwiftUI\n\n"
        "Enterprise apps need enterprise patterns. VIPER keeps it clean at scale.\n\n"
        "https://21zerixpm.medium.com/viper-architecture-in-swiftui-enterprise-grade-app-structure-a8a00b4601a7\n\n"
        "#SwiftUI #100DaysOfCode #iOSDev"
    ),
    57: (
        "\U0001f3d7\ufe0f Part 57/100 \u2014 Modular App Architecture\n\n"
        "Your app will grow. Plan for it now with modular architecture.\n\n"
        "https://21zerixpm.medium.com/modular-app-architecture-in-swiftui-scaling-your-codebase-b35eb985eb61\n\n"
        "#SwiftUI #100DaysOfCode #iOSDev"
    ),
    58: (
        "\U0001f4e6 Part 58/100 \u2014 App Structure Best Practices\n\n"
        "Good folder structure = faster development. Organize it right from day 1.\n\n"
        "https://21zerixpm.medium.com/app-structure-best-practices-in-swiftui-organizing-your-project-4664894d497b\n\n"
        "#SwiftUI #100DaysOfCode #iOSDev"
    ),
    59: (
        "\U0001f4e6 Part 59/100 \u2014 Multi-Window Support in SwiftUI\n\n"
        "iPadOS + macOS multi-window. One codebase, multiple windows.\n\n"
        "https://21zerixpm.medium.com/multi-window-support-in-swiftui-ipados-and-macos-53daa5a2e94e\n\n"
        "#SwiftUI #100DaysOfCode #iOSDev"
    ),
    60: (
        "\U0001f4e6 Part 60/100 \u2014 Widget Integration in SwiftUI\n\n"
        "Home + Lock screen widgets. Keep users engaged without opening your app.\n\n"
        "https://21zerixpm.medium.com/widget-integration-in-swiftui-home-screen-and-lock-screen-widgets-9935bb118564\n\n"
        "#SwiftUI #100DaysOfCode #iOSDev"
    ),
}


def run_applescript(script, timeout=60):
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=timeout
        )
        return result.stdout.strip(), result.returncode, result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "", 1, "TIMEOUT"


def log(msg):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def click_page_center():
    """Click center of Chrome window using Quartz to ensure page has focus."""
    try:
        import Quartz
        bounds_str, rc, _ = run_applescript('''
            tell application "Google Chrome"
                set winBounds to bounds of front window
                return (item 1 of winBounds) & "," & (item 2 of winBounds) & "," & (item 3 of winBounds) & "," & (item 4 of winBounds)
            end tell
        ''')
        if bounds_str and rc == 0:
            parts = [int(x.strip()) for x in bounds_str.split(",")]
            cx = parts[0] + (parts[2] - parts[0]) // 2
            cy = parts[1] + 400  # Well below toolbar, in page content area
            point = Quartz.CGPointMake(cx, cy)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap,
                Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, point, Quartz.kCGMouseButtonLeft))
            time.sleep(0.1)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap,
                Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDown, point, Quartz.kCGMouseButtonLeft))
            time.sleep(0.05)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap,
                Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseUp, point, Quartz.kCGMouseButtonLeft))
            log(f"  Quartz click at ({cx}, {cy})")
            return True
    except Exception as e:
        log(f"  Quartz click failed: {e}")
    return False


def post_one_tweet(text, part_num):
    """Post a single tweet using the reliable quick_post.py approach."""

    # Step 1: Navigate to x.com/home in active tab
    log(f"  Step 1: Navigate to x.com/home")
    run_applescript('''
        tell application "Google Chrome"
            activate
            tell active tab of window 1
                set URL to "https://x.com/home"
            end tell
        end tell
    ''')
    time.sleep(7)

    # Step 2: Activate Chrome and ensure focus
    log(f"  Step 2: Activate Chrome")
    run_applescript('tell application "Google Chrome" to activate')
    time.sleep(1)

    # Step 3: Click page center with Quartz (like quick_post.py)
    log(f"  Step 3: Click page center")
    click_page_center()
    time.sleep(1)

    # Step 4: Press "n" to open compose dialog
    log(f"  Step 4: Press 'n' for compose")
    out, rc, err = run_applescript('''
        tell application "System Events"
            tell process "Google Chrome"
                keystroke "n"
            end tell
        end tell
    ''')
    if rc != 0:
        log(f"  [!] keystroke 'n' failed: {err}")
        return False
    time.sleep(4)

    # Step 5: Paste tweet text
    log(f"  Step 5: Paste tweet")
    subprocess.run(["pbcopy"], input=text.encode(), capture_output=True)
    time.sleep(0.5)

    out, rc, err = run_applescript('''
        tell application "System Events"
            tell process "Google Chrome"
                keystroke "v" using command down
            end tell
        end tell
    ''')
    if rc != 0:
        log(f"  [!] Paste failed: {err}")
        return False
    time.sleep(2)

    # Step 6: Post with Cmd+Enter
    log(f"  Step 6: Cmd+Enter to post")
    out, rc, err = run_applescript('''
        tell application "System Events"
            tell process "Google Chrome"
                keystroke return using command down
            end tell
        end tell
    ''')
    if rc != 0:
        log(f"  [!] Cmd+Enter failed: {err}")
        return False
    time.sleep(6)

    log(f"  DONE - Part {part_num} posted")
    return True


def main():
    log("=== RETRY Part 53-60 (Quartz click approach) ===")

    # Open Chrome Profile 10 first
    log("Opening Chrome Profile 10 to x.com/home...")
    subprocess.run([
        "open", "-na", "Google Chrome",
        "--args", f"--profile-directory={CHROME_PROFILE}",
        "https://x.com/home"
    ], capture_output=True)
    time.sleep(10)
    run_applescript('tell application "Google Chrome" to activate')
    time.sleep(2)

    for part_num in sorted(TWEETS.keys()):
        tweet = TWEETS[part_num]
        char_count = len(tweet)

        log(f"--- Part {part_num} ({char_count} chars) ---")

        if char_count > 277:
            log(f"  [!!!] {char_count} chars > 277! SKIPPING.")
            continue

        success = post_one_tweet(tweet, part_num)

        if success:
            log(f"  Twitter: Part {part_num} POSTED")
        else:
            log(f"  Twitter: Part {part_num} FAILED")

        # Wait between posts (avoid rate limit + give time for UI)
        if part_num < max(TWEETS.keys()):
            wait = 25
            log(f"  Waiting {wait}s before next post...")
            time.sleep(wait)

    log("=== RETRY COMPLETE Part 53-60 ===")


if __name__ == "__main__":
    main()
