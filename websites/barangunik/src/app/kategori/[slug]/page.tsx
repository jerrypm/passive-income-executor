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
