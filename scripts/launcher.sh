#!/bin/bash
# Master Launcher — Start/Stop all passive income services
# Usage: ./scripts/launcher.sh [start|stop|status]

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$PROJECT_DIR/logs"
PID_DIR="$PROJECT_DIR/.pids"
mkdir -p "$LOG_DIR" "$PID_DIR"

start_service() {
    NAME=$1
    CMD=$2
    LOG="$LOG_DIR/$NAME.log"
    PID_FILE="$PID_DIR/$NAME.pid"

    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
        echo "  $NAME: already running (PID $(cat "$PID_FILE"))"
        return
    fi

    cd "$PROJECT_DIR"
    nohup $CMD >> "$LOG" 2>&1 &
    echo $! > "$PID_FILE"
    echo "  $NAME: started (PID $!)"
}

stop_service() {
    NAME=$1
    PID_FILE="$PID_DIR/$NAME.pid"

    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            kill "$PID"
            echo "  $NAME: stopped (PID $PID)"
        else
            echo "  $NAME: not running (stale PID)"
        fi
        rm -f "$PID_FILE"
    else
        echo "  $NAME: not running"
    fi
}

check_service() {
    NAME=$1
    PID_FILE="$PID_DIR/$NAME.pid"

    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
        echo "  $NAME: RUNNING (PID $(cat "$PID_FILE"))"
    else
        echo "  $NAME: STOPPED"
    fi
}

case "${1:-status}" in
    start)
        echo "Starting passive income services..."
        echo ""

        # Ensure Ollama is running
        if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
            echo "  Starting Ollama..."
            ollama serve &>/dev/null &
            sleep 2
        fi
        echo "  ollama: running"

        # Start LNbits (payment backend)
        bash scripts/lnbits_start.sh
        sleep 2

        start_service "dvm" "python3 scripts/nostr/dvm_text_generation.py"
        start_service "api-server" "python3 scripts/ai-inference/ollama_api_server.py"
        start_service "rapidapi" "python3 scripts/ai-inference/rapidapi_wrapper.py"
        echo ""
        echo "All services started. Check logs in $LOG_DIR/"
        ;;

    stop)
        echo "Stopping services..."
        stop_service "dvm"
        stop_service "api-server"
        stop_service "rapidapi"
        pkill -f "uvicorn lnbits" 2>/dev/null && echo "  lnbits: stopped" || echo "  lnbits: not running"
        echo ""
        echo "Ollama left running (stop manually: pkill ollama)"
        ;;

    status)
        echo "=== Passive Income Services ==="
        echo ""

        # Ollama
        if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
            MODELS=$(curl -s http://localhost:11434/api/tags | python3 -c "import json,sys; d=json.load(sys.stdin); print(', '.join(m['name'] for m in d.get('models',[])))" 2>/dev/null)
            echo "  ollama: RUNNING (models: $MODELS)"
        else
            echo "  ollama: STOPPED"
        fi

        # LNbits
        if curl -s http://127.0.0.1:5001/api/v1/health >/dev/null 2>&1; then
            echo "  lnbits: RUNNING (port 5001)"
        else
            echo "  lnbits: STOPPED"
        fi

        check_service "dvm"
        check_service "api-server"
        check_service "rapidapi"

        echo ""
        echo "=== Cron Jobs ==="
        crontab -l 2>/dev/null | grep -v "^#" | while read line; do
            echo "  $line"
        done

        echo ""
        echo "=== Nostr Identity ==="
        if [ -f "$PROJECT_DIR/.env" ]; then
            NPUB=$(grep NOSTR_NPUB "$PROJECT_DIR/.env" | cut -d= -f2)
            echo "  npub: $NPUB"
        fi
        ;;

    *)
        echo "Usage: $0 [start|stop|status]"
        ;;
esac
