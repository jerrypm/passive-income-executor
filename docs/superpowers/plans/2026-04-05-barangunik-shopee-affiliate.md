# BarangUnik — Shopee Affiliate Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Shopee affiliate website showcasing unique/weird products, categorized by price, with an admin dashboard for CRUD and a Python scraper for product discovery.

**Architecture:** Next.js 15 App Router with Tailwind CSS v4. Product data stored as JSON in Vercel Blob. Admin dashboard protected by JWT cookie auth with credentials from environment variables. Python scraper runs locally and outputs JSON for bulk import via dashboard.

**Tech Stack:** Next.js 15, Tailwind CSS v4, Vercel Blob, jose (JWT), Python 3 + requests

---

## File Structure

```
websites/barangunik/
├── package.json
├── next.config.ts
├── tsconfig.json
├── tailwind.config.ts          # Tailwind v4 config (orange theme)
├── postcss.config.mjs
├── .env.local                  # Local dev env vars (gitignored)
├── middleware.ts                # Auth middleware — protect /admin/* routes
├── public/
│   └── placeholder.png         # Default empty product image (200x200 grey)
├── src/
│   ├── app/
│   │   ├── globals.css         # Tailwind imports + custom CSS vars
│   │   ├── layout.tsx          # Root layout — metadata, fonts, body wrapper
│   │   ├── page.tsx            # Homepage — kategori cards + featured products
│   │   ├── kategori/
│   │   │   └── [slug]/
│   │   │       └── page.tsx    # Category page — product grid + sort + pagination
│   │   ├── admin/
│   │   │   ├── layout.tsx      # Admin layout — sidebar nav, different from public
│   │   │   ├── page.tsx        # Dashboard — stats + product table + search/filter
│   │   │   ├── login/
│   │   │   │   └── page.tsx    # Login form
│   │   │   ├── tambah/
│   │   │   │   └── page.tsx    # Add product form + preview
│   │   │   └── edit/
│   │   │       └── [id]/
│   │   │           └── page.tsx # Edit product form + preview
│   │   └── api/
│   │       ├── auth/
│   │       │   └── route.ts    # POST login, DELETE logout
│   │       └── products/
│   │           ├── route.ts    # GET list, POST create/bulk-import
│   │           └── [id]/
│   │               └── route.ts # GET one, PUT update, DELETE remove
│   ├── lib/
│   │   ├── types.ts            # Product interface + PriceCategory type
│   │   ├── constants.ts        # Category config (slugs, ranges, colors, labels)
│   │   ├── products.ts         # Vercel Blob read/write helpers
│   │   ├── auth.ts             # JWT sign/verify + cookie helpers
│   │   └── format.ts          # formatRupiah, getPriceCategory utilities
│   └── components/
│       ├── ProductCard.tsx     # Reusable product card (public + admin preview)
│       ├── Header.tsx          # Public site header
│       ├── Footer.tsx          # Public site footer
│       ├── CategoryCard.tsx    # Category card for homepage
│       ├── Pagination.tsx      # Page navigation component
│       └── ProductForm.tsx     # Shared add/edit form with live preview
├── scripts/
│   └── scrape-shopee.py        # Python scraper — keywords → products.json
└── data/
    └── seed.json               # 10 sample products for initial seeding
```

---

## Task 1: Project Scaffold + Tailwind Theme

**Files:**
- Create: `websites/barangunik/package.json`
- Create: `websites/barangunik/next.config.ts`
- Create: `websites/barangunik/tsconfig.json`
- Create: `websites/barangunik/postcss.config.mjs`
- Create: `websites/barangunik/src/app/globals.css`
- Create: `websites/barangunik/src/app/layout.tsx`
- Create: `websites/barangunik/src/app/page.tsx`
- Create: `websites/barangunik/public/placeholder.png`
- Create: `websites/barangunik/.env.local`
- Create: `websites/barangunik/.gitignore`

- [ ] **Step 1: Create project directory**

```bash
mkdir -p websites/barangunik
```

- [ ] **Step 2: Initialize Next.js project**

```bash
cd websites/barangunik
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --no-import-alias --use-npm
```

When prompted, accept defaults. This creates package.json, next.config.ts, tsconfig.json, tailwind config, and App Router structure.

- [ ] **Step 3: Install dependencies**

```bash
cd websites/barangunik
npm install @vercel/blob jose
```

- `@vercel/blob` — Vercel Blob storage SDK
- `jose` — lightweight JWT library (works in Edge + Node)

- [ ] **Step 4: Create `.env.local`**

Create `websites/barangunik/.env.local`:

```
ADMIN_USERNAME=admin
ADMIN_PASSWORD=barangunik2026
BLOB_READ_WRITE_TOKEN=vercel_blob_placeholder
JWT_SECRET=barangunik-jwt-secret-change-me-32ch
```

- [ ] **Step 5: Update `.gitignore`**

Append to `websites/barangunik/.gitignore`:

```
.env.local
.env*.local
```

- [ ] **Step 6: Create placeholder image**

```bash
cd websites/barangunik
python3 -c "
from PIL import Image, ImageDraw, ImageFont
img = Image.new('RGB', (200, 200), '#f3f4f6')
draw = ImageDraw.Draw(img)
draw.text((55, 90), 'No Image', fill='#9ca3af')
img.save('public/placeholder.png')
"
```

If Pillow is not available, create a simple 1x1 grey PNG:

```bash
python3 -c "
import struct, zlib
def png(w,h,r,g,b):
    raw=b''
    for _ in range(h): raw+=b'\x00'+bytes([r,g,b])*w
    d=zlib.compress(raw)
    sig=b'\x89PNG\r\n\x1a\n'
    def chunk(t,data): return struct.pack('>I',len(data))+t+data+struct.pack('>I',zlib.crc32(t+data)&0xffffffff)
    return sig+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+chunk(b'IDAT',d)+chunk(b'IEND',b'')
open('public/placeholder.png','wb').write(png(200,200,243,244,246))
"
```

- [ ] **Step 7: Set up Tailwind theme with orange color palette**

Replace `websites/barangunik/src/app/globals.css` with:

```css
@import "tailwindcss";

:root {
  --color-brand-50: #fff7ed;
  --color-brand-100: #ffedd5;
  --color-brand-200: #fed7aa;
  --color-brand-300: #fdba74;
  --color-brand-400: #fb923c;
  --color-brand-500: #f97316;
  --color-brand-600: #ea580c;
  --color-brand-700: #c2410c;
  --color-brand-800: #9a3412;
  --color-brand-900: #7c2d12;
}

body {
  font-family: system-ui, -apple-system, sans-serif;
}
```

- [ ] **Step 8: Create root layout**

Replace `websites/barangunik/src/app/layout.tsx` with:

```tsx
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "BarangUnik — Barang Unik & Aneh dari Shopee",
    template: "%s | BarangUnik",
  },
  description: "Temukan barang unik, aneh, dan lucu dari Shopee Indonesia. Dikategorikan berdasarkan harga.",
  openGraph: {
    title: "BarangUnik — Barang Unik & Aneh dari Shopee",
    description: "Temukan barang unik, aneh, dan lucu dari Shopee Indonesia.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id">
      <body className="bg-gray-50 text-gray-900 antialiased">
        {children}
      </body>
    </html>
  );
}
```

- [ ] **Step 9: Create minimal homepage placeholder**

Replace `websites/barangunik/src/app/page.tsx` with:

```tsx
export default function HomePage() {
  return (
    <main className="min-h-screen flex items-center justify-center">
      <h1 className="text-4xl font-bold text-[var(--color-brand-500)]">
        BarangUnik
      </h1>
    </main>
  );
}
```

- [ ] **Step 10: Verify dev server runs**

```bash
cd websites/barangunik && npm run dev
```

Open http://localhost:3000 — should see orange "BarangUnik" text centered on page.

- [ ] **Step 11: Commit**

```bash
git add websites/barangunik/
git commit -m "feat(barangunik): scaffold Next.js 15 + Tailwind project"
```

---

## Task 2: Types, Constants, and Utility Functions

**Files:**
- Create: `websites/barangunik/src/lib/types.ts`
- Create: `websites/barangunik/src/lib/constants.ts`
- Create: `websites/barangunik/src/lib/format.ts`

