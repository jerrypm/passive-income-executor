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
