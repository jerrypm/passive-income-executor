# Chrome Web Store Listing — Judol & Adult Blocker

This document is the copy-paste source for the Chrome Web Store developer console submission. Everything below is drafted and ready; manual tasks (screenshots, promo tile, hosting the privacy policy) are marked `TODO` / `PLACEHOLDER`.

---

## 1. Title

```
Judol & Adult Blocker — Indonesia
```

**Character count: 33 / 50** (within CWS 50-char limit)

---

## 2. Summary (Short description)

```
Blokir iklan judi online (judol) dan konten dewasa di semua situs. Gratis, ringan, tanpa tracking.
```

**Character count: 98 / 132** (within CWS 132-char limit)

---

## 3. Detailed description

Paste the block below into the "Detailed description" field in the Chrome Web Store developer console. Indonesian primary, short English summary at the bottom.

```
Bosan dibanjiri iklan judi online (judol) di setiap situs berita, forum, dan portal Indonesia? Banner Slot, DominoQQ, "Gacor Maxwin", popup bandar bola — muncul di Detik, Kompas, Tribun, Kaskus, dan hampir semua halaman yang kamu buka. Ekstensi ini menghentikan semua itu.

MASALAH
Iklan judol sekarang disuntikkan langsung ke halaman (inline ads), bukan cuma lewat jaringan iklan biasa. Adblocker umum sering kecolongan karena iklan ini di-serve dari domain first-party situsnya sendiri. Belum lagi konten dewasa yang nyelip di pop-under dan redirect.

SOLUSI
Judol & Adult Blocker bekerja di dua lapis sekaligus:
1. Network-level blocking pakai Chrome declarativeNetRequest — cepat, native, zero overhead.
2. DOM scanner yang nyari keyword judol di halaman dan menyembunyikan elemen iklan yang lolos dari blocklist domain.

FITUR
✅ Blokir ~30.000 domain konten dewasa (sumber: StevenBlack/hosts, MIT license)
✅ Blokir domain judol Indonesia (daftar kurasi + keyword match)
✅ Sembunyikan iklan judol inline di Detik, Kompas, Tribun, Kaskus, dll lewat content script
✅ Toggle on/off global dari popup
✅ Whitelist per-situs kalau ada halaman yang salah keblokir
✅ Stats counter — badge per-tab + total seumur hidup
✅ Halaman Options lengkap untuk atur whitelist dan kategori

PRIVASI
✅ Tidak ada tracking, tidak ada analytics, tidak ada remote call
✅ Filter list dibundel saat build, bukan di-fetch runtime
✅ Settings disimpan lokal via chrome.storage.sync (cuma sync antar Chrome profile kamu sendiri)
✅ Tidak ada server kami — ekstensi ini tidak pernah "nelpon pulang"

OPEN SOURCE
Source code 100% terbuka, MIT license. Baca setiap baris sebelum install.
GitHub: PLACEHOLDER_GITHUB_URL

---

English summary: Blocks Indonesian online gambling (judol) ads and ~30k adult content domains via Chrome's declarativeNetRequest API plus a DOM content script for inline ad removal. No tracking, no remote calls, MIT licensed. Free forever.

Install sekarang dan bebas dari gangguan iklan judol!
```

**Word count (approx): ~280 words, ~1,750 characters** (within the ~1000-1500 char target; slightly over because the feature list is detailed — trim if CWS rejects length)

---

## 4. Category

**Productivity**

