#!/usr/bin/env python3
"""
Nostr AI DVM (Data Vending Machine) — Kind 5050 Text Generation
Listens for DVM requests on Nostr, processes them with Ollama, returns results.

NIP-90 DVM Protocol:
- Client posts kind 5050 event (text generation request)
- DVM responds with kind 6050 (result) or 7000 (status/feedback)
- Input is in "i" tags, output via content

This script uses pure Python websockets (no external dependencies).
"""

import json
import hashlib
import time
import sys
import ssl
import socket
import struct
import os
import secrets
import base64
import threading
import urllib.request

# Import signing from our post script
sys.path.insert(0, os.path.dirname(__file__))
from post_to_nostr import (
    load_env, scalar_mult, schnorr_sign, tagged_hash,
    P, N, Gx, Gy, modinv
)

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3"

RELAYS = [
    "wss://nos.lol",
    "wss://relay.damus.io",
]

# DVM kinds (NIP-90)
KIND_TEXT_GEN_REQUEST = 5050
KIND_TEXT_GEN_RESULT = 6050
KIND_DVM_FEEDBACK = 7000


def create_signed_event(privkey_hex, content, kind, tags):
    """Create a signed Nostr event with tags."""
    privkey_int = int(privkey_hex, 16)
    G = (Gx, Gy)
    pub = scalar_mult(privkey_int, G)
    pubkey_hex = pub[0].to_bytes(32, 'big').hex()

    created_at = int(time.time())

    serialized = json.dumps(
        [0, pubkey_hex, created_at, kind, tags, content],
        separators=(',', ':'), ensure_ascii=False
    )
    event_id = hashlib.sha256(serialized.encode()).hexdigest()
    sig = schnorr_sign(bytes.fromhex(event_id), privkey_int)

    return {
        "id": event_id,
        "pubkey": pubkey_hex,
        "created_at": created_at,
        "kind": kind,
        "tags": tags,
        "content": content,
        "sig": sig.hex()
    }


def query_ollama(prompt, model=DEFAULT_MODEL):
    """Query Ollama local inference."""
    data = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False
    }).encode()

    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            return result.get("response", "")
    except Exception as e:
        return f"Error: {e}"


