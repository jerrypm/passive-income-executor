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
