# Tancab Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build Tancab (Tanam Cabe) — responsive web app for chili farm monitoring with manual data input.

**Architecture:** Next.js 14 App Router with route groups: `(auth)` for login/register, `(app)` for authenticated pages with shared bottom nav layout. Supabase handles auth, database, and file storage. All pages mobile-first, desktop renders centered 480px container.

**Tech Stack:** Next.js 14, TypeScript, Tailwind CSS, Supabase (Auth + PostgreSQL + Storage), Recharts, Lucide React, Vercel.

**Project location:** `~/Documents/14_Web-projects/tancab/`

---

## File Structure

```
tancab/
├── app/
│   ├── globals.css
│   ├── layout.tsx                    # Root layout (Inter font, metadata)
│   ├── page.tsx                      # Redirect → /beranda or /login
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── (app)/
│   │   ├── layout.tsx                # Bottom nav + auth guard
│   │   ├── beranda/page.tsx
│   │   ├── lahan/page.tsx
│   │   ├── riwayat/page.tsx
│   │   ├── profil/page.tsx
│   │   ├── tambah-lahan/page.tsx
│   │   ├── edit-lahan/[id]/page.tsx
│   │   └── input-harian/page.tsx
├── components/
│   ├── ui/
│   │   ├── bottom-nav.tsx
│   │   ├── stat-card.tsx
│   │   ├── farm-card.tsx
│   │   ├── sensor-card.tsx
│   │   ├── activity-item.tsx
│   │   ├── form-input.tsx
│   │   ├── form-select.tsx
│   │   ├── form-textarea.tsx
│   │   ├── toast-provider.tsx
│   │   ├── empty-state.tsx
│   │   ├── skeleton-card.tsx
│   │   ├── status-badge.tsx
│   │   ├── page-header.tsx
│   │   └── info-grid.tsx
├── lib/
│   ├── supabase/
│   │   ├── client.ts                 # createBrowserClient
│   │   ├── server.ts                 # createServerClient
│   │   └── middleware.ts             # Auth middleware helper
│   ├── types.ts                      # DB types
│   ├── utils.ts                      # Helpers (greeting, date format, etc.)
│   └── constants.ts                  # Jenis bibit, kondisi, pupuk options
├── middleware.ts                     # Next.js middleware (auth redirect)
├── supabase/
│   └── schema.sql                    # Full DB schema
├── .env.local.example
├── tailwind.config.ts
├── next.config.js
├── package.json
└── tsconfig.json
```

---

## Task 1: Project Scaffold + Tailwind Config

**Files:**
- Create: `~/Documents/14_Web-projects/tancab/` (entire project)
- Create: `tailwind.config.ts` (custom design tokens)
- Create: `app/globals.css` (base styles)
- Create: `app/layout.tsx` (root layout)

**Step 1: Create Next.js project**

```bash
cd ~/Documents/14_Web-projects
npx create-next-app@latest tancab --typescript --tailwind --eslint --app --src-dir=false --import-alias="@/*" --use-npm
```

**Step 2: Install dependencies**

```bash
cd ~/Documents/14_Web-projects/tancab
npm install @supabase/supabase-js @supabase/ssr lucide-react recharts
```

**Step 3: Configure Tailwind with Tancab design tokens**

`tailwind.config.ts`:
```ts
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#2D5A27",
        action: "#4CAF50",
        background: "#F5F5F0",
        card: "#FFFFFF",
        warning: "#FF9800",
        error: "#E53935",
        "error-bg": "#FFEBEE",
        success: "#4CAF50",
        "success-bg": "#E8F5E9",
        "text-dark": "#1A1A1A",
        "text-gray": "#757575",
        border: "#E0E0E0",
        "sensor-normal": "#E8F5E9",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      maxWidth: {
        app: "480px",
      },
    },
  },
  plugins: [],
};
export default config;
```

**Step 4: Set up globals.css**

`app/globals.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  background-color: #F5F5F0;
  color: #1A1A1A;
  -webkit-font-smoothing: antialiased;
}

/* Hide scrollbar for mobile app feel */
::-webkit-scrollbar {
  display: none;
}

/* Centered app container for desktop */
@layer components {
  .app-container {
    @apply mx-auto w-full max-w-app min-h-screen bg-background;
  }
}
```

**Step 5: Root layout**

`app/layout.tsx`:
```tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Tancab — Tanam Cabe",
  description: "Monitoring dan optimasi pertanian cabe",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id">
      <body className={inter.className}>
        <div className="app-container">{children}</div>
      </body>
    </html>
  );
}
```

**Step 6: Verify dev server runs**

```bash
cd ~/Documents/14_Web-projects/tancab && npm run dev
```

Expected: App runs on localhost:3000

**Step 7: Init git and commit**

```bash
cd ~/Documents/14_Web-projects/tancab
git init
git add -A
git commit -m "feat: scaffold Tancab project with Next.js 14 + Tailwind design tokens"
```

---

## Task 2: Supabase Schema + Client Setup

**Files:**
- Create: `supabase/schema.sql`
- Create: `lib/supabase/client.ts`
- Create: `lib/supabase/server.ts`
- Create: `lib/supabase/middleware.ts`
- Create: `middleware.ts`
- Create: `.env.local.example`
- Create: `lib/types.ts`

**Step 1: Create .env.local.example**

```
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

User must create `.env.local` with real Supabase credentials.

**Step 2: Write schema.sql**

`supabase/schema.sql`:
```sql
-- Users profile (extends Supabase Auth)
create table public.users (
  id uuid references auth.users on delete cascade primary key,
  nama text not null,
  email text not null,
  phone text,
  created_at timestamptz default now()
);

alter table public.users enable row level security;
create policy "Users can read own profile" on public.users for select using (auth.uid() = id);
create policy "Users can update own profile" on public.users for update using (auth.uid() = id);
create policy "Users can insert own profile" on public.users for insert with check (auth.uid() = id);

-- Lahan (farm plots)
create table public.lahan (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references public.users(id) on delete cascade not null,
  nama_lahan text not null,
  lokasi text,
  luas_m2 integer,
  jenis_bibit text not null default 'Cabe Rawit',
  tanggal_tanam date,
  status text not null default 'aktif' check (status in ('aktif', 'panen', 'istirahat')),
  foto_url text,
  catatan text,
  created_at timestamptz default now()
);

alter table public.lahan enable row level security;
create policy "Users can CRUD own lahan" on public.lahan for all using (auth.uid() = user_id);

-- Log Harian (daily records)
create table public.log_harian (
  id uuid default gen_random_uuid() primary key,
  lahan_id uuid references public.lahan(id) on delete cascade not null,
  tanggal date not null default current_date,
  suhu_celcius decimal,
  kelembaban_persen decimal,
  ph_tanah decimal,
  air_liter decimal,
  pupuk_jenis text,
  pupuk_jumlah_gram decimal,
  kondisi_tanaman text check (kondisi_tanaman in ('Sehat', 'Layu', 'Kuning', 'Berbuah')),
  foto_url text,
  catatan text,
  created_at timestamptz default now()
);

alter table public.log_harian enable row level security;
create policy "Users can CRUD own logs" on public.log_harian for all
  using (lahan_id in (select id from public.lahan where user_id = auth.uid()));

-- Auto-create user profile on signup
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.users (id, nama, email)
  values (new.id, coalesce(new.raw_user_meta_data->>'nama', split_part(new.email, '@', 1)), new.email);
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();
```

**Step 3: Supabase browser client**

`lib/supabase/client.ts`:
```ts
import { createBrowserClient } from "@supabase/ssr";

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

**Step 4: Supabase server client**

`lib/supabase/server.ts`:
```ts
import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

export async function createClient() {
  const cookieStore = await cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            );
          } catch {
            // Server Component — ignore
          }
        },
      },
    }
  );
}
```

**Step 5: Middleware helper**

`lib/supabase/middleware.ts`:
```ts
import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

export async function updateSession(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          );
          supabaseResponse = NextResponse.next({ request });
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          );
        },
      },
    }
  );

  const {
    data: { user },
  } = await supabase.auth.getUser();

  // Not logged in → redirect to login (except auth pages)
  if (
    !user &&
    !request.nextUrl.pathname.startsWith("/login") &&
    !request.nextUrl.pathname.startsWith("/register")
  ) {
    const url = request.nextUrl.clone();
    url.pathname = "/login";
    return NextResponse.redirect(url);
  }

  // Logged in → redirect away from auth pages
  if (
    user &&
    (request.nextUrl.pathname.startsWith("/login") ||
      request.nextUrl.pathname.startsWith("/register"))
  ) {
    const url = request.nextUrl.clone();
    url.pathname = "/beranda";
    return NextResponse.redirect(url);
  }

  return supabaseResponse;
}
```

**Step 6: Next.js middleware**

`middleware.ts`:
```ts
import { type NextRequest } from "next/server";
import { updateSession } from "@/lib/supabase/middleware";

export async function middleware(request: NextRequest) {
  return await updateSession(request);
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
```

**Step 7: TypeScript types**

