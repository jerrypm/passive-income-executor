# Actionable Deep Dive: AI Inference + Nostr Monetization (Part 4)

> **Tanggal:** 2026-03-13
> **Konteks:** Deep dive ke 2 area paling promising dari Part 3 — monetisasi AI lokal & Nostr ecosystem
> **Prinsip:** 100% dari terminal, zero registration, self-custodial
> **Focus:** Tool-tool SPESIFIK yang sudah ada, siap pakai

---

## SECTION A: Monetisasi AI Inference Lokal

### Kenapa Ini Paling Promising?

- AI inference market: ~$106B (2025) → $255B (2030)
- Per-kWh revenue: AI hosting $0.25-0.35 vs crypto mining $0.07-0.09 → **3-10x lebih menguntungkan**
- Margin 40-50% gross profit
- Demand REAL: privacy, uncensored models, cheap alternative to OpenAI
- Kamu sudah punya Mac dengan chip Apple Silicon = inference cepat

---

### Tool #1: Aperture (L402 Protocol) — THE BEST OPTION ⭐

**Apa ini?** Reverse proxy dari Lightning Labs yang wrap API apapun (termasuk Ollama) di balik Lightning paywall. Pakai HTTP 402 "Payment Required".

**Flow:**
```
Client request → Aperture (402 + Lightning invoice) → Client bayar → Macaroon token → Forward ke Ollama → Response
```

```bash
# 1. Install (butuh Go 1.19+)
brew install go
git clone https://github.com/lightninglabs/aperture.git
cd aperture
make install

# 2. Config aperture.yaml
cat > aperture.yaml << 'EOF'
listenaddr: "localhost:8080"
services:
  - name: "ollama-inference"
    hostregexp: "localhost"
    pathregexp: "/api/.*"
    address: "localhost:11434"  # Ollama backend
    protocol: "http"
    price: 100  # sats per request
EOF

# 3. Jalankan (butuh LND node running)
aperture --configfile=aperture.yaml
```

**Pricing:** Set per-request fee dalam satoshis. 100 sats = ~$0.07.
**Repo:** https://github.com/lightninglabs/aperture
**Docs:** https://docs.lightning.engineering/the-lightning-network/l402

---

### Tool #2: x402 Protocol (Coinbase) — Stablecoin Alternative

**Apa ini?** Protocol baru dari Coinbase — HTTP 402 tapi bayar pakai USDC (stablecoin). Ada **ready-made n8n workflow** yang langsung combine Ollama + x402.

**Keuntungan vs Lightning:**
- USDC = stablecoin, tidak volatil
- Lebih familiar untuk non-crypto users
- Ready-made workflow template

```bash
# Option A: Via n8n workflow (easiest)
# Template: https://n8n.io/workflows/6597-monetize-your-private-llm-models-with-x402-and-ollama/

# Option B: Manual setup
git clone https://github.com/coinbase/x402.git
cd x402
npm install

# Wrap Ollama endpoint:
# Client hits webhook → x402 checks USDC payment → forwards to Ollama → returns response
```

**Pricing configurable:** $0.01 per 1K tokens, $0.10 per image, etc.
**Repo:** https://github.com/coinbase/x402
**Awesome list:** https://github.com/xpaysh/awesome-x402

---

### Tool #3: LNbits + Paywall Extension

**Apa ini?** Self-hosted Lightning wallet dengan extension system. Paywall extension bisa gating content/API di balik Lightning payment.

```bash
# 1. Install LNbits
git clone https://github.com/lnbits/lnbits.git
cd lnbits
python3 -m venv venv && source venv/bin/activate
pip install -e .
lnbits  # runs on port 5000

# 2. Enable Paywall extension dari web UI

# 3. Python middleware: LNbits + Ollama
```

