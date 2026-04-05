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

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: "BarangUnik",
  description: "Temukan barang unik, aneh, dan lucu dari Shopee Indonesia.",
  url: process.env.NEXT_PUBLIC_SITE_URL || "https://barangunik.vercel.app",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body className="bg-gray-50 text-gray-900 antialiased">
        {children}
      </body>
    </html>
  );
}
