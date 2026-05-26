# Chrome Ad Blocker (Judol + Adult) Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Chrome extension (Manifest V3) that blocks Indonesian online gambling (judol) ads and adult content across the web using declarative network request rules and a keyword-based DOM hider.

**Architecture:** Manifest V3 extension using `declarativeNetRequest` for fast network-level domain blocking, a content script for keyword-based DOM element hiding, a service worker for badge counting and whitelist logic, plus vanilla JS popup and options pages for user control. Settings persisted via `chrome.storage.sync`. No build step, no frameworks — pure HTML/CSS/JS for simplicity.

**Tech Stack:**
- Manifest V3 Chrome Extension API
- `chrome.declarativeNetRequest` (DNR) for request blocking
- `chrome.storage.sync` for settings
- Vanilla JavaScript (ES modules)
- HTML + CSS for popup/options UI
- Node.js (one-off build script for converting hosts lists → DNR JSON)

**Target browsers:** Chrome 120+, Edge 120+ (Chromium-based)

**Distribution:** Chrome Web Store (developer fee $5 one-time) + optional direct ZIP for sideload

**Project location:** `products/chrome-adblocker-judol/`

---

## Background: How Chrome Extension Ad Blockers Work

For context before implementing:

1. **Manifest V3** is the current extension standard. It deprecates `webRequest` blocking in favor of `declarativeNetRequest` (DNR) — you pre-register rules that Chrome enforces natively. Faster, safer, but less flexible than the old API.

2. **Two-layer blocking strategy:**
   - **Network layer (DNR):** Intercepts outgoing HTTP requests, blocks by URL/domain pattern. Used for known judol/adult domain lists. Runs before the request hits the network — fastest and most reliable.
   - **DOM layer (content script):** Scans loaded pages for judol keywords (gacor, maxwin, slot88, rtp live, etc.) and hides matching elements. Catches content not blocked at network layer, like inline native ads.

3. **DNR rules file format** (simplified):
   ```json
   {
     "id": 1,
     "priority": 1,
     "action": { "type": "block" },
     "condition": {
       "urlFilter": "||slot88.com^",
       "resourceTypes": ["main_frame", "sub_frame", "script", "image"]
     }
   }
   ```
   Uses Adblock Plus-style URL filters.

4. **Whitelist logic:** When user whitelists a domain, we dynamically add an `allowAllRequests` rule for that domain that overrides the block rules (priority-based). Content script also checks whitelist before hiding elements.

5. **Badge counter:** Service worker listens for blocked requests via `chrome.declarativeNetRequest.onRuleMatchedDebug` (in dev mode) or tracks content script hide events via `runtime.sendMessage`, increments counter per tab, displays on extension icon.

---

## Filter List Strategy

- **Adult content:** Download `StevenBlack/hosts` (porn variant) from GitHub raw, convert to DNR JSON once per release. License: MIT, redistribution allowed.
  - Source: `https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn-only/hosts`
  - Contains ~50K domains.

- **Judol (Indonesian gambling):** Curated manually — no good public list exists. Start with ~100 popular domains seen in Indonesian web (slot88, gacor77, maxwin138, etc.) plus patterns like `*slot*`, `*gacor*`, `*rtp*` as fallback.

- **Judol keyword list** (for content script DOM hiding): Indonesian gambling slang — `slot gacor`, `rtp live`, `maxwin`, `jackpot`, `judi online`, `casino online`, `bandar togel`, `situs slot`, `daftar slot`, `bonus new member`, etc. ~50 keywords.

- **Update strategy:** Bundled with extension. Future enhancement (not in MVP): fetch updates from remote URL on extension startup.

---

## Project Folder Structure

```
products/chrome-adblocker-judol/
├── manifest.json                       # Extension manifest (MV3)
├── README.md                           # User-facing docs
├── icons/
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
├── src/
│   ├── background/
│   │   └── service-worker.js           # Badge counter, message router
│   ├── content/
│   │   └── content-script.js           # DOM keyword hider
│   ├── popup/
│   │   ├── popup.html
│   │   ├── popup.css
│   │   └── popup.js
│   ├── options/
│   │   ├── options.html
│   │   ├── options.css
│   │   └── options.js
│   └── utils/
│       ├── storage.js                  # chrome.storage wrapper
│       └── keywords.js                 # Judol keyword list (exported)
├── rules/
│   ├── judol-domains.json              # DNR rules for judol domains
│   └── adult-domains.json              # DNR rules for adult domains
├── data/
│   ├── judol-domains.txt               # Source list (human-editable)
│   └── adult-hosts-source.txt          # Downloaded from StevenBlack
├── scripts/
│   └── build-rules.js                  # Node script: hosts → DNR JSON
├── tests/
│   ├── storage.test.js                 # Unit test for storage wrapper
│   └── keywords.test.js                # Unit test for keyword matcher
└── package.json                        # Just for test runner (no bundler)
```

---

## Task List

### Task 1: Project scaffold and manifest

**Files:**
- Create: `products/chrome-adblocker-judol/manifest.json`
- Create: `products/chrome-adblocker-judol/README.md`

**Step 1: Create folder structure**

```bash
cd products
mkdir -p chrome-adblocker-judol/{src/{background,content,popup,options,utils},rules,data,icons,scripts,tests}
```

**Step 2: Write `manifest.json`**

