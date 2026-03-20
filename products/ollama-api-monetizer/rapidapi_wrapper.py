#!/usr/bin/env python3
"""
RapidAPI-compatible wrapper for Ollama.

This server mimics the format RapidAPI expects, so you can list your
Ollama-powered AI API on RapidAPI marketplace.

Setup:
  1. Create account: https://rapidapi.com/
  2. Go to: https://rapidapi.com/provider/dashboard
  3. Add new API -> External API
  4. Point base URL to your server (needs public URL / ngrok)
  5. Define endpoints matching this server

Endpoints (RapidAPI compatible):
  POST /v1/generate     -- Text generation
  POST /v1/chat         -- Chat completion
  GET  /v1/models       -- List models
  GET  /v1/health       -- Health check

Usage:
  python3 rapidapi_wrapper.py [--port 8082]
"""

import json
import http.server
import urllib.request
import os
import sys
import time

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
PORT = int(os.environ.get("RAPIDAPI_PORT", "8082"))
RAPIDAPI_SECRET = os.environ.get("RAPIDAPI_SECRET", "")


def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())


def proxy_ollama(path, data=None):
    url = f"{OLLAMA_URL}{path}"
    if data:
        req = urllib.request.Request(url, data=json.dumps(data).encode(),
                                     headers={"Content-Type": "application/json"})
    else:
        req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read()), resp.status
    except Exception as e:
        return {"error": str(e)}, 500


class RapidAPIHandler(http.server.BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def verify_rapidapi(self):
        """Verify request comes from RapidAPI (optional)."""
        if not RAPIDAPI_SECRET:
            return True
        proxy_secret = self.headers.get("X-RapidAPI-Proxy-Secret", "")
        return proxy_secret == RAPIDAPI_SECRET

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_GET(self):
        if self.path == "/v1/health":
            self.send_json({"status": "ok", "timestamp": int(time.time())})

        elif self.path == "/v1/models":
            result, status = proxy_ollama("/api/tags")
            if "models" in result:
                models = [{"id": m["name"], "object": "model", "owned_by": "local"} for m in result["models"]]
                self.send_json({"object": "list", "data": models})
            else:
                self.send_json(result, status)
        else:
            self.send_json({"error": "Not found. Endpoints: /v1/generate, /v1/chat, /v1/models, /v1/health"}, 404)

    def do_POST(self):
        if not self.verify_rapidapi():
            self.send_json({"error": "Unauthorized"}, 401)
            return

        body = self.read_body()

        if self.path == "/v1/generate":
            if "prompt" not in body:
                self.send_json({"error": "Missing 'prompt'"}, 400)
                return
            body.setdefault("model", "llama3")
            body["stream"] = False
            result, status = proxy_ollama("/api/generate", body)
            # Format response to be RapidAPI-friendly
            self.send_json({
                "text": result.get("response", ""),
                "model": body["model"],
                "usage": {
                    "prompt_tokens": result.get("prompt_eval_count", 0),
                    "completion_tokens": result.get("eval_count", 0),
                }
            })

        elif self.path == "/v1/chat":
            if "messages" not in body:
                self.send_json({"error": "Missing 'messages'"}, 400)
                return
            body.setdefault("model", "llama3")
            body["stream"] = False
            result, status = proxy_ollama("/api/chat", body)
            msg = result.get("message", {})
            self.send_json({
                "choices": [{
                    "message": {"role": msg.get("role", "assistant"), "content": msg.get("content", "")},
                    "finish_reason": "stop",
                }],
                "model": body["model"],
                "usage": {
                    "prompt_tokens": result.get("prompt_eval_count", 0),
                    "completion_tokens": result.get("eval_count", 0),
                }
            })
        else:
            self.send_json({"error": "Not found"}, 404)

    def log_message(self, format, *args):
        print(f"[{time.strftime('%H:%M:%S')}] {format % args}")


def main():
    load_env()
    global RAPIDAPI_SECRET
    RAPIDAPI_SECRET = os.environ.get("RAPIDAPI_SECRET", "")

    print("=" * 50)
    print("RAPIDAPI-COMPATIBLE OLLAMA WRAPPER")
    print("=" * 50)
    print(f"Port:    {PORT}")
    print(f"Ollama:  {OLLAMA_URL}")
    print(f"Auth:    {'RapidAPI proxy secret' if RAPIDAPI_SECRET else 'open (no secret)'}")
    print(f"\nEndpoints:")
    print(f"  POST /v1/generate  -- Text generation")
    print(f"  POST /v1/chat      -- Chat completion (OpenAI-compatible)")
    print(f"  GET  /v1/models    -- List models")
    print(f"  GET  /v1/health    -- Health check")
    print("=" * 50)

    server = http.server.HTTPServer(("0.0.0.0", PORT), RapidAPIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
