#!/bin/bash
# Twitter Auto Post — Cron Script
# Posts 3x/day with rotating referral, promo, and organic content
#
# Cron schedule (add via: crontab -e):
#   0 9 * * * /Users/avika/Documents/passive-income-executor/scripts/twitter/daily_twitter.sh >> /Users/avika/Documents/passive-income-executor/logs/twitter-cron.log 2>&1
#   0 14 * * * /Users/avika/Documents/passive-income-executor/scripts/twitter/daily_twitter.sh >> /Users/avika/Documents/passive-income-executor/logs/twitter-cron.log 2>&1
#   0 19 * * * /Users/avika/Documents/passive-income-executor/scripts/twitter/daily_twitter.sh >> /Users/avika/Documents/passive-income-executor/logs/twitter-cron.log 2>&1

export PATH="/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin:$HOME/go/bin:$HOME/go-sdk/go/bin:/Users/avika/Library/Python/3.9/bin:$PATH"
cd /Users/avika/Documents/passive-income-executor

echo "=== $(date) === Twitter Auto Post ==="

/usr/bin/python3 scripts/twitter/auto_post_twitter.py 2>&1

echo "=== Done ==="
