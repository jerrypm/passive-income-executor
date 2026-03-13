# Hidden Gems: Passive Income dari Terminal (Part 2)

> **Tanggal:** 2026-03-13
> **Konteks:** Tambahan dari riset deep internet — hal-hal yang jarang orang tau tapi terbukti menghasilkan
> **Target:** $5-100/hari per stream
> **Prinsip:** Semua bisa di-build/manage dari Claude Code terminal

---

## Master List

| # | Stream | Potensi/Hari | Setup | Hidden Level |
|---|--------|-------------|-------|-------------|
| 7 | Polymarket Weather Bot | $10-800 | 3-5 jam | 🔥🔥🔥🔥🔥 |
| 8 | Sell Datasets (Data-as-a-Service) | $5-50 | 2-4 jam | 🔥🔥🔥🔥🔥 |
| 9 | Telegram Bot Monetized | $5-100 | 4-8 jam | 🔥🔥🔥🔥 |
| 10 | Jual AI Prompts | $5-30 | 1-2 jam | 🔥🔥🔥🔥 |
| 11 | SaaS Boilerplate / Starter Kit | $10-100 | 1-2 hari | 🔥🔥🔥🔥 |
| 12 | Chrome Extension | $5-300 | 1-2 hari | 🔥🔥🔥 |
| 13 | Notion/Obsidian Templates | $5-50 | 2-4 jam | 🔥🔥🔥 |
| 14 | Hummingbot (Crypto Market Making) | $10-500 | 4-8 jam | 🔥🔥🔥🔥🔥 |
| 15 | Newsletter Otomatis (Beehiiv) | $5-50 | 3-5 jam | 🔥🔥🔥 |
| 16 | MCP Server / Claude Plugin | $5-100 | 4-8 jam | 🔥🔥🔥🔥🔥 |
| 17 | Discord Bot Premium | $5-50 | 4-8 jam | 🔥🔥🔥 |

---

## Stream #7: Polymarket Weather Bot ⭐ HIDDEN GEM TERBESAR

### Apa Ini?
Bot otomatis yang trading di Polymarket (prediction market) berdasarkan data cuaca NOAA. Bot membandingkan forecast cuaca professional vs odds di Polymarket → kalau ada gap → bot taruhan di sisi yang benar.

### Kenapa Ini Hidden Gem?
- Weather bots quietly making **$24,000+** di Polymarket
- Satu bot OpenClaw generate **$115,000 profit dalam 1 minggu**
- Bot lain execute 8,894 trades → **$150,000 profit**
- NOAA forecast accuracy 85-90% → edge yang konsisten
- Kebanyakan orang nggak tau ini ada

### Cara Kerja
```
Cron job setiap jam
  │
  ▼
Fetch NOAA weather forecast data (free API)
  │
  ▼
Bandingkan dengan Polymarket odds
  │
  ▼
Kalau gap > threshold → place bet otomatis
  │
  ▼
Profit dari market yang mispriced
```

### Setup dari Terminal
```bash
# 1. Clone Polymarket agents repo
git clone https://github.com/Polymarket/agents.git
cd agents

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API keys
# - Polymarket API key
# - NOAA weather API key (free)
# - Polygon wallet (untuk deposit USDC)

# 4. Claude Code customisasi strategy
# Edit strategy untuk fokus weather markets

# 5. Jalankan bot
python main.py

# 6. Setup cron untuk auto-run
```

### Earnings Realistis
| Modal Awal | Strategi | Profit/Hari |
|-----------|----------|-------------|
| $100 | Conservative (small bets) | $2-10 |
| $500 | Moderate | $10-50 |
| $2,000+ | Aggressive | $50-800 |

### Risiko
- ⚠️ Ini TRADING — bisa rugi
- ⚠️ Butuh modal awal (USDC di Polygon)
- ⚠️ Market conditions bisa berubah
- ✅ Tapi weather prediction punya edge yang terukur (85-90% accuracy)
- ✅ Arbitrage opportunities = lower risk than directional trading

### Resources
- Polymarket Agents: https://github.com/Polymarket/agents
- NOAA Weather API: https://www.weather.gov/documentation/services-web-api
- Article: https://blog.devgenius.io/found-the-weather-trading-bots-quietly-making-24-000-on-polymarket-and-built-one-myself-for-free-120bd34d6f09

---

