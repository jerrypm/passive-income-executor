# Docker Passive Income — Research Baru (2026-03-15)

## Yang SUDAH Jalan
- Honeygain (via money4band Docker)
- Watchtower (auto-update)

## Yang BELUM Dijalankan (Baru Ditemukan)

### Tier 1: Tanpa Modal, Pendapatan Lebih Besar

| App | Docker | Est. Earnings | Cara Kerja | Registrasi |
|-----|--------|---------------|------------|------------|
| **Mysterium (MystNodes)** | `docker run -d --cap-add NET_ADMIN -p 4449:4449 mysteriumnetwork/myst service` | **$1-30/bulan** (avg $25-30 di lokasi bagus) | Decentralized VPN — user bayar pakai MYST token buat pake bandwidth kamu | [mystnodes.com](https://mystnodes.com) |
| **Grass Network** | `docker run -d mrcolorrain/grass-node` | **Points → Token airdrop** (GRASS di Solana, sudah listing) | AI data pipeline — bandwidth kamu dipakai buat scrape web data untuk AI training | [grass.io](https://grass.io) |
| **Nodepay** | `docker run -d kellphy/nodepay` | **Points → Nodecoin (NC)** token airdrop | DePIN + AI bandwidth sharing | [nodepay.ai](https://nodepay.ai) |
| **Titan Network** | `docker run -d titannet/titan-node` | **Token rewards** (TNT) — tergantung bandwidth & uptime | IP leasing + storage + CDN node | [titannet.io](https://titannet.io) |
| **EarnApp** (Bright Data) | Via money4band/CashFactory | **$5-15/bulan** | Bandwidth → enterprise proxy (by Bright Data, legit company) | [earnapp.com](https://earnapp.com) |
| **Peer2Profit** | Via money4band/CashFactory | **$3-10/bulan** | Bandwidth sharing for businesses | [peer2profit.com](https://peer2profit.com) |
| **ProxyRack** | Via money4band/CashFactory | **$4-8/bulan** | Residential proxy network | [proxyrack.com](https://proxyrack.com) |
| **Bitping** | `docker run mrcolorrain/bitping` | **$2-5/bulan** (crypto) | Network monitoring & testing | [bitping.com](https://bitping.com) |
| **PacketStream** | Via money4band | **$1-5/bulan** | Bandwidth marketplace | [packetstream.io](https://packetstream.io) |
| **Repocket** | Via money4band | **$2-5/bulan** | Bandwidth sharing | [repocket.com](https://repocket.com) |

### Tier 2: Butuh Modal/GPU, Pendapatan Jauh Lebih Besar

| App | Requirement | Est. Earnings | Cara Kerja |
|-----|-------------|---------------|------------|
| **Flux Nodes** | Collateral: 1000-40000 FLUX (~$50-2000) | **$50-500/bulan** tergantung tier | Cloud compute + hosting, 3 tiers (Cumulus/Nimbus/Stratus) |
| **Render Network** | GPU (minimal RTX 3060) | **$50-300/bulan** | GPU rendering untuk AI/3D artists |
| **Akash Network** | Compute resources | **Variable** | Decentralized cloud compute marketplace |
| **Presearch Node** | Stake 4000 PRE (~$80-200) | **$5-20/bulan** PRE tokens | Decentralized search engine |

### Docker Stacks (Jalankan Banyak App Sekaligus)

| Stack | GitHub | Apps Included |
|-------|--------|---------------|
| **money4band** (sudah punya) | MRColorR/money4band | Honeygain, EarnApp, Pawns, PacketStream, Peer2Profit, Repocket, Proxyrack, Bitping, PacketShare |
| **CashFactory** | OlivierGaland/CashFactory | Honeygain, EarnApp, Pawns, PacketStream, Peer2Profit |
| **earning-machine** | jf-m/earning-machine | Bitping, ProxyRack, dll |
| **InternetIncome** | engageub/InternetIncome | Multi-proxy, multi-IP support |

## Estimasi Total Kalau Jalankan Semua

### Bandwidth Sharing Stack (Tanpa Modal):
- Honeygain: $5-10/bulan ✅ sudah jalan
- EarnApp: $5-15/bulan
- Peer2Profit: $3-10/bulan
- ProxyRack: $4-8/bulan
- Bitping: $2-5/bulan
- PacketStream: $1-5/bulan
- Repocket: $2-5/bulan
- Pawns.app: $3-8/bulan
- **Subtotal: $25-66/bulan** (dari 1 IP residential)

### DePIN/AI Nodes (Tanpa Modal):
- Mysterium: $10-30/bulan
- Grass: Token airdrop (GRASS ~$1-2, potensi besar)
- Nodepay: Token airdrop
- Titan: Token rewards
- **Subtotal: $10-30/bulan + token upside**

### TOTAL POTENSI: **$35-96/bulan** dari 1 mesin Docker

## Action Plan — Yang Perlu Dilakukan

### Step 1: Tambah apps di money4band yang belum aktif
```bash
cd services/money4band
# Edit .env — tambah credentials EarnApp, Peer2Profit, ProxyRack, Bitping, PacketStream, Repocket
docker compose up -d
```

### Step 2: Setup Mysterium Node (pendapatan terbesar)
```bash
docker run --cap-add NET_ADMIN -d -p 4449:4449 --name myst \
  -v myst-data:/var/lib/mysterium-node \
  mysteriumnetwork/myst:latest service \
  --agreed-terms-and-conditions
# Buka http://localhost:4449 untuk setup wallet
```

### Step 3: Setup Grass Node
```bash
# Register di grass.io dulu, dapat email + password
docker run -d --name grass \
  -e GRASS_USER=your_email \
  -e GRASS_PASS=your_password \
  mrcolorrain/grass-node
```

### Step 4: Setup Nodepay
```bash
# Register di nodepay.ai, dapat token dari browser extension
docker run -d --name nodepay \
  -e NP_TOKEN=your_token \
  kellphy/nodepay
```

### Step 5: Setup Titan Network
```bash
docker run -d --name titan-node \
  -v titan-data:/root/.titanedge \
  -p 1234:1234 \
  titannet/titan-edge
# Bind device code di dashboard titannet.io
```

## Catatan Penting
- Semua bisa jalan BERSAMAAN di 1 mesin (Mac Mini)
- Bandwidth sharing apps compete untuk bandwidth yang sama, tapi tetap worth it
- DePIN nodes (Mysterium, Grass, Nodepay, Titan) punya token upside selain earning reguler
- Mysterium paling proven & bayaran paling gede untuk bandwidth
- Grass punya potensi airdrop besar (backed by Polychain Capital)
