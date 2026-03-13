# Passive Income dari Terminal / Claude Code

> **Tanggal:** 2026-03-13
> **Goal:** Setup multiple passive income streams yang bisa di-manage 100% dari terminal
> **Target:** $250-6,580/bulan (combined semua stream)
> **Prinsip:** Setup sekali → monitor uang masuk

---

## Daftar Semua Stream

| # | Stream | Target Income | Pasif Level | Setup Time | Modal |
|---|--------|---------------|-------------|------------|-------|
| 1 | money4band Docker | $15-50/bulan | ⭐⭐⭐⭐⭐ | 30 menit | $0 |
| 2 | Mysterium Node | $5-30/bulan | ⭐⭐⭐⭐⭐ | 10 menit | $0 |
| 3 | Cron Content + Affiliate | $30-500/bulan | ⭐⭐⭐⭐ | 2-3 jam | $0 |
| 4 | RapidAPI (Jual API) | $50-2,000/bulan | ⭐⭐⭐⭐ | 3-5 jam | $0 |
| 5 | Apify Store (Jual Scraper) | $100-5,000/bulan | ⭐⭐⭐⭐ | 5-8 jam | $1/bulan |
| 6 | Printify API (Print-on-Demand) | $50-500/bulan | ⭐⭐⭐⭐ | 3-5 jam | $0 |

---

## Stream #1: money4band Docker (Bandwidth Sharing Stack)

### Apa Ini?
Docker stack yang jalankan 15+ bandwidth sharing apps sekaligus dalam satu `docker compose`. Apps yang didukung:
- Honeygain, EarnApp, IPRoyal Pawns, PacketStream, Repocket, EarnFM, Proxyrack, ProxyLite, Bitping, Speedshare, Grass, PacketShare, Gradient, MystNode, Dawn, Teneo, ProxyBase, Wipter, TraffMonetizer

### Earnings Realistis
| Lokasi IP | Per Bulan |
|-----------|-----------|
| US/EU | $50-200 |
| **Indonesia** | **$15-50** |

### Prasyarat
- [x] macOS dengan Docker Desktop terinstall
- [ ] Daftar akun di setiap platform (1x saja, perlu browser)
- [ ] Catat semua email/token/device ID

### Akun yang Perlu Didaftarkan

| App | URL Registrasi | Yang Dicatat |
|-----|---------------|--------------|
| Honeygain | https://www.honeygain.com | Email + password |
| EarnApp | https://earnapp.com | Google account → device ID |
| Pawns (IPRoyal) | https://pawns.app | Email + password |
| PacketStream | https://packetstream.io | Email + password |
| Repocket | https://repocket.co | Email + API key |
| EarnFM | https://earn.fm | Email + password |
| Bitping | https://bitping.com | Email + password |
| Grass | https://grass.io | Email + password |
| TraffMonetizer | https://traffmonetizer.com | Email + device token |
| PacketShare | https://packetshare.io | Email + password |

### Setup dari Terminal

```bash
# Step 1: Clone repo
git clone https://github.com/MRColorR/money4band.git
cd money4band

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Jalankan guided setup (masukkan token dari tiap app)
python3 main.py

# Step 4: Start semua apps
docker compose up -d

# Step 5: Cek status
docker compose ps

# Step 6: Monitor dashboard
# Buka localhost di browser untuk web dashboard
```

### Maintenance
- **Effort setelah setup:** NOL
- Docker containers auto-restart
- money4band punya auto-updater built-in

### Scaling Options
- Jalankan di Mac + HP + perangkat lain (lebih banyak device = lebih banyak earnings)
- Sewa VPS US ($3-5/bulan) untuk IP US → 10x rate
  - ⚠️ Beberapa apps detect datacenter IP dan tidak bayar

---

## Stream #2: Mysterium Node (Decentralized VPN)

### Apa Ini?
Kamu jadi node di jaringan VPN decentralized. Orang pakai internet lewat koneksi kamu → kamu dibayar token MYST (bisa convert ke USD).

### Bedanya dari money4band
- Decentralized VPN network → demand lebih tinggi
- Bayaran per GB lebih besar
- Legal framework yang melindungi node runner

