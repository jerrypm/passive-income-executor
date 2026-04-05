import { notFound } from "next/navigation";
import { getProductById } from "@/lib/products";
import ProductForm from "@/components/ProductForm";

interface PageProps {
  params: Promise<{ id: string }>;
}

export default async function EditPage({ params }: PageProps) {
  const { id } = await params;
  const product = await getProductById(id);
  if (!product) notFound();

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Edit Produk</h1>
      <ProductForm mode="edit" initial={product} />
    </div>
  );
}
