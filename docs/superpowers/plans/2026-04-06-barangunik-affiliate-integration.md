# BarangUnik Shopee Affiliate Integration — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate Shopee Affiliate tracking into BarangUnik website with double-layer link conversion, upgrade scraper to fill 30-50 real products, and clean up dummy data.

**Architecture:** Layer 1 (scraper) generates affiliate links at scrape time. Layer 2 (website) auto-converts any raw Shopee URL in ProductCard as a fallback. Both layers use one shared `toAffiliateLink()` utility. Sub-ID tracking enables per-source analytics in Shopee dashboard.

**Tech Stack:** Next.js 16 + Tailwind CSS v4 + Vercel Blob + Python 3 (scraper)

**Spec:** `docs/superpowers/specs/2026-04-06-barangunik-affiliate-integration-design.md`

---

## File Structure

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `src/lib/affiliate.ts` | `toAffiliateLink()` utility — URL encoding, affiliate ID injection, sub-ID tracking |
| Modify | `src/components/ProductCard.tsx:15` | Wrap `shopeeUrl` with `toAffiliateLink()` before rendering href |
| Modify | `scripts/scrape-shopee.py` | Add affiliate link generation, quality filters, updated keywords |
| Config | Vercel env | Add `NEXT_PUBLIC_SHOPEE_AFFILIATE_ID=11306601811` |

---

### Task 1: Create Affiliate Link Utility

**Files:**
- Create: `websites/barangunik/src/lib/affiliate.ts`

- [ ] **Step 1: Create `toAffiliateLink()` function**

Create `websites/barangunik/src/lib/affiliate.ts`:

```typescript
const SHOPEE_AFFILIATE_ID = process.env.NEXT_PUBLIC_SHOPEE_AFFILIATE_ID || "";
const SHOPEE_REDIR_BASE = "https://s.shopee.co.id/an_redir";

export function toAffiliateLink(url: string, subId?: string): string {
  if (!SHOPEE_AFFILIATE_ID) return url;
  if (!url || !url.includes("shopee.co.id")) return url;
  if (url.includes("affiliate_id=")) return url;

  const params = new URLSearchParams({
    origin_link: url,
    affiliate_id: SHOPEE_AFFILIATE_ID,
  });

  if (subId) {
    params.set("sub_id", subId);
  }

  return `${SHOPEE_REDIR_BASE}?${params.toString()}`;
}
```

- [ ] **Step 2: Verify it compiles**

Run: `cd websites/barangunik && npx tsc --noEmit src/lib/affiliate.ts`
Expected: No errors

- [ ] **Step 3: Commit**

```bash
git add websites/barangunik/src/lib/affiliate.ts
git commit -m "feat(barangunik): add Shopee affiliate link utility"
```

---

### Task 2: Integrate Affiliate Links into ProductCard

**Files:**
- Modify: `websites/barangunik/src/components/ProductCard.tsx`

- [ ] **Step 1: Add affiliate import and generate href**

In `ProductCard.tsx`, add the import at the top (after existing imports):

```typescript
import { toAffiliateLink } from "@/lib/affiliate";
```

Then replace the `<a>` tag's `href` attribute. Change:

```tsx
href={product.shopeeUrl}
```

to:

```tsx
href={toAffiliateLink(product.shopeeUrl, `web-${product.priceCategory}-${product.id}`)}
```

This passes sub-ID tracking: `web-{category}-{productId}`.

- [ ] **Step 2: Verify the build works**

Run: `cd websites/barangunik && npm run build`
Expected: Build succeeds with no errors

- [ ] **Step 3: Commit**

```bash
git add websites/barangunik/src/components/ProductCard.tsx
git commit -m "feat(barangunik): integrate affiliate link conversion in ProductCard"
```

---

### Task 3: Add Environment Variable to Vercel

**Files:**
- Config: Vercel project env

- [ ] **Step 1: Add env var locally for dev**

Append to `websites/barangunik/.env.local`:

```
NEXT_PUBLIC_SHOPEE_AFFILIATE_ID=11306601811
```

- [ ] **Step 2: Add env var to Vercel**

Run:

```bash
cd websites/barangunik && echo "11306601811" | npx vercel env add NEXT_PUBLIC_SHOPEE_AFFILIATE_ID production preview development
```

If that prompts interactively, use:

```bash
cd websites/barangunik && npx vercel env add NEXT_PUBLIC_SHOPEE_AFFILIATE_ID production preview development <<< "11306601811"
```