### Earnings Realistis
| Skenario | Per Bulan |
|----------|-----------|
| 1 node di Mac (Indonesia IP) | $5-20 |
| 1 node di VPS US ($5/bulan) | $15-30 → profit $10-25 |
| 5 node di VPS berbeda | $50-125 |

### Prasyarat
- [x] Docker terinstall
- [ ] Wallet crypto (untuk terima MYST token)

### Setup dari Terminal

```bash
# Step 1: Pull image
docker pull mysteriumnetwork/myst:latest

# Step 2: Jalankan node
docker run --cap-add NET_ADMIN -d -p 4449:4449 \
  --name myst \
  -v myst-data:/var/lib/mysterium-node \
  mysteriumnetwork/myst:latest service --agreed-terms-and-conditions

# Step 3: Cek node status
curl http://localhost:4449/healthcheck

# Step 4: Monitor earnings
# Dashboard di http://localhost:4449
```

### Maintenance
- **Effort setelah setup:** NOL
- Node jalan 24/7 selama Docker running
- Withdraw MYST ke wallet kapan saja

### Catatan
- MYST token bisa di-convert ke USD via exchange
- Staking MYST bisa menambah rewards
- GitHub repo: https://github.com/mysteriumnetwork/node

---

## Stream #3: Cron Job Content + Affiliate Links

### Apa Ini?
Script otomatis yang generate artikel → publish ke dev.to & Hashnode via API → artikel berisi affiliate links → orang klik/beli → kamu dapat komisi.

### Flow

```
Cron (setiap hari jam 8 pagi)
  │
  ▼
Script baca topics.json → ambil topic berikutnya
  │
  ▼
Generate artikel markdown (dari template atau Claude API)
  │
  ▼
Inject affiliate links + CTA ke digital product
  │
  ▼
POST ke dev.to API → published ✅
POST ke Hashnode GraphQL → published ✅
  │
  ▼
Log hasil → update topics.json
```

### Earnings Realistis
| Timeline | Artikel Total | Estimasi Income |
|----------|---------------|-----------------|
| Bulan 1 | 30 | $0-10 (build audience) |
| Bulan 3 | 90 | $30-100/bulan |
| Bulan 6 | 180 | $100-500/bulan |
| Bulan 12 | 360 | $300-1,500/bulan |

> Uang datang dari affiliate links & digital products di dalam artikel, bukan dari platform-nya.

### Prasyarat
- [ ] Akun dev.to → API key dari dev.to/settings/extensions
- [ ] Akun Hashnode → Personal Access Token dari hashnode.com/settings/developer
- [ ] Daftar affiliate programs (lihat daftar di bawah)

### API Details

**dev.to:**
```bash
# Endpoint
POST https://dev.to/api/articles

# Headers
Content-Type: application/json
api-key: YOUR_DEVTO_API_KEY

# Body
{
  "article": {
    "title": "Judul Artikel",
    "body_markdown": "# Content...\n\n[Affiliate link](url)",
    "published": true,
    "tags": ["swift", "ios", "tutorial", "programming"]
  }
}
```

**Hashnode:**
```bash
# Endpoint
POST https://gql.hashnode.com

# Headers
Content-Type: application/json
Authorization: YOUR_HASHNODE_PAT

# Body (GraphQL mutation)
{
  "query": "mutation PublishPost($input: PublishPostInput!) { publishPost(input: $input) { post { id url } } }",
  "variables": {
    "input": {
      "title": "Judul Artikel",
      "contentMarkdown": "# Content...",
      "publicationId": "YOUR_PUB_ID",
      "tags": [{"name": "swift", "slug": "swift"}]
    }
  }
}
```

**Medium (manual workaround):**
- Medium API locked untuk token baru
- Workaround: publish ke dev.to dulu → import URL ke Medium via medium.com/me/stories → "Import a story"
- Medium otomatis set canonical URL

### Affiliate Programs untuk Niche iOS/Developer

