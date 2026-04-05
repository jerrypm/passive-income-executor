import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "BarangUnik — Barang Unik & Aneh dari Shopee",
    template: "%s | BarangUnik",
  },
  description: "Temukan barang unik, aneh, dan lucu dari Shopee Indonesia. Dikategorikan berdasarkan harga.",
  openGraph: {
    title: "BarangUnik — Barang Unik & Aneh dari Shopee",
    description: "Temukan barang unik, aneh, dan lucu dari Shopee Indonesia.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id">
      <body className="bg-gray-50 text-gray-900 antialiased">
        {children}
      </body>
    </html>
  );
}
