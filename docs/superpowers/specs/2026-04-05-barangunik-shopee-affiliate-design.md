# BarangUnik — Shopee Affiliate Website Design Spec

**Date:** 2026-04-05
**Status:** Approved
**Project path:** `websites/barangunik/`

## Overview

Website "BarangUnik" menampilkan produk unik dan aneh dari Shopee Indonesia, dikategorikan berdasarkan range harga. Produk di-scrape dari Shopee, dikelola via admin dashboard, dan setiap link produk mengarah ke Shopee (affiliate link ditambahkan nanti).

## Tech Stack

- **Framework:** Next.js 15 App Router
- **Styling:** Tailwind CSS v4
- **Storage:** Vercel Blob (free 500MB) — products JSON + uploaded images
- **Auth:** JWT cookie, credentials di environment variable
- **Scraper:** Python 3 + requests (standalone script)
- **Deploy:** Vercel (free tier)

## Architecture

```
websites/barangunik/
├── src/app/
│   ├── page.tsx                 # Homepage — featured products + kategori
│   ├── kategori/[slug]/page.tsx # Product list per kategori harga
│   ├── produk/[id]/page.tsx     # Detail produk → redirect ke Shopee
│   ├── admin/
│   │   ├── page.tsx             # Dashboard — list semua produk
│   │   ├── login/page.tsx       # Login page
│   │   ├── tambah/page.tsx      # Form tambah produk
│   │   └── edit/[id]/page.tsx   # Form edit produk
│   └── api/
│       ├── products/route.ts    # CRUD API produk (termasuk bulk import)
│       └── auth/route.ts        # Login/logout API
├── scripts/
│   └── scrape-shopee.py         # Python scraper
├── public/
│   └── placeholder.png          # Default empty image
└── data/
    └── products.json            # Initial seed data
```

## Data Model

Setiap produk memiliki fields berikut:

```typescript
interface Product {
  id: string;              // Unique ID (Shopee product ID atau generated)
  name: string;            // Nama produk
  price: number;           // Harga dalam Rupiah
  priceCategory: string;   // Auto-assigned: "dibawah-20rb" | "20rb-50rb" | "50rb-100rb" | "100rb-500rb" | "diatas-500rb"
  discount?: number;       // Persentase diskon (optional)
  imageUrl: string;        // URL gambar (Shopee CDN / custom / Vercel Blob)
  shopeeUrl: string;       // Link ke produk di Shopee
  rating?: number;         // Rating bintang (optional)
  sold?: number;           // Jumlah terjual (optional)
  status: "active" | "hidden" | "pending"; // Status tampil
  scrapedAt?: string;      // Timestamp scrape (ISO format)
  createdAt: string;       // Timestamp created
  updatedAt: string;       // Timestamp last updated
}
```

## 5 Kategori Harga

| Kategori | Range | Slug | Badge Color |
|----------|-------|------|-------------|
| Super Murah | < Rp 20.000 | `dibawah-20rb` | Green |
| Murah | Rp 20.000 - 50.000 | `20rb-50rb` | Blue |
| Menengah | Rp 50.000 - 100.000 | `50rb-100rb` | Yellow |
| Premium | Rp 100.000 - 500.000 | `100rb-500rb` | Purple |
| Mewah | > Rp 500.000 | `diatas-500rb` | Red |

Kategori harga di-auto-assign berdasarkan `price`, bisa di-override manual dari dashboard.

## Frontend — Public Website

### Homepage (`/`)
- Header: logo "BarangUnik" + tagline "Temukan Barang Unik & Aneh dari Shopee"
- 5 kategori cards dengan emoji/icon + jumlah produk masing-masing
- Featured products grid (8-12 produk terbaru, status "active")
- Footer: simple credits

### Product Card
- Image produk (aspect ratio 1:1, fallback ke placeholder.png)
- Nama produk (max 2 baris, truncate)
- Harga format Rupiah ("Rp 18.700")
- Badge diskon kalau ada ("-63%")
- Badge kategori harga (warna sesuai tabel di atas)
- Klik → buka `shopeeUrl` di tab baru (`target="_blank"`)

### Kategori Page (`/kategori/[slug]`)
- Grid produk sesuai range harga
- Sort options: terbaru, termurah, termahal
- Pagination: 12 produk per page
- Breadcrumb: Home > Kategori > [Nama Kategori]

