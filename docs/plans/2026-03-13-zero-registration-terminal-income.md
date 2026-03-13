# Zero Registration: Pure Terminal Income (Part 3)

> **Tanggal:** 2026-03-13
> **Konteks:** Deep research — income streams yang bisa dijalankan 100% dari terminal TANPA register ke platform apapun
> **Prinsip:** Hanya butuh generate wallet/keys lokal dari CLI. Tidak ada signup, tidak ada KYC, tidak ada browser.
> **Target:** Filter dari 30+ opsi → yang BENAR-BENAR bisa jalan tanpa registrasi

---

## Honest Disclaimer

Hampir semua cara menghasilkan uang di internet butuh registrasi di suatu tempat. Yang benar-benar "zero registration" terbatas pada:
1. **Crypto mining** — generate wallet lokal, mine langsung
2. **Blockchain staking/validating** — bond token on-chain, earn rewards
3. **Decentralized networks** — run node, earn token dari network
4. **Self-hosted services** — host sendiri, terima crypto langsung
5. **Peer-to-peer protocols** — Nostr, Lightning Network

---

## Master List: TRULY Zero Registration

| # | Stream | Modal | macOS? | Earning/Bulan | Zero-Reg Score |
|---|--------|-------|--------|---------------|----------------|
| 1 | Golem Network (jual compute) | $0 | ❌ Linux | $1-30 | 10/10 |
| 2 | Solana CLI Staking | SOL tokens | ✅ | 6-9% APY | 10/10 |
| 3 | Cosmos (ATOM) Staking | ATOM tokens | ✅ | 9-19% APY | 10/10 |
| 4 | Lightning Network Node | BTC | ✅ | $1-300 | 9/10 |
| 5 | BTCPay Server + Digital Products | $0 | ✅ | Tergantung sales | 10/10 |
| 6 | Ollama AI Inference + Lightning | $0 | ✅ | $10-100 | 8/10 |
| 7 | Nostr Relay + Zaps | $0 | ✅ | $0-50 | 9/10 |
| 8 | Monero P2Pool Mining | $0 | ✅ | -$2 (RUGI) | 10/10 |
| 9 | Nym Mixnode | ~$0.20 (100 NYM) | VPS | $1-10 | 10/10 |
| 10 | Sentinel dVPN Node | ~$1 (50 DVPN) | VPS | $1-5 | 10/10 |
| 11 | PKT Network Mining | $0 | ✅ | $0.10-2 | 10/10 |
| 12 | Flux Node | $57+ (FLUX) | VPS Linux | $0-5 | 10/10 |
| 13 | Bittensor (TAO) Mining | Small TAO fee | Partial | $100-1000+ | 8/10 |
| 14 | Ethereum Solo Staking | 32 ETH (~$80K) | ✅* | $270-380 | 10/10 |

*ETH staking butuh 24/7 uptime, Mac bukan ideal

---

## ⭐ TIER 1: Bisa Mulai SEKARANG, $0 Modal

### Stream #1: Golem Network — Jual CPU Power

**Apa ini?** Rent out CPU compute kamu ke Golem decentralized marketplace. Orang bayar kamu dalam GLM token untuk menjalankan task di komputer kamu.

**⚠️ CATATAN: Linux only.** macOS TIDAK didukung untuk provider. Butuh VPS Linux ($3-5/bulan) atau dual-boot.

```bash
# Di Linux VPS atau mesin Linux:
# 1. Install Golem provider
curl -sSf https://join.golem.network/as-provider | bash

# 2. Wallet auto-generated lokal (ZERO signup)
# Atau provide ETH address sendiri

# 3. Jalankan provider
golemsp run

# 4. Cek status & earnings
golemsp status
```

**Earnings:** $1-30/bulan (CPU only). GPU providers bisa $300-800/bulan tapi butuh NVIDIA.
**Verdict:** Truly zero registration, tapi butuh Linux. Jika punya VPS $5/bulan, bisa profit $0-25/bulan.

**Links:**
- Docs: https://docs.golem.network/docs/providers/provider-installation
- Site: https://golem.network

---

### Stream #2: Monero P2Pool Mining (Educational Only)

**Apa ini?** Mine Monero (XMR) lewat P2Pool — fully decentralized mining pool tanpa registrasi apapun. Wallet di-generate lokal.