```python
# pay_per_query.py — Middleware LNbits + Ollama
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

LNBITS_URL = "http://localhost:5000"
LNBITS_API_KEY = "your-invoice-read-key"
OLLAMA_URL = "http://localhost:11434"

@app.route("/api/chat", methods=["POST"])
def chat():
    # Step 1: Create Lightning invoice
    inv = requests.post(f"{LNBITS_URL}/api/v1/payments",
        headers={"X-Api-Key": LNBITS_API_KEY},
        json={"out": False, "amount": 50, "memo": "AI query"})
    invoice_data = inv.json()

    # Step 2: Return invoice to client
    # Client pays, then calls back with payment_hash
    return jsonify({
        "payment_request": invoice_data["payment_request"],
        "payment_hash": invoice_data["payment_hash"],
        "message": "Pay this invoice, then POST to /api/chat/complete"
    })

@app.route("/api/chat/complete", methods=["POST"])
def chat_complete():
    payment_hash = request.json["payment_hash"]
    prompt = request.json["prompt"]

    # Step 3: Verify payment
    check = requests.get(f"{LNBITS_URL}/api/v1/payments/{payment_hash}",
        headers={"X-Api-Key": LNBITS_API_KEY})
    if not check.json().get("paid"):
        return jsonify({"error": "Not paid"}), 402

    # Step 4: Forward to Ollama
    response = requests.post(f"{OLLAMA_URL}/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False})
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(port=8080)
```

**Repo:** https://github.com/lnbits/lnbits
**Paywall ext:** https://github.com/lnbits/paywall

---

### Tool #4: ln-paywall (Go Middleware)

```go
// Minimal Go middleware — any route behind this requires Lightning payment
import "github.com/philippgille/ln-paywall"

// First request → 402 + bolt11 invoice in response body
// Second request with X-Preimage header → verified → forwarded to Ollama
```

**Repo:** https://github.com/philippgille/ln-paywall

---

### Tool #5: Boltwall (Node.js/Express Middleware)

```bash
npm install boltwall express cors body-parser
```

```javascript
const express = require('express');
const { boltwall } = require('boltwall');
const app = express();

app.use(require('cors')());
app.use(require('body-parser').json());

// Everything AFTER boltwall() requires Lightning payment
app.use(boltwall());

app.post('/api/chat', async (req, res) => {
  // Paywalled — only accessible after Lightning payment
  const response = await fetch('http://localhost:11434/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req.body)
  });
  res.json(await response.json());
});

app.listen(8080, () => console.log('Paywalled Ollama API on :8080'));
```

**Repo:** https://github.com/Tierion/boltwall

---

### Tool #6: OpenAgents — GPU Marketplace (Passive)

**Apa ini?** Marketplace di mana kamu contribute GPU → dapat job AI inference → earn Bitcoin otomatis.

```bash
# Download worker software dari openagents.com
# Connect ke marketplace → get inference jobs → earn sats
```

**Target earnings:** ~$500/bulan per GPU.
**Payment:** Alby Lightning wallet.
**Site:** https://openagents.com

---

### Siapa Yang Bayar? (Realistic Demand)

| Niche | Willingness to Pay | Kenapa |
|-------|-------------------|--------|
| **Healthcare/Medical** | SANGAT TINGGI | HIPAA — data pasien tidak boleh ke OpenAI |
| **Legal** | TINGGI | Attorney-client privilege |
| **Finance** | TINGGI | Proprietary trading strategies |
| **AI Agents (M2M)** | GROWING FAST | Agent butuh fast micropayments |
| **Uncensored models** | MEDIUM | Creative writing, research |
| **Indie developers** | MEDIUM | Cheaper than OpenAI, no API key hassle |

---

### Revenue Comparison

| Method | Effort | Monthly Revenue |
|--------|--------|----------------|
| OpenAgents (sell GPU) | Low | $80-500 |
| Aperture + Ollama API | High | $100-1,000 |
| x402 + Ollama (n8n) | Medium | $50-500 |
| LNbits paywall | Low | $10-100 |
| Nostr DVM (see Section B) | Medium | $30-300 |

---

## SECTION B: Nostr Earning Ecosystem

### Kenapa Nostr?

- **ZERO registration** — generate keypair lokal, done
- **ZERO platform fees** — zaps langsung ke wallet kamu
- **ZERO deplatforming risk** — decentralized protocol
- **900M+ potential users** (Nostr + Lightning adoption growing)
- 5 juta+ zaps sudah terjadi
- Average zap = 462 sats (~$0.51) — **128x lebih dari Spotify stream**

---

### Stream B1: Nostr Data Vending Machines (NIP-90) ⭐ HIDDEN GEM

**Apa ini?** Decentralized marketplace untuk compute. User post "job request" → DVM kamu proses → user bayar Lightning → kamu deliver result. Seperti **serverless AWS Lambda tapi di Nostr**.

