import Link from "next/link";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export default function NotFound() {
  return (
    <>
      <Header />
      <main className="max-w-7xl mx-auto px-4 py-16 text-center">
        <h1 className="text-4xl font-bold mb-4">404</h1>
        <p className="text-gray-500 mb-6">Halaman tidak ditemukan.</p>
        <Link
          href="/"
          className="inline-block bg-[var(--color-brand-500)] text-white px-6 py-2 rounded hover:bg-[var(--color-brand-600)]"
        >
          Kembali ke Beranda
        </Link>
      </main>
      <Footer />
    </>
  );
}
