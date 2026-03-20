# Lightning / Bitcoin Faucet List

> Last updated: 2026-03-14
> Reality check: Most faucets pay 1-50 sats per claim (~$0.001-$0.05).
> Monthly from faucets alone: realistically $0.50-$5 max.
> Worth it? Marginal, but free sats are free sats. Best combined with other streams.

---

## TIER 1: Lightning Faucets (Instant Payout)

### 1. Lightning Network Stores Faucet
- **URL**: https://lightningnetworkstores.com/faucet
- **Claim**: Browser-based, click button + paste Lightning invoice
- **Payout**: ~10-50 sats per claim
- **Frequency**: Once per IP per day (approx)
- **Terminal-friendly**: PARTIAL — Vue.js SPA, needs browser interaction or headless scraping
- **API**: No public API
- **Notes**: One of the oldest Lightning faucets. Simple but requires browser. Uses CAPTCHA sometimes.

### 2. LNPulse Sats Faucet (Nostr Users)
- **URL**: https://faucet.lnpulse.app/
- **Claim**: Connect Nostr identity, claim via Lightning
- **Payout**: ~10-100 sats per claim (randomized)
- **Frequency**: Daily
- **Terminal-friendly**: POSSIBLE — if they have a Nostr-based claim mechanism (NIP-based auth)
- **API**: No documented public API
- **Notes**: Requires Nostr pubkey. Good fit since we already have Nostr keys set up.

### 3. LightningFaucet.com
- **URL**: https://lightningfaucet.com/
- **Claim**: Free weekly spin (browser)
- **Payout**: 5-100 sats per spin
- **Frequency**: Weekly
- **Terminal-friendly**: NO — requires browser, account, spin mechanism
- **API**: Has L402 API registry but that's for PAYING for APIs, not claiming faucet
- **Notes**: More of a casino/rewards site than a pure faucet. Weekly spin is tiny.

### 4. Boltcoiner
- **URL**: https://boltcoiner.io/
- **Claim**: Enter Lightning address + CAPTCHA + share tweet
- **Payout**: Unknown (was ~50-100 sats)
- **Frequency**: Daily
- **Terminal-friendly**: NO — CAPTCHA + social sharing required
- **API**: None
- **Notes**: Currently OUT OF SERVICE / out of funds as of late 2024. May return.

---

## TIER 2: Bitcoin Faucets with Lightning Withdrawal

### 5. SatsFaucet
- **URL**: https://www.satsfaucet.com/
- **Claim**: Browser — tasks, surveys, app testing, watching videos
- **Payout**: 10 sats per faucet claim, up to 400 sats/hour with tasks
- **Frequency**: Hourly faucet claim
- **Terminal-friendly**: NO — requires browser, account, completing tasks
- **API**: None
- **Withdrawal**: Lightning Network (Wallet of Satoshi compatible)
- **Notes**: Legit but very time-consuming. 400 sats/hour = $0.40/hour. Not worth automating.

### 6. Cointiply
- **URL**: https://cointiply.com/
- **Claim**: Browser — surveys, tasks, games, offerwall
- **Payout**: Variable, very small per task
- **Frequency**: Continuous (task-based)
- **Terminal-friendly**: NO — fully browser-based with account
- **API**: None
- **Withdrawal**: BTC on-chain (minimum 50,000 coins = ~$3), no Lightning
- **Notes**: One of the oldest faucet sites. Very low pay. Not Lightning-compatible.

### 7. FreeBitco.in
- **URL**: https://freebitco.in/
- **Claim**: Roll dice every hour
- **Payout**: ~1-200 sats per roll (weighted heavily toward 1 sat)
- **Frequency**: Hourly
- **Terminal-friendly**: NO — heavy CAPTCHA, anti-bot measures
- **API**: Has a "multiply BTC" API but the faucet itself has no API
- **Withdrawal**: BTC on-chain only, no Lightning. High minimum.
- **Notes**: Domain may be down. Was one of the biggest faucets but extremely anti-automation.

---

## TIER 3: Earn Sats (Not Traditional Faucets, but Free)

### 8. Stacker News
- **URL**: https://stacker.news/
- **Claim**: Post quality content, get upvoted → earn sats
- **Payout**: 1-1000+ sats per quality post/comment
- **Frequency**: Unlimited (content-based)
- **Terminal-friendly**: PARTIAL — has no public posting API, but could script via browser
- **API**: No public API for posting
- **Notes**: Best "faucet" if you produce quality Bitcoin/tech content. Real earning potential.