`lib/types.ts`:
```ts
export interface User {
  id: string;
  nama: string;
  email: string;
  phone: string | null;
  created_at: string;
}

export interface Lahan {
  id: string;
  user_id: string;
  nama_lahan: string;
  lokasi: string | null;
  luas_m2: number | null;
  jenis_bibit: string;
  tanggal_tanam: string | null;
  status: "aktif" | "panen" | "istirahat";
  foto_url: string | null;
  catatan: string | null;
  created_at: string;
}

export interface LogHarian {
  id: string;
  lahan_id: string;
  tanggal: string;
  suhu_celcius: number | null;
  kelembaban_persen: number | null;
  ph_tanah: number | null;
  air_liter: number | null;
  pupuk_jenis: string | null;
  pupuk_jumlah_gram: number | null;
  kondisi_tanaman: "Sehat" | "Layu" | "Kuning" | "Berbuah" | null;
  foto_url: string | null;
  catatan: string | null;
  created_at: string;
  // joined
  lahan?: Lahan;
}
```

**Step 8: Constants**

`lib/constants.ts`:
```ts
export const JENIS_BIBIT = [
  "Cabe Rawit",
  "Cabe Merah",
  "Cabe Keriting",
  "Cabe Hijau",
  "Cabe Kathur",
] as const;

export const KONDISI_TANAMAN = [
  "Sehat",
  "Layu",
  "Kuning",
  "Berbuah",
] as const;

export const JENIS_PUPUK = [
  "NPK",
  "Organik",
  "ZA",
  "Urea",
  "KCl",
  "TSP",
] as const;

export const STATUS_LAHAN = [
  "aktif",
  "panen",
  "istirahat",
] as const;

// Estimasi hari panen per jenis bibit
export const HARI_PANEN: Record<string, number> = {
  "Cabe Rawit": 90,
  "Cabe Merah": 100,
  "Cabe Keriting": 95,
  "Cabe Hijau": 85,
  "Cabe Kathur": 90,
};

// Threshold sensor values
export const SENSOR_THRESHOLDS = {
  suhu: { min: 20, max: 35, unit: "°C" },
  kelembaban: { min: 60, max: 80, unit: "%" },
  ph: { min: 5.5, max: 7.0, unit: "" },
} as const;
```

**Step 9: Utils**

`lib/utils.ts`:
```ts
export function getGreeting(): string {
  const hour = new Date().getHours();
  if (hour < 11) return "Selamat Pagi";
  if (hour < 15) return "Selamat Siang";
  if (hour < 18) return "Selamat Sore";
  return "Selamat Malam";
}

export function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("id-ID", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

export function formatDateShort(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("id-ID", {
    day: "numeric",
    month: "short",
  });
}

export function daysBetween(dateStr: string): number {
  const date = new Date(dateStr);
  const today = new Date();
  const diff = today.getTime() - date.getTime();
  return Math.floor(diff / (1000 * 60 * 60 * 24));
}

export function timeAgo(dateStr: string): string {
  const diff = daysBetween(dateStr);
  if (diff === 0) return "Hari ini";
  if (diff === 1) return "Kemarin";
  if (diff < 7) return `${diff} hari lalu`;
  if (diff < 30) return `${Math.floor(diff / 7)} minggu lalu`;
  return `${Math.floor(diff / 30)} bulan lalu`;
}

export function getSensorStatus(
  type: "suhu" | "kelembaban" | "ph",
  value: number
): { label: string; color: "green" | "orange" | "red" } {
  const t = {
    suhu: { min: 20, max: 35 },
    kelembaban: { min: 60, max: 80 },
    ph: { min: 5.5, max: 7.0 },
  }[type];

  if (value >= t.min && value <= t.max) return { label: "Normal", color: "green" };
  if (value < t.min - 5 || value > t.max + 5) return { label: "Bahaya", color: "red" };
  return { label: "Perhatian", color: "orange" };
}

export function getWaterStatus(
  suhu: number | null,
  kelembaban: number | null
): { label: string; color: "green" | "orange" | "red" } {
  if (!suhu || !kelembaban) return { label: "—", color: "green" };
  if (kelembaban > 70 && suhu < 30) return { label: "Cukup", color: "green" };
  if (kelembaban < 50 || suhu > 35) return { label: "Kurang", color: "red" };
  return { label: "Sedang", color: "orange" };
}

export function getInitials(nama: string): string {
  return nama
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);
}
```

**Step 10: Commit**

```bash
git add -A
git commit -m "feat: Supabase schema, client setup, types, constants, and utils"
```

---

## Task 3: Shared UI Components

**Files:**
- Create: `components/ui/bottom-nav.tsx`
- Create: `components/ui/stat-card.tsx`
- Create: `components/ui/sensor-card.tsx`
- Create: `components/ui/farm-card.tsx`
- Create: `components/ui/activity-item.tsx`
- Create: `components/ui/empty-state.tsx`
- Create: `components/ui/skeleton-card.tsx`
- Create: `components/ui/status-badge.tsx`
- Create: `components/ui/page-header.tsx`
- Create: `components/ui/toast-provider.tsx`
- Create: `components/ui/form-input.tsx`
- Create: `components/ui/form-select.tsx`
- Create: `components/ui/form-textarea.tsx`
- Create: `components/ui/info-grid.tsx`

**Step 1: Bottom Nav**

`components/ui/bottom-nav.tsx`:
```tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Sprout, Clock, User } from "lucide-react";

const tabs = [
  { href: "/beranda", label: "Beranda", icon: Home },
  { href: "/lahan", label: "Lahan", icon: Sprout },
  { href: "/riwayat", label: "Riwayat", icon: Clock },
  { href: "/profil", label: "Profil", icon: User },
];

export function BottomNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-app bg-white border-t border-border z-50">
      <div className="flex items-center justify-around h-16">
        {tabs.map((tab) => {
          const isActive = pathname.startsWith(tab.href);
          const Icon = tab.icon;
          return (
            <Link
              key={tab.href}
              href={tab.href}
              className={`flex flex-col items-center gap-1 px-4 py-2 rounded-2xl transition-colors ${
                isActive
                  ? "bg-primary text-white"
                  : "text-text-gray hover:text-primary"
              }`}
            >
              <Icon size={20} />
              <span className="text-xs font-medium">{tab.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
```

**Step 2: Stat Card**

`components/ui/stat-card.tsx`:
```tsx
import { type LucideIcon } from "lucide-react";

interface StatCardProps {
  icon: LucideIcon;
  value: number | string;
  label: string;
  iconColor?: string;
  iconBg?: string;
}

export function StatCard({
  icon: Icon,
  value,
  label,
  iconColor = "text-primary",
  iconBg = "bg-green-50",
}: StatCardProps) {
  return (
    <div className="bg-card rounded-xl p-4 flex flex-col items-center gap-2 shadow-sm">
      <div className={`w-10 h-10 rounded-full ${iconBg} flex items-center justify-center`}>
        <Icon size={20} className={iconColor} />
      </div>
      <span className="text-2xl font-bold text-text-dark">{value}</span>
      <span className="text-xs text-text-gray">{label}</span>
    </div>
  );
}
```

**Step 3: Sensor Card**

`components/ui/sensor-card.tsx`:
```tsx
interface SensorCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  status: string;
  statusColor: "green" | "orange" | "red";
}

const statusBg = {
  green: "bg-success-bg",
  orange: "bg-orange-50",
  red: "bg-error-bg",
};

const statusText = {
  green: "text-success",
  orange: "text-warning",
  red: "text-error",
};

export function SensorCard({ icon, label, value, status, statusColor }: SensorCardProps) {
  return (
    <div className={`${statusBg[statusColor]} rounded-xl p-4`}>
      <div className="flex items-center justify-between mb-2">
        {icon}
        <span className={`text-xs font-medium ${statusText[statusColor]}`}>
          {status}
        </span>
      </div>
      <p className="text-sm text-text-gray">{label}</p>
      <p className="text-2xl font-bold text-text-dark">{value}</p>
    </div>
  );
}
```

**Step 4: Farm Card**

`components/ui/farm-card.tsx`:
```tsx
import Link from "next/link";
import { Sprout } from "lucide-react";
import { StatusBadge } from "./status-badge";
import type { Lahan } from "@/lib/types";
import { formatDateShort } from "@/lib/utils";

interface FarmCardProps {
  lahan: Lahan;
}

export function FarmCard({ lahan }: FarmCardProps) {
  return (
    <div className="bg-card rounded-xl p-4 shadow-sm">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-green-50 flex items-center justify-center">
            <Sprout size={20} className="text-primary" />
          </div>
          <div>
            <h3 className="font-semibold text-text-dark">{lahan.nama_lahan}</h3>
            <p className="text-sm text-text-gray">📍 {lahan.lokasi || "-"}</p>
          </div>
        </div>
        <StatusBadge status={lahan.status} />
      </div>
      <div className="grid grid-cols-3 gap-2 text-sm mb-4">
        <div>
          <p className="text-text-gray">Luas</p>
          <p className="font-semibold">{lahan.luas_m2 || "-"} m²</p>
        </div>
        <div>
          <p className="text-text-gray">Tanaman</p>
          <p className="font-semibold">{lahan.jenis_bibit}</p>
        </div>
        <div>
          <p className="text-text-gray">Ditanam</p>
          <p className="font-semibold">
            {lahan.tanggal_tanam ? formatDateShort(lahan.tanggal_tanam) : "-"}
          </p>
        </div>
      </div>
      <div className="flex gap-3">
        <Link
          href={`/edit-lahan/${lahan.id}`}
          className="flex-1 text-center py-2 rounded-lg border border-border text-text-dark text-sm font-medium"
        >
          ✏️ Edit
        </Link>
        <Link
          href={`/lahan?id=${lahan.id}`}
          className="flex-1 text-center py-2 rounded-lg bg-primary text-white text-sm font-medium"
        >
          📊 Lihat Data
        </Link>
      </div>
    </div>
  );
}
```

