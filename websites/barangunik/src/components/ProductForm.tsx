"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import ProductCard from "./ProductCard";
import { getPriceCategory } from "@/lib/format";
import { CATEGORIES, STATUS_OPTIONS } from "@/lib/constants";
import type { Product, PriceCategory, ProductStatus } from "@/lib/types";

interface ProductFormProps {
  initial?: Product;
  mode: "create" | "edit";
}

export default function ProductForm({ initial, mode }: ProductFormProps) {
  const router = useRouter();
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    name: initial?.name || "",
    price: initial?.price || 0,
    shopeeUrl: initial?.shopeeUrl || "",
    imageUrl: initial?.imageUrl || "",
    discount: initial?.discount || 0,
    priceCategory: initial?.priceCategory || ("dibawah-20rb" as PriceCategory),
    status: initial?.status || ("active" as ProductStatus),
  });

  type FormField = keyof typeof form;

  function handleChange(field: FormField, value: string | number) {
    setForm((prev) => {
      const next = { ...prev, [field]: value };
      if (field === "price") {
        next.priceCategory = getPriceCategory(value as number);
      }
      return next;
    });
  }

  // Build preview product object
  const preview: Product = {
    id: initial?.id || "preview",
    name: form.name || "Nama Produk",
    price: form.price,
    priceCategory: form.priceCategory,
    discount: form.discount || undefined,
    imageUrl: form.imageUrl,
    shopeeUrl: form.shopeeUrl,
    status: form.status,
    createdAt: initial?.createdAt || new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setError("");

    const url =
      mode === "create"
        ? "/api/products"
        : `/api/products/${initial!.id}`;
    const method = mode === "create" ? "POST" : "PUT";

    try {
      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        setError(data.error || `Gagal menyimpan (${res.status})`);
        setSaving(false);
        return;
      }

      router.push("/admin");
    } catch (err) {
      setError(`Gagal menyimpan: ${err instanceof Error ? err.message : "Network error"}`);
      setSaving(false);
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      {/* Form */}
      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Nama Produk</label>
          <input
            type="text"
            value={form.name}
            onChange={(e) => handleChange("name", e.target.value)}
            className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-500)]"
            required
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Harga (Rp)</label>
            <input
              type="number"
              value={form.price}
              onChange={(e) => handleChange("price", parseInt(e.target.value) || 0)}
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-500)]"
              required
              min={0}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Diskon (%)</label>
            <input
              type="number"
              value={form.discount}
              onChange={(e) => handleChange("discount", parseInt(e.target.value) || 0)}
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-500)]"
              min={0}
              max={100}
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Link Shopee</label>
          <input
            type="url"
            value={form.shopeeUrl}
            onChange={(e) => handleChange("shopeeUrl", e.target.value)}
            className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-500)]"
            placeholder="https://shopee.co.id/..."
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Image URL</label>
          <input
            type="text"
            value={form.imageUrl}
            onChange={(e) => handleChange("imageUrl", e.target.value)}
            className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-500)]"
            placeholder="https://cf.shopee.co.id/file/..."
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Kategori Harga</label>
            <select
              value={form.priceCategory}
              onChange={(e) => handleChange("priceCategory", e.target.value)}
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-500)]"
            >
              {CATEGORIES.map((cat) => (
                <option key={cat.slug} value={cat.slug}>
                  {cat.emoji} {cat.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Status</label>
            <select
              value={form.status}
              onChange={(e) => handleChange("status", e.target.value)}
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-500)]"
            >
              {STATUS_OPTIONS.map((s) => (
                <option key={s.value} value={s.value}>{s.label}</option>
              ))}
            </select>
          </div>
        </div>

        {error && (
          <p className="text-red-500 text-sm bg-red-50 p-3 rounded">{error}</p>
        )}

        <button
          type="submit"
          disabled={saving}
          className="w-full bg-[var(--color-brand-500)] text-white py-2 rounded font-medium hover:bg-[var(--color-brand-600)] disabled:opacity-50"
        >
          {saving ? "Menyimpan..." : mode === "create" ? "Tambah Produk" : "Simpan Perubahan"}
        </button>
      </form>

      {/* Preview */}
      <div>
        <h3 className="text-sm font-medium text-gray-500 mb-3">Preview Card</h3>
        <div className="w-56">
          <ProductCard product={preview} />
        </div>
      </div>
    </div>
  );
}
