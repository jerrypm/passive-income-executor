#!/usr/bin/env python3
"""
Batch post multiple SwiftUI Medium articles to Twitter + Nostr.
Usage: python3 batch_post.py 12 20
"""

import sys
import time
import datetime
from pathlib import Path

# Reuse functions from daily_medium_post
sys.path.insert(0, str(Path(__file__).resolve().parent))
from daily_medium_post import (
    load_articles, get_posted_parts, mark_posted,
    format_tweet, format_nostr_post, post_twitter, post_nostr, log
)


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 batch_post.py <start_part> <end_part>")
        sys.exit(1)

    start = int(sys.argv[1])
    end = int(sys.argv[2])

    data = load_articles()
    articles_map = {a["part"]: a for a in data["articles"]}
    list_url = data["list_url"]
    posted = get_posted_parts()

    log(f"=== BATCH POST: Part {start} to {end} ===")

    success_count = 0
    fail_count = 0

    for part in range(start, end + 1):
        if part not in articles_map:
            log(f"Part {part}: NOT FOUND in articles JSON, skipping")
            fail_count += 1
            continue

        article = articles_map[part]
        tweet = format_tweet(article, list_url)
        nostr_post = format_nostr_post(article, list_url)

        log(f"\n--- Part {part}: {article['title']} ---")
        log(f"Tweet ({len(tweet)} chars): {tweet[:80]}...")

        # Post to Twitter
        try:
            post_twitter(tweet)
            log(f"Twitter: Part {part} POSTED OK")
        except Exception as e:
            log(f"Twitter Part {part} FAILED: {e}")
            fail_count += 1
            continue

        time.sleep(3)

        # Post to Nostr
        try:
            post_nostr(nostr_post)
            log(f"Nostr: Part {part} POSTED OK")
        except Exception as e:
            log(f"Nostr Part {part} FAILED: {e}")

        # Mark as posted
        if part not in posted:
            mark_posted(part)
            posted.add(part)

        success_count += 1
        log(f"Part {part} DONE ({success_count}/{end - start + 1})")

        # Wait between posts to avoid rate limiting
        if part < end:
            log(f"Waiting 30s before next post...")
            time.sleep(30)

    log(f"\n=== BATCH COMPLETE: {success_count} success, {fail_count} failed ===")


if __name__ == "__main__":
    main()
