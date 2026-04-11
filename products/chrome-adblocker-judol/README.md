# Judol & Adult Blocker

A Chrome extension that blocks Indonesian online gambling (judol) ads and adult content across the web.

## What It Does

Indonesian news sites, forums, and free-content portals are flooded with "judol" (judi online / online gambling) banners, popups, and inline ad injections — plus the usual wave of adult content. This extension silences both at two layers: network-level domain blocking via Chrome's `declarativeNetRequest` API, and DOM-level keyword scanning that hides inline judol ads which slip past the domain blocklist. Install it once and browsing Detik, Kompas, Tribun, Kaskus, and the rest of the Indonesian web stops looking like a casino lobby.

## Features

- Blocks ~30,000 adult content domains (from the StevenBlack hosts list, porn-only variant)
- Blocks Indonesian judol (gambling) domains — 85 curated entries plus more via keyword match
- Hides inline judol ads on any site (e.g., Detik, Kompas, Tribun) via DOM keyword scanning
- Toggle on/off globally, or whitelist individual sites
- Stats counter: per-tab badge count and all-time blocked total
- No tracking, no remote calls, no analytics
- Pure JavaScript, no frameworks, no build step (except rule regeneration)

## Installation — Developer Mode (Sideload)

1. Clone this repo, or download it as a ZIP and extract it.
2. Open Chrome and go to `chrome://extensions`.
3. Toggle **Developer mode** on (top right corner).
4. Click **Load unpacked**.
5. Select the `products/chrome-adblocker-judol/` folder.
6. The red shield icon should appear in your Chrome toolbar. Pin it if it's hidden under the puzzle-piece menu.

## Installation — Chrome Web Store

Not yet published. Use the developer-mode steps above for now.

## Usage

- **Click the toolbar icon** to open the popup. From here you can toggle the blocker on/off, see how many things were blocked on the current tab, and whitelist the current site.
- **Right-click the icon → Options** (or click the "Settings" link inside the popup) to open the full options page: manage the whitelist, toggle individual categories (adult / judol), and view or reset lifetime stats.
- **If a site you need is being blocked**, add it to the whitelist from the popup or the options page.

## How It Works (Architecture)

This is a Manifest V3 extension with two independent blocking layers:

- **`declarativeNetRequest` (DNR)** handles network-level domain blocking. Rules are compiled at build time from the source filter lists into `rules/*.json` and registered declaratively — Chrome evaluates them natively, so there is zero per-request JavaScript overhead.
- **Content script** runs on every page at `document_idle` and scans the DOM for inline judol ads using a keyword list. Anything matching gets hidden via CSS. This catches ads served from first-party domains that DNR can't block without breaking the host site.

A service worker tracks per-tab badge counts via messages from the content script, and persists user settings (toggle state, whitelist, category flags) in `chrome.storage.sync`.

### Permissions

| Permission | Why |
|---|---|
| `storage` | Save toggle state, whitelist, and stats |
| `declarativeNetRequest` | Register the bundled blocking rulesets |
| `declarativeNetRequestFeedback` | Count matched rules for the stats counter |
| `tabs` | Read the active tab's URL for per-site whitelist and badge updates |
| `activeTab` | Apply per-tab actions from the popup |
| `<all_urls>` host permission | Run the content script on every site so inline ads can be hidden anywhere |

## Filter Lists & Credits

- **Adult domains** — [`StevenBlack/hosts`](https://github.com/StevenBlack/hosts), MIT license. We use the *porn-only* variant and truncate to the first 30,000 domains to stay under Chrome's DNR per-ruleset limit. All credit for the adult domain list goes to Steven Black and the contributors to that project.
- **Judol domains** — custom curated list at `data/judol-domains.txt` (~85 domains), plus ~30 Indonesian gambling keyword phrases at `data/judol-keywords.txt` used by the DOM scanner.

## Updating the Rules

If the upstream source list changes, or you want to refresh the adult list:

```bash
cd products/chrome-adblocker-judol
curl -fsSL https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn-only/hosts -o data/adult-hosts-source.txt
npm run build:rules
```

Then go back to `chrome://extensions` and click the reload icon on the extension card.

## Privacy

- **No telemetry, no analytics, no remote calls at runtime.** The extension never talks to any server.
- **Filter lists are bundled at build time**, not fetched live. What you install is what runs.
- **Settings stored in `chrome.storage.sync`** — this means they sync across your own Chrome profiles if you're signed into Chrome, but they never leave Google's sync infrastructure and never reach us.
- **Source code: 100% open.** Read every line before you load it.

## Known Limitations

- The adult domain ruleset is truncated to 30,000 rules due to Chrome's DNR per-ruleset cap. A future release may split it across multiple rulesets to raise that ceiling.
- The content script's keyword list is duplicated inline because content scripts can't ES-import modules. Updating the list means editing two files.
- The badge count can reset when Chrome unloads the ephemeral service worker between tabs — lifetime stats in `chrome.storage.sync` are authoritative.
- The judol domain list is manually curated, so newer sites will slip through until the list is updated. The DOM keyword scanner is the backup for that.

## Development

```bash
cd products/chrome-adblocker-judol
npm test               # run unit tests (storage, keywords)
npm run build:rules    # regenerate rules/*.json from data/ source files
```

For manual end-to-end testing against live sites, see [`TEST-RESULTS.md`](./TEST-RESULTS.md).

## License

MIT License

Copyright (c) 2026 Judol & Adult Blocker contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
