#!/usr/bin/env python3
"""
Post Part 51 to Twitter via CGEvent (JXA).
Bypasses System Events entirely — no Accessibility permission needed for System Events.
Uses CGEventCreateKeyboardEvent + CGEventCreateMouseEvent.
"""

import subprocess
import time

CHROME_PROFILE = "Profile 10"

TWEET = (
    "\U0001f9ed Part 51/100 \u2014 Navigation Patterns in SwiftUI\n\n"
    "Stop hardcoding navigation. Build it to scale.\n\n"
    "https://21zerixpm.medium.com/navigation-patterns-in-swiftui-building-scalable-navigation-636e44f1f2aa\n\n"
    "#SwiftUI #100DaysOfCode #iOSDev"
)


def osa(script, timeout=30):
    r = subprocess.run(["osascript", "-e", script],
                       capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0 and r.stderr.strip():
        print(f"    osa err: {r.stderr.strip()[:120]}")
    return r.stdout.strip(), r.returncode


def jxa(code, timeout=15):
    """Run JavaScript for Automation (JXA) via osascript."""
    r = subprocess.run(["osascript", "-l", "JavaScript", "-e", code],
                       capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0 and r.stderr.strip():
        print(f"    jxa err: {r.stderr.strip()[:120]}")
    return r.returncode


def cg_click(x, y):
    """Mouse click at (x,y) via CGEvent."""
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
    print(f"    click({x},{y})")


def cg_key(keycode, cmd=False):
    """Press a key via CGEvent keyboard event."""
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
    name = f"key({keycode})" + (" +Cmd" if cmd else "")
    print(f"    {name}")


# Key codes
KEY_V = 9
KEY_N = 45
KEY_RETURN = 36
KEY_ENTER = 76  # numpad
KEY_TAB = 48
KEY_SPACE = 49
KEY_ESC = 53


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


def main():
    print(f"Tweet ({len(TWEET)} chars):")
    print(TWEET)
    print()

    # === STEP 1: Open Chrome ===
    print("[1/7] Opening Chrome Profile 10 -> x.com/home")
    subprocess.run([
        "open", "-na", "Google Chrome",
        "--args", f"--profile-directory={CHROME_PROFILE}",
        "https://x.com/home"
    ], capture_output=True)
    time.sleep(10)

    # === STEP 2: Activate Chrome ===
    print("[2/7] Activating Chrome")
    osa('tell application "Google Chrome" to activate')
    time.sleep(2)

    # === STEP 3: Click page center ===
    print("[3/7] Clicking page center (CGEvent mouse)")
    bounds = get_bounds()
    print(f"    Window bounds: {bounds}")
    if bounds:
        cx = bounds[0] + (bounds[2] - bounds[0]) // 2
        cy = bounds[1] + 400
        cg_click(cx, cy)
    time.sleep(1)

    # === STEP 4: Press "n" to open compose (via CGEvent keyboard) ===
    print("[4/7] Pressing 'n' to open compose (CGEvent)")
    cg_key(KEY_N)
    time.sleep(4)
    print("    Compose should be open now")

    # === STEP 5: Paste tweet (pbcopy + Cmd+V via CGEvent) ===
    print("[5/7] Pasting tweet (pbcopy + CGEvent Cmd+V)")
    subprocess.run(["pbcopy"], input=TWEET.encode(), capture_output=True)
    time.sleep(0.5)
    cg_key(KEY_V, cmd=True)
    time.sleep(3)
    print("    Text should be pasted now")

    # === STEP 6: Post — try all methods ===
    print()
    print("[6/7] === POSTING ATTEMPTS ===")
    print()

    # Method A: Cmd+Return via CGEvent
    print("  [A] Cmd+Return (CGEvent key code 36)")
    cg_key(KEY_RETURN, cmd=True)
    time.sleep(5)
    print("      Check if posted.")
    print()

    # Method B: Cmd+Enter numpad via CGEvent
    print("  [B] Cmd+Enter numpad (CGEvent key code 76)")
    cg_key(KEY_ENTER, cmd=True)
    time.sleep(5)
    print("      Check if posted.")
    print()

    # Method C: Click Post button location
    print("  [C] Click Post button (CGEvent mouse)")
    bounds = get_bounds()
    if bounds:
        win_w = bounds[2] - bounds[0]
        win_h = bounds[3] - bounds[1]
        positions = [
            ("right of modal bottom", bounds[0] + win_w // 2 + 230, bounds[1] + win_h // 2 + 110),
            ("right of modal bottom v2", bounds[0] + win_w // 2 + 250, bounds[1] + win_h // 2 + 90),
            ("right of modal bottom v3", bounds[0] + win_w // 2 + 200, bounds[1] + win_h // 2 + 130),
        ]
        for desc, bx, by in positions:
            print(f"      {desc} ({bx},{by})")
            cg_click(bx, by)
            time.sleep(2)
    print()

    # Method D: Tab to Post button + Space
    print("  [D] Tab x10 then Space+Enter (CGEvent)")
    for i in range(10):
        cg_key(KEY_TAB)
        time.sleep(0.3)
    cg_key(KEY_SPACE)
    time.sleep(1)
    cg_key(KEY_RETURN)
    time.sleep(3)
    print("      Done.")
    print()

    print("[7/7] All methods tried!")
    print("      CHECK TWITTER — did Part 51 get posted?")
    print("      Tell me which method (A/B/C/D) worked, or what you see on screen.")


if __name__ == "__main__":
    main()