### 9. Zebedee (ZBD)
- **URL**: https://zebedee.io/
- **Claim**: Play games, earn sats
- **Payout**: Variable (1-100 sats per game session)
- **Frequency**: Continuous
- **Terminal-friendly**: NO — mobile app required
- **API**: Yes! Free tier: 100K tx/month, 1M sats volume. But for SENDING, not claiming.
- **Notes**: Good API for building Lightning apps, but not a faucet you can claim from.

### 10. Nostr Zaps (Organic)
- **URL**: Any Nostr client
- **Claim**: Post valuable content → receive zaps from community
- **Payout**: 1-10,000+ sats per zap
- **Frequency**: Based on content quality
- **Terminal-friendly**: YES — we already have scripts for this
- **API**: Nostr protocol (NIP-57 zaps)
- **Notes**: This is our best "faucet" — already set up. Post good content, get zapped.

---

## TIER 4: LNURL-Withdraw Faucets (Most Scriptable)

### 11. Custom LNURL-Withdraw Faucets
- **URL**: Various (community-run, appear and disappear)
- **Claim**: GET request to LNURL endpoint → submit Lightning invoice to callback
- **Payout**: 1-100 sats typically
- **Frequency**: Varies
- **Terminal-friendly**: YES — pure HTTP requests
- **API**: LNURL-withdraw protocol (standard)
- **How it works**:
  1. Decode LNURL (bech32 → URL)
  2. GET the URL → receive `{"tag":"withdrawRequest", "callback":"...", "k1":"...", "maxWithdrawable":...}`
  3. Generate a Lightning invoice for the amount
  4. GET callback?k1=...&pr=<invoice>
- **Notes**: These are the most automation-friendly but are rare on mainnet and frequently go offline.

### 12. LNbits Withdraw Links (Self-Hosted)
- **URL**: Your own LNbits instance
- **Claim**: Create LNURL-withdraw vouchers
- **Terminal-friendly**: YES — full API
- **Notes**: This is for DISTRIBUTING sats, not claiming. But useful for creating your own faucet.

---

## TIER 5: Testnet Only (No Real Value)

### 13. Lightning Labs Faucet
- **URL**: https://github.com/lightninglabs/lightning-faucet
- **Type**: Testnet only — opens payment channels, no real BTC
- **Notes**: For development testing only.

### 14. Bitcoin Testnet Faucets
- **URLs**: bitcoinfaucet.uo1.net, testnet.help, signetfaucet.com
- **Type**: Testnet/Signet — no real value
- **Notes**: Useful for testing but not for earning.

---

## Summary: What's Actually Worth Automating?

| Method | Scriptable? | Daily Sats | Monthly Sats | Monthly USD | Effort |
|--------|-------------|------------|--------------|-------------|--------|
| LN Stores Faucet | Partial | ~20 | ~600 | ~$0.60 | Low |
| LNPulse (Nostr) | Partial | ~50 | ~1,500 | ~$1.50 | Low |
| LNURL-withdraw | Yes | ~10 | ~300 | ~$0.30 | Low |
| Nostr zaps | Yes (already set up) | ~100-500 | ~3,000-15,000 | ~$3-15 | Medium |
| Stacker News | Manual | ~50-200 | ~1,500-6,000 | ~$1.50-6 | High |
| SatsFaucet tasks | No | ~400 | ~12,000 | ~$12 | Very High |

### Honest Assessment
- **Pure faucets are not worth significant effort** — they pay pennies
- **Best ROI**: Nostr content + zaps (already set up in our system)
- **The script below tries known endpoints** but expect most to fail or pay very little
- **Treat faucets as a fun bonus**, not an income stream

---

## LNURL-Withdraw Protocol Reference (For Scripting)

```
# Step 1: Resolve Lightning Address to LNURL-pay endpoint
curl https://walletofsatoshi.com/.well-known/lnurlp/freshbeach08

# Step 2: For LNURL-withdraw faucets, decode the LNURL
# LNURL is bech32-encoded → decode to get HTTP URL
# GET that URL → returns withdrawRequest JSON

# Step 3: Submit your invoice
# GET <callback>?k1=<k1>&pr=<bolt11_invoice>
```

Note: Most faucets do NOT use LNURL-withdraw. They use browser forms with CAPTCHAs
to prevent exactly what we're trying to do (automate claims).