- [ ] **Step 3: Verify env var is set**

Run: `cd websites/barangunik && npx vercel env ls`
Expected: `NEXT_PUBLIC_SHOPEE_AFFILIATE_ID` appears in the list

---

### Task 4: Upgrade Scraper with Affiliate Links + Quality Filters

**Files:**
- Modify: `websites/barangunik/scripts/scrape-shopee.py`

- [ ] **Step 1: Add affiliate link generation function**

Add this function after the existing `get_price_category()` function (around line 61):

```python
SHOPEE_AFFILIATE_ID = "11306601811"
SHOPEE_REDIR_BASE = "https://s.shopee.co.id/an_redir"

def to_affiliate_link(url: str, sub_id: str = "") -> str:
    """Convert a Shopee URL to an affiliate tracking link."""
    if not url or "shopee.co.id" not in url:
        return url
    if "affiliate_id=" in url:
        return url
    from urllib.parse import urlencode, quote
    params = {
        "origin_link": url,
        "affiliate_id": SHOPEE_AFFILIATE_ID,
    }
    if sub_id:
        params["sub_id"] = sub_id
    return f"{SHOPEE_REDIR_BASE}?{urlencode(params, quote_via=quote)}"
```

- [ ] **Step 2: Update keywords list**

Replace the existing `KEYWORDS` list (line 27-38) with:

```python
KEYWORDS = [
    "barang unik murah",
    "alat dapur unik",
    "lampu unik lucu",
    "organizer unik",
    "gadget unik murah",
    "aksesoris HP unik",
    "barang aneh shopee",
    "barang viral murah",
]
```

- [ ] **Step 3: Add quality filter + affiliate link in `extract_product()`**

In the `extract_product()` function, after the line that builds `shopee_url` (line 134), add affiliate link generation:

```python
        # Generate affiliate link (Layer 1)
        affiliate_sub_id = f"scraper-{get_price_category(price)}-{item_id}"
        affiliate_url = to_affiliate_link(shopee_url, affiliate_sub_id)
```

Then in the return dict, change `"shopeeUrl": shopee_url,` to:

```python
            "shopeeUrl": affiliate_url,
            "shopeeUrlRaw": shopee_url,
```

- [ ] **Step 4: Add quality filter in `main()`**

After the deduplication loop (after line 180), add filtering before saving:

```python
    # Quality filter: rating >= 4.0 and sold >= 100
    products_list = [
        p for p in all_products.values()
        if (p.get("rating") is None or p["rating"] >= 4.0)
        and (p.get("sold") or 0) >= 100
    ]
```

Replace the existing `products_list = list(all_products.values())` line (line 188).

- [ ] **Step 5: Add `--min-rating` and `--min-sold` CLI args**

In the `main()` argument parser section, add:

```python
    parser.add_argument("--min-rating", type=float, default=4.0, help="Min rating filter (default: 4.0)")
    parser.add_argument("--min-sold", type=int, default=100, help="Min sold filter (default: 100)")
```

Then update the quality filter to use these args:

```python
    products_list = [
        p for p in all_products.values()
        if (p.get("rating") is None or p["rating"] >= args.min_rating)
        and (p.get("sold") or 0) >= args.min_sold
    ]
```

- [ ] **Step 6: Test scraper runs without error**

Run: `cd websites/barangunik/scripts && python3 scrape-shopee.py --limit 5`
Expected: Scrapes products, prints stats, saves `products.json`. Each product's `shopeeUrl` should start with `https://s.shopee.co.id/an_redir?origin_link=`.

- [ ] **Step 7: Commit**

```bash
git add websites/barangunik/scripts/scrape-shopee.py
git commit -m "feat(barangunik): upgrade scraper with affiliate links + quality filters"
```

---

### Task 5: Scrape Real Products (30-50)

**Files:**
- Output: `websites/barangunik/scripts/products.json` (temporary, not committed)

- [ ] **Step 1: Run full scrape**

```bash
cd websites/barangunik/scripts && python3 scrape-shopee.py --limit 30
```

Expected: 30-50 unique products across 5 price categories.

- [ ] **Step 2: Verify output quality**

