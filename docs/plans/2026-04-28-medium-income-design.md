# Medium Income 2026 — Product Design

**Date:** 2026-04-28
**Author:** Jeri P.M. (jrdevhub.com)
**Status:** Design locked, ready to build
**Build folder:** `products/medium-income/`
**Reference product (same pipeline):** `products/1000-expert-prompts/`

---

## 1. Positioning

**Working title:** *Medium Income 2026: The Beginner's Playbook to Your First $100 (Updated for the 2026 Partner Program)*

**Subtitle:** From zero stories to your first paid Stripe payout — written by a working dev who earns on Medium today, for writers anywhere in the world.

**Cover badge:** `UPDATED FOR 2026 · 100+ COUNTRIES SUPPORTED`

**Back-cover paragraph:**
Most Medium guides on the market were written before August 2023, when the 100-follower rule was killed and the Partner Program was rebuilt. They were written before the August 2024 expansion that added 77 new countries to the program — bringing eligible writers to 100+ countries across six continents. They were written before the Friend tier (4× writer pay), the February 2026 new-member-conversion bonus, and the AI-content paywall ban. This guide is written for the 2026 reality, by an author who applied, got accepted, and earns through it now.

**Author credibility:**
"By Jeri P.M. — Medium writer since 2017, jrdevhub.com. Real receipts inside: a single 12-item listicle that earned $67.99 (5,800 views, 2,700 reads), built with the exact title formula taught in Chapter 4."

**Target buyer:**
Complete beginner anywhere in the world (Asia, Europe, Africa, LATAM, US) who has never published on Medium and wants a step-by-step path to their first paid story.

**Price:** $19 launch. Bump to $24 after first 100 sales.

**Format:** PDF + standalone HTML + ZIP bundle. 100–130 pp PDF, A4. Cover image 2560×3200 PNG.

---

## 2. Market Wedge (vs competitors)

Research surfaced 8 competing Gumroad/Kindle products. Most are 2023-vintage, US-centric, and skip the parts buyers actually struggle with.

**What no competitor owns (= our wedge):**
- Stripe payout walkthrough for writers in the 100+ supported countries (post-2024 expansion)
- 2026 reality: Friend tier 4× math, Feb 2026 conversion bonus, Boost decline
- AI-policy enforcement (undisclosed AI = "Network only" distribution)
- Fill-in-the-blank title templates with niche variants (not just descriptions)
- Repurpose 1 Medium hit → 1 Gumroad product, with the author's own catalog as worked example

**Reference competitors:**
- Lizzie Davey, *Medium Course* — Gumroad, ~$29–$49, 158 pp + course (most comprehensive; we win on recency + price)
- Paul Rose, *The Medium Income Playbook* — Gumroad, ~$15–$25 (we win on depth + global angle)
- Christina Piccoli, *Medium Money* — Gumroad, ~$9–$19 (we win on depth)

---

## 3. Chapter Outline (12 chapters, ~100–130 pp)

### Front matter (~6 pp)
Cover, title page, "Who this is for", "What's NOT in this book", "How to use this book in 14 days", legal/license, table of contents.

### Part I — Foundations (~25 pp)
1. **The 2026 Medium Economy** — what changed since 2023, Friend tier 4× math, Boost decline, AI policy, Feb 2026 conversion bonus.
2. **Eligibility Without Confusion** — 6 stories + 3 months active + paying member. 100+ country list (post-2024 expansion). Common rejection reasons + 30-day cooldown trap. Worldwide examples (US, UK, India, Indonesia, Nigeria, Brazil, Philippines, Germany).
3. **Setting Up Your Profile to Convert** — bio formula, profile photo, pinned story, custom domain ($5/mo Member benefit), publication choice.

### Part II — The First Article (~30 pp)
4. **The Number+Hook Title Formula** — Why "I" wins, odd vs even data, $67.99 SwiftUI receipts case study, 6 hook patterns with examples per niche (tech, finance, productivity, lifestyle, AI, career).
5. **The 7-Part Article Skeleton** — opening pattern, scannable subheads, image placement, code/data blocks, pull-quotes, CTA, friend-link footer. 8 niche-specific fill-in templates.
6. **Your First Article in 14 Days** — day-by-day checklist. Topic picking, draft, edit, image sourcing, publication submission.

