#!/bin/bash
# Daily Nostr post script - run via cron
# Posts a "gm" message with day number using nak CLI

set -euo pipefail

# Load env
cd "$(dirname "$0")/../.."
source .env

DAY=$(( ($(date +%s) - 1741824000) / 86400 ))  # days since project start (Mar 13, 2026)

export PATH="$HOME/go/bin:$PATH"

nak event --sec "$NOSTR_NSEC" \
  -c "gm! Day ${DAY} of building in public. #nostr #buildinpublic" \
  wss://nos.lol \
  >> logs/nostr-cron.log 2>&1