```bash
cd websites/barangunik/scripts && python3 -c "
import json
products = json.load(open('products.json'))
print(f'Total: {len(products)}')
cats = {}
for p in products:
    cats[p['priceCategory']] = cats.get(p['priceCategory'], 0) + 1
    assert 'affiliate_id=' in p['shopeeUrl'], f'Missing affiliate: {p[\"name\"]}'
    assert p['imageUrl'], f'Missing image: {p[\"name\"]}'
for cat, count in sorted(cats.items()):
    print(f'  {cat}: {count}')
print('All checks passed!')
"
```

Expected: All products have affiliate links and images. All 5 categories have products.

- [ ] **Step 3: If Shopee API is blocked, use playwright fallback**

If Step 1 returns 0 products (API blocked), install playwright and modify scraper:

```bash
pip3 install playwright && python3 -m playwright install chromium
```

Then use the `--keywords` flag to try fewer keywords with longer delays:

```bash
cd websites/barangunik/scripts && python3 scrape-shopee.py --limit 10 --keywords "barang unik murah" "alat dapur unik"
```

If still blocked, manually curate products from Shopee website and add via admin dashboard.

---

### Task 6: Clean Up Dummy Data + Import Real Products

**Files:**
- Vercel Blob: `products.json` (remote storage)

- [ ] **Step 1: Clear existing dummy products via API**

Create a one-time cleanup script and run it:

```bash
cd websites/barangunik && npx tsx -e "
import { put } from '@vercel/blob';
// Overwrite with empty array to clear all products
await put('products.json', JSON.stringify([]), {
  access: 'public',
  addRandomSuffix: false,
  allowOverwrite: true,
  contentType: 'application/json',
  cacheControlMaxAge: 60,
});
console.log('All products cleared!');
"
```

Requires `BLOB_READ_WRITE_TOKEN` in `.env.local`.

- [ ] **Step 2: Import scraped products via API**

```bash
cd websites/barangunik && npx tsx -e "
import { readFileSync } from 'fs';
const products = JSON.parse(readFileSync('scripts/products.json', 'utf-8'));
console.log('Importing', products.length, 'products...');

// POST to local dev server or production API
const res = await fetch('https://barangunik.vercel.app/api/products', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(products),
});
const data = await res.json();
console.log('Result:', data);
"
```

Note: This requires auth. Alternative — use the seed script approach:

```bash
cd websites/barangunik && BLOB_READ_WRITE_TOKEN=$(grep BLOB_READ_WRITE_TOKEN .env.local | cut -d= -f2) npx tsx -e "
import { put } from '@vercel/blob';
import { readFileSync } from 'fs';
const products = JSON.parse(readFileSync('scripts/products.json', 'utf-8'));
await put('products.json', JSON.stringify(products, null, 2), {
  access: 'public',
  addRandomSuffix: false,
  allowOverwrite: true,
  contentType: 'application/json',
  cacheControlMaxAge: 60,
});
console.log('Uploaded', products.length, 'products to Vercel Blob');
"
```

- [ ] **Step 3: Verify products are live**

Run: `curl -s https://barangunik.vercel.app/api/products | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d)} products loaded')"`

Expected: 30-50 products loaded

---

### Task 7: Deploy + Verify Affiliate Links

**Files:**
- Deploy to Vercel production

- [ ] **Step 1: Deploy to production**

```bash
cd websites/barangunik && npx vercel --yes --prod
```

Expected: Deploy succeeds, URL shows barangunik.vercel.app

- [ ] **Step 2: Verify affiliate links in browser**

Open: `https://barangunik.vercel.app/`

Check:
1. Products display with images
2. Right-click a product → "Copy link address"
3. Link should contain `s.shopee.co.id/an_redir?origin_link=` and `affiliate_id=11306601811`
4. Click a product → should redirect to Shopee product page

- [ ] **Step 3: Verify in Shopee Affiliate dashboard**

Open: `https://affiliate.shopee.co.id/`
Check: Under Reports/Performance, the click should register within a few minutes.

- [ ] **Step 4: Commit all remaining changes**

```bash
git add websites/barangunik/
git commit -m "feat(barangunik): Shopee Affiliate integration complete — affiliate links + real products"
```

---

## Summary

| Task | What | Estimate |
|------|------|----------|
| 1 | Affiliate link utility | 2 min |
| 2 | ProductCard integration | 2 min |
| 3 | Vercel env var | 2 min |
| 4 | Scraper upgrade | 5 min |
| 5 | Scrape real products | 5 min |
| 6 | Data cleanup + import | 3 min |
| 7 | Deploy + verify | 5 min |
