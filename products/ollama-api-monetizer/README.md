# Ollama API Monetizer — Sell Your Local AI

**Price: $14**

Turn your local Ollama installation into a revenue-generating API service. This package gives you everything you need to serve AI inference over HTTP, integrate with the RapidAPI marketplace, and accept Lightning Network payments -- all from your terminal.

---

## What You Get

- **3 production-ready Python servers** for monetizing Ollama
- **HTTP API server** with rate limiting and optional Lightning paywall
- **RapidAPI-compatible wrapper** ready for marketplace listing
- **Lightning Address server** for receiving payments via LNURL-pay
- **Advanced setup guide** for L402 paywall with LND + Aperture

## Features

- **Zero external dependencies** — pure Python standard library only
- **Dual mode** — free (rate-limited) or paid (Lightning invoices via LNbits)
- **RapidAPI integration** — list your API on the world's largest API marketplace
- **OpenAI-compatible chat endpoint** — drop-in replacement for OpenAI API
- **Lightning Address server** — receive payments at `you@yourdomain.com`
- **CORS enabled** — works with frontend apps and browser-based clients
- **Privacy-first** — no data logging, no tracking, runs on your hardware
- **Rate limiting** — configurable per-IP rate limits for free tier
- **L402 paywall option** — advanced HTTP 402 payment protocol (guide included)

## Included Files

| File | Purpose |
|------|---------|
| `ollama_api_server.py` | Main HTTP API server with tip jar and optional LNbits paywall |
| `rapidapi_wrapper.py` | RapidAPI-compatible wrapper for marketplace listing |
| `lightning_address_server.py` | Self-hosted LNURL-pay Lightning address server |
| `ADVANCED_SETUP.md` | Guide for L402 paywall using LND + Aperture |

## Quick Start

### 1. Install Ollama and pull a model

```bash
# Install: https://ollama.com
ollama pull llama3
```

### 2. Start the API server

```bash
python3 ollama_api_server.py --free
```

Your API is now live at `http://localhost:8080`.

### 3. Test it

```bash
# List models
curl http://localhost:8080/models

# Generate text
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a haiku about coding"}'

# Chat completion
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello!"}]}'
```

## Monetization Options

### Option A: RapidAPI Marketplace (Easiest)

1. Start the RapidAPI wrapper:
   ```bash
   python3 rapidapi_wrapper.py
   ```

2. Expose with a public URL (ngrok, Cloudflare Tunnel, etc.):
   ```bash
   ngrok http 8082
   ```

3. Create a RapidAPI provider account at https://rapidapi.com/provider/dashboard

4. Add your API with the public URL as the base URL

5. Define pricing plans (free tier + paid tiers)

### Option B: Lightning Payments (LNbits)

1. Install and run LNbits:
   ```bash
   pip install lnbits
   lnbits  # runs on port 5000
   ```

2. Create a `.env` file:
   ```env
   LNBITS_URL=http://localhost:5000
   LNBITS_API_KEY=your_invoice_key_here
   ```

3. Start the server without `--free`:
   ```bash
   python3 ollama_api_server.py
   ```

   Clients will receive a Lightning invoice (10 sats) before accessing the API.

### Option C: Lightning Address (Custom Domain)

1. Point a domain to your server
2. Configure and start:
   ```bash
   DOMAIN=yourdomain.com python3 lightning_address_server.py
   ```
3. Receive payments at `you@yourdomain.com`

### Option D: L402 Paywall (Advanced)

See `ADVANCED_SETUP.md` for setting up Aperture + LND for HTTP 402 payment protocol.

## Configuration

Create a `.env` file in the same directory:

```env
# Ollama (default: http://localhost:11434)
OLLAMA_URL=http://localhost:11434

# API Server
API_PORT=8080

# LNbits (optional, for paid mode)
LNBITS_URL=http://localhost:5000
LNBITS_API_KEY=your_invoice_key_here

# RapidAPI (optional)
RAPIDAPI_PORT=8082
RAPIDAPI_SECRET=your_proxy_secret_here

# Lightning Address Server (optional)
DOMAIN=yourdomain.com
LN_ADDR_PORT=8090
LN_USERNAME=yourname
LNBITS_API_KEY=your_invoice_key_here
```

## API Endpoints

### Main Server (port 8080)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info and status |
| GET | `/models` | List available Ollama models |
| POST | `/generate` | Text generation (body: `{"prompt": "...", "model": "llama3"}`) |
| POST | `/chat` | Chat completion (body: `{"messages": [...], "model": "llama3"}`) |

### RapidAPI Wrapper (port 8082)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/health` | Health check |
| GET | `/v1/models` | List models (OpenAI format) |
| POST | `/v1/generate` | Text generation |
| POST | `/v1/chat` | Chat completion (OpenAI-compatible) |

## Requirements

- **Python 3.8+** (no pip packages needed for core functionality)
- **Ollama** (free, local AI) — https://ollama.com
- **LNbits** (optional, for Lightning payments) — https://lnbits.com
- **Public URL** (optional, for RapidAPI — use ngrok, Cloudflare Tunnel, etc.)

## Revenue Potential

| Channel | Pricing | Est. Monthly |
|---------|---------|-------------|
| RapidAPI free tier | Free (50 req/mo) | $0 (lead gen) |
| RapidAPI Pro | $5/mo (500 req) | $5-50 |
| RapidAPI Ultra | $15/mo (2000 req) | $15-150 |
| Lightning tips | Voluntary | $1-20 |
| Lightning paywall | 10 sats/req | $5-100 |

## FAQ

**Do I need a GPU?**
No. Ollama runs on CPU too (slower but works). Apple Silicon Macs run it well.

**Can I add more models?**
Yes. Run `ollama pull <model>` and the API automatically serves them.

**Is this production-ready?**
For personal/small-scale use, yes. For high-traffic, consider adding a reverse proxy (nginx/caddy) in front.

---

Your hardware, your models, your revenue. No middleman.