**Step 5: Activity Item**

`components/ui/activity-item.tsx`:
```tsx
interface ActivityItemProps {
  icon: React.ReactNode;
  title: string;
  subtitle: string;
}

export function ActivityItem({ icon, title, subtitle }: ActivityItemProps) {
  return (
    <div className="flex items-center gap-3 py-3">
      <div className="w-10 h-10 rounded-full bg-green-50 flex items-center justify-center shrink-0">
        {icon}
      </div>
      <div>
        <p className="font-medium text-text-dark">{title}</p>
        <p className="text-sm text-text-gray">{subtitle}</p>
      </div>
    </div>
  );
}
```

**Step 6: Empty State**

`components/ui/empty-state.tsx`:
```tsx
interface EmptyStateProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  actionLabel: string;
  onAction?: () => void;
  href?: string;
  variant?: "green" | "orange";
}

export function EmptyState({
  icon,
  title,
  description,
  actionLabel,
  onAction,
  href,
  variant = "green",
}: EmptyStateProps) {
  const btnClass =
    variant === "green"
      ? "bg-action text-white"
      : "bg-warning text-white";

  const content = (
    <div className="flex flex-col items-center text-center py-12 px-6">
      <div className="w-16 h-16 rounded-full bg-green-50 flex items-center justify-center mb-4">
        {icon}
      </div>
      <h3 className="font-bold text-text-dark mb-1">{title}</h3>
      <p className="text-sm text-text-gray mb-4">{description}</p>
      {href ? (
        <a
          href={href}
          className={`px-6 py-2.5 rounded-full font-semibold text-sm ${btnClass}`}
        >
          {actionLabel}
        </a>
      ) : (
        <button
          onClick={onAction}
          className={`px-6 py-2.5 rounded-full font-semibold text-sm ${btnClass}`}
        >
          {actionLabel}
        </button>
      )}
    </div>
  );

  return content;
}
```

**Step 7: Skeleton Card**

`components/ui/skeleton-card.tsx`:
```tsx
export function SkeletonCard({ variant = "default" }: { variant?: "default" | "small" }) {
  if (variant === "small") {
    return (
      <div className="bg-card rounded-xl p-4 animate-pulse">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gray-200" />
          <div className="flex-1 space-y-2">
            <div className="h-4 bg-gray-200 rounded w-3/4" />
            <div className="h-3 bg-gray-200 rounded w-1/2" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-card rounded-xl p-4 animate-pulse">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-full bg-gray-200" />
        <div className="flex-1 space-y-2">
          <div className="h-4 bg-gray-200 rounded w-3/4" />
          <div className="h-3 bg-gray-200 rounded w-1/2" />
        </div>
      </div>
      <div className="h-3 bg-gray-200 rounded w-full mb-2" />
      <div className="flex gap-3 mt-4">
        <div className="h-9 bg-gray-200 rounded-lg flex-1" />
        <div className="h-9 bg-gray-200 rounded-lg flex-1" />
      </div>
    </div>
  );
}
```

**Step 8: Status Badge**

`components/ui/status-badge.tsx`:
```tsx
const styles = {
  aktif: "bg-success-bg text-success",
  panen: "bg-orange-50 text-warning",
  istirahat: "bg-gray-100 text-text-gray",
};

const labels = {
  aktif: "Aktif",
  panen: "Panen",
  istirahat: "Istirahat",
};

export function StatusBadge({ status }: { status: "aktif" | "panen" | "istirahat" }) {
  return (
    <span className={`px-3 py-1 rounded-full text-xs font-medium ${styles[status]}`}>
      {labels[status]}
    </span>
  );
}
```

**Step 9: Page Header (back arrow + title)**

`components/ui/page-header.tsx`:
```tsx
"use client";

import { useRouter } from "next/navigation";
import { ArrowLeft } from "lucide-react";

interface PageHeaderProps {
  title: string;
  onBack?: () => void;
}

export function PageHeader({ title, onBack }: PageHeaderProps) {
  const router = useRouter();

  return (
    <div className="flex items-center gap-3 py-4">
      <button
        onClick={onBack || (() => router.back())}
        className="w-10 h-10 flex items-center justify-center rounded-full hover:bg-gray-100"
      >
        <ArrowLeft size={24} />
      </button>
      <h1 className="text-xl font-bold text-text-dark">{title}</h1>
    </div>
  );
}
```

**Step 10: Toast Provider**

`components/ui/toast-provider.tsx`:
```tsx
"use client";

import { createContext, useContext, useState, useCallback } from "react";
import { CheckCircle, XCircle, X } from "lucide-react";

interface Toast {
  id: number;
  type: "success" | "error";
  message: string;
}

interface ToastContextType {
  showToast: (type: "success" | "error", message: string) => void;
}

const ToastContext = createContext<ToastContextType>({ showToast: () => {} });

export function useToast() {
  return useContext(ToastContext);
}

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const showToast = useCallback((type: "success" | "error", message: string) => {
    const id = Date.now();
    setToasts((prev) => [...prev, { id, type, message }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 3000);
  }, []);

  const dismiss = (id: number) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      <div className="fixed top-4 left-1/2 -translate-x-1/2 z-[100] w-full max-w-app px-4 space-y-2">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={`flex items-center gap-2 px-4 py-3 rounded-xl text-sm font-medium shadow-lg transition-all ${
              toast.type === "success"
                ? "bg-success-bg text-primary border border-success"
                : "bg-error-bg text-error border border-error"
            }`}
          >
            {toast.type === "success" ? (
              <CheckCircle size={18} />
            ) : (
              <XCircle size={18} />
            )}
            <span className="flex-1">{toast.message}</span>
            <button onClick={() => dismiss(toast.id)}>
              <X size={16} />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}
```

**Step 11: Form Input (3 states)**

`components/ui/form-input.tsx`:
```tsx
import { forwardRef } from "react";

interface FormInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  success?: boolean;
  icon?: React.ReactNode;
  suffix?: string;
}

export const FormInput = forwardRef<HTMLInputElement, FormInputProps>(
  ({ label, error, success, icon, suffix, className, ...props }, ref) => {
    const borderClass = error
      ? "border-error"
      : success
        ? "border-success"
        : "border-border focus-within:border-primary";

    return (
      <div className="space-y-1.5">
        <label className={`text-sm font-medium ${error ? "text-error" : "text-text-dark"}`}>
          {label}
        </label>
        <div className={`flex items-center gap-2 px-4 py-3 rounded-xl border ${borderClass} bg-white transition-colors`}>
          {icon && <span className="text-text-gray">{icon}</span>}
          <input
            ref={ref}
            className={`flex-1 outline-none text-text-dark placeholder:text-text-gray bg-transparent ${className || ""}`}
            {...props}
          />
          {suffix && <span className="text-text-gray text-sm">{suffix}</span>}
          {success && !error && (
            <span className="text-success">✓</span>
          )}
        </div>
        {error && (
          <p className="text-xs text-error flex items-center gap-1">
            ⚠ {error}
          </p>
        )}
      </div>
    );
  }
);
FormInput.displayName = "FormInput";
```

**Step 12: Form Select**

`components/ui/form-select.tsx`:
```tsx
import { forwardRef } from "react";

interface FormSelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label: string;
  error?: string;
  options: { value: string; label: string }[];
}

export const FormSelect = forwardRef<HTMLSelectElement, FormSelectProps>(
  ({ label, error, options, ...props }, ref) => {
    return (
      <div className="space-y-1.5">
        <label className={`text-sm font-medium ${error ? "text-error" : "text-text-dark"}`}>
          {label}
        </label>
        <select
          ref={ref}
          className={`w-full px-4 py-3 rounded-xl border bg-white outline-none transition-colors ${
            error ? "border-error" : "border-border focus:border-primary"
          }`}
          {...props}
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
        {error && <p className="text-xs text-error">⚠ {error}</p>}
      </div>
    );
  }
);
FormSelect.displayName = "FormSelect";
```

**Step 13: Form Textarea**

`components/ui/form-textarea.tsx`:
```tsx
import { forwardRef } from "react";

interface FormTextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label: string;
  error?: string;
}

export const FormTextarea = forwardRef<HTMLTextAreaElement, FormTextareaProps>(
  ({ label, error, ...props }, ref) => {
    return (
      <div className="space-y-1.5">
        <label className={`text-sm font-medium ${error ? "text-error" : "text-text-dark"}`}>
          {label}
        </label>
        <textarea
          ref={ref}
          className={`w-full px-4 py-3 rounded-xl border bg-white outline-none transition-colors resize-none ${
            error ? "border-error" : "border-border focus:border-primary"
          }`}
          rows={3}
          {...props}
        />
        {error && <p className="text-xs text-error">⚠ {error}</p>}
      </div>
    );
  }
);
FormTextarea.displayName = "FormTextarea";
```

