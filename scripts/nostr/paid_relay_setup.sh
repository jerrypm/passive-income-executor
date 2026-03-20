#!/bin/bash
# Paid Nostr Relay Setup (nostream)
# Requires: Docker, LNbits or LND
#
# nostream is a Nostr relay that charges sats for write access.
# Revenue model: users pay to post/store events on your relay.

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

check_docker() {
    if ! command -v docker &>/dev/null; then
        echo "Docker not found. Install Docker Desktop first."
        echo "  https://www.docker.com/products/docker-desktop/"
        exit 1
    fi
    if ! command -v docker-compose &>/dev/null && ! docker compose version &>/dev/null; then
        echo "docker-compose not found."
        exit 1
    fi
    echo "Docker: $(docker --version)"
}

setup_nostream() {
    RELAY_DIR="$PROJECT_DIR/services/nostream"
    mkdir -p "$RELAY_DIR"

    if [ -d "$RELAY_DIR/.git" ]; then
        echo "nostream already cloned"
    else
        echo "Cloning nostream..."
        git clone https://github.com/cameri/nostream.git "$RELAY_DIR"
    fi

    cd "$RELAY_DIR"

    # Create .env for nostream
    cat > .env << 'ENVEOF'
RELAY_PORT=7777
NOSTREAM_CONFIG_DIR=.

# Database
DB_HOST=db
DB_PORT=5432
DB_NAME=nostream
DB_USER=nostream
DB_PASSWORD=nostream_password

# Redis
REDIS_HOST=cache
REDIS_PORT=6379

# Payment (LNbits)
PAYMENTS_ENABLED=true
PAYMENTS_PROCESSOR=lnbits
LNBITS_BASE_URL=http://host.docker.internal:5000
# Set your LNbits invoice key below:
# LNBITS_API_KEY=your_invoice_key_here

# Admission fee (sats to write)
ADMISSION_FEE_ENABLED=true
ADMISSION_FEE_AMOUNT=1000
ENVEOF

    echo ""
    echo "nostream setup complete!"
    echo ""
    echo "To start the relay:"
    echo "  cd $RELAY_DIR"
    echo "  docker compose up -d"
    echo ""
    echo "Relay will be at: ws://localhost:7777"
    echo ""
    echo "Before starting, edit $RELAY_DIR/.env and set:"
    echo "  - LNBITS_API_KEY (from your LNbits instance)"
    echo "  - ADMISSION_FEE_AMOUNT (sats to charge)"
}

status() {
    RELAY_DIR="$PROJECT_DIR/services/nostream"
    cd "$RELAY_DIR" 2>/dev/null || { echo "nostream not set up yet"; exit 1; }
    docker compose ps 2>/dev/null || echo "Relay not running"
}

start() {
    RELAY_DIR="$PROJECT_DIR/services/nostream"
    cd "$RELAY_DIR" 2>/dev/null || { echo "nostream not set up yet. Run: $0 setup"; exit 1; }
    docker compose up -d
    echo "Relay started at ws://localhost:7777"
}

stop() {
    RELAY_DIR="$PROJECT_DIR/services/nostream"
    cd "$RELAY_DIR" 2>/dev/null || exit 1
    docker compose down
    echo "Relay stopped"
}

case "${1:-help}" in
    setup)  check_docker && setup_nostream ;;
    start)  check_docker && start ;;
    stop)   check_docker && stop ;;
    status) check_docker && status ;;
    help|*)
        echo "Paid Nostr Relay (nostream) Manager"
        echo ""
        echo "Usage: $0 <command>"
        echo ""
        echo "Commands:"
        echo "  setup   Clone and configure nostream"
        echo "  start   Start the relay (Docker)"
        echo "  stop    Stop the relay"
        echo "  status  Check relay status"
        echo ""
        echo "Revenue: Charges admission fee (sats) for write access"
        echo "Requires: Docker, LNbits"
        ;;
esac
