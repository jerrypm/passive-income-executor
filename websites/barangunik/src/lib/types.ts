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
