#!/usr/bin/env python3
"""
Publish long-form content to Nostr (kind 30023) for Habla.news and other readers.

NIP-23: Long-form Content
- kind: 30023
- tags: d (identifier), title, summary, published_at, t (hashtags), image
- content: Markdown text

Usage:
    python3 publish_longform.py --title "Title" --file article.md
    python3 publish_longform.py --title "Title" --content "Markdown content..."
"""

import json
import sys
import os
import time
import argparse

sys.path.insert(0, os.path.dirname(__file__))
from post_to_nostr import load_env, post_to_relay
from dvm_text_generation import create_signed_event


def slugify(text):
    """Create a URL-friendly slug."""
    slug = text.lower().strip()
    for ch in " _/\\:;.,!?'\"()[]{}":
        slug = slug.replace(ch, "-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")[:80]


def main():
    parser = argparse.ArgumentParser(description="Publish long-form content to Nostr")
    parser.add_argument("--title", required=True, help="Article title")
    parser.add_argument("--content", help="Article content (Markdown)")
    parser.add_argument("--file", help="Read content from file")
    parser.add_argument("--summary", help="Short summary")
    parser.add_argument("--tags", help="Comma-separated hashtags")
    parser.add_argument("--image", help="Header image URL")
    args = parser.parse_args()

    env = load_env()
    privkey = env.get("NOSTR_PRIVKEY")
    if not privkey:
        print("Error: NOSTR_PRIVKEY not found in .env")
        print("Run generate_keypair.py first.")
        sys.exit(1)

    # Get content
    if args.file:
        with open(args.file) as f:
            content = f.read()
    elif args.content:
        content = args.content
    else:
        print("Error: --content or --file required")
        sys.exit(1)

    # Build tags
    slug = slugify(args.title)
    now = str(int(time.time()))
    tags = [
        ["d", slug],
        ["title", args.title],
        ["published_at", now],
    ]

    if args.summary:
        tags.append(["summary", args.summary])
    else:
        # Auto-generate summary from first 200 chars
        summary = content[:200].replace("\n", " ").strip()
        if len(content) > 200:
            summary += "..."
        tags.append(["summary", summary])

    if args.image:
        tags.append(["image", args.image])

    if args.tags:
        for tag in args.tags.split(","):
            tags.append(["t", tag.strip().lower()])

    # Create kind 30023 event
    event = create_signed_event(privkey, content, 30023, tags)

    print(f"Publishing: \"{args.title}\"")
    print(f"Slug: {slug}")
    print(f"Event ID: {event['id']}")
    print(f"Content length: {len(content)} chars")

    relays = ["wss://nos.lol", "wss://relay.damus.io"]
    for relay in relays:
        try:
            success, response = post_to_relay(relay, event)
            status = "OK" if "true" in str(response) else "FAIL"
            print(f"  {relay}: {status} - {response}")
        except Exception as e:
            print(f"  {relay}: ERROR - {e}")

    print(f"\nView at: https://habla.news/a/{event['pubkey']}:{30023}:{slug}")
    print(f"Also at: https://njump.me/{event['id']}")


if __name__ == "__main__":
    main()
