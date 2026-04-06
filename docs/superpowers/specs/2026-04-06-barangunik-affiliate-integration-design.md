# BarangUnik — Shopee Affiliate Integration Design Spec

**Date:** 2026-04-06
**Status:** Approved
**Affiliate ID:** 11306601811
**Project path:** `websites/barangunik/`

## Overview

Integrasi Shopee Affiliate ke website BarangUnik yang sudah LIVE. Double layer affiliate link conversion (scraper + website fallback), upgrade scraper untuk isi 30-50 produk real, dan cleanup data dummy.

## Affiliate Link System

### Format
```
https://s.shopee.co.id/an_redir?origin_link={ENCODED_SHOPEE_URL}&affiliate_id=11306601811&sub_id={SOURCE}-{CATEGORY}-{PRODUCT_ID}
```

### Double Layer Convert

**Layer 1 — Scraper:** Waktu scrape, setiap `shopeeUrl` langsung di-encode jadi affiliate link sebelum masuk JSON output.

**Layer 2 — Website fallback:** Di `ProductCard.tsx`, sebelum render `<a href>`, cek apakah URL sudah mengandung `affiliate_id`. Kalau belum → auto-wrap. Cover produk yang ditambah manual via admin.

### Implementation
- 1 utility function `toAffiliateLink(url: string, subId?: string)` di `src/lib/affiliate.ts`
- Affiliate ID dari env var `NEXT_PUBLIC_SHOPEE_AFFILIATE_ID`
- Dipakai di ProductCard component dan bisa di-import di scraper logic

### Sub-ID Tracking
- Format: `{source}-{category}-{productId}`
- Contoh: `web-20rb50rb-12345`
- Untuk tracking sumber traffic mana yang convert paling bagus di dashboard Shopee

## Scraper Upgrade

### Target Keywords
```
"barang unik murah", "alat dapur unik", "lampu unik lucu",
"organizer unik", "gadget unik murah", "aksesoris HP unik",
"barang aneh shopee", "barang viral murah"
```

### Flow
1. Loop tiap keyword → hit Shopee search page
2. Extract: nama, harga, image, link produk, rating, sold, discount
3. Deduplicate by Shopee product ID
4. Auto-assign `priceCategory` dari harga
5. Generate affiliate link (Layer 1) pakai `toAffiliateLink()`
6. Filter: hanya produk rating >= 4.0, sold >= 100
7. Output → `data/scraped-products.json` (status: "pending")
8. Upload via admin "Import" atau POST ke `/api/products`

### Target Output
- 30-50 produk unik
- Semua 5 kategori harga keisi (minimal 3-5 per kategori)
- Semua punya image URL dari Shopee CDN

### Tech
- Python 3 + `requests` + `BeautifulSoup`
- Fallback: `playwright` headless browser kalau Shopee block
- Jalankan manual dari terminal

## Website Changes

### File Baru
- `src/lib/affiliate.ts` — utility `toAffiliateLink(url, subId?)`

### File Edit
- `src/components/ProductCard.tsx` — wrap `shopeeUrl` pakai `toAffiliateLink()`
- `websites/barangunik/scripts/scrape-shopee.py` — upgrade keywords, affiliate link gen, quality filter

### Environment Variable
- `NEXT_PUBLIC_SHOPEE_AFFILIATE_ID=11306601811` → tambah ke Vercel env

### Yang TIDAK Diubah
- Admin dashboard — input `shopeeUrl` biasa (Layer 2 auto-convert)
- Data model Product — tidak perlu field baru
- Routing, pages, API — semua tetap
- Styling — tidak ada perubahan visual

## Data Cleanup

- Hapus semua 8 produk dummy lama
- Replace dengan 30-50 produk real dari scraper
- Fresh start, data bersih

## Visitor Flow
```
Visitor buka barangunik.vercel.app
  → Lihat produk cards
  → Klik produk
  → ProductCard render href = toAffiliateLink(shopeeUrl)
  → Redirect ke s.shopee.co.id/an_redir → Shopee app/web
  → Visitor beli dalam 7 hari → komisi masuk
```

## Deployment
```bash
# Add env var
vercel env add NEXT_PUBLIC_SHOPEE_AFFILIATE_ID

# Deploy
cd websites/barangunik && npx vercel --yes --prod
```