- [ ] **Step 1: Create types**

Create `websites/barangunik/src/lib/types.ts`:

```typescript
export type PriceCategory =
  | "dibawah-20rb"
  | "20rb-50rb"
  | "50rb-100rb"
  | "100rb-500rb"
  | "diatas-500rb";

export type ProductStatus = "active" | "hidden" | "pending";

export interface Product {
  id: string;
  name: string;
  price: number;
  priceCategory: PriceCategory;
  discount?: number;
  imageUrl: string;
  shopeeUrl: string;
  rating?: number;
  sold?: number;
  status: ProductStatus;
  scrapedAt?: string;
  createdAt: string;
  updatedAt: string;
}
```

- [ ] **Step 2: Create constants**

Create `websites/barangunik/src/lib/constants.ts`:

```typescript
import type { PriceCategory } from "./types";

export interface CategoryConfig {
  slug: PriceCategory;
  label: string;
  shortLabel: string;
  emoji: string;
  min: number;
  max: number;
  badgeColor: string;
  badgeBg: string;
}

export const CATEGORIES: CategoryConfig[] = [
  {
    slug: "dibawah-20rb",
    label: "Super Murah",
    shortLabel: "< Rp 20rb",
    emoji: "💰",
    min: 0,
    max: 19999,
    badgeColor: "text-green-800",
    badgeBg: "bg-green-100",
  },
  {
    slug: "20rb-50rb",
    label: "Murah",
    shortLabel: "Rp 20rb - 50rb",
    emoji: "🏷️",
    min: 20000,
    max: 50000,
    badgeColor: "text-blue-800",
    badgeBg: "bg-blue-100",
  },
  {
    slug: "50rb-100rb",
    label: "Menengah",
    shortLabel: "Rp 50rb - 100rb",
    emoji: "⭐",
    min: 50001,
    max: 100000,
    badgeColor: "text-yellow-800",
    badgeBg: "bg-yellow-100",
  },
  {
    slug: "100rb-500rb",
    label: "Premium",
    shortLabel: "Rp 100rb - 500rb",
    emoji: "💎",
    min: 100001,
    max: 500000,
    badgeColor: "text-purple-800",
    badgeBg: "bg-purple-100",
  },
  {
    slug: "diatas-500rb",
    label: "Mewah",
    shortLabel: "> Rp 500rb",
    emoji: "👑",
    min: 500001,
    max: Infinity,
    badgeColor: "text-red-800",
    badgeBg: "bg-red-100",
  },
];

export const PRODUCTS_PER_PAGE = 12;
export const FEATURED_PRODUCTS_COUNT = 12;
```

- [ ] **Step 3: Create format utilities**

Create `websites/barangunik/src/lib/format.ts`:

```typescript
import { CATEGORIES } from "./constants";
import type { PriceCategory } from "./types";

export function formatRupiah(price: number): string {
  return `Rp ${price.toLocaleString("id-ID")}`;
}

export function getPriceCategory(price: number): PriceCategory {
  for (const cat of CATEGORIES) {
    if (price >= cat.min && price <= cat.max) {
      return cat.slug;
    }
  }
  return "diatas-500rb";
}

export function getCategoryBySlug(slug: string) {
  return CATEGORIES.find((c) => c.slug === slug);
}

export function generateId(): string {
  return `prod_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}
```

- [ ] **Step 4: Verify TypeScript compiles**

```bash
cd websites/barangunik && npx tsc --noEmit
```

Expected: no errors.

- [ ] **Step 5: Commit**

```bash
git add websites/barangunik/src/lib/
git commit -m "feat(barangunik): add types, constants, and format utilities"
```

---

## Task 3: Vercel Blob Product Storage Layer

**Files:**
- Create: `websites/barangunik/src/lib/products.ts`
- Create: `websites/barangunik/data/seed.json`

- [ ] **Step 1: Create seed data with 10 sample products**

Create `websites/barangunik/data/seed.json`:

```json
[
  {
    "id": "seed_001",
    "name": "Lampu Tidur Astronot LED Unik",
    "price": 18700,
    "priceCategory": "dibawah-20rb",
    "discount": 63,
    "imageUrl": "",
    "shopeeUrl": "https://shopee.co.id",
    "rating": 4.8,
    "sold": 1200,
    "status": "active",
    "createdAt": "2026-04-05T00:00:00Z",
    "updatedAt": "2026-04-05T00:00:00Z"
  },
  {
    "id": "seed_002",
    "name": "Garam Himalaya Pink 1000gr Premium",
    "price": 34500,
    "priceCategory": "20rb-50rb",
    "discount": 83,
    "imageUrl": "",
    "shopeeUrl": "https://shopee.co.id",
    "rating": 4.9,
    "sold": 5400,
    "status": "active",
    "createdAt": "2026-04-05T00:00:00Z",
    "updatedAt": "2026-04-05T00:00:00Z"
  },
  {
    "id": "seed_003",
    "name": "Sendok Garpu Lipat Portable Camping",
    "price": 15000,
    "priceCategory": "dibawah-20rb",
    "imageUrl": "",
    "shopeeUrl": "https://shopee.co.id",
    "rating": 4.5,
    "sold": 800,
    "status": "active",
    "createdAt": "2026-04-05T00:00:00Z",
    "updatedAt": "2026-04-05T00:00:00Z"
  },
  {
    "id": "seed_004",
    "name": "Smartwatch SKMEI B77 Waterproof",
    "price": 602100,
    "priceCategory": "diatas-500rb",
    "discount": 40,
    "imageUrl": "",
    "shopeeUrl": "https://shopee.co.id",
    "rating": 4.7,
    "sold": 320,
    "status": "active",
    "createdAt": "2026-04-05T00:00:00Z",
    "updatedAt": "2026-04-05T00:00:00Z"
  },
  {
    "id": "seed_005",
    "name": "Tissue Basah Beli 3 Gratis 2",
    "price": 11300,
    "priceCategory": "dibawah-20rb",
    "discount": 89,
    "imageUrl": "",
    "shopeeUrl": "https://shopee.co.id",
    "rating": 4.9,
    "sold": 15000,
    "status": "active",
    "createdAt": "2026-04-05T00:00:00Z",
    "updatedAt": "2026-04-05T00:00:00Z"
  },
  {
    "id": "seed_006",
    "name": "Parfum Pria EDT 100ml Anti Mainstream",
    "price": 254000,
    "priceCategory": "100rb-500rb",
    "discount": 49,
    "imageUrl": "",
    "shopeeUrl": "https://shopee.co.id",
    "rating": 4.6,
    "sold": 670,
    "status": "active",
    "createdAt": "2026-04-05T00:00:00Z",
    "updatedAt": "2026-04-05T00:00:00Z"
  },
  {
    "id": "seed_007",
    "name": "Alat Pemotong Bawang Anti Nangis",
    "price": 45000,
    "priceCategory": "20rb-50rb",
    "imageUrl": "",
    "shopeeUrl": "https://shopee.co.id",
    "rating": 4.3,
    "sold": 2300,
    "status": "active",
    "createdAt": "2026-04-05T00:00:00Z",
    "updatedAt": "2026-04-05T00:00:00Z"
  },
  {
    "id": "seed_008",
    "name": "Lampu LED Strip RGB Remote Control 5M",
    "price": 75000,
    "priceCategory": "50rb-100rb",
    "discount": 30,
    "imageUrl": "",
    "shopeeUrl": "https://shopee.co.id",
    "rating": 4.7,
    "sold": 4100,
    "status": "active",
    "createdAt": "2026-04-05T00:00:00Z",
    "updatedAt": "2026-04-05T00:00:00Z"
  },
  {
    "id": "seed_009",
    "name": "Boneka Capybara Giant 60cm Viral",
    "price": 125000,
    "priceCategory": "100rb-500rb",
    "imageUrl": "",
    "shopeeUrl": "https://shopee.co.id",
    "rating": 4.9,
    "sold": 890,
    "status": "active",
    "createdAt": "2026-04-05T00:00:00Z",
    "updatedAt": "2026-04-05T00:00:00Z"
  },
  {
    "id": "seed_010",
    "name": "Fidget Spinner Metal Premium Gold",
    "price": 8500,
    "priceCategory": "dibawah-20rb",
    "imageUrl": "",
    "shopeeUrl": "https://shopee.co.id",
    "rating": 4.2,
    "sold": 7600,
    "status": "pending",
    "createdAt": "2026-04-05T00:00:00Z",
    "updatedAt": "2026-04-05T00:00:00Z"
  }
]
```

- [ ] **Step 2: Create Vercel Blob product storage layer**

Create `websites/barangunik/src/lib/products.ts`:

```typescript
import { put, list } from "@vercel/blob";
import type { Product } from "./types";

