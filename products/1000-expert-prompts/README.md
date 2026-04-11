# 1000 Expert Prompts — Gumroad Product

**Price:** $9 launch → $19 after 100 sales → $29 at 500 sales
**Category:** Digital download / ebook
**Status:** Ready to upload

## Package Contents

| File | Purpose |
|------|------|
| `1000-expert-prompts.md` | Master ebook — 1000 prompts + intro + TOC (3000+ lines) |
| `HOW-TO-USE.md` | Quick-start guide teaching the four pillars of pro prompting |
| `gumroad-listing.md` | Full Gumroad listing copy, title, description, launch thread |
| `src/01-marketing-sales-copywriting.md` | Category 1 — 100 prompts |
| `src/02-content-blogging-seo.md` | Category 2 — 100 prompts |
| `src/03-business-strategy-startup.md` | Category 3 — 100 prompts |
| `src/04-software-development.md` | Category 4 — 100 prompts |
| `src/05-ai-automation-productivity.md` | Category 5 — 100 prompts |
| `src/06-writing-editing-storytelling.md` | Category 6 — 100 prompts |
| `src/07-social-media-growth.md` | Category 7 — 100 prompts |
| `src/08-data-research-finance.md` | Category 8 — 100 prompts |
| `src/09-design-branding.md` | Category 9 — 100 prompts |
| `src/10-career-coaching-learning.md` | Category 10 — 100 prompts |

## Pre-Launch Checklist

- [ ] Convert `1000-expert-prompts.md` to PDF (pandoc or Typora)
- [ ] Generate cover image (Midjourney prompt in `gumroad-listing.md`)
- [ ] Create ZIP bundle: master.md + PDF + HOW-TO-USE.md + 10 category files
- [ ] Upload to Gumroad at zerix1.gumroad.com
- [ ] Set price to $9, enable 14-day refund
- [ ] Paste long description from `gumroad-listing.md`
- [ ] Add tags (see `gumroad-listing.md`)
- [ ] Add to CLAUDE.md's Gumroad products list (new 5th product)
- [ ] Schedule launch tweet thread (8 tweets, already drafted)
- [ ] Cross-post on LinkedIn, Nostr, dev.to, Hashnode

## PDF Build Command

```bash
cd /Users/jeripurnamamaulid/Documents/14_Web-projects/passive-income-executor/products/1000-expert-prompts

# Option 1 — pandoc (needs: brew install pandoc + basictex)
pandoc 1000-expert-prompts.md \
  -o 1000-expert-prompts.pdf \
  --toc \
  --toc-depth=2 \
  -V geometry:margin=1in \
  -V documentclass=book \
  -V fontsize=11pt

# Option 2 — markdown-pdf (node)
npx markdown-pdf 1000-expert-prompts.md
```

## Gumroad Upload Bundle Command

```bash
cd /Users/jeripurnamamaulid/Documents/14_Web-projects/passive-income-executor/products/1000-expert-prompts

# Build the zip that customers download
zip -r 1000-expert-prompts.zip \
  1000-expert-prompts.md \
  1000-expert-prompts.pdf \
  HOW-TO-USE.md \
  src/
```

## Revenue Projection

Conservative at $9:
- 10 sales/mo × $9 = **$90/mo** (minus ~10% Gumroad fees = ~$81)
- 50 sales/mo × $9 = **$450/mo** (~$405 net)

Bump to $19 after social proof:
- 30 sales/mo × $19 = **$570/mo** (~$513 net)

Bundle with existing products (Terminal Income Starter, Ollama Monetizer, Nostr Toolkit) for a "Terminal Founder Bundle" at $29 to lift AOV.

## Notes

- Every prompt is role-based, framework-powered, variable-driven, and has a defined output format
- 10 categories × 100 prompts = 1000 total
- Covers: Marketing, Content/SEO, Business, Engineering, AI, Writing, Social, Data, Design, Career
- Master file is a single markdown ebook with cover, TOC, intro, and all categories concatenated