**DVM Kinds (task types):**
| Kind | Task |
|------|------|
| 5000 | Text extraction |
| 5001 | Summarization |
| 5050 | Text generation (LLM) ← **kita pakai ini** |
| 5100 | Image generation |
| 5250 | Translation |
| 5300 | Content discovery/feeds |

#### Setup DVM dengan nostrdvm (Python)

```bash
# 1. Install
python3 -m venv venv && source venv/bin/activate
pip install nostr-dvm

# 2. Clone untuk examples
git clone https://github.com/believethehype/nostrdvm
cd nostrdvm
cp .env_example .env

# 3. Edit .env:
# - NOSTR_PRIVATE_KEY=<your nsec>
# - LNBITS_URL=http://localhost:5000
# - LNBITS_API_KEY=<your key>

# 4. Run
python3 main.py
```

**Repo:** https://github.com/believethehype/nostrdvm

#### Setup DVM dengan ezdvm (Simpler)

```bash
pip install ezdvm
```

```python
# my_ai_dvm.py
from ezdvm import DVM
import requests

class OllamaDVM(DVM):
    kind = 5050  # text generation

    def do_work(self, event):
        # Call Ollama lokal
        r = requests.post("http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": event.content, "stream": False})
        return r.json()["response"]

dvm = OllamaDVM()
dvm.add_relay("wss://relay.damus.io")
dvm.add_relay("wss://nos.lol")
dvm.start()
```

**Repo:** https://github.com/dtdannen/ezdvm

#### DVMCP — Bridge MCP ke Nostr DVM

**Apa ini?** Bridge antara MCP (Model Context Protocol) dan Nostr DVM. Artinya MCP tools kamu bisa diakses via Nostr.

```bash
npx dvmcp
# Interactive CLI — setup MCP server as Nostr DVM
```

**Repo:** https://github.com/gzuuus/dvmcp

#### getAlby MCP — Lightning Wallet untuk LLM

```bash
npm install @getalby/mcp
# Set NWC_CONNECTION_STRING env var
# LLM agent bisa create/pay invoices natively
```

**Repo:** https://github.com/getAlby/mcp

**DVM Earnings:**
- Charge 50-500 sats per text gen (~$0.03-$0.35)
- Image gen: 500-2000 sats
- Realistic: **$2-25/bulan** (early stage, growing)

---

### Stream B2: Nostr Marketplace (NIP-15) — Jual Digital Products

**Apa ini?** Full e-commerce protocol di Nostr. Jual apapun, terima Lightning, tanpa platform.

#### Shopstr — Marketplace utama

- Global, permissionless marketplace
- Lightning + Cashu payments
- Fully anonymous transactions
- **Site:** https://shopstr.store
- **Repo:** https://github.com/shopstr-eng/shopstr

#### LNbits Nostr Market — Self-hosted shop

```bash
# Di LNbits, enable Nostr Market extension
# Full NIP-15 implementation
# Buat stall → tambah products → publish ke relay
```

**Repo:** https://github.com/lnbits/nostrmarket

#### SatShoot — Freelance marketplace

- Post jobs, bid, get paid in sats
- Reviews & reputation system
- **Repo:** https://github.com/Pleb5/satshoot

#### NostrTask — Micro-task bounties

- Post task → AI verifies completion → earn sats
- **Site:** https://nostrtask.com

#### Apa yang bisa dijual di Nostr?

| Product | Harga (sats) | ~USD |
|---------|-------------|------|
| AI Prompt packs | 5,000-20,000 | $3-14 |
| Code templates/boilerplate | 10,000-50,000 | $7-35 |
| Obsidian vault templates | 5,000-15,000 | $3-10 |
| SwiftUI components | 10,000-30,000 | $7-21 |
| Web scraper scripts | 5,000-25,000 | $3-17 |
| Ebook/guides | 10,000-100,000 | $7-70 |

---

### Stream B3: Nostr Content + Zaps (NIP-23 Long-form)

**Apa ini?** Publish artikel (NIP-23, kind 30023) → readers zap kamu Lightning tips.

#### Publishing platforms:
- **Habla** (habla.news) — Medium-like, NIP-23 client
- **YakiHonne** (yakihonne.com) — Content incentive rounds (up to 100,000 sats per top post)
- **Blogstack** (blogstack.io) — Blogging on Nostr

