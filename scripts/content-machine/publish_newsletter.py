#!/usr/bin/env python3
"""
Publish newsletter content — formats for copy-paste to Substack/Beehiiv
and cross-posts a teaser to Nostr.

Substack doesn't have a public API, so this script:
  1. Outputs the formatted newsletter content for manual paste
  2. Copies it to clipboard (macOS pbcopy) if available
  3. Cross-posts a teaser + link to Nostr automatically

Usage:
    python3 publish_newsletter.py --file articles/newsletter_issue_1.md
    python3 publish_newsletter.py --file articles/newsletter_issue_1.md --no-nostr
    python3 publish_newsletter.py --file articles/newsletter_issue_1.md --teaser "Custom teaser text"
"""

import os
import sys
import argparse
import subprocess
import re

# Add parent dirs for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "nostr"))


def load_env():
    """Load environment variables from .env file."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
    env = {}
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
    return env


def extract_title(content):
    """Extract the first H1 title from markdown content."""
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return "Untitled Newsletter"


def extract_teaser(content, max_length=280):
    """Extract a teaser from the newsletter content for social posting.

    Looks for the first substantial paragraph after the title.
    """
    lines = content.split("\n")
    in_frontmatter = False
    paragraphs = []
    current = []

    for line in lines:
        stripped = line.strip()

        # Skip title and metadata
        if stripped.startswith("# ") or stripped.startswith("*Issue"):
            continue
        if stripped == "---":
            continue
        if stripped.startswith("```"):
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue

        # Skip headers, tables, empty lines
        if stripped.startswith("#") or stripped.startswith("|"):
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue

        if stripped:
            current.append(stripped)
        else:
            if current:
                paragraphs.append(" ".join(current))
                current = []

    if current:
        paragraphs.append(" ".join(current))

    # Find a good paragraph for teaser (not too short)
    for p in paragraphs:
        # Skip very short lines or formatting artifacts
        if len(p) > 50 and not p.startswith("```") and not p.startswith("|"):
            if len(p) <= max_length:
                return p
            return p[:max_length - 3] + "..."

    return "New newsletter issue just dropped!"


def format_for_clipboard(content):
    """Format the content for pasting into Substack/Beehiiv editor.

    Both platforms accept markdown, so we mostly pass it through.
    Minor cleanup for better rendering.
    """
    # Remove the issue subtitle line (Substack has its own)
    lines = content.split("\n")
    cleaned = []
    for line in lines:
        # Skip the subtitle/issue line
        if line.strip().startswith("*Issue #") and line.strip().endswith("*"):
            continue
        cleaned.append(line)

    return "\n".join(cleaned)


def copy_to_clipboard(text):
    """Copy text to macOS clipboard using pbcopy."""
    try:
        process = subprocess.Popen(
            ["pbcopy"],
            stdin=subprocess.PIPE,
            env={"PATH": "/usr/bin:/bin"}
        )
        process.communicate(text.encode("utf-8"))
        return process.returncode == 0
    except FileNotFoundError:
        return False
    except Exception:
        return False


def post_teaser_to_nostr(env, title, teaser, newsletter_url=None):
    """Post a teaser to Nostr promoting the newsletter."""
    privkey = env.get("NOSTR_PRIVKEY")
    if not privkey:
        print("  NOSTR_PRIVKEY not found in .env — skipping Nostr post")
        return False

    # Build the teaser post
    parts = []
    parts.append(f"NEW NEWSLETTER: {title}")
    parts.append("")
    parts.append(teaser)
    parts.append("")

    if newsletter_url:
        parts.append(f"Read the full issue: {newsletter_url}")
        parts.append("")

    parts.append("Subscribe for weekly updates on building passive income from the terminal.")
    parts.append("")
    parts.append("#buildinpublic #passiveincome #developer #nostr #bitcoin #ai")

    content = "\n".join(parts)

    try:
        from post_to_nostr import create_event, post_to_relay

        print(f"\n  Creating Nostr event...")
        event = create_event(privkey, content)
        print(f"  Event ID: {event['id']}")

        relays = [
            "wss://nos.lol",
            "wss://relay.damus.io",
            "wss://relay.nostr.band",
        ]

        success_count = 0
        for relay in relays:
            try:
                success, response = post_to_relay(relay, event)
                status = "OK" if success else "FAIL"
                print(f"  {relay}: {status}")
                if success:
                    success_count += 1
            except Exception as e:
                print(f"  {relay}: ERROR - {e}")

        if success_count > 0:
            print(f"\n  Nostr teaser posted! View at: https://njump.me/{event['id']}")
            return True
        else:
            print("  Warning: Failed to post to any relay")
            return False

    except ImportError as e:
        print(f"  Could not import Nostr modules: {e}")
        return False
    except Exception as e:
        print(f"  Error posting to Nostr: {e}")
        return False


def post_longform_to_nostr(env, title, content):
    """Also publish the full newsletter as a long-form article on Nostr (NIP-23)."""
    privkey = env.get("NOSTR_PRIVKEY")
    if not privkey:
        return False

    try:
        from post_to_nostr import post_to_relay
        from dvm_text_generation import create_signed_event
        import time

        # Create slug
        slug = title.lower().strip()
        for ch in " _/\\:;.,!?'\"()[]{}":
            slug = slug.replace(ch, "-")
        while "--" in slug:
            slug = slug.replace("--", "-")
        slug = slug.strip("-")[:80]

        now = str(int(time.time()))
        tags = [
            ["d", slug],
            ["title", title],
            ["published_at", now],
            ["summary", f"Newsletter issue: {title}"],
            ["t", "newsletter"],
            ["t", "passiveincome"],
            ["t", "developer"],
            ["t", "buildinpublic"],
        ]

        event = create_signed_event(privkey, content, 30023, tags)
        print(f"\n  Publishing long-form to Nostr...")
        print(f"  Event ID: {event['id']}")

        relays = ["wss://nos.lol", "wss://relay.damus.io"]
        for relay in relays:
            try:
                success, response = post_to_relay(relay, event)
                status = "OK" if success else "FAIL"
                print(f"  {relay}: {status}")
            except Exception as e:
                print(f"  {relay}: ERROR - {e}")

        print(f"  View at: https://habla.news/a/{event['pubkey']}:30023:{slug}")
        return True

    except Exception as e:
        print(f"  Error publishing long-form: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Format newsletter for Substack/Beehiiv and cross-post teaser to Nostr"
    )
    parser.add_argument("--file", required=True, help="Path to newsletter markdown file")
    parser.add_argument("--teaser", help="Custom teaser text for Nostr post")
    parser.add_argument("--url", help="Newsletter URL (Substack/Beehiiv link to include in teaser)")
    parser.add_argument("--no-nostr", action="store_true", help="Skip posting to Nostr")
    parser.add_argument("--no-longform", action="store_true", help="Skip long-form NIP-23 post")
    parser.add_argument("--no-clipboard", action="store_true", help="Skip copying to clipboard")
    parser.add_argument("--output", help="Write formatted content to file instead of stdout")
    args = parser.parse_args()

    env = load_env()

    # Read newsletter content
    file_path = args.file
    if not os.path.isabs(file_path):
        file_path = os.path.join(os.path.dirname(__file__), file_path)

    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    with open(file_path) as f:
        raw_content = f.read()

    title = extract_title(raw_content)
    formatted = format_for_clipboard(raw_content)
    teaser = args.teaser or extract_teaser(raw_content)

    print("=" * 60)
    print("NEWSLETTER PUBLISHER")
    print("=" * 60)
    print(f"Title: {title}")
    print(f"Length: {len(raw_content)} chars (~{len(raw_content.split())} words)")
    print(f"Teaser: {teaser[:100]}...")

    # Step 1: Copy to clipboard for Substack/Beehiiv
    if not args.no_clipboard:
        print("\n--- Clipboard ---")
        if copy_to_clipboard(formatted):
            print("  Content copied to clipboard!")
            print("  Paste into Substack/Beehiiv editor.")
        else:
            print("  Could not copy to clipboard (pbcopy not available)")
            print("  Use --output flag to write to a file instead.")

    # Step 2: Write to file if requested
    if args.output:
        print(f"\n--- Output File ---")
        with open(args.output, "w") as f:
            f.write(formatted)
        print(f"  Written to: {args.output}")

    # Step 3: Post teaser to Nostr
    if not args.no_nostr:
        print("\n--- Nostr Teaser ---")
        post_teaser_to_nostr(env, title, teaser, args.url)

    # Step 4: Post full newsletter as long-form on Nostr
    if not args.no_nostr and not args.no_longform:
        print("\n--- Nostr Long-Form (NIP-23) ---")
        post_longform_to_nostr(env, title, raw_content)

    # Step 5: Show the formatted content preview
    print("\n" + "=" * 60)
    print("CONTENT PREVIEW (first 500 chars)")
    print("=" * 60)
    print(formatted[:500])
    print("...")
    print("=" * 60)

    print("\nNEXT STEPS:")
    print("  1. Go to Substack/Beehiiv and create a new post")
    print("  2. Paste the content (already in your clipboard)")
    print("  3. Set the title, preview text, and schedule")
    print("  4. Publish!")
    if args.url:
        print(f"  5. Nostr teaser links to: {args.url}")
    else:
        print("  5. Re-run with --url <link> to post Nostr teaser with newsletter link")


if __name__ == "__main__":
    main()