### Style & Responsive
- Warna tema oranye (Shopee-inspired tapi lebih muted/modern)
- Cards dengan shadow + hover effect (scale up sedikit)
- Responsive grid: 4 kolom desktop, 2 kolom tablet, 1 kolom mobile
- Tailwind CSS only, no external UI library

## Dashboard Admin

### Authentication
- Login page: `/admin/login` — form username + password
- Credentials dari env: `ADMIN_USERNAME`, `ADMIN_PASSWORD`
- Session: JWT token di httpOnly cookie, expire 24 jam
- Secret: `JWT_SECRET` dari env
- Middleware protect semua `/admin/*` routes kecuali `/admin/login`

### Dashboard Home (`/admin`)
- Stats: total produk per kategori (5 angka)
- Tabel produk: thumbnail, nama, harga, kategori, status
- Search bar + filter by kategori + filter by status
- Action buttons per row: Edit, Hapus, Toggle Active/Hidden
- Tombol "Tambah Produk" + "Import Hasil Scrape" (upload JSON)

### Form Tambah/Edit (`/admin/tambah`, `/admin/edit/[id]`)
- Fields:
  - Nama produk (text)
  - Harga (number, auto-format ke Rupiah di preview)
  - Link Shopee (URL)
  - Image URL (text — dari Shopee / custom URL)
  - Upload image manual (file upload → Vercel Blob)
  - Diskon % (number, optional)
  - Kategori harga (auto-detect dari harga, dropdown bisa override)
  - Status: active / hidden (radio/toggle)
- Preview: tampilan product card real-time sebelum save

### Scraper Trigger
- Scraper dijalankan **local** di terminal (Python script), bukan di Vercel serverless
- Tombol "Import Hasil Scrape" di dashboard — upload `products.json` hasil scrape
- `/api/products` endpoint menerima bulk import (POST array of products)
- Produk yang di-import masuk sebagai status "pending"
- Admin review: approve (→ active) atau reject (→ delete) satu-satu

## Scraper — Python Script

### File: `scripts/scrape-shopee.py`

**Keywords pencarian:**
- "barang unik", "barang aneh", "barang lucu"
- "gadget unik", "alat dapur unik", "hadiah unik"
- "barang viral", "barang anti mainstream"
- "mainan unik", "dekorasi unik"

**Proses:**
1. Loop setiap keyword
2. Hit Shopee search API: `https://shopee.co.id/api/v4/search/search_items`
3. Ambil 20-50 produk per keyword
4. Extract: id, name, price, discount, image_url, shopee_url, rating, sold
5. Deduplicate by Shopee product ID
6. Auto-assign `priceCategory` berdasarkan harga
7. Set status = "pending"
8. Output ke `products.json`

**Fallback jika API blocked:**
- Retry dengan different User-Agent
- Fallback ke Selenium/Playwright (headless browser)

**Image fallback:**
1. Shopee CDN image URL (primary)
2. Cari gambar dari internet (secondary)
3. `placeholder.png` (last resort)
4. Bisa di-update manual dari dashboard

### Output Format
```json
[
  {
    "id": "shopee_12345",
    "name": "Lampu Tidur Astronot Unik",
    "price": 45000,
    "priceCategory": "20rb-50rb",
    "discount": 30,
    "imageUrl": "https://cf.shopee.co.id/file/...",
    "shopeeUrl": "https://shopee.co.id/product/...",
    "rating": 4.8,
    "sold": 1200,
    "status": "pending",
    "scrapedAt": "2026-04-05T10:00:00Z",
    "createdAt": "2026-04-05T10:00:00Z",
    "updatedAt": "2026-04-05T10:00:00Z"
  }
]
```

## Environment Variables

```
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<strong-password>
BLOB_READ_WRITE_TOKEN=<dari-vercel-blob>
JWT_SECRET=<random-32-char-string>
```

## SEO

- Auto-generated sitemap (semua kategori + produk active)
- Meta tags + Open Graph per halaman
- JSON-LD structured data (Product schema per produk)
- Title format: "[Nama Produk] | BarangUnik" atau "Barang Unik [Kategori] | BarangUnik"
- Canonical URLs

## Monetisasi (Fase Berikutnya)

- Semua `shopeeUrl` akan diganti ke Shopee affiliate link (tambah tracking ID)
- Affiliate program: https://affiliate.shopee.co.id/
- Optional: slot Google AdSense, banner promo

## Deployment

- **Path:** `websites/barangunik/`
- **Platform:** Vercel (free tier)
- **Command:** `cd websites/barangunik && vercel --yes --prod`
- **Storage:** Vercel Blob (auto-provisioned saat link project)