## Stream #8: Sell Datasets (Data-as-a-Service)

### Apa Ini?
Scrape data secara otomatis → package sebagai dataset → jual di marketplace atau langganan ke klien. Orang bayar untuk data yang sudah clean & structured.

### Kenapa Hidden Gem?
- Kebanyakan orang cuma scrape data untuk diri sendiri, nggak jual
- Demand untuk AI training data SANGAT TINGGI di 2026
- Dataset marketplace masih relatively baru & low competition
- Recurring income: klien subscribe untuk data update mingguan/bulanan

### Contoh Dataset yang Laku

| Dataset | Target Buyer | Harga |
|---------|-------------|-------|
| Trending GitHub repos harian | Developer tools, VCs | $10-50/bulan |
| App Store rankings + reviews | Mobile developers | $20-100/bulan |
| Job listings tech companies | Recruiters, job boards | $50-200/bulan |
| Real estate listings | Property investors | $50-300/bulan |
| Restaurant data + reviews | Food industry | $20-100/bulan |
| E-commerce product prices | Retailers, analysts | $50-500/bulan |
| Crypto/NFT market data | Traders | $20-200/bulan |

### Marketplace untuk Jual Dataset

| Platform | Revenue Share | URL |
|----------|--------------|-----|
| **Opendatabay** | Varies | https://www.opendatabay.com |
| **Bounding.ai** | Varies | https://bounding.ai |
| **Datarade** | Varies | https://datarade.ai |
| **TARTLE DataVault** | Varies | https://www.tartle.co |
| **Gumroad** (self-hosted) | 90% (10% fee) | https://gumroad.com |

### Setup dari Terminal
```bash
# 1. Claude Code bikin scraper (Python + BeautifulSoup/Playwright)
mkdir ~/projects/data-service && cd ~/projects/data-service

# 2. Buat scraper script
# File: scraper.py — Claude Code generate

# 3. Buat data cleaner
# File: cleaner.py — normalize, deduplicate, format

# 4. Output ke CSV/JSON
python scraper.py --output data/github-trending-2026-03-13.csv

# 5. Upload ke marketplace via API
# Atau jual via Gumroad API

# 6. Setup cron untuk auto-scrape & update
crontab -e
# 0 6 * * * cd ~/projects/data-service && python scraper.py && python upload.py
```

### Earnings Realistis
| Jumlah Dataset | Subscribers | Income/Bulan |
|----------------|------------|--------------|
| 1 dataset | 5-10 | $50-500 |
| 3 datasets | 15-30 | $200-2,000 |
| 5+ datasets | 30-50 | $500-5,000 |

### Pasif Level: ⭐⭐⭐⭐
Scraper jalan via cron. Data auto-update. Subscribers auto-renew. Kadang perlu fix scraper kalau website berubah.

---

## Stream #9: Telegram Bot Monetized

### Apa Ini?
Build Telegram bot yang kasih value (alerts, tools, content) → monetisasi via subscription, affiliate links, atau Telegram Ads revenue share.

### Kenapa Hidden Gem?
- Telegram punya 900M+ users
- Revenue share 90/10 (paling creator-friendly)
- Bot bisa handle semuanya otomatis 24/7
- Bisa integrate payment langsung di chat

### Ide Bot yang Menghasilkan

| Bot Idea | Monetisasi | Potensi |
|----------|-----------|---------|
| Crypto price alert bot | Premium tier $5/bulan | $100-2,000/bulan |
| AI writing assistant bot | Per-use fee | $50-500/bulan |
| Job alert bot (tech) | Affiliate links | $50-300/bulan |
| News summary bot | Ads + premium | $100-1,000/bulan |
| Stock screener bot | Subscription $10/bulan | $200-3,000/bulan |
| Deals/coupon finder bot | Affiliate commissions | $100-2,000/bulan |

### Setup dari Terminal
```bash
# 1. Create bot via @BotFather di Telegram (1x, perlu HP)

# 2. Claude Code bikin bot (Python python-telegram-bot)
mkdir ~/projects/tg-bot && cd ~/projects/tg-bot
pip install python-telegram-bot

# 3. Claude Code bikin logic
# File: bot.py

# 4. Deploy (bisa di Mac sendiri atau free VPS)
nohup python bot.py &

# 5. Atau deploy via Docker
docker build -t mybot .
docker run -d --restart always mybot
```

