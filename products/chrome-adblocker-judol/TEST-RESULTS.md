# Chrome Ad Blocker (Judol) — End-to-End Test Results

This is a manual test checklist for the unpacked Chrome extension. Sideload the build, walk through every section, and mark each checkbox `[x]` as you verify it. Record any failures or surprises in the **Tester notes** section at the bottom.

---

## 1. Installation

1. Open Chrome using **Profile 10 (Jeri / 21zerixpm@gmail.com)** — this is required by the project workflow rules.
   ```bash
   open -na "Google Chrome" --args --profile-directory="Profile 10" "chrome://extensions"
   ```
2. In `chrome://extensions`, enable the **Developer mode** toggle (top-right corner).
3. Click **Load unpacked**.
4. Select the folder: `products/chrome-adblocker-judol/` (the folder containing `manifest.json`).
5. Confirm the extension appears in the list with no red error banner.

- [ ] Extension loaded without errors
- [ ] Using Chrome Profile 10 (Jeri)
- [ ] Extension ID recorded below: `__________________________`

---

## 2. Pre-test setup

- [ ] Extension icon is visible in the Chrome toolbar (pin it if needed)
- [ ] `chrome://extensions` shows **no red error message** for this extension
- [ ] Click **Service Worker** link under the extension card → DevTools opens → **Console tab has no red errors**
- [ ] On first install you should see a log similar to: `[adblocker] installed, settings: {...}`
- [ ] Right-click the extension icon → **Options** → the Options page opens with no errors in its DevTools console
- [ ] Click the extension icon → the **Popup** opens with no errors in its DevTools console

---

## 3. Test site matrix

Visit each site in a fresh tab. Mark PASS/FAIL and add notes if behavior differs from expected.

| # | Site | Expected behavior | What this verifies | Result |
|---|---|---|---|---|
| 1 | `https://slot88.com` | Blocked — page shows `ERR_BLOCKED_BY_CLIENT` or "This site can't be reached" | Network-level DNR block for judol hosts list | [ ] PASS [ ] FAIL |
| 2 | `https://www.detik.com` | Loads normally, but some banner / ad slots are hidden | Content script hides judol-related elements on allowed sites | [ ] PASS [ ] FAIL |
| 3 | `https://www.kompas.com` | Loads normally, but some banner / ad slots are hidden | Content script hides judol-related elements on allowed sites | [ ] PASS [ ] FAIL |
| 4 | `https://github.com` | Loads normally, nothing hidden, no layout breakage | No false positives on clean sites | [ ] PASS [ ] FAIL |
| 5 | `https://stackoverflow.com` | Loads normally, nothing hidden, no layout breakage | No false positives on clean sites | [ ] PASS [ ] FAIL |
| 6 | `https://www.pornhub.com` (or any domain from the first few lines of `data/adult-hosts-source.txt`) | Blocked — page shows `ERR_BLOCKED_BY_CLIENT` | Adult category list is compiled into DNR rules and active | [ ] PASS [ ] FAIL |

**Notes for failed cases:**

```
(write here)
```

---

## 4. User flow checklist

Run through each flow in order. Reset state between flows where it matters (e.g. re-enable toggles).

1. **Global disable via popup**
   - [ ] Open popup → flip the global **Enabled** toggle OFF
   - [ ] Visit `https://slot88.com` → page should now **load** (not blocked)
   - [ ] Re-enable the global toggle → reload → site should be **blocked again**

2. **Whitelist current site via popup**
   - [ ] Visit `https://www.detik.com` → open popup → click **Allow this site** (or equivalent whitelist button)
   - [ ] Reload detik.com → **no elements should be hidden** by the content script
   - [ ] Remove whitelist → reload → hiding resumes

3. **Badge counter on toolbar icon**
   - [ ] Visit `https://www.detik.com`
   - [ ] Confirm the extension icon shows a **numeric badge > 0** (blocked/hidden count for that tab)
   - [ ] Switch tabs → badge updates to reflect the active tab

4. **Stats accumulate over multiple sites**
   - [ ] Open Options page → note current **Total blocked** value: `______`
   - [ ] Visit 3 judol-heavy sites in sequence
   - [ ] Reopen Options → confirm **Total blocked** has **increased**

5. **Category toggle: Block adult**
   - [ ] Options page → uncheck **Block adult**
   - [ ] Visit the adult domain from row 6 in the matrix → site should **load** now (no longer blocked)
   - [ ] Re-check the toggle → reload → site is blocked again

6. **Persistence across Chrome restarts**
   - [ ] Change a setting (e.g. add a whitelist entry or toggle a category)
   - [ ] Fully **quit Chrome** (Cmd+Q, not just close window)
   - [ ] Relaunch Chrome with Profile 10
   - [ ] Open Options → confirm the setting change **persisted**

7. **Popup shows correct hostname for current tab**
   - [ ] Visit `https://www.detik.com` → open popup → popup displays `www.detik.com` (or `detik.com`)
   - [ ] Switch to a `github.com` tab → open popup → popup displays `github.com`

8. **Whitelist removal from Options**
   - [ ] Add `www.detik.com` to whitelist via popup
   - [ ] Options page → whitelist section → **remove** `www.detik.com`
   - [ ] Reload detik.com → content script hiding is active again

9. **Reset stats button**
   - [ ] Options page → click **Reset stats** button
   - [ ] Confirm **Total blocked** counter drops to `0`
   - [ ] Per-category counters (if shown) also reset

---

## 5. Service worker health checks

Open `chrome://extensions` → find this extension → click **Service Worker** → **inspect**.

- [ ] Console shows `[adblocker] installed, settings: {...}` on first install / reload
- [ ] No **red errors** in the console during normal browsing
- [ ] When content scripts report a hit, you may see `console.debug` style messages (optional, not required)
- [ ] Service worker reports as **active** (not "inactive") while you're actively browsing test sites
- [ ] Network tab shows DNR rules being applied (check `chrome://net-export` if deep diagnosis is needed)

---

## 6. Known limitations to verify (not bugs)

Confirm these are present — they are **expected** behavior, not regressions.

- [ ] **Adult list truncated to 30,000 rules.** Chrome's Declarative Net Request has a hard limit on static rule count. When running `npm run build:rules`, a warning like `adult-hosts truncated to 30000 rules` is printed. The rest of the adult list is silently dropped.
- [ ] **Judol keyword list duplicated in content script.** Chrome content scripts cannot use ES module imports, so the keyword array is copy-pasted inline inside `src/content/content-script.js`. Any change to `src/utils/keywords.js` must be mirrored there manually.
- [ ] **Service worker is ephemeral.** Per-tab badge counts may reset to `0` if Chrome unloads the background service worker between user activity. This is by design for MV3. Total stats (stored in `chrome.storage`) are unaffected.

---

## 7. Tester notes

**Freeform notes, observations, surprises, bugs:**

```
(write here)
```

**Environment:**

- Chrome version: `_______________________` (copy from `chrome://version`)
- OS: `_______________________` (e.g. macOS 15.2 on Mac Mini M2)
- Chrome profile: Profile 10 (Jeri / 21zerixpm@gmail.com)
- Date of test: `_______________________`
- Tester: `_______________________`

**Overall verdict:** [ ] SHIP IT   [ ] FIX FIRST   [ ] BLOCKED