```bash
# 1. Install dependencies
brew install cmake libuv openssl hwloc

# 2. Build XMRig dari source
git clone https://github.com/xmrig/xmrig.git
cd xmrig && mkdir build && cd build
cmake .. -DOPENSSL_ROOT_DIR=$(brew --prefix openssl)
make -j$(sysctl -n hw.logicalcpu)

# 3. Download & run Monero daemon (untuk P2Pool)
# Download dari getmonero.org/downloads
./monerod --zmq-pub tcp://127.0.0.1:18083

# 4. Generate wallet LOKAL (zero signup)
./monero-wallet-cli --generate-new-wallet=mywallet

# 5. Download & run P2Pool (NO registration)
# Download dari github.com/SChernykh/p2pool/releases
./p2pool --host 127.0.0.1 --wallet YOUR_MONERO_ADDRESS

# 6. Point XMRig ke local P2Pool
./xmrig -o 127.0.0.1:3333
```

**Hashrate Mac:**
| Chip | Hashrate | Earning/Bulan |
|------|----------|---------------|
| M1 | ~1,500-2,500 H/s | ~$0.50-1.00 |
| M2 | ~2,000-3,000 H/s | ~$0.75-1.50 |
| M3/M4 | ~7,000-10,000 H/s | ~$1.50-2.00 |

**Electricity cost:** ~$3.30/bulan → **RUGI di Mac.**

**Verdict:** 10/10 zero-registration, tapi TIDAK profitable di Mac. Hanya untuk edukasi/eksperimen.

**Links:**
- P2Pool: https://p2pool.io
- XMRig: https://github.com/xmrig/xmrig
- Monero CLI: https://www.getmonero.org/resources/user-guides/monero-wallet-cli.html

---

### Stream #3: PKT Network Mining

**Apa ini?** Bandwidth mining protocol. Mine PKT token dengan CPU — wallet generated lokal.

```bash
# 1. Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 2. Build PacketCrypt
git clone https://github.com/pkt-cash/pktd.git
cd pktd
cargo build --release

# 3. Generate wallet lokal (embedded dalam pktd)
./target/release/pktd wallet create

# 4. Mine (announcement mining)
./target/release/packetcrypt ann -p <YOUR_PKT_WALLET_ADDRESS> pool1 pool2 pool3
```

**Earnings:** Sangat rendah di 2025-2026. PKT price depressed. ~$0.10-2/bulan.
**Verdict:** Truly zero registration. Tapi earnings hampir nol.

---

## ⭐ TIER 2: Butuh Crypto, Tapi ZERO Registration

### Stream #4: Solana CLI Staking

**Apa ini?** Generate Solana wallet dari terminal → stake SOL → earn 6-9% APY. Semua dari CLI.

```bash
# 1. Install Solana CLI
sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"

# 2. Generate wallet LOKAL (zero signup)
solana-keygen new

# 3. Cek balance (setelah kirim SOL ke wallet)
solana balance

# 4. Create stake account & delegate
solana create-stake-account stake-account.json 10 --from keypair.json
solana delegate-stake stake-account.json <VALIDATOR_VOTE_ACCOUNT>

# 5. Cek rewards
solana stake-account stake-account.json
```

**Earnings:**
| SOL Staked | APY | Earning/Bulan |
|-----------|-----|---------------|
| 10 SOL (~$1,500) | 6-9% | ~$7.5-11.25 |
| 50 SOL (~$7,500) | 6-9% | ~$37.5-56.25 |
| 100 SOL (~$15,000) | 6-9% | ~$75-112.50 |

**Rewards dibayar setiap epoch (~2-3 hari).**
**Verdict:** 10/10 zero-registration. Wallet dari `solana-keygen new`. Tapi butuh beli SOL dulu.

**Links:**
- Solana Staking: https://solana.com/docs/references/staking
- Validator list: https://www.validators.app

---

### Stream #5: Cosmos (ATOM) CLI Staking

**Apa ini?** Stake ATOM dari CLI. APY lebih tinggi dari Solana (9-19%).

