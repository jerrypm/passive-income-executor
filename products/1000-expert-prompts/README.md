# 1000 Expert Prompts — Gumroad Product

**Price:** $9 launch → $19 after 100 sales → $29 at 500 sales
**Category:** Digital download / ebook
**Status:** Ready to upload

## Package Contents

| File | Purpose |
|------|------|
| `1000-expert-prompts.md` | Master ebook — 1000 prompts + intro + TOC (3127 lines) |
| `1000-expert-prompts.pdf` | Print-ready PDF, orange-accent styling, ~60 pages |
| `1000-expert-prompts.html` | Self-contained styled HTML (open in browser) |
| `HOW-TO-USE.md` | Quick-start guide teaching the four pillars of pro prompting |
| `gumroad-listing.md` | Full Gumroad listing copy, title, description, launch thread |
| `src/01-marketing-sales-copywriting-100-prompts.md` | Category 1 |
| `src/02-content-blogging-seo-100-prompts.md` | Category 2 |
| `src/03-business-strategy-startup-100-prompts.md` | Category 3 |
| `src/04-software-development-100-prompts.md` | Category 4 |
| `src/05-ai-automation-productivity-100-prompts.md` | Category 5 |
| `src/06-writing-editing-storytelling-100-prompts.md` | Category 6 |
| `src/07-social-media-growth-100-prompts.md` | Category 7 |
| `src/08-data-research-finance-100-prompts.md` | Category 8 |
| `src/09-design-branding-100-prompts.md` | Category 9 |
| `src/10-career-coaching-learning-100-prompts.md` | Category 10 |

## Pre-Launch Checklist

- [x] Build PDF (Chrome headless → `1000-expert-prompts.pdf`)
- [x] Build HTML (`1000-expert-prompts.html`, styled with ebook CSS)
- [ ] Generate cover image (Midjourney prompt in `gumroad-listing.md`)
- [ ] Create ZIP bundle: master.md + PDF + HTML + HOW-TO-USE.md + 10 category files
- [ ] Upload to Gumroad at zerix1.gumroad.com
- [ ] Set price to $9, enable 14-day refund
- [ ] Paste long description from `gumroad-listing.md`
- [ ] Add tags (see `gumroad-listing.md`)
- [ ] Add to CLAUDE.md's Gumroad products list (new 5th product)
- [ ] Schedule launch tweet thread (8 tweets, already drafted)
- [ ] Cross-post on LinkedIn, Nostr, dev.to, Hashnode

## Rebuild Commands

```bash
cd /Users/jeripurnamamaulid/Documents/14_Web-projects/passive-income-executor/products/1000-expert-prompts

# 1. Rebuild master markdown from src/
cat src/01-*.md src/02-*.md src/03-*.md src/04-*.md src/05-*.md \
    src/06-*.md src/07-*.md src/08-*.md src/09-*.md src/10-*.md > 1000-expert-prompts.md

# 2. Rebuild styled HTML (ebook CSS in /tmp/ebook.css)
pandoc 1000-expert-prompts.md \
  -o 1000-expert-prompts.html \
  --standalone \
  --toc \
  --toc-depth=2 \
  --metadata title="1000 Expert Prompts" \
  -c /tmp/ebook.css \
  --embed-resources

# 3. Rebuild PDF via Chrome headless (no LaTeX needed)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=1000-expert-prompts.pdf \
  "file://$(pwd)/1000-expert-prompts.html"
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
