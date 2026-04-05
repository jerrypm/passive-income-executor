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