```bash
# 1. Install gaiad
git clone https://github.com/cosmos/gaia.git
cd gaia && make install

# 2. Generate keys LOKAL (zero signup)
gaiad keys add myvalidator

# 3. Delegate ATOM ke validator
gaiad tx staking delegate <VALIDATOR_ADDRESS> 1000000uatom \
  --from myvalidator \
  --chain-id cosmoshub-4

# 4. Claim rewards
gaiad tx distribution withdraw-rewards <VALIDATOR_ADDRESS> \
  --from myvalidator
```

**Earnings:**
| ATOM Staked | APY | Earning/Bulan |
|------------|-----|---------------|
| 100 ATOM (~$500) | 9-19% | ~$3.75-7.90 |
| 500 ATOM (~$2,500) | 9-19% | ~$18.75-39.50 |
| 1000 ATOM (~$5,000) | 9-19% | ~$37.50-79 |

**Unbonding period: 21 hari.**
**Verdict:** 10/10 zero-registration. Butuh beli ATOM.

---

### Stream #6: Bitcoin Lightning Network Routing Node

**Apa ini?** Jalankan Bitcoin + Lightning node. Earn routing fees saat payment lewat channel kamu.

```bash
# 1. Install Bitcoin Core
brew install bitcoin

# 2. Start Bitcoin Core (download ~600GB blockchain)
bitcoind -daemon

# 3. Create wallet LOKAL (zero signup)
bitcoin-cli createwallet "mywalletname"
bitcoin-cli getnewaddress

# 4. Install LND (Lightning Network Daemon)
# Download dari github.com/lightningnetwork/lnd/releases

# 5. Start LND
lnd --bitcoin.active --bitcoin.mainnet --bitcoin.node=bitcoind

# 6. Create Lightning wallet (lokal)
lncli create

# 7. Open channels & set fees
lncli openchannel --node_key=<PEER_PUBKEY> --local_amt=<SATS>
lncli updatechanpolicy --base_fee_msat 1000 --fee_rate 0.000001
```

**Earnings:**
| BTC in Channels | Routing/Hari | Profit/Bulan |
|----------------|-------------|--------------|
| 0.1 BTC (~$6K) | ~10-50 sats | $1-10 |
| 1 BTC (~$60K) | ~500-2,000 sats | $10-50 |
| 10 BTC (~$600K) | ~30,000 sats | $100-300 |

**Catatan:**
- Butuh download full blockchain (~600GB)
- Butuh BTC untuk open channels
- Tool `charge-lnd` bisa auto-optimize fees
- Satu operator butuh 4 tahun dari -497% ke +63% profit

**Verdict:** 9/10 zero-registration. Butuh modal BTC signifikan untuk meaningful income.

**Links:**
- LND: https://github.com/lightningnetwork/lnd
- Docs: https://docs.lightning.engineering

---

## ⭐ TIER 3: Self-Hosted Monetization (Build Once, Earn Forever)

### Stream #7: BTCPay Server + Jual Digital Products

**Apa ini?** Self-hosted payment processor. Terima Bitcoin/Lightning untuk jual apapun — TANPA third-party, TANPA fees ke platform.

```bash
# 1. Clone BTCPay Server
git clone https://github.com/btcpayserver/btcpayserver-docker
cd btcpayserver-docker

# 2. Configure (zero registration anywhere)
export BTCPAY_HOST="yourdomain.com"  # atau IP
export NBITCOIN_NETWORK="mainnet"
export BTCPAYGEN_CRYPTO1="btc"
export BTCPAYGEN_LIGHTNING="clightning"
export BTCPAYGEN_REVERSEPROXY="nginx"

# 3. Launch
. ./btcpay-setup.sh -i

# 4. BTCPay auto-generate wallet lokal
# Bisa langsung buat invoice & terima pembayaran
```

**Apa yang bisa dijual:**
| Product | Harga | Delivery |
|---------|-------|----------|
| Starter kit / boilerplate code | 0.001-0.005 BTC | GitHub access / zip |
| AI prompt packs | 0.0005 BTC | PDF download |
| API access tokens | 0.0001 BTC/bulan | Auto-generated key |
| Obsidian/Notion templates | 0.0003 BTC | File download |
| Web scraper scripts | 0.001 BTC | Code delivery |

**Verdict:** 10/10 zero-registration. Tapi butuh domain/VPS dan marketing sendiri.

