# Tancab (Tanam Cabe) — Design Document

**Date:** 2026-04-16
**Status:** Final — Ready to Build

## Overview

Web app untuk monitoring dan optimasi pertanian cabe. Petani input data harian (suhu, kelembaban tanah, pH, air, pupuk, foto). App simpan history, tampilkan trend, dan kalkulasi profit.

**Target user:** Petani cabe, termasuk orang tua — UI harus sangat simpel.
**Platform:** Responsive web (mobile-first), deploy di Vercel (free tier).
**Stack:** Next.js 14 + Supabase (Auth + PostgreSQL + Storage) + Tailwind CSS.

## Roadmap

1. **MVP (sekarang)** — Web app, input manual via form, untuk lahan sendiri
2. **Kalkulator** — Simulasi profit berdasarkan luas lahan + estimasi panen
3. **Multi-user** — Buka untuk petani lain
4. **IoT** — Sensor hardware (ESP32 + suhu/kelembaban/pH sensors)

---

## Data Model

### users
| Field | Type | Notes |
|-------|------|-------|
| id | uuid | PK, from Supabase Auth |
| nama | text | |
| email | text | |
| phone | text | nullable |
| created_at | timestamptz | |

### lahan
| Field | Type | Notes |
|-------|------|-------|
| id | uuid | PK |
| user_id | uuid | FK → users |
| nama_lahan | text | "Kebun Belakang" |
| lokasi | text | kota/kabupaten |
| luas_m2 | integer | luas dalam m² |
| jenis_bibit | text | "Cabe Rawit", "Cabe Merah", "Cabe Keriting" |
| tanggal_tanam | date | |
| status | text | "aktif", "panen", "istirahat" |
| foto_url | text | nullable, foto lahan |
| catatan | text | nullable |
| created_at | timestamptz | |

### log_harian
| Field | Type | Notes |
|-------|------|-------|
| id | uuid | PK |
| lahan_id | uuid | FK → lahan |
| tanggal | date | |
| suhu_celcius | decimal | |
| kelembaban_persen | decimal | kelembaban tanah % |
| ph_tanah | decimal | |
| air_liter | decimal | berapa liter disiram |
| pupuk_jenis | text | nullable, "NPK", "Organik", "ZA" |
| pupuk_jumlah_gram | decimal | nullable |
| kondisi_tanaman | text | "Sehat", "Layu", "Kuning", "Berbuah" |
| foto_url | text | nullable |
| catatan | text | nullable |
| created_at | timestamptz | |

### kalkulator_simulasi
| Field | Type | Notes |
|-------|------|-------|
| id | uuid | PK |
| user_id | uuid | FK → users |
| luas_hektar | decimal | |
| estimasi_hasil_kg | decimal | |
| harga_per_kg | integer | Rupiah |
| total_pendapatan | integer | |
| total_biaya | integer | |
| profit | integer | |
| created_at | timestamptz | |

**Computed fields (client-side):**
- Usia Tanaman = today - tanggal_tanam (days)
- Estimasi Panen = ~90 hari (cabe rawit) dari tanggal_tanam - today
- Kebutuhan Air = derived from suhu + kelembaban

---

## Design System

### Colors
```
Primary:       #2D5A27  (dark green — nav active, headers)
Action:        #4CAF50  (buttons, success states, CTA)
Background:    #F5F5F0  (warm light beige — page bg)
Card:          #FFFFFF  (white — all cards)
Warning:       #FF9800  (orange — countdown, riwayat empty)
Error:         #E53935  (red — toast, validation, danger values)
Error BG:      #FFEBEE  (light red — error toast bg)
Success:       #4CAF50  (green — status badge, success toast icon)
Success BG:    #E8F5E9  (light green — success toast bg)
Text Dark:     #1A1A1A  (primary text)
Text Gray:     #757575  (captions, secondary text)
Border:        #E0E0E0  (input borders, dividers)
Sensor Normal: #E8F5E9  (light green bg for sensor cards)
```

### Typography
```
Font:          System sans-serif (Inter or similar)
Heading:       24px, bold (page titles)
Subheading:    18px, semibold (section titles)
Body:          16px, regular
Caption:       14px, regular, #757575
Stat Number:   28px, bold (sensor readings, stat values)
Button:        16px, semibold, white on green
```

### Spacing & Radius
```
Card padding:  16px
Card radius:   12px
Button radius: 12px (full-width), 20px (pill)
Gap:           12px between cards
Page padding:  16px horizontal
Bottom nav:    64px height
```

### Components
1. **Bottom Nav** — 4 tabs, active = filled icon + green bg pill
2. **Stat Card** — Icon + number + label, rounded, light bg
3. **Farm Card** — Icon + name + location badge + 3 detail cols + 2 action buttons
4. **Sensor Card** — Icon + label + value + status badge, 2x2 grid
5. **Activity Item** — Circle icon bg + title + subtitle (time ago)
6. **Form Input** — 3 states: default (gray), success (green + checkmark), error (red + message)
7. **Toast** — Success (green border, green bg) / Error (red border, pink bg), dismissable
8. **Empty State** — Centered icon in circle + bold text + description + CTA button
9. **Skeleton** — Pulse animation, rounded shapes matching card layouts
10. **Status Badge** — Small pill "Aktif" green, "Panen" orange, "Istirahat" gray
11. **Dropdown Selector** — Pill shape with location icon + chevron down
12. **Info Grid** — 2-column, icon + label + value per cell

---

## Pages