**Step 14: Info Grid**

`components/ui/info-grid.tsx`:
```tsx
interface InfoGridItem {
  icon: React.ReactNode;
  label: string;
  value: string;
  highlight?: boolean;
}

export function InfoGrid({ items }: { items: InfoGridItem[] }) {
  return (
    <div className="grid grid-cols-2 gap-3">
      {items.map((item, i) => (
        <div key={i} className="flex items-start gap-2 p-3 rounded-xl bg-gray-50">
          <span className="text-text-gray mt-0.5">{item.icon}</span>
          <div>
            <p className="text-xs text-text-gray">{item.label}</p>
            <p className={`text-sm font-semibold ${item.highlight ? "text-warning" : "text-text-dark"}`}>
              {item.value}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}
```

**Step 15: Commit**

```bash
git add -A
git commit -m "feat: all shared UI components (bottom-nav, cards, forms, toasts, empty states, skeletons)"
```

---

## Task 4: Auth Pages (Login + Register)

**Files:**
- Create: `app/(auth)/login/page.tsx`
- Create: `app/(auth)/register/page.tsx`
- Create: `app/page.tsx` (root redirect)

**Step 1: Root redirect**

`app/page.tsx`:
```tsx
import { redirect } from "next/navigation";

export default function Home() {
  redirect("/beranda");
}
```

**Step 2: Login page**

`app/(auth)/login/page.tsx`:
```tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Sprout } from "lucide-react";
import { createClient } from "@/lib/supabase/client";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");

    const supabase = createClient();
    const { error } = await supabase.auth.signInWithPassword({ email, password });

    if (error) {
      setError("Email atau password salah");
      setLoading(false);
      return;
    }

    router.push("/beranda");
    router.refresh();
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6">
      <div className="w-full max-w-sm">
        <div className="flex flex-col items-center mb-8">
          <div className="w-16 h-16 rounded-full bg-primary flex items-center justify-center mb-3">
            <Sprout size={32} className="text-white" />
          </div>
          <h1 className="text-2xl font-bold text-primary">Tancab</h1>
          <p className="text-text-gray text-sm">Tanam Cabe — Monitoring Pertanian</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-4">
          <div className="space-y-1.5">
            <label className="text-sm font-medium text-text-dark">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="nama@email.com"
              required
              className="w-full px-4 py-3 rounded-xl border border-border bg-white outline-none focus:border-primary"
            />
          </div>
          <div className="space-y-1.5">
            <label className="text-sm font-medium text-text-dark">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Masukkan password"
              required
              className="w-full px-4 py-3 rounded-xl border border-border bg-white outline-none focus:border-primary"
            />
          </div>

          {error && (
            <p className="text-sm text-error text-center">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-action text-white font-semibold disabled:opacity-50"
          >
            {loading ? "Masuk..." : "Masuk"}
          </button>
        </form>

        <p className="text-center text-sm text-text-gray mt-6">
          Belum punya akun?{" "}
          <Link href="/register" className="text-primary font-semibold">
            Daftar
          </Link>
        </p>
      </div>
    </div>
  );
}
```

**Step 3: Register page**

`app/(auth)/register/page.tsx`:
```tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Sprout } from "lucide-react";
import { createClient } from "@/lib/supabase/client";

export default function RegisterPage() {
  const [nama, setNama] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleRegister(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");

    const supabase = createClient();
    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: { data: { nama } },
    });

    if (error) {
      setError(error.message);
      setLoading(false);
      return;
    }

    router.push("/beranda");
    router.refresh();
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6">
      <div className="w-full max-w-sm">
        <div className="flex flex-col items-center mb-8">
          <div className="w-16 h-16 rounded-full bg-primary flex items-center justify-center mb-3">
            <Sprout size={32} className="text-white" />
          </div>
          <h1 className="text-2xl font-bold text-primary">Tancab</h1>
          <p className="text-text-gray text-sm">Buat akun baru</p>
        </div>

        <form onSubmit={handleRegister} className="space-y-4">
          <div className="space-y-1.5">
            <label className="text-sm font-medium text-text-dark">Nama Lengkap</label>
            <input
              type="text"
              value={nama}
              onChange={(e) => setNama(e.target.value)}
              placeholder="Jeri Purnama"
              required
              className="w-full px-4 py-3 rounded-xl border border-border bg-white outline-none focus:border-primary"
            />
          </div>
          <div className="space-y-1.5">
            <label className="text-sm font-medium text-text-dark">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="nama@email.com"
              required
              className="w-full px-4 py-3 rounded-xl border border-border bg-white outline-none focus:border-primary"
            />
          </div>
          <div className="space-y-1.5">
            <label className="text-sm font-medium text-text-dark">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Min. 6 karakter"
              required
              minLength={6}
              className="w-full px-4 py-3 rounded-xl border border-border bg-white outline-none focus:border-primary"
            />
          </div>

          {error && (
            <p className="text-sm text-error text-center">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-action text-white font-semibold disabled:opacity-50"
          >
            {loading ? "Mendaftar..." : "Daftar"}
          </button>
        </form>

        <p className="text-center text-sm text-text-gray mt-6">
          Sudah punya akun?{" "}
          <Link href="/login" className="text-primary font-semibold">
            Masuk
          </Link>
        </p>
      </div>
    </div>
  );
}
```

**Step 4: Commit**

```bash
git add -A
git commit -m "feat: auth pages (login + register) with Supabase"
```

---

## Task 5: App Layout (Bottom Nav + Auth Guard)

**Files:**
- Create: `app/(app)/layout.tsx`
- Modify: `app/layout.tsx` (add ToastProvider)

**Step 1: App layout with bottom nav**

`app/(app)/layout.tsx`:
```tsx
import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import { BottomNav } from "@/components/ui/bottom-nav";
import { ToastProvider } from "@/components/ui/toast-provider";

export default async function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    redirect("/login");
  }

  return (
    <ToastProvider>
      <main className="pb-20 px-4">
        {children}
      </main>
      <BottomNav />
    </ToastProvider>
  );
}
```

**Step 2: Commit**

```bash
git add -A
git commit -m "feat: app layout with bottom nav and auth guard"
```

---

## Task 6: Dashboard (Beranda)

**Files:**
- Create: `app/(app)/beranda/page.tsx`

**Step 1: Beranda page**

`app/(app)/beranda/page.tsx`:
```tsx
import { createClient } from "@/lib/supabase/server";
import { getGreeting, timeAgo, daysBetween } from "@/lib/utils";
import { HARI_PANEN } from "@/lib/constants";
import { StatCard } from "@/components/ui/stat-card";
import { ActivityItem } from "@/components/ui/activity-item";
import { EmptyState } from "@/components/ui/empty-state";
import { MapPin, Sprout, Calendar, Droplets, FlaskConical, Bug, Bell } from "lucide-react";
import Link from "next/link";

export default async function BerandaPage() {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  const { data: profile } = await supabase
    .from("users")
    .select("*")
    .eq("id", user!.id)
    .single();

  const { data: lahanList } = await supabase
    .from("lahan")
    .select("*")
    .eq("user_id", user!.id);

  const { data: recentLogs } = await supabase
    .from("log_harian")
    .select("*, lahan:lahan_id(nama_lahan)")
    .order("created_at", { ascending: false })
    .limit(5);

  const totalLahan = lahanList?.length || 0;
  const tanamanAktif = lahanList?.filter((l) => l.status === "aktif").length || 0;

  // Nearest harvest countdown
  let panenHari = 0;
  if (lahanList && lahanList.length > 0) {
    const aktifLahan = lahanList.filter((l) => l.status === "aktif" && l.tanggal_tanam);
    if (aktifLahan.length > 0) {
      const countdowns = aktifLahan.map((l) => {
        const target = HARI_PANEN[l.jenis_bibit] || 90;
        const age = daysBetween(l.tanggal_tanam!);
        return Math.max(0, target - age);
      });
      panenHari = Math.min(...countdowns);
    }
  }

  const hasData = totalLahan > 0;

  const activityIcons: Record<string, React.ReactNode> = {
    air: <Droplets size={18} className="text-blue-500" />,
    pupuk: <FlaskConical size={18} className="text-green-600" />,
    hama: <Bug size={18} className="text-orange-500" />,
    default: <Sprout size={18} className="text-primary" />,
  };

  function getActivityInfo(log: any) {
    if (log.pupuk_jenis) {
      return { icon: activityIcons.pupuk, title: "Pemupukan", detail: log.pupuk_jenis };
    }
    if (log.air_liter && log.air_liter > 0) {
      return { icon: activityIcons.air, title: "Penyiraman", detail: `${log.air_liter}L` };
    }
    return { icon: activityIcons.default, title: "Pencatatan Data", detail: "" };
  }

  return (
    <div className="pt-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-text-dark">
            {getGreeting()}, {profile?.nama?.split(" ")[0] || "Petani"} 👋
          </h1>
          <p className="text-sm text-text-gray">Apa kabar kebun hari ini?</p>
        </div>
        <button className="w-10 h-10 rounded-full border border-border flex items-center justify-center">
          <Bell size={20} className="text-text-gray" />
        </button>
      </div>

      {/* Weather (hardcoded MVP) */}
      <div className="bg-card rounded-xl px-4 py-3 flex items-center gap-3 mb-6 shadow-sm">
        <span className="text-2xl">☀️</span>
        <div>
          <p className="font-semibold text-text-dark">Cerah, 32°C</p>
          <p className="text-sm text-text-gray">Bandung, Jawa Barat</p>
        </div>
      </div>

      {!hasData ? (
        <EmptyState
          icon={<Sprout size={28} className="text-primary" />}
          title="Belum ada data"
          description="Yuk mulai catat data harian kamu"
          actionLabel="✏️ Mulai Catat"
          href="/tambah-lahan"
        />
      ) : (
        <>
          {/* Stats */}
          <div className="grid grid-cols-3 gap-3 mb-6">
            <StatCard icon={MapPin} value={totalLahan} label="Total Lahan" />
            <StatCard
              icon={Sprout}
              value={tanamanAktif}
              label="Tanaman Aktif"
              iconColor="text-action"
              iconBg="bg-success-bg"
            />
            <StatCard
              icon={Calendar}
              value={panenHari}
              label="Panen (hari)"
              iconColor="text-warning"
              iconBg="bg-orange-50"
            />
          </div>

          {/* CTA */}
          <div className="mb-6">
            <h2 className="font-semibold text-text-dark mb-3">Input Harian</h2>
            <Link
              href="/input-harian"
              className="block w-full py-3.5 rounded-xl bg-action text-white font-semibold text-center"
            >
              ✏️ Catat Data Hari Ini
            </Link>
          </div>

          {/* Recent Activity */}
          <div>
            <h2 className="font-semibold text-text-dark mb-3">Aktivitas Terakhir</h2>
            {recentLogs && recentLogs.length > 0 ? (
              <div className="bg-card rounded-xl divide-y divide-gray-100 shadow-sm">
                {recentLogs.map((log) => {
                  const info = getActivityInfo(log);
                  const lahanName = (log.lahan as any)?.nama_lahan || "";
                  return (
                    <div key={log.id} className="px-4">
                      <ActivityItem
                        icon={info.icon}
                        title={info.title}
                        subtitle={`${lahanName} · ${timeAgo(log.created_at)}`}
                      />
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="text-sm text-text-gray text-center py-4">
                Belum ada aktivitas
              </p>
            )}
          </div>
        </>
      )}
    </div>
  );
}
```