#### Zap earnings data:
| Metric | Value |
|--------|-------|
| Average zap | 462 sats (~$0.51) |
| Viral article | 50,000+ sats ($10+) |
| vs Spotify stream | **128x lebih besar** |
| Total zaps (2025) | 5 juta+ |
| YakiHonne incentive | Up to 100,000 sats/round |

---

### Stream B4: Paid Nostr Relay

**Reality check:** 95% relay operators tidak bisa cover operational costs. Tapi paid relay model sedang berkembang.

#### nostream — Best untuk paid relay

```bash
# 1. VPS Linux (8GB RAM recommended, ~$10-20/bulan)

# 2. Clone & start
git clone https://github.com/cameri/nostream.git
cd nostream
./scripts/start

# 3. Edit settings.yaml untuk paid access:
# payments:
#   enabled: true
#   feeSchedules:
#     admission:
#       enabled: true
#       amount: 50000  # sats (~$35) one-time

# 4. Payment processors: zebedee, nodeless, opennode, lnbits, lnurl
```

**Earnings:** Top relay ~150,000 sats total. filter.nostr.wine charges 10,000 sats/bulan.
**Realistic:** 50-200 users × one-time fee = cover VPS costs.

**Relay software options:**
| Software | Language | Paid Support | Notes |
|----------|----------|-------------|-------|
| **nostream** | TypeScript | Built-in Lightning | Best untuk paid relay |
| **strfry** | C++ | Via plugins | Fastest, lowest resources |
| **nostr-rs-relay** | Rust | Via auth | Good middle ground |
| **nerostr** | - | Monero payments | Privacy-focused |

---

### Stream B5: Bot Automation dari CLI

#### nak — CLI tool paling lengkap

```bash
# Install
go install github.com/fiatjaf/nak@latest

# Generate keys
nak key generate
nak key public <hex-secret-key>

# Post note
nak event --sec <your-key> -c 'Hello Nostr!' wss://nos.lol wss://relay.damus.io

# Post with tags
nak event --sec <key> -c 'Check out #bitcoin' --tag t=bitcoin wss://nos.lol

# Query events
nak req -k 1 --limit 10 wss://nos.lol
```

**Repo:** https://github.com/fiatjaf/nak

#### Cron automation — Daily post bot

```bash
# Crontab: post setiap hari jam 6:15 AM
crontab -e

# Tambahkan:
15 6 * * * /usr/local/bin/nak event --sec <your-hex-key> -c 'gm ☀️' wss://nos.lol wss://relay.damus.io
```

#### Automated content bot

```bash
# nostr-bot-poster: reads lines from file, posts scheduled
git clone https://github.com/swmtr/nostr-bot-poster
# Configure topics → cron post daily
```

**Repo:** https://github.com/swmtr/nostr-bot-poster

#### AI auto-reply bot (Nostr + Ollama)

```bash
git clone https://github.com/jooray/nostr-ai-bot.git
cd nostr-ai-bot
# Configure: Ollama endpoint + Nostr keys
# Bot responds to DMs using local LLM
python3 main.py
```

**Repo:** https://github.com/jooray/nostr-ai-bot

#### Auto-reply keyword bot

```bash
git clone https://github.com/Xeift/Nostr-Bot
cd Nostr-Bot
# Configure keywords + responses
python3 Bot/main.py
```

**Repo:** https://github.com/Xeift/Nostr-Bot

---

### Full Self-Hosted Nostr + Lightning Stack

```
[Mac / VPS — ZERO third-party registration]
    │
    ├── LND (Lightning Network Daemon)
    │     │
    │     └── Ligess/Nostdress (self-hosted Lightning address + zap server)
    │
    ├── Nostr Relay (nostream/strfry)
    │     │
    │     └── Paid access via Lightning admission fee
    │
    ├── Ollama (local AI models)
    │     │
    │     └── Aperture/LNbits paywall → paywalled AI API
    │
    ├── DVM (nostrdvm/ezdvm)
    │     │
    │     └── Sell AI inference as Nostr service (NIP-90)
    │
    ├── Content Publishing
    │     │
    │     └── nak + cron → auto-publish articles → earn zaps
    │
    └── Marketplace
          │
          └── LNbits Nostr Market → sell digital products
```

#### Self-hosted Lightning address (untuk terima zaps)