### 1. Beranda (Dashboard)
- Greeting: "Selamat Pagi, [nama]" + wave emoji + notification bell
- Weather card: icon + temp + location (hardcoded or API later)
- 3 stat cards row: Total Lahan, Tanaman Aktif, Panen (hari countdown)
- "Catat Data Hari Ini" CTA button (green, full-width)
- Aktivitas Terakhir list (recent log entries across all lahan)
- Empty state jika belum ada data

### 2. Lahan (Detail Management)
- Dropdown selector top: pilih lahan (switch antar lahan)
- Info Lahan card: 2x4 grid (nama, lokasi, luas, jenis bibit, tanggal tanam, status, usia tanaman, estimasi panen) + edit icon
- Kondisi Terakhir: timestamp + 2x2 sensor cards (suhu, kelembaban, pH, kebutuhan air) with status badges
- Tren Kondisi Lahan: line chart 7 hari (suhu + kelembaban trend)
- Empty state jika belum ada lahan

### 3. Riwayat (History)
- Filter: dropdown pilih lahan + date range picker
- List/timeline view: cards per hari
  - Tanggal (heading)
  - Suhu, kelembaban, pH, air, pupuk — inline badges
  - Foto thumbnail jika ada
  - Kondisi tanaman badge
  - Catatan text
- Bisa scroll infinite / pagination
- Empty state jika belum ada riwayat

### 4. Profil
- Profile card: avatar (initials), nama, email, "Edit Profil" button
- Lahan Saya: list of farm cards (nama, lokasi, luas, tanaman, tanggal, status) + Edit/Lihat Data buttons
- "+ Tambah Lahan Baru" button (green, full-width)
- Menu list: Kalkulator Keuntungan, Pengaturan, Bantuan & Panduan
- "Keluar" (red text)

### 5. Tambah Lahan (Form — sub-page)
- Back arrow + "Tambah Lahan Baru" title
- Fields: Nama Lahan*, Lokasi, Luas Lahan (m²), Jenis Tanaman (dropdown), Tanggal Tanam (date picker), Catatan (textarea)
- Tambah Foto Lahan (camera/upload area)
- "Simpan Lahan" button (green, full-width)
- Validation: inline errors per field

### 6. Input Harian (Form — sub-page, DESIGNED by us)
- Back arrow + "Catat Data Harian" title
- Lahan selector (jika punya >1 lahan)
- Fields:
  - Tanggal (default hari ini, bisa ubah)
  - Suhu (°C) — number input
  - Kelembaban Tanah (%) — number input
  - pH Tanah — number input (step 0.1)
  - Air Disiram (liter) — number input
  - Pupuk — toggle "Hari ini pakai pupuk?" → expand: jenis (dropdown) + jumlah (gram)
  - Kondisi Tanaman — pill selector: Sehat / Layu / Kuning / Berbuah
  - Foto Tanaman — camera/upload
  - Catatan — textarea
- "Simpan Data" button (green, full-width)
- Success toast after save

### 7. Kalkulator Keuntungan (sub-page, DESIGNED by us)
- Back arrow + "Kalkulator Keuntungan" title
- Input section:
  - Luas Lahan (m² atau hektar toggle)
  - Jenis Cabe (dropdown — affects yield estimate)
  - Estimasi Hasil Panen (kg) — auto-suggest based on luas + jenis, editable
  - Harga Jual per Kg (Rp) — default Rp30.000, editable
  - Biaya section: Bibit, Pupuk, Pestisida, Air, Tenaga Kerja, Lainnya
- Hasil Kalkulasi card:
  - Total Pendapatan (green, large)
  - Total Biaya (red)
  - Profit Bersih (bold, large)
  - ROI %
- "Simpan Simulasi" button
- Note: harga cabe fluktuatif, ini estimasi saja

### 8. Pengaturan (sub-page)
- Sections with list items:
  - **Akun:** Nama, Email, Ubah Password (→ chevron)
  - **Notifikasi:** Pengingat Harian (toggle), Waktu Pengingat, Notifikasi Panen (toggle)
  - **Aplikasi:** Bahasa, Tema (Terang), Satuan Luas (m²)
  - **Data:** Ekspor Data (→ chevron)

---

## Responsive Behavior

- **Mobile (< 640px):** Full-width cards, single column, bottom nav visible
- **Tablet (640-1024px):** 2-column grid for cards, bottom nav → side nav optional
- **Desktop (> 1024px):** Centered max-width 480px (app-like), or expand to dashboard layout

MVP focus: mobile-first. Desktop = centered mobile layout.

---

## Tech Stack

```
Framework:    Next.js 14 (App Router)
Styling:      Tailwind CSS
UI:           Custom components (no shadcn — too complex for this)
Database:     Supabase PostgreSQL
Auth:         Supabase Auth (email + password)
Storage:      Supabase Storage (foto upload)
Charts:       Chart.js or Recharts (tren kondisi)
Deploy:       Vercel (free tier)
Icons:        Lucide React
```

---

## MVP Scope (Build Now)

**In:**
- Auth (login/register)
- CRUD Lahan
- Input Harian form
- Dashboard with stats
- Lahan detail with sensor readings
- Riwayat list
- Profil page
- Empty states, loading skeletons, toasts
- Responsive mobile-first

**Out (Later):**
- Kalkulator Keuntungan (Phase 2)
- Pengaturan page (Phase 2)
- IoT sensor integration (Phase 4)
- Multi-user public registration (Phase 3)
- Push notifications
- Weather API integration
- AI recommendations
- Data export
