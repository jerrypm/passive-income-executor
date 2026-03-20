# I Built 12 Passive Income Streams Using Only My Terminal — Here's What Actually Earns Money

I spent the last few weeks setting up passive income streams entirely from the command line. No web dashboards, no drag-and-drop builders, no corporate platforms begging for KYC docs. Just a Mac Mini, a terminal, and open source tools.

Some of these streams earn sats. Most of them earn nothing yet. Here's an honest breakdown of what I built, what works, and what's still aspirational.

## The Stack

Everything runs on a Mac Mini. The core tools:

- **Ollama** — local AI inference (llama3, deepseek-r1, codellama)
- **nak** — Nostr CLI by fiatjaf
- **LNbits** — self-hosted Lightning wallet
- **Python + Bash** — glue for everything
- **cron** — the OG automation

No cloud. No subscriptions. No third-party API keys for the core income streams.

## Stream 1: Nostr AI DVM (Data Vending Machine)

This is the one I'm most excited about. NIP-90 defines a protocol where anyone on Nostr can request compute work, and "Data Vending Machines" fulfill those requests.

I wrote a Python script that listens for kind 5050 events (text generation requests), routes them to Ollama running locally, and publishes the result as kind 6050. Pure peer-to-peer AI inference on a decentralized protocol.

```bash
# The DVM listens on Nostr relays for AI requests
python3 scripts/nostr/dvm_text_generation.py
```

The DVM subscribes to relays, watches for requests, sends a "processing" status (kind 7000), queries Ollama, and returns the result. All signed with my Nostr key.

**Earnings so far:** 0 sats. The NIP-90 ecosystem is early. Very few clients send DVM requests yet. But the protocol is sound, and when adoption grows, the infrastructure is ready. I'm betting on Nostr's DVM ecosystem the same way people bet on Lightning in 2018.

## Stream 2: Ollama API with Lightning Paywall

I wrapped Ollama in an HTTP API server with LNbits integration. Hit `/generate`, get a 402 response with a Lightning invoice. Pay 10 sats, get your AI response. No accounts, no API keys, no KYC.

```bash
python3 scripts/ai-inference/ollama_api_server.py --port 8080
```

The server creates invoices via self-hosted LNbits, checks payment status, then proxies to Ollama. Currently running in free mode with rate limiting (10 req/hour per IP) because getting inbound Lightning liquidity as a solo operator is the real bottleneck.

**Earnings so far:** 0 sats in paid mode. A handful of test requests in free mode. The L402 standard (formerly LSATS) from Lightning Labs is the right long-term approach here — Aperture as a reverse proxy handles auth at the protocol level.

## Stream 3: Nostr Content + Zaps

Three automated posts per day via cron:

```bash
# crontab
15 6  * * * /path/to/daily_post.sh       # gm post
0  12 * * * python3 auto_content.py       # AI-generated content
0  18 * * * python3 auto_content.py       # evening post
```

The `auto_content.py` script uses Ollama to generate posts about Bitcoin, Lightning, self-hosting, and dev topics, then signs and publishes them to Nostr relays using pure Python (BIP-340 Schnorr signatures, raw WebSocket — zero external dependencies).

I also published a long-form article via NIP-23 that shows up on habla.news.

**Earnings so far:** A few zaps here and there. The honest truth is that automated content doesn't get zapped much. Original, thoughtful content does. The automation keeps the profile active, but the real zap money comes from genuine posts. I'm treating the auto-posts as a presence-keeper, not a revenue generator.

## Stream 4: Digital Products on Shopstr

Shopstr is a Nostr-native marketplace (NIP-15). I listed three products:

1. AI API access (100 requests) — 1,000 sats
2. Terminal passive income setup guide — 5,000 sats
3. Custom AI bot setup for your Nostr profile — 10,000 sats

```python
# NIP-15 product listing (kind 30017)
tags = [
    ["d", "ai-api-access"],
    ["title", "AI Text Generation API Access"],
    ["price", "1000", "sat"],
    ["type", "digital"],
]
```

**Earnings so far:** 0 sats. Shopstr has low traffic. But listing products is free and takes 5 minutes, so the opportunity cost is near zero.

## Stream 5: Self-Hosted Lightning Address

Instead of relying on custodial services, I built a simple LNURL-pay server (LUD-06/LUD-16). Point a domain at it, and you get `you@yourdomain.com` as a Lightning address backed by your own LNbits instance.

```bash
DOMAIN=yourdomain.com python3 lightning_address_server.py
```

It handles the `.well-known/lnurlp/` endpoint and creates invoices via LNbits. Full sovereignty over your payment rails.

**Earnings so far:** This is infrastructure, not a direct earner. But it connects to everything else — zaps, DVM payments, product sales all flow through your own stack.

## Stream 6: Bandwidth Sharing (The "Normie" Stream)

This is the one stream that actually earns something predictable. Docker containers that share unused bandwidth:

```bash
docker compose up -d  # money4band stack
```

Honeygain is running. Earnings are tiny (~$0.10-0.30/day) but consistent. Not very cypherpunk, I know. It requires registration and KYC for payout. I include it for completeness, but it's philosophically the weakest stream here.

**Earnings so far:** ~$3-5/month. Real money, but not Bitcoin, and not sovereign.

## What I Learned

**What actually works right now:**
- Bandwidth sharing earns small but consistent fiat
- Nostr presence-building works if you combine automated + genuine posts
- The tooling for Lightning-gated APIs exists and is functional

**What doesn't work yet (but will):**
- NIP-90 DVMs are too early — clients need to catch up
- Selling digital products on Nostr needs more marketplace traffic
- Lightning API paywalls need inbound liquidity and discoverability

**What surprised me:**
- How mature the Nostr dev tooling has become. nak CLI is excellent.
- How little code you need. My entire DVM is ~350 lines of pure Python, zero dependencies.
- BIP-340 Schnorr signatures are elegant. Implementing them from scratch was a great exercise.
- LNbits is incredibly powerful for a self-hosted tool.

## The Uncomfortable Truth

Most of these streams earn nothing today. The Bitcoin/Lightning/Nostr ecosystem for machine-to-machine payments is early. Really early.

But here's why I keep building: every one of these streams is **permissionless**. No platform can deplatform me. No company can change their ToS and kill my revenue. No KYC process stands between me and getting paid. The value of sovereignty is that it compounds — slowly, then all at once.

The total setup cost was $0 (I already had the Mac Mini). Time investment was about a weekend of focused work. Everything is open source.

## All the Tools (For the Builders)

| Tool | What it does |
|------|-------------|
| [Ollama](https://ollama.com) | Local AI inference |
| [nak](https://github.com/fiatjaf/nak) | Nostr CLI |
| [LNbits](https://github.com/lnbits/lnbits) | Self-hosted Lightning wallet |
| [Aperture](https://github.com/lightninglabs/aperture) | L402 reverse proxy paywall |
| [nostream](https://github.com/cameri/nostream) | Paid Nostr relay |
| [Shopstr](https://shopstr.store) | Nostr marketplace |
| [Ligess](https://github.com/Dolu89/ligess) | Self-hosted Lightning address |

Everything runs from the terminal. No web GUIs required (though LNbits has a nice one if you want it).

---

**Question for the stackers:** Has anyone here actually earned meaningful sats from Nostr zaps or NIP-90 DVMs? I'm curious whether the "build it and they will come" thesis holds for Nostr-native monetization, or if the network effects just aren't there yet. What's your experience?
