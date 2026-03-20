#!/usr/bin/env python3
"""
Self-hosted Lightning Address Server (like Ligess but simpler).

Implements LNURL-pay (LUD-06/LUD-16) so you can receive payments at:
  user@yourdomain.com

Requires:
- A domain pointed to this server
- LNbits instance (for invoice creation)

Endpoints:
  GET /.well-known/lnurlp/<username>  — LNURL-pay metadata
  GET /lnurlp/<username>/callback     — Create invoice

Usage:
  LNBITS_URL=http://localhost:5000 LNBITS_API_KEY=xxx DOMAIN=yourdomain.com python3 lightning_address_server.py
"""

import json
import http.server
import urllib.request
import os
import sys
import time

DOMAIN = os.environ.get("DOMAIN", "localhost")
LNBITS_URL = os.environ.get("LNBITS_URL", "http://localhost:5000")
LNBITS_API_KEY = os.environ.get("LNBITS_API_KEY", "")
PORT = int(os.environ.get("LN_ADDR_PORT", "8090"))
USERNAME = os.environ.get("LN_USERNAME", "avika")

# Min/max sendable in millisats
MIN_SENDABLE = 1000      # 1 sat
MAX_SENDABLE = 1000000000  # 1M sats


def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())


def create_lnbits_invoice(amount_msats, memo):
    """Create invoice via LNbits."""
    amount_sats = amount_msats // 1000
    data = json.dumps({"out": False, "amount": amount_sats, "memo": memo}).encode()
    req = urllib.request.Request(
        f"{LNBITS_URL}/api/v1/payments",
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-Api-Key": LNBITS_API_KEY
        }
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


class LNAddressHandler(http.server.BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        # LNURL-pay metadata endpoint
        # GET /.well-known/lnurlp/<username>
        if self.path.startswith("/.well-known/lnurlp/"):
            username = self.path.split("/")[-1]
            if username != USERNAME:
                self.send_json({"status": "ERROR", "reason": "User not found"}, 404)
                return

            callback_url = f"https://{DOMAIN}/lnurlp/{username}/callback"
            if DOMAIN == "localhost":
                callback_url = f"http://localhost:{PORT}/lnurlp/{username}/callback"

            self.send_json({
                "callback": callback_url,
                "maxSendable": MAX_SENDABLE,
                "minSendable": MIN_SENDABLE,
                "metadata": json.dumps([
                    ["text/plain", f"Payment to {username}@{DOMAIN}"],
                    ["text/identifier", f"{username}@{DOMAIN}"]
                ]),
                "tag": "payRequest",
                "allowsNostr": True,
                "nostrPubkey": os.environ.get("NOSTR_PUBKEY", ""),
            })

        # Callback — create invoice
        # GET /lnurlp/<username>/callback?amount=<msats>
        elif "/lnurlp/" in self.path and "/callback" in self.path:
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)

            amount_msats = int(params.get("amount", [0])[0])
            if amount_msats < MIN_SENDABLE or amount_msats > MAX_SENDABLE:
                self.send_json({
                    "status": "ERROR",
                    "reason": f"Amount must be between {MIN_SENDABLE} and {MAX_SENDABLE} msats"
                })
                return

            username = parsed.path.split("/")[2]
            memo = f"Payment to {username}@{DOMAIN}"

            try:
                invoice = create_lnbits_invoice(amount_msats, memo)
                self.send_json({
                    "pr": invoice.get("payment_request", ""),
                    "routes": [],
                })
            except Exception as e:
                self.send_json({"status": "ERROR", "reason": str(e)})

        elif self.path == "/":
            self.send_json({
                "service": "Lightning Address Server",
                "address": f"{USERNAME}@{DOMAIN}",
                "status": "running",
            })

        else:
            self.send_json({"error": "Not found"}, 404)

    def log_message(self, format, *args):
        print(f"[{time.strftime('%H:%M:%S')}] {format % args}")


def main():
    load_env()

    global DOMAIN, LNBITS_URL, LNBITS_API_KEY, USERNAME
    DOMAIN = os.environ.get("DOMAIN", "localhost")
    LNBITS_URL = os.environ.get("LNBITS_URL", "http://localhost:5000")
    LNBITS_API_KEY = os.environ.get("LNBITS_API_KEY", "")
    USERNAME = os.environ.get("LN_USERNAME", "avika")

    print("=" * 50)
    print("LIGHTNING ADDRESS SERVER")
    print("=" * 50)
    print(f"Address:  {USERNAME}@{DOMAIN}")
    print(f"Port:     {PORT}")
    print(f"LNbits:   {LNBITS_URL}")
    print(f"Nostr:    {os.environ.get('NOSTR_PUBKEY', 'not set')[:20]}...")
    if not LNBITS_API_KEY:
        print("WARNING:  LNBITS_API_KEY not set — invoices will fail")
    print("=" * 50)

    server = http.server.HTTPServer(("0.0.0.0", PORT), LNAddressHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
