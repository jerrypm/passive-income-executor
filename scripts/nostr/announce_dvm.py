#!/usr/bin/env python3
"""
Announce DVM service on Nostr (NIP-89 App Handler).
Posts a kind 31990 event so clients can discover our DVM.
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from post_to_nostr import load_env, create_event, post_to_relay

# Import signing with tags
from dvm_text_generation import create_signed_event

def main():
    env = load_env()
    privkey = env.get("NOSTR_PRIVKEY")
    pubkey = env.get("NOSTR_PUBKEY")

    if not privkey:
        print("Error: NOSTR_PRIVKEY not found in .env")
        sys.exit(1)

    # NIP-89 Handler Information (kind 31990)
    handler_info = {
        "name": "Ollama AI DVM",
        "about": "Local AI text generation powered by Ollama. Send a kind 5050 event to get AI-generated text responses.",
        "picture": "",
        "nip90Params": {
            "model": {
                "required": False,
                "values": ["llama3"]
            }
        }
    }

    tags = [
        ["d", "ollama-ai-dvm"],
        ["k", "5050"],  # handles kind 5050
        ["web", f"https://njump.me/{pubkey}", "nip90"],
    ]

    event = create_signed_event(
        privkey,
        json.dumps(handler_info),
        31990,  # NIP-89 Handler Information
        tags
    )

    print("Announcing DVM on Nostr...")
    print(f"Event ID: {event['id']}")

    relays = ["wss://nos.lol", "wss://relay.damus.io"]
    for relay in relays:
        try:
            success, response = post_to_relay(relay, event)
            print(f"  {relay}: {response}")
        except Exception as e:
            print(f"  {relay}: ERROR - {e}")

    # Also post a regular note about the DVM
    from post_to_nostr import post_to_relay as post_note
    note_event = create_signed_event(
        privkey,
        "Just launched my AI DVM on Nostr! Send a kind 5050 event with your prompt to get AI-generated responses powered by local Ollama inference. #nostr #dvm #ai #ollama",
        1,
        []
    )
    print(f"\nPosting announcement note...")
    for relay in relays:
        try:
            success, response = post_to_relay(relay, note_event)
            print(f"  {relay}: {response}")
        except Exception as e:
            print(f"  {relay}: ERROR - {e}")

    print(f"\nDone! View at: https://njump.me/{note_event['id']}")

if __name__ == "__main__":
    main()
