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
