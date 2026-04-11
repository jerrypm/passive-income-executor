// Content script: scan DOM for judol keywords and hide matching elements.
// Runs at document_idle (after initial load).
// NOTE: Cannot import from src/utils/keywords.js — content scripts don't support ES modules.
// The keyword list is duplicated here intentionally; keep in sync with src/utils/keywords.js.

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
  try {
    const response = await chrome.runtime.sendMessage({
      type: 'CHECK_WHITELIST',
      hostname,
    });
    if (!response?.enabled) return;
    if (response?.whitelisted) return;
  } catch (e) {
    // Service worker may be asleep or extension context invalidated; fail safe.
    console.debug('[adblocker] whitelist check failed:', e);
    return;
  }
  runScan();
  observeMutations();
}

function runScan() {
  if (!document.body) return;
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
    try {
      chrome.runtime.sendMessage({ type: 'CONTENT_HIDDEN', count: hiddenCount });
    } catch (_) {
      // extension context may have been invalidated on reload; ignore
    }
    hiddenCount = 0;
  }
}

function hideElement(el) {
  el.style.setProperty('display', 'none', 'important');
  el.dataset.adblockerHidden = '1';
  hiddenCount += 1;
}

function observeMutations() {
  if (!document.body) return;
  const observer = new MutationObserver((mutations) => {
    let shouldRescan = false;
    for (const m of mutations) {
      if (m.addedNodes.length > 0) {
        shouldRescan = true;
        break;
      }
    }
    if (shouldRescan) {
      clearTimeout(observeMutations.timer);
      observeMutations.timer = setTimeout(runScan, 500);
    }
  });
  observer.observe(document.body, { childList: true, subtree: true });
}

checkWhitelistAndRun();