```json
{
  "manifest_version": 3,
  "name": "Judol & Adult Blocker",
  "version": "1.0.0",
  "description": "Block Indonesian online gambling (judol) ads and adult content across the web.",
  "default_locale": "en",
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  },
  "action": {
    "default_popup": "src/popup/popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "background": {
    "service_worker": "src/background/service-worker.js",
    "type": "module"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["src/content/content-script.js"],
      "run_at": "document_idle"
    }
  ],
  "options_page": "src/options/options.html",
  "permissions": [
    "storage",
    "declarativeNetRequest",
    "declarativeNetRequestFeedback",
    "tabs",
    "activeTab"
  ],
  "host_permissions": ["<all_urls>"],
  "declarative_net_request": {
    "rule_resources": [
      {
        "id": "judol",
        "enabled": true,
        "path": "rules/judol-domains.json"
      },
      {
        "id": "adult",
        "enabled": true,
        "path": "rules/adult-domains.json"
      }
    ]
  }
}
```

**Step 3: Write minimal placeholder files so manifest loads**

Create empty files:
- `src/background/service-worker.js` (with `console.log("sw loaded")`)
- `src/content/content-script.js` (empty)
- `src/popup/popup.html` (minimal `<html><body>Popup</body></html>`)
- `src/options/options.html` (minimal `<html><body>Options</body></html>`)
- `rules/judol-domains.json` (empty array: `[]`)
- `rules/adult-domains.json` (empty array: `[]`)

**Step 4: Create placeholder icons**

Use a quick script to generate solid-color PNGs:

```bash
# From products/chrome-adblocker-judol/
python3 -c "
from PIL import Image
for size in [16, 48, 128]:
    img = Image.new('RGB', (size, size), '#c62641')
    img.save(f'icons/icon{size}.png')
"
```

If PIL not installed: `pip install Pillow`

**Step 5: Load unpacked in Chrome to verify**

1. Open Chrome (Profile 10): `open -na "Google Chrome" --args --profile-directory="Profile 10" "chrome://extensions"`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked" → select `products/chrome-adblocker-judol/`
4. Extension should appear with red icon, no errors

Expected: No manifest errors. If errors, fix before commit.

**Step 6: Commit**

```bash
git add products/chrome-adblocker-judol/
git commit -m "feat(chrome-adblocker): scaffold MV3 extension project structure"
```

---

### Task 2: Judol domain list + DNR rules

**Files:**
- Create: `products/chrome-adblocker-judol/data/judol-domains.txt`
- Create: `products/chrome-adblocker-judol/rules/judol-domains.json`

**Step 1: Write `data/judol-domains.txt`**

One domain per line, comments with `#`. Include known Indonesian judol sites. Start with this seed list:

```
# Popular Indonesian judol domains (as of 2026)
slot88.com
slotgacor77.com
maxwin138.com
gacor77.net
slot138.com
rtplive.net
situsjudi.com
bandartogel303.com
slotbonus.com
judionline88.com
slotdemo.net
daftarslot.com
# Pattern-based catch (common substrings — handled via urlFilter)
```

Add 50-100 domains based on common Indonesian judol slang.

**Step 2: Write `rules/judol-domains.json`**

Generate DNR rules array. Each entry:

```json
[
  {
    "id": 1,
    "priority": 1,
    "action": { "type": "block" },
    "condition": {
      "urlFilter": "||slot88.com^",
      "resourceTypes": ["main_frame", "sub_frame", "script", "image", "xmlhttprequest"]
    }
  },
  {
    "id": 2,
    "priority": 1,
    "action": { "type": "block" },
    "condition": {
      "urlFilter": "||slotgacor77.com^",
      "resourceTypes": ["main_frame", "sub_frame", "script", "image", "xmlhttprequest"]
    }
  }
]
```

Rule ID must be unique integer. Use sequential IDs 1-999 for judol block rules.

**Step 3: Reload extension in Chrome**

Go to `chrome://extensions`, click refresh icon on the extension card. Check for "declarative_net_request rules failed to load" errors.

**Step 4: Manual test**

1. Open a test URL in new tab: `https://slot88.com`
2. Expected: Page fails to load (blocked). Chrome shows "This site can't be reached" or `ERR_BLOCKED_BY_CLIENT`.
3. Check `chrome://extensions/?id=<ext-id>` → Service Worker → Logs → look for rule match debug info.

**Step 5: Commit**

```bash
git add data/judol-domains.txt rules/judol-domains.json
git commit -m "feat(chrome-adblocker): add judol domain blocklist and DNR rules"
```

---

### Task 3: Build script — StevenBlack hosts → DNR JSON (adult list)

**Files:**
- Create: `products/chrome-adblocker-judol/scripts/build-rules.js`
- Create: `products/chrome-adblocker-judol/package.json`
- Create: `products/chrome-adblocker-judol/data/adult-hosts-source.txt`
- Create: `products/chrome-adblocker-judol/rules/adult-domains.json` (generated)

**Step 1: Download StevenBlack adult hosts list**

```bash
cd products/chrome-adblocker-judol
curl -fsSL https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn-only/hosts -o data/adult-hosts-source.txt
```

Verify file size: `wc -l data/adult-hosts-source.txt` → expect 50K+ lines.

**Step 2: Write `package.json` (minimal — for running scripts)**

```json
{
  "name": "chrome-adblocker-judol",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "build:rules": "node scripts/build-rules.js",
    "test": "node --test tests/"
  }
}
```

**Step 3: Write `scripts/build-rules.js`**