### Part III — Distribution & Earnings (~30 pp)
7. **Publications: Pitch & Get In** — top 30 paying publications, pitch email templates, Boost-eligible publications list.
8. **Engagement Mechanics** — read time vs claps, Friend Links, conversion-bonus mechanics (Feb 2026 update), what NOT to do (clap-trade groups = ban risk).
9. **Stripe Payout Worldwide** — wallet setup, country-by-country tax notes (W-8BEN for non-US, supported currencies), $10 minimum, payout calendar.

### Part IV — Compounding (~25 pp)
10. **The 90-Day Calendar** — week-by-week posting cadence, topic clustering, when to start your own publication.
11. **Repurpose: Medium → Gumroad Funnel** — take 1 hit listicle → 1 paid PDF. Live examples from author's catalog.
12. **What Comes After the First $100** — niche down, hire editor, ghostwrite, paid newsletter alternative.

### Back matter (~10 pp)
30 title templates appendix, 8 article skeleton appendix, audit checklist, glossary, "next steps" CTA to Gumroad.

---

## 4. Visual Design

Matches `1000-expert-prompts` brand for catalog cohesion.

- **Fonts:** Charter / Georgia (body), Inter (headings)
- **Primary color:** `#1a8917` (Medium green)
- **Accent color:** `#ff7f24` (jrdevhub orange)
- **H2:** green border-top, `page-break-before: always`
- **Pull-quotes:** green left border on cream background
- **Code/template boxes:** dark theme (`#1e1e1e` bg, cream text) — visually distinguishes "copy this"
- **Stat cards:** orange border boxes for receipts ("$67.99 · 5.8K views · 2.7K reads")

### Embedded screenshots (7 PNGs in `images/`)
1. Stats dashboard (32K presentations / 10.4K views / 3.2K reads / +19 followers) — Ch 1
2. Top 3 SwiftUI articles ($67.99 / $66.42 / $31.27) — Ch 4
3. Partner Program landing page — Ch 2
4. MPP application form — Ch 2
5. Member ($5/mo) vs Friend ($15/mo) monthly pricing — Ch 1
6. Annual pricing ($50/$150 with $30 savings) — Ch 1
7. Earnings history table (Apr 2026 → Oct 2024, $17–$92 range) — Ch 1

All in HTML at 600 px max width for print.

### Cover (`cover.html`)
1280×1600, dark background. Big "$100" wordmark replacing the "1000" pattern from prompts cover. Subtitle: "The 2026 Beginner's Playbook". Bottom bar: "100+ countries · Updated for 2026" left, "jrdevhub.com" right.

---

## 5. File Structure

```
products/medium-income/
├── medium-income.md              ← master MD (assembled from src/)
├── medium-income.html            ← pandoc-generated
├── medium-income.pdf             ← Chrome headless print
├── medium-income.zip             ← distribution bundle
├── cover.html                    ← cover source
├── cover.png                     ← 2560×3200 (2x)
├── README.md                     ← buyer-facing
├── HOW-TO-USE.md                 ← 14-day quickstart
├── gumroad-listing.md            ← marketing copy
├── header.html                   ← CSS injection for pandoc
├── images/                       ← embedded screenshots (7 PNGs)
├── bonuses/
│   ├── 30-title-templates.md
│   ├── 8-article-skeletons.md
│   ├── stripe-country-checklist.pdf
│   ├── 14-day-launch-calendar.html
│   └── medium-to-gumroad-funnel-template.md
└── src/
    ├── 00-frontmatter.md
    ├── 01-the-2026-economy.md
    ├── 02-eligibility.md
    ├── 03-profile-setup.md
    ├── 04-title-formula.md
    ├── 05-article-skeleton.md
    ├── 06-first-article-14-days.md
    ├── 07-publications.md
    ├── 08-engagement-mechanics.md
    ├── 09-stripe-payout.md
    ├── 10-90-day-calendar.md
    ├── 11-medium-to-gumroad.md
    ├── 12-after-first-100.md
    └── 99-backmatter.md
```

