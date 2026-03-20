# I Built 12 Passive Income Streams from My Terminal in 48 Hours

*Issue #1 — Building Passive Income from Terminal*

---

Hey, I'm a developer from Indonesia. iOS apps, web stuff, the usual.

Last week I asked myself a dumb question: **How many passive income streams can I set up using only my terminal?** No signup forms. No KYC. No credit cards. Just a Mac Mini, a terminal window, and stubbornness.

48 hours later, I had 12 streams running. Some are earning sats already. Some are simmering. All of them were set up without ever opening a browser to fill out a registration form.

Here's the full breakdown.

---

## The Setup

My weapon of choice:

- **Mac Mini** (M-series, 8GB RAM — nothing fancy)
- **Ollama** — run AI models locally, completely free
- **Python, Node.js, Go** — the holy trinity
- **Docker** — for the heavier services
- **Claude Code** — AI pair programmer in the terminal

Total cost to start: **$0**

The only "investment" was the Mac I already owned and electricity.

---

## What I Built (All 12 Streams)

### 1. Nostr AI DVM (Data Vending Machine)

This is probably the most interesting one. Nostr has this protocol called NIP-90 where you can offer "data vending" services on the decentralized network. Think of it like a Fiverr gig, but no platform, no fees, no account.

I wrote a Python script that listens for `kind 5050` events (text generation requests), processes them through my local Ollama instance running Llama 3, and returns results. Payment comes through Lightning Network.

```bash
# That's literally the whole stack
ollama serve &
python3 scripts/nostr/dvm_text_generation.py
```

**Potential**: $30-50/month once you get regular users

### 2. Self-Hosted Ollama API with Lightning Paywall

I wrapped Ollama in a simple HTTP server with a tip jar model — free to use, but with a Lightning address for tips. Developers who want a private, cheap alternative to OpenAI hit my endpoint instead.

It runs on port 8080. No API keys to manage, no OAuth flows. Just HTTP requests and sats.

**Potential**: $10-100/month depending on traffic

### 3. RapidAPI Marketplace Listing

Took that same Ollama API and listed it on RapidAPI as "Ollama AI Text Generation." Four pricing tiers from free (50 requests) to $30/month (5000 requests). This one required a signup, but it's a distribution channel worth having.

**Potential**: $50-200/month with good SEO on the marketplace

### 4. Bandwidth Sharing (Honeygain + More)

One Docker command:

```bash
docker compose up -d
```

