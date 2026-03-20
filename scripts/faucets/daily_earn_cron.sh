#!/bin/bash
# Daily Earn Faucet — Cron wrapper
# Cron: 0 8,20 * * * /Users/avika/Documents/passive-income-executor/scripts/faucets/daily_earn_cron.sh >> /Users/avika/Documents/passive-income-executor/logs/daily-earn.log 2>&1

export PATH="/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin:$HOME/go/bin:$HOME/go-sdk/go/bin:$PATH"
cd /Users/avika/Documents/passive-income-executor

echo "=== $(date) === Daily Earn ==="

/usr/bin/python3 scripts/faucets/daily_earn.py 2>&1

echo "=== Done ==="