**Step 2: Commit**

```bash
git add -A
git commit -m "feat: dashboard (beranda) page with stats, CTA, and activity list"
```

---

## Task 7: Tambah Lahan + Edit Lahan Forms

**Files:**
- Create: `app/(app)/tambah-lahan/page.tsx`
- Create: `app/(app)/edit-lahan/[id]/page.tsx`

**Step 1: Tambah Lahan form**

`app/(app)/tambah-lahan/page.tsx`:
```tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import { useToast } from "@/components/ui/toast-provider";
import { PageHeader } from "@/components/ui/page-header";
import { FormInput } from "@/components/ui/form-input";
import { FormSelect } from "@/components/ui/form-select";
import { FormTextarea } from "@/components/ui/form-textarea";
import { JENIS_BIBIT } from "@/lib/constants";
import { MapPin, Camera } from "lucide-react";

export default function TambahLahanPage() {
  const router = useRouter();
  const { showToast } = useToast();
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [form, setForm] = useState({
    nama_lahan: "",
    lokasi: "",
    luas_m2: "",
    jenis_bibit: "Cabe Rawit",
    tanggal_tanam: "",
    catatan: "",
  });

  function update(field: string, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }));
    setErrors((prev) => ({ ...prev, [field]: "" }));
  }

  function validate(): boolean {
    const newErrors: Record<string, string> = {};
    if (!form.nama_lahan.trim()) newErrors.nama_lahan = "Nama lahan wajib diisi";
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!validate()) return;

    setLoading(true);
    const supabase = createClient();
    const { data: { user } } = await supabase.auth.getUser();

    const { error } = await supabase.from("lahan").insert({
      user_id: user!.id,
      nama_lahan: form.nama_lahan,
      lokasi: form.lokasi || null,
      luas_m2: form.luas_m2 ? parseInt(form.luas_m2) : null,
      jenis_bibit: form.jenis_bibit,
      tanggal_tanam: form.tanggal_tanam || null,
      catatan: form.catatan || null,
    });

    setLoading(false);

    if (error) {
      showToast("error", "Gagal menyimpan. Coba lagi.");
      return;
    }

    showToast("success", "Data berhasil disimpan!");
    router.push("/profil");
    router.refresh();
  }

  return (
    <div>
      <PageHeader title="Tambah Lahan Baru" />

      <form onSubmit={handleSubmit} className="space-y-4">
        <FormInput
          label="Nama Lahan"
          placeholder="contoh: Kebun Belakang"
          value={form.nama_lahan}
          onChange={(e) => update("nama_lahan", e.target.value)}
          error={errors.nama_lahan}
        />

        <FormInput
          label="Lokasi"
          placeholder="contoh: Bandung"
          value={form.lokasi}
          onChange={(e) => update("lokasi", e.target.value)}
          icon={<MapPin size={18} />}
        />

        <FormInput
          label="Luas Lahan"
          type="number"
          placeholder="0"
          value={form.luas_m2}
          onChange={(e) => update("luas_m2", e.target.value)}
          suffix="m²"
        />

        <FormSelect
          label="Jenis Tanaman"
          value={form.jenis_bibit}
          onChange={(e) => update("jenis_bibit", e.target.value)}
          options={JENIS_BIBIT.map((j) => ({ value: j, label: j }))}
        />

        <FormInput
          label="Tanggal Tanam"
          type="date"
          value={form.tanggal_tanam}
          onChange={(e) => update("tanggal_tanam", e.target.value)}
        />

        <FormTextarea
          label="Catatan"
          placeholder="Catatan tambahan (opsional)"
          value={form.catatan}
          onChange={(e) => update("catatan", e.target.value)}
        />

        {/* Photo upload placeholder */}
        <div className="border-2 border-dashed border-border rounded-xl py-8 flex flex-col items-center gap-2 text-text-gray">
          <Camera size={32} />
          <span className="text-sm">Tambah Foto Lahan</span>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3.5 rounded-xl bg-action text-white font-semibold disabled:opacity-50 flex items-center justify-center gap-2"
        >
          {loading ? "Menyimpan..." : "✅ Simpan Lahan"}
        </button>
      </form>
    </div>
  );
}
```

**Step 2: Edit Lahan page**

`app/(app)/edit-lahan/[id]/page.tsx`:
```tsx
"use client";

import { useState, useEffect } from "react";
import { useRouter, useParams } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import { useToast } from "@/components/ui/toast-provider";
import { PageHeader } from "@/components/ui/page-header";
import { FormInput } from "@/components/ui/form-input";
import { FormSelect } from "@/components/ui/form-select";
import { FormTextarea } from "@/components/ui/form-textarea";
import { SkeletonCard } from "@/components/ui/skeleton-card";
import { JENIS_BIBIT, STATUS_LAHAN } from "@/lib/constants";
import { MapPin } from "lucide-react";

export default function EditLahanPage() {
  const router = useRouter();
  const params = useParams();
  const { showToast } = useToast();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({
    nama_lahan: "",
    lokasi: "",
    luas_m2: "",
    jenis_bibit: "Cabe Rawit",
    tanggal_tanam: "",
    status: "aktif",
    catatan: "",
  });

  useEffect(() => {
    async function load() {
      const supabase = createClient();
      const { data } = await supabase
        .from("lahan")
        .select("*")
        .eq("id", params.id)
        .single();

      if (data) {
        setForm({
          nama_lahan: data.nama_lahan,
          lokasi: data.lokasi || "",
          luas_m2: data.luas_m2?.toString() || "",
          jenis_bibit: data.jenis_bibit,
          tanggal_tanam: data.tanggal_tanam || "",
          status: data.status,
          catatan: data.catatan || "",
        });
      }
      setLoading(false);
    }
    load();
  }, [params.id]);

  function update(field: string, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);

    const supabase = createClient();
    const { error } = await supabase
      .from("lahan")
      .update({
        nama_lahan: form.nama_lahan,
        lokasi: form.lokasi || null,
        luas_m2: form.luas_m2 ? parseInt(form.luas_m2) : null,
        jenis_bibit: form.jenis_bibit,
        tanggal_tanam: form.tanggal_tanam || null,
        status: form.status,
        catatan: form.catatan || null,
      })
      .eq("id", params.id);

    setSaving(false);

    if (error) {
      showToast("error", "Gagal menyimpan. Coba lagi.");
      return;
    }

    showToast("success", "Lahan berhasil diupdate!");
    router.push("/profil");
    router.refresh();
  }

  if (loading) {
    return (
      <div>
        <PageHeader title="Edit Lahan" />
        <div className="space-y-4">
          <SkeletonCard />
          <SkeletonCard />
        </div>
      </div>
    );
  }

  return (
    <div>
      <PageHeader title="Edit Lahan" />

      <form onSubmit={handleSubmit} className="space-y-4">
        <FormInput
          label="Nama Lahan"
          value={form.nama_lahan}
          onChange={(e) => update("nama_lahan", e.target.value)}
        />
        <FormInput
          label="Lokasi"
          value={form.lokasi}
          onChange={(e) => update("lokasi", e.target.value)}
          icon={<MapPin size={18} />}
        />
        <FormInput
          label="Luas Lahan"
          type="number"
          value={form.luas_m2}
          onChange={(e) => update("luas_m2", e.target.value)}
          suffix="m²"
        />
        <FormSelect
          label="Jenis Tanaman"
          value={form.jenis_bibit}
          onChange={(e) => update("jenis_bibit", e.target.value)}
          options={JENIS_BIBIT.map((j) => ({ value: j, label: j }))}
        />
        <FormInput
          label="Tanggal Tanam"
          type="date"
          value={form.tanggal_tanam}
          onChange={(e) => update("tanggal_tanam", e.target.value)}
        />
        <FormSelect
          label="Status"
          value={form.status}
          onChange={(e) => update("status", e.target.value)}
          options={STATUS_LAHAN.map((s) => ({ value: s, label: s.charAt(0).toUpperCase() + s.slice(1) }))}
        />
        <FormTextarea
          label="Catatan"
          value={form.catatan}
          onChange={(e) => update("catatan", e.target.value)}
        />

        <button
          type="submit"
          disabled={saving}
          className="w-full py-3.5 rounded-xl bg-action text-white font-semibold disabled:opacity-50"
        >
          {saving ? "Menyimpan..." : "💾 Simpan Perubahan"}
        </button>
      </form>
    </div>
  );
}
```