### Monetisasi Channel
```
Bot gratis → build 1,000+ users
  │
  ▼
Tambah premium features (subscribe via Telegram Stars / Stripe)
  │
  ▼
Tambah affiliate links di bot responses
  │
  ▼
Join Telegram Ad Revenue Share (50% dari ads di channel)
```

### Earnings Realistis
| Users | Method | Income/Bulan |
|-------|--------|--------------|
| 500 | Affiliate only | $20-100 |
| 1,000 | Premium + affiliate | $100-500 |
| 5,000 | Ads + premium + affiliate | $500-3,000 |
| 10,000+ | Full monetization | $1,000-5,000+ |

---

## Stream #10: Jual AI Prompts

### Apa Ini?
Bikin prompt yang bagus untuk ChatGPT/Claude/Midjourney → jual di marketplace.

### Kenapa Hidden Gem?
- Market growing massively di 2026
- Bikinnya cuma 5-30 menit per prompt
- Satu shop Etsy: 2,715 sales × $3.43 avg = **$9,312** dari prompts saja
- PromptBase: 80% revenue ke seller
- Bisa batch generate ratusan prompts dari Claude Code

### Setup dari Terminal
```bash
# 1. Claude Code batch generate prompt packs
# Misal: "50 SwiftUI Code Review Prompts"
# Misal: "100 Business Email Prompts"
# Misal: "30 Midjourney Architecture Prompts"

# 2. Format sebagai PDF/Notion template

# 3. Upload ke PromptBase
# https://promptbase.com/sell
# Revenue: 80% ke kamu

# 4. Upload ke Gumroad
# Via API (sudah ada di plan sebelumnya)
curl -X POST https://api.gumroad.com/v2/products \
  -d "access_token=XXX" \
  -d "name=50 SwiftUI Code Review Prompts" \
  -d "price=499" \
  -d "description=..."

# 5. Cross-list ke Etsy (manual 1x)
```

### Earnings Realistis
| Jumlah Prompt Packs | Platform | Income/Bulan |
|---------------------|----------|--------------|
| 5 packs | PromptBase | $20-100 |
| 10 packs | PromptBase + Gumroad | $50-300 |
| 20+ packs | Multi-platform | $100-1,000 |

### Pasif Level: ⭐⭐⭐⭐⭐
Upload sekali. Sales datang dari marketplace traffic. Zero maintenance.

---

## Stream #11: SaaS Boilerplate / Starter Kit

### Apa Ini?
Claude Code bikin full boilerplate project (auth + database + payment + deployment sudah setup) → jual di Gumroad sebagai starter kit. Developer bayar $49-199 supaya nggak perlu setup dari nol.

### Kenapa Hidden Gem?
- Developer WILLING to pay $100+ untuk skip boilerplate setup
- "Build once, sell forever" — literally zero maintenance
- Kamu sudah punya skill (iOS/SwiftUI + Python + Web)
- Delivered as GitHub repo access or zip file

### Ide Starter Kit

| Kit | Target Buyer | Harga |
|-----|-------------|-------|
| SwiftUI + Firebase Starter | iOS developers | $49-99 |
| FastAPI + Supabase + Auth | Python devs | $49-79 |
| Next.js + Stripe + Auth | Web devs | $79-199 |
| Telegram Bot Template | Bot builders | $29-49 |
| iOS App + AdMob Template | Indie devs | $39-79 |
| Python Web Scraper Framework | Data people | $29-59 |
| Docker Compose All-in-One | DevOps | $19-49 |

### Setup dari Terminal
```bash
# 1. Claude Code bikin full boilerplate
mkdir ~/projects/swiftui-starter-kit
# Claude Code generates all files

# 2. Push ke private GitHub repo
gh repo create swiftui-firebase-starter --private

# 3. List di Gumroad via API
curl -X POST https://api.gumroad.com/v2/products \
  -d "access_token=XXX" \
  -d "name=SwiftUI + Firebase Starter Kit" \
  -d "price=4900" \
  -d "description=Complete starter with Auth, Firestore, Push Notifications..."

# 4. Promosikan via artikel (Cron Content stream)
# Artikel di dev.to → CTA ke Gumroad product
```

### Earnings Realistis
| Products | Sales/Bulan | Avg Price | Income |
|----------|------------|-----------|--------|
| 1 kit | 5-15 | $49 | $245-735 |
| 3 kits | 15-45 | $49-99 | $735-4,455 |
| 5+ kits | 25-75 | $49-199 | $1,225-14,925 |

