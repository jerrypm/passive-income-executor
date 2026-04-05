import Link from "next/link";

export default function Header() {
  return (
    <header className="bg-[var(--color-brand-500)] text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-2xl font-bold">BarangUnik</span>
        </Link>
        <p className="hidden sm:block text-sm text-orange-100">
          Temukan Barang Unik &amp; Aneh dari Shopee
        </p>
      </div>
    </header>
  );
}
