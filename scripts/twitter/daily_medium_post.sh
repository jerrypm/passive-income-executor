#!/bin/bash
# Daily Medium SwiftUI series poster
# Cron: 0 15 * * * /Users/avika/Documents/passive-income-executor/scripts/twitter/daily_medium_post.sh
#
# Posts next unposted part to: Twitter + Nostr
# Tracks progress in posted_parts.txt

export PATH="/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin:$HOME/go/bin:$HOME/go-sdk/go/bin:$PATH"
cd /Users/avika/Documents/passive-income-executor

echo "=== $(date) === Daily Medium SwiftUI Post ==="

python3 scripts/twitter/daily_medium_post.py 2>&1

echo "=== Done ==="