---

## 6. Build Pipeline

Reuse exact pipeline from `1000-expert-prompts/` — already debugged.

1. Each src `.md` ends with trailing blank line (regression-proof for concat).
2. Concatenate `src/*.md` → master `medium-income.md`.
3. Body TOC slugs use single dash to match pandoc auto-id.
4. `pandoc medium-income.md --standalone --metadata title="Medium Income 2026" --metadata author="Jeri P.M." -H header.html -o medium-income.html` (no `--toc` — body TOC suffices).
5. Chrome headless print → PDF (Skia/PDF producer).
6. Cover: Chrome headless screenshot at 1280×1600 with `--force-device-scale-factor=2`.
7. ZIP: master MD + HTML + PDF + cover + bonuses/ + src/.

---

## 7. Timeline (3 weeks part-time, 21 days)

| Week | Days | Deliverables |
|------|------|--------------|
| 1 | 1–7 | Part I (Ch 1–3) + Part II (Ch 4–6). Embed screenshots. Review. |
| 2 | 8–14 | Part III (Ch 7–9) + Part IV (Ch 10–12). Backmatter + bonuses. |
| 3 | 15–21 | Cover design, build pipeline, copy editing pass, `gumroad-listing.md`, upload as draft, soft launch. |

---

## 8. Launch Checklist (post-build)

- Upload PDF + ZIP to Gumroad ($19, "Medium Income 2026")
- Cross-promote in existing Gumroad products' "next products" section
- Tweet thread from @luffyselah (under 277 chars per CLAUDE.md rule, Profile 10)
- Post Medium article: "How I Wrote a Medium Income Guide" (meta self-promo, Friend Link enabled)
- Add to jrdevhub.com sidebar/footer
- Add to all existing Blogger articles' bottom CTA
- Add to `CLAUDE.md` Gumroad Products list

---

## 9. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| MPP rules change before launch | "Updated for 2026" badge, free email update for buyers, `updates@jrdevhub.com` list |
| Lizzie Davey's $29 / 158 pp guide outranks | Win on price ($19), recency (2026 vs 2023), global angle (100+ countries vs US-default) |
| "Another Medium guide" perception | Cover badge + receipts on page 1 |
| Buyer disappointment if earnings claims oversold | Honest framing: "first $100", not "$10K/mo". Real $17–$92/mo author receipts. |

---

## 10. Source Research

Research conducted 2026-04-28 via web search. Key citations:

- [Medium Help — MPP Eligibility](https://help.medium.com/hc/en-us/articles/39121627791639-Medium-Partner-Program-eligibility)
- [Medium Blog — +77 Countries (2024 expansion)](https://medium.com/blog/weve-added-77-countries-to-the-medium-partner-program-827a574fcdf0)
- [Medium Help — AI Content Policy](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy)
- [Medium Blog — Become a Friend of Medium (4× pay tier)](https://medium.com/blog/become-a-friend-of-medium-dd2fa7bf16c3)
- [Medium Blog — Feb 2026 Conversion Bonus](https://medium.com/blog/partner-program-update-starting-february-17-were-rewarding-stories-that-bring-in-new-members-3e84d2eb6e68)
- [Medium Help — Calculating Earnings](https://help.medium.com/hc/en-us/articles/360036691193-Calculating-earnings-in-the-Partner-Program)
- [Medium Help — Payouts](https://help.medium.com/hc/en-us/articles/25267297935895-Payouts)
- [OptinMonster — 21 Viral Headlines (odd-number CTR data)](https://optinmonster.com/why-these-21-headlines-went-viral-and-how-you-can-copy-their-success/)
- [CoSchedule — Headline Formulas](https://coschedule.com/headlines/headline-formulas-and-templates)
- Competing products: Lizzie Davey *Medium Course*, Paul Rose *Medium Income Playbook*, Christina Piccoli *Medium Money*, Victoria Kurichenko *4 Figures Selling eBooks on Gumroad*.