```javascript
// Converts hosts-format file to Chrome DNR rules JSON.
// Usage: node scripts/build-rules.js

import { readFileSync, writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');

function parseHostsFile(content) {
  const domains = [];
  for (const line of content.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const match = trimmed.match(/^(?:0\.0\.0\.0|127\.0\.0\.1)\s+([\w.-]+)/);
    if (match && match[1] !== 'localhost' && match[1] !== '0.0.0.0') {
      domains.push(match[1]);
    }
  }
  return [...new Set(domains)];
}

function domainsToRules(domains, startId) {
  return domains.map((domain, i) => ({
    id: startId + i,
    priority: 1,
    action: { type: 'block' },
    condition: {
      urlFilter: `||${domain}^`,
      resourceTypes: ['main_frame', 'sub_frame', 'script', 'image', 'xmlhttprequest'],
    },
  }));
}

function buildAdultRules() {
  const source = readFileSync(resolve(root, 'data/adult-hosts-source.txt'), 'utf8');
  const domains = parseHostsFile(source);
  // DNR safe rule ID starts at 1000 for adult (judol uses 1-999)
  const rules = domainsToRules(domains, 1000);
  writeFileSync(
    resolve(root, 'rules/adult-domains.json'),
    JSON.stringify(rules, null, 2)
  );
  console.log(`Built ${rules.length} adult block rules`);
}

function buildJudolRules() {
  const source = readFileSync(resolve(root, 'data/judol-domains.txt'), 'utf8');
  const domains = source
    .split('\n')
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith('#'));
  const rules = domainsToRules(domains, 1);
  writeFileSync(
    resolve(root, 'rules/judol-domains.json'),
    JSON.stringify(rules, null, 2)
  );
  console.log(`Built ${rules.length} judol block rules`);
}

buildJudolRules();
buildAdultRules();
```

**Step 4: Run build script**

```bash
cd products/chrome-adblocker-judol
npm run build:rules
```

Expected output:
```
Built 60 judol block rules
Built 53421 adult block rules
```

**Note:** Chrome DNR has a **static rule limit of 30,000 per ruleset** (can be raised to 330K with `declarativeNetRequest.MAX_NUMBER_OF_STATIC_RULES` in manifest). If adult list exceeds 30K, either (a) truncate to top 30K or (b) split into multiple rulesets. For MVP: truncate to first 30,000.

Update `build-rules.js` `buildAdultRules` to slice:
```javascript
const rules = domainsToRules(domains, 1000).slice(0, 30000);
```

**Step 5: Reload extension and verify**

Chrome extensions page → reload. Check Service Worker logs for "Declarative Net Request: X rules loaded".

**Step 6: Manual test**

Open a known adult domain from the list (pick one from `data/adult-hosts-source.txt`) — expect block.

**Step 7: Commit**

```bash
git add scripts/build-rules.js package.json data/adult-hosts-source.txt rules/adult-domains.json
git commit -m "feat(chrome-adblocker): add StevenBlack adult list + rules build script"
```

---

### Task 4: Storage utility + unit test

**Files:**
- Create: `products/chrome-adblocker-judol/src/utils/storage.js`
- Create: `products/chrome-adblocker-judol/tests/storage.test.js`

**Step 1: Write failing test `tests/storage.test.js`**

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { getDefaultSettings, mergeSettings } from '../src/utils/storage.js';

test('getDefaultSettings returns expected shape', () => {
  const defaults = getDefaultSettings();
  assert.equal(defaults.enabled, true);
  assert.equal(defaults.blockJudol, true);
  assert.equal(defaults.blockAdult, true);
  assert.deepEqual(defaults.whitelist, []);
  assert.equal(defaults.stats.blocked, 0);
});

test('mergeSettings preserves user overrides and fills missing defaults', () => {
  const stored = { enabled: false, whitelist: ['example.com'] };
  const merged = mergeSettings(stored);
  assert.equal(merged.enabled, false);
  assert.deepEqual(merged.whitelist, ['example.com']);
  assert.equal(merged.blockJudol, true); // default filled
});
```

**Step 2: Run test, verify it fails**

```bash
npm test
```

Expected: FAIL with "Cannot find module storage.js" or similar.

**Step 3: Implement `src/utils/storage.js`**

```javascript
// chrome.storage.sync wrapper with defaults and pure helpers.

export function getDefaultSettings() {
  return {
    enabled: true,
    blockJudol: true,
    blockAdult: true,
    whitelist: [],
    stats: { blocked: 0 },
  };
}

export function mergeSettings(stored) {
  return { ...getDefaultSettings(), ...(stored || {}) };
}

// Runtime-only (not unit tested — requires chrome API):
export async function loadSettings() {
  const stored = await chrome.storage.sync.get('settings');
  return mergeSettings(stored.settings);
}

export async function saveSettings(settings) {
  await chrome.storage.sync.set({ settings });
}

export async function addToWhitelist(domain) {
  const settings = await loadSettings();
  if (!settings.whitelist.includes(domain)) {
    settings.whitelist.push(domain);
    await saveSettings(settings);
  }
}

export async function removeFromWhitelist(domain) {
  const settings = await loadSettings();
  settings.whitelist = settings.whitelist.filter((d) => d !== domain);
  await saveSettings(settings);
}

export async function incrementBlockedCount(n = 1) {
  const settings = await loadSettings();
  settings.stats.blocked += n;
  await saveSettings(settings);
}
```

**Step 4: Run tests, verify pass**

```bash
npm test
```

Expected: PASS (2/2).

**Step 5: Commit**

```bash
git add src/utils/storage.js tests/storage.test.js
git commit -m "feat(chrome-adblocker): add storage utility with defaults + tests"
```

---

### Task 5: Keyword matcher utility + unit test

**Files:**
- Create: `products/chrome-adblocker-judol/src/utils/keywords.js`
- Create: `products/chrome-adblocker-judol/tests/keywords.test.js`

**Step 1: Write failing test `tests/keywords.test.js`**

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { JUDOL_KEYWORDS, containsJudolKeyword } from '../src/utils/keywords.js';

test('JUDOL_KEYWORDS contains common Indonesian gambling terms', () => {
  assert.ok(JUDOL_KEYWORDS.includes('slot gacor'));
  assert.ok(JUDOL_KEYWORDS.includes('maxwin'));
  assert.ok(JUDOL_KEYWORDS.includes('rtp live'));
});

test('containsJudolKeyword matches case-insensitive', () => {
  assert.equal(containsJudolKeyword('Main Slot Gacor sekarang!'), true);
  assert.equal(containsJudolKeyword('MAXWIN JACKPOT'), true);
  assert.equal(containsJudolKeyword('artikel biasa tentang coding'), false);
});

test('containsJudolKeyword handles word boundaries', () => {
  // "slot" alone is ambiguous (car slot, time slot) — require phrase
  assert.equal(containsJudolKeyword('time slot for meeting'), false);
  assert.equal(containsJudolKeyword('slot gacor hari ini'), true);
});
```

