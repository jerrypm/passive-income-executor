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

## BLOGGER AUTO-POST (jrdevhub.com)

### Quick Post Draft
```bash
echo "y" | /usr/bin/python3 -W ignore post_to_blogger.py -f "/full/path/to/article.html" --draft 2>&1
```
Run from: `scripts/blogger/`
Python: HARUS pakai `/usr/bin/python3` (bukan default python3)

### Article Format
Setiap file HTML artikel HARUS punya comment block di atas:
```html
<!--
TITLE: Judul Artikel
SEARCH DESCRIPTION: Deskripsi SEO (max 155 char)
LABELS: tag1, tag2, tag3
-->
(konten HTML di sini)
```

### Rules
- JANGAN pakai HTML entities (`&mdash;`, `&ndash;`) — pakai unicode langsung: — dan –
- Simpan artikel di `articles/` dengan format: `NNN-slug-name.html`
- SELALU post sebagai `--draft` kecuali user bilang publish
- Include gambar Unsplash (free license, tambah `?w=800&q=80`)
- Include Gumroad product CTA di akhir artikel yang relevan
- Pakai `!important` untuk list styles (override template CSS reset)

### Gumroad Products (promote di artikel)
1. Terminal Income Starter ($9) — https://zerix1.gumroad.com/l/ptikgy
2. Ollama API Monetizer ($14) — https://zerix1.gumroad.com/l/pzesvw
3. Nostr AI Toolkit ($19) — https://zerix1.gumroad.com/l/vrblqu
4. InfiXOX Android Source ($14) — https://zerix1.gumroad.com/l/pheupx
5. 1000 Expert Prompts ($9, launch) — Gumroad URL pending upload. Source: `products/1000-expert-prompts/`. 10 kategori × 100 prompt (Marketing/SEO/Business/Dev/AI/Writing/Social/Data/Design/Career). Role-based + framework-powered + variable-driven.
6. Mastering Claude Code ($19) — Gumroad URL pending upload. Source: `products/claude-code-ebook/`. 20 chapters, 50 hidden tips, beginner-to-expert guide. 36K words, 156 pages PDF.

### Amazon Affiliate
- Associate ID: `fullmoonmauli-20`
- Link: `https://www.amazon.com/dp/ASIN?tag=fullmoonmauli-20`

### Blog Design Specs
- Fonts: Domine (body), Josefin Sans (headings), Montserrat (labels)
- Colors: #ff7f24 (primary), #c62641 (links), #333 (headings)
- Width: 728px content area

## FOLDER STRUCTURE
```
passive-income-executor/
├── CLAUDE.md              ← File ini (auto-loaded by Claude Code)
├── docs/plans/            ← Research documents (Part 1-4)
├── articles/              ← HTML articles for Blogger (siap post)
├── scripts/               ← Automation scripts
│   ├── blogger/           ← Blogger API auto-poster
│   │   ├── post_to_blogger.py  ← Post HTML ke Blogger
│   │   ├── auto_article.py     ← Generate + post via Ollama
│   │   ├── client_secret.json  ← OAuth credentials (gitignored)
│   │   └── token.json          ← Auth token (gitignored)
│   ├── nostr/             ← Nostr bot & DVM scripts
│   ├── ai-inference/      ← Ollama paywall middleware
│   ├── content-machine/   ← Auto-publish scripts
│   ├── youtube/           ← YouTube Shorts generation pipeline
│   └── staking/           ← Staking helper scripts
├── videos/
│   ├── ready/             ← Generated shorts (MP4 + metadata)
│   └── archive/           ← Already uploaded
├── products/              ← Gumroad digital products
├── logs/                  ← Earnings & activity logs
├── blogger.xml            ← Blogger template (jrdevhub theme)
├── .env                   ← Credentials (gitignored)
└── .gitignore
```