const BLOB_FILENAME = "products.json";

export async function getAllProducts(): Promise<Product[]> {
  try {
    const { blobs } = await list({ prefix: BLOB_FILENAME });
    if (blobs.length === 0) return [];
    const response = await fetch(blobs[0].url);
    return (await response.json()) as Product[];
  } catch {
    return [];
  }
}

export async function saveAllProducts(products: Product[]): Promise<void> {
  await put(BLOB_FILENAME, JSON.stringify(products, null, 2), {
    access: "public",
    addRandomSuffix: false,
    contentType: "application/json",
  });
}

export async function getProductById(
  id: string
): Promise<Product | undefined> {
  const products = await getAllProducts();
  return products.find((p) => p.id === id);
}

export async function addProduct(product: Product): Promise<void> {
  const products = await getAllProducts();
  products.push(product);
  await saveAllProducts(products);
}

export async function updateProduct(
  id: string,
  updates: Partial<Product>
): Promise<Product | null> {
  const products = await getAllProducts();
  const index = products.findIndex((p) => p.id === id);
  if (index === -1) return null;
  products[index] = { ...products[index], ...updates, updatedAt: new Date().toISOString() };
  await saveAllProducts(products);
  return products[index];
}

export async function deleteProduct(id: string): Promise<boolean> {
  const products = await getAllProducts();
  const filtered = products.filter((p) => p.id !== id);
  if (filtered.length === products.length) return false;
  await saveAllProducts(filtered);
  return true;
}

export async function bulkImportProducts(
  newProducts: Product[]
): Promise<number> {
  const existing = await getAllProducts();
  const existingIds = new Set(existing.map((p) => p.id));
  const toAdd = newProducts.filter((p) => !existingIds.has(p.id));
  if (toAdd.length === 0) return 0;
  await saveAllProducts([...existing, ...toAdd]);
  return toAdd.length;
}

export function getActiveProducts(products: Product[]): Product[] {
  return products.filter((p) => p.status === "active");
}

export function getProductsByCategory(
  products: Product[],
  slug: string
): Product[] {
  return products.filter((p) => p.priceCategory === slug);
}
```

- [ ] **Step 3: Verify TypeScript compiles**

```bash
cd websites/barangunik && npx tsc --noEmit
```

Expected: no errors.

- [ ] **Step 4: Commit**

```bash
git add websites/barangunik/src/lib/products.ts websites/barangunik/data/seed.json
git commit -m "feat(barangunik): add Vercel Blob product storage layer + seed data"
```

---

## Task 4: Auth — JWT Login/Logout + Middleware

**Files:**
- Create: `websites/barangunik/src/lib/auth.ts`
- Create: `websites/barangunik/src/app/api/auth/route.ts`
- Create: `websites/barangunik/middleware.ts`

- [ ] **Step 1: Create auth helpers**

Create `websites/barangunik/src/lib/auth.ts`:

```typescript
import { SignJWT, jwtVerify } from "jose";
import { cookies } from "next/headers";

const COOKIE_NAME = "barangunik_session";

function getSecret() {
  const secret = process.env.JWT_SECRET;
  if (!secret) throw new Error("JWT_SECRET not set");
  return new TextEncoder().encode(secret);
}

export async function createSession(): Promise<string> {
  const token = await new SignJWT({ role: "admin" })
    .setProtectedHeader({ alg: "HS256" })
    .setExpirationTime("24h")
    .setIssuedAt()
    .sign(getSecret());
  return token;
}

export async function verifySession(token: string): Promise<boolean> {
  try {
    await jwtVerify(token, getSecret());
    return true;
  } catch {
    return false;
  }
}

export function validateCredentials(
  username: string,
  password: string
): boolean {
  return (
    username === process.env.ADMIN_USERNAME &&
    password === process.env.ADMIN_PASSWORD
  );
}

export async function getSessionFromCookies(): Promise<boolean> {
  const cookieStore = await cookies();
  const session = cookieStore.get(COOKIE_NAME);
  if (!session) return false;
  return verifySession(session.value);
}

export { COOKIE_NAME };
```

- [ ] **Step 2: Create auth API route**

Create `websites/barangunik/src/app/api/auth/route.ts`:

```typescript
import { NextRequest, NextResponse } from "next/server";
import { createSession, validateCredentials, COOKIE_NAME } from "@/lib/auth";

export async function POST(request: NextRequest) {
  const { username, password } = await request.json();

  if (!validateCredentials(username, password)) {
    return NextResponse.json(
      { error: "Username atau password salah" },
      { status: 401 }
    );
  }

  const token = await createSession();
  const response = NextResponse.json({ success: true });
  response.cookies.set(COOKIE_NAME, token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    maxAge: 60 * 60 * 24, // 24 hours
    path: "/",
  });
  return response;
}

export async function DELETE() {
  const response = NextResponse.json({ success: true });
  response.cookies.delete(COOKIE_NAME);
  return response;
}
```

- [ ] **Step 3: Create middleware to protect admin routes**

Create `websites/barangunik/middleware.ts`:

```typescript
import { NextRequest, NextResponse } from "next/server";
import { jwtVerify } from "jose";

const COOKIE_NAME = "barangunik_session";

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Skip login page and API routes
  if (pathname === "/admin/login" || pathname.startsWith("/api/")) {
    return NextResponse.next();
  }

  // Check for session cookie
  const token = request.cookies.get(COOKIE_NAME)?.value;
  if (!token) {
    return NextResponse.redirect(new URL("/admin/login", request.url));
  }

  // Verify JWT
  try {
    const secret = new TextEncoder().encode(process.env.JWT_SECRET);
    await jwtVerify(token, secret);
    return NextResponse.next();
  } catch {
    return NextResponse.redirect(new URL("/admin/login", request.url));
  }
}

export const config = {
  matcher: ["/admin/:path*"],
};
```

- [ ] **Step 4: Verify TypeScript compiles**

```bash
cd websites/barangunik && npx tsc --noEmit
```

Expected: no errors.

- [ ] **Step 5: Commit**

```bash
git add websites/barangunik/src/lib/auth.ts websites/barangunik/src/app/api/auth/ websites/barangunik/middleware.ts
git commit -m "feat(barangunik): add JWT auth — login/logout API + middleware"
```

---

## Task 5: Products API — CRUD + Bulk Import

**Files:**
- Create: `websites/barangunik/src/app/api/products/route.ts`
- Create: `websites/barangunik/src/app/api/products/[id]/route.ts`

- [ ] **Step 1: Create products list + create/import endpoint**

Create `websites/barangunik/src/app/api/products/route.ts`:

```typescript
import { NextRequest, NextResponse } from "next/server";
import {
  getAllProducts,
  addProduct,
  bulkImportProducts,
} from "@/lib/products";
import { getPriceCategory, generateId } from "@/lib/format";
import type { Product } from "@/lib/types";

export async function GET(request: NextRequest) {
  const products = await getAllProducts();
  const { searchParams } = request.nextUrl;
  const category = searchParams.get("category");
  const status = searchParams.get("status");
  const search = searchParams.get("search")?.toLowerCase();

  let filtered = products;
  if (category) filtered = filtered.filter((p) => p.priceCategory === category);
  if (status) filtered = filtered.filter((p) => p.status === status);
  if (search)
    filtered = filtered.filter((p) => p.name.toLowerCase().includes(search));

  return NextResponse.json(filtered);
}

