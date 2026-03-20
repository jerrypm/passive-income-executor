#!/usr/bin/env python3
"""
List a digital product on Nostr marketplace (Shopstr / NIP-15 Marketplace).

NIP-15 Nostr Marketplace:
- kind 30017: Product listing (parameterized replaceable)
- tags: d, title, summary, price, currency, t, image, etc.

Usage:
    python3 list_product_shopstr.py
"""

import json
import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))
from post_to_nostr import load_env, post_to_relay
from dvm_text_generation import create_signed_event


def list_product(privkey, title, description, price_sats, category, tags_list, image=""):
    """Create a NIP-15 product listing."""
    slug = title.lower().replace(" ", "-")[:60]

    tags = [
        ["d", slug],
        ["title", title],
        ["summary", description[:200]],
        ["price", str(price_sats), "sat"],
        ["t", category],
        ["type", "digital"],
    ]

    if image:
        tags.append(["image", image])

    for t in tags_list:
        tags.append(["t", t.lower()])

    event = create_signed_event(privkey, description, 30017, tags)
    return event, slug


def main():
    env = load_env()
    privkey = env.get("NOSTR_PRIVKEY")
    if not privkey:
        print("Error: NOSTR_PRIVKEY not found in .env")
        sys.exit(1)

    # Product listings
    products = [
        {
            "title": "AI Text Generation API Access (100 requests)",
            "description": (
                "Get 100 API calls to my local Ollama AI inference server. "
                "Supports llama3, codellama, and deepseek-r1 models.\n\n"
                "What you get:\n"
                "- 100 API requests (text generation or chat)\n"
                "- Access to multiple AI models\n"
                "- No data logging, full privacy\n"
                "- API documentation included\n\n"
                "After purchase, you'll receive an API key via DM."
            ),
            "price_sats": 1000,
            "category": "digital",
            "tags": ["ai", "api", "ollama", "llm", "text-generation"],
        },
        {
            "title": "Terminal Passive Income Setup Guide",
            "description": (
                "Complete guide to setting up passive income streams entirely from the terminal.\n\n"
                "Includes:\n"
                "- Local AI monetization (Ollama + DVM)\n"
                "- Nostr identity & daily posting automation\n"
                "- Lightning Network payment setup\n"
                "- API paywall configuration\n"
                "- Content publishing pipeline\n"
                "- All scripts included (Python, Bash)\n\n"
                "No platforms, no registrations, pure terminal."
            ),
            "price_sats": 5000,
            "category": "digital",
            "tags": ["guide", "passive-income", "terminal", "bitcoin", "nostr"],
        },
        {
            "title": "Custom AI Bot for Your Nostr Profile",
            "description": (
                "I'll set up a custom AI-powered bot for your Nostr profile.\n\n"
                "Features:\n"
                "- Auto-reply to mentions with AI responses\n"
                "- Customizable personality/system prompt\n"
                "- Runs on your hardware (Ollama)\n"
                "- Full source code included\n"
                "- Setup assistance via DM\n\n"
                "DM me after purchase to discuss your requirements."
            ),
            "price_sats": 10000,
            "category": "service",
            "tags": ["ai", "bot", "nostr", "custom", "service"],
        },
    ]

    relays = ["wss://nos.lol", "wss://relay.damus.io"]

    print("=" * 60)
    print("LISTING PRODUCTS ON NOSTR MARKETPLACE")
    print("=" * 60)

    for product in products:
        event, slug = list_product(
            privkey,
            product["title"],
            product["description"],
            product["price_sats"],
            product["category"],
            product["tags"]
        )

        print(f"\nProduct: {product['title']}")
        print(f"  Price: {product['price_sats']} sats")
        print(f"  Event ID: {event['id']}")

        for relay in relays:
            try:
                success, response = post_to_relay(relay, event)
                status = "OK" if "true" in str(response) else "FAIL"
                print(f"  {relay}: {status}")
            except Exception as e:
                print(f"  {relay}: ERROR - {e}")

    print(f"\nView on Shopstr: https://shopstr.store")
    print("Products are now discoverable on any NIP-15 compatible client!")


if __name__ == "__main__":
    main()
