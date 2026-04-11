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
    const span = document.createElement('span');
    span.textContent = domain;
    const btn = document.createElement('button');
    btn.textContent = 'Remove';
    btn.dataset.domain = domain;
    li.appendChild(span);
    li.appendChild(btn);
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
