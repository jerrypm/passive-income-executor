#!/usr/bin/env python3
"""Retry posting Part 51-58 to Twitter (failed on 2026-04-02 due to AppleScript timeout)."""

import subprocess
import time
import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
LOG_FILE = PROJECT_DIR / "logs" / "medium-daily.log"
CHROME_PROFILE = "Profile 10"

# The 8 tweets that failed yesterday
TWEETS = {
    51: (
        "\U0001f9ed Part 51/100 \u2014 Navigation Patterns in SwiftUI\n\n"
        "Stop hardcoding navigation. Build it to scale.\n\n"
        "https://21zerixpm.medium.com/navigation-patterns-in-swiftui-building-scalable-navigation-636e44f1f2aa\n\n"
        "#SwiftUI #100DaysOfCode #iOSDev"
    ),
    52: (
        "\U0001f9ed Part 52/100 \u2014 Coordinator Pattern in SwiftUI\n\n"
        "Your views shouldn't know where to go next. Let Coordinators handle it.\n\n"
        "https://21zerixpm.medium.com/coordinator-pattern-in-swiftui-managing-complex-navigation-flows-87434026961e\n\n"
        "#SwiftUI #100DaysOfCode #iOSDev"
    ),
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
}


def run_applescript(script, timeout=60):
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=timeout
    )
    return result.stdout.strip(), result.returncode, result.stderr.strip()


def ensure_chrome_open():
    """Make sure Chrome is open with Profile 10."""
    subprocess.run([
        "open", "-na", "Google Chrome",
        "--args", f"--profile-directory={CHROME_PROFILE}",
        "https://x.com/compose/post"
    ], capture_output=True)
    time.sleep(8)
    run_applescript('tell application "Google Chrome" to activate')
    time.sleep(2)


def post_twitter(text, part_num):
    """Post a tweet using Chrome Profile 10 via compose URL."""
    log(f"Opening compose for Part {part_num}...")

    # Open compose URL directly (skips needing to press 'n')
    script_open = f'''
    tell application "Google Chrome"
        activate
        set found to false
        repeat with w in windows
            repeat with t in tabs of w
                if URL of t contains "x.com" or URL of t contains "twitter.com" then
                    set URL of t to "https://x.com/compose/post"
                    set active tab index of w to (index of t)
                    set found to true
                    exit repeat
                end if
            end repeat
            if found then exit repeat
        end repeat
        if not found then
            tell window 1
                set URL of active tab to "https://x.com/compose/post"
            end tell
        end if
    end tell
    '''
    run_applescript(script_open)
    time.sleep(5)

    # Copy tweet to clipboard
    subprocess.run(["pbcopy"], input=text.encode(), capture_output=True)
    time.sleep(0.5)

    # Paste
    run_applescript(
        'tell application "System Events" to tell process "Google Chrome" '
        'to keystroke "v" using command down'
    )
    time.sleep(2)

    # Click Post button (Cmd+Enter)
    run_applescript(
        'tell application "System Events" to tell process "Google Chrome" '
        'to keystroke return using command down'
    )
    time.sleep(5)

    log(f"Twitter: Part {part_num} POSTED (retry)")
    return True


def log(msg):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def main():
    log("=== RETRY FAILED POSTS Part 51-58 ===")

    # Open Chrome first
    ensure_chrome_open()

    for part_num in sorted(TWEETS.keys()):
        tweet = TWEETS[part_num]
        char_count = len(tweet)
        log(f"--- Part {part_num} ({char_count} chars) ---")

        if char_count > 277:
            log(f"[!!!] Part {part_num} is {char_count} chars > 277! SKIPPING.")
            continue

        try:
            post_twitter(tweet, part_num)
        except Exception as e:
            log(f"Twitter FAILED Part {part_num}: {e}")

        # Wait between posts
        if part_num < max(TWEETS.keys()):
            wait = 20
            log(f"Waiting {wait}s before next post...")
            time.sleep(wait)

    log("=== RETRY COMPLETE Part 51-58 ===")


if __name__ == "__main__":
    main()
