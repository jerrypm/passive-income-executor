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