(CWS category dropdown — "Productivity" is the closest fit. Alternatives considered: "Accessibility" — no, this isn't an a11y tool. "Social & Communication" — no.)

---

## 5. Language

- **Primary**: Indonesian (`id`)
- **Secondary**: English (`en`)

Set the developer console "Default language" to Indonesian. The manifest currently has `"default_locale": "en"` — leave as-is since the UI strings are in English; only the store listing copy is Indonesian primary.

---

## 6. Screenshots required (1280x800 PNG)

Chrome Web Store requires at least 1 screenshot, up to 5. Capture these after sideloading the extension:

- [ ] **TODO** — Popup open on a Detik article, showing toggle ON, badge count ≥ 1, and current site whitelist button
- [ ] **TODO** — Options page showing whitelist list, category toggles (adult / judol), and lifetime stats
- [ ] **TODO** — "Before/after" split showing a blocked judol banner on Kompas or Tribun (before = judol banner visible, after = clean layout)
- [ ] **TODO** — Stats visible: popup with badge count > 10 on a heavily-ad-laden site
- [ ] **TODO** *(optional)* — Right-click context menu showing the "Options" entry

**Capture workflow**: sideload via `chrome://extensions` → Developer mode → Load unpacked → navigate to test sites in TEST-RESULTS.md → screenshot via Cmd+Shift+4 on macOS → resize/pad to exactly 1280x800 PNG.

---

## 7. Promo tile requirements

- **Small promo tile**: 440x280 PNG — **required**
- **Large promo tile**: 920x680 PNG — optional
- **Marquee**: 1400x560 PNG — optional (only shown if featured)

- [ ] **TODO** — Create 440x280 promo tile. Placeholder design: solid red `#c62641` background, white text "Judol & Adult Blocker" in Josefin Sans Bold, subtitle "Bebas iklan judol & konten dewasa" in Domine. Ship this as v1 and upgrade later.

---

## 8. Privacy policy

CWS requires a hosted privacy policy URL for extensions with broad host permissions (`<all_urls>`). Draft below — host this on a public URL before submission.

**Suggested hosting URL**: `https://jrdevhub.com/privacy-judol-blocker` *(PLACEHOLDER — create page first)*

### Draft privacy policy (host this text)

```
Privacy Policy — Judol & Adult Blocker
Last updated: 2026-04-11

Judol & Adult Blocker ("the extension") is a Chrome extension that blocks Indonesian online gambling ads and adult content. This policy explains what data the extension handles.

1. DATA COLLECTION
The extension does NOT collect any personal data. It does not track browsing history, clicks, search queries, or any user activity. There is no user account, no login, and no telemetry.

2. REMOTE CALLS
The extension does NOT make any network requests to any remote server at runtime. All filter lists are bundled into the extension at build time and shipped with the installed package. The extension never "phones home".

3. LOCAL STORAGE
The extension stores the following settings locally using Chrome's `chrome.storage.sync` API:
- Global on/off toggle state
- User-defined whitelist (list of sites where blocking is disabled)
- Category toggles (adult content, judol)
- Aggregate stats counter (total blocked count, per-tab badge counter)

`chrome.storage.sync` is a Chrome-native sync mechanism. If you are signed into Chrome and have sync enabled, these settings will sync across your own Chrome profiles via Google's infrastructure. The extension developers never receive or access this data.

4. PERMISSIONS
The extension requests the following Chrome permissions:
- `storage` — to persist user settings and stats locally
- `declarativeNetRequest` — to block network requests to blocked domains at the browser level
- `declarativeNetRequestFeedback` — to count matched blocking rules for the stats counter
- `tabs` — to read the active tab's hostname for per-site whitelist logic
- `activeTab` — to apply per-tab actions from the popup
- `<all_urls>` host permission — so the content script can hide inline ads on every website the user visits

None of these permissions are used to collect or transmit user data.

5. THIRD-PARTY DATA
The extension bundles two filter lists:
- Adult domain list: sourced from StevenBlack/hosts (porn-only variant), MIT license
- Judol domain list: custom curated list maintained by the extension authors
These lists are embedded at build time and never fetched live.

6. CHILDREN'S PRIVACY
The extension is intended for adult users who want to block unwanted content. It does not knowingly collect data from anyone, including children.

7. CHANGES TO THIS POLICY
If this policy changes, the updated version will be published at the same URL with a new "Last updated" date.

8. CONTACT
For questions about this policy, open an issue on the GitHub repository: PLACEHOLDER_GITHUB_URL
```

---

## 9. Permissions justification (mandatory for CWS review)

Paste each justification into the corresponding field in the CWS developer console "Privacy practices" tab.

### `storage`
```
Used to persist user settings (global on/off toggle, per-site whitelist, category flags for adult/judol, and aggregate blocked-count stats) via chrome.storage.sync. No remote storage; data stays in the user's Chrome profile.
```

### `declarativeNetRequest`
```
Core blocking functionality. The extension ships two bundled rulesets — ~30,000 adult domains and a curated judol (Indonesian online gambling) domain list — and registers them declaratively so Chrome blocks requests to those domains at the network layer with zero per-request JavaScript overhead. This is the primary mechanism the extension uses to do its job.
```

### `declarativeNetRequestFeedback`
```
Used to surface the count of matched blocking rules so the popup and badge can display how many requests have been blocked on the current tab and in total. This permission only provides read-only feedback about rules the extension itself registered — it does not grant access to any broader browsing data. (Note: this permission may be removed in a future version if the stats counter is rewired to use message-passing from the content script alone.)
```

### `tabs`
```
Used to (a) reset the per-tab badge counter when the user navigates to a new page, and (b) reload the active tab after the user whitelists or un-whitelists it from the popup, so the change takes effect immediately. The extension only reads the active tab's URL for whitelist matching; it does not read tab titles, history, or content.
```

### `activeTab`
```
Used by the popup to read the current tab's hostname so it can display per-site stats and offer a "whitelist this site" button. Scoped to the active tab only, per Chrome's activeTab semantics — the extension has no access to other tabs via this permission.
```

### `host_permissions: <all_urls>`
```
Required so the content script can run on every website the user visits. This is necessary because inline judol ads are injected by Indonesian news sites from first-party domains that cannot be blocked at the network level without breaking the host site. The content script scans the DOM for judol keywords and hides matching elements via CSS. No page content is read, transmitted, or stored beyond what is needed for local in-page ad hiding.
```

---

## 10. Submission checklist

Run top-to-bottom in order. Most steps are manual and cannot be automated.

- [ ] Create Chrome Web Store developer account at `https://chrome.google.com/webstore/devconsole/` (pay $5 one-time registration fee)
- [ ] Host the privacy policy draft (section 8 above) at a public URL — suggested: `https://jrdevhub.com/privacy-judol-blocker`
- [ ] Capture 4-5 screenshots at exactly 1280x800 PNG (see section 6 for the list)
- [ ] Create the 440x280 PNG promo tile (see section 7)
- [ ] Push the extension source to a public GitHub repo and update all `PLACEHOLDER_GITHUB_URL` references in this doc and in the hosted privacy policy
- [ ] Go to the developer console → "New item" → upload `chrome-adblocker-judol-v1.0.zip`
- [ ] Paste the title from section 1
- [ ] Paste the summary from section 2
- [ ] Paste the detailed description from section 3
- [ ] Select category **Productivity** (section 4)
- [ ] Set default language to **Indonesian** (section 5)
- [ ] Upload screenshots (section 6)
- [ ] Upload promo tile (section 7)
- [ ] Paste privacy policy URL (section 8)
- [ ] Paste each permissions justification from section 9 into the "Privacy practices" tab
- [ ] Check "Single purpose" declaration: "Block online gambling (judol) and adult content across websites"
- [ ] Submit for review — typical turnaround 1-3 business days, sometimes up to 7

---

## 11. Post-launch

### Monitoring
- Watch the developer console "Item status" page daily for the first week
- If the review rejects, read the rejection reason carefully — most common issues are permissions justification wording, missing privacy policy, or screenshots that don't match the extension's actual UI
- Respond to rejections by fixing the issue and resubmitting; the review clock restarts

### Promotion
- Tweet the launch from @luffyselah (Profile 10) with CWS install link, screenshots, and a short demo GIF — MAX 277 chars per tweet
- Write a launch blog post at jrdevhub.com: "How I blocked judol ads on every Indonesian website with one Chrome extension"
- Cross-post the blog article to Medium and dev.to
- Link from existing jrdevhub.com articles about "how to block judol" or "cara blokir iklan judi online"
- Post to r/indonesia, r/chrome_extensions subreddits with a plain "I built this, open source, no tracking" intro
- Post to Kaskus forum thread about adblockers if one exists

### Future monetization (from plan Task 13)
Consider a paid Gumroad upgrade ($5-9) with advanced features:
- Custom rules editor (add your own domains/keywords)
- Cloud sync via a user-provided Gist (not our server)
- Detailed stats dashboard (blocked per category per day)
- Preset profiles (strict / balanced / permissive)

Keep the base CWS version 100% free forever — the paid upgrade is a sideload-only companion. This preserves the "free, open source, no tracking" trust story on the store listing while creating a monetization path.

### Metrics to track
- CWS install count (public on listing page)
- CWS rating + reviews (respond to every review in Indonesian)
- Weekly active users (developer console → Statistics tab)
- GitHub stars + issues
- Blog post traffic from jrdevhub.com referrers