### Pasif Level: ⭐⭐⭐⭐⭐
Build once, sell forever. Occasional update kalau framework major version change.

---

## Stream #12: Chrome Extension

### Apa Ini?
Build Chrome extension sederhana yang solve 1 problem → monetisasi via freemium model atau one-time purchase.

### Kenapa Hidden Gem?
- Satu developer: **$10,000/bulan MRR** dari Chrome extensions
- Satu developer: **multi six-figure exit** dari jual extension
- 70-80% profit margin
- Build once, earn recurring

### Ide Extension

| Extension | Target User | Revenue Model |
|-----------|------------|---------------|
| Tab manager/organizer | Everyone | Freemium $3/bulan |
| GitHub profile enhancer | Developers | $5/bulan |
| AI writing assistant sidebar | Writers | $7/bulan |
| Website color palette extractor | Designers | $3 one-time |
| JSON formatter + viewer | Developers | Free + donate |
| SEO quick analyzer | Marketers | $5/bulan |

### Setup dari Terminal
```bash
# 1. Claude Code bikin extension
mkdir ~/projects/chrome-ext
# manifest.json, popup.html, content.js, background.js

# 2. Test locally
# Load unpacked di chrome://extensions (1x via browser)

# 3. Package
zip -r extension.zip manifest.json popup.html *.js icons/

# 4. Publish ke Chrome Web Store
# Upload via developer.chrome.com (1x, $5 one-time fee)

# 5. Add payment via ExtensionPay
# https://extensionpay.com — handles subscriptions inside extension
```

### Earnings Realistis
| Users | Model | Income/Bulan |
|-------|-------|--------------|
| 100 | Freemium $3/mo | $30-90 |
| 1,000 | Freemium $5/mo | $200-1,500 |
| 10,000 | Freemium $5/mo | $2,000-15,000 |

---

## Stream #13: Notion / Obsidian Templates

### Apa Ini?
Bikin template produktivitas → jual di Gumroad, Etsy, atau Notion marketplace.

### Kenapa Hidden Gem?
- Top creator Easlo: **$20,000/bulan** dari Notion templates
- Satu creator: **$15,000** dari 1 template saja
- 35M+ Notion users = massive market
- Bikin template = 2-4 jam per template
- Zero maintenance setelah upload

### Setup dari Terminal
```bash
# 1. Claude Code bikin template structure (markdown/JSON)
# Untuk Notion: bikin di Notion app, lalu share link
# Untuk Obsidian: bikin vault template (files + folders)

# 2. Buat landing page copy (Claude Code generate)

# 3. Upload ke Gumroad via API
curl -X POST https://api.gumroad.com/v2/products \
  -d "access_token=XXX" \
  -d "name=Ultimate Developer Productivity System" \
  -d "price=1900" \
  -d "url=notion-template-link"

# 4. Cross-list ke Etsy (manual)
# 5. Promote via Pinterest + TikTok + articles
```

### Template Ideas (Niche kamu: Developer)

| Template | Harga | Target |
|----------|-------|--------|
| iOS Project Planner | $9-19 | iOS devs |
| Sprint Planning System | $12-29 | Dev teams |
| Code Review Tracker | $9-15 | Engineers |
| Developer Job Hunt System | $15-29 | Job seekers |
| Content Creator Dashboard | $12-25 | Writers/devs |
| Bug Tracking System | $9-19 | QA/devs |

---

## Stream #14: Hummingbot (Crypto Market Making)

### Apa Ini?
Open-source bot yang otomatis jadi market maker di crypto exchanges. Kamu provide liquidity → earn dari spread (selisih buy/sell price).

### Kenapa Hidden Gem?
- Framework open-source = GRATIS
- Users generated **$34 BILLION** trading volume di 2025
- Jalan 100% dari terminal (CLI-based)
- Support 35+ exchanges
- Market making = lower risk than directional trading

### Setup dari Terminal
```bash
# 1. Install Hummingbot
# Via Docker (recommended)
docker pull hummingbot/hummingbot:latest
docker run -it --name hummingbot \
  -v ~/hummingbot_conf:/conf \
  -v ~/hummingbot_logs:/logs \
  hummingbot/hummingbot:latest

# 2. Di dalam Hummingbot CLI:
# > connect binance  (masukkan API key)
# > create           (pilih strategy: pure_market_making)
# > config           (set parameters)
# > start            (mulai trading)

# 3. Bot jalan 24/7, auto buy/sell, earn spread
```