export async function POST(request: NextRequest) {
  const body = await request.json();

  // Bulk import: array of products
  if (Array.isArray(body)) {
    const now = new Date().toISOString();
    const products: Product[] = body.map((item: Partial<Product>) => ({
      id: item.id || generateId(),
      name: item.name || "Unnamed Product",
      price: item.price || 0,
      priceCategory: item.priceCategory || getPriceCategory(item.price || 0),
      discount: item.discount,
      imageUrl: item.imageUrl || "",
      shopeeUrl: item.shopeeUrl || "",
      rating: item.rating,
      sold: item.sold,
      status: "pending" as const,
      scrapedAt: item.scrapedAt,
      createdAt: now,
      updatedAt: now,
    }));
    const imported = await bulkImportProducts(products);
    return NextResponse.json({ imported }, { status: 201 });
  }

  // Single product create
  const now = new Date().toISOString();
  const product: Product = {
    id: generateId(),
    name: body.name,
    price: body.price,
    priceCategory: body.priceCategory || getPriceCategory(body.price),
    discount: body.discount,
    imageUrl: body.imageUrl || "",
    shopeeUrl: body.shopeeUrl || "",
    rating: body.rating,
    sold: body.sold,
    status: body.status || "active",
    createdAt: now,
    updatedAt: now,
  };
  await addProduct(product);
  return NextResponse.json(product, { status: 201 });
}
```

- [ ] **Step 2: Create single product CRUD endpoint**

Create `websites/barangunik/src/app/api/products/[id]/route.ts`:

```typescript
import { NextRequest, NextResponse } from "next/server";
import { getProductById, updateProduct, deleteProduct } from "@/lib/products";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const product = await getProductById(id);
  if (!product) {
    return NextResponse.json({ error: "Product not found" }, { status: 404 });
  }
  return NextResponse.json(product);
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const body = await request.json();
  const updated = await updateProduct(id, body);
  if (!updated) {
    return NextResponse.json({ error: "Product not found" }, { status: 404 });
  }
  return NextResponse.json(updated);
}

export async function DELETE(
  _request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const deleted = await deleteProduct(id);
  if (!deleted) {
    return NextResponse.json({ error: "Product not found" }, { status: 404 });
  }
  return NextResponse.json({ success: true });
}
```

- [ ] **Step 3: Verify TypeScript compiles**

```bash
cd websites/barangunik && npx tsc --noEmit
```

Expected: no errors.

- [ ] **Step 4: Commit**

```bash
git add websites/barangunik/src/app/api/products/
git commit -m "feat(barangunik): add products CRUD API + bulk import endpoint"
```

---

## Task 6: Public Components — Header, Footer, ProductCard, CategoryCard, Pagination

**Files:**
- Create: `websites/barangunik/src/components/Header.tsx`
- Create: `websites/barangunik/src/components/Footer.tsx`
- Create: `websites/barangunik/src/components/ProductCard.tsx`
- Create: `websites/barangunik/src/components/CategoryCard.tsx`
- Create: `websites/barangunik/src/components/Pagination.tsx`

- [ ] **Step 1: Create Header component**

Create `websites/barangunik/src/components/Header.tsx`:

```tsx
import Link from "next/link";

export default function Header() {
  return (
    <header className="bg-[var(--color-brand-500)] text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-2xl font-bold">BarangUnik</span>
        </Link>
        <p className="hidden sm:block text-sm text-orange-100">
          Temukan Barang Unik &amp; Aneh dari Shopee
        </p>
      </div>
    </header>
  );
}
```

- [ ] **Step 2: Create Footer component**

Create `websites/barangunik/src/components/Footer.tsx`:

```tsx
export default function Footer() {
  return (
    <footer className="bg-gray-800 text-gray-400 py-8 mt-12">
      <div className="max-w-7xl mx-auto px-4 text-center text-sm">
        <p>&copy; {new Date().getFullYear()} BarangUnik. Semua harga dari Shopee.</p>
        <p className="mt-1">
          Harga dan ketersediaan dapat berubah sewaktu-waktu.
        </p>
      </div>
    </footer>
  );
}
```

- [ ] **Step 3: Create ProductCard component**

Create `websites/barangunik/src/components/ProductCard.tsx`:

```tsx
import Image from "next/image";
import { formatRupiah, getCategoryBySlug } from "@/lib/format";
import type { Product } from "@/lib/types";

export default function ProductCard({ product }: { product: Product }) {
  const category = getCategoryBySlug(product.priceCategory);

  return (
    <a
      href={product.shopeeUrl}
      target="_blank"
      rel="noopener noreferrer"
      className="group block bg-white rounded-lg shadow hover:shadow-lg transition-all hover:-translate-y-1"
    >
      <div className="relative aspect-square overflow-hidden rounded-t-lg bg-gray-100">
        <Image
          src={product.imageUrl || "/placeholder.png"}
          alt={product.name}
          fill
          className="object-cover"
          sizes="(max-width: 640px) 50vw, (max-width: 1024px) 33vw, 25vw"
          unoptimized={product.imageUrl?.startsWith("http")}
        />
        {product.discount && (
          <span className="absolute top-2 right-2 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">
            -{product.discount}%
          </span>
        )}
      </div>
      <div className="p-3">
        <h3 className="text-sm font-medium line-clamp-2 min-h-[2.5rem]">
          {product.name}
        </h3>
        <p className="text-[var(--color-brand-600)] font-bold mt-1">
          {formatRupiah(product.price)}
        </p>
        {category && (
          <span
            className={`inline-block text-xs px-2 py-0.5 rounded mt-1 ${category.badgeBg} ${category.badgeColor}`}
          >
            {category.shortLabel}
          </span>
        )}
        {product.sold !== undefined && product.sold > 0 && (
          <p className="text-xs text-gray-400 mt-1">
            {product.sold.toLocaleString("id-ID")} terjual
          </p>
        )}
      </div>
    </a>
  );
}
```

- [ ] **Step 4: Create CategoryCard component**

Create `websites/barangunik/src/components/CategoryCard.tsx`:

```tsx
import Link from "next/link";
import type { CategoryConfig } from "@/lib/constants";

interface CategoryCardProps {
  category: CategoryConfig;
  count: number;
}

export default function CategoryCard({ category, count }: CategoryCardProps) {
  return (
    <Link
      href={`/kategori/${category.slug}`}
      className="block bg-white rounded-lg shadow hover:shadow-lg transition-all hover:-translate-y-1 p-6 text-center"
    >
      <span className="text-4xl">{category.emoji}</span>
      <h3 className="font-bold mt-2">{category.label}</h3>
      <p className="text-sm text-gray-500">{category.shortLabel}</p>
      <p className="text-xs text-gray-400 mt-1">{count} produk</p>
    </Link>
  );
}
```

- [ ] **Step 5: Create Pagination component**

Create `websites/barangunik/src/components/Pagination.tsx`:

```tsx
import Link from "next/link";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  baseUrl: string;
}

