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