**Links:**
- BTCPay: https://github.com/btcpayserver/btcpayserver
- Docs: https://docs.btcpayserver.org

---

### Stream #8: Ollama AI Inference + Lightning Payments ⭐ HIDDEN GEM

**Apa ini?** Jalankan LLM lokal (Llama, DeepSeek, dll) → expose API → orang bayar per query via Lightning. Privacy-focused AI inference = ada demand nyata.

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull model
ollama pull llama3.2
ollama pull deepseek-r1
ollama pull codellama

# 3. Ollama serve OpenAI-compatible API di localhost:11434
# Test:
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.2","messages":[{"role":"user","content":"Hello"}]}'

# 4. Expose via reverse proxy (caddy/nginx)
# + Payment gating via BTCPay Server atau LNbits (self-hosted)

# 5. Wrap dengan script: cek Lightning invoice paid → serve inference
# Claude Code bisa bikin wrapper ini
```

**Kenapa ada demand?**
- Privacy-focused users mau AI tanpa logging
- Uncensored models (tidak bisa di cloud)
- Cheaper than OpenAI untuk bulk queries
- Developer testing tanpa rate limits

**Pricing model:**
| Model | Cost/Query | Charge/Query | Margin |
|-------|-----------|-------------|--------|
| llama3.2 | ~$0 (lokal) | $0.001-0.01 | 100% |
| deepseek-r1 | ~$0 (lokal) | $0.005-0.02 | 100% |
| codellama | ~$0 (lokal) | $0.002-0.01 | 100% |

**Earnings:** $10-100/bulan tergantung marketing & demand.
**Verdict:** 8/10. Semua self-hosted. Tapi perlu advertise endpoint (bisa via Nostr).

---

### Stream #9: Nostr Relay + Content + Zaps

**Apa ini?** Nostr = protocol sosial media TANPA registrasi. Generate keypair lokal → post content → terima Lightning tips (zaps) dari followers.

```bash
# === OPTION A: Post Content, Earn Zaps ===

# 1. Generate Nostr keypair LOKAL (zero signup)
pip install nostr
python3 -c "
from nostr.key import PrivateKey
pk = PrivateKey()
print(f'Private key (nsec): {pk.bech32()}')
print(f'Public key (npub): {pk.public_key.bech32()}')
"

# 2. Setup Lightning address via Ligess (self-hosted)
git clone https://github.com/nicklord/ligess.git
# Configure dengan LND node kamu

# 3. Post content via CLI
# Atau pakai nostr-commander-rs
cargo install nostr-commander-rs
nostr-commander --publish "Your content here"

# === OPTION B: Run Paid Relay ===

# 1. Install strfry relay
git clone https://github.com/hoytech/strfry.git
cd strfry && make setup-golpe && make -j4

# 2. Configure paid access (charge sats untuk publish)
# Edit strfry.conf

# 3. Run relay
./strfry relay
```

**Nostr Zap Stats (2025):**
- 5 juta+ zaps sudah terjadi
- Growing rapidly
- Content creators earning real sats

**Earnings:**
| Activity | Effort | Income/Bulan |
|---------|--------|-------------|
| Post content daily + zaps | 30 min/hari | $5-50 |
| Run paid relay | Setup once | $0-20 |
| Both combined | | $5-70 |

**Verdict:** 9/10 zero-registration. Keypair generated lokal. Butuh build audience.

**Links:**
- Nostr: https://nostr.com
- strfry relay: https://github.com/hoytech/strfry
- Ligess: https://github.com/nicklord/ligess

---

## ⭐ TIER 4: Decentralized Network Nodes (Butuh VPS)

### Stream #10: Nym Mixnode (Privacy Infrastructure)

**Apa ini?** Jalankan mixnode di Nym privacy network. Earn NYM tokens untuk routing encrypted traffic.

```bash
# 1. Download nym-node binary
# Dari github.com/nymtech/nym/releases

# 2. Init & run (wallet auto-generated)
./nym-node run --mode mixnode

# 3. Bond 100+ NYM on-chain (very cheap, ~$0.20)
# Via nym wallet CLI

