# BarangUnik Data Refresh Fix — Implementation Plan

**Date:** 2026-04-05
**Problem:** All CRUD operations (delete, update, toggle status) appear broken — changes don't persist on page reload.

## Root Cause

`saveAllProducts()` writes to **public** Vercel Blob with default `cacheControlMaxAge` of **1 MONTH**.
`getAllProducts()` reads via CDN URL → serves stale cached data → mutations appear to fail.

## Solution

Switch from public blobs (CDN-cached) to **private blobs** with `get()` using `useCache: false` — bypasses CDN entirely.

## Steps

### Step 1: Rewrite `src/lib/products.ts`

- Import `get` from `@vercel/blob` (available in v2.3.3)
- `getAllProducts()`:
  - Primary: `get(BLOB_FILENAME, { access: "private", useCache: false })` → read stream → parse JSON
  - Fallback: if `null` (blob not found), try old public blob via `list()` + `fetch()` for one-time migration
- `saveAllProducts()`:
  - Change `access: "public"` → `access: "private"`
  - Remove `cacheControlMaxAge` dependency (private blobs don't use CDN)
- Remove `?_=${Date.now()}` hack (no longer needed for primary path)

**Migration flow:** First mutation (add/edit/delete) after deploy reads from public blob (fallback), writes to private blob. All subsequent reads use private blob with `useCache: false`.

### Step 2: Clean up `src/app/admin/page.tsx`

- `handleDelete`: Check `res.ok`, show error if failed
- `handleToggleStatus`: Check `res.ok`, show error if failed
- Add toast/alert feedback for errors

### Step 3: Deploy + Verify

- `cd websites/barangunik && vercel --yes --prod`
- Verify: https://barangunik.vercel.app/admin — delete, edit, toggle should work instantly
