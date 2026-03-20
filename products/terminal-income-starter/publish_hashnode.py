#!/usr/bin/env python3
"""
Publish articles to Hashnode via GraphQL API.

Setup:
  1. Get API key: https://hashnode.com/settings/developer -> Personal Access Token
  2. Get publication ID: from your Hashnode blog URL
  3. Add to .env:
     HASHNODE_API_KEY=your_token
     HASHNODE_PUBLICATION_ID=your_pub_id

Usage:
  python3 publish_hashnode.py --title "Title" --file article.md --tags python ai
"""

import json
import urllib.request
import os
import sys
import argparse

HASHNODE_API = "https://gql.hashnode.com"


def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())


def slugify(text):
    slug = text.lower().strip()
    for ch in " _/\\:;.,!?'\"()[]{}":
        slug = slug.replace(ch, "-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")[:100]


def publish(api_key, pub_id, title, body, tags):
    """Publish article to Hashnode via GraphQL."""
    tag_objects = [{"slug": t.strip().lower(), "name": t.strip()} for t in tags]

    query = """
    mutation PublishPost($input: PublishPostInput!) {
        publishPost(input: $input) {
            post {
                id
                title
                slug
                url
            }
        }
    }
    """

    variables = {
        "input": {
            "title": title,
            "contentMarkdown": body,
            "publicationId": pub_id,
            "slug": slugify(title),
            "tags": tag_objects,
        }
    }

    data = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        HASHNODE_API,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": api_key,
        }
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def main():
    load_env()

    parser = argparse.ArgumentParser(description="Publish to Hashnode")
    parser.add_argument("--title", required=True)
    parser.add_argument("--content", help="Article body (Markdown)")
    parser.add_argument("--file", help="Read body from file")
    parser.add_argument("--tags", nargs="+", default=["programming"], help="Tags")
    args = parser.parse_args()

    api_key = os.environ.get("HASHNODE_API_KEY", "")
    pub_id = os.environ.get("HASHNODE_PUBLICATION_ID", "")

    if not api_key:
        print("Error: HASHNODE_API_KEY not set in .env")
        print("Get one at: https://hashnode.com/settings/developer")
        sys.exit(1)
    if not pub_id:
        print("Error: HASHNODE_PUBLICATION_ID not set in .env")
        sys.exit(1)

    if args.file:
        with open(args.file) as f:
            body = f.read()
    elif args.content:
        body = args.content
    else:
        print("Error: --content or --file required")
        sys.exit(1)

    print(f"Publishing to Hashnode: \"{args.title}\"")
    print(f"  Tags: {', '.join(args.tags)}")

    try:
        result = publish(api_key, pub_id, args.title, body, args.tags)
        post = result.get("data", {}).get("publishPost", {}).get("post", {})
        if post:
            print(f"  URL: {post.get('url', 'N/A')}")
            print(f"  Slug: {post.get('slug', 'N/A')}")
            print("Done!")
        else:
            errors = result.get("errors", [])
            print(f"Error: {errors}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
