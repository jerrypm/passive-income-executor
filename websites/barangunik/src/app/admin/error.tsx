"use client";

export default function AdminError({
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="text-center py-16">
      <h1 className="text-2xl font-bold mb-4">Terjadi Kesalahan</h1>
      <p className="text-gray-500 mb-6">Gagal memuat halaman admin.</p>
      <button
        onClick={reset}
        className="bg-[var(--color-brand-500)] text-white px-6 py-2 rounded hover:bg-[var(--color-brand-600)]"
      >
        Coba Lagi
      </button>
    </div>
  );
}