export default function Pagination({
  currentPage,
  totalPages,
  baseUrl,
}: PaginationProps) {
  if (totalPages <= 1) return null;

  const pages = Array.from({ length: totalPages }, (_, i) => i + 1);

  return (
    <nav className="flex justify-center gap-2 mt-8">
      {pages.map((page) => (
        <Link
          key={page}
          href={`${baseUrl}?page=${page}`}
          className={`px-3 py-2 rounded text-sm ${
            page === currentPage
              ? "bg-[var(--color-brand-500)] text-white"
              : "bg-white text-gray-700 hover:bg-gray-100"
          }`}
        >
          {page}
        </Link>
      ))}
    </nav>
  );
}
```

- [ ] **Step 6: Verify TypeScript compiles**

```bash
cd websites/barangunik && npx tsc --noEmit
```

Expected: no errors.

- [ ] **Step 7: Commit**

```bash
git add websites/barangunik/src/components/
git commit -m "feat(barangunik): add public components — Header, Footer, ProductCard, CategoryCard, Pagination"
```

---

## Task 7: Homepage + Category Page

**Files:**
- Modify: `websites/barangunik/src/app/page.tsx`
- Create: `websites/barangunik/src/app/kategori/[slug]/page.tsx`

- [ ] **Step 1: Build the homepage**

Replace `websites/barangunik/src/app/page.tsx`:

```tsx
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import ProductCard from "@/components/ProductCard";
import CategoryCard from "@/components/CategoryCard";
import { getAllProducts, getActiveProducts } from "@/lib/products";
import { CATEGORIES, FEATURED_PRODUCTS_COUNT } from "@/lib/constants";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  const allProducts = await getAllProducts();
  const activeProducts = getActiveProducts(allProducts);

  const categoryCounts = CATEGORIES.map((cat) => ({
    category: cat,
    count: activeProducts.filter((p) => p.priceCategory === cat.slug).length,
  }));

  const featured = activeProducts
    .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
    .slice(0, FEATURED_PRODUCTS_COUNT);

  return (
    <>
      <Header />
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Kategori Section */}
        <section>
          <h2 className="text-2xl font-bold mb-4">Kategori Harga</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
            {categoryCounts.map(({ category, count }) => (
              <CategoryCard key={category.slug} category={category} count={count} />
            ))}
          </div>
        </section>

        {/* Featured Products Section */}
        <section className="mt-12">
          <h2 className="text-2xl font-bold mb-4">Produk Terbaru</h2>
          {featured.length === 0 ? (
            <p className="text-gray-500">Belum ada produk. Tambahkan via dashboard admin.</p>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {featured.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          )}
        </section>
      </main>
      <Footer />
    </>
  );
}
```

- [ ] **Step 2: Build the category page**

Create `websites/barangunik/src/app/kategori/[slug]/page.tsx`:

```tsx
import { notFound } from "next/navigation";
import Link from "next/link";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import ProductCard from "@/components/ProductCard";
import Pagination from "@/components/Pagination";
import {
  getAllProducts,
  getActiveProducts,
  getProductsByCategory,
} from "@/lib/products";
import { CATEGORIES, PRODUCTS_PER_PAGE } from "@/lib/constants";
import { getCategoryBySlug } from "@/lib/format";
import type { Metadata } from "next";

export const dynamic = "force-dynamic";

interface PageProps {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ page?: string; sort?: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const category = getCategoryBySlug(slug);
  if (!category) return {};
  return {
    title: `Barang Unik ${category.label} (${category.shortLabel})`,
    description: `Temukan barang unik dan aneh dengan harga ${category.shortLabel} dari Shopee Indonesia.`,
  };
}

export default async function CategoryPage({ params, searchParams }: PageProps) {
  const { slug } = await params;
  const { page: pageStr, sort } = await searchParams;
  const category = getCategoryBySlug(slug);
  if (!category) notFound();

  const allProducts = await getAllProducts();
  const active = getActiveProducts(allProducts);
  let products = getProductsByCategory(active, slug);

  // Sort
  switch (sort) {
    case "termurah":
      products.sort((a, b) => a.price - b.price);
      break;
    case "termahal":
      products.sort((a, b) => b.price - a.price);
      break;
    default:
      products.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
  }

  // Pagination
  const currentPage = Math.max(1, parseInt(pageStr || "1", 10));
  const totalPages = Math.ceil(products.length / PRODUCTS_PER_PAGE);
  const paginated = products.slice(
    (currentPage - 1) * PRODUCTS_PER_PAGE,
    currentPage * PRODUCTS_PER_PAGE
  );

  return (
    <>
      <Header />
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Breadcrumb */}
        <nav className="text-sm text-gray-500 mb-4">
          <Link href="/" className="hover:text-[var(--color-brand-500)]">Home</Link>
          <span className="mx-2">&gt;</span>
          <span>{category.emoji} {category.label}</span>
        </nav>

        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold">
            {category.emoji} {category.label}
            <span className="text-sm font-normal text-gray-500 ml-2">
              ({products.length} produk)
            </span>
          </h1>

          {/* Sort */}
          <div className="flex gap-2 text-sm">
            {[
              { key: "terbaru", label: "Terbaru" },
              { key: "termurah", label: "Termurah" },
              { key: "termahal", label: "Termahal" },
            ].map(({ key, label }) => (
              <Link
                key={key}
                href={`/kategori/${slug}?sort=${key}`}
                className={`px-3 py-1 rounded ${
                  (sort || "terbaru") === key
                    ? "bg-[var(--color-brand-500)] text-white"
                    : "bg-white text-gray-700 hover:bg-gray-100"
                }`}
              >
                {label}
              </Link>
            ))}
          </div>
        </div>

        {paginated.length === 0 ? (
          <p className="text-gray-500">Belum ada produk di kategori ini.</p>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {paginated.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}

        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          baseUrl={`/kategori/${slug}${sort ? `?sort=${sort}` : ""}`}
        />
      </main>
      <Footer />
    </>
  );
}
```

- [ ] **Step 3: Start dev server and verify homepage loads**

```bash
cd websites/barangunik && npm run dev
```

Open http://localhost:3000 — should show "Kategori Harga" (5 cards with 0 count each) + "Produk Terbaru" (empty message since no blob data yet).

- [ ] **Step 4: Commit**

```bash
git add websites/barangunik/src/app/page.tsx websites/barangunik/src/app/kategori/
git commit -m "feat(barangunik): add homepage + category page with sort & pagination"
```

---

## Task 8: Admin Login Page

**Files:**
- Create: `websites/barangunik/src/app/admin/login/page.tsx`
- Create: `websites/barangunik/src/app/admin/layout.tsx`

- [ ] **Step 1: Create admin layout**

Create `websites/barangunik/src/app/admin/layout.tsx`:

```tsx
import Link from "next/link";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-gray-900 text-white px-4 py-3">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <Link href="/admin" className="font-bold text-lg">
            BarangUnik Admin
          </Link>
          <div className="flex gap-4 text-sm">
            <Link href="/admin" className="hover:text-orange-300">Dashboard</Link>
            <Link href="/admin/tambah" className="hover:text-orange-300">Tambah Produk</Link>
            <Link href="/" className="hover:text-orange-300" target="_blank">Lihat Site</Link>
            <form action="/api/auth" method="dialog">
              <button
                type="button"
                className="hover:text-red-300"
                onClick="fetch('/api/auth',{method:'DELETE'}).then(()=>location.href='/admin/login')"
              >
                Logout
              </button>
            </form>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto px-4 py-6">{children}</main>
    </div>
  );
}
```

Wait — the onClick with a string won't work in React. Fix it as a client component button:

Replace the layout with:

```tsx
import Link from "next/link";
import LogoutButton from "./LogoutButton";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-gray-900 text-white px-4 py-3">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <Link href="/admin" className="font-bold text-lg">
            BarangUnik Admin
          </Link>
          <div className="flex items-center gap-4 text-sm">
            <Link href="/admin" className="hover:text-orange-300">Dashboard</Link>
            <Link href="/admin/tambah" className="hover:text-orange-300">Tambah Produk</Link>
            <Link href="/" className="hover:text-orange-300" target="_blank">Lihat Site</Link>
            <LogoutButton />
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto px-4 py-6">{children}</main>
    </div>
  );
}
```

- [ ] **Step 2: Create LogoutButton client component**

Create `websites/barangunik/src/app/admin/LogoutButton.tsx`:

```tsx
"use client";

import { useRouter } from "next/navigation";

