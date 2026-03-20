#!/usr/bin/env python3
"""
Auto-generate and post content to Nostr using Ollama.
Generates AI/dev/Nostr tips and posts them automatically.

Usage:
    python3 auto_content.py              # generate and post 1 tip
    python3 auto_content.py --dry-run    # generate but don't post
    python3 auto_content.py --topic "python"  # specific topic
"""

import json
import sys
import os
import urllib.request
import random
import argparse

sys.path.insert(0, os.path.dirname(__file__))
from post_to_nostr import load_env, create_event, websocket_send

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"  # Change to any Ollama model you have

TOPICS = [
    "a useful terminal/CLI tip for developers",
    "a Python one-liner that saves time",
    "why running AI locally (Ollama) matters for privacy",
    "a cool thing you can do with Nostr protocol",
    "a Bitcoin/Lightning Network tip for beginners",
    "a productivity hack for programmers",
    "an interesting fact about decentralized technology",
    "a simple automation idea that saves hours",
    "why open source software matters",
    "a tip about securing your digital life",
]

PROMPT_TEMPLATE = """Write a short social media post (max 280 chars) about {topic}.
Rules:
- Be concise and informative
- Use 1-2 relevant emojis
- Include 2-3 hashtags at the end
- Don't use quotes around the post
- Write as a developer sharing a genuine tip
- Do NOT start with "Here is" or "Here's"
Just output the post text, nothing else."""


def query_ollama(prompt):
    data = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())
        return result.get("response", "").strip()


def post_to_relays(content, privkey):
    event = create_event(privkey, content)
    relays = [
        ("nos.lol", 443, "/"),
        ("relay.damus.io", 443, "/"),
    ]
    results = []
    for host, port, path in relays:
        try:
            message = json.dumps(["EVENT", event])
            ok, resp = websocket_send(host, port, path, message)
            results.append((host, ok, resp))
        except Exception as e:
            results.append((host, False, str(e)))
    return event, results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--topic", type=str, default=None)
    args = parser.parse_args()

    env = load_env()
    privkey = env.get("NOSTR_PRIVKEY")
    if not privkey:
        print("Error: NOSTR_PRIVKEY not found in .env")
        print("Run generate_keypair.py first.")
        sys.exit(1)

    topic = args.topic or random.choice(TOPICS)
    prompt = PROMPT_TEMPLATE.format(topic=topic)

    print(f"Topic: {topic}")
    print("Generating content with Ollama...")

    content = query_ollama(prompt)
    # Clean up - remove quotes if wrapped
    content = content.strip('"').strip("'").strip()
    # Truncate if too long
    if len(content) > 500:
        content = content[:497] + "..."

    print(f"\nGenerated post:\n{content}\n")

    if args.dry_run:
        print("(dry run -- not posting)")
        return

    event, results = post_to_relays(content, privkey)
    print(f"Event ID: {event['id']}")
    for host, ok, resp in results:
        status = "OK" if ok else "FAIL"
        print(f"  [{host}] {status}: {resp}")

    print(f"\nView: https://njump.me/{event['id']}")


if __name__ == "__main__":
    main()
