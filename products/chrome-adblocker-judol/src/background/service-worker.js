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
chrome.tabs.onUpdated.addListener((tabId, changeInfo) => {
  if (changeInfo.status === 'loading' && changeInfo.url) {
    blockedCountPerTab.set(tabId, 0);
    updateBadge(tabId, 0);
  }
});

// Clean up when tab closes
chrome.tabs.onRemoved.addListener((tabId) => {
  blockedCountPerTab.delete(tabId);
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
    return false;
  }

  if (msg.type === 'GET_TAB_COUNT') {
    const tabId = msg.tabId ?? sender.tab?.id;
    sendResponse({ count: blockedCountPerTab.get(tabId) || 0 });
    return false;
  }

  if (msg.type === 'CHECK_WHITELIST') {
    loadSettings().then((settings) => {
      const hostname = msg.hostname || '';
      const whitelisted = settings.whitelist.some(
        (w) => hostname === w || hostname.endsWith('.' + w)
      );
      sendResponse({ whitelisted, enabled: settings.enabled });
    });
    return true; // async response
  }

  return false;
});

function updateBadge(tabId, count) {
  chrome.action.setBadgeText({
    tabId,
    text: count > 0 ? String(count) : '',
  });
  chrome.action.setBadgeBackgroundColor({ tabId, color: '#c62641' });
}
