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