[Honeygain](https://join.honeygain.com/JERRYF5C2E) is now sharing my idle bandwidth in the background. It's not life-changing money, but it's literally zero effort after setup. If you want to try it yourself, you can [sign up through my referral link](https://join.honeygain.com/JERRYF5C2E) — you get a $5 starting bonus and I get a small kickback. Win-win.

**Potential**: $5-30/month (depends on location and bandwidth)

### 5. Auto-Publishing Content Bot

I have a cron job that runs 3 times a day. It uses Ollama to generate a developer-focused post, then publishes it to Nostr automatically. The content ranges from coding tips to AI insights to building-in-public updates.

```cron
15 6  * * * /path/to/daily_post.sh
0  12 * * * python3 auto_content.py
0  18 * * * python3 auto_content.py
```

This builds audience on Nostr, which feeds into everything else.

**Potential**: Audience growth → indirect revenue from all other streams

### 6. Digital Products on Shopstr

Shopstr is a decentralized marketplace built on Nostr. I listed three digital products:

- AI API access pass — 1,000 sats
- "Monetize Local AI" guide — 5,000 sats
- Custom AI bot setup — 10,000 sats

No listing fees. No platform cut. Just publish a NIP-15 event and your product is live.

**Potential**: $10-50/month

### 7. Long-Form Content on Habla.news

Habla is like Medium, but on Nostr. I published my first long-form article about monetizing local AI inference. It lives on the Nostr network forever — no platform risk, no algorithm changes.

Every article is a NIP-23 event posted from my terminal:

```bash
python3 publish_longform.py --title "How to Monetize Local AI" --file article.md
```

**Potential**: Reputation + zaps (Lightning tips) — $5-20/month

### 8. LNbits (Self-Hosted Lightning Wallet)

This is infrastructure, not a direct income stream. But it powers everything else. I'm running LNbits locally as the payment backend for my API paywall, my DVM, and my Lightning address.

```bash
cd lnbits && python3 -m uvicorn lnbits.__main__:app --port 5001
```

### 9. Solana Staking Setup

Got the Solana CLI installed and ready. Once I have SOL to stake, it's one command:

```bash
solana delegate-stake stake-account validator-address
```

At current rates, $1,000 in SOL earns about $5-7/month. Not sexy, but it compounds.

**Potential**: $5-7/month per $1K staked

### 10. Cosmos/ATOM Staking Setup

Same deal as Solana. Got `gaiad` installed, wallet created. Waiting for capital.

**Potential**: $8-15/month per $1K staked

### 11. Lightning Address for Zaps

Set up a Lightning address so people can zap (tip) me on Nostr. Every post, every DVM response, every piece of content — all linked to my Lightning address. It's like having a tip jar on everything I do.

**Potential**: $5-30/month (grows with audience)

### 12. Content Cross-Publishing Pipeline

Built a script that takes one article and publishes it everywhere — Nostr, dev.to, Hashnode. Write once, distribute everywhere. When I add API keys for the platforms, it's one command:

```bash
python3 publish_all.py --title "Title" --file article.md --tags ai,python
```

**Potential**: Affiliate links in content → $50-200/month at scale

---

## The Numbers (Realistic)

Let me be honest. I'm not making $2,000/month yet. Here's what the math looks like:

### Without Any Capital (Month 1-6)
| Stream | Monthly Estimate |
|--------|-----------------|
| Nostr DVM + content | ~$30-50 |
| AI inference paywall | ~$10-100 |
| Bandwidth sharing | ~$5-30 |
| Digital products | ~$10-50 |
| Zaps & tips | ~$5-30 |
| **Total** | **$60-260** |

### With $1K-5K in Crypto (Month 1-6)
| Stream | Monthly Estimate |
|--------|-----------------|
| All zero-capital streams | ~$60-260 |
| Staking (SOL + ATOM) | ~$40-50 |
| **Total** | **$100-310** |

### Full Stack with Platforms (Month 6+)
| Stream | Monthly Estimate |
|--------|-----------------|
| All above | ~$100-310 |
| Content + affiliate | ~$200 |
| API marketplace | ~$200-450 |
| **Total** | **$500-960** |

These aren't "passive income guru" numbers. These are real, conservative estimates. Some months will be $50. Some will surprise you. The point is: **the marginal cost of adding each new stream is near zero** because they all share the same infrastructure.

---

## What Surprised Me

**The zero-registration streams are actually the most interesting.**

I expected the platform-based stuff (RapidAPI, dev.to) to be the real moneymakers. And they might be eventually. But the Nostr ecosystem blew my mind.

Here's why:

1. **No platform risk.** Nobody can ban your account or change the algorithm.
2. **Instant payments.** Lightning settles in milliseconds. No 30-day payment terms.
3. **Composability.** My DVM, my content, my products, my Lightning address — they all reinforce each other on the same protocol.
4. **Terminal-native.** Everything is CLI tools and scripts. No web dashboards, no point-and-click.

The downside? The Nostr ecosystem is still small. But it's growing fast, and being early means you get noticed.

---

## The Stack at a Glance

```
Mac Mini (always-on)
├── Ollama (4 models: llama3, llama3.2, codellama, deepseek-r1)
├── Nostr DVM (listening for AI requests 24/7)
├── API Server (port 8080, free with tip jar)
├── LNbits (port 5001, Lightning wallet)
├── Honeygain (Docker, bandwidth sharing)
├── Cron jobs (3 posts/day to Nostr)
└── Scripts (content pipeline, staking helpers, marketplace)
```

Total RAM usage: ~4GB when idle, ~8GB when processing AI requests. My Mac Mini barely breaks a sweat.

---

## What's Next

This week I'm focused on:

- Getting my first real Lightning payment through the DVM
- Adding more bandwidth-sharing services (PacketStream, Repocket) — if you want to start with [Honeygain](https://join.honeygain.com/JERRYF5C2E), it's the easiest one
- Writing more long-form content to build the Nostr audience
- Setting up a paid Nostr relay (charge other users to store their events)

---

## Follow Along

This is Issue #1 of "Building Passive Income from Terminal." Every week I'll share:

- **Actual earnings** from each stream (transparent, no BS)
- **New streams** I add to the stack
- **Technical breakdowns** of what works and what doesn't
- **Scripts and configs** you can copy

If you're a developer who's tired of "start a dropshipping store" advice and want to build income streams using skills you already have — this is for you.

Subscribe to get the next issue. I'll show you exactly how much each stream earned in Week 1.

---

*All the code is open. All the tools are free. The only cost is your time and a computer that's already sitting on your desk.*

*— Built entirely from the terminal. No registration, no platforms, no middlemen.*