| Program | Komisi | URL |
|---------|--------|-----|
| RevenueCat | 15% recurring | https://www.revenuecat.com/affiliates |
| Digital Ocean | $200 per referral | https://www.digitalocean.com/referral |
| Namecheap | 20-50% | https://www.namecheap.com/affiliates |
| Udemy | 15% per sale | https://www.udemy.com/affiliate |
| Hostinger | 60% per sale | https://www.hostinger.com/affiliates |

### Setup Cron Job (macOS)

```bash
# Buat script publish.py (Claude Code buatkan)
# Letakkan di ~/scripts/content-machine/

# Setup cron
crontab -e

# Tambahkan baris:
0 8 * * * cd ~/scripts/content-machine && /usr/bin/python3 publish.py >> ~/scripts/content-machine/log.txt 2>&1
```

### Environment Variables (.env)

```bash
DEVTO_API_KEY=your_devto_api_key
HASHNODE_PAT=your_hashnode_pat
HASHNODE_PUB_ID=your_publication_id
```

### Maintenance
- **Effort setelah setup:** Minimal
- Perlu isi topics.json dengan topik baru secara berkala
- Atau batch generate 100+ topik sekaligus dari awal

### Keunggulan Kamu
- Sudah punya 40+ artikel SwiftUI di folder ini
- Bisa re-publish ke dev.to + Hashnode + sisipkan affiliate links

---

## Stream #4: RapidAPI — Jual API

### Apa Ini?
Build API sederhana → deploy ke hosting gratis → list di RapidAPI marketplace → orang subscribe & bayar per request → kamu terima uang.

### Contoh API yang Laku (Low Maintenance)

| API Idea | Effort Bikin | Potensi/Bulan |
|----------|-------------|---------------|
| QR Code Generator | 1 jam | $100-500 |
| Text-to-Speech | 2 jam | $200-1,000 |
| Image Compressor/Resizer | 1 jam | $100-300 |
| Currency Converter | 1 jam | $50-200 |
| Random Quote/Joke API | 30 menit | $50-150 |
| URL Shortener | 1 jam | $50-200 |
| PDF Generator | 2 jam | $200-500 |
| Markdown to HTML | 30 menit | $50-100 |
| Color Palette Generator | 1 jam | $50-150 |
| Lorem Ipsum Generator | 30 menit | $30-100 |

### Earnings Realistis
| Timeline | Income |
|----------|--------|
| Bulan 1-3 | $0-50 (build users) |
| Bulan 6 | $100-500/bulan |
| 1 tahun+ | $500-2,000/bulan |
| Top sellers | $5,000-20,000/bulan |

### Full Process dari Terminal

```bash
# Step 1: Claude Code bikin API (Python FastAPI)
mkdir ~/projects/my-api && cd ~/projects/my-api

# File: main.py (Claude Code generate)
# File: requirements.txt
# File: Dockerfile

# Step 2: Test locally
pip install -r requirements.txt
uvicorn main:app --reload

# Step 3: Push ke GitHub
git init && git add . && git commit -m "initial API"
gh repo create my-api --public --push

# Step 4: Deploy ke Render.com (gratis)
# - Connect GitHub repo di render.com dashboard (1x saja)
# - Auto-deploy setiap push

# Step 5: List di RapidAPI
# - Daftar di rapidapi.com/provider (1x saja)
# - Submit API URL + documentation
# - Set pricing tiers:
#   - Free: 100 requests/bulan
#   - Basic: $5/bulan — 10,000 requests
#   - Pro: $15/bulan — 100,000 requests
```

### Prasyarat
- [ ] Akun GitHub
- [ ] Akun Render.com (free tier)
- [ ] Akun RapidAPI (provider)

### Pricing Models
- **Pay Per Use:** Charge per API call (misal $0.001 per request)
- **Monthly Subscription:** $5-50/bulan per user tier
- **Freemium:** Free tier limited → paid tier unlimited

### Maintenance
- **Simple API (QR code, converter):** Hampir nol maintenance
- RapidAPI handle billing, user management, rate limiting, documentation
- Auto-deploy via GitHub → Render pipeline

### Tips
- Bikin 3-5 API berbeda untuk diversifikasi
- Target niche yang belum saturated di RapidAPI
- Claude Code bisa bikin semua API ini dalam 1 hari

---

