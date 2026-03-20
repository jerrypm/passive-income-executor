#!/usr/bin/env python3
"""
Ollama API Paywall Server
A simple HTTP API server that wraps Ollama with optional Lightning payment.

Endpoints:
  GET  /           -- API info
  GET  /models     -- List available models
  POST /generate   -- Generate text (requires payment if paywall enabled)
  POST /chat       -- Chat completion (requires payment if paywall enabled)

Payment:
  When LNbits is configured, requests require a Lightning invoice payment.
  Without LNbits, runs in free/demo mode with rate limiting.

Usage:
  python3 ollama_api_server.py [--port 8080] [--free]
"""

import json
import http.server
import urllib.request
import urllib.parse
import os
import sys
import time
import hashlib
from collections import defaultdict

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
LNBITS_URL = os.environ.get("LNBITS_URL", "")
LNBITS_API_KEY = os.environ.get("LNBITS_API_KEY", "")
PORT = int(os.environ.get("API_PORT", "8080"))
FREE_MODE = "--free" in sys.argv

# Rate limiting for free mode
RATE_LIMIT = 10  # requests per hour per IP
rate_tracker = defaultdict(list)

# Stats
stats = {"total_requests": 0, "total_paid": 0, "started_at": int(time.time())}


def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())


def check_rate_limit(ip):
    """Check if IP is within rate limit."""
    now = time.time()
    hour_ago = now - 3600
    rate_tracker[ip] = [t for t in rate_tracker[ip] if t > hour_ago]
    if len(rate_tracker[ip]) >= RATE_LIMIT:
        return False
    rate_tracker[ip].append(now)
    return True


def proxy_ollama(path, data=None, method="GET"):
    """Proxy request to Ollama."""
    url = f"{OLLAMA_URL}{path}"
    if data:
        req = urllib.request.Request(
            url, data=json.dumps(data).encode(),
            headers={"Content-Type": "application/json"}
        )
    else:
        req = urllib.request.Request(url)

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read()), resp.status
    except urllib.error.HTTPError as e:
        return {"error": str(e)}, e.code
    except Exception as e:
        return {"error": str(e)}, 500


def create_invoice(amount_sats, memo="Ollama API request"):
    """Create Lightning invoice via LNbits."""
    if not LNBITS_URL or not LNBITS_API_KEY:
        return None, "LNbits not configured"

    data = json.dumps({"out": False, "amount": amount_sats, "memo": memo}).encode()
    req = urllib.request.Request(
        f"{LNBITS_URL}/api/v1/payments",
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-Api-Key": LNBITS_API_KEY
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            return result, None
    except Exception as e:
        return None, str(e)


def check_invoice(payment_hash):
    """Check if invoice is paid via LNbits."""
    if not LNBITS_URL or not LNBITS_API_KEY:
        return False

    req = urllib.request.Request(
        f"{LNBITS_URL}/api/v1/payments/{payment_hash}",
        headers={"X-Api-Key": LNBITS_API_KEY}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            return result.get("paid", False)
    except Exception:
        return False


class APIHandler(http.server.BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length:
            return json.loads(self.rfile.read(length))
        return {}

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        if self.path == "/" or self.path == "/info":
            self.send_json({
                "name": "Ollama AI API",
                "version": "1.0",
                "mode": "free (rate-limited)" if FREE_MODE or not LNBITS_URL else "paid (Lightning)",
                "rate_limit": f"{RATE_LIMIT}/hour per IP",
                "endpoints": {
                    "GET /models": "List available models",
                    "POST /generate": "Generate text",
                    "POST /chat": "Chat completion",
                },
                "tip_jar": {
                    "lightning_address": "",  # Set your Lightning address here
                    "message": "If you find this API useful, tips are appreciated!"
                },
                "stats": {
                    "uptime_seconds": int(time.time()) - stats["started_at"],
                    "total_requests": stats["total_requests"],
                }
            })

        elif self.path == "/models":
            result, status = proxy_ollama("/api/tags")
            if status == 200 and "models" in result:
                models = [{"name": m["name"], "size": m.get("size", 0)} for m in result["models"]]
                self.send_json({"models": models})
            else:
                self.send_json(result, status)

        else:
            self.send_json({"error": "Not found"}, 404)

    def do_POST(self):
        stats["total_requests"] += 1
        client_ip = self.client_address[0]

        if self.path not in ["/generate", "/chat"]:
            self.send_json({"error": "Not found"}, 404)
            return

        # Payment / rate limit check
        if not FREE_MODE and LNBITS_URL and LNBITS_API_KEY:
            # Check for payment
            payment_hash = self.headers.get("X-Payment-Hash", "")

            if not payment_hash:
                # Create invoice
                invoice, err = create_invoice(10, f"Ollama API - {self.path}")
                if err:
                    self.send_json({"error": f"Payment required but invoice creation failed: {err}"}, 402)
                    return
                self.send_json({
                    "status": "payment_required",
                    "invoice": invoice.get("payment_request", ""),
                    "payment_hash": invoice.get("payment_hash", ""),
                    "amount_sats": 10,
                    "memo": "Pay this Lightning invoice, then retry with X-Payment-Hash header"
                }, 402)
                return

            if not check_invoice(payment_hash):
                self.send_json({"error": "Invoice not paid yet"}, 402)
                return

            stats["total_paid"] += 1

        else:
            # Free mode: rate limit
            if not check_rate_limit(client_ip):
                self.send_json({
                    "error": "Rate limit exceeded",
                    "limit": f"{RATE_LIMIT} requests per hour",
                    "tip": "Configure LNbits for unlimited paid access"
                }, 429)
                return

        # Process request
        body = self.read_body()

        if self.path == "/generate":
            if "prompt" not in body:
                self.send_json({"error": "Missing 'prompt' field"}, 400)
                return
            body.setdefault("model", "llama3")
            body["stream"] = False
            result, status = proxy_ollama("/api/generate", body)
            self.send_json(result, status)

        elif self.path == "/chat":
            if "messages" not in body:
                self.send_json({"error": "Missing 'messages' field"}, 400)
                return
            body.setdefault("model", "llama3")
            body["stream"] = False
            result, status = proxy_ollama("/api/chat", body)
            self.send_json(result, status)

    def log_message(self, format, *args):
        print(f"[{time.strftime('%H:%M:%S')}] {self.client_address[0]} - {format % args}")


def main():
    load_env()

    global LNBITS_URL, LNBITS_API_KEY
    LNBITS_URL = os.environ.get("LNBITS_URL", "")
    LNBITS_API_KEY = os.environ.get("LNBITS_API_KEY", "")

    print("=" * 60)
    print("OLLAMA API PAYWALL SERVER")
    print("=" * 60)
    print(f"Port:     {PORT}")
    print(f"Ollama:   {OLLAMA_URL}")
    print(f"Mode:     {'FREE' if FREE_MODE or not LNBITS_URL else 'PAID (LNbits)'}")
    if LNBITS_URL:
        print(f"LNbits:   {LNBITS_URL}")
        print(f"Price:    10 sats/request")
    else:
        print(f"LNbits:   Not configured (running in free mode)")
        print(f"Rate:     {RATE_LIMIT} requests/hour per IP")
    print(f"\nEndpoints:")
    print(f"  http://localhost:{PORT}/          -- API info")
    print(f"  http://localhost:{PORT}/models    -- List models")
    print(f"  http://localhost:{PORT}/generate  -- Generate text")
    print(f"  http://localhost:{PORT}/chat      -- Chat completion")
    print("=" * 60)

    server = http.server.HTTPServer(("0.0.0.0", PORT), APIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