**Step 2: Run test, verify fail**

```bash
npm test
```

Expected: FAIL — module not found.

**Step 3: Implement `src/utils/keywords.js`**

```javascript
// Indonesian judol keyword list and matcher.
// Phrases preferred over single words to reduce false positives.

export const JUDOL_KEYWORDS = [
  'slot gacor',
  'slot online',
  'situs slot',
  'daftar slot',
  'slot88',
  'slot138',
  'maxwin',
  'rtp live',
  'rtp slot',
  'jackpot slot',
  'bonus new member',
  'bonus slot',
  'judi online',
  'judi bola',
  'casino online',
  'bandar togel',
  'togel online',
  'bandar slot',
  'agen slot',
  'situs judi',
  'link slot',
  'slot pulsa',
  'slot deposit',
  'gacor hari ini',
  'gacor malam ini',
  'slot terbaru',
  'slot terpercaya',
  'slot resmi',
  'game slot',
  'mesin slot',
];

export function containsJudolKeyword(text) {
  if (!text || typeof text !== 'string') return false;
  const lower = text.toLowerCase();
  return JUDOL_KEYWORDS.some((kw) => lower.includes(kw));
}
```

**Step 4: Run tests, verify pass**

```bash
npm test
```

Expected: PASS (5/5 total including Task 4 tests).

**Step 5: Commit**

```bash
git add src/utils/keywords.js tests/keywords.test.js
git commit -m "feat(chrome-adblocker): add judol keyword matcher utility + tests"
```

---

### Task 6: Service worker — message router + badge counter

**Files:**
- Modify: `products/chrome-adblocker-judol/src/background/service-worker.js`

**Step 1: Write `service-worker.js`**

```javascript
// Service worker: message router, badge counter, whitelist dynamic rules.

import {
  loadSettings,
  saveSettings,
  incrementBlockedCount,
} from '../utils/storage.js';

const blockedCountPerTab = new Map();

// Init on install
chrome.runtime.onInstalled.addListener(async () => {
  const settings = await loadSettings();
  await saveSettings(settings);
  console.log('[adblocker] installed, settings:', settings);
});

// Reset per-tab counter on navigation
chrome.webNavigation?.onBeforeNavigate?.addListener((details) => {
  if (details.frameId === 0) {
    blockedCountPerTab.set(details.tabId, 0);
    updateBadge(details.tabId, 0);
  }
});

// Listen for content script hide events
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === 'CONTENT_HIDDEN') {
    const tabId = sender.tab?.id;
    if (tabId != null) {
      const current = blockedCountPerTab.get(tabId) || 0;
      const next = current + (msg.count || 1);
      blockedCountPerTab.set(tabId, next);
      updateBadge(tabId, next);
      incrementBlockedCount(msg.count || 1).catch(console.error);
    }
  } else if (msg.type === 'GET_TAB_COUNT') {
    const tabId = msg.tabId || sender.tab?.id;
    sendResponse({ count: blockedCountPerTab.get(tabId) || 0 });
    return true; // keep channel open for async response
  } else if (msg.type === 'CHECK_WHITELIST') {
    loadSettings().then((settings) => {
      const hostname = msg.hostname || '';
      const whitelisted = settings.whitelist.some(
        (w) => hostname === w || hostname.endsWith('.' + w)
      );
      sendResponse({ whitelisted, enabled: settings.enabled });
    });
    return true;
  }
});

function updateBadge(tabId, count) {
  chrome.action.setBadgeText({
    tabId,
    text: count > 0 ? String(count) : '',
  });
  chrome.action.setBadgeBackgroundColor({ tabId, color: '#c62641' });
}
```

**Step 2: Reload extension**

`chrome://extensions` → reload. Check Service Worker → inspect → Console for "[adblocker] installed" log.

**Step 3: Verify no errors**

If Service Worker inspector shows errors (import errors, API errors), fix before commit. ES module imports require `"type": "module"` in manifest background declaration (already set).

**Step 4: Commit**

```bash
git add src/background/service-worker.js
git commit -m "feat(chrome-adblocker): service worker with badge counter and message router"
```

---

### Task 7: Content script — DOM keyword hider

**Files:**
- Modify: `products/chrome-adblocker-judol/src/content/content-script.js`

**Note:** Content scripts can't directly import ES modules. We duplicate the keyword list here or bundle at build time. For simplicity (no build step), duplicate the list inline.

**Step 1: Write `content-script.js`**

