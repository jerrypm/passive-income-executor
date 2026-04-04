# Passive Income Executor — Claude Code Context

## Siapa Saya
- iOS developer & web developer dari Indonesia
- Pakai macOS (Mac Mini untuk execution, MacBook untuk planning)
- Punya Claude Code, Docker, Homebrew, Python, Node.js, Go
- Bahasa: Indonesia campur Inggris
- Prefer simple, jangan over-engineer

## Apa Project Ini
Project ini adalah **execution hub** untuk setup multiple passive income streams dari terminal.
Semua research sudah selesai (4 dokumen di `docs/plans/`). Sekarang tinggal EKSEKUSI.

## Research Files (BACA INI DULU)
- `docs/plans/2026-03-13-passive-income-terminal-plan.md` — Part 1: 6 streams platform-based
- `docs/plans/2026-03-13-hidden-gems-terminal-income.md` — Part 2: 11 hidden gem streams
- `docs/plans/2026-03-13-zero-registration-terminal-income.md` — Part 3: Zero-registration methods
- `docs/plans/2026-03-13-actionable-zero-reg-deep-dive.md` — Part 4: Actionable deep dive AI + Nostr

## PRIORITAS EKSEKUSI (Urutan)

### Phase 1: Hari Ini — Zero Modal, Pure Terminal
1. **Install Ollama + pull models**
   ```
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull llama3.2
   ollama pull deepseek-r1
   ollama pull codellama
   ```

2. **Generate Nostr keypair**
   ```
   pip install nostr
   # Generate via Python script
   ```

3. **Install nak CLI (Nostr)**
   ```
   brew install go
   go install github.com/fiatjaf/nak@latest
   ```

4. **Post pertama ke Nostr**
   ```
   nak event --sec <key> -c 'Hello Nostr!' wss://nos.lol wss://relay.damus.io
   ```

5. **Setup cron daily post**
   ```
   crontab -e
   # 15 6 * * * /path/to/nak event --sec <key> -c 'gm' wss://nos.lol
   ```

6. **Setup Nostr AI DVM (ezdvm + Ollama)**
   ```
   pip install ezdvm
   # Buat DVM kind 5050 (text generation) backed by Ollama
   ```

### Phase 2: Minggu 1 — Payment Infrastructure
7. **Install LNbits** (self-hosted Lightning wallet)
   ```
   git clone https://github.com/lnbits/lnbits.git
   cd lnbits && pip install -e . && lnbits
   ```

8. **Setup paywall Ollama API** (LNbits + Python middleware)

9. **List digital products di Shopstr** (Nostr marketplace)

10. **Publish long-form content di Habla** (habla.news via nak CLI)

### Phase 3: Bulan 1 — Scaling (Kalau Punya Crypto)
11. Stake SOL via `solana-keygen new` + `solana delegate-stake`
12. Stake ATOM via `gaiad keys add` + `gaiad tx staking delegate`
13. Setup LND + Aperture (L402 paywall untuk Ollama)
14. Self-hosted Lightning address (Ligess)
15. Run paid Nostr relay (nostream)

### Phase 4: Ongoing — Platform-Based (Butuh Registrasi)
16. money4band Docker (bandwidth sharing)
17. Content machine (dev.to + Hashnode + affiliate)
18. RapidAPI (jual API)
19. Apify (jual scraper)

## KEY TOOLS & REPOS

### AI Inference Monetization
| Tool | Repo | Purpose |
|------|------|---------|
| Aperture | github.com/lightninglabs/aperture | L402 reverse proxy paywall |
| x402 | github.com/coinbase/x402 | USDC payment protocol |
| LNbits | github.com/lnbits/lnbits | Self-hosted Lightning wallet |
| Boltwall | github.com/Tierion/boltwall | Node.js Lightning middleware |
| ln-paywall | github.com/philippgille/ln-paywall | Go Lightning middleware |

