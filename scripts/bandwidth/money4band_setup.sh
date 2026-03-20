#!/bin/bash
# money4band — Bandwidth Sharing Docker Stack
# Earns passive income by sharing unused bandwidth
# Repo: github.com/MRColorR/money4band
#
# Includes: Honeygain, EarnApp, PacketStream, Peer2Profit, etc.
# Requires: Docker

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
M4B_DIR="$PROJECT_DIR/services/money4band"

check_docker() {
    export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
    if ! command -v docker &>/dev/null; then
        echo "Docker not found. Install Docker Desktop first:"
        echo "  https://www.docker.com/products/docker-desktop/"
        exit 1
    fi
    echo "Docker: $(docker --version)"
}

setup() {
    if [ -d "$M4B_DIR/.git" ]; then
        echo "money4band already cloned at $M4B_DIR"
        echo "Run: cd $M4B_DIR && bash runme.sh"
        return
    fi

    echo "Cloning money4band..."
    git clone https://github.com/MRColorR/money4band.git "$M4B_DIR"

    echo ""
    echo "============================================"
    echo "money4band setup complete!"
    echo "============================================"
    echo ""
    echo "Next steps:"
    echo "  1. Register at these platforms (free):"
    echo "     - Honeygain:    https://r.honeygain.me/"
    echo "     - EarnApp:      https://earnapp.com/"
    echo "     - PacketStream: https://packetstream.io/"
    echo "     - Peer2Profit:  https://peer2profit.com/"
    echo "     - Repocket:     https://repocket.com/"
    echo ""
    echo "  2. Run the interactive setup:"
    echo "     cd $M4B_DIR"
    echo "     bash runme.sh"
    echo ""
    echo "  3. The script will ask for your account details"
    echo "     and generate a docker-compose.yml"
    echo ""
    echo "  4. Start earning:"
    echo "     docker compose up -d"
    echo ""
    echo "Expected earnings: \$10-30/month (depends on location)"
}

status() {
    if [ ! -d "$M4B_DIR" ]; then
        echo "Not set up yet. Run: $0 setup"
        exit 1
    fi
    cd "$M4B_DIR"
    docker compose ps 2>/dev/null || echo "Not running"
}

start() {
    cd "$M4B_DIR" 2>/dev/null || { echo "Not set up. Run: $0 setup"; exit 1; }
    docker compose up -d
    echo "money4band started"
}

stop() {
    cd "$M4B_DIR" 2>/dev/null || exit 1
    docker compose down
    echo "money4band stopped"
}

case "${1:-help}" in
    setup)  check_docker && setup ;;
    start)  check_docker && start ;;
    stop)   check_docker && stop ;;
    status) check_docker && status ;;
    help|*)
        echo "money4band — Bandwidth Sharing"
        echo ""
        echo "Usage: $0 <command>"
        echo "  setup   Clone repo and show registration links"
        echo "  start   Start Docker containers"
        echo "  stop    Stop containers"
        echo "  status  Check running status"
        echo ""
        echo "Expected: \$10-30/month passive income"
        ;;
esac
