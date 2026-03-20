#!/usr/bin/env python3
"""
Lightning Bitcoin Faucet Auto-Claimer
=====================================
Attempts to claim free sats from various Lightning/Bitcoin faucets.

REALITY CHECK:
- Most faucets have CAPTCHAs and anti-bot measures → NOT scriptable
- The ones that ARE scriptable pay very little (1-50 sats)
- Expected monthly earnings from faucets alone: $0.50-$5
- This script is a "nice to have", not a serious income stream
- Your Nostr content + zaps will earn 10-100x more than faucets

Usage:
    python3 claim_faucets.py              # Run all faucet claims
    python3 claim_faucets.py --dry-run    # Test without claiming
    python3 claim_faucets.py --list       # List all known faucets

Designed to run daily via cron:
    0 7 * * * /usr/bin/python3 /path/to/claim_faucets.py >> /path/to/logs/faucets.log 2>&1

Dependencies: Python standard library only (urllib, json, ssl, etc.)
Lightning address: freshbeach08@walletofsatoshi.com
"""

import json
import os
import sys
import ssl
import time
import hashlib
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

LIGHTNING_ADDRESS = "freshbeach08@walletofsatoshi.com"

# Resolve paths relative to this script
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_DIR = SCRIPT_DIR.parent.parent
LOG_FILE = PROJECT_DIR / "logs" / "faucets.log"
ENV_FILE = PROJECT_DIR / ".env"

# HTTP request timeout in seconds
REQUEST_TIMEOUT = 15

# User-Agent to look like a normal browser
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

# SSL context that doesn't verify (some faucets have bad certs)
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

# Also keep a proper SSL context for well-known services
SSL_CTX_VERIFY = ssl.create_default_context()


# ============================================================================
# LOGGING
# ============================================================================