**Ligess:**
```bash
git clone https://github.com/Dolu89/ligess
cd ligess && npm install
# Configure: LND REST API + macaroon
# Result: yourname@yourdomain.com sebagai Lightning address
```

**Nostdress (LN address + NIP-05 + NIP-57):**
```bash
git clone https://github.com/iWarpBTC/nostdress
cd nostdress
# Configure HOST, PORT, DOMAIN, NOSTR_PRIVATE_KEY
# NIP-57 zaps work with LND backend
```

---

## SECTION C: Staking CLI Cheatsheet

### Solana

```bash
sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"
solana-keygen new                    # generate wallet
solana balance                       # check balance
solana create-stake-account stake.json 10 --from keypair.json
solana delegate-stake stake.json <VALIDATOR>
solana stake-account stake.json      # check rewards
# APY: 6-9%, rewards setiap 2-3 hari
```

### Cosmos (ATOM)

```bash
git clone https://github.com/cosmos/gaia.git && cd gaia && make install
gaiad keys add mykey                 # generate wallet
gaiad tx staking delegate <VALIDATOR> 1000000uatom --from mykey --chain-id cosmoshub-4
gaiad tx distribution withdraw-rewards <VALIDATOR> --from mykey
# APY: 9-19%, unbonding: 21 hari
```

### Stacks (STX) → Earn BTC

```bash
# Install stacks CLI
npm install -g @stacks/cli
stx make_keychain                    # generate wallet
# Delegate STX via CLI → earn BTC rewards
# APY: ~8-10% paid in BTC
```

---

## SECTION D: Consolidated Action Plan

### Phase 1: Hari Ini (0 modal, 2-3 jam)

| Step | Action | Tool |
|------|--------|------|
| 1 | Install Ollama + pull llama3.2 | `curl -fsSL https://ollama.com/install.sh \| sh` |
| 2 | Generate Nostr keypair | `pip install nostr` + Python script |
| 3 | Install nak CLI | `go install github.com/fiatjaf/nak@latest` |
| 4 | Post first note ke Nostr | `nak event -c 'hello' wss://nos.lol` |
| 5 | Setup cron daily post | `crontab -e` |
| 6 | Setup Nostr AI DVM (ezdvm + Ollama) | `pip install ezdvm` |

**Hasil:** AI DVM running, daily Nostr presence, mulai collect zaps.

### Phase 2: Minggu Pertama (butuh sedikit setup)

| Step | Action | Tool |
|------|--------|------|
| 7 | Install LNbits | `git clone lnbits/lnbits` |
| 8 | Setup paywall untuk Ollama API | Python middleware |
| 9 | List digital products di Shopstr | Via Nostr keypair |
| 10 | Claude Code bikin prompt packs → jual via Nostr marketplace | ezdvm + LNbits |
| 11 | Publish long-form content (NIP-23) di Habla | nak CLI |

**Hasil:** Multiple income channels active, AI inference paywalled.

### Phase 3: Bulan Pertama (kalau punya crypto)

| Step | Action | Tool |
|------|--------|------|
| 12 | Stake SOL via CLI | `solana-keygen new` + delegate |
| 13 | Stake ATOM via CLI | `gaiad keys add` + delegate |
| 14 | Setup LND + Aperture (L402 paywall) | Full Lightning node |
| 15 | Self-hosted Lightning address (Ligess) | Self-custodial zaps |
| 16 | Run paid Nostr relay (nostream) | VPS + Docker |

**Hasil:** Staking rewards + professional paywalled AI API + self-custodial everything.

---

## Revenue Projection (Konservatif, dari Indonesia)

### Skenario A: $0 Modal

| Stream | Bulan 1 | Bulan 3 | Bulan 6 |
|--------|---------|---------|---------|
| Nostr DVM (AI inference) | $2 | $10 | $25 |
| Nostr content zaps | $1 | $5 | $15 |
| Digital product sales (Nostr) | $0 | $10 | $30 |
| LNbits paywalled API | $0 | $5 | $20 |
| **Total** | **$3** | **$30** | **$90** |

### Skenario B: $1,000 Modal Crypto

| Stream | Bulan 1 | Bulan 3 | Bulan 6 |
|--------|---------|---------|---------|
| SOL staking ($500) | $3 | $3 | $3 |
| ATOM staking ($500) | $5 | $5 | $5 |
| + Skenario A | $3 | $30 | $90 |
| **Total** | **$11** | **$38** | **$98** |