# 4. Node masuk rewarded set jika uptime bagus
```

**Requirements:** VPS Linux recommended ($5/bulan) untuk uptime 24/7.
**Bond:** 100 NYM (~$0.20) — hampir gratis.
**Earnings:** $1-10/bulan (depends on network demand & stake).

**Verdict:** 10/10 zero-registration. Sangat murah untuk masuk.

**Links:**
- Docs: https://nym.com/docs/operators/nodes
- GitHub: https://github.com/nymtech/nym

---

### Stream #11: Sentinel dVPN Node

**Apa ini?** Jalankan VPN node di Sentinel decentralized network. Kamu set harga sendiri per GB.

```bash
# 1. Run via Docker (di VPS Linux)
docker pull sentinel-official/dvpn-node

# 2. Configure — set price per GB, wallet auto-generated
# Edit config file

# 3. Start node
docker run -d sentinel-official/dvpn-node

# 4. Minimum balance: ~50 DVPN di node account (~$1)
```

**Earnings:** $1-5/bulan (historically low, tapi Sentinel targeting growth di 2025-2026).
**Verdict:** 10/10 zero-registration. Privacy-first. Tapi low earnings saat ini.

**Links:**
- Docs: https://docs.sentinel.co/dvpn-node-setup
- GitHub: https://github.com/sentinel-official/dvpn-node

---

### Stream #12: Bittensor (TAO) Subnet Mining ⭐ HIGH POTENTIAL

**Apa ini?** Contribute AI compute ke Bittensor subnets. Earn TAO tokens. Market untuk decentralized AI.

```bash
# 1. Install Bittensor
pip install bittensor

# 2. Create wallet LOKAL (zero signup)
btcli wallet create --wallet.name mywallet

# 3. Register on subnet (small TAO fee, on-chain)
btcli subnet register --wallet.name mywallet --subtensor.network finney

