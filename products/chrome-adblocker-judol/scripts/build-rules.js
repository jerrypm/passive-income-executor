import { readFileSync, writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');

const RULE_TEMPLATE = {
  priority: 1,
  action: { type: 'block' },
  resourceTypes: ['main_frame', 'sub_frame', 'script', 'image', 'xmlhttprequest'],
};

// Chrome DNR enforces a 30,000 static rule ceiling per ruleset.
// StevenBlack's porn-only list currently has ~76K domains; anything past
// the first 30K gets dropped alphabetically. For full coverage, split into
// multiple rulesets or set max_number_of_static_rules in manifest.json.
const ADULT_MAX_RULES = 30000;
const JUDOL_ID_START = 1;
const ADULT_ID_START = 100000;

function parseJudolTxt(content) {
  return content
    .split('\n')
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith('#'));
}

function parseHostsFile(content) {
  const domains = [];
  for (const line of content.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const match = trimmed.match(/^(?:0\.0\.0\.0|127\.0\.0\.1)\s+([\w.-]+)/);
    if (match) {
      const domain = match[1];
      if (domain !== 'localhost' && domain !== '0.0.0.0' && domain.includes('.')) {
        domains.push(domain);
      }
    }
  }
  return [...new Set(domains)];
}

function domainsToRules(domains, startId) {
  return domains.map((domain, i) => ({
    id: startId + i,
    priority: RULE_TEMPLATE.priority,
    action: { type: RULE_TEMPLATE.action.type },
    condition: {
      urlFilter: `||${domain}^`,
      resourceTypes: [...RULE_TEMPLATE.resourceTypes],
    },
  }));
}

function buildJudolRules() {
  const src = readFileSync(resolve(root, 'data/judol-domains.txt'), 'utf8');
  const domains = parseJudolTxt(src);
  const rules = domainsToRules(domains, JUDOL_ID_START);
  writeFileSync(
    resolve(root, 'rules/judol-domains.json'),
    JSON.stringify(rules)
  );
  console.log(`Built ${rules.length} judol block rules`);
}

function buildAdultRules() {
  const src = readFileSync(resolve(root, 'data/adult-hosts-source.txt'), 'utf8');
  const domains = parseHostsFile(src);
  const truncated = domains.slice(0, ADULT_MAX_RULES);
  if (domains.length > ADULT_MAX_RULES) {
    const dropped = domains.length - ADULT_MAX_RULES;
    console.warn(
      `WARNING: dropped ${dropped} adult domains due to DNR per-ruleset limit ` +
      `(${ADULT_MAX_RULES}). Consider splitting into multiple rulesets or raising ` +
      `max_number_of_static_rules in manifest.json.`
    );
  }
  const rules = domainsToRules(truncated, ADULT_ID_START);
  writeFileSync(
    resolve(root, 'rules/adult-domains.json'),
    JSON.stringify(rules)
  );
  console.log(`Built ${rules.length} adult block rules (from ${domains.length} source domains)`);
}

buildJudolRules();
buildAdultRules();
