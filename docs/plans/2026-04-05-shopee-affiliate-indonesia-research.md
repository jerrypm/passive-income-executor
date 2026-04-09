# Shopee Affiliate Program Indonesia — Comprehensive Research

**Date:** 2026-04-05
**Purpose:** Research for business decision — affiliate marketing via unique/quirky product curation
**Market:** Indonesia

---

## 1. Shopee Affiliate Program Indonesia — How It Works

### Overview

Shopee Affiliate Program (SAP) allows content creators, bloggers, and social media users to earn commissions by promoting Shopee products through unique tracking links. When someone clicks your link and purchases within the attribution window, you earn a commission.

**Portal URL:** https://affiliate.shopee.co.id

### How It Works (Flow)

1. Register at affiliate.shopee.co.id (free, requires Shopee account)
2. Application reviewed in 1-5 working days
3. Once approved, generate affiliate links via dashboard
4. Share links on social media, blogs, YouTube, etc.
5. Earn commission when buyers purchase within 7 days of clicking
6. Withdraw earnings to bank account (min IDR 100,000)

### Two Tiers of Affiliates

| Tier | Commission Cap/Order | Requirements |
|------|---------------------|--------------|
| **Shopee Affiliate** (regular) | Max Rp 10,000/order | Basic approval |
| **Shopee Partner** | Max Rp 50,000/order | Higher performance, Golden Tick creators |

### Requirements to Join

- Active Shopee account (free)
- Social media presence (recommended 500-1,000+ followers)
- Must list promotional channels: Facebook, Instagram, TikTok, YouTube, blog, website
- Content quality and audience engagement evaluated
- No strict minimum follower count (unlike Lazada which wants 1,000+)
- Approval: 1-5 working days

### Cookie Duration

- **7 days** — if a user clicks your link and purchases ANY product within 7 days, you earn commission
- This includes **indirect orders** (user clicks your link for Product A but buys Product B)

### Minimum Payout

- **IDR 100,000** (approx. $6 USD)
- Payment via bank transfer (SeaBank or local bank)
- Disbursement: 5-7 working days after request
- Monthly cycle: 1st to end of month, must submit withdrawal before month-end

### Return Rate

