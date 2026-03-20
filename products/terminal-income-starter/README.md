# Terminal Income Starter Kit

**Price: $9**

Everything you need to start earning passive income from your terminal. This kit covers three proven strategies: automated content publishing, crypto staking, and bandwidth sharing -- all managed from the command line.

---

## What You Get

- **6 production-ready scripts** across three income categories
- **Content publishing pipeline** that cross-publishes to dev.to, Hashnode, and Nostr simultaneously
- **Crypto staking helpers** for Solana (SOL) and Cosmos (ATOM) with wallet creation, delegation, and reward tracking
- **Bandwidth sharing setup** via Docker that earns money from unused internet bandwidth

## Features

- **One-command cross-publishing** — write once, publish to 3 platforms
- **dev.to API integration** — publish articles as drafts or go live instantly
- **Hashnode GraphQL API** — full article publishing with tags and slugs
- **Solana staking CLI** — create wallet, check balance, delegate stake, track rewards
- **Cosmos/ATOM staking CLI** — full delegation lifecycle including reward claims
- **Bandwidth sharing** — Docker-based passive income ($10-30/month)
- **No external Python dependencies** — pure standard library
- **All scripts work independently** — use what you need, skip the rest

## Included Files

### Content Machine

| File | Purpose |
|------|---------|
| `publish_devto.py` | Publish Markdown articles to dev.to |
| `publish_hashnode.py` | Publish articles to Hashnode via GraphQL |
| `publish_all.py` | Cross-publish to Nostr + dev.to + Hashnode in one command |

### Crypto Staking

| File | Purpose |
|------|---------|
| `solana_setup.sh` | Solana wallet creation, balance check, staking, rewards |
| `cosmos_setup.sh` | Cosmos/ATOM wallet, delegation, rewards, claiming |

### Bandwidth Sharing

| File | Purpose |
|------|---------|
| `money4band_setup.sh` | Clone and set up the money4band Docker stack |

## Quick Start

### Content Publishing

#### 1. Get your API keys

- **dev.to**: Go to https://dev.to/settings/extensions and generate an API key
- **Hashnode**: Go to https://hashnode.com/settings/developer and create a Personal Access Token

#### 2. Create a `.env` file

```env
# dev.to
DEVTO_API_KEY=your_devto_api_key_here

# Hashnode
HASHNODE_API_KEY=your_hashnode_token_here
HASHNODE_PUBLICATION_ID=your_publication_id_here
```

#### 3. Publish an article

```bash
# To dev.to (as draft)
python3 publish_devto.py --title "My Article" --file article.md --tags python,ai

# To dev.to (publish immediately)
python3 publish_devto.py --title "My Article" --file article.md --tags python,ai --publish

# To Hashnode
python3 publish_hashnode.py --title "My Article" --file article.md --tags python ai

# To ALL platforms at once
python3 publish_all.py --title "My Article" --file article.md --tags python,ai
```

### Crypto Staking

#### Solana (SOL)

```bash
# Check if Solana CLI is installed
bash solana_setup.sh check

# Create a wallet
bash solana_setup.sh create-wallet

# Check balance
bash solana_setup.sh balance

# Browse validators
bash solana_setup.sh list-validators

# Stake (after funding wallet)
bash solana_setup.sh stake 10 <validator_address>

# Check rewards
bash solana_setup.sh rewards
```

#### Cosmos (ATOM)

```bash
# Check if gaiad is installed
bash cosmos_setup.sh check

# Create wallet (save your mnemonic!)
bash cosmos_setup.sh create-wallet

# Check balance
bash cosmos_setup.sh balance

# Browse validators
bash cosmos_setup.sh list-validators

# Delegate (after funding wallet)
bash cosmos_setup.sh stake 1000000 cosmosvaloper1...

# Check & claim rewards
bash cosmos_setup.sh rewards
bash cosmos_setup.sh claim
```

### Bandwidth Sharing

```bash
# Install Docker first: https://docker.com

# Clone and set up money4band
bash money4band_setup.sh setup

# Register at the platforms (links shown after setup)
# Then run the interactive configuration
cd services/money4band
bash runme.sh

# Start earning
docker compose up -d

# Check status
bash money4band_setup.sh status
```

## Configuration

Create a `.env` file in the same directory as the scripts:

```env
# Content Publishing
DEVTO_API_KEY=your_devto_api_key
HASHNODE_API_KEY=your_hashnode_token
HASHNODE_PUBLICATION_ID=your_pub_id

# Nostr (optional, for cross-publishing via publish_all.py)
NOSTR_PRIVKEY=your_nostr_hex_privkey
NOSTR_PUBKEY=your_nostr_hex_pubkey
```

## Requirements

| Component | Requirement |
|-----------|-------------|
| Content publishing | Python 3.8+, API keys (free) |
| Solana staking | Solana CLI, SOL tokens |
| Cosmos staking | gaiad CLI, ATOM tokens |
| Bandwidth sharing | Docker Desktop |

## Revenue Potential

| Stream | Investment | Est. Monthly |
|--------|-----------|-------------|
| Content + affiliate links | Time only | $50-200 |
| Solana staking (100 SOL) | ~$2,000 | $10-15 |
| Cosmos staking (100 ATOM) | ~$500 | $3-5 |
| Bandwidth sharing | Electricity | $10-30 |
| **Combined** | | **$73-250** |

## Tips for Success

1. **Content is king** — publish consistently (3-5 articles/week) to build an audience
2. **Include affiliate links** — tools you genuinely use (hosting, SaaS, courses)
3. **Cross-publish everywhere** — same article, multiple platforms, maximum reach
4. **Staking is set-and-forget** — delegate once, rewards compound automatically
5. **Bandwidth sharing runs 24/7** — just keep your machine on

## FAQ

**Do I need crypto to start?**
No. Content publishing and bandwidth sharing require zero investment. Staking requires purchasing tokens.

**Is bandwidth sharing safe?**
Yes. Services like Honeygain and PacketStream only use your unused bandwidth for legitimate purposes (price comparison, ad verification, etc.).

**Can I run this on a VPS?**
Content publishing and staking scripts work anywhere. Bandwidth sharing needs a residential IP.

---

Start small. Stack income streams. Let the terminal do the work.
