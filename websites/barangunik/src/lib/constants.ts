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
