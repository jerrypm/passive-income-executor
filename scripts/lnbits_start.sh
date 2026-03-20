#!/bin/bash
# Start LNbits on port 5001
# Uses FakeWallet for testing — switch to NWCWallet or PhoenixdWallet for production

set -euo pipefail

SITE_PACKAGES="/Users/avika/Library/Python/3.9/lib/python/site-packages"
DATA_DIR="/Users/avika/Documents/passive-income-executor/data/lnbits"
LOG_FILE="/Users/avika/Documents/passive-income-executor/logs/lnbits.log"
PORT=5001

# Check if already running
if curl -s http://127.0.0.1:$PORT/api/v1/health >/dev/null 2>&1; then
    echo "LNbits already running on port $PORT"
    exit 0
fi

mkdir -p "$DATA_DIR" "$(dirname "$LOG_FILE")"

cd "$SITE_PACKAGES"

LNBITS_BACKEND_WALLET_CLASS=FakeWallet \
FAKE_WALLET_SECRET=ToTheMoon1 \
LNBITS_DATA_FOLDER="$DATA_DIR" \
HOST=127.0.0.1 \
PORT=$PORT \
LNBITS_TITLE="Passive Income LNbits" \
python3 -m uvicorn lnbits.__main__:app --host 127.0.0.1 --port $PORT >> "$LOG_FILE" 2>&1 &

echo "LNbits started (PID: $!, port: $PORT)"
echo "Dashboard: http://127.0.0.1:$PORT"
echo "Log: $LOG_FILE"

# Wait for health
for i in 1 2 3 4 5; do
    sleep 2
    if curl -s http://127.0.0.1:$PORT/api/v1/health >/dev/null 2>&1; then
        echo "LNbits is healthy!"
        exit 0
    fi
done

echo "Warning: LNbits may not have started properly. Check $LOG_FILE"
