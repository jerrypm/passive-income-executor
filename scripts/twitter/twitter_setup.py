#!/usr/bin/env python3
"""
Twitter Session Setup
=====================
Buka browser Playwright, login Twitter manual (atau pakai existing session),
lalu simpan state untuk auto-posting.

Usage:
    python3 scripts/twitter/twitter_setup.py

Setelah browser terbuka:
1. Pastikan sudah login Twitter/X
2. Kalau belum login, login dulu
3. Tekan Enter di terminal untuk simpan session
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Paths
PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
STATE_FILE = PROJECT_DIR / "scripts" / "twitter" / "browser_state.json"
PLAYWRIGHT_PROFILE = PROJECT_DIR / "scripts" / "twitter" / "chrome_profile"
CHROME_USER_DATA = Path.home() / "Library" / "Application Support" / "Google" / "Chrome"


def find_chrome_profile(email_hint="21zerixpm"):
    """Find Chrome profile by email hint"""
    for profile_dir in sorted(CHROME_USER_DATA.iterdir()):
        prefs_file = profile_dir / "Preferences"
        if prefs_file.exists():
            try:
                import json
                prefs = json.loads(prefs_file.read_text())
                accounts = prefs.get("account_info", [])
                for acc in accounts:
                    if email_hint.lower() in acc.get("email", "").lower():
                        return profile_dir.name
            except:
                continue
    return "Profile 10"  # default fallback


def copy_chrome_cookies(chrome_profile_name):
    """Copy Chrome cookies to Playwright profile for initial session"""
    src = CHROME_USER_DATA / chrome_profile_name
    dst = PLAYWRIGHT_PROFILE

    if dst.exists():
        print(f"[*] Playwright profile sudah ada di {dst}")
        print(f"    Hapus dulu kalau mau refresh: rm -rf '{dst}'")
        return True

    if not src.exists():
        print(f"[!] Chrome profile '{chrome_profile_name}' tidak ditemukan")
        return False

    # Check if Chrome is running
    result = subprocess.run(["pgrep", "-x", "Google Chrome"], capture_output=True)
    if result.returncode == 0:
        print("\n[!] Chrome sedang berjalan!")
        print("    Tutup Chrome dulu sebelum copy profile.")
        print("    Atau jalankan tanpa --import untuk login manual.\n")
        resp = input("Mau tutup Chrome sekarang? (y/n): ").strip().lower()
        if resp == 'y':
            subprocess.run(["osascript", "-e", 'quit app "Google Chrome"'])
            import time
            time.sleep(3)
        else:
            print("[*] Skipping profile copy, akan login manual...")
            return False

    print(f"[*] Copying Chrome profile '{chrome_profile_name}'...")
    print(f"    From: {src}")
    print(f"    To:   {dst}")

    # Copy only essential files (cookies, storage)
    dst.mkdir(parents=True, exist_ok=True)
    essential_files = [
        "Cookies", "Cookies-journal",
        "Login Data", "Login Data-journal",
        "Web Data", "Web Data-journal",
        "Preferences", "Secure Preferences",
    ]
    essential_dirs = [
        "Local Storage",
        "Session Storage",
        "IndexedDB",
    ]

    for f in essential_files:
        src_file = src / f
        if src_file.exists():
            shutil.copy2(str(src_file), str(dst / f))

    for d in essential_dirs:
        src_dir = src / d
        if src_dir.exists():
            dst_dir = dst / d
            if dst_dir.exists():
                shutil.rmtree(str(dst_dir))
            shutil.copytree(str(src_dir), str(dst_dir))

    print("[+] Chrome profile copied!")
    return True


def setup_session(import_profile=True):
    """Open browser, verify Twitter login, save state"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[!] Playwright belum terinstall: pip3 install playwright")
        sys.exit(1)

    chrome_profile = find_chrome_profile()
    print(f"[*] Chrome profile ditemukan: {chrome_profile}")

    if import_profile:
        copy_chrome_cookies(chrome_profile)

    with sync_playwright() as p:
        print("\n[*] Membuka browser...")

        # Launch with persistent context
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PLAYWRIGHT_PROFILE),
            headless=False,
            viewport={"width": 1280, "height": 800},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ],
            ignore_default_args=["--enable-automation"],
        )

        page = context.pages[0] if context.pages else context.new_page()

        print("[*] Navigating ke Twitter/X...")
        page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30000)

        import time
        time.sleep(3)

        # Check if logged in
        current_url = page.url
        if "login" in current_url or "flow" in current_url:
            print("\n[!] Belum login Twitter!")
            print("    Silakan login di browser yang terbuka.")
            print("    Setelah login, tekan Enter di terminal ini.\n")
        else:
            print("\n[+] Sepertinya sudah login Twitter!")
            print("    Verifikasi di browser, lalu tekan Enter.\n")

        input(">>> Tekan Enter setelah login Twitter... ")

        # Save storage state
        context.storage_state(path=str(STATE_FILE))
        print(f"\n[+] Session tersimpan di: {STATE_FILE}")
        print("[+] Setup selesai! Sekarang bisa jalankan twitter_auto_post.py")

        context.close()


if __name__ == "__main__":
    import_flag = "--no-import" not in sys.argv
    setup_session(import_profile=import_flag)