export default function LogoutButton() {
  const router = useRouter();

  async function handleLogout() {
    await fetch("/api/auth", { method: "DELETE" });
    router.push("/admin/login");
  }

  return (
    <button onClick={handleLogout} className="hover:text-red-300">
      Logout
    </button>
  );
}
```

- [ ] **Step 3: Create login page**

Create `websites/barangunik/src/app/admin/login/page.tsx`:

```tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");

    const res = await fetch("/api/auth", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (res.ok) {
      router.push("/admin");
    } else {
      const data = await res.json();
      setError(data.error || "Login gagal");
    }
    setLoading(false);
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-sm">
        <h1 className="text-2xl font-bold text-center mb-6">BarangUnik Admin</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Username
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500"
              required
            />
          </div>
          {error && (
            <p className="text-red-500 text-sm">{error}</p>
          )}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[var(--color-brand-500)] text-white py-2 rounded font-medium hover:bg-[var(--color-brand-600)] disabled:opacity-50"
          >
            {loading ? "Loading..." : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
}
```

- [ ] **Step 4: Verify login page loads**

```bash
cd websites/barangunik && npm run dev
```

Open http://localhost:3000/admin — should redirect to `/admin/login`. Enter username `admin`, password `barangunik2026` — should redirect back to `/admin`.

- [ ] **Step 5: Commit**

```bash
git add websites/barangunik/src/app/admin/
git commit -m "feat(barangunik): add admin login page + layout + logout"
```

---

## Task 9: Admin Dashboard — Product Table + Stats

**Files:**
- Create: `websites/barangunik/src/app/admin/page.tsx`

- [ ] **Step 1: Create admin dashboard page**

Create `websites/barangunik/src/app/admin/page.tsx`:

```tsx
"use client";

import { useState, useEffect, useCallback } from "react";
import Image from "next/image";
import Link from "next/link";
import { formatRupiah } from "@/lib/format";
import { CATEGORIES } from "@/lib/constants";
import type { Product, PriceCategory, ProductStatus } from "@/lib/types";

export default function AdminDashboard() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [filterCategory, setFilterCategory] = useState("");
  const [filterStatus, setFilterStatus] = useState("");

  const fetchProducts = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (search) params.set("search", search);
    if (filterCategory) params.set("category", filterCategory);
    if (filterStatus) params.set("status", filterStatus);
    const res = await fetch(`/api/products?${params}`);
    const data = await res.json();
    setProducts(data);
    setLoading(false);
  }, [search, filterCategory, filterStatus]);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  async function handleDelete(id: string) {
    if (!confirm("Hapus produk ini?")) return;
    await fetch(`/api/products/${id}`, { method: "DELETE" });
    fetchProducts();
  }

  async function handleToggleStatus(id: string, currentStatus: ProductStatus) {
    const newStatus = currentStatus === "active" ? "hidden" : "active";
    await fetch(`/api/products/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus }),
    });
    fetchProducts();
  }

  async function handleImport(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    const text = await file.text();
    const data = JSON.parse(text);
    const res = await fetch("/api/products", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const result = await res.json();
    alert(`Imported ${result.imported} produk baru (status: pending)`);
    fetchProducts();
    e.target.value = "";
  }

  // Stats
  const allProducts = products;
  const stats = CATEGORIES.map((cat) => ({
    label: `${cat.emoji} ${cat.label}`,
    count: allProducts.filter((p) => p.priceCategory === cat.slug).length,
  }));

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-4 mb-6">
        {stats.map((s) => (
          <div key={s.label} className="bg-white rounded-lg p-4 shadow text-center">
            <p className="text-2xl font-bold">{s.count}</p>
            <p className="text-xs text-gray-500">{s.label}</p>
          </div>
        ))}
      </div>

      {/* Actions */}
      <div className="flex flex-wrap gap-3 mb-6">
        <Link
          href="/admin/tambah"
          className="bg-[var(--color-brand-500)] text-white px-4 py-2 rounded hover:bg-[var(--color-brand-600)]"
        >
          + Tambah Produk
        </Link>
        <label className="bg-blue-500 text-white px-4 py-2 rounded cursor-pointer hover:bg-blue-600">
          Import Hasil Scrape
          <input type="file" accept=".json" onChange={handleImport} className="hidden" />
        </label>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-4">
        <input
          type="text"
          placeholder="Cari produk..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border rounded px-3 py-2 text-sm w-64"
        />
        <select
          value={filterCategory}
          onChange={(e) => setFilterCategory(e.target.value)}
          className="border rounded px-3 py-2 text-sm"
        >
          <option value="">Semua Kategori</option>
          {CATEGORIES.map((cat) => (
            <option key={cat.slug} value={cat.slug}>
              {cat.emoji} {cat.label}
            </option>
          ))}
        </select>
        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          className="border rounded px-3 py-2 text-sm"
        >
          <option value="">Semua Status</option>
          <option value="active">Active</option>
          <option value="hidden">Hidden</option>
          <option value="pending">Pending</option>
        </select>
      </div>

      {/* Table */}
      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-left">
              <tr>
                <th className="px-4 py-3">Image</th>
                <th className="px-4 py-3">Nama</th>
                <th className="px-4 py-3">Harga</th>
                <th className="px-4 py-3">Kategori</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Aksi</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {products.map((product) => {
                const cat = CATEGORIES.find((c) => c.slug === product.priceCategory);
                return (
                  <tr key={product.id} className="hover:bg-gray-50">
                    <td className="px-4 py-2">
                      <Image
                        src={product.imageUrl || "/placeholder.png"}
                        alt=""
                        width={40}
                        height={40}
                        className="rounded object-cover"
                        unoptimized={product.imageUrl?.startsWith("http")}
                      />
                    </td>
                    <td className="px-4 py-2 max-w-xs truncate">{product.name}</td>
                    <td className="px-4 py-2 whitespace-nowrap">{formatRupiah(product.price)}</td>
                    <td className="px-4 py-2">
                      {cat && (
                        <span className={`text-xs px-2 py-0.5 rounded ${cat.badgeBg} ${cat.badgeColor}`}>
                          {cat.label}
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-2">
                      <span
                        className={`text-xs px-2 py-0.5 rounded ${
                          product.status === "active"
                            ? "bg-green-100 text-green-800"
                            : product.status === "pending"
                            ? "bg-yellow-100 text-yellow-800"
                            : "bg-gray-100 text-gray-600"
                        }`}
                      >
                        {product.status}
                      </span>
                    </td>
                    <td className="px-4 py-2">
                      <div className="flex gap-2">
                        <Link
                          href={`/admin/edit/${product.id}`}
                          className="text-blue-500 hover:underline"
                        >
                          Edit
                        </Link>
                        <button
                          onClick={() => handleToggleStatus(product.id, product.status)}
                          className="text-yellow-600 hover:underline"
                        >
                          {product.status === "active" ? "Hide" : "Activate"}
                        </button>
                        <button
                          onClick={() => handleDelete(product.id)}
                          className="text-red-500 hover:underline"
                        >
                          Hapus
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
              {products.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-gray-500">
                    Belum ada produk.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 2: Verify dashboard loads**

```bash
cd websites/barangunik && npm run dev
```

Login at `/admin/login`, then verify dashboard shows at `/admin` — empty table + stats + import button.

- [ ] **Step 3: Commit**

```bash
git add websites/barangunik/src/app/admin/page.tsx
git commit -m "feat(barangunik): add admin dashboard — stats, product table, search, filter, import"
```

---

## Task 10: Admin Add/Edit Product Form with Live Preview

**Files:**
- Create: `websites/barangunik/src/components/ProductForm.tsx`
- Create: `websites/barangunik/src/app/admin/tambah/page.tsx`
- Create: `websites/barangunik/src/app/admin/edit/[id]/page.tsx`

- [ ] **Step 1: Create shared ProductForm component**

Create `websites/barangunik/src/components/ProductForm.tsx`:

```tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import ProductCard from "./ProductCard";
import { getPriceCategory } from "@/lib/format";
import { CATEGORIES } from "@/lib/constants";
import type { Product, PriceCategory, ProductStatus } from "@/lib/types";

interface ProductFormProps {
  initial?: Product;
  mode: "create" | "edit";
}

export default function ProductForm({ initial, mode }: ProductFormProps) {
  const router = useRouter();
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({
    name: initial?.name || "",
    price: initial?.price || 0,
    shopeeUrl: initial?.shopeeUrl || "",
    imageUrl: initial?.imageUrl || "",
    discount: initial?.discount || 0,
    priceCategory: initial?.priceCategory || ("dibawah-20rb" as PriceCategory),
    status: initial?.status || ("active" as ProductStatus),
  });

  function handleChange(field: string, value: string | number) {
    setForm((prev) => {
      const next = { ...prev, [field]: value };
      if (field === "price") {
        next.priceCategory = getPriceCategory(value as number);
      }
      return next;
    });
  }

  // Build preview product object
  const preview: Product = {
    id: initial?.id || "preview",
    name: form.name || "Nama Produk",
    price: form.price,
    priceCategory: form.priceCategory,
    discount: form.discount || undefined,
    imageUrl: form.imageUrl,
    shopeeUrl: form.shopeeUrl,
    status: form.status,
    createdAt: initial?.createdAt || new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);

    const url =
      mode === "create"
        ? "/api/products"
        : `/api/products/${initial!.id}`;
    const method = mode === "create" ? "POST" : "PUT";

    await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    setSaving(false);
    router.push("/admin");
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      {/* Form */}
      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Nama Produk</label>
          <input
            type="text"
            value={form.name}
            onChange={(e) => handleChange("name", e.target.value)}
            className="w-full border rounded px-3 py-2"
            required
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Harga (Rp)</label>
            <input
              type="number"
              value={form.price}
              onChange={(e) => handleChange("price", parseInt(e.target.value) || 0)}
              className="w-full border rounded px-3 py-2"
              required
              min={0}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Diskon (%)</label>
            <input
              type="number"
              value={form.discount}
              onChange={(e) => handleChange("discount", parseInt(e.target.value) || 0)}
              className="w-full border rounded px-3 py-2"
              min={0}
              max={100}
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Link Shopee</label>
          <input
            type="url"
            value={form.shopeeUrl}
            onChange={(e) => handleChange("shopeeUrl", e.target.value)}
            className="w-full border rounded px-3 py-2"
            placeholder="https://shopee.co.id/..."
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Image URL</label>
          <input
            type="text"
            value={form.imageUrl}
            onChange={(e) => handleChange("imageUrl", e.target.value)}
            className="w-full border rounded px-3 py-2"
            placeholder="https://cf.shopee.co.id/file/..."
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Kategori Harga</label>
            <select
              value={form.priceCategory}
              onChange={(e) => handleChange("priceCategory", e.target.value)}
              className="w-full border rounded px-3 py-2"
            >
              {CATEGORIES.map((cat) => (
                <option key={cat.slug} value={cat.slug}>
                  {cat.emoji} {cat.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Status</label>
            <select
              value={form.status}
              onChange={(e) => handleChange("status", e.target.value)}
              className="w-full border rounded px-3 py-2"
            >
              <option value="active">Active</option>
              <option value="hidden">Hidden</option>
              <option value="pending">Pending</option>
            </select>
          </div>
        </div>

        <button
          type="submit"
          disabled={saving}
          className="w-full bg-[var(--color-brand-500)] text-white py-2 rounded font-medium hover:bg-[var(--color-brand-600)] disabled:opacity-50"
        >
          {saving ? "Menyimpan..." : mode === "create" ? "Tambah Produk" : "Simpan Perubahan"}
        </button>
      </form>

      {/* Preview */}
      <div>
        <h3 className="text-sm font-medium text-gray-500 mb-3">Preview Card</h3>
        <div className="w-56">
          <ProductCard product={preview} />
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Create Tambah (Add) page**

Create `websites/barangunik/src/app/admin/tambah/page.tsx`:

```tsx
import ProductForm from "@/components/ProductForm";

export default function TambahPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Tambah Produk</h1>
      <ProductForm mode="create" />
    </div>
  );
}
```

- [ ] **Step 3: Create Edit page**

Create `websites/barangunik/src/app/admin/edit/[id]/page.tsx`:

```tsx
import { notFound } from "next/navigation";
import { getProductById } from "@/lib/products";
import ProductForm from "@/components/ProductForm";

interface PageProps {
  params: Promise<{ id: string }>;
}

export default async function EditPage({ params }: PageProps) {
  const { id } = await params;
  const product = await getProductById(id);
  if (!product) notFound();

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Edit Produk</h1>
      <ProductForm mode="edit" initial={product} />
    </div>
  );
}
```

- [ ] **Step 4: Verify add product form works**

```bash
cd websites/barangunik && npm run dev
```

Go to `/admin/tambah` — form should show with live preview on the right.

- [ ] **Step 5: Commit**

```bash
git add websites/barangunik/src/components/ProductForm.tsx websites/barangunik/src/app/admin/tambah/ websites/barangunik/src/app/admin/edit/
git commit -m "feat(barangunik): add product form with live preview — create + edit pages"
```

---

## Task 11: Python Scraper — Shopee Product Discovery

**Files:**
- Create: `websites/barangunik/scripts/scrape-shopee.py`

- [ ] **Step 1: Create the Shopee scraper script**

Create `websites/barangunik/scripts/scrape-shopee.py`:

```python
#!/usr/bin/env python3
"""
Shopee Product Scraper — BarangUnik
Searches for unique/weird products on Shopee Indonesia.
Outputs products.json for import into the admin dashboard.

Usage:
    python3 scrape-shopee.py
    python3 scrape-shopee.py --limit 10
"""

import json
import time
import random
import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("Installing requests...")
    import subprocess
    subprocess.check_call(["pip3", "install", "requests"])
    import requests

KEYWORDS = [
    "barang unik",
    "barang aneh",
    "barang lucu",
    "gadget unik",
    "alat dapur unik",
    "hadiah unik",
    "barang viral",
    "barang anti mainstream",
    "mainan unik",
    "dekorasi unik",
]

SHOPEE_SEARCH_URL = "https://shopee.co.id/api/v4/search/search_items"

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
]

PRICE_CATEGORIES = [
    ("dibawah-20rb", 0, 19999),
    ("20rb-50rb", 20000, 50000),
    ("50rb-100rb", 50001, 100000),
    ("100rb-500rb", 100001, 500000),
    ("diatas-500rb", 500001, float("inf")),
]


def get_price_category(price: int) -> str:
    for slug, min_price, max_price in PRICE_CATEGORIES:
        if min_price <= price <= max_price:
            return slug
    return "diatas-500rb"


def search_shopee(keyword: str, limit: int = 30) -> list:
    """Search Shopee for products matching keyword."""
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json",
        "Referer": "https://shopee.co.id/",
        "X-Requested-With": "XMLHttpRequest",
    }

    params = {
        "keyword": keyword,
        "limit": limit,
        "newest": 0,
        "order": "relevancy",
        "page_type": "search",
        "scenario": "PAGE_GLOBAL_SEARCH",
        "version": 2,
    }

    try:
        response = requests.get(
            SHOPEE_SEARCH_URL,
            params=params,
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("items", [])
    except Exception as e:
        print(f"  Error searching '{keyword}': {e}")
        return []


def extract_product(item: dict) -> dict | None:
    """Extract product data from Shopee search result item."""
    try:
        info = item.get("item_basic", item)
        shop_id = info.get("shopid", 0)
        item_id = info.get("itemid", 0)

        price_raw = info.get("price", 0)
        # Shopee prices are in units of 100000 (IDR * 100000)
        price = price_raw // 100000 if price_raw > 100000 else price_raw

        if price <= 0:
            return None

        name = info.get("name", "")
        if not name:
            return None

        # Image
        image_hash = info.get("image", "")
        image_url = f"https://cf.shopee.co.id/file/{image_hash}" if image_hash else ""

        # Discount
        raw_discount = info.get("raw_discount", 0)
        discount = int(raw_discount) if raw_discount else None

        # Rating
        rating_star = info.get("item_rating", {}).get("rating_star", None)

        # Sold
        sold = info.get("sold", 0)
        if isinstance(sold, dict):
            sold = sold.get("sold", 0)

        # Shopee URL
        slug = name.lower().replace(" ", "-")[:80]
        shopee_url = f"https://shopee.co.id/{slug}-i.{shop_id}.{item_id}"

        now = datetime.now(timezone.utc).isoformat()
        product_id = f"shopee_{shop_id}_{item_id}"

        return {
            "id": product_id,
            "name": name,
            "price": price,
            "priceCategory": get_price_category(price),
            "discount": discount,
            "imageUrl": image_url,
            "shopeeUrl": shopee_url,
            "rating": round(rating_star, 1) if rating_star else None,
            "sold": sold,
            "status": "pending",
            "scrapedAt": now,
            "createdAt": now,
            "updatedAt": now,
        }
    except Exception as e:
        print(f"  Error extracting product: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Scrape unique products from Shopee")
    parser.add_argument("--limit", type=int, default=30, help="Products per keyword (default: 30)")
    parser.add_argument("--output", type=str, default="products.json", help="Output file")
    parser.add_argument("--keywords", type=str, nargs="*", help="Custom keywords (overrides defaults)")
    args = parser.parse_args()

    keywords = args.keywords or KEYWORDS
    all_products = {}

    print(f"Scraping Shopee for {len(keywords)} keywords, {args.limit} products each...")
    print()

    for i, keyword in enumerate(keywords, 1):
        print(f"[{i}/{len(keywords)}] Searching: '{keyword}'...")
        items = search_shopee(keyword, args.limit)
        print(f"  Found {len(items)} results")

        for item in items:
            product = extract_product(item)
            if product and product["id"] not in all_products:
                all_products[product["id"]] = product

        # Be nice to Shopee servers
        if i < len(keywords):
            delay = random.uniform(2, 5)
            print(f"  Waiting {delay:.1f}s...")
            time.sleep(delay)

    products_list = list(all_products.values())

    # Stats
    print()
    print(f"Total unique products: {len(products_list)}")
    for slug, _, _ in PRICE_CATEGORIES:
        count = sum(1 for p in products_list if p["priceCategory"] == slug)
        print(f"  {slug}: {count}")

    # Save
    output_path = Path(__file__).parent / args.output
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(products_list, f, ensure_ascii=False, indent=2)

    print(f"\nSaved to {output_path}")
    print(f"Import this file via the admin dashboard 'Import Hasil Scrape' button.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test scraper runs (dry run)**

```bash
cd websites/barangunik && python3 scripts/scrape-shopee.py --limit 5 --keywords "barang unik"
```

Expected: fetches products from Shopee, saves to `scripts/products.json`. If Shopee blocks the API, the script prints an error and produces an empty list — that's OK for now. The import flow works regardless of scraper success.

- [ ] **Step 3: Commit**

```bash
git add websites/barangunik/scripts/scrape-shopee.py
git commit -m "feat(barangunik): add Python Shopee product scraper"
```

---

## Task 12: SEO — Sitemap + JSON-LD + Meta Tags

**Files:**
- Modify: `websites/barangunik/next.config.ts`
- Modify: `websites/barangunik/src/app/layout.tsx`
- Create: `websites/barangunik/src/app/sitemap.ts`

- [ ] **Step 1: Configure Next.js for image domains**

Replace `websites/barangunik/next.config.ts`:

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "cf.shopee.co.id",
      },
      {
        protocol: "https",
        hostname: "down-id.img.susercontent.com",
      },
    ],
  },
};

export default nextConfig;
```

- [ ] **Step 2: Create dynamic sitemap**

Create `websites/barangunik/src/app/sitemap.ts`:

```typescript
import { MetadataRoute } from "next";
import { getAllProducts, getActiveProducts } from "@/lib/products";
import { CATEGORIES } from "@/lib/constants";

export const dynamic = "force-dynamic";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://barangunik.vercel.app";

  const staticPages: MetadataRoute.Sitemap = [
    { url: baseUrl, lastModified: new Date(), changeFrequency: "daily", priority: 1 },
  ];

  // Category pages
  const categoryPages: MetadataRoute.Sitemap = CATEGORIES.map((cat) => ({
    url: `${baseUrl}/kategori/${cat.slug}`,
    lastModified: new Date(),
    changeFrequency: "daily" as const,
    priority: 0.8,
  }));

  return [...staticPages, ...categoryPages];
}
```

- [ ] **Step 3: Add JSON-LD to layout**

Modify `websites/barangunik/src/app/layout.tsx` — add JSON-LD script in the `<head>`:

Replace the existing layout with:

```tsx
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "BarangUnik — Barang Unik & Aneh dari Shopee",
    template: "%s | BarangUnik",
  },
  description:
    "Temukan barang unik, aneh, dan lucu dari Shopee Indonesia. Dikategorikan berdasarkan harga.",
  openGraph: {
    title: "BarangUnik — Barang Unik & Aneh dari Shopee",
    description: "Temukan barang unik, aneh, dan lucu dari Shopee Indonesia.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: "BarangUnik",
    description: "Temukan barang unik, aneh, dan lucu dari Shopee Indonesia.",
    url: process.env.NEXT_PUBLIC_SITE_URL || "https://barangunik.vercel.app",
  };

  return (
    <html lang="id">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body className="bg-gray-50 text-gray-900 antialiased">{children}</body>
    </html>
  );
}
```

- [ ] **Step 4: Verify build passes**

```bash
cd websites/barangunik && npm run build
```

Expected: build succeeds with no errors.

- [ ] **Step 5: Commit**

```bash
git add websites/barangunik/next.config.ts websites/barangunik/src/app/sitemap.ts websites/barangunik/src/app/layout.tsx
git commit -m "feat(barangunik): add SEO — sitemap, JSON-LD, image domains"
```

---

## Task 13: Seed Data Upload + Initial Deploy to Vercel

**Files:**
- Create: `websites/barangunik/scripts/seed.ts`

- [ ] **Step 1: Create seed script**

Create `websites/barangunik/scripts/seed.ts`:

```typescript
/**
 * Seed script — uploads initial products to Vercel Blob.
 * Run: npx tsx scripts/seed.ts
 * Requires BLOB_READ_WRITE_TOKEN in .env.local
 */
import { put } from "@vercel/blob";
import { readFileSync } from "fs";
import { join } from "path";

async function seed() {
  const seedPath = join(__dirname, "..", "data", "seed.json");
  const data = readFileSync(seedPath, "utf-8");
  const products = JSON.parse(data);

  console.log(`Uploading ${products.length} seed products to Vercel Blob...`);

  const blob = await put("products.json", JSON.stringify(products, null, 2), {
    access: "public",
    addRandomSuffix: false,
    contentType: "application/json",
  });

  console.log(`Done! Blob URL: ${blob.url}`);
}

seed().catch(console.error);
```

- [ ] **Step 2: Install tsx for running TypeScript scripts**

```bash
cd websites/barangunik && npm install -D tsx
```

- [ ] **Step 3: Link project to Vercel**

```bash
cd websites/barangunik && npx vercel link
```

Follow prompts: select scope, link to existing project or create new one named "barangunik".

- [ ] **Step 4: Add Vercel Blob storage**

Go to Vercel dashboard → project "barangunik" → Storage → Add → Blob Store → Create.

Or via CLI:
```bash
cd websites/barangunik && npx vercel env pull .env.local
```

This pulls the `BLOB_READ_WRITE_TOKEN` into `.env.local`.

- [ ] **Step 5: Run seed script**

```bash
cd websites/barangunik && npx tsx scripts/seed.ts
```

Expected: "Uploading 10 seed products to Vercel Blob..." then "Done! Blob URL: ..."

- [ ] **Step 6: Deploy to Vercel**

```bash
cd websites/barangunik && npx vercel --yes --prod
```

Expected: successful deployment. Note the production URL.

- [ ] **Step 7: Verify live site**

Open the Vercel URL — should see:
- 5 kategori cards with product counts
- 9 product cards (seed_010 is "pending" so not shown)
- Orange theme, responsive grid

Open `/admin/login` — login and verify dashboard works.

- [ ] **Step 8: Commit**

```bash
git add websites/barangunik/scripts/seed.ts websites/barangunik/package.json websites/barangunik/package-lock.json
git commit -m "feat(barangunik): add seed script + initial Vercel deployment"
```

---

## Summary

| Task | Description | Key Files |
|------|------------|-----------|
| 1 | Project scaffold + Tailwind theme | package.json, layout.tsx, globals.css |
| 2 | Types, constants, utilities | lib/types.ts, lib/constants.ts, lib/format.ts |
| 3 | Vercel Blob storage layer | lib/products.ts, data/seed.json |
| 4 | JWT auth + middleware | lib/auth.ts, api/auth/route.ts, middleware.ts |
| 5 | Products CRUD API | api/products/route.ts, api/products/[id]/route.ts |
| 6 | Public components | Header, Footer, ProductCard, CategoryCard, Pagination |
| 7 | Homepage + category page | page.tsx, kategori/[slug]/page.tsx |
| 8 | Admin login page | admin/login/page.tsx, admin/layout.tsx |
| 9 | Admin dashboard | admin/page.tsx |
| 10 | Add/edit product form | ProductForm.tsx, admin/tambah, admin/edit/[id] |
| 11 | Python scraper | scripts/scrape-shopee.py |
| 12 | SEO — sitemap + JSON-LD | sitemap.ts, next.config.ts, layout.tsx |
| 13 | Seed data + deploy | scripts/seed.ts, Vercel deployment |
