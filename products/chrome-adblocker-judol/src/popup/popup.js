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
  const url = tab?.url ? safeParseUrl(tab.url) : null;
  const hostname = url?.hostname || '';

  $('enabled-toggle').checked = settings.enabled;
  $('total-count').textContent = settings.stats.blocked.toLocaleString();
  $('current-site').textContent = hostname || 'No active tab';

  // Tab count
  if (tab?.id != null) {
    try {
      const resp = await chrome.runtime.sendMessage({
        type: 'GET_TAB_COUNT',
        tabId: tab.id,
      });
      $('tab-count').textContent = resp?.count || 0;
    } catch (_) {
      $('tab-count').textContent = 0;
    }
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
    if (tab?.id != null) {
      chrome.tabs.reload(tab.id);
    }
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

function safeParseUrl(url) {
  try {
    return new URL(url);
  } catch (_) {
    return null;
  }
}

init().catch(console.error);