def log(message: str, level: str = "INFO"):
    """Log message to both stdout and log file."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{timestamp}] [{level}] {message}"
    print(line)
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception as e:
        print(f"  (Could not write to log: {e})")


def log_separator():
    """Print a separator line."""
    sep = "=" * 70
    log(sep)


# ============================================================================
# HTTP HELPERS
# ============================================================================

def http_get(url: str, headers: dict = None, timeout: int = REQUEST_TIMEOUT,
             verify_ssl: bool = True) -> dict:
    """
    Make an HTTP GET request and return parsed JSON or raw text.
    Returns: {"ok": True, "data": ..., "status": 200}
          or {"ok": False, "error": "...", "status": ...}
    """
    req_headers = {"User-Agent": USER_AGENT}
    if headers:
        req_headers.update(headers)

    req = urllib.request.Request(url, headers=req_headers, method="GET")
    ctx = SSL_CTX_VERIFY if verify_ssl else SSL_CTX

    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            status = resp.status
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                data = raw
            return {"ok": True, "data": data, "status": status}
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            pass
        return {"ok": False, "error": f"HTTP {e.code}: {e.reason} — {body}", "status": e.code}
    except urllib.error.URLError as e:
        return {"ok": False, "error": f"URL Error: {e.reason}", "status": 0}
    except Exception as e:
        return {"ok": False, "error": f"Request failed: {e}", "status": 0}


def http_post(url: str, data: dict = None, json_body: dict = None,
              headers: dict = None, timeout: int = REQUEST_TIMEOUT,
              verify_ssl: bool = True) -> dict:
    """Make an HTTP POST request."""
    req_headers = {"User-Agent": USER_AGENT}
    if headers:
        req_headers.update(headers)

    if json_body is not None:
        body = json.dumps(json_body).encode("utf-8")
        req_headers["Content-Type"] = "application/json"
    elif data is not None:
        body = urllib.parse.urlencode(data).encode("utf-8")
        req_headers["Content-Type"] = "application/x-www-form-urlencoded"
    else:
        body = None

    req = urllib.request.Request(url, data=body, headers=req_headers, method="POST")
    ctx = SSL_CTX_VERIFY if verify_ssl else SSL_CTX

    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            status = resp.status
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                parsed = raw
            return {"ok": True, "data": parsed, "status": status}
    except urllib.error.HTTPError as e:
        body_text = ""
        try:
            body_text = e.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            pass
        return {"ok": False, "error": f"HTTP {e.code}: {e.reason} — {body_text}", "status": e.code}
    except urllib.error.URLError as e:
        return {"ok": False, "error": f"URL Error: {e.reason}", "status": 0}
    except Exception as e:
        return {"ok": False, "error": f"Request failed: {e}", "status": 0}


# ============================================================================
# LIGHTNING ADDRESS RESOLUTION
# ============================================================================

def resolve_lightning_address(address: str) -> dict:
    """
    Resolve a Lightning Address (user@domain) to its LNURL-pay endpoint.
    Returns the LNURL-pay metadata JSON.

    Lightning Address spec: https://github.com/andrerfneves/lightning-address
    user@domain → GET https://domain/.well-known/lnurlp/user
    """
    if "@" not in address:
        return {"ok": False, "error": "Invalid Lightning address format"}

    user, domain = address.split("@", 1)
    url = f"https://{domain}/.well-known/lnurlp/{user}"

    log(f"Resolving Lightning address: {address}")
    log(f"  → GET {url}")

    result = http_get(url)
    if result["ok"]:
        data = result["data"]
        if isinstance(data, dict) and data.get("tag") == "payRequest":
            min_sat = data.get("minSendable", 0) // 1000
            max_sat = data.get("maxSendable", 0) // 1000
            log(f"  Lightning address valid! Accepts {min_sat}-{max_sat} sats")
            return {"ok": True, "data": data}
        else:
            return {"ok": False, "error": f"Unexpected response: {data}"}
    return result


# ============================================================================
# FAUCET CLAIM FUNCTIONS
#
# Each function attempts to claim from one faucet.
# Returns: {"claimed": True/False, "sats": N, "message": "..."}
#
# HONEST STATUS of each faucet:
# - Most will FAIL because they require CAPTCHAs or browser interaction
# - This is documented so you know what's real vs aspirational
# ============================================================================

def claim_lnpulse_faucet(dry_run: bool = False) -> dict:
    """
    LNPulse Sats Faucet — https://faucet.lnpulse.app/

    STATUS: EXPERIMENTAL
    - Requires Nostr identity
    - May have an API endpoint for Nostr-authenticated claims
    - If it uses NIP-98 HTTP auth, we could potentially script it

    This attempts to discover if there's a claimable API endpoint.
    """
    log("Attempting: LNPulse Sats Faucet")
    base_url = "https://faucet.lnpulse.app"

    if dry_run:
        return {"claimed": False, "sats": 0, "message": "DRY RUN — would attempt LNPulse"}

    # Try to find API endpoints
    # Common patterns: /api/claim, /api/faucet, /claim
    endpoints_to_try = [
        f"{base_url}/api/claim",
        f"{base_url}/api/faucet",
        f"{base_url}/api/status",
    ]

    for endpoint in endpoints_to_try:
        log(f"  Probing: {endpoint}")
        result = http_get(endpoint, verify_ssl=True)
        if result["ok"]:
            log(f"  Response: {json.dumps(result['data'])[:200]}")
            # If we find a working endpoint, try to claim
            if isinstance(result["data"], dict):
                if "claim" in str(result["data"]).lower() or "sats" in str(result["data"]).lower():
                    log(f"  Found potential claim endpoint!")
                    return {"claimed": False, "sats": 0,
                            "message": f"Found endpoint {endpoint} — needs manual investigation"}
        else:
            log(f"  {result['error'][:100]}")

    return {
        "claimed": False, "sats": 0,
        "message": "No scriptable API found. Requires browser + Nostr login."
    }


def claim_ln_stores_faucet(dry_run: bool = False) -> dict:
    """
    Lightning Network Stores Faucet — https://lightningnetworkstores.com/faucet

    STATUS: UNLIKELY TO WORK VIA SCRIPT
    - Vue.js SPA — content loaded dynamically
    - Likely requires CAPTCHA
    - Claim mechanism hidden in JS bundle

    We try common API patterns anyway.
    """
    log("Attempting: Lightning Network Stores Faucet")
    base_url = "https://lightningnetworkstores.com"

    if dry_run:
        return {"claimed": False, "sats": 0, "message": "DRY RUN — would attempt LN Stores"}

    # Try API endpoints
    endpoints = [
        f"{base_url}/api/faucet",
        f"{base_url}/api/claim",
        f"{base_url}/faucet/claim",
    ]

    for endpoint in endpoints:
        log(f"  Probing: {endpoint}")
        result = http_get(endpoint, verify_ssl=True)
        if result["ok"] and result["status"] == 200:
            log(f"  Response: {str(result['data'])[:200]}")
            if isinstance(result["data"], dict) and "error" not in str(result["data"]).lower():
                return {"claimed": False, "sats": 0,
                        "message": f"Got response from {endpoint} — needs investigation"}
        else:
            log(f"  {result.get('error', 'No response')[:100]}")

    # Try posting a Lightning invoice to the faucet
    # This is speculative — we don't know the exact endpoint
    log("  Trying POST with Lightning address...")
    result = http_post(
        f"{base_url}/api/faucet",
        json_body={"lightning_address": LIGHTNING_ADDRESS},
        verify_ssl=True
    )
    if result["ok"]:
        log(f"  POST response: {str(result['data'])[:200]}")

    return {
        "claimed": False, "sats": 0,
        "message": "Vue.js SPA — no scriptable API found. Requires browser."
    }


def claim_lnurl_withdraw_faucet(lnurl_or_url: str, name: str = "Unknown",
                                 dry_run: bool = False) -> dict:
    """
    Generic LNURL-Withdraw Faucet Claimer

    STATUS: WORKS — if you have a valid LNURL-withdraw URL

    This is the most automation-friendly type of faucet.
    Problem: very few mainnet LNURL-withdraw faucets exist publicly.

    Protocol:
    1. GET the LNURL endpoint → withdrawRequest JSON
    2. Generate invoice (we can't do this without a wallet with API)
    3. Submit invoice to callback

    LIMITATION: We need a way to generate Lightning invoices.
    Options:
    - LNbits API (we have this, but it uses FakeWallet)
    - Wallet of Satoshi (no invoice generation API)
    - Phoenix (has API but needs to be running)

    For now, this logs what WOULD happen.
    """
    log(f"Attempting LNURL-withdraw: {name}")

    if dry_run:
        return {"claimed": False, "sats": 0, "message": f"DRY RUN — would attempt {name}"}

    # If it's a raw URL (not bech32 LNURL), use directly
    url = lnurl_or_url
    if lnurl_or_url.lower().startswith("lnurl"):
        # Would need bech32 decoding — skip for now
        log("  LNURL bech32 decoding not implemented (would need bech32 library)")
        return {"claimed": False, "sats": 0, "message": "LNURL bech32 decoding needed"}

    log(f"  GET {url}")
    result = http_get(url, verify_ssl=False)

    if not result["ok"]:
        return {"claimed": False, "sats": 0, "message": f"Failed: {result['error'][:100]}"}

    data = result["data"]
    if not isinstance(data, dict):
        return {"claimed": False, "sats": 0, "message": f"Not JSON response: {str(data)[:100]}"}

    if data.get("tag") != "withdrawRequest":
        return {"claimed": False, "sats": 0,
                "message": f"Not a withdrawRequest: tag={data.get('tag')}"}

    # Parse withdraw request
    callback = data.get("callback", "")
    k1 = data.get("k1", "")
    max_sats = data.get("maxWithdrawable", 0) // 1000  # msats → sats
    min_sats = data.get("minWithdrawable", 0) // 1000
    description = data.get("defaultDescription", "")

    log(f"  Withdraw request found!")
    log(f"  Amount: {min_sats}-{max_sats} sats")
    log(f"  Description: {description}")
    log(f"  Callback: {callback}")

    # To complete the withdrawal, we need a Lightning invoice (BOLT11)
    # We'd need an LNbits or other wallet API to generate one
    # For now, log this as a successful discovery
    log(f"  NOTE: Cannot complete — need Lightning invoice generation")
    log(f"  To claim manually: create a {max_sats} sat invoice and submit to callback")

    return {
        "claimed": False, "sats": 0,
        "message": f"Found valid withdraw: {min_sats}-{max_sats} sats. "
                   f"Need invoice generation to complete claim."
    }


def claim_lightning_faucet_com(dry_run: bool = False) -> dict:
    """
    LightningFaucet.com — https://lightningfaucet.com/

    STATUS: NOT SCRIPTABLE
    - Weekly free spin only
    - Requires account + browser
    - Has L402 API but that's for paying, not claiming
    """
    log("Attempting: LightningFaucet.com")

    if dry_run:
        return {"claimed": False, "sats": 0, "message": "DRY RUN — would attempt LightningFaucet.com"}

    # Check if the site is up and look for any API
    result = http_get("https://lightningfaucet.com/", verify_ssl=True)
    if result["ok"]:
        log(f"  Site is up (status {result['status']})")
        log(f"  Weekly spin requires browser + account. Not scriptable.")
    else:
        log(f"  Site error: {result['error'][:100]}")

    return {
        "claimed": False, "sats": 0,
        "message": "Weekly spin only. Requires browser + account. Not scriptable."
    }


def check_lnbits_for_invoice_generation(dry_run: bool = False) -> dict:
    """
    Check if our local LNbits can generate real invoices.

    STATUS: LNbits is running but uses FakeWallet backend.
    With FakeWallet, invoices are not real — can't receive actual sats.
    This would work if LNbits were connected to a real Lightning node.
    """
    log("Checking LNbits invoice generation capability...")

    lnbits_url = os.environ.get("LNBITS_URL", "http://127.0.0.1:5001")
    invoice_key = os.environ.get("LNBITS_INVOICE_KEY", "")

    if not invoice_key:
        # Try loading from .env file
        if ENV_FILE.exists():
            with open(ENV_FILE) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("LNBITS_INVOICE_KEY="):
                        invoice_key = line.split("=", 1)[1]
                    elif line.startswith("LNBITS_URL="):
                        lnbits_url = line.split("=", 1)[1]

    if not invoice_key:
        return {"ok": False, "message": "No LNbits invoice key found"}

    if dry_run:
        return {"ok": True, "message": "DRY RUN — would check LNbits"}

    # Try to create a test invoice
    log(f"  LNbits URL: {lnbits_url}")
    result = http_post(
        f"{lnbits_url}/api/v1/payments",
        json_body={"out": False, "amount": 10, "memo": "faucet-test"},
        headers={"X-Api-Key": invoice_key},
        verify_ssl=False
    )

    if result["ok"] and isinstance(result["data"], dict):
        bolt11 = result["data"].get("payment_request", "")
        if bolt11:
            log(f"  LNbits can generate invoices!")
            log(f"  Invoice: {bolt11[:50]}...")
            # Check if it's a FakeWallet invoice
            if "lnbc" in bolt11.lower():
                log(f"  WARNING: This may be a FakeWallet invoice (not redeemable)")
                return {"ok": True, "invoice": bolt11,
                        "message": "Invoice generated but likely FakeWallet (not real)"}
            return {"ok": True, "invoice": bolt11, "message": "Real invoice generated!"}

    log(f"  LNbits invoice creation failed: {result.get('error', 'unknown')}")
    return {"ok": False, "message": f"LNbits error: {result.get('error', 'unknown')[:100]}"}


def probe_for_new_faucets(dry_run: bool = False) -> dict:
    """
    Probe known URLs that sometimes host community Lightning faucets.

    Community faucets come and go. This checks a list of URLs
    that have historically hosted faucets or might in the future.
    """
    log("Probing for community faucets...")

    if dry_run:
        return {"claimed": False, "sats": 0, "message": "DRY RUN — would probe for faucets"}

    # List of URLs that have been known to host Lightning faucets
    # These change frequently — update as new ones are discovered
    known_faucet_urls = [
        # Active / recently active
        ("https://faucet.lnpulse.app/", "LNPulse Nostr Faucet"),
        ("https://lightningnetworkstores.com/faucet", "LN Stores Faucet"),
        ("https://lightningfaucet.com/", "LightningFaucet.com"),
        ("https://boltcoiner.io/", "Boltcoiner"),
        ("https://www.satsfaucet.com/", "SatsFaucet"),
        # Potentially new / community
        ("https://stakwork.com/", "Stakwork (earn sats for tasks)"),
    ]

    found = []
    for url, name in known_faucet_urls:
        log(f"  Checking: {name} ({url})")
        result = http_get(url, verify_ssl=True)
        status = "UP" if result["ok"] else "DOWN"
        log(f"    Status: {status}")
        if result["ok"]:
            found.append(name)

    return {
        "claimed": False, "sats": 0,
        "message": f"Probed {len(known_faucet_urls)} faucets. "
                   f"Online: {', '.join(found) if found else 'none'}"
    }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def print_summary(results: list):
    """Print a summary of all faucet claim attempts."""
    log_separator()
    log("FAUCET CLAIM SUMMARY")
    log_separator()

    total_sats = 0
    successful = 0

    for name, result in results:
        status = "OK" if result.get("claimed") else "SKIP"
        sats = result.get("sats", 0)
        msg = result.get("message", "")
        total_sats += sats
        if result.get("claimed"):
            successful += 1
        log(f"  [{status}] {name}: {sats} sats — {msg}")

    log_separator()
    log(f"Total claimed: {total_sats} sats from {successful}/{len(results)} faucets")
    if total_sats == 0:
        log("No sats claimed. This is normal — most faucets require browser interaction.")
        log("Better earning methods: Nostr content + zaps, DVM, API paywall")
    log_separator()


def list_faucets():
    """Print a list of all known faucets."""
    print("\nKnown Lightning/Bitcoin Faucets:")
    print("=" * 60)
    faucets = [
        ("LNPulse Sats Faucet", "https://faucet.lnpulse.app/", "Nostr auth", "~50 sats/day"),
        ("LN Stores Faucet", "https://lightningnetworkstores.com/faucet", "Browser", "~20 sats/day"),
        ("LightningFaucet.com", "https://lightningfaucet.com/", "Browser", "5-100 sats/week"),
        ("SatsFaucet", "https://www.satsfaucet.com/", "Browser+tasks", "~400 sats/hour"),
        ("Boltcoiner", "https://boltcoiner.io/", "CAPTCHA+tweet", "~50 sats (offline)"),
        ("Cointiply", "https://cointiply.com/", "Browser+tasks", "Variable"),
        ("FreeBitco.in", "https://freebitco.in/", "Browser+CAPTCHA", "1-200 sats/hour"),
        ("Stacker News", "https://stacker.news/", "Post content", "50-1000 sats/post"),
        ("Nostr Zaps", "Any Nostr client", "Post content", "1-10000+ sats/zap"),
    ]

    for name, url, method, payout in faucets:
        print(f"\n  {name}")
        print(f"    URL: {url}")
        print(f"    Method: {method}")
        print(f"    Payout: {payout}")

    print("\n" + "=" * 60)
    print("Scriptable: Only LNURL-withdraw faucets (rare on mainnet)")
    print("Best ROI: Nostr zaps + Stacker News (content-based)")
    print()


def main():
    """Main entry point."""
    # Parse arguments
    dry_run = "--dry-run" in sys.argv
    list_only = "--list" in sys.argv

    if list_only:
        list_faucets()
        return

    log_separator()
    log("LIGHTNING FAUCET AUTO-CLAIMER")
    log(f"Lightning Address: {LIGHTNING_ADDRESS}")
    log(f"Dry Run: {dry_run}")
    log(f"Log File: {LOG_FILE}")
    log_separator()

    # Step 1: Verify our Lightning address is valid
    la_result = resolve_lightning_address(LIGHTNING_ADDRESS)
    if not la_result["ok"]:
        log(f"WARNING: Could not resolve Lightning address: {la_result['error']}", "WARN")
        log("Continuing anyway — some faucets accept addresses directly", "WARN")

    # Step 2: Check LNbits invoice capability
    lnbits_result = check_lnbits_for_invoice_generation(dry_run)
    can_generate_invoices = lnbits_result.get("ok", False)
    if can_generate_invoices:
        log(f"LNbits: {lnbits_result['message']}")
    else:
        log(f"LNbits: Not available for invoice generation")
        log("  (Most LNURL-withdraw faucets need invoice generation)")

    log("")

    # Step 3: Attempt claims from each faucet
    results = []

    # Faucet 1: LNPulse
    r = claim_lnpulse_faucet(dry_run)
    results.append(("LNPulse Sats Faucet", r))
    time.sleep(1)  # Be polite between requests

    # Faucet 2: LN Stores
    r = claim_ln_stores_faucet(dry_run)
    results.append(("LN Stores Faucet", r))
    time.sleep(1)

    # Faucet 3: LightningFaucet.com
    r = claim_lightning_faucet_com(dry_run)
    results.append(("LightningFaucet.com", r))
    time.sleep(1)

    # Faucet 4: Probe for new/community faucets
    r = probe_for_new_faucets(dry_run)
    results.append(("Community Faucet Probe", r))

    # Step 4: Print summary
    print_summary(results)

    # Step 5: Advice
    log("")
    log("RECOMMENDATION:")
    log("  Faucets are NOT a reliable income source.")
    log("  Focus on these instead (already set up):")
    log("    1. Nostr content + zaps (scripts/nostr/auto_content.py)")
    log("    2. DVM text generation (scripts/nostr/dvm_text_generation.py)")
    log("    3. Ollama API paywall (scripts/ai-inference/ollama_api_server.py)")
    log("    4. Nostr marketplace products (scripts/nostr/list_product_shopstr.py)")
    log("")


if __name__ == "__main__":
    main()
