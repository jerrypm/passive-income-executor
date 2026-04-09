#!/usr/bin/env python3
"""
Post Part 52-60 to Twitter via CGEvent (JXA).
Same flow as test_post_51.py which posted successfully.
"""

import subprocess
import time
import datetime
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent.parent / "logs" / "medium-daily.log"
CHROME_PROFILE = "Profile 10"

TWEETS = {
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

# CGEvent key codes
KEY_V = 9
KEY_N = 45
KEY_RETURN = 36


def osa(script, timeout=30):
    r = subprocess.run(["osascript", "-e", script],
                       capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip(), r.returncode


def jxa(code, timeout=15):
    r = subprocess.run(["osascript", "-l", "JavaScript", "-e", code],
                       capture_output=True, text=True, timeout=timeout)
    return r.returncode


def cg_click(x, y):
    jxa(f'''
    ObjC.import('Cocoa');
    var pt = $.CGPointMake({x}, {y});
    var mv = $.CGEventCreateMouseEvent($(), $.kCGEventMouseMoved, pt, $.kCGMouseButtonLeft);
    $.CGEventPost($.kCGHIDEventTap, mv);
    delay(0.1);
    var dn = $.CGEventCreateMouseEvent($(), $.kCGEventLeftMouseDown, pt, $.kCGMouseButtonLeft);
    $.CGEventPost($.kCGHIDEventTap, dn);
    delay(0.05);
    var up = $.CGEventCreateMouseEvent($(), $.kCGEventLeftMouseUp, pt, $.kCGMouseButtonLeft);
    $.CGEventPost($.kCGHIDEventTap, up);
    ''')


def cg_key(keycode, cmd=False):
    flags = "$.kCGEventFlagMaskCommand" if cmd else "0"
    jxa(f'''
    ObjC.import('Cocoa');
    var down = $.CGEventCreateKeyboardEvent($(), {keycode}, true);
    $.CGEventSetFlags(down, {flags});
    $.CGEventPost($.kCGHIDEventTap, down);
    delay(0.05);
    var up = $.CGEventCreateKeyboardEvent($(), {keycode}, false);
    $.CGEventSetFlags(up, {flags});
    $.CGEventPost($.kCGHIDEventTap, up);
    ''')


def get_bounds():
    out, rc = osa('''
        tell application "Google Chrome"
            set b to bounds of front window
            set AppleScript's text item delimiters to ","
            return b as text
        end tell
    ''')
    if out and rc == 0:
        try:
            return [int(x.strip()) for x in out.split(",")]
        except ValueError:
            pass
    return None


def log(msg):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def post_one(text, part_num):
    """Post a single tweet — same flow as test_post_51.py."""
    # Navigate to x.com/home
    osa('''
        tell application "Google Chrome"
            activate
            tell active tab of window 1
                set URL to "https://x.com/home"
            end tell
        end tell
    ''')
    time.sleep(7)

    # Click page center
    bounds = get_bounds()
    if bounds:
        cx = bounds[0] + (bounds[2] - bounds[0]) // 2
        cy = bounds[1] + 400
        cg_click(cx, cy)
    time.sleep(1)

    # Press N to open compose
    cg_key(KEY_N)
    time.sleep(4)

    # Paste
    subprocess.run(["pbcopy"], input=text.encode(), capture_output=True)
    time.sleep(0.5)
    cg_key(KEY_V, cmd=True)
    time.sleep(3)

    # Post with Cmd+Return
    cg_key(KEY_RETURN, cmd=True)
    time.sleep(5)

    return True


def main():
    log("=== BATCH POST Part 52-60 (CGEvent) ===")

    # Open Chrome Profile 10
    subprocess.run([
        "open", "-na", "Google Chrome",
        "--args", f"--profile-directory={CHROME_PROFILE}",
        "https://x.com/home"
    ], capture_output=True)
    time.sleep(10)
    osa('tell application "Google Chrome" to activate')
    time.sleep(2)

    for part_num in sorted(TWEETS.keys()):
        tweet = TWEETS[part_num]
        char_count = len(tweet)

        if char_count > 277:
            log(f"Part {part_num}: {char_count} chars > 277! SKIPPING.")
            continue

        log(f"--- Part {part_num} ({char_count} chars) ---")

        try:
            post_one(tweet, part_num)
            log(f"Part {part_num} POSTED")
        except Exception as e:
            log(f"Part {part_num} FAILED: {e}")

        # Wait between posts
        if part_num < max(TWEETS.keys()):
            log("Waiting 25s...")
            time.sleep(25)

    log("=== BATCH COMPLETE Part 52-60 ===")


if __name__ == "__main__":
    main()
