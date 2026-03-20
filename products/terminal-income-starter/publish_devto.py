#!/usr/bin/env python3
"""
Publish articles to dev.to via API.

Setup:
  1. Get API key: https://dev.to/settings/extensions -> Generate API Key
  2. Add to .env: DEVTO_API_KEY=your_key_here

Usage:
  python3 publish_devto.py --title "Title" --file article.md --tags python,ai
  python3 publish_devto.py --title "Title" --content "Body..." --tags devops
"""

import json
import urllib.request
import os
import sys
import argparse

DEVTO_API = "https://dev.to/api/articles"


def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())


def publish(api_key, title, body, tags, canonical_url="", published=False):
    """Publish article to dev.to."""
    tag_list = [t.strip() for t in tags.split(",")][:4]  # max 4 tags

    article = {
        "article": {
            "title": title,
            "body_markdown": body,
            "published": published,
            "tags": tag_list,
        }
    }

    if canonical_url:
        article["article"]["canonical_url"] = canonical_url

    data = json.dumps(article).encode()
    req = urllib.request.Request(
        DEVTO_API,
        data=data,
        headers={
            "Content-Type": "application/json",
            "api-key": api_key,
        }
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
        return result


def main():
    load_env()

    parser = argparse.ArgumentParser(description="Publish to dev.to")
    parser.add_argument("--title", required=True)
    parser.add_argument("--content", help="Article body (Markdown)")
    parser.add_argument("--file", help="Read body from file")
    parser.add_argument("--tags", default="programming", help="Comma-separated tags (max 4)")
    parser.add_argument("--canonical", default="", help="Canonical URL")
    parser.add_argument("--publish", action="store_true", help="Publish immediately (default: draft)")
    args = parser.parse_args()

    api_key = os.environ.get("DEVTO_API_KEY", "")
    if not api_key:
        print("Error: DEVTO_API_KEY not set in .env")
        print("Get one at: https://dev.to/settings/extensions")
        sys.exit(1)

    if args.file:
        with open(args.file) as f:
            body = f.read()
    elif args.content:
        body = args.content
    else:
        print("Error: --content or --file required")
        sys.exit(1)

    print(f"Publishing to dev.to: \"{args.title}\"")
    print(f"  Tags: {args.tags}")
    print(f"  Status: {'published' if args.publish else 'draft'}")

    try:
        result = publish(api_key, args.title, body, args.tags, args.canonical, args.publish)
        print(f"  URL: {result.get('url', 'N/A')}")
        print(f"  ID: {result.get('id', 'N/A')}")
        print("Done!")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"Error {e.code}: {error_body}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