**Step 3: Commit**

```bash
git add -A
git commit -m "feat: tambah lahan and edit lahan forms with validation"
```

---

## Task 8: Input Harian Form

**Files:**
- Create: `app/(app)/input-harian/page.tsx`

**Step 1: Input Harian page**

`app/(app)/input-harian/page.tsx`:
```tsx
"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import { useToast } from "@/components/ui/toast-provider";
import { PageHeader } from "@/components/ui/page-header";
import { FormInput } from "@/components/ui/form-input";
import { FormSelect } from "@/components/ui/form-select";
import { FormTextarea } from "@/components/ui/form-textarea";
import { EmptyState } from "@/components/ui/empty-state";
import { JENIS_PUPUK, KONDISI_TANAMAN } from "@/lib/constants";
import { Camera, Sprout } from "lucide-react";
import type { Lahan } from "@/lib/types";

export default function InputHarianPage() {
  const router = useRouter();
  const { showToast } = useToast();
  const [lahanList, setLahanList] = useState<Lahan[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [usePupuk, setUsePupuk] = useState(false);
  const [form, setForm] = useState({
    lahan_id: "",
    tanggal: new Date().toISOString().split("T")[0],
    suhu_celcius: "",
    kelembaban_persen: "",
    ph_tanah: "",
    air_liter: "",
    pupuk_jenis: "NPK",
    pupuk_jumlah_gram: "",
    kondisi_tanaman: "Sehat",
    catatan: "",
  });

  useEffect(() => {
    async function load() {
      const supabase = createClient();
      const { data: { user } } = await supabase.auth.getUser();
      const { data } = await supabase
        .from("lahan")
        .select("*")
        .eq("user_id", user!.id)
        .eq("status", "aktif");

      if (data && data.length > 0) {
        setLahanList(data);
        setForm((prev) => ({ ...prev, lahan_id: data[0].id }));
      }
      setLoading(false);
    }
    load();
  }, []);

  function update(field: string, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.lahan_id) return;

    setSaving(true);
    const supabase = createClient();

    const { error } = await supabase.from("log_harian").insert({
      lahan_id: form.lahan_id,
      tanggal: form.tanggal,
      suhu_celcius: form.suhu_celcius ? parseFloat(form.suhu_celcius) : null,
      kelembaban_persen: form.kelembaban_persen ? parseFloat(form.kelembaban_persen) : null,
      ph_tanah: form.ph_tanah ? parseFloat(form.ph_tanah) : null,
      air_liter: form.air_liter ? parseFloat(form.air_liter) : null,
      pupuk_jenis: usePupuk ? form.pupuk_jenis : null,
      pupuk_jumlah_gram: usePupuk && form.pupuk_jumlah_gram ? parseFloat(form.pupuk_jumlah_gram) : null,
      kondisi_tanaman: form.kondisi_tanaman,
      catatan: form.catatan || null,
    });

    setSaving(false);

    if (error) {
      showToast("error", "Gagal menyimpan. Coba lagi.");
      return;
    }

    showToast("success", "Data berhasil disimpan!");
    router.push("/beranda");
    router.refresh();
  }

  if (loading) return null;

  if (lahanList.length === 0) {
    return (
      <div>
        <PageHeader title="Catat Data Harian" />
        <EmptyState
          icon={<Sprout size={28} className="text-primary" />}
          title="Belum ada lahan"
          description="Tambahkan lahan pertama kamu"
          actionLabel="+ Tambah Lahan"
          href="/tambah-lahan"
        />
      </div>
    );
  }

  return (
    <div>
      <PageHeader title="Catat Data Harian" />

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Lahan selector */}
        {lahanList.length > 1 && (
          <FormSelect
            label="Pilih Lahan"
            value={form.lahan_id}
            onChange={(e) => update("lahan_id", e.target.value)}
            options={lahanList.map((l) => ({ value: l.id, label: l.nama_lahan }))}
          />
        )}

        <FormInput
          label="Tanggal"
          type="date"
          value={form.tanggal}
          onChange={(e) => update("tanggal", e.target.value)}
        />

        <FormInput
          label="Suhu"
          type="number"
          placeholder="32"
          value={form.suhu_celcius}
          onChange={(e) => update("suhu_celcius", e.target.value)}
          suffix="°C"
        />

        <FormInput
          label="Kelembaban Tanah"
          type="number"
          placeholder="75"
          value={form.kelembaban_persen}
          onChange={(e) => update("kelembaban_persen", e.target.value)}
          suffix="%"
        />

        <FormInput
          label="pH Tanah"
          type="number"
          step="0.1"
          placeholder="6.5"
          value={form.ph_tanah}
          onChange={(e) => update("ph_tanah", e.target.value)}
        />

        <FormInput
          label="Air Disiram"
          type="number"
          placeholder="5"
          value={form.air_liter}
          onChange={(e) => update("air_liter", e.target.value)}
          suffix="liter"
        />

        {/* Pupuk toggle */}
        <div className="space-y-3">
          <label className="flex items-center gap-3 cursor-pointer">
            <div
              className={`w-12 h-7 rounded-full transition-colors relative ${
                usePupuk ? "bg-action" : "bg-gray-300"
              }`}
              onClick={() => setUsePupuk(!usePupuk)}
            >
              <div
                className={`w-5 h-5 bg-white rounded-full absolute top-1 transition-transform ${
                  usePupuk ? "translate-x-6" : "translate-x-1"
                }`}
              />
            </div>
            <span className="text-sm font-medium text-text-dark">
              Hari ini pakai pupuk?
            </span>
          </label>

          {usePupuk && (
            <div className="space-y-3 pl-2 border-l-2 border-action ml-3">
              <FormSelect
                label="Jenis Pupuk"
                value={form.pupuk_jenis}
                onChange={(e) => update("pupuk_jenis", e.target.value)}
                options={JENIS_PUPUK.map((p) => ({ value: p, label: p }))}
              />
              <FormInput
                label="Jumlah Pupuk"
                type="number"
                placeholder="100"
                value={form.pupuk_jumlah_gram}
                onChange={(e) => update("pupuk_jumlah_gram", e.target.value)}
                suffix="gram"
              />
            </div>
          )}
        </div>

        {/* Kondisi Tanaman pills */}
        <div className="space-y-1.5">
          <label className="text-sm font-medium text-text-dark">Kondisi Tanaman</label>
          <div className="flex flex-wrap gap-2">
            {KONDISI_TANAMAN.map((k) => (
              <button
                key={k}
                type="button"
                onClick={() => update("kondisi_tanaman", k)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                  form.kondisi_tanaman === k
                    ? "bg-primary text-white"
                    : "bg-gray-100 text-text-gray"
                }`}
              >
                {k}
              </button>
            ))}
          </div>
        </div>

        {/* Photo placeholder */}
        <div className="border-2 border-dashed border-border rounded-xl py-8 flex flex-col items-center gap-2 text-text-gray">
          <Camera size={32} />
          <span className="text-sm">Tambah Foto Tanaman</span>
        </div>

        <FormTextarea
          label="Catatan"
          placeholder="Catatan tambahan (opsional)"
          value={form.catatan}
          onChange={(e) => update("catatan", e.target.value)}
        />

        <button
          type="submit"
          disabled={saving}
          className="w-full py-3.5 rounded-xl bg-action text-white font-semibold disabled:opacity-50"
        >
          {saving ? "Menyimpan..." : "💾 Simpan Data"}
        </button>
      </form>
    </div>
  );
}
```

**Step 2: Commit**

```bash
git add -A
git commit -m "feat: input harian form with pupuk toggle and kondisi pills"
```

---

## Task 9: Lahan Detail Page

**Files:**
- Create: `app/(app)/lahan/page.tsx`

**Step 1: Lahan detail page**

`app/(app)/lahan/page.tsx`:
```tsx
"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import { SensorCard } from "@/components/ui/sensor-card";
import { InfoGrid } from "@/components/ui/info-grid";
import { EmptyState } from "@/components/ui/empty-state";
import { SkeletonCard } from "@/components/ui/skeleton-card";
import { getSensorStatus, getWaterStatus, daysBetween, formatDate } from "@/lib/utils";
import { HARI_PANEN } from "@/lib/constants";
import {
  Thermometer, Droplets, FlaskConical, CloudRain,
  Home, MapPin, Maximize, Sprout, Calendar, Activity,
  Clock, Pen, ChevronDown, TreePine,
} from "lucide-react";
import type { Lahan, LogHarian } from "@/lib/types";

