import Link from "next/link";
import LogoutButton from "./LogoutButton";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-gray-900 text-white px-4 py-3">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <Link href="/admin" className="font-bold text-lg">
            BarangUnik Admin
          </Link>
          <div className="flex items-center gap-4 text-sm">
            <Link href="/admin" className="hover:text-orange-300">Dashboard</Link>
            <Link href="/admin/tambah" className="hover:text-orange-300">Tambah Produk</Link>
            <Link href="/" className="hover:text-orange-300" target="_blank">Lihat Site</Link>
            <LogoutButton />
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto px-4 py-6">{children}</main>
    </div>
  );
}
