#!/bin/bash
# ==============================================================
# Telegram Bot Setup Script
# Creates and tests the Ollama Telegram Bot
# ==============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"
BOT_SCRIPT="$SCRIPT_DIR/ollama_telegram_bot.py"

echo "============================================================"
echo "  OLLAMA TELEGRAM BOT — SETUP"
echo "============================================================"
echo ""

# Step 1: Instructions for creating the bot
echo "STEP 1: Create a Telegram Bot"
echo "------------------------------------------------------------"
echo ""
echo "  1. Open Telegram and search for @BotFather"
echo "  2. Send /newbot"
echo "  3. Choose a display name (e.g., 'Ollama AI Bot')"
echo "  4. Choose a username (must end in 'bot', e.g., 'my_ollama_bot')"
echo "  5. BotFather will give you a token like:"
echo "     123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
echo ""
echo "  Optional — customize your bot:"
echo "    /setdescription — Set bot description"
echo "    /setabouttext   — Set 'About' section"
echo "    /setuserpic     — Set bot profile photo"
echo "    /setcommands    — Set command menu:"
echo "      ask - Ask the AI a question"
echo "      models - List available AI models"
echo "      help - Show help message"
echo ""

# Step 2: Check if token already exists
if [ -f "$ENV_FILE" ] && grep -q "TELEGRAM_BOT_TOKEN" "$ENV_FILE" 2>/dev/null; then
    EXISTING_TOKEN=$(grep "TELEGRAM_BOT_TOKEN" "$ENV_FILE" | head -1 | cut -d'=' -f2 | tr -d ' ')
    if [ -n "$EXISTING_TOKEN" ] && [ "$EXISTING_TOKEN" != "" ]; then
        echo "STEP 2: Bot Token"
        echo "------------------------------------------------------------"
        echo "  Found existing token in .env: ${EXISTING_TOKEN:0:10}..."
        echo ""
        read -p "  Use this token? [Y/n] " USE_EXISTING
        if [ "$USE_EXISTING" != "n" ] && [ "$USE_EXISTING" != "N" ]; then
            TOKEN="$EXISTING_TOKEN"
        fi
    fi
fi

if [ -z "$TOKEN" ]; then
    echo "STEP 2: Add Bot Token"
    echo "------------------------------------------------------------"
    echo ""
    read -p "  Paste your bot token from BotFather: " TOKEN
    echo ""

    if [ -z "$TOKEN" ]; then
        echo "  ERROR: No token provided. Exiting."
        exit 1
    fi

    # Save to .env
    if [ -f "$ENV_FILE" ]; then
        # Remove existing entry if any
        if grep -q "TELEGRAM_BOT_TOKEN" "$ENV_FILE" 2>/dev/null; then
            # Replace existing line
            sed -i '' "s|^TELEGRAM_BOT_TOKEN=.*|TELEGRAM_BOT_TOKEN=$TOKEN|" "$ENV_FILE"
            echo "  Updated TELEGRAM_BOT_TOKEN in .env"
        else
            echo "" >> "$ENV_FILE"
            echo "# Telegram Bot" >> "$ENV_FILE"
            echo "TELEGRAM_BOT_TOKEN=$TOKEN" >> "$ENV_FILE"
            echo "  Added TELEGRAM_BOT_TOKEN to .env"
        fi
    else
        echo "# Telegram Bot" > "$ENV_FILE"
        echo "TELEGRAM_BOT_TOKEN=$TOKEN" >> "$ENV_FILE"
        echo "  Created .env with TELEGRAM_BOT_TOKEN"
    fi
    echo ""
fi

# Step 3: Test the token
echo "STEP 3: Testing Bot Token"
echo "------------------------------------------------------------"

RESPONSE=$(curl -s "https://api.telegram.org/bot${TOKEN}/getMe" 2>&1)

if echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if d.get('ok') else 1)" 2>/dev/null; then
    BOT_USERNAME=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['username'])" 2>/dev/null)
    BOT_NAME=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['first_name'])" 2>/dev/null)
    echo ""
    echo "  Token is VALID"
    echo "  Bot: @${BOT_USERNAME} (${BOT_NAME})"
    echo ""
else
    echo ""
    echo "  ERROR: Token is INVALID"
    echo "  Response: $RESPONSE"
    echo ""
    echo "  Please check your token and try again."
    exit 1
fi

# Step 4: Check Ollama
echo "STEP 4: Checking Ollama"
echo "------------------------------------------------------------"

if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    MODELS=$(curl -s http://localhost:11434/api/tags | python3 -c "
import sys, json
models = json.load(sys.stdin).get('models', [])
for m in models:
    size = m.get('size', 0) / (1024**3)
    print(f\"  - {m['name']} ({size:.1f} GB)\")
" 2>/dev/null)
    echo ""
    echo "  Ollama is RUNNING"
    echo "  Available models:"
    echo "$MODELS"
    echo ""
else
    echo ""
    echo "  WARNING: Ollama is not running."
    echo "  Start it with: ollama serve"
    echo "  The bot will report errors until Ollama is available."
    echo ""
fi

# Step 5: Start the bot
echo "============================================================"
echo "  READY TO START"
echo "============================================================"
echo ""
echo "  Bot:    @${BOT_USERNAME}"
echo "  Script: $BOT_SCRIPT"
echo ""
read -p "  Start the bot now? [Y/n] " START_NOW

if [ "$START_NOW" = "n" ] || [ "$START_NOW" = "N" ]; then
    echo ""
    echo "  To start manually:"
    echo "    python3 $BOT_SCRIPT"
    echo ""
    echo "  To run in background:"
    echo "    nohup python3 $BOT_SCRIPT > $PROJECT_ROOT/logs/telegram_bot.log 2>&1 &"
    echo ""
    exit 0
fi

echo ""
echo "Starting bot..."
echo ""

exec python3 "$BOT_SCRIPT"