# 4. Run miner (specific per subnet)
# Subnet 1: text prompting
# Subnet 3: data scraping
# Subnet 8: time-series prediction
# dll.
```

**Earnings:** SANGAT variable.
| Tier | TAO/Hari | USD/Bulan |
|------|---------|-----------|
| Top miners | 1-10 TAO | $300-3,000+ |
| Mid miners | 0.1-1 TAO | $30-300 |
| Low miners | 0.01-0.1 TAO | $3-30 |

**Catatan:** Beberapa subnet butuh GPU. Tapi ada subnet yang CPU-friendly.
**Verdict:** 8/10 zero-registration. High potential tapi complex setup.

**Links:**
- Docs: https://docs.learnbittensor.org
- Site: https://bittensor.com

---

## YANG TERNYATA BUTUH REGISTRASI (Jangan Tertipu)

| Project | Apa yang mereka sembunyikan |
|---------|---------------------------|
| **Mysterium** | Butuh signup di mystnodes.com + $1 deposit |
| **Storj** | Butuh email untuk auth token |
| **Render Network** | Butuh waitlist approval di renderfoundation.com |
| **Grass** | Butuh account signup di grass.io |
| **Pipe Network** | Butuh email + onboarding |
| **Filecoin Saturn** | Butuh email + Linux server + 10Gbps |

---

## YANG ZERO-REG TAPI ZERO EARNINGS (Volunteer Only)

| Project | macOS | Earnings |
|---------|-------|---------|
| **Tor Relay** | ✅ | $0 — purely volunteer |
| **I2P Router** | ✅ | $0 — purely volunteer |
| **IPFS Node** | ✅ | $0 — no native incentive |
| **Celestia Light Node** | ✅ | $0 — light nodes tidak dapat reward |
| **Matrix Homeserver** | ✅ | $0 — no rewards |

---

## Realistic Action Plan: Kombinasi Terbaik

### Kalau Punya $0 Modal (Hanya Mac + Terminal):

| Action | Waktu Setup | Expected/Bulan |
|--------|------------|----------------|
| Ollama AI inference + self-hosted LN payments | 3-5 jam | $10-100 |
| Nostr content + zaps | 1 jam setup + daily posting | $5-50 |
| BTCPay + jual digital products (prompts, templates, code) | 4-8 jam | Depends on sales |
| **Total realistic** | | **$15-200/bulan** |

### Kalau Punya Crypto (~$500-2,000):

| Action | Waktu Setup | Expected/Bulan |
|--------|------------|----------------|
| Solana CLI staking ($1,500 SOL) | 10 menit | $7-11 |
| Cosmos ATOM staking ($1,000) | 15 menit | $7-16 |
| Nym Mixnode on VPS | 1 jam | $1-10 |
| Sentinel dVPN on VPS | 1 jam | $1-5 |
| + Tier $0 actions above | | $15-200 |
| **Total realistic** | | **$31-242/bulan** |

### Kalau Punya Crypto Signifikan (~$10K+):

| Action | Waktu Setup | Expected/Bulan |
|--------|------------|----------------|
| Lightning routing node (1 BTC) | 1 hari | $10-50 |
| Solana staking (50 SOL) | 10 menit | $37-56 |
| Cosmos staking (1000 ATOM) | 15 menit | $37-79 |
| Bittensor subnet mining | 4-8 jam | $30-300 |
| + Tier $0 & $500 actions | | $31-242 |
| **Total realistic** | | **$145-727/bulan** |

---

## Honest Assessment dari Indonesia 🇮🇩

**Kenyataan pahit:**
1. **Mining di Mac = RUGI.** Electricity cost > earnings untuk semua PoW coins.
2. **Bandwidth selling dari Indonesia = LOW.** Rate per GB jauh lebih rendah dari US/EU.
3. **Staking = paling reliable** tapi butuh modal crypto.
4. **Self-hosted AI inference = paling promising** karena demand growing dan zero overhead cost.
5. **Nostr + Lightning = emerging** tapi audience masih kecil.

**Rekomendasi paling realistis tanpa modal:**
1. **Ollama + BTCPay** — host AI inference, charge per query
2. **Nostr content** — post daily, build following, earn zaps
3. **Claude Code bikin digital products** → jual via BTCPay (prompts, templates, boilerplate)

**Rekomendasi dengan modal kecil ($500):**
1. **Solana staking** — paling straightforward, 6-9% APY
2. **VPS + Nym Mixnode** — $5/bulan VPS, earn NYM
3. **VPS + Golem provider** — jual CPU compute

---

## Perbandingan: Zero-Reg (Part 3) vs Butuh-Reg (Part 1 & 2)

| Aspek | Zero Registration | Butuh Registration |
|-------|------------------|-------------------|
| **Earning ceiling** | Lower ($15-727/bulan) | Higher ($920-14,580/bulan) |
| **Setup complexity** | Higher (crypto, nodes, self-host) | Lower (signup + deploy) |
| **Privacy** | Maksimal | Minimal (email, KYC) |
| **Payment** | Crypto only | PayPal, bank, Stripe |
| **Maintenance** | Varies | Generally lower |
| **Legal risk** | Lower (permissionless) | Lower (regulated platforms) |

**Kesimpulan:** Zero-registration income itu MUNGKIN tapi earning ceiling jauh lebih rendah. Untuk maximize income, kombinasi **zero-reg passive streams (staking, nodes)** + **1-2 platform dengan registrasi (dev.to, Gumroad, RapidAPI)** adalah strategi terbaik.

---

## Links ke Plan Sebelumnya

- **Part 1 (Stream #1-6):** [2026-03-13-passive-income-terminal-plan.md](./2026-03-13-passive-income-terminal-plan.md)
- **Part 2 (Stream #7-17):** [2026-03-13-hidden-gems-terminal-income.md](./2026-03-13-hidden-gems-terminal-income.md)
- **Part 3 (Zero Registration):** File ini

---

## Sources

- P2Pool: https://p2pool.io
- XMRig: https://github.com/xmrig/xmrig
- Solana Staking: https://solana.com/docs/references/staking
- Cosmos Hub: https://hub.cosmos.network
- LND: https://github.com/lightningnetwork/lnd
- BTCPay Server: https://github.com/btcpayserver/btcpayserver
- Ollama: https://ollama.com
- Nostr: https://nostr.com
- strfry: https://github.com/hoytech/strfry
- Nym: https://nym.com/docs/operators/nodes
- Sentinel: https://docs.sentinel.co
- Bittensor: https://docs.learnbittensor.org
- Golem: https://docs.golem.network
- PKT: https://docs.pkt.cash
- Flux: https://wiki.runonflux.io
