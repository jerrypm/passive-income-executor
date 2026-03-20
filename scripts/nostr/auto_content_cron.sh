#!/bin/bash
# Nostr Auto Content — Cron wrapper
# Cron: 0 12,18 * * * /Users/avika/Documents/passive-income-executor/scripts/nostr/auto_content_cron.sh >> /Users/avika/Documents/passive-income-executor/logs/auto-content.log 2>&1

export PATH="/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin:$HOME/go/bin:$HOME/go-sdk/go/bin:$PATH"
cd /Users/avika/Documents/passive-income-executor

echo "=== $(date) === Auto Content ==="

/usr/bin/python3 scripts/nostr/auto_content.py 2>&1

echo "=== Done ==="
