"use client";

import { useState, useEffect, useCallback, useMemo } from "react";
import Link from "next/link";
import { formatRupiah } from "@/lib/format";
import { CATEGORIES, STATUS_OPTIONS } from "@/lib/constants";
import CategoryIcon from "@/components/CategoryIcon";
import type { Product, ProductStatus } from "@/lib/types";

export default function AdminDashboard() {
  const [allProducts, setAllProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [filterCategory, setFilterCategory] = useState("");
  const [filterStatus, setFilterStatus] = useState("");

  const fetchProducts = useCallback(async () => {
    setLoading(true);
    const res = await fetch("/api/products");
    if (!res.ok) {
      setLoading(false);
      return;
    }
    const data = await res.json();
    setAllProducts(data);
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  const products = useMemo(() => {
    let filtered = allProducts;
    if (search) {
      const q = search.toLowerCase();
      filtered = filtered.filter((p) => p.name.toLowerCase().includes(q));
    }
    if (filterCategory) filtered = filtered.filter((p) => p.priceCategory === filterCategory);
    if (filterStatus) filtered = filtered.filter((p) => p.status === filterStatus);
    return filtered;
  }, [allProducts, search, filterCategory, filterStatus]);

  async function handleDelete(id: string) {
    if (!confirm("Hapus produk ini?")) return;
    const res = await fetch(`/api/products/${id}`, { method: "DELETE" });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      alert(data.error || "Gagal menghapus produk");
      return;
    }
    fetchProducts();
  }

  async function handleToggleStatus(id: string, currentStatus: ProductStatus) {
    const newStatus = currentStatus === "active" ? "hidden" : "active";
    const res = await fetch(`/api/products/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus }),
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      alert(data.error || "Gagal mengubah status");
      return;
    }
    fetchProducts();
  }

  async function handleImport(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    const text = await file.text();
    let data;
    try {
      data = JSON.parse(text);
    } catch {
      alert("File JSON tidak valid");
      e.target.value = "";
      return;
    }
    const res = await fetch("/api/products", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      alert(err.error || "Gagal import produk");
      e.target.value = "";
      return;
    }
    const result = await res.json();
    alert(`Imported ${result.imported} produk baru (status: pending)`);
    fetchProducts();
    e.target.value = "";
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-4 mb-6">
        {CATEGORIES.map((cat) => (
          <div key={cat.slug} className="bg-white rounded-lg p-4 shadow text-center flex flex-col items-center gap-2">
            <CategoryIcon category={cat} size="sm" />
            <p className="text-2xl font-bold">{allProducts.filter((p) => p.priceCategory === cat.slug).length}</p>
            <p className="text-xs text-gray-500">{cat.label}</p>
          </div>
        ))}
      </div>

      {/* Actions */}
      <div className="flex flex-wrap gap-3 mb-6">
        <Link
          href="/admin/tambah"
          className="bg-[var(--color-brand-500)] text-white px-4 py-2 rounded hover:bg-[var(--color-brand-600)]"
        >
          + Tambah Produk
        </Link>
        <label className="bg-blue-500 text-white px-4 py-2 rounded cursor-pointer hover:bg-blue-600">
          Import Hasil Scrape
          <input type="file" accept=".json" onChange={handleImport} className="hidden" aria-label="Import produk dari file JSON" />
        </label>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-4">
        <input
          type="text"
          placeholder="Cari produk..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border rounded px-3 py-2 text-sm w-64 focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-500)]"
        />
        <select
          value={filterCategory}
          onChange={(e) => setFilterCategory(e.target.value)}
          className="border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-500)]"
        >
          <option value="">Semua Kategori</option>
          {CATEGORIES.map((cat) => (
            <option key={cat.slug} value={cat.slug}>
              {cat.emoji} {cat.label}
            </option>
          ))}
        </select>
        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          className="border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-500)]"
        >
          <option value="">Semua Status</option>
          {STATUS_OPTIONS.map((s) => (
            <option key={s.value} value={s.value}>{s.label}</option>
          ))}
        </select>
      </div>

      {/* Table */}
      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-left">
              <tr>
                <th className="px-4 py-3">Image</th>
                <th className="px-4 py-3">Nama</th>
                <th className="px-4 py-3">Harga</th>
                <th className="px-4 py-3">Kategori</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Aksi</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {products.map((product) => {
                const cat = CATEGORIES.find((c) => c.slug === product.priceCategory);
                return (
                  <tr key={product.id} className="hover:bg-gray-50">
                    <td className="px-4 py-2">
                      <img
                        src={product.imageUrl || "/placeholder.png"}
                        alt={product.name}
                        width={40}
                        height={40}
                        className="rounded object-cover"
                        onError={(e) => { e.currentTarget.src = "/placeholder.png"; }}
                      />
                    </td>
                    <td className="px-4 py-2 max-w-xs truncate">{product.name}</td>
                    <td className="px-4 py-2 whitespace-nowrap">{formatRupiah(product.price)}</td>
                    <td className="px-4 py-2">
                      {cat && (
                        <span className={`text-xs px-2 py-0.5 rounded ${cat.badgeBg} ${cat.badgeColor}`}>
                          {cat.label}
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-2">
                      {(() => {
                        const st = STATUS_OPTIONS.find((s) => s.value === product.status);
                        return (
                          <span className={`text-xs px-2 py-0.5 rounded ${st?.badgeBg ?? ""} ${st?.badgeColor ?? ""}`}>
                            {product.status}
                          </span>
                        );
                      })()}
                    </td>
                    <td className="px-4 py-2">
                      <div className="flex gap-2">
                        <Link
                          href={`/admin/edit/${product.id}`}
                          className="text-blue-500 hover:underline"
                        >
                          Edit
                        </Link>
                        <button
                          onClick={() => handleToggleStatus(product.id, product.status)}
                          className="text-yellow-600 hover:underline"
                        >
                          {product.status === "active" ? "Hide" : "Activate"}
                        </button>
                        <button
                          onClick={() => handleDelete(product.id)}
                          className="text-red-500 hover:underline"
                        >
                          Hapus
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
              {products.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-gray-500">
                    Belum ada produk.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