```javascript
// Content script: scan DOM for judol keywords and hide matching elements.
// Runs at document_idle (after initial load).

const JUDOL_KEYWORDS = [
  'slot gacor', 'slot online', 'situs slot', 'daftar slot',
  'slot88', 'slot138', 'maxwin', 'rtp live', 'rtp slot',
  'jackpot slot', 'bonus new member', 'bonus slot',
  'judi online', 'judi bola', 'casino online',
  'bandar togel', 'togel online', 'bandar slot',
  'agen slot', 'situs judi', 'link slot', 'slot pulsa',
  'slot deposit', 'gacor hari ini', 'gacor malam ini',
  'slot terbaru', 'slot terpercaya', 'slot resmi',
  'game slot', 'mesin slot',
];

function containsJudol(text) {
  if (!text) return false;
  const lower = text.toLowerCase();
  return JUDOL_KEYWORDS.some((kw) => lower.includes(kw));
}

// Selectors likely to contain ad/promo content
const CANDIDATE_SELECTORS = [
  '[class*="ad"]', '[id*="ad"]',
  '[class*="banner"]', '[id*="banner"]',
  '[class*="promo"]', '[id*="promo"]',
  'aside', '.sidebar',
  'iframe',
  'a[href]',
];

let hiddenCount = 0;

async function checkWhitelistAndRun() {
  const hostname = window.location.hostname;
  const response = await chrome.runtime.sendMessage({
    type: 'CHECK_WHITELIST',
    hostname,
  });
  if (!response?.enabled) return;
  if (response?.whitelisted) return;
  runScan();
  observeMutations();
}

function runScan() {
  const elements = document.querySelectorAll(CANDIDATE_SELECTORS.join(','));
  for (const el of elements) {
    if (el.dataset.adblockerHidden) continue;
    const text = (el.innerText || el.textContent || '').slice(0, 500);
    const href = el.getAttribute?.('href') || '';
    if (containsJudol(text) || containsJudol(href)) {
      hideElement(el);
    }
  }
  if (hiddenCount > 0) {
    chrome.runtime.sendMessage({ type: 'CONTENT_HIDDEN', count: hiddenCount });
    hiddenCount = 0;
  }
}

function hideElement(el) {
  el.style.setProperty('display', 'none', 'important');
  el.dataset.adblockerHidden = '1';
  hiddenCount += 1;
}

function observeMutations() {
  const observer = new MutationObserver((mutations) => {
    let shouldRescan = false;
    for (const m of mutations) {
      if (m.addedNodes.length > 0) shouldRescan = true;
    }
    if (shouldRescan) {
      clearTimeout(observeMutations.timer);
      observeMutations.timer = setTimeout(runScan, 500);
    }
  });
  observer.observe(document.body, { childList: true, subtree: true });
}

checkWhitelistAndRun().catch(console.error);
```

**Step 2: Reload extension**

**Step 3: Manual test on judol-heavy site**

1. Open `https://www.detik.com` or any Indonesian news site with known judol ads
2. Expected: Elements with "slot gacor", "maxwin", etc. text are hidden
3. Extension badge should show count > 0

**Step 4: Check for false positives**

1. Open a normal site: `https://github.com`
2. Expected: Nothing hidden, badge count stays 0

If false positives (normal content hidden), tighten keyword list or selectors.

**Step 5: Commit**

```bash
git add src/content/content-script.js
git commit -m "feat(chrome-adblocker): content script DOM keyword hider"
```

---

### Task 8: Popup UI — HTML + CSS

**Files:**
- Modify: `products/chrome-adblocker-judol/src/popup/popup.html`
- Create: `products/chrome-adblocker-judol/src/popup/popup.css`

**Step 1: Write `popup.html`**

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Judol & Adult Blocker</title>
    <link rel="stylesheet" href="popup.css" />
  </head>
  <body>
    <header>
      <h1>Blocker</h1>
      <label class="toggle">
        <input type="checkbox" id="enabled-toggle" checked />
        <span class="slider"></span>
      </label>
    </header>

    <section class="stats">
      <div class="stat-card">
        <div class="stat-value" id="tab-count">0</div>
        <div class="stat-label">This tab</div>
      </div>
      <div class="stat-card">
        <div class="stat-value" id="total-count">0</div>
        <div class="stat-label">All time</div>
      </div>
    </section>

    <section class="site-controls">
      <div class="current-site" id="current-site">—</div>
      <button id="whitelist-btn" class="btn">Allow this site</button>
    </section>

    <footer>
      <a href="#" id="options-link">Settings</a>
    </footer>

    <script type="module" src="popup.js"></script>
  </body>
</html>
```

**Step 2: Write `popup.css`**

```css
:root {
  --primary: #c62641;
  --bg: #ffffff;
  --text: #333;
  --muted: #888;
  --border: #eee;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: -apple-system, system-ui, sans-serif;
  width: 300px;
  background: var(--bg);
  color: var(--text);
  padding: 16px;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border);
}

h1 { font-size: 16px; font-weight: 600; }

.toggle { position: relative; display: inline-block; width: 40px; height: 22px; }
.toggle input { opacity: 0; width: 0; height: 0; }
.slider {
  position: absolute; cursor: pointer; inset: 0;
  background: #ccc; border-radius: 22px; transition: 0.3s;
}
.slider::before {
  content: ''; position: absolute;
  height: 18px; width: 18px; left: 2px; bottom: 2px;
  background: white; border-radius: 50%; transition: 0.3s;
}
.toggle input:checked + .slider { background: var(--primary); }
.toggle input:checked + .slider::before { transform: translateX(18px); }

.stats {
  display: flex; gap: 12px; margin: 16px 0;
}
.stat-card {
  flex: 1; text-align: center; padding: 12px;
  background: #f8f8f8; border-radius: 8px;
}
.stat-value { font-size: 24px; font-weight: 700; color: var(--primary); }
.stat-label { font-size: 11px; color: var(--muted); margin-top: 4px; }