- ~5-8% return rate (relatively stable compared to TikTok's higher volatility)

---

## 2. Commission Rates by Category

### Base Commission (Komisi Shopee)

| Category Type | Base Rate | Max Cap/Order |
|---------------|-----------|---------------|
| **Non-Electronic** (Fashion, Beauty, Home & Living, Toys, Accessories, Mother & Baby) | **2%** | Rp 10,000 (Affiliate) / Rp 50,000 (Partner) |
| **Electronic** (Smartphones, Laptops, Gadgets, Appliances) | **0.5%** | Rp 10,000 (Affiliate) / Rp 50,000 (Partner) |

### XTRA Commission (Komisi XTRA) — The Real Money Maker

Komisi XTRA is **additional unlimited commission** from sellers who opt into the Affiliate Marketing Solution (AMS). This is ON TOP of the base commission and has **no cap**.

| XTRA Commission Level | Bonus from Shopee (Non-Electronic) | Bonus from Shopee (Electronic) |
|------------------------|------------------------------------|---------------------------------|
| XTRA >= 10% | +7% bonus | +7% bonus |
| XTRA 6% to <10% (Non-Electronic) | +3% bonus | — |
| XTRA 1% to <10% (Electronic) | — | +3% bonus |

**Minimum XTRA thresholds for Golden Tick creators:**
- Non-electronic: >= 6%
- Electronic: >= 1%

**Some sellers offer XTRA commissions of 25-40%** on their products.

### Effective Commission Examples

For a non-electronic product (e.g., quirky home decor item priced Rp 150,000):
- Base Shopee commission: 2% = Rp 3,000 (capped at Rp 10,000)
- Seller XTRA commission: 10% = Rp 15,000 (NO cap)
- Shopee bonus for XTRA >= 10%: +7% = Rp 10,500
- **Total: Rp 28,500 per sale (~19% effective rate)**

For an electronic product (e.g., gadget priced Rp 500,000):
- Base Shopee commission: 0.5% = Rp 2,500 (capped at Rp 10,000)
- Seller XTRA commission: 5% = Rp 25,000 (NO cap)
- Shopee bonus for XTRA 1-10%: +3% = Rp 15,000
- **Total: Rp 42,500 per sale (~8.5% effective rate)**

### Categories Relevant to Unique/Quirky Products

| Category | Type | Base Rate | Typical XTRA Range |
|----------|------|-----------|---------------------|
| Home & Living / Home Decor | Non-Electronic | 2% | 6-15% |
| Toys & Games | Non-Electronic | 2% | 6-15% |
| Fashion Accessories | Non-Electronic | 2% | 6-20% |
| Gadgets & Tech Accessories | Electronic | 0.5% | 1-10% |
| Kitchen & Dining (novelty items) | Non-Electronic | 2% | 6-15% |
| Stationery & Craft | Non-Electronic | 2% | 6-15% |
| Pet Accessories | Non-Electronic | 2% | 6-15% |
| Beauty (novelty/quirky) | Non-Electronic | 2% | 6-15% |
| Automotive Accessories | Non-Electronic | 2% | 6-10% |
| Mother & Baby | Non-Electronic | 2% | 6-10% |

### Which Categories Have the HIGHEST Commission?

**Non-electronic categories consistently offer higher commissions because:**
1. Higher seller margins (fashion/beauty can be 50-80% margin)
2. More sellers opt into XTRA commission
3. Base rate is 4x higher than electronics (2% vs 0.5%)
4. No practical cap on XTRA commissions

**Top categories for affiliate earnings in Indonesia (by total effective commission):**
1. **Fashion & Accessories** — XTRA up to 20-40%, high volume
2. **Beauty & Personal Care** — XTRA up to 15-25%, repeat purchases
3. **Home & Living / Home Decor** — XTRA 6-15%, good for quirky/novelty curation
4. **Toys & Hobbies** — XTRA 6-15%, impulse buy category
5. **Kitchen & Dining** — XTRA 6-15%, viral product potential

**For quirky/novelty products specifically:** Non-electronic categories (Home Decor, Toys, Accessories, Kitchen gadgets) are ideal — you get the 2% base + uncapped XTRA from motivated sellers, typically landing at 8-17% total commission.

---

## 3. Shopee Affiliate Link Format

### Deep Link Structure

```
https://s.shopee.co.id/an_redir?origin_link={URL_ENCODED_PRODUCT_URL}&affiliate_id={YOUR_ID}&sub_id={TRACKING}
```

**Components:**
- **Domain:** `s.shopee.co.id` (Indonesia) or `shope.ee` (universal short domain)
- **Path:** `/an_redir` (redirect endpoint)
- **Parameters:**
  - `origin_link` — URL-encoded destination (product page, category page, or shop page)
  - `affiliate_id` — Your unique affiliate ID (numeric, e.g., `14354840000`)
  - `sub_id` — 5-segment tracking value: `{value1}-{value2}-{value3}-{value4}-{value5}`

### Sub ID Format

```
{sub-publisher}-{network-click}-{referral-source}-{custom}-{custom}
```

Use this to track performance across different channels (e.g., `twitter-post1-homepage-campaign1-test`).

### Auto-Generated UTM Parameters

When a user lands on Shopee via your link, these are automatically appended:
- `utm_source=an_{affiliate_id}`
- `utm_medium=affiliates`
- `utm_campaign=-`
- `utm_content={sub_id_value}`
- `uls_trackid` (system tracking)
- `utm_term` (system populated)

### Short Link Format

Generated via dashboard: `https://shope.ee/3poh74Bvt2`

### Link Types You Can Generate

1. **Product Link** — Direct to specific product page
2. **Shop Link** — Direct to seller's shop page
3. **Category Link** — Direct to category browse page
4. **Campaign Link** — Direct to sale/campaign pages
5. **Custom Link** — Any Shopee URL

---

## 4. Shopee Affiliate Tools Available

### Built-in Dashboard Tools

| Tool | Description |
|------|-------------|
| **Link Generator** | Create affiliate links for any product/shop/category URL |
| **Deeplink Generator** | Generate deep links that open directly in Shopee app |
| **Short Link** | Automatic URL shortening (shope.ee domain) |
| **Performance Dashboard** | Track clicks, orders, commissions in real-time |
| **Weekly Reports** | Detailed commission reports published every Thursday |
| **Product Discovery** | Browse products with XTRA commission badges |
| **XTRA Commission Filter** | Filter products specifically offering XTRA commissions |

### Open API

- **Portal:** https://affiliate.shopee.co.id/api
- **Authentication:** App ID + Secret Key (obtained from affiliate dashboard)
- **Capabilities:** Conversion tracking, order data, commission reports
- **Implementation:** URL-based redirect mechanism (no complex API calls needed for link generation)

### Third-Party Integrations

| Platform | Integration Type |
|----------|-----------------|
| **Involve Asia** | Affiliate network with Shopee campaigns |
| **ACCESSTRADE** | Affiliate network (popular in Indonesia) |
| **wecantrack** | Conversion tracking + analytics integration |
| **Content Egg** (WordPress) | Product module with Shopee deeplink support |

### Analytics Integrations (via wecantrack)

Shopee conversion data can be pushed to:
- Google Analytics
- Google Ads
- Microsoft Ads
- Facebook Ads Manager (Conversion API)
- Looker Studio
- Zapier

### Shopee Live & Shopee Video

- Affiliates can earn commissions through live selling (up to 10% rate)
- Shopee Live: 1% base (Shopee products), 6% (XTRA products)
- Shopee Video: 1% base
- Content creators get priority in Shopee's algorithm

---

## 5. Comparison: Shopee vs Tokopedia vs Lazada Affiliate

### Commission Rates Comparison

| Feature | Shopee | Tokopedia | Lazada |
|---------|--------|-----------|--------|
| **Base Rate (Non-Electronic)** | 2% | 1-10% (varies by category) | Up to 10% (seller-determined) |
| **Base Rate (Electronic)** | 0.5% | 1% | ~6% |
| **Fashion/Beauty** | 2% + XTRA (up to 40%) | 10% (max Rp 20,000) | Up to 12% |
| **Gadgets/Accessories** | 0.5-2% + XTRA | 5% (max Rp 20,000) | ~6% |
| **Home & Living** | 2% + XTRA | 4% (max Rp 20,000) | Up to 10% |
| **Toys & Hobbies** | 2% + XTRA | 2% (max Rp 20,000) | Up to 10% |
| **Food & Beverages** | 2% + XTRA | 7% (max Rp 20,000) | Up to 10% |
| **Extra Commission** | XTRA up to 25-40% (NO cap) | Up to 20% from selected stores | Up to 36% during mega sales |
| **Max Cap/Order** | Rp 10,000 base (XTRA unlimited) | Rp 20,000 per product | Not publicly capped |

### Tokopedia Category-Specific Rates

| Category | Commission Rate | Max/Product |
|----------|----------------|-------------|
| Beauty, Fashion | 10% | Rp 20,000 |
| Food & Beverages | 7% | Rp 20,000 |
| Accessories, Gadgets, Health, Mother & Baby | 5% | Rp 20,000 |
| Household, Books | 4% | Rp 20,000 |
| Audio, Automotive, Sports, Toys, Hobbies | 2% | Rp 20,000 |
| Electronics, Mobile Phones, Tablets | 1% | Rp 20,000 |

**Tokopedia Bonus:** Visit commission of Rp 50/verified visit (daily limit Rp 32,000).

### Program Features Comparison

| Feature | Shopee | Tokopedia | Lazada |
|---------|--------|-----------|--------|
| **Cookie Duration** | 7 days | 7 days | 7 days (app) / 30 days (web) |
| **Min Payout** | Rp 100,000 | Varies (via Affiliate Balance) | ~Rp 300,000 (via Involve Asia) |
| **Payment Method** | Bank transfer | Bank transfer | Bank transfer (via network) |
| **Payment Frequency** | Monthly | Monthly | Monthly |
| **Min Followers** | None (500+ recommended) | None | 1,000+ (5,000+ for Talent tier) |
| **Approval Time** | 1-5 working days | Instant/fast | 1-3 working days |
| **Open API** | Yes | Limited | Via Involve Asia |
| **Deep Link Generator** | Yes (built-in) | Yes (built-in) | Yes (via Involve Asia) |
| **Visit Commission** | No | Yes (Rp 50/visit) | No |
| **Live Selling Commission** | Yes (up to 10%) | No | Yes |

### Ease of Use Comparison

| Aspect | Shopee | Tokopedia | Lazada |
|--------|--------|-----------|--------|
| **Registration** | Easy, direct | Easiest, minimal requirements | Moderate (via Involve Asia) |
| **Link Generation** | Very easy, built-in tools | Easy, built-in | Easy via Involve Asia |
| **Dashboard** | Comprehensive | Good | Good (via network) |
| **Product Discovery** | Excellent (XTRA filter) | Good | Good |
| **Payout Process** | Straightforward | Straightforward | Through affiliate network |
| **Learning Curve** | Low | Lowest | Medium |

### Market Share Context (Indonesia 2025)

| Platform | Monthly Web Visits (May 2025) | Market Position |
|----------|-------------------------------|-----------------|
| Shopee | ~150M+ | #1 in Indonesia |
| Tokopedia | ~100M+ | #2 (merged with TikTok Shop) |
| Lazada | ~30-40M | #3 |

---

## 6. Strategic Recommendations for Quirky/Novelty Product Affiliate

### Why Shopee is Best for This Use Case

1. **Largest product selection** — Shopee has the most sellers in Indonesia, meaning more unique/quirky products
2. **XTRA commission is uncapped** — Unlike Tokopedia's Rp 20,000 cap, XTRA has no limit
3. **Non-electronic base rate (2%)** — Most quirky items are non-electronic, getting the higher base
4. **7-day cookie + indirect orders** — Even if they don't buy your promoted product, you earn on anything they buy
5. **Lowest barrier to entry** — No minimum followers required
6. **Best app penetration** — Most Indonesian shoppers already have Shopee app installed

### Recommended Multi-Platform Strategy

| Priority | Platform | Why |
|----------|----------|-----|
| **Primary** | Shopee Affiliate | Largest market, best for novelty products, XTRA commission |
| **Secondary** | Tokopedia Affiliate | Visit commission is free money, good for fashion/beauty |
| **Tertiary** | Lazada Affiliate | Higher base rates, 30-day web cookie, good for electronics |

### Revenue Projection (Conservative)

Assuming a curated quirky products account on Instagram/TikTok promoting 3-5 products/day:

| Metric | Month 1 | Month 3 | Month 6 |
|--------|---------|---------|---------|
| Daily clicks | 50 | 200 | 500 |
| Conversion rate | 2% | 3% | 4% |
| Orders/day | 1 | 6 | 20 |
| Avg commission/order | Rp 15,000 | Rp 18,000 | Rp 22,000 |
| **Monthly revenue** | **Rp 450,000** | **Rp 3,240,000** | **Rp 13,200,000** |
| **USD equivalent** | ~$28 | ~$200 | ~$825 |

*Based on promoting products with XTRA commission in the 8-15% range, average order value Rp 100,000-200,000*

---

## Sources

- [Shopee Affiliate Program — Reacheffect (2026)](https://reacheffect.com/blog/shopee-affiliate-program/)
- [Shopee Affiliate — Involve Asia](https://involve.asia/blog/shopee-affiliate-program/)
- [Skema Komisi Baru Shopee Affiliate — Shopee Help Center ID](https://help.shopee.co.id/10/article/147677-[Shopee-Affiliate-Program]-Apa-itu-Skema-Komisi-Baru-Shopee-Affiliate)
- [Komisi XTRA Shopee — Shopee Help Center ID](https://help.shopee.co.id/4/article/88616-[Shopee-Affiliate-Program]-Apa-itu-Komisi-XTRA)
- [Perhitungan Komisi Sosial Media — Shopee Help Center ID](https://help.shopee.co.id/portal/10/article/123866-%5BShopee-Affiliate-Program%5D-Bagaimana-Perhitungan-Komisi-dari-Shopee-Affiliate-Program-di-Sosial-Media)
- [Komisi Affiliate Shopee, TikTok, Tokopedia 2025 — Tuwaga](https://tuwaga.id/artikel/komisi-affiliate-shopee-tiktok-tokopedia-2025/)
- [Comparing Affiliate Commissions — Pongoshare](https://pongoshare.com/affiliate-commissions-tiktok-youtube-shopee-lazada/)
- [TikTok vs Shopee Affiliate 2026 — Ecomobi](https://ecomobi.com/tiktok-affiliate-vs-shopee-affiliate/)
- [Lazada Affiliate Strategies 2025 — Ecomobi](https://ecomobi.com/lazada-affiliate-program-trategies-to-boost-earnings/)
- [Shopee Affiliate Short Link Guide — Shopee Help Center SG](https://help.shopee.sg/portal/10/article/171184-Affiliate-Short-Link-Implementation-Guide)
- [Shopee Conversion Integration — wecantrack](https://wecantrack.com/shopee-integration/)
- [How to Cash Out Shopee Affiliate — Primenet](https://primenet.co.id/how-to-cash-out-affiliate-commissions-on-shopee/)
- [Tokopedia Affiliate Program — Tokopedia](https://affiliate.tokopedia.com/)
- [Top Affiliate Programs Indonesia 2025 — Admitad](https://www.admitad.com/idn/blog/affiliate-programm-indone/)
- [Lazada Affiliate — Cuelinks](https://www.cuelinks.com/campaigns/lazada-indonesia-affiliate-program)
- [Lazada $100M Affiliate Investment — PR Newswire](https://www.prnewswire.com/apac/news-releases/lazada-invests-us100-million-as-part-of-strategic-push-to-strengthen-affiliate-programme-and-lead-creator-commerce-in-the-region-302465003.html)
- [Komisi Shopee Affiliate — ACCESSTRADE](https://accesstrade.co.id/blogs/affiliate-marketing/cara-menghitung-komisi-program-shopee-affiliate-jangan-sampai-ada-yang-hilang)
- [Produk Affiliate Shopee Paling Laris — ACCESSTRADE](https://accesstrade.co.id/blogs/insights/produk-affiliate-shopee-paling-laris)
