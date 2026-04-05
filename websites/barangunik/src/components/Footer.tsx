export default function Footer() {
  return (
    <footer className="bg-gray-800 text-gray-400 py-8 mt-12">
      <div className="max-w-7xl mx-auto px-4 text-center text-sm">
        <p>&copy; {new Date().getFullYear()} BarangUnik. Semua harga dari Shopee.</p>
        <p className="mt-1">
          Harga dan ketersediaan dapat berubah sewaktu-waktu.
        </p>
      </div>
    </footer>
  );
}