### Skenario C: $5,000+ Modal Crypto + VPS

| Stream | Bulan 1 | Bulan 3 | Bulan 6 |
|--------|---------|---------|---------|
| SOL staking ($2,500) | $15 | $15 | $15 |
| ATOM staking ($2,500) | $25 | $25 | $25 |
| Lightning routing node | $0 | $5 | $15 |
| Paid Nostr relay | $0 | $5 | $10 |
| Aperture paywalled AI API | $5 | $30 | $100 |
| + Skenario A growth | $3 | $30 | $90 |
| **Total** | **$48** | **$110** | **$255** |

---

## Honest Final Verdict

**Zero-registration income dari terminal itu NYATA tapi KECIL.**

Paling realistis tanpa modal:
- **$30-90/bulan** setelah 3-6 bulan effort
- Mayoritas dari Nostr DVM + content zaps + digital product sales

Dengan modal crypto $1K-5K:
- **$100-255/bulan** setelah 6 bulan
- Staking = steady income, Nostr = growth potential

**Perbandingan dengan platform yang butuh registrasi (Part 1 & 2):**
- Zero-reg ceiling: ~$255/bulan
- With-reg ceiling: ~$14,580/bulan
- **Ratio: 1:57**

**Rekomendasi pragmatis:**
Gunakan zero-reg streams (staking, Nostr, self-hosted AI) sebagai **passive base income**, lalu tambahkan 1-2 platform with-registration (dev.to content + Gumroad products) untuk **10-50x boost**.

---

## All Repos Referenced

| Tool | URL |
|------|-----|
| Aperture (L402) | https://github.com/lightninglabs/aperture |
| x402 (Coinbase) | https://github.com/coinbase/x402 |
| LNbits | https://github.com/lnbits/lnbits |
| LNbits Paywall | https://github.com/lnbits/paywall |
| ln-paywall (Go) | https://github.com/philippgille/ln-paywall |
| Boltwall (Node.js) | https://github.com/Tierion/boltwall |
| nostrdvm | https://github.com/believethehype/nostrdvm |
| ezdvm | https://github.com/dtdannen/ezdvm |
| DVMCP | https://github.com/gzuuus/dvmcp |
| getAlby MCP | https://github.com/getAlby/mcp |
| LangChainBitcoin | https://github.com/lightninglabs/LangChainBitcoin |
| nostr-ai-bot | https://github.com/jooray/nostr-ai-bot |
| Nostr-Bot | https://github.com/Xeift/Nostr-Bot |
| nostr-bot-poster | https://github.com/swmtr/nostr-bot-poster |
| nak (CLI) | https://github.com/fiatjaf/nak |
| nostril | https://github.com/jb55/nostril |
| nostr-commander-rs | https://github.com/8go/nostr-commander-rs |
| Shopstr | https://github.com/shopstr-eng/shopstr |
| LNbits Nostr Market | https://github.com/lnbits/nostrmarket |
| SatShoot | https://github.com/Pleb5/satshoot |
| nostream (relay) | https://github.com/cameri/nostream |
| strfry (relay) | https://github.com/hoytech/strfry |
| Ligess | https://github.com/Dolu89/ligess |
| Nostdress | https://github.com/iWarpBTC/nostdress |
| nostr-zap-server | https://github.com/feikede/nostr-zap-server |
| BoostZapper | https://github.com/vicariousdrama/BoostZapper |
| Ollama | https://ollama.com |
| Bittensor | https://docs.learnbittensor.org |
| n8n x402 workflow | https://n8n.io/workflows/6597 |
| NIP-90 Spec | https://nips.nostr.com/90 |
| DVM Registry | https://github.com/nostr-protocol/data-vending-machines |
| Nostr Zap Stats | https://zaplytics.app |

---

## Links ke Semua Plan

- **Part 1 (Stream #1-6):** [passive-income-terminal-plan.md](./2026-03-13-passive-income-terminal-plan.md)
- **Part 2 (Stream #7-17):** [hidden-gems-terminal-income.md](./2026-03-13-hidden-gems-terminal-income.md)
- **Part 3 (Zero Registration overview):** [zero-registration-terminal-income.md](./2026-03-13-zero-registration-terminal-income.md)
- **Part 4 (Actionable deep dive):** File ini
