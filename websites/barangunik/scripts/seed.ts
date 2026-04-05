/**
 * Seed script — uploads initial products to Vercel Blob.
 * Run: npx tsx scripts/seed.ts
 * Requires BLOB_READ_WRITE_TOKEN in .env.local
 */
import { put } from "@vercel/blob";
import { readFileSync } from "fs";
import { join } from "path";

async function seed() {
  const seedPath = join(__dirname, "..", "data", "seed.json");
  const data = readFileSync(seedPath, "utf-8");
  const products = JSON.parse(data);

  console.log(`Uploading ${products.length} seed products to Vercel Blob...`);

  const blob = await put("products.json", JSON.stringify(products, null, 2), {
    access: "public",
    addRandomSuffix: false,
    contentType: "application/json",
  });

  console.log(`Done! Blob URL: ${blob.url}`);
}

seed().catch(console.error);
