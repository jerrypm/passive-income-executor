#!/usr/bin/env python3
"""Batch post SwiftUI Medium articles Part 51-60 to Twitter + Nostr (viral style)."""

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

# --- Viral tweets (hand-crafted for engagement) ---
VIRAL_TWEETS = {
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

    START = 51
    END = 60

    log(f"=== BATCH POST Part {START}-{END} (VIRAL EDITION) ===")

    for part_num in range(START, END + 1):
        if part_num in posted:
            log(f"Part {part_num} already posted, skipping.")
            continue

        if part_num not in VIRAL_TWEETS:
            log(f"Part {part_num} no viral tweet prepared, skipping.")
            continue

        tweet = VIRAL_TWEETS[part_num]
        char_count = len(tweet)

        if char_count > MAX_CHARS:
            log(f"[!!!] Part {part_num} tweet is {char_count} chars (MAX {MAX_CHARS})! SKIPPING.")
            continue

        article = articles_map.get(part_num, {})
        title = article.get("title", f"Part {part_num}")

        log(f"--- Part {part_num}: {title} ---")
        log(f"Twitter ({char_count} chars):\n{tweet}")

        # Post to Twitter
        try:
            post_twitter(tweet)
            log(f"Twitter: Part {part_num} POSTED")
        except Exception as e:
            log(f"Twitter FAILED Part {part_num}: {e}")

        time.sleep(3)

        # Post to Nostr (longer format)
        nostr_post = (
            f"\U0001f4f1 Part {part_num}/100 \u2014 SwiftUI Zero to Expert\n\n"
            f"{title}\n\n{article.get('desc', '')}\n\n"
            f"Read: {article.get('url', '')}\n\n"
            f"Full series: {list_url}\n\n"
            f"#SwiftUI #iOS #iOSDev #100DaysOfCode #programming"
        )
        try:
            post_nostr(nostr_post)
            log(f"Nostr: Part {part_num} POSTED")
        except Exception as e:
            log(f"Nostr FAILED Part {part_num}: {e}")

        # Mark as posted
        mark_posted(part_num)
        log(f"Part {part_num} DONE.")

        # Wait between posts
        if part_num < END:
            log(f"Waiting 15 seconds before next post...")
            time.sleep(15)

    log(f"=== BATCH COMPLETE Part {START}-{END} ===")

if __name__ == "__main__":
    main()