## Stream #5: Apify Store — Jual Web Scraper

### Apa Ini?
Build web scraper/automation tool → publish ke Apify Store (marketplace 19,000+ tools) → orang jalankan tool kamu → kamu dapat 80% revenue.

### Top Earning Actors di Apify Store

| Target Scraper | Earning Top Actors |
|----------------|--------------------|
| Google Maps | $5,000-20,000/bulan |
| Instagram | $3,000-10,000/bulan |
| LinkedIn | $2,000-8,000/bulan |
| Amazon Products | $1,000-5,000/bulan |
| TikTok | $1,000-5,000/bulan |
| Yellow Pages | $500-2,000/bulan |
| Yelp Reviews | $500-2,000/bulan |
| Twitter/X | $500-3,000/bulan |

### Revenue Model
- **Revenue share:** 80% masuk ke developer
- **Pricing options:**
  - Pay-Per-Result (PPR): $1 per 1,000 results
  - Pay-Per-Event (PPE): charge per action
  - Rental: $X/bulan flat fee
- **Profit formula:** `(0.8 × revenue) - platform usage costs`

### Full Process dari Terminal

```bash
# Step 1: Install Apify CLI
npm install -g apify-cli

# Step 2: Login
apify login

# Step 3: Create scraper project
apify create my-scraper --template python-beautifulsoup
# atau
apify create my-scraper --template python-playwright

# Step 4: Claude Code bikin scraper logic
# Edit src/main.py

# Step 5: Test locally
apify run

# Step 6: Deploy ke Apify
apify push

# Step 7: Publish ke Store
# Set title, description, pricing di Apify Console
# (1x saja, bisa via API juga)
```

### Prasyarat
- [ ] Akun Apify ($1/bulan — first 6 bulan dapat $500 credit)
- [ ] Node.js + npm terinstall
- [ ] Python terinstall

### Maintenance
- **5-10 jam per 3 bulan** (fix kalau website target update HTML structure)
- Apify punya monitoring — kamu dapat notifikasi kalau scraper gagal

### Earnings Realistis
| Timeline | Income |
|----------|--------|
| Bulan 1-2 | $0-50 (build users) |
| Bulan 3-6 | $100-500/bulan |
| 1 tahun+ | $500-5,000/bulan |

### Tips
- Target website populer yang belum ada scraper-nya di Apify Store
- Bikin scraper yang solve real problem (lead generation, price monitoring, dll)
- Claude Code bisa bikin scraper dalam 1-2 jam

---

## Stream #6: Printify API — Print-on-Demand Otomatis

### Apa Ini?
Generate desain → upload ke Printify via API → auto-listing di Etsy/Shopify → orang beli → Printify print & kirim → kamu terima profit margin.

### Flow

```
Claude Code generate desain (via AI image tools)
  │
  ▼
Upload via Printify API → create product
  │
  ▼
Auto-publish ke Etsy/Shopify
  │
  ▼
Customer beli → Printify cetak & kirim
  │
  ▼
Profit masuk ke akun kamu
```

### Earnings Realistis
| Jumlah Desain | Estimasi/Bulan |
|---------------|----------------|
| 50 desain | $10-50 |
| 200 desain | $50-200 |
| 500+ desain | $200-500 |

### Process dari Terminal

```bash
# Step 1: Generate desain (Claude Code + AI image tool)
# Bisa pakai nano-banana skill atau DALL-E API

# Step 2: Upload product via Printify API
curl -X POST "https://api.printify.com/v1/shops/{shop_id}/products.json" \
  -H "Authorization: Bearer {PRINTIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cool SwiftUI Dev T-Shirt",
    "description": "Perfect for iOS developers",
    "blueprint_id": 6,
    "print_provider_id": 1,
    "variants": [...],
    "print_areas": [{"variant_ids": [...], "placeholders": [...]}]
  }'

# Step 3: Publish ke Etsy
curl -X POST "https://api.printify.com/v1/shops/{shop_id}/products/{product_id}/publish.json" \
  -H "Authorization: Bearer {PRINTIFY_TOKEN}" \
  -d '{"title": true, "description": true, "images": true, "variants": true, "tags": true}'
```