class WebSocketClient:
    """Minimal WebSocket client for Nostr relay communication."""

    def __init__(self, relay_url):
        self.relay_url = relay_url
        url = relay_url.replace("wss://", "").replace("ws://", "")
        self.host = url.split("/")[0]
        self.path = "/" + "/".join(url.split("/")[1:]) if "/" in url else "/"
        self.port = 443 if relay_url.startswith("wss://") else 80
        self.sock = None
        self.connected = False

    def connect(self):
        context = ssl.create_default_context()
        raw = socket.create_connection((self.host, self.port), timeout=15)
        self.sock = context.wrap_socket(raw, server_hostname=self.host)

        key = base64.b64encode(secrets.token_bytes(16)).decode()
        handshake = (
            f"GET {self.path} HTTP/1.1\r\n"
            f"Host: {self.host}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(handshake.encode())

        response = b""
        while b"\r\n\r\n" not in response:
            response += self.sock.recv(4096)

        if b"101" not in response:
            raise ConnectionError(f"WebSocket handshake failed")

        self.connected = True

    def send(self, message):
        payload = message.encode()
        frame = bytearray([0x81])
        mask_key = secrets.token_bytes(4)

        if len(payload) < 126:
            frame.append(0x80 | len(payload))
        elif len(payload) < 65536:
            frame.append(0x80 | 126)
            frame.extend(struct.pack(">H", len(payload)))
        else:
            frame.append(0x80 | 127)
            frame.extend(struct.pack(">Q", len(payload)))

        frame.extend(mask_key)
        frame.extend(bytearray(b ^ mask_key[i % 4] for i, b in enumerate(payload)))
        self.sock.sendall(frame)

    def recv(self):
        """Receive a WebSocket frame and return text payload."""
        header = self._recv_exact(2)
        if not header:
            return None

        opcode = header[0] & 0x0f
        masked = (header[1] & 0x80) != 0
        length = header[1] & 0x7f

        if length == 126:
            length = struct.unpack(">H", self._recv_exact(2))[0]
        elif length == 127:
            length = struct.unpack(">Q", self._recv_exact(8))[0]

        if masked:
            mask = self._recv_exact(4)
            data = bytearray(self._recv_exact(length))
            data = bytearray(b ^ mask[i % 4] for i, b in enumerate(data))
        else:
            data = self._recv_exact(length)

        if opcode == 0x08:  # close
            self.connected = False
            return None
        if opcode == 0x09:  # ping
            self.send_pong(data)
            return self.recv()

        return data.decode(errors='replace')

    def send_pong(self, data):
        frame = bytearray([0x8A])
        mask_key = secrets.token_bytes(4)
        frame.append(0x80 | len(data))
        frame.extend(mask_key)
        frame.extend(bytearray(b ^ mask_key[i % 4] for i, b in enumerate(data)))
        self.sock.sendall(frame)

    def _recv_exact(self, n):
        data = b""
        while len(data) < n:
            chunk = self.sock.recv(n - len(data))
            if not chunk:
                return None
            data += chunk
        return data

    def close(self):
        if self.sock:
            try:
                mask_key = secrets.token_bytes(4)
                self.sock.sendall(bytearray([0x88, 0x80]) + mask_key)
                self.sock.close()
            except Exception:
                pass
        self.connected = False


def run_dvm(privkey_hex, pubkey_hex):
    """Main DVM loop: subscribe to requests, process with Ollama, respond."""
    print(f"DVM starting...")
    print(f"Pubkey: {pubkey_hex}")
    print(f"Model: {DEFAULT_MODEL}")
    print(f"Relays: {', '.join(RELAYS)}")
    print(f"Listening for kind {KIND_TEXT_GEN_REQUEST} events...\n")

    processed = set()

    while True:
        for relay_url in RELAYS:
            try:
                ws = WebSocketClient(relay_url)
                ws.connect()
                print(f"[{relay_url}] Connected")

                # Subscribe to all DVM text generation requests (single sub)
                sub_id = secrets.token_hex(8)
                sub = json.dumps(["REQ", sub_id, {
                    "kinds": [KIND_TEXT_GEN_REQUEST],
                    "since": int(time.time()) - 60,
                }])
                ws.send(sub)

                # Listen loop
                ws.sock.settimeout(30)
                while ws.connected:
                    try:
                        msg = ws.recv()
                        if msg is None:
                            break

                        data = json.loads(msg)
                        if data[0] == "EVENT" and len(data) >= 3:
                            event = data[2]
                            event_id = event.get("id", "")

                            if event_id in processed:
                                continue
                            processed.add(event_id)

                            # Extract prompt from "i" tags or content
                            prompt = ""
                            for tag in event.get("tags", []):
                                if tag[0] == "i" and len(tag) >= 2:
                                    prompt = tag[1]
                                    break
                            if not prompt:
                                prompt = event.get("content", "")

                            if not prompt:
                                continue

                            requester = event.get("pubkey", "")
                            print(f"\n[REQUEST] From: {requester[:16]}...")
                            print(f"  Prompt: {prompt[:100]}...")

                            # Send "processing" feedback (kind 7000)
                            feedback_tags = [
                                ["e", event_id],
                                ["p", requester],
                                ["status", "processing"],
                            ]
                            feedback = create_signed_event(
                                privkey_hex, "", KIND_DVM_FEEDBACK, feedback_tags
                            )
                            ws.send(json.dumps(["EVENT", feedback]))

                            # Process with Ollama
                            print(f"  Querying Ollama ({DEFAULT_MODEL})...")
                            result = query_ollama(prompt)
                            print(f"  Response: {result[:100]}...")

                            # Send result (kind 6050)
                            result_tags = [
                                ["e", event_id],
                                ["p", requester],
                                ["request", json.dumps(event)],
                            ]
                            result_event = create_signed_event(
                                privkey_hex, result, KIND_TEXT_GEN_RESULT, result_tags
                            )
                            ws.send(json.dumps(["EVENT", result_event]))
                            print(f"  Result sent!")

                        elif data[0] == "EOSE":
                            pass  # End of stored events

                    except socket.timeout:
                        # Send ping to keep alive
                        continue
                    except json.JSONDecodeError:
                        continue

                ws.close()

            except KeyboardInterrupt:
                print("\nDVM shutting down...")
                return
            except Exception as e:
                print(f"[{relay_url}] Error: {e}")
                time.sleep(5)


def main():
    # PID lock to prevent duplicate instances
    pidfile = "/tmp/nostr_dvm.pid"
    if os.path.exists(pidfile):
        try:
            old_pid = int(open(pidfile).read().strip())
            os.kill(old_pid, 0)  # Check if still running
            print(f"DVM already running (PID {old_pid}). Exiting.")
            sys.exit(0)
        except (OSError, ValueError):
            pass  # Old process dead, continue

    with open(pidfile, "w") as f:
        f.write(str(os.getpid()))

    import atexit
    atexit.register(lambda: os.path.exists(pidfile) and os.unlink(pidfile))

    env = load_env()
    privkey = env.get("NOSTR_PRIVKEY")
    pubkey = env.get("NOSTR_PUBKEY")

    if not privkey or not pubkey:
        print("Error: NOSTR_PRIVKEY/NOSTR_PUBKEY not found in .env")
        sys.exit(1)

    # Check Ollama is running
    try:
        test = query_ollama("hi", DEFAULT_MODEL)
        if test.startswith("Error"):
            print(f"Warning: Ollama may not be running: {test}")
    except Exception:
        print("Warning: Cannot connect to Ollama. Make sure it's running.")

    print("=" * 60)
    print("NOSTR AI DVM — Text Generation (Kind 5050)")
    print("=" * 60)

    run_dvm(privkey, pubkey)


if __name__ == "__main__":
    main()
