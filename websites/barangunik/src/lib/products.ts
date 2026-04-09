import { put, list } from "@vercel/blob";
import type { Product } from "./types";

const BLOB_FILENAME = "products.json";

export async function getAllProducts(): Promise<Product[]> {
  try {
    const { blobs } = await list({ prefix: BLOB_FILENAME });
    if (blobs.length === 0) return [];
    // Cache bust: unique query param forces CDN to fetch from origin
    const url = new URL(blobs[0].url);
    url.searchParams.set("t", Date.now().toString());
    const response = await fetch(url.toString(), { cache: "no-store" });
    return (await response.json()) as Product[];
  } catch (err) {
    console.error("getAllProducts error:", err);
    return [];
  }
}

export async function saveAllProducts(products: Product[]): Promise<void> {
  await put(BLOB_FILENAME, JSON.stringify(products, null, 2), {
    access: "public",
    addRandomSuffix: false,
    allowOverwrite: true,
    contentType: "application/json",
    cacheControlMaxAge: 60,
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
