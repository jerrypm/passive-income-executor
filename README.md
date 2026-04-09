# Passive Income Executor

Execution hub untuk multiple passive income streams langsung dari terminal. Semua research sudah selesai (4 dokumen di `docs/plans/`), repo ini fokus ke **eksekusi**: scripts, automations, cron jobs, dan tooling untuk jalanin masing-masing stream.

## Apa Isinya

- Nostr bots, DVMs, marketplace publisher, long-form publisher
- Ollama paywall (HTTP API + Lightning + RapidAPI wrapper)
- Content machine (dev.to, Hashnode, Medium/Twitter, newsletter)
- Bandwidth sharing (money4band Docker stack)
- Staking helpers (Solana, Cosmos, Stacks)
- Twitter auto-post (Chrome automation, no API key)
- Auto research pipeline (HN, Reddit, dev.to, GitHub, Product Hunt, IH)
- Websites (`devtoolkit`, `barangunik`) — Next.js on Vercel
- Gumroad-ready product bundles (`products/*.zip`)

## Folder Structure

```
passive-income-executor/
├── CLAUDE.md              # Claude Code context (project instructions)
├── README.md              # You are here
├── docs/
│   └── plans/             # Research documents (Part 1–4 + hidden gems + Docker)
├── scripts/
│   ├── nostr/             # Nostr bot, DVM, publisher scripts
│   ├── ai-inference/      # Ollama paywall middleware
│   ├── content-machine/   # Auto-publish dev.to / Hashnode / Nostr
│   ├── twitter/           # Chrome-based Twitter auto-post
│   ├── youtube/           # YouTube Shorts pipeline
│   ├── staking/           # Solana / Cosmos / Stacks helpers
│   ├── bandwidth/         # money4band Docker setup
│   ├── faucets/           # Lightning faucet rotation
│   ├── telegram/          # Telegram bot (Ollama-backed)
│   ├── auto-research/     # Daily research + email digest
│   └── launcher.sh        # Master start/stop/status for all services
├── websites/
│   ├── devtoolkit/        # https://devtoolkit-sigma.vercel.app
│   └── barangunik/        # Shopee affiliate site
├── products/              # Gumroad ZIP bundles
├── services/              # Docker stacks (money4band, etc.)
├── videos/                # YouTube Shorts ready/archive
├── logs/                  # Earnings & activity logs
└── .env                   # Credentials (gitignored)
```

## Phases

### Phase 1 — Zero Modal (Pure Terminal)
Install Ollama, generate Nostr keypair, install `nak` CLI, post ke Nostr, setup cron daily post, bikin Nostr AI DVM backed by Ollama.

### Phase 2 — Payment Infrastructure
Self-host LNbits, paywall Ollama API, list digital products di Shopstr, publish long-form di Habla.

### Phase 3 — Scaling (butuh crypto)
Stake SOL / ATOM / STX, setup LND + Aperture (L402 paywall), self-hosted Lightning address, paid Nostr relay.

### Phase 4 — Platform-Based
money4band Docker (bandwidth sharing), content machine (dev.to + Hashnode + affiliate), RapidAPI, Apify.

## Research Documents

- `docs/plans/2026-03-13-passive-income-terminal-plan.md` — 6 platform-based streams
- `docs/plans/2026-03-13-hidden-gems-terminal-income.md` — 11 hidden gem streams
- `docs/plans/2026-03-13-zero-registration-terminal-income.md` — Zero-registration methods
- `docs/plans/2026-03-13-actionable-zero-reg-deep-dive.md` — Deep dive: AI + Nostr
- `docs/plans/2026-03-14-hidden-gem-tools-research.md` — 83 extra tools
- `docs/plans/2026-03-15-docker-passive-income-research.md` — Docker apps research
- `docs/plans/2026-03-17-ios-developer-passive-income-research.md`
- `docs/plans/2026-03-17-website-passive-income-no-ads-research.md`
- `docs/plans/2026-04-05-barangunik-marketing-research-complete.md`

## Key Tools

### AI Inference Monetization
| Tool | Purpose |
|------|---------|
| Aperture | L402 reverse proxy paywall |
| x402 | USDC payment protocol |
| LNbits | Self-hosted Lightning wallet |
| Boltwall / ln-paywall | Lightning middleware |

### Nostr Ecosystem
| Tool | Purpose |
|------|---------|
| nak | Nostr CLI (post, query) |
| nostrdvm / ezdvm | DVM frameworks |
| DVMCP | Bridge MCP ↔ Nostr DVM |
| Shopstr | Nostr marketplace |
| nostream | Paid Nostr relay |
| Ligess / Nostdress | Self-hosted LN address |

### Staking CLI
| Chain | Wallet | Stake |
|-------|--------|-------|
| Solana | `solana-keygen new` | `solana delegate-stake` |
| Cosmos | `gaiad keys add mykey` | `gaiad tx staking delegate` |
| Stacks | `stx make_keychain` | Delegate STX → earn BTC |

## Revenue Targets

- **Tanpa modal (6 bulan):** ~$100–190/bulan (Nostr DVM + content + marketplace + AI paywall)
- **Dengan crypto $1K–5K (6 bulan):** +$40–50/bulan dari staking
- **Dengan registrasi platform (6 bulan):** $810–2,375/bulan combined

## Workflow Rules

- Eksekusi satu phase pada satu waktu, jangan lompat
- Test setiap stream sebelum move on
- Log earnings di `logs/earnings.md`
- Credentials di `.env` (JANGAN commit)
- Commit sering dengan pesan yang jelas

## Status

See `CLAUDE.md` and the memory at `~/.claude/projects/-Users-avika-Documents-passive-income-executor/memory/MEMORY.md` for live project status.