### Strategies
| Strategy | Risk | Return |
|----------|------|--------|
| Pure Market Making | Medium | 0.5-2%/hari |
| Cross-Exchange Arbitrage | Low-Medium | 0.3-1%/hari |
| AMM Arbitrage (DeFi) | Medium | 0.5-3%/hari |
| Funding Rate Arbitrage | Low | 15-50% APR |

### Earnings Realistis
| Modal | Strategy | Profit/Hari |
|-------|----------|-------------|
| $500 | Market Making | $2-10 |
| $2,000 | Market Making | $10-40 |
| $5,000 | Arbitrage + MM | $25-100 |
| $10,000+ | Multi-strategy | $50-500 |

### Risiko
- ⚠️ Butuh modal (crypto di exchange)
- ⚠️ Impermanent loss possible
- ⚠️ Exchange bisa down
- ✅ Market making = systematic, bukan gambling
- ✅ Spread earning = consistent small profits

### Resources
- Hummingbot: https://hummingbot.org
- GitHub: https://github.com/hummingbot/hummingbot
- Docs: https://docs.hummingbot.org

---

## Stream #15: Newsletter Otomatis (Beehiiv)

### Apa Ini?
Setup newsletter → auto-generate content via Claude → auto-send via Beehiiv API → monetisasi via ads, sponsors, paid subscribers.

### Kenapa Hidden Gem?
- Beehiiv punya **Ad Network built-in** (kamu langsung earn dari ads)
- **Boost feature**: newsletter lain bayar KAMU untuk recommend subscribers
- Beehiiv API = bisa automate semua dari terminal
- Revenue share paling bagus di industry

### Setup dari Terminal
```bash
# 1. Daftar Beehiiv (beehiiv.com) — free plan available

# 2. Get API key dari Beehiiv dashboard

# 3. Claude Code bikin auto-newsletter script
# - Fetch trending topics (dev.to API, GitHub trending, HN)
# - Generate newsletter content
# - Send via Beehiiv API

# 4. Cron job: send newsletter 2x/minggu
crontab -e
# 0 7 * * 1,4 cd ~/scripts/newsletter && python send_newsletter.py
```

### Monetisasi
| Method | Requirement | Income |
|--------|------------|--------|
| Beehiiv Ad Network | 1,000+ subscribers | $50-500/bulan |
| Boosts (paid recommendations) | Any size | $1-3 per subscriber gained |
| Paid subscriptions | Good content | $5-20/subscriber/bulan |
| Sponsor slots | 5,000+ subscribers | $100-2,000/issue |

---

## Stream #16: MCP Server / Claude Plugin ⭐ EMERGING

### Apa Ini?
Build MCP (Model Context Protocol) server yang extend Claude's capabilities → publish di marketplace. Ini market BARU dan masih sangat early.

### Kenapa Hidden Gem?
- MCP ecosystem baru mulai 2025 → 1,000+ servers di 2026
- OpenAI juga adopt MCP → massive market
- Market masih SANGAT early = low competition
- Kamu sudah pakai Claude Code = familiar dengan ecosystem

### Ide MCP Server

| MCP Server | Target User | Monetisasi |
|------------|------------|-----------|
| Stock market data fetcher | Traders/analysts | Subscription |
| SEO analyzer | Content creators | Per-use |
| Database query optimizer | Developers | Subscription |
| Email drafter/sender | Business users | Per-use |
| Social media scheduler | Marketers | Subscription |
| Invoice generator | Freelancers | Per-use |

### Setup dari Terminal
```bash
# 1. Claude Code bikin MCP server
mkdir ~/projects/mcp-server
# Ikuti MCP protocol spec

# 2. Test locally
# Add ke Claude Code config

# 3. Publish ke marketplace
# - claudemarketplaces.com
# - mcpmarket.com
# - claudecodemarketplace.net

# 4. Monetisasi via Gumroad/Stripe integration
```

### Earnings Potential
Belum ada data pasti karena market sangat baru. Tapi potensi besar mengingat:
- Claude punya jutaan users
- Setiap MCP server = tool baru untuk Claude
- First-mover advantage SANGAT besar di early market

