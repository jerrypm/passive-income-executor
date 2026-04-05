import ProductForm from "@/components/ProductForm";

export default function TambahPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Tambah Produk</h1>
      <ProductForm mode="create" />
    </div>
  );
}