export default function LahanPage() {
  const searchParams = useSearchParams();
  const initialId = searchParams.get("id");

  const [lahanList, setLahanList] = useState<Lahan[]>([]);
  const [selectedId, setSelectedId] = useState<string>(initialId || "");
  const [latestLog, setLatestLog] = useState<LogHarian | null>(null);
  const [loading, setLoading] = useState(true);
  const [showDropdown, setShowDropdown] = useState(false);

  useEffect(() => {
    async function load() {
      const supabase = createClient();
      const { data: { user } } = await supabase.auth.getUser();
      const { data } = await supabase
        .from("lahan")
        .select("*")
        .eq("user_id", user!.id);

      if (data && data.length > 0) {
        setLahanList(data);
        if (!selectedId) setSelectedId(data[0].id);
      }
      setLoading(false);
    }
    load();
  }, []);

  useEffect(() => {
    if (!selectedId) return;
    async function loadLog() {
      const supabase = createClient();
      const { data } = await supabase
        .from("log_harian")
        .select("*")
        .eq("lahan_id", selectedId)
        .order("tanggal", { ascending: false })
        .limit(1)
        .single();
      setLatestLog(data);
    }
    loadLog();
  }, [selectedId]);

  if (loading) {
    return (
      <div className="pt-6 space-y-4">
        <SkeletonCard />
        <SkeletonCard />
      </div>
    );
  }

  if (lahanList.length === 0) {
    return (
      <div className="pt-6">
        <EmptyState
          icon={<TreePine size={28} className="text-primary" />}
          title="Belum ada lahan"
          description="Tambahkan lahan pertama kamu"
          actionLabel="+ Tambah Lahan"
          href="/tambah-lahan"
        />
      </div>
    );
  }

  const lahan = lahanList.find((l) => l.id === selectedId)!;
  const usiaTanaman = lahan.tanggal_tanam ? daysBetween(lahan.tanggal_tanam) : 0;
  const hariPanen = HARI_PANEN[lahan.jenis_bibit] || 90;
  const sisaPanen = Math.max(0, hariPanen - usiaTanaman);

  const suhuStatus = latestLog?.suhu_celcius
    ? getSensorStatus("suhu", latestLog.suhu_celcius)
    : { label: "—", color: "green" as const };
  const kelembabanStatus = latestLog?.kelembaban_persen
    ? getSensorStatus("kelembaban", latestLog.kelembaban_persen)
    : { label: "—", color: "green" as const };
  const phStatus = latestLog?.ph_tanah
    ? getSensorStatus("ph", latestLog.ph_tanah)
    : { label: "—", color: "green" as const };
  const airStatus = getWaterStatus(
    latestLog?.suhu_celcius || null,
    latestLog?.kelembaban_persen || null
  );

  return (
    <div className="pt-6">
      {/* Lahan Selector */}
      <div className="relative mb-6">
        <button
          onClick={() => setShowDropdown(!showDropdown)}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-card border border-border shadow-sm"
        >
          <MapPin size={16} className="text-primary" />
          <span className="font-medium">{lahan.nama_lahan}</span>
          <ChevronDown size={16} className="text-text-gray" />
        </button>
        {showDropdown && (
          <div className="absolute top-12 left-0 bg-card rounded-xl shadow-lg border border-border z-10 min-w-[200px]">
            {lahanList.map((l) => (
              <button
                key={l.id}
                onClick={() => {
                  setSelectedId(l.id);
                  setShowDropdown(false);
                }}
                className={`w-full text-left px-4 py-3 text-sm hover:bg-gray-50 first:rounded-t-xl last:rounded-b-xl ${
                  l.id === selectedId ? "font-semibold text-primary" : ""
                }`}
              >
                {l.nama_lahan}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Info Lahan Card */}
      <div className="bg-card rounded-xl p-4 shadow-sm mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-semibold text-text-dark flex items-center gap-2">
            <Sprout size={20} className="text-primary" />
            Info Lahan
          </h2>
          <a href={`/edit-lahan/${lahan.id}`}>
            <Pen size={18} className="text-primary" />
          </a>
        </div>
        <InfoGrid
          items={[
            { icon: <Home size={16} />, label: "Nama", value: lahan.nama_lahan },
            { icon: <MapPin size={16} />, label: "Lokasi", value: lahan.lokasi || "-" },
            { icon: <Maximize size={16} />, label: "Luas", value: `${lahan.luas_m2 || "-"} m²` },
            { icon: <Sprout size={16} />, label: "Jenis Bibit", value: lahan.jenis_bibit },
            { icon: <Calendar size={16} />, label: "Tanggal Tanam", value: lahan.tanggal_tanam ? formatDate(lahan.tanggal_tanam) : "-" },
            { icon: <Activity size={16} />, label: "Status", value: lahan.status.charAt(0).toUpperCase() + lahan.status.slice(1) },
            { icon: <Clock size={16} />, label: "Usia Tanaman", value: `${usiaTanaman} hari` },
            { icon: <Calendar size={16} />, label: "Estimasi Panen", value: `${sisaPanen} hari lagi`, highlight: true },
          ]}
        />
      </div>

      {/* Kondisi Terakhir */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-3">
          <h2 className="font-semibold text-text-dark">Kondisi Terakhir</h2>
          {latestLog && (
            <span className="text-xs text-text-gray">
              Update: {formatDate(latestLog.tanggal)}
            </span>
          )}
        </div>

        {latestLog ? (
          <div className="grid grid-cols-2 gap-3">
            <SensorCard
              icon={<Thermometer size={20} className="text-red-400" />}
              label="Suhu"
              value={`${latestLog.suhu_celcius || "-"}°C`}
              status={suhuStatus.label}
              statusColor={suhuStatus.color}
            />
            <SensorCard
              icon={<Droplets size={20} className="text-blue-400" />}
              label="Kelembaban"
              value={`${latestLog.kelembaban_persen || "-"}%`}
              status={kelembabanStatus.label}
              statusColor={kelembabanStatus.color}
            />
            <SensorCard
              icon={<FlaskConical size={20} className="text-purple-400" />}
              label="pH Tanah"
              value={`${latestLog.ph_tanah || "-"}`}
              status={phStatus.label}
              statusColor={phStatus.color}
            />
            <SensorCard
              icon={<CloudRain size={20} className="text-cyan-400" />}
              label="Kebutuhan Air"
              value={airStatus.label}
              status={airStatus.label}
              statusColor={airStatus.color}
            />
          </div>
        ) : (
          <EmptyState
            icon={<Sprout size={28} className="text-primary" />}
            title="Belum ada data"
            description="Yuk mulai catat data harian kamu"
            actionLabel="✏️ Mulai Catat"
            href="/input-harian"
          />
        )}
      </div>
    </div>
  );
}
```

**Step 2: Commit**

```bash
git add -A
git commit -m "feat: lahan detail page with sensor cards and info grid"
```

---

## Task 10: Riwayat Page

**Files:**
- Create: `app/(app)/riwayat/page.tsx`

**Step 1: Riwayat page**

`app/(app)/riwayat/page.tsx`:
```tsx
"use client";

import { useState, useEffect } from "react";
import { createClient } from "@/lib/supabase/client";
import { EmptyState } from "@/components/ui/empty-state";
import { SkeletonCard } from "@/components/ui/skeleton-card";
import { FormSelect } from "@/components/ui/form-select";
import { formatDate } from "@/lib/utils";
import { Clipboard, Thermometer, Droplets, FlaskConical, CloudRain, FlaskRound } from "lucide-react";
import type { Lahan, LogHarian } from "@/lib/types";

export default function RiwayatPage() {
  const [lahanList, setLahanList] = useState<Lahan[]>([]);
  const [selectedLahan, setSelectedLahan] = useState("all");
  const [logs, setLogs] = useState<LogHarian[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const supabase = createClient();
      const { data: { user } } = await supabase.auth.getUser();
      const { data } = await supabase
        .from("lahan")
        .select("*")
        .eq("user_id", user!.id);
      setLahanList(data || []);
      setLoading(false);
    }
    load();
  }, []);

  useEffect(() => {
    async function loadLogs() {
      const supabase = createClient();

      let query = supabase
        .from("log_harian")
        .select("*, lahan:lahan_id(nama_lahan)")
        .order("tanggal", { ascending: false })
        .limit(50);

      if (selectedLahan !== "all") {
        query = query.eq("lahan_id", selectedLahan);
      } else if (lahanList.length > 0) {
        query = query.in("lahan_id", lahanList.map((l) => l.id));
      }

      const { data } = await query;
      setLogs(data || []);
    }

    if (lahanList.length > 0) loadLogs();
  }, [selectedLahan, lahanList]);

  if (loading) {
    return (
      <div className="pt-6 space-y-4">
        <SkeletonCard variant="small" />
        <SkeletonCard />
        <SkeletonCard />
      </div>
    );
  }

  return (
    <div className="pt-6">
      <h1 className="text-2xl font-bold text-text-dark mb-4">Riwayat</h1>

      {/* Filter */}
      {lahanList.length > 0 && (
        <div className="mb-4">
          <FormSelect
            label=""
            value={selectedLahan}
            onChange={(e) => setSelectedLahan(e.target.value)}
            options={[
              { value: "all", label: "Semua Lahan" },
              ...lahanList.map((l) => ({ value: l.id, label: l.nama_lahan })),
            ]}
          />
        </div>
      )}

      {logs.length === 0 ? (
        <EmptyState
          icon={<Clipboard size={28} className="text-warning" />}
          title="Belum ada riwayat"
          description="Mulai input data harian untuk melihat riwayat"
          actionLabel="+ Input Data"
          href="/input-harian"
          variant="orange"
        />
      ) : (
        <div className="space-y-3">
          {logs.map((log) => (
            <div key={log.id} className="bg-card rounded-xl p-4 shadow-sm">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold text-text-dark">{formatDate(log.tanggal)}</h3>
                <span className="text-xs text-text-gray px-2 py-1 bg-gray-100 rounded-full">
                  {(log as any).lahan?.nama_lahan}
                </span>
              </div>

              <div className="flex flex-wrap gap-2 mb-2">
                {log.suhu_celcius && (
                  <span className="inline-flex items-center gap-1 text-xs bg-red-50 text-red-600 px-2 py-1 rounded-full">
                    <Thermometer size={12} /> {log.suhu_celcius}°C
                  </span>
                )}
                {log.kelembaban_persen && (
                  <span className="inline-flex items-center gap-1 text-xs bg-blue-50 text-blue-600 px-2 py-1 rounded-full">
                    <Droplets size={12} /> {log.kelembaban_persen}%
                  </span>
                )}
                {log.ph_tanah && (
                  <span className="inline-flex items-center gap-1 text-xs bg-purple-50 text-purple-600 px-2 py-1 rounded-full">
                    <FlaskConical size={12} /> pH {log.ph_tanah}
                  </span>
                )}
                {log.air_liter && (
                  <span className="inline-flex items-center gap-1 text-xs bg-cyan-50 text-cyan-600 px-2 py-1 rounded-full">
                    <CloudRain size={12} /> {log.air_liter}L
                  </span>
                )}
                {log.pupuk_jenis && (
                  <span className="inline-flex items-center gap-1 text-xs bg-green-50 text-green-600 px-2 py-1 rounded-full">
                    <FlaskRound size={12} /> {log.pupuk_jenis} {log.pupuk_jumlah_gram ? `${log.pupuk_jumlah_gram}g` : ""}
                  </span>
                )}
                {log.kondisi_tanaman && (
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    log.kondisi_tanaman === "Sehat" ? "bg-success-bg text-success" :
                    log.kondisi_tanaman === "Berbuah" ? "bg-orange-50 text-warning" :
                    "bg-error-bg text-error"
                  }`}>
                    {log.kondisi_tanaman}
                  </span>
                )}
              </div>

              {log.catatan && (
                <p className="text-sm text-text-gray mt-2">{log.catatan}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

**Step 2: Commit**

```bash
git add -A
git commit -m "feat: riwayat page with filter and log cards"
```

---

## Task 11: Profil Page

**Files:**
- Create: `app/(app)/profil/page.tsx`

**Step 1: Profil page**

`app/(app)/profil/page.tsx`:
```tsx
"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { createClient } from "@/lib/supabase/client";
import { FarmCard } from "@/components/ui/farm-card";
import { SkeletonCard } from "@/components/ui/skeleton-card";
import { getInitials } from "@/lib/utils";
import { Calculator, Settings, HelpCircle, LogOut, ChevronRight } from "lucide-react";
import type { User, Lahan } from "@/lib/types";

export default function ProfilPage() {
  const router = useRouter();
  const [profile, setProfile] = useState<User | null>(null);
  const [lahanList, setLahanList] = useState<Lahan[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const supabase = createClient();
      const { data: { user } } = await supabase.auth.getUser();

      const [{ data: prof }, { data: lahan }] = await Promise.all([
        supabase.from("users").select("*").eq("id", user!.id).single(),
        supabase.from("lahan").select("*").eq("user_id", user!.id).order("created_at", { ascending: false }),
      ]);

      setProfile(prof);
      setLahanList(lahan || []);
      setLoading(false);
    }
    load();
  }, []);

  async function handleLogout() {
    const supabase = createClient();
    await supabase.auth.signOut();
    router.push("/login");
    router.refresh();
  }

  if (loading) {
    return (
      <div className="pt-6 space-y-4">
        <SkeletonCard />
        <SkeletonCard />
        <SkeletonCard variant="small" />
      </div>
    );
  }

  return (
    <div className="pt-6">
      <h1 className="text-2xl font-bold text-text-dark mb-6">Profil Saya</h1>

      {/* Profile Card */}
      <div className="bg-card rounded-xl p-4 shadow-sm mb-6">
        <div className="flex items-center gap-4 mb-4">
          <div className="w-14 h-14 rounded-full bg-primary flex items-center justify-center text-white font-bold text-lg">
            {profile ? getInitials(profile.nama) : "?"}
          </div>
          <div>
            <h2 className="font-semibold text-text-dark text-lg">{profile?.nama}</h2>
            <p className="text-sm text-text-gray">{profile?.email}</p>
          </div>
        </div>
        <button className="w-full py-2.5 rounded-lg border border-border text-text-dark text-sm font-medium">
          ✏️ Edit Profil
        </button>
      </div>

      {/* Lahan Saya */}
      <div className="mb-6">
        <h2 className="font-semibold text-text-dark mb-3">Lahan Saya</h2>
        <div className="space-y-3">
          {lahanList.map((lahan) => (
            <FarmCard key={lahan.id} lahan={lahan} />
          ))}
        </div>
        <Link
          href="/tambah-lahan"
          className="block w-full py-3.5 rounded-xl bg-action text-white font-semibold text-center mt-3"
        >
          + Tambah Lahan Baru
        </Link>
      </div>

      {/* Menu */}
      <div className="bg-card rounded-xl shadow-sm divide-y divide-gray-100 mb-6">
        <MenuItem icon={Calculator} label="Kalkulator Keuntungan" href="#" />
        <MenuItem icon={Settings} label="Pengaturan" href="#" />
        <MenuItem icon={HelpCircle} label="Bantuan & Panduan" href="#" />
      </div>

      {/* Logout */}
      <button
        onClick={handleLogout}
        className="w-full flex items-center justify-between px-4 py-4 bg-card rounded-xl shadow-sm text-error"
      >
        <span className="flex items-center gap-3 font-medium">
          <LogOut size={20} />
          Keluar
        </span>
        <ChevronRight size={18} />
      </button>
    </div>
  );
}

function MenuItem({
  icon: Icon,
  label,
  href,
}: {
  icon: any;
  label: string;
  href: string;
}) {
  return (
    <Link href={href} className="flex items-center justify-between px-4 py-4">
      <span className="flex items-center gap-3 text-text-dark">
        <Icon size={20} className="text-text-gray" />
        <span className="font-medium">{label}</span>
      </span>
      <ChevronRight size={18} className="text-text-gray" />
    </Link>
  );
}
```

**Step 2: Commit**

```bash
git add -A
git commit -m "feat: profil page with farm cards, menu, and logout"
```

---

## Task 12: Final Polish + Deploy Check

**Step 1: Verify all pages render**

```bash
cd ~/Documents/14_Web-projects/tancab && npm run build
```

Expected: Build succeeds with no errors.

**Step 2: Test dev server**

```bash
npm run dev
```

Manually test: /login → register → /beranda → /tambah-lahan → /lahan → /input-harian → /riwayat → /profil

**Step 3: Create .gitignore additions**

Ensure `.env.local` is in `.gitignore` (create-next-app does this by default).

**Step 4: Final commit**

```bash
git add -A
git commit -m "chore: final build verification"
```

---

## Setup Checklist (Before Running)

1. Create Supabase project at supabase.com
2. Run `supabase/schema.sql` in Supabase SQL Editor
3. Create `.env.local` from `.env.local.example` with real keys
4. Enable Email Auth in Supabase → Authentication → Providers
5. Create Storage bucket `photos` in Supabase (for future photo uploads)
6. `npm run dev` and test

---

## Summary

| Task | What | Files |
|------|------|-------|
| 1 | Project scaffold + Tailwind config | 5 files |
| 2 | Supabase schema + client + types | 8 files |
| 3 | All shared UI components | 14 files |
| 4 | Auth pages (login + register) | 3 files |
| 5 | App layout (bottom nav + guard) | 1 file |
| 6 | Dashboard (Beranda) | 1 file |
| 7 | Tambah Lahan + Edit Lahan | 2 files |
| 8 | Input Harian form | 1 file |
| 9 | Lahan Detail page | 1 file |
| 10 | Riwayat page | 1 file |
| 11 | Profil page | 1 file |
| 12 | Build verify + deploy check | 0 new files |

**Total: 12 tasks, ~37 files, ~11 commits**
