"use client";

import { useState } from "react";
import Image from "next/image";
import { formatRupiah, getCategoryBySlug } from "@/lib/format";
import { toAffiliateLink } from "@/lib/affiliate";
import type { Product } from "@/lib/types";

export default function ProductCard({ product }: { product: Product }) {
  const category = getCategoryBySlug(product.priceCategory);
  const [imgSrc, setImgSrc] = useState(product.imageUrl || "/placeholder.png");
  const isExternal = imgSrc.startsWith("http");

  return (
    <a
      href={toAffiliateLink(product.shopeeUrl, `web-${product.priceCategory}-${product.id}`)}
      target="_blank"
      rel="noopener noreferrer"
      className="group block bg-white rounded-lg shadow hover:shadow-lg transition-all hover:-translate-y-1"
    >
      <div className="relative aspect-square overflow-hidden rounded-t-lg bg-gray-100">
        <Image
          src={imgSrc}
          alt={product.name}
          fill
          className="object-cover"
          sizes="(max-width: 640px) 50vw, (max-width: 1024px) 33vw, 25vw"
          unoptimized={isExternal}
          onError={() => setImgSrc("/placeholder.png")}
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