### Prasyarat
- [ ] Akun Printify (gratis)
- [ ] Akun Etsy (listing fee $0.20 per item)
- [ ] Printify API token

### Maintenance
- **Effort setelah setup:** Minimal
- Printify handle printing, shipping, customer service
- Kamu cuma perlu upload desain baru secara berkala

### Catatan Indonesia
- Printify support seller dari mana saja
- ⚠️ Etsy butuh setup payment yang mungkin perlu Payoneer dari Indonesia
- Alternatif: connect Printify ke Shopify (basic plan $29/bulan)

---

## Action Plan: Urutan Setup

### Minggu 1 — Quick Wins (Paling Cepat Jalan)
- [ ] **Setup money4band Docker** — 30 menit, langsung jalan
- [ ] **Setup Mysterium Node** — 10 menit, langsung jalan
- [ ] Daftar semua akun bandwidth apps (butuh browser, 1x saja)

### Minggu 2 — Content Machine
- [ ] Daftar dev.to + Hashnode + ambil API keys
- [ ] Daftar affiliate programs (RevenueCat, DO, Namecheap, dll)
- [ ] **Claude Code bikin publish.py script**
- [ ] Batch generate 30+ topics dari artikel SwiftUI yang sudah ada
- [ ] **Setup cron job** — auto publish setiap hari

### Minggu 3 — API Business
- [ ] Brainstorm 3-5 API ideas
- [ ] **Claude Code bikin API** (FastAPI + Dockerfile)
- [ ] Deploy ke Render.com
- [ ] List di RapidAPI dengan pricing tiers
- [ ] Repeat untuk API ke-2 dan ke-3

### Minggu 4 — Apify Scraper
- [ ] Riset scraper yang belum ada / kurang di Apify Store
- [ ] **Claude Code bikin scraper**
- [ ] Test + deploy via `apify push`
- [ ] Set pricing + publish ke Store

### Ongoing — Print-on-Demand (Kalau Sempat)
- [ ] Batch generate 50-100 desain
- [ ] Upload via Printify API
- [ ] Connect ke Etsy/Shopify

---

## Monitor Earnings

### Dashboard / Cara Cek

| Stream | Cara Monitor |
|--------|-------------|
| money4band | Web dashboard di localhost |
| Mysterium | http://localhost:4449 |
| dev.to | dev.to/dashboard |
| Hashnode | hashnode.com/analytics |
| RapidAPI | rapidapi.com/developer/dashboard |
| Apify | console.apify.com → analytics |
| Printify | printify.com/orders |

### Payment Methods

| Stream | Pembayaran |
|--------|-----------|
| money4band (apps) | PayPal, crypto (varies per app) |
| Mysterium | MYST token → exchange → USD |
| Affiliate links | PayPal, wire transfer (varies) |
| RapidAPI | Stripe → bank account |
| Apify | Wire transfer, PayPal |
| Printify/Etsy | Payoneer, bank transfer |

---

## Total Projected Income (Konservatif)

| Bulan | money4band | Mysterium | Content | RapidAPI | Apify | Printify | TOTAL |
|-------|-----------|-----------|---------|----------|-------|----------|-------|
| 1 | $15 | $5 | $0 | $0 | $0 | $0 | **$20** |
| 3 | $30 | $15 | $50 | $30 | $50 | $20 | **$195** |
| 6 | $40 | $20 | $200 | $150 | $300 | $100 | **$810** |
| 12 | $50 | $25 | $500 | $500 | $1,000 | $300 | **$2,375** |

> Ini estimasi **konservatif**. Beberapa stream (Apify, RapidAPI) bisa jauh lebih tinggi kalau produknya hit.

---

## Resources & Links

- money4band: https://github.com/MRColorR/money4band
- Mysterium Node: https://github.com/mysteriumnetwork/node
- dev.to API: https://developers.forem.com/api/v1
- Hashnode API: https://apidocs.hashnode.com
- RapidAPI Provider: https://rapidapi.com/provider
- Apify CLI: https://docs.apify.com/cli
- Printify API: https://developers.printify.com
- Render.com (free hosting): https://render.com
