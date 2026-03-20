#!/usr/bin/env python3
"""
Post a message to Nostr relays using pure Python (no external dependencies).
Uses raw sockets + SSL for WebSocket communication.

Usage:
    python3 post_to_nostr.py "Hello Nostr!"
    python3 post_to_nostr.py  # defaults to "gm" message
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

# Load keys from .env
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    env = {}
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
    return env

# secp256k1 parameters
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

def modinv(a, m=P):
    return pow(a, m - 2, m)

def point_add(p1, p2):
    if p1 is None: return p2
    if p2 is None: return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and y1 != y2: return None
    if x1 == x2:
        lam = (3 * x1 * x1) * modinv(2 * y1) % P
    else:
        lam = (y2 - y1) * modinv(x2 - x1) % P
    x3 = (lam * lam - x1 - x2) % P
    y3 = (lam * (x1 - x3) - y1) % P
    return (x3, y3)

def scalar_mult(k, point):
    result = None
    addend = point
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result

def tagged_hash(tag, data):
    """BIP-340 tagged hash: SHA256(SHA256(tag) || SHA256(tag) || data)."""
    tag_hash = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256(tag_hash + tag_hash + data).digest()

def schnorr_sign(msg_hash_bytes, privkey_int):
    """BIP-340 Schnorr signature."""
    G = (Gx, Gy)
    pub = scalar_mult(privkey_int, G)
    px_bytes = pub[0].to_bytes(32, 'big')

    # Negate privkey if pub.y is odd
    d = privkey_int
    if pub[1] % 2 != 0:
        d = N - d

    # Deterministic nonce per BIP-340
    aux = secrets.token_bytes(32)
    t = (d ^ int.from_bytes(tagged_hash("BIP0340/aux", aux), 'big')).to_bytes(32, 'big')

    nonce_hash = tagged_hash("BIP0340/nonce", t + px_bytes + msg_hash_bytes)
    k = int.from_bytes(nonce_hash, 'big') % N
    if k == 0:
        raise ValueError("Bad nonce")

    R = scalar_mult(k, G)
    if R[1] % 2 != 0:
        k = N - k

    rx = R[0].to_bytes(32, 'big')

    e_hash = tagged_hash("BIP0340/challenge", rx + px_bytes + msg_hash_bytes)
    e = int.from_bytes(e_hash, 'big') % N

    s = (k + e * d) % N

    return rx + s.to_bytes(32, 'big')

def create_event(privkey_hex, content, kind=1):
    """Create a signed Nostr event."""
    privkey_int = int(privkey_hex, 16)
    G = (Gx, Gy)
    pub = scalar_mult(privkey_int, G)
    pubkey_hex = pub[0].to_bytes(32, 'big').hex()

    created_at = int(time.time())
    tags = []

    # Serialize for hashing (NIP-01)
    serialized = json.dumps([0, pubkey_hex, created_at, kind, tags, content], separators=(',', ':'), ensure_ascii=False)
    event_id = hashlib.sha256(serialized.encode()).hexdigest()

    # Sign
    sig = schnorr_sign(bytes.fromhex(event_id), privkey_int)

    event = {
        "id": event_id,
        "pubkey": pubkey_hex,
        "created_at": created_at,
        "kind": kind,
        "tags": tags,
        "content": content,
        "sig": sig.hex()
    }
    return event

def websocket_send(host, port, path, message):
    """Send a WebSocket message to a relay (minimal implementation)."""
    context = ssl.create_default_context()
    sock = socket.create_connection((host, port), timeout=10)
    sock = context.wrap_socket(sock, server_hostname=host)

    # WebSocket handshake
    key = secrets.token_bytes(16)
    import base64
    ws_key = base64.b64encode(key).decode()

    handshake = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {ws_key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n"
        f"\r\n"
    )
    sock.sendall(handshake.encode())

    # Read response
    response = b""
    while b"\r\n\r\n" not in response:
        response += sock.recv(4096)

    if b"101" not in response:
        sock.close()
        return False, f"Handshake failed: {response[:200].decode(errors='replace')}"

    # Send WebSocket frame (text)
    payload = message.encode()
    frame = bytearray()
    frame.append(0x81)  # FIN + text opcode
    mask_key = secrets.token_bytes(4)

    if len(payload) < 126:
        frame.append(0x80 | len(payload))  # MASK bit + length
    elif len(payload) < 65536:
        frame.append(0x80 | 126)
        frame.extend(struct.pack(">H", len(payload)))
    else:
        frame.append(0x80 | 127)
        frame.extend(struct.pack(">Q", len(payload)))

    frame.extend(mask_key)
    masked = bytearray(b ^ mask_key[i % 4] for i, b in enumerate(payload))
    frame.extend(masked)

    sock.sendall(frame)

    # Read response
    try:
        sock.settimeout(5)
        resp_data = sock.recv(4096)
        # Parse WebSocket frame
        if len(resp_data) > 2:
            opcode = resp_data[0] & 0x0f
            length = resp_data[1] & 0x7f
            if length < 126:
                payload_start = 2
            elif length == 126:
                payload_start = 4
            else:
                payload_start = 10
            resp_text = resp_data[payload_start:payload_start+length].decode(errors='replace')
        else:
            resp_text = ""
    except socket.timeout:
        resp_text = "(no response)"

    # Close
    close_frame = bytearray([0x88, 0x80]) + mask_key
    try:
        sock.sendall(close_frame)
    except Exception:
        pass
    sock.close()

    return True, resp_text

def post_to_relay(relay_url, event):
    """Post event to a relay via WebSocket."""
    # Parse relay URL
    url = relay_url.replace("wss://", "").replace("ws://", "")
    host = url.split("/")[0]
    path = "/" + "/".join(url.split("/")[1:]) if "/" in url else "/"
    port = 443 if relay_url.startswith("wss://") else 80

    message = json.dumps(["EVENT", event])
    return websocket_send(host, port, path, message)

def main():
    env = load_env()
    privkey = env.get("NOSTR_PRIVKEY")
    if not privkey:
        print("Error: NOSTR_PRIVKEY not found in .env")
        print("Run generate_keypair.py first to create your keys.")
        sys.exit(1)

    content = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "gm"

    print(f"Creating event: \"{content}\"")
    event = create_event(privkey, content)
    print(f"Event ID: {event['id']}")
    print(f"Pubkey: {event['pubkey']}")

    relays = [
        "wss://nos.lol",
        "wss://relay.damus.io",
        "wss://relay.nostr.band",
    ]

    for relay in relays:
        try:
            print(f"\nPosting to {relay}...")
            success, response = post_to_relay(relay, event)
            if success:
                print(f"  OK: {response}")
            else:
                print(f"  FAIL: {response}")
        except Exception as e:
            print(f"  ERROR: {e}")

    print(f"\nDone! View at: https://njump.me/{event['id']}")

if __name__ == "__main__":
    main()