---

## Stream #17: Discord Bot Premium

### Apa Ini?
Build Discord bot → monetisasi via premium features, Server Subscriptions (90/10 split), atau sell bot licenses.

### Setup dari Terminal
```bash
# 1. Create bot di Discord Developer Portal (1x)
# 2. Claude Code bikin bot (Python discord.py)
pip install discord.py

# 3. Deploy via Docker
docker build -t discord-bot .
docker run -d --restart always discord-bot

# 4. Monetisasi:
# - Discord Server Subscriptions (90% ke kamu)
# - Premium commands (via Stripe)
# - Sell bot licenses ($50-500)
```

### Revenue: 90/10 split = paling creator-friendly platform

---

## Ranking Hidden Gems by "Bisa Langsung dari Claude Code" Score

| # | Stream | Terminal Score | Pasif Score | Potensi/Hari |
|---|--------|--------------|-------------|-------------|
| 7 | **Polymarket Bot** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $10-800 |
| 8 | **Sell Datasets** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $5-50 |
| 9 | **Telegram Bot** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $5-100 |
| 10 | **AI Prompts** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $5-30 |
| 11 | **SaaS Boilerplate** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $10-100 |
| 12 | **Chrome Extension** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $5-300 |
| 13 | **Notion Templates** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $5-50 |
| 14 | **Hummingbot** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $10-500 |
| 15 | **Newsletter** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $5-50 |
| 16 | **MCP Server** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | $5-100 |
| 17 | **Discord Bot** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $5-50 |

---

## Combined Total (Semua 17 Stream)

### Konservatif (Bulan 6+)

| Category | Streams | Income/Bulan |
|----------|---------|-------------|
| Bandwidth (money4band + Mysterium) | #1, #2 | $20-80 |
| Content (Cron + Newsletter) | #3, #15 | $100-500 |
| Products (API + Scraper + Boilerplate + Prompts + Templates) | #4, #5, #10, #11, #13 | $300-5,000 |
| Bots (Telegram + Discord) | #9, #17 | $100-1,000 |
| Trading (Polymarket + Hummingbot) | #7, #14 | $200-5,000 |
| Extension + MCP | #12, #16 | $100-2,000 |
| Data Service | #8 | $50-500 |
| Print-on-Demand | #6 | $50-500 |
| **TOTAL** | | **$920-14,580/bulan** |

### Prioritas Eksekusi (ROI vs Effort)

**Tier 1 — Quick Setup, Immediate Income:**
1. money4band Docker (30 menit)
2. Mysterium Node (10 menit)
3. AI Prompts packs → Gumroad/PromptBase (2 jam)

**Tier 2 — Medium Setup, High ROI:**
4. SaaS Boilerplate → Gumroad (1 hari)
5. Cron Content + Affiliate (3 jam)
6. Telegram Bot (4-8 jam)
7. Sell Datasets (2-4 jam)

**Tier 3 — Bigger Setup, Biggest Potential:**
8. RapidAPI (3-5 jam)
9. Apify Scraper (5-8 jam)
10. Chrome Extension (1-2 hari)
11. MCP Server (4-8 jam)

**Tier 4 — Butuh Modal, Highest Returns:**
12. Polymarket Bot (butuh USDC)
13. Hummingbot (butuh crypto di exchange)

---

## Links ke Plan Sebelumnya

- **Part 1 (Stream #1-6):** [2026-03-13-passive-income-terminal-plan.md](./2026-03-13-passive-income-terminal-plan.md)
- **Part 2 (Stream #7-17):** File ini

---

## Sources

- Polymarket Agents: https://github.com/Polymarket/agents
- Polymarket Weather Bot Article: https://blog.devgenius.io/found-the-weather-trading-bots-quietly-making-24-000-on-polymarket
- Hummingbot: https://github.com/hummingbot/hummingbot
- PromptBase: https://promptbase.com/sell
- Gumroad API: https://gumroad.com/api
- Beehiiv: https://www.beehiiv.com
- Apify CLI: https://docs.apify.com/cli
- ExtensionPay: https://extensionpay.com
- MCP Market: https://mcpmarket.com
- Opendatabay: https://www.opendatabay.com
- Telegram Bot API: https://core.telegram.org/bots/api
- Discord Developer: https://discord.com/developers
- NOAA Weather API: https://www.weather.gov/documentation/services-web-api
