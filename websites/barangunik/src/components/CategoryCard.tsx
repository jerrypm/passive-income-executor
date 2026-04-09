import Link from "next/link";
import CategoryIcon from "./CategoryIcon";
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
      <CategoryIcon category={category} size="lg" />
      <h3 className="font-bold mt-2">{category.label}</h3>
      <p className="text-sm text-gray-500">{category.shortLabel}</p>
      <p className="text-xs text-gray-400 mt-1">{count} produk</p>
    </Link>
  );
}