### Nostr Ecosystem
| Tool | Repo | Purpose |
|------|------|---------|
| nak | github.com/fiatjaf/nak | Nostr CLI (post, query, etc) |
| nostrdvm | github.com/believethehype/nostrdvm | DVM framework (Python) |
| ezdvm | github.com/dtdannen/ezdvm | Simple DVM lib |
| DVMCP | github.com/gzuuus/dvmcp | Bridge MCP ↔ Nostr DVM |
| nostr-ai-bot | github.com/jooray/nostr-ai-bot | AI bot on Nostr |
| Shopstr | shopstr.store | Nostr marketplace |
| nostream | github.com/cameri/nostream | Paid Nostr relay |
| Ligess | github.com/Dolu89/ligess | Self-hosted LN address |
| Nostdress | github.com/iWarpBTC/nostdress | LN address + NIP-05 |

### Staking CLI
| Chain | Install | Wallet | Stake |
|-------|---------|--------|-------|
| Solana | `sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"` | `solana-keygen new` | `solana delegate-stake` |
| Cosmos | `git clone cosmos/gaia && make install` | `gaiad keys add mykey` | `gaiad tx staking delegate` |
| Stacks | `npm install -g @stacks/cli` | `stx make_keychain` | Delegate STX → earn BTC |

### Other Tools
| Tool | Repo | Purpose |
|------|------|---------|
| money4band | github.com/MRColorR/money4band | Bandwidth sharing Docker stack |
| Hummingbot | github.com/hummingbot/hummingbot | Crypto market making |
| BTCPay Server | github.com/btcpayserver/btcpayserver | Self-hosted payment processor |

## REVENUE TARGETS

### Tanpa Modal (6 bulan)
- Nostr DVM + content + marketplace: ~$90/bulan
- AI inference paywall: ~$10-100/bulan

### Dengan Crypto $1K-5K (6 bulan)
- Staking: ~$40-50/bulan
- + Zero-modal streams: ~$98-255/bulan

### Dengan Registrasi Platform (6 bulan, dari Part 1 & 2)
- Content + affiliate: $200/bulan
- API + scraper: $450/bulan
- Digital products: $100/bulan
- Total combined: **$810-2,375/bulan**

## WORKFLOW RULES
- Eksekusi satu phase pada satu waktu, jangan lompat
- Test setiap stream sebelum move on
- Log earnings di `logs/earnings.md`
- Simpan semua credentials di `.env` (JANGAN commit)
- Commit sering dengan pesan yang jelas

## TWITTER RULES (WAJIB)
- **MAX 277 CHARACTERS per tweet** — HITUNG DULU sebelum post, jangan pernah melebihi
- Selalu pakai Chrome Profile 10 (Jeri / @luffyselah) — JANGAN pakai profile lain
- Hitung karakter pakai `len()` di Python atau manual sebelum copy ke clipboard
- Kalau lebih dari 277, POTONG dulu baru post

## CHROME RULES (WAJIB)
- **SELALU pakai Profile 10 (Jeri / 21zerixpm@gmail.com)**
- Command buka: `open -na "Google Chrome" --args --profile-directory="Profile 10" "URL"`
- Command navigate tab: cari window yang title mengandung "Jeri" lalu set URL
- **JANGAN PERNAH** ubah atau pakai user/profile Chrome lain
- **SEMUA SCRIPT PYTHON** yang pakai Chrome HARUS specify Profile 10
- Untuk navigate di tab yang sama, HARUS cari window Chrome yang profile "Jeri" dulu
- Kalau salah profile = salah akun = MASALAH BESAR

## FOLDER STRUCTURE
```
passive-income-executor/
├── CLAUDE.md              ← File ini (auto-loaded by Claude Code)
├── docs/plans/            ← Research documents (Part 1-4)
├── scripts/               ← Automation scripts (cron, bots, etc)
│   ├── nostr/             ← Nostr bot & DVM scripts
│   ├── ai-inference/      ← Ollama paywall middleware
│   ├── content-machine/   ← Auto-publish scripts
│   ├── youtube/           ← YouTube Shorts generation pipeline
│   └── staking/           ← Staking helper scripts
├── videos/
│   ├── ready/             ← Generated shorts (MP4 + metadata)
│   └── archive/           ← Already uploaded
├── logs/                  ← Earnings & activity logs
├── .env                   ← Credentials (gitignored)
└── .gitignore
```
