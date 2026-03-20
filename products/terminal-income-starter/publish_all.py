#!/usr/bin/env python3
"""
Cross-publish an article to all platforms at once:
  - Nostr (Habla.news) -- if NOSTR_PRIVKEY is set
  - dev.to -- if DEVTO_API_KEY is set
  - Hashnode -- if HASHNODE_API_KEY is set

Usage:
  python3 publish_all.py --title "Title" --file article.md --tags ai,python
"""

import subprocess
import sys
import os
import argparse


def run_script(script, args_list):
    """Run a publisher script and return success status."""
    cmd = [sys.executable, script] + args_list
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"  Error: {e}")
        return False


def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())


def main():
    load_env()
    script_dir = os.path.dirname(__file__)

    parser = argparse.ArgumentParser(description="Cross-publish article to all platforms")
    parser.add_argument("--title", required=True)
    parser.add_argument("--file", required=True, help="Markdown file")
    parser.add_argument("--tags", default="programming", help="Comma-separated tags")
    parser.add_argument("--summary", help="Short summary")
    args = parser.parse_args()

    results = {}

    print("=" * 60)
    print(f"CROSS-PUBLISHING: {args.title}")
    print("=" * 60)

    # 1. dev.to
    if os.environ.get("DEVTO_API_KEY"):
        print("\n--- dev.to ---")
        devto_args = ["--title", args.title, "--file", args.file, "--tags", args.tags]
        results["devto"] = run_script(os.path.join(script_dir, "publish_devto.py"), devto_args)
    else:
        print("\n--- dev.to: SKIPPED (DEVTO_API_KEY not set) ---")
        results["devto"] = None

    # 2. Hashnode
    if os.environ.get("HASHNODE_API_KEY"):
        print("\n--- Hashnode ---")
        hn_tags = args.tags.split(",")
        hn_args = ["--title", args.title, "--file", args.file, "--tags"] + hn_tags
        results["hashnode"] = run_script(os.path.join(script_dir, "publish_hashnode.py"), hn_args)
    else:
        print("\n--- Hashnode: SKIPPED (HASHNODE_API_KEY not set) ---")
        results["hashnode"] = None

    # Summary
    print("\n" + "=" * 60)
    print("RESULTS:")
    for platform, status in results.items():
        if status is True:
            icon = "OK"
        elif status is False:
            icon = "FAILED"
        else:
            icon = "SKIPPED"
        print(f"  {platform:<12} {icon}")
    print("=" * 60)


if __name__ == "__main__":
    main()
