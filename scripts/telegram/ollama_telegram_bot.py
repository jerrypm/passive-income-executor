#!/usr/bin/env python3
"""
Ollama Telegram Bot
A Telegram bot that connects to a local Ollama instance for AI text generation.
Uses ONLY Python standard library — no pip install needed.

Features:
  /start  — Welcome message
  /ask    — Query Ollama (llama3 model)
  /models — List available Ollama models
  /help   — Show commands

Rate limiting: 10 requests per user per hour (free tier).

Usage:
    python3 ollama_telegram_bot.py
    python3 ollama_telegram_bot.py --model deepseek-r1
    python3 ollama_telegram_bot.py --limit 20
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from collections import defaultdict

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OLLAMA_URL = "http://localhost:11434"
POLL_TIMEOUT = 30  # long-polling timeout in seconds
MAX_RESPONSE_LENGTH = 4000  # Telegram message limit ~4096, leave margin
OLLAMA_TIMEOUT = 120  # seconds to wait for Ollama response
UPGRADE_LINK = "https://t.me/your_username"  # replace with your contact/payment link

# Mutable config — overridden by CLI args in main()
config = {
    "model": "llama3",
    "rate_limit": 10,  # requests per user per hour
}

# ---------------------------------------------------------------------------
# .env loader (same pattern as other project scripts)
# ---------------------------------------------------------------------------


def load_env():
    """Load .env file from project root."""
    env = {}
    env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
    env_path = os.path.abspath(env_path)
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
    return env


# ---------------------------------------------------------------------------
# Telegram Bot API helpers
# ---------------------------------------------------------------------------

class TelegramAPI:
    """Minimal Telegram Bot API client using urllib."""

    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.offset = 0

    def _request(self, method, data=None):
        """Make a request to the Telegram Bot API."""
        url = f"{self.base_url}/{method}"
        if data:
            payload = json.dumps(data).encode()
            req = urllib.request.Request(
                url, data=payload,
                headers={"Content-Type": "application/json"}
            )
        else:
            req = urllib.request.Request(url)

        try:
            with urllib.request.urlopen(req, timeout=POLL_TIMEOUT + 10) as resp:
                result = json.loads(resp.read())
                if not result.get("ok"):
                    log(f"API error: {result.get('description', 'Unknown error')}")
                    return None
                return result.get("result")
        except urllib.error.HTTPError as e:
            body = e.read().decode() if e.fp else ""
            log(f"HTTP {e.code} from Telegram API ({method}): {body}")
            return None
        except urllib.error.URLError as e:
            log(f"Connection error ({method}): {e.reason}")
            return None
        except Exception as e:
            log(f"Request error ({method}): {e}")
            return None

    def get_me(self):
        """Test bot token and get bot info."""
        return self._request("getMe")

    def get_updates(self):
        """Long-poll for new messages."""
        data = {
            "offset": self.offset,
            "timeout": POLL_TIMEOUT,
            "allowed_updates": ["message"]
        }
        updates = self._request("getUpdates", data)
        if updates:
            for update in updates:
                update_id = update.get("update_id", 0)
                if update_id >= self.offset:
                    self.offset = update_id + 1
        return updates or []

    def send_message(self, chat_id, text, parse_mode=None):
        """Send a text message."""
        data = {"chat_id": chat_id, "text": text}
        if parse_mode:
            data["parse_mode"] = parse_mode
        return self._request("sendMessage", data)

    def send_chat_action(self, chat_id, action="typing"):
        """Show typing indicator."""
        return self._request("sendChatAction", {
            "chat_id": chat_id,
            "action": action
        })


# ---------------------------------------------------------------------------
# Ollama API helpers
# ---------------------------------------------------------------------------

def ollama_generate(prompt, model=None):
    """Generate text using local Ollama instance."""
    if model is None:
        model = config["model"]
    url = f"{OLLAMA_URL}/api/generate"
    data = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False
    }).encode()

    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as resp:
            result = json.loads(resp.read())
            response_text = result.get("response", "").strip()
            total_duration = result.get("total_duration", 0)
            # Convert nanoseconds to seconds
            duration_sec = total_duration / 1_000_000_000 if total_duration else 0
            return response_text, duration_sec, None
    except urllib.error.URLError as e:
        return None, 0, f"Cannot connect to Ollama at {OLLAMA_URL}. Is it running?"
    except Exception as e:
        return None, 0, f"Ollama error: {e}"


def ollama_list_models():
    """List available models from Ollama."""
    url = f"{OLLAMA_URL}/api/tags"
    req = urllib.request.Request(url)

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            models = result.get("models", [])
            return models, None
    except urllib.error.URLError:
        return None, f"Cannot connect to Ollama at {OLLAMA_URL}. Is it running?"
    except Exception as e:
        return None, f"Error listing models: {e}"


# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------

class RateLimiter:
    """In-memory per-user rate limiter."""

    def __init__(self, max_requests=None, window_seconds=3600):
        if max_requests is None:
            max_requests = config["rate_limit"]
        self.max_requests = max_requests
        self.window = window_seconds
        self.tracker = defaultdict(list)

    def check(self, user_id):
        """Check if user is within rate limit. Returns (allowed, remaining)."""
        now = time.time()
        cutoff = now - self.window
        # Clean old entries
        self.tracker[user_id] = [t for t in self.tracker[user_id] if t > cutoff]
        count = len(self.tracker[user_id])
        if count >= self.max_requests:
            return False, 0
        return True, self.max_requests - count

    def record(self, user_id):
        """Record a request for the user."""
        self.tracker[user_id].append(time.time())

    def time_until_reset(self, user_id):
        """Seconds until the oldest request in the window expires."""
        if not self.tracker[user_id]:
            return 0
        oldest = min(self.tracker[user_id])
        remaining = (oldest + self.window) - time.time()
        return max(0, int(remaining))


# ---------------------------------------------------------------------------
# Bot command handlers
# ---------------------------------------------------------------------------

def handle_start(bot, chat_id, user_first_name):
    """Handle /start command."""
    text = (
        f"Hello {user_first_name}! I'm an AI assistant powered by Ollama running locally.\n\n"
        "I can answer questions, write code, explain concepts, and more — "
        "all processed on a private local server.\n\n"
        "Commands:\n"
        "  /ask <your question> — Ask me anything\n"
        "  /models — See available AI models\n"
        "  /help — Show all commands\n\n"
        f"Free tier: {config['rate_limit']} requests per hour.\n"
        "Try it: /ask What is the meaning of life?"
    )
    bot.send_message(chat_id, text)


def handle_help(bot, chat_id):
    """Handle /help command."""
    text = (
        "Available commands:\n\n"
        "/start — Welcome message\n"
        "/ask <prompt> — Ask the AI a question\n"
        "/models — List available AI models\n"
        "/help — Show this help message\n\n"
        "Examples:\n"
        "  /ask Explain quantum computing in simple terms\n"
        "  /ask Write a Python function to sort a list\n"
        "  /ask Translate 'hello world' to Japanese\n\n"
        f"Rate limit: {config['rate_limit']} requests per hour (free tier)."
    )
    bot.send_message(chat_id, text)


def handle_models(bot, chat_id):
    """Handle /models command."""
    models, err = ollama_list_models()
    if err:
        bot.send_message(chat_id, f"Error: {err}")
        return

    if not models:
        bot.send_message(chat_id, "No models found. Pull a model first: ollama pull llama3")
        return

    lines = ["Available models:\n"]
    for m in models:
        name = m.get("name", "unknown")
        size_bytes = m.get("size", 0)
        size_gb = size_bytes / (1024 ** 3)
        lines.append(f"  {name} ({size_gb:.1f} GB)")

    lines.append(f"\nDefault model: {config['model']}")
    bot.send_message(chat_id, "\n".join(lines))


def handle_ask(bot, chat_id, user_id, prompt, rate_limiter):
    """Handle /ask command with rate limiting."""
    if not prompt:
        bot.send_message(chat_id, "Please provide a question after /ask.\n\nExample: /ask What is Python?")
        return

    # Check rate limit
    allowed, remaining = rate_limiter.check(user_id)
    if not allowed:
        reset_mins = rate_limiter.time_until_reset(user_id) // 60
        bot.send_message(
            chat_id,
            f"You've reached the free limit ({config['rate_limit']} requests/hour).\n"
            f"Resets in ~{reset_mins} minutes.\n\n"
            f"Upgrade for unlimited access: {UPGRADE_LINK}"
        )
        return

    # Show typing indicator
    bot.send_chat_action(chat_id, "typing")

    # Query Ollama
    response, duration, err = ollama_generate(prompt)
    if err:
        bot.send_message(chat_id, f"Error: {err}")
        return

    if not response:
        bot.send_message(chat_id, "The model returned an empty response. Try rephrasing your question.")
        return

    # Record the request after successful generation
    rate_limiter.record(user_id)
    remaining -= 1

    # Truncate if response is too long
    if len(response) > MAX_RESPONSE_LENGTH:
        response = response[:MAX_RESPONSE_LENGTH] + "\n\n... (response truncated)"

    # Add footer
    footer = f"\n\n[{config['model']} | {duration:.1f}s | {remaining} requests left]"
    bot.send_message(chat_id, response + footer)


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log(message):
    """Print a timestamped log message."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main():
    # Parse CLI args
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--model" and i + 1 < len(args):
            config["model"] = args[i + 1]
            i += 2
        elif args[i] == "--limit" and i + 1 < len(args):
            config["rate_limit"] = int(args[i + 1])
            i += 2
        else:
            i += 1

    # Load environment
    env = load_env()
    token = env.get("TELEGRAM_BOT_TOKEN", os.environ.get("TELEGRAM_BOT_TOKEN", ""))

    if not token:
        print("=" * 60)
        print("ERROR: TELEGRAM_BOT_TOKEN not found")
        print()
        print("1. Talk to @BotFather on Telegram")
        print("2. Create a new bot with /newbot")
        print("3. Copy the token and add to .env:")
        print("   TELEGRAM_BOT_TOKEN=your_token_here")
        print("=" * 60)
        sys.exit(1)

    # Initialize bot
    bot = TelegramAPI(token)

    # Verify token
    me = bot.get_me()
    if not me:
        print("ERROR: Invalid bot token. Could not connect to Telegram API.")
        print("Check your TELEGRAM_BOT_TOKEN in .env")
        sys.exit(1)

    bot_username = me.get("username", "unknown")
    bot_name = me.get("first_name", "Bot")

    # Check Ollama connection
    models, err = ollama_list_models()
    ollama_status = "CONNECTED" if not err else f"NOT AVAILABLE ({err})"

    # Initialize rate limiter
    rate_limiter = RateLimiter(max_requests=config["rate_limit"])

    # Startup banner
    print("=" * 60)
    print("OLLAMA TELEGRAM BOT")
    print("=" * 60)
    print(f"Bot:      @{bot_username} ({bot_name})")
    print(f"Model:    {config['model']}")
    print(f"Ollama:   {ollama_status}")
    print(f"Limit:    {config['rate_limit']} requests/user/hour")
    print(f"Polling:  {POLL_TIMEOUT}s timeout")
    print()
    print(f"Send /start to @{bot_username} on Telegram to begin.")
    print("Press Ctrl+C to stop.")
    print("=" * 60)

    # Main polling loop
    consecutive_errors = 0
    max_consecutive_errors = 10

    while True:
        try:
            updates = bot.get_updates()
            consecutive_errors = 0  # reset on success

            for update in updates:
                message = update.get("message")
                if not message:
                    continue

                text = message.get("text", "").strip()
                chat_id = message["chat"]["id"]
                user = message.get("from", {})
                user_id = user.get("id", 0)
                user_name = user.get("first_name", "User")
                username = user.get("username", "")

                if not text:
                    continue

                # Log incoming message
                user_label = f"@{username}" if username else user_name
                log(f"[{user_label} ({user_id})] {text[:80]}")

                # Route commands
                if text.startswith("/start"):
                    handle_start(bot, chat_id, user_name)

                elif text.startswith("/help"):
                    handle_help(bot, chat_id)

                elif text.startswith("/models"):
                    handle_models(bot, chat_id)

                elif text.startswith("/ask"):
                    prompt = text[4:].strip()
                    # Also handle /ask@botname format
                    if prompt.startswith(f"@{bot_username}"):
                        prompt = prompt[len(f"@{bot_username}"):].strip()
                    handle_ask(bot, chat_id, user_id, prompt, rate_limiter)

                elif text.startswith("/"):
                    bot.send_message(
                        chat_id,
                        "Unknown command. Use /help to see available commands."
                    )

                else:
                    # Non-command messages: treat as /ask
                    handle_ask(bot, chat_id, user_id, text, rate_limiter)

        except KeyboardInterrupt:
            log("Bot stopped by user.")
            break

        except Exception as e:
            consecutive_errors += 1
            log(f"Error in main loop: {e}")

            if consecutive_errors >= max_consecutive_errors:
                log(f"Too many consecutive errors ({max_consecutive_errors}). Exiting.")
                sys.exit(1)

            # Back off on errors: wait longer with each consecutive error
            wait = min(consecutive_errors * 2, 30)
            log(f"Retrying in {wait}s... (error {consecutive_errors}/{max_consecutive_errors})")
            time.sleep(wait)


if __name__ == "__main__":
    main()
