#!/bin/bash
# Quick Nostr post using nak CLI
# Usage: ./nak_post.sh "Your message here"
# Usage: ./nak_post.sh (interactive - reads from stdin)

set -euo pipefail

cd "$(dirname "$0")/../.."
source .env

export PATH="$HOME/go/bin:$PATH"

RELAYS="wss://nos.lol"

if [ $# -gt 0 ]; then
  MSG="$*"
else
  echo "Type your post (Ctrl+D to send):"
  MSG=$(cat)
fi

if [ -z "$MSG" ]; then
  echo "Error: empty message"
  exit 1
fi

echo "Posting: $MSG"
nak event --sec "$NOSTR_NSEC" -c "$MSG" $RELAYS
echo "Done!"