.site-controls {
  margin: 16px 0;
  padding: 12px; background: #f8f8f8; border-radius: 8px;
}
.current-site {
  font-size: 12px; color: var(--muted);
  margin-bottom: 8px; word-break: break-all;
}
.btn {
  width: 100%;
  padding: 8px;
  background: var(--primary); color: white;
  border: none; border-radius: 6px;
  cursor: pointer; font-size: 13px;
}
.btn:hover { opacity: 0.9; }
.btn.whitelisted { background: #888; }

footer {
  padding-top: 12px;
  border-top: 1px solid var(--border);
  text-align: center;
}
footer a {
  color: var(--primary); text-decoration: none; font-size: 12px;
}
```

**Step 3: Reload extension and click icon to preview**

Visual check: popup opens, styled correctly, toggle works visually (no logic yet).

**Step 4: Commit**

```bash
git add src/popup/popup.html src/popup/popup.css
git commit -m "feat(chrome-adblocker): popup HTML and CSS"
```

---

### Task 9: Popup logic — wire up JS

**Files:**
- Create: `products/chrome-adblocker-judol/src/popup/popup.js`

**Step 1: Write `popup.js`**

```javascript
import {
  loadSettings,
  saveSettings,
  addToWhitelist,
  removeFromWhitelist,
} from '../utils/storage.js';

const $ = (id) => document.getElementById(id);

async function init() {
  const settings = await loadSettings();
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = tab?.url ? new URL(tab.url) : null;
  const hostname = url?.hostname || '';

  $('enabled-toggle').checked = settings.enabled;
  $('total-count').textContent = settings.stats.blocked.toLocaleString();
  $('current-site').textContent = hostname || 'No active tab';

  // Tab count
  if (tab?.id != null) {
    const resp = await chrome.runtime.sendMessage({
      type: 'GET_TAB_COUNT',
      tabId: tab.id,
    });
    $('tab-count').textContent = resp?.count || 0;
  }

  // Whitelist state
  const whitelisted = settings.whitelist.includes(hostname);
  updateWhitelistButton(whitelisted);

  // Event handlers
  $('enabled-toggle').addEventListener('change', async (e) => {
    const s = await loadSettings();
    s.enabled = e.target.checked;
    await saveSettings(s);
  });

  $('whitelist-btn').addEventListener('click', async () => {
    if (!hostname) return;
    const s = await loadSettings();
    if (s.whitelist.includes(hostname)) {
      await removeFromWhitelist(hostname);
      updateWhitelistButton(false);
    } else {
      await addToWhitelist(hostname);
      updateWhitelistButton(true);
    }
    // Reload tab to apply change
    chrome.tabs.reload(tab.id);
  });

  $('options-link').addEventListener('click', (e) => {
    e.preventDefault();
    chrome.runtime.openOptionsPage();
  });
}

function updateWhitelistButton(whitelisted) {
  const btn = $('whitelist-btn');
  btn.textContent = whitelisted ? 'Remove from whitelist' : 'Allow this site';
  btn.classList.toggle('whitelisted', whitelisted);
}

init().catch(console.error);
```

**Step 2: Reload extension, test popup**

1. Click extension icon
2. Verify toggle reflects saved state
3. Toggle off, close popup, reopen → should still be off
4. Open any site, click popup → hostname should show
5. Click "Allow this site" → button changes to "Remove from whitelist", tab reloads

**Step 3: Commit**

```bash
git add src/popup/popup.js
git commit -m "feat(chrome-adblocker): popup logic with toggle, stats, whitelist"
```

---

### Task 10: Options page — full settings UI

**Files:**
- Modify: `products/chrome-adblocker-judol/src/options/options.html`
- Create: `products/chrome-adblocker-judol/src/options/options.css`
- Create: `products/chrome-adblocker-judol/src/options/options.js`

**Step 1: Write `options.html`**

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Judol & Adult Blocker — Settings</title>
    <link rel="stylesheet" href="options.css" />
  </head>
  <body>
    <main>
      <h1>Judol &amp; Adult Blocker Settings</h1>

      <section>
        <h2>Categories</h2>
        <label><input type="checkbox" id="block-judol" /> Block judol (online gambling)</label>
        <label><input type="checkbox" id="block-adult" /> Block adult content</label>
      </section>

      <section>
        <h2>Whitelist</h2>
        <p class="hint">Domains in this list won't be blocked.</p>
        <div class="whitelist-add">
          <input type="text" id="whitelist-input" placeholder="example.com" />
          <button id="whitelist-add-btn">Add</button>
        </div>
        <ul id="whitelist-list"></ul>
      </section>

      <section>
        <h2>Statistics</h2>
        <div class="stat-row">
          <span>Total blocked all time:</span>
          <strong id="total-blocked">0</strong>
        </div>
        <button id="reset-stats-btn" class="btn-secondary">Reset stats</button>
      </section>

      <footer>
        <p>v1.0.0 — <a href="https://github.com/yourname/chrome-adblocker-judol" target="_blank">GitHub</a></p>
      </footer>
    </main>
    <script type="module" src="options.js"></script>
  </body>
</html>
```

**Step 2: Write `options.css`**

```css
:root {
  --primary: #c62641;
  --bg: #f8f8f8;
  --card: #ffffff;
  --text: #333;
  --muted: #888;
  --border: #e5e5e5;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: -apple-system, system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  padding: 40px 20px;
}

main {
  max-width: 640px;
  margin: 0 auto;
  background: var(--card);
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

h1 { font-size: 24px; margin-bottom: 24px; }
h2 { font-size: 16px; margin-bottom: 12px; color: var(--primary); }

section {
  padding: 20px 0;
  border-bottom: 1px solid var(--border);
}
section:last-of-type { border-bottom: none; }

label {
  display: block;
  padding: 6px 0;
  cursor: pointer;
}

.hint { font-size: 12px; color: var(--muted); margin-bottom: 12px; }

.whitelist-add {
  display: flex; gap: 8px; margin-bottom: 12px;
}
.whitelist-add input {
  flex: 1; padding: 8px;
  border: 1px solid var(--border); border-radius: 6px;
}
.whitelist-add button,
.btn-secondary {
  padding: 8px 16px;
  background: var(--primary); color: white;
  border: none; border-radius: 6px; cursor: pointer;
}
.btn-secondary { background: #888; }

#whitelist-list {
  list-style: none;
}
#whitelist-list li {
  display: flex; justify-content: space-between;
  padding: 8px; background: var(--bg);
  border-radius: 4px; margin-bottom: 4px;
}
#whitelist-list button {
  background: transparent; border: none;
  color: var(--primary); cursor: pointer;
}

.stat-row {
  display: flex; justify-content: space-between;
  padding: 8px 0; margin-bottom: 12px;
}

footer {
  margin-top: 24px;
  text-align: center;
  font-size: 12px;
  color: var(--muted);
}
footer a { color: var(--primary); }
```

**Step 3: Write `options.js`**

```javascript
import {
  loadSettings,
  saveSettings,
  addToWhitelist,
  removeFromWhitelist,
} from '../utils/storage.js';

const $ = (id) => document.getElementById(id);

async function render() {
  const settings = await loadSettings();
  $('block-judol').checked = settings.blockJudol;
  $('block-adult').checked = settings.blockAdult;
  $('total-blocked').textContent = settings.stats.blocked.toLocaleString();

  const list = $('whitelist-list');
  list.innerHTML = '';
  for (const domain of settings.whitelist) {
    const li = document.createElement('li');
    li.innerHTML = `<span>${domain}</span><button data-domain="${domain}">Remove</button>`;
    list.appendChild(li);
  }
}

async function init() {
  await render();

  $('block-judol').addEventListener('change', async (e) => {
    const s = await loadSettings();
    s.blockJudol = e.target.checked;
    await saveSettings(s);
    await updateDNRRuleset('judol', s.blockJudol);
  });

  $('block-adult').addEventListener('change', async (e) => {
    const s = await loadSettings();
    s.blockAdult = e.target.checked;
    await saveSettings(s);
    await updateDNRRuleset('adult', s.blockAdult);
  });

  $('whitelist-add-btn').addEventListener('click', async () => {
    const input = $('whitelist-input');
    const domain = input.value.trim().toLowerCase();
    if (!domain) return;
    await addToWhitelist(domain);
    input.value = '';
    await render();
  });

  $('whitelist-list').addEventListener('click', async (e) => {
    const btn = e.target.closest('button[data-domain]');
    if (!btn) return;
    await removeFromWhitelist(btn.dataset.domain);
    await render();
  });

  $('reset-stats-btn').addEventListener('click', async () => {
    const s = await loadSettings();
    s.stats.blocked = 0;
    await saveSettings(s);
    await render();
  });
}

async function updateDNRRuleset(id, enabled) {
  try {
    if (enabled) {
      await chrome.declarativeNetRequest.updateEnabledRulesets({
        enableRulesetIds: [id],
      });
    } else {
      await chrome.declarativeNetRequest.updateEnabledRulesets({
        disableRulesetIds: [id],
      });
    }
  } catch (e) {
    console.error('Failed to toggle ruleset', id, e);
  }
}

init().catch(console.error);
```

**Step 4: Reload extension, open options**

Right-click extension icon → "Options" OR go to `chrome://extensions` → Details → Extension options.

**Step 5: Manual test**

1. Toggle "Block judol" off → open known judol domain → should load (not blocked)
2. Toggle back on → reload → should block
3. Add domain to whitelist via options → open that domain → should allow
4. Remove from whitelist → should block again
5. Reset stats → counter goes to 0

**Step 6: Commit**

```bash
git add src/options/options.html src/options/options.css src/options/options.js
git commit -m "feat(chrome-adblocker): options page with category toggle, whitelist, stats"
```

---

### Task 11: End-to-end testing checklist

**Files:** None created; this is a manual testing task.

**Test sites:**

| Site | Expected | What to verify |
|---|---|---|
| `https://slot88.com` | Blocked | Network-level block (DNR) |
| `https://www.detik.com` | Loads, some elements hidden | Content script hides judol banners |
| `https://www.kompas.com` | Loads, some elements hidden | Content script hides judol banners |
| `https://github.com` | Loads normally | No false positives |
| `https://stackoverflow.com` | Loads normally | No false positives |
| `https://www.pornhub.com` (from hosts list) | Blocked | Adult list works |

**Test flows:**

1. **Disable globally** → popup toggle off → visit `slot88.com` → should load (blocking disabled)
2. **Whitelist current site** → visit detik.com → click "Allow this site" → page reloads → no elements hidden
3. **Badge counter** → visit detik.com → extension icon should show number > 0
4. **Stats accumulate** → visit 3 different judol-heavy sites → options page "Total blocked" should increase
5. **Category toggle** → options page → uncheck "Block adult" → visit adult domain → should load
6. **Persistence** → change settings → close browser → reopen → settings preserved

**Step 1: Run through entire checklist**

Take screenshots of working states for README.

**Step 2: Log findings**

Create `products/chrome-adblocker-judol/TEST-RESULTS.md` with pass/fail per row. Fix any failures before proceeding.

**Step 3: Commit test results**

```bash
git add TEST-RESULTS.md
git commit -m "test(chrome-adblocker): end-to-end manual test results"
```

---

### Task 12: README + user documentation

**Files:**
- Modify: `products/chrome-adblocker-judol/README.md`

**Step 1: Write `README.md`**

Sections to include:
- **What it does** — one-paragraph pitch
- **Features** — bulleted list
- **Installation (dev mode)** — steps to load unpacked
- **Installation (Chrome Web Store)** — link (add after publishing)
- **Usage** — popup controls, options page
- **How it works** — brief architecture overview
- **Filter lists** — credits to StevenBlack, note judol list is custom
- **Privacy** — no tracking, no remote calls except filter updates (and even those are bundled in MVP)
- **License** — MIT

**Step 2: Take screenshots for README**

Save to `products/chrome-adblocker-judol/docs/screenshots/`:
- `popup.png` — popup open
- `options.png` — options page
- `blocked-site.png` — blocked page example

**Step 3: Commit**

```bash
git add README.md docs/screenshots/
git commit -m "docs(chrome-adblocker): README with installation, usage, screenshots"
```

---

### Task 13: Package for distribution

**Files:**
- Create: `products/chrome-adblocker-judol/chrome-adblocker-judol-v1.0.zip`

**Step 1: Build fresh rules**

```bash
cd products/chrome-adblocker-judol
npm run build:rules
```

**Step 2: Create dist folder without dev files**

```bash
# From products/chrome-adblocker-judol/
zip -r chrome-adblocker-judol-v1.0.zip . \
  -x "*.git*" \
  -x "node_modules/*" \
  -x "tests/*" \
  -x "data/adult-hosts-source.txt" \
  -x "scripts/*" \
  -x "package.json" \
  -x "*.zip" \
  -x "TEST-RESULTS.md" \
  -x "docs/*"
```

Verify ZIP contents:

```bash
unzip -l chrome-adblocker-judol-v1.0.zip
```

Should contain: `manifest.json`, `icons/`, `src/`, `rules/`, `README.md`, `data/judol-domains.txt`. Size should be < 5 MB (mainly the adult rules JSON).

**Step 3: Test ZIP installation**

1. Unzip to temp folder
2. Chrome → extensions → Load unpacked → select temp folder
3. Verify extension loads cleanly

**Step 4: Commit**

```bash
git add chrome-adblocker-judol-v1.0.zip
git commit -m "feat(chrome-adblocker): v1.0 distribution ZIP"
```

---

### Task 14: Chrome Web Store listing prep (optional — do when publishing)

**Files:**
- Create: `products/chrome-adblocker-judol/store-listing.md`

**Step 1: Write store listing copy in `store-listing.md`**

Sections:
- **Title** (max 50 chars): "Judol & Adult Blocker — Indonesia"
- **Summary** (max 132 chars): "Blokir iklan judi online (judol) dan konten dewasa di semua situs. Gratis, ringan, privasi terjaga."
- **Description** (long form, ~1000 chars): pitch + features + privacy note
- **Category**: Productivity
- **Screenshots**: 1280x800 PNG, 3-5 images (from Task 12)
- **Promo tile**: 440x280 PNG

**Step 2: Record promo video (optional)**

30-60 second screen capture: install → browse detik.com → show counter → whitelist → toggle off.

**Step 3: Commit**

```bash
git add store-listing.md
git commit -m "docs(chrome-adblocker): Chrome Web Store listing copy"
```

**Step 4: Submit to Chrome Web Store** (manual, outside Claude)

1. Register developer account at https://chrome.google.com/webstore/devconsole/ ($5 one-time fee)
2. Upload `chrome-adblocker-judol-v1.0.zip`
3. Fill in listing from `store-listing.md`
4. Submit for review (takes 1-3 days typically)

---

## Acceptance Criteria

- [ ] Extension loads in Chrome without errors
- [ ] DNR rules block known judol domains (verified with 3+ test URLs)
- [ ] DNR rules block adult domains from StevenBlack list
- [ ] Content script hides judol-keyword elements on Indonesian news sites
- [ ] Popup shows correct toggle state, tab count, total count
- [ ] Whitelist works per-domain (add from popup, remove from options)
- [ ] Options page toggles categories (judol/adult independently)
- [ ] Settings persist across browser restart
- [ ] No false positives on github.com, stackoverflow.com, dev.to
- [ ] Unit tests pass (`npm test`): storage + keywords
- [ ] ZIP package loads cleanly as unpacked extension
- [ ] README has installation + usage instructions
- [ ] All changes committed with clear messages

---

## Known Limitations (Post-MVP / Future Work)

1. **Judol domain list is manual** — no auto-update. Future: fetch from a GitHub raw URL periodically.
2. **Content script keyword list is duplicated** inline (can't import ES modules). Future: add a minimal build step.
3. **Adult list truncated to 30K** due to DNR static rule limit. Future: split into multiple rulesets (max 100 rulesets, 30K each = 3M rules theoretical max).
4. **No rule update mechanism** — list refresh requires extension update. Future: dynamic rules via `chrome.declarativeNetRequest.updateDynamicRules`.
5. **No telemetry / A/B testing** — deliberate, for privacy.
6. **No i18n for UI** — English only. Future: add Indonesian locale.
7. **No dark mode** for popup/options. Future: `prefers-color-scheme` media query.

---

## Revenue / Distribution Notes

Fits into the passive-income-executor project as:
- **Free Chrome Web Store listing** → build brand + user base
- **Paid upgrade version** on Gumroad ($5-9): advanced features (custom rule editor, cloud sync, stats dashboard)
- **Blog post traffic** on jrdevhub.com: "How I built a judol ad blocker" → affiliate + product CTAs
- **Source code listing** on CodeCanyon ($14-19): full source as a template for other blockers

Positioning: solves a real problem (judol ads are rampant on Indonesian web, very few Indonesian-localized blockers exist). Differentiator = Indonesian keyword focus.
