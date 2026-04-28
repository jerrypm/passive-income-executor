# Medium Income 2026 — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Ship a 100–130 page beginner's guide to earning on Medium in 2026 as PDF + HTML + ZIP, ready to upload to Gumroad at $19.

**Architecture:** Markdown source per chapter under `src/`, concatenated into a master MD, rendered to HTML via pandoc, printed to PDF via headless Chrome, packaged into ZIP. Same pipeline as `products/1000-expert-prompts/` — already debugged. Cover generated separately from `cover.html` via Chrome screenshot at 2× scale.

**Tech Stack:** pandoc (Homebrew), Chrome headless (`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`), Python 3 (`/usr/bin/python3`) for assembly + verification, `zip` for packaging.

**Reference product:** `products/1000-expert-prompts/` — read its `cover.html`, `header.html` (extracted at build time), and `src/` layout before starting. Anything that worked there is the default here.

**Design source:** `docs/plans/2026-04-28-medium-income-design.md` — read this once before Task 0.1 for full context.

**Working directory for all tasks:** `/Users/jeripurnamamaulid/Documents/14_Web-projects/passive-income-executor`

---

## Phase 0: Setup

### Task 0.1: Create folder structure

**Files:**
- Create: `products/medium-income/{src,images,bonuses}/`

**Step 1: Verify clean slate**

Run: `ls products/medium-income/`
Expected: empty (or "No such file or directory" — both fine)

**Step 2: Create directories**

Run: `mkdir -p products/medium-income/{src,images,bonuses}`

**Step 3: Verify**

Run: `ls -la products/medium-income/`
Expected: three subdirectories `src/`, `images/`, `bonuses/`

**Step 4: Commit**

Skip — no files yet.

---

### Task 0.2: Save the 7 source screenshots into `images/`

**Files:**
- Create: `products/medium-income/images/01-stats-dashboard.png`
- Create: `products/medium-income/images/02-top-articles.png`
- Create: `products/medium-income/images/03-mpp-landing.png`
- Create: `products/medium-income/images/04-mpp-application.png`
- Create: `products/medium-income/images/05-pricing-monthly.png`
- Create: `products/medium-income/images/06-pricing-annual.png`
- Create: `products/medium-income/images/07-earnings-history.png`

**Step 1: Locate source images**

The 7 screenshots are already on disk in `~/Downloads/` from a prior brainstorming session. List candidates:
Run: `ls -lt ~/Downloads/Screenshot*2026-04-28*.png | head -20`
Expected: see at least 7 PNGs from 2026-04-28.

**Step 2: Identify each image**

Open each candidate (Quicklook or Read tool) and map to filenames in the list above. Stats dashboard = the green-line chart with 32K presentations. Top articles = the dark list with $67.99/$66.42/$31.27. MPP landing = green plant illustration. MPP application = white form. Pricing monthly = "Pay monthly" highlighted. Pricing annual = "Pay annually" highlighted. Earnings history = month-by-month dollar list.

**Step 3: Copy with renames**

Use `cp` (preserves originals). Example:
```bash
cp ~/Downloads/Screenshot\ 2026-04-28\ at\ 08.21.07.png products/medium-income/images/01-stats-dashboard.png
```
Repeat for each, mapping carefully. If wrong file copied, `rm` and redo — do not commit until all 7 are right.

**Step 4: Verify**

Run: `ls products/medium-income/images/`
Expected: 7 PNGs named `01-…` through `07-…`.
Run: `sips -g pixelWidth -g pixelHeight products/medium-income/images/*.png`
Expected: all readable, dimensions logged.

**Step 5: Commit**

```bash
git add products/medium-income/images/
git commit -m "feat(medium-income): seed 7 source screenshots from author Medium account"
```

---

### Task 0.3: Add to `.gitignore` and `CLAUDE.md`

**Files:**
- Modify: `CLAUDE.md` (Gumroad Products section, add as item 7)

**Step 1: Read CLAUDE.md Gumroad section**

Use Read tool on `CLAUDE.md`, find the "Gumroad Products" list.

**Step 2: Append item 7 (placeholder URL)**

Add: `7. Medium Income 2026 ($19, launch) — Gumroad URL pending upload. Source: 'products/medium-income/'. 12 chapters, 100-130pp PDF, beginner playbook for the 2026 Partner Program.`

**Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(claude.md): register Medium Income 2026 product slot"
```

---

## Phase 1: Frontmatter

### Task 1: Write `src/00-frontmatter.md`

**Files:**
- Create: `products/medium-income/src/00-frontmatter.md`

**Word count target:** 800–1,200 words

**Required content beats (in order):**
1. `# Medium Income 2026` (h1)
2. `### The Beginner's Playbook to Your First $100 — Updated for the 2026 Partner Program` (h3)
3. Blockquote tagline: 12 chapters · 100+ countries · zero-to-payout. From a working dev who earns on Medium today, for writers anywhere in the world.
4. `## Who This Is For` — 5 bulleted personas (complete beginner, returning lapsed writer, non-US writer, niche expert wanting paid audience, side-income seeker)
5. `## What's NOT In This Book` — set expectations honestly: not a get-rich-quick guide, not viral hacks, not for existing pro writers, not US-only, not AI-content workarounds
6. `## How To Use This Book In 14 Days` — day-by-day overview (Day 1: read Ch 1-3, Day 2: apply Ch 7 publication research, etc.)
7. `## Legal & License` — personal+commercial use, no resale of pack, no warranty, AI output requires human review (mirror 1000-expert-prompts language)
8. `---`
9. `## Table of Contents` — 12 numbered links: `1. [The 2026 Medium Economy](#the-2026-medium-economy) — *what changed since 2023, Friend tier 4× math, AI policy*` (use single-dash slugs to match pandoc auto-id; see Task 23 for verification)

**Required slug list (must match `## N — Title` heading slugs after pandoc):**
```
the-2026-medium-economy
eligibility-without-confusion
setting-up-your-profile-to-convert
the-numberhook-title-formula
the-7-part-article-skeleton
your-first-article-in-14-days
publications-pitch-get-in
engagement-mechanics
stripe-payout-worldwide
the-90-day-calendar
repurpose-medium-gumroad-funnel
what-comes-after-the-first-100
```

**Step 1: Draft the file**

Use Write tool. Apply professional-writer voice (warm, specific, no hype). Include the blockquote tagline. Use markdown lists, not numbered prose, where the design says "5 bullets" or "by-day overview".

**Step 2: Verify word count + structure**

Run:
```bash
wc -w products/medium-income/src/00-frontmatter.md
grep -c '^## ' products/medium-income/src/00-frontmatter.md
grep -c '^- \|^[0-9]\+\.' products/medium-income/src/00-frontmatter.md
```
Expected: 800 ≤ word count ≤ 1200; at least 5 `## ` headings; at least 17 list items (5 personas + 5 not-in-book + 7 day overview).

**Step 3: Verify the TOC slugs are exactly right**

Run:
```bash
grep -oE '#[a-z0-9-]+' products/medium-income/src/00-frontmatter.md | sort -u
```
Expected: includes the 12 slugs listed above.

**Step 4: Append trailing blank line (regression-proof for concat)**

Run:
```bash
/usr/bin/python3 -c "from pathlib import Path; p=Path('products/medium-income/src/00-frontmatter.md'); p.write_text(p.read_text().rstrip('\n')+'\n\n')"
```

**Step 5: Commit**

```bash
git add products/medium-income/src/00-frontmatter.md
git commit -m "feat(medium-income): frontmatter — title, audience, TOC, license"
```

---

## Phase 2: Part I — Foundations

### Task 2: Write `src/01-the-2026-economy.md`

**Files:**
- Create: `products/medium-income/src/01-the-2026-economy.md`

**Word count target:** 1,800–2,400 words

**Required heading:** `## 1 — The 2026 Medium Economy`
Followed by `### What This Chapter Covers` blockquote with 4-bullet list.

**Required content beats:**
1. Why 2023+ guides are wrong (100-follower rule killed Aug 2023, MPP rebuilt around paying members)
2. The Friend-tier math (Member $5/mo vs Friend $15/mo — Friend pays 4× per read; show worked example)
3. The Feb 17, 2026 conversion-bonus update (writers now earn when paywall hit converts to new member; cite blog post)
4. The Boost-program decline (was ~30% bonus, now ~7% per Jan 2026 rebalance; cite analysis)
5. The AI content policy (undisclosed AI = "Network only" distribution = no MPP earnings; disclosed AI cannot be paywalled)
6. Honest receipts table — embed `images/07-earnings-history.png` and walk through real $17–$92 monthly variance, not a $10K hype claim
7. End-of-chapter "What's next" pointing to Ch 2 eligibility check

**Required embedded images:**
- `images/01-stats-dashboard.png` (caption: "32K monthly story presentations from a writer with 1,171 followers — distribution is not just for the famous.")
- `images/05-pricing-monthly.png` and `images/06-pricing-annual.png` side-by-side (caption: "Member vs Friend tiers — the Friend tier sends 4× more dollars per read to the writer.")
- `images/07-earnings-history.png` (caption: "Real monthly earnings, Oct 2024 → Apr 2026. No hype, no $10K screenshots — your first $100 is the realistic milestone.")

**Image markdown syntax:**
```markdown
![Caption text here](../images/01-stats-dashboard.png)
*Caption text here.*
```
(The relative path `../images/` resolves correctly when the master MD is in `products/medium-income/`.)

**Step 1: Draft the chapter**

Write in clear paragraphs, not bullet walls. Use one h3 per content beat. Include the worked Friend-tier math example: "If a Friend reads your story for 4 minutes vs a Member reading for 4 minutes, you earn approximately 4× as much from the Friend read."

**Step 2: Verify**

```bash
wc -w products/medium-income/src/01-the-2026-economy.md
grep -c '^## \|^### ' products/medium-income/src/01-the-2026-economy.md
grep -c '!\[' products/medium-income/src/01-the-2026-economy.md
```
Expected: 1800 ≤ words ≤ 2400; at least 6 headings; at least 3 image embeds.

**Step 3: Append trailing blank line**

```bash
/usr/bin/python3 -c "from pathlib import Path; p=Path('products/medium-income/src/01-the-2026-economy.md'); p.write_text(p.read_text().rstrip('\n')+'\n\n')"
```

**Step 4: Commit**

```bash
git add products/medium-income/src/01-the-2026-economy.md
git commit -m "feat(medium-income): chapter 1 — the 2026 Medium economy"
```

---

### Task 3: Write `src/02-eligibility.md`

**Word count target:** 1,400–1,800 words

**Required heading:** `## 2 — Eligibility Without Confusion`

**Required content beats:**
1. The 4 hard requirements: 6 published stories, 3 months active, 18+, paying Medium member
2. The country list (100+ post-2024 expansion). Mention specifically that the 2024 update added 77 new countries. Provide a categorized list (Asia: India, Indonesia, Philippines, Malaysia, Vietnam, Bangladesh, Pakistan, Thailand…; Africa: Nigeria, Kenya, South Africa, Egypt, Ghana…; LATAM: Brazil, Mexico, Argentina, Colombia, Chile…; Europe: most EU + UK, Norway, Switzerland; Americas: US, Canada). Direct readers to the official Stripe-supported list for the canonical version.
3. Common rejection reasons (6 items): not paying member, country not Stripe-eligible, "insufficient unique value", AI-flagged writing, profile incomplete, under 6 stories or 3 months active
4. The 30-day cooldown after rejection — what to fix during it
5. Step-by-step application walkthrough — embed `images/03-mpp-landing.png` then `images/04-mpp-application.png`, narrate field by field
6. Profile completeness checklist before applying (5 items)

**Required embedded images:**
- `images/03-mpp-landing.png`
- `images/04-mpp-application.png`

**Step 1: Draft**

Use Write tool. Use a 3-column markdown table for the country list (Continent | Sample countries | Notes).

**Step 2-4:** Same verify / blank-line / commit pattern as Task 2.

Commit message: `feat(medium-income): chapter 2 — MPP eligibility worldwide`

---

### Task 4: Write `src/03-profile-setup.md`

**Word count target:** 1,200–1,600 words

**Required heading:** `## 3 — Setting Up Your Profile to Convert`

**Required content beats:**
1. Bio formula: `[role] who writes about [topic 1], [topic 2], [topic 3]. [Hook line about what reader gets].`
2. Profile photo — clear face, neutral background, smile. Why selfie cameras are fine.
3. Pinned story — pick your strongest, ideally a listicle. Pin it before applying to MPP.
4. Custom domain via Member subscription ($5/mo benefit) — when it's worth it (after first $100 earned)
5. Picking a niche — frame as "what 3 topic tags do you want to be known for"
6. Should you join an existing publication or create your own — rule: join for the first 6 stories, create after.

**Required embedded images:** none (text-only chapter — keeps PDF size down)

**Step 1-4:** Standard pattern.

Commit message: `feat(medium-income): chapter 3 — profile setup that converts`

---

## Phase 3: Part II — The First Article

### Task 5: Write `src/04-title-formula.md`

**Word count target:** 2,000–2,600 words

**Required heading:** `## 4 — The Number+Hook Title Formula`

**Required content beats:**
1. Why "I" is the most predictive word in viral Medium titles (cite the 100-headlines analysis)
2. Optimal number range (10 strongest, 5/7/15 close behind, under 15 dominates)
3. Odd vs even data — odd ~20% higher CTR per OptinMonster, BUT authenticity beats the rule (cite this)
4. **Author case study with receipts** — embed `images/02-top-articles.png` and walk through "12 SwiftUI Components" (5.8K views, 2.7K reads, $67.99) — explain why an even number won (real exhaustive list + "I use these daily" frame)
5. The 6 hook patterns table:
   - "X [items] I Use [daily / every day / in production]" — usage hook
   - "X [items] That [Saved Me / Changed My / Made Me $Y]" — outcome hook
   - "X [items] Most [audience] Get Wrong" — contrarian hook
   - "X [items] I Wish I Knew Before [milestone]" — regret hook
   - "X Underrated / Hidden [items]" — secret hook
   - "After [X years/months], Here Are [N] [items]" — credibility hook
6. Title-length rules (6–12 words, 50–70 chars). Include a Python one-liner snippet for length checking.
7. 5-step exercise: pick a number, pick a hook pattern, draft 3 candidate titles, kill 2, commit to 1.

**Required embedded image:** `images/02-top-articles.png`

**Step 1-4:** Standard pattern.

Commit message: `feat(medium-income): chapter 4 — number+hook title formula with receipts`

---

### Task 6: Write `src/05-article-skeleton.md`

**Word count target:** 1,800–2,400 words

**Required heading:** `## 5 — The 7-Part Article Skeleton`

**Required content beats — the 7 parts (1 h3 each):**
1. Opening (3–5 sentences) — pattern: pain → promise → proof
2. Scannable subheads (every 200–300 words; sentence case; avoid clickbait)
3. Image placement (one image per major section; Unsplash + caption + credit)
4. Code/data blocks (use triple-backtick with language; keep under 30 lines per block; explain in plain English first)
5. Pull-quotes (one per article max; use blockquote syntax; ideal length 12–20 words)
6. CTA (link to your other article OR your newsletter — never both)
7. Friend-link footer (always include; explain why; show example markdown)

**Plus a closing section: 8 niche-specific micro-skeletons** (just the structural outline, 5–8 lines each):
- Tech listicle
- Personal essay
- Tutorial
- Contrarian opinion
- Case study
- Listicle review (book/tool round-up)
- How-to (problem → step 1 → step 2 → step 3 → result)
- Story (situation → conflict → choice → outcome → lesson)

**Step 1-4:** Standard pattern.

Commit message: `feat(medium-income): chapter 5 — 7-part article skeleton + 8 niche templates`

---

### Task 7: Write `src/06-first-article-14-days.md`

**Word count target:** 1,400–1,800 words

**Required heading:** `## 6 — Your First Article in 14 Days`

**Required content beats:**
- Day-by-day plan (use a markdown table: Day | Focus | Time | Output)
- Day 1: pick niche + target publication (1 hr)
- Day 2: brainstorm 10 title candidates using Ch 4 (45 min)
- Day 3: outline using Ch 5 skeleton (1 hr)
- Day 4-6: write first draft (2 hrs total, broken into sessions)
- Day 7: rest day — do NOT touch the draft
- Day 8: edit pass 1 — structure (1 hr)
- Day 9: edit pass 2 — line edit (1 hr)
- Day 10: image sourcing from Unsplash (30 min)
- Day 11: format in Medium editor + add Friend Link footer (1 hr)
- Day 12: submit to publication via their submission form
- Day 13: while you wait, draft your second article's title (15 min)
- Day 14: published — share on 1 (one) platform; do NOT spam

**Plus:** "What to do if the publication says no" — 3-step recovery (re-pitch elsewhere, self-publish under your profile + tag, learn from feedback)

**Step 1-4:** Standard pattern.

Commit message: `feat(medium-income): chapter 6 — first article in 14 days plan`

---

## Phase 4: Part III — Distribution & Earnings

### Task 8: Write `src/07-publications.md`

**Word count target:** 1,600–2,000 words

**Required heading:** `## 7 — Publications: Pitch & Get In`

**Required content beats:**
1. What a publication is and why it matters (distribution multiplier)
2. The 3 publication tiers: free-to-submit (e.g., ILLUMINATION), curation-based (e.g., Better Programming), invitation-only (e.g., The Startup tier)
3. Top 30 paying publications table (Name | Niche | Submission style | Boost-eligible Y/N | Notes). At minimum cover: Better Programming, The Startup, In Plain English, ILLUMINATION, Better Humans, UX Collective, JavaScript in Plain English, ITNEXT, Level Up Coding, AI in Plain English, Write A Catalyst, The Writing Cooperative.
4. Pitch email template — for invite-only publications. Subject line + 3-paragraph body + signature.
5. Submission via form — for free-to-submit, what to fill in.
6. What gets a story Boosted (cite Boost Nomination Program help center URL)
7. Don't-do list: spamming editors, submitting same draft to 5 publications simultaneously, lying about niche

**Step 1-4:** Standard pattern.

Commit message: `feat(medium-income): chapter 7 — publications pitch and submission`

---

### Task 9: Write `src/08-engagement-mechanics.md`

**Word count target:** 1,400–1,800 words

**Required heading:** `## 8 — Engagement Mechanics`

**Required content beats:**
1. How earnings are actually calculated (member read time + engagement points + boost multiplier; cite Help Center)
2. Read time vs claps — the 2026 weighting (read time still dominant; claps are signal not direct payout)
3. Friend Links — what they are, how to add to article footer, why they help conversion
4. Feb 17, 2026 conversion bonus — when a non-member hits paywall and converts, the writer earns extra (cite blog post)
5. The 7 things NOT to do: clap-trading groups, sock-puppet accounts, paying for views, submitting plagiarized content, ignoring AI-disclosure rules, follower-spamming, comment-spamming on others' articles
6. The 5 healthy habits: reply to every comment in first 24 hr, clap others' work genuinely, follow writers in your niche, write 1 response per week to a popular article in niche, share Friend Links not paywalled links

**Step 1-4:** Standard pattern.

Commit message: `feat(medium-income): chapter 8 — engagement mechanics and 2026 payout rules`

---

### Task 10: Write `src/09-stripe-payout.md`

**Word count target:** 1,600–2,000 words

**Required heading:** `## 9 — Stripe Payout Worldwide`

**Required content beats:**
1. Why Stripe — Medium uses Stripe Express; you do NOT need a separate Stripe business account
2. Setup steps in Medium settings → Payouts → Connect Stripe
3. Country-by-country tax notes (worldwide framing, not just one country):
   - Non-US writers: W-8BEN form during onboarding; tax treaty rates vary
   - US writers: W-9 form; income reported to IRS
   - EU writers: VAT not collected by Medium; declare as personal income locally
4. Supported currencies per region (USD payout default; some countries allow local payout — check Stripe Express dashboard)
5. The $10 minimum payout threshold and the "rolling 30 days" rule
6. Payout calendar — runs around the 5th, lands 5–7 business days later
7. What to do if Stripe rejects your bank (3 fixes: try a different account, use a fintech wallet that supports Stripe, contact Stripe Express support)
8. Tracking earnings — recommend a 1-page Notion or Google Sheets template with columns: month, gross earnings, USD value if exchanged, fees, net.

**Step 1-4:** Standard pattern.

Commit message: `feat(medium-income): chapter 9 — stripe payout worldwide`

---

## Phase 5: Part IV — Compounding

### Task 11: Write `src/10-90-day-calendar.md`

**Word count target:** 1,400–1,800 words

**Required heading:** `## 10 — The 90-Day Calendar`

**Required content beats:**
- Week-by-week table (Week | Theme | Output | Goal)
- Weeks 1-4: post 1 article/week, all listicles in chosen niche, build credibility
- Weeks 5-8: post 2 articles/week (1 listicle + 1 essay or tutorial), test publication submissions
- Weeks 9-12: post 2 articles/week (settle into best-performing format), evaluate first $100 milestone
- Topic clustering — pick 3 topic tags, write 4 articles per tag in 90 days
- When to start your own publication (rule: after first $100 OR 25 followers from organic, whichever first)
- The 3-question 90-day review: which article earned most? which got most reads? what surprised you?

**Step 1-4:** Standard pattern.

Commit message: `feat(medium-income): chapter 10 — 90-day publishing calendar`

---

### Task 12: Write `src/11-medium-to-gumroad.md`

**Word count target:** 1,600–2,000 words

**Required heading:** `## 11 — Repurpose: Medium → Gumroad Funnel`

**Required content beats:**
1. The principle: 1 hit listicle = 1 paid Gumroad PDF that triples its lifetime value
2. Identifying a "hit" — read count > 1,500 in 30 days, reads/views ratio > 25%, specific implementation comments in responses
3. The expand pattern: 12-item listicle → 50-item ebook with templates and case studies
4. Pricing rules of thumb: $5 swipe file, $9 short ebook, $19 full guide, $29 with bonuses, $49 with course module
5. Live worked example — author's own products (1000-expert-prompts $9, this Medium Income guide $19, Mastering Claude Code $19, Ollama API Monetizer $14, Nostr AI Toolkit $19). Brief case for each: which Medium thread/article fed it.
6. Gumroad listing essentials (3 mockup images, 3-paragraph description, 3 testimonials/proof shots, FAQ section)
7. Cross-promo loop — every Gumroad product links back to your Medium profile + newest article; every Medium article links to your most relevant Gumroad product via Friend Link footer.

**Step 1-4:** Standard pattern.

Commit message: `feat(medium-income): chapter 11 — medium to gumroad funnel`

---

### Task 13: Write `src/12-after-first-100.md`

**Word count target:** 1,200–1,600 words

**Required heading:** `## 12 — What Comes After the First $100`

**Required content beats:**
1. The decision tree at $100/month milestone:
   - Niche down (drop topics that earn least)
   - Hire an editor (~$30–50 per article via Upwork/Fiverr)
   - Ghostwrite for others ($100–500/article in your niche)
   - Launch a paid newsletter (Substack/Beehiiv)
   - Build a digital product (back to Ch 11)
2. The 4 mistakes that kill momentum after $100: chasing every new niche, posting daily without quality, ignoring email list, free Medium membership churn
3. The compounding mindset — 6 articles → 12 articles → 25 articles → 50 articles flywheel
4. Where to next — closing CTA pointing to backmatter, the 30-template appendix, and the author's other products

**Step 1-4:** Standard pattern.

Commit message: `feat(medium-income): chapter 12 — what comes after first $100`

---

## Phase 6: Backmatter

### Task 14: Write `src/99-backmatter.md`

**Word count target:** 600–900 words (most of the substance moves to bonus files)

**Required content beats:**
1. `## Appendix A — 30 Title Templates` — short intro paragraph, then refer to bonus file `bonuses/30-title-templates.md` for the full set; include 5 sample templates inline so the chapter is useful even without the bonuses folder open
2. `## Appendix B — 8 Article Skeletons` — short intro, refer to `bonuses/8-article-skeletons.md`, include 1 sample skeleton inline
3. `## Appendix C — Pre-Publish Audit Checklist` — 12-item bulleted checklist (title <70 chars, hook in first 3 sentences, 1 image per section, Friend Link footer, etc.)
4. `## Glossary` — 15 terms (MPP, Boost, Friend tier, Member tier, Friend Link, Boost Nomination, Highlights, Claps, Read Ratio, Curation, Publication, Stripe Express, W-8BEN, Boost Bonus, Conversion Bonus)
5. `## Next Steps` — 3 calls to action: download bonuses, leave a Gumroad rating, follow author on Medium

**Step 1-4:** Standard pattern.

Commit message: `feat(medium-income): backmatter — appendices, glossary, next steps`

---

## Phase 7: Bonuses

### Task 15: Write `bonuses/30-title-templates.md`

**Word count target:** 1,500–2,000 words

**Required structure:**
- 6 hook categories from Ch 4 (usage, outcome, contrarian, regret, secret, credibility)
- 5 templates per category = 30 total
- Each template: pattern + 1 worked example for tech/dev niche + 1 for non-tech niche
- Ends with a 3-step "how to fill in a template" mini-tutorial

**Step 1-3:** Write, verify (`wc -w` ≥ 1500), append blank line.

**Step 4: Commit**

```bash
git add products/medium-income/bonuses/30-title-templates.md
git commit -m "feat(medium-income): bonus — 30 title templates"
```

---

### Task 16: Write `bonuses/8-article-skeletons.md`

**Word count target:** 1,200–1,600 words

**Required structure:**
- 8 skeletons matching Ch 5 list (tech listicle, personal essay, tutorial, contrarian opinion, case study, listicle review, how-to, story)
- Each skeleton: section-by-section markdown template with `[FILL IN: ...]` placeholders, target word count per section, recommended hooks per section

**Step 1-4:** Standard pattern.

Commit message: `feat(medium-income): bonus — 8 article skeletons`

---

### Task 17: Write `bonuses/14-day-launch-calendar.html`

**Files:**
- Create: `products/medium-income/bonuses/14-day-launch-calendar.html`

**Step 1: Create a printable HTML calendar**

Single self-contained HTML file. Light background (printer-friendly). 14 day cards in a 2×7 grid. Each card shows day number, focus from Ch 6, time estimate, output. Use Inter or system-ui font. Add `@media print { @page { size: A4; margin: 1cm; } }`.

**Step 2: Verify in Chrome**

Open file in Chrome, Cmd+P, ensure it prints to a single A4 page with all 14 days visible.

**Step 3: Commit**

```bash
git add products/medium-income/bonuses/14-day-launch-calendar.html
git commit -m "feat(medium-income): bonus — printable 14-day launch calendar"
```

---

### Task 18: Write `bonuses/medium-to-gumroad-funnel-template.md`

**Word count target:** 800–1,200 words

**Required structure:**
- Numbered SOP: pick hit article → expand outline → write expanded chapters → cover design → Gumroad listing copy → cross-promo links
- Worked example using author's "12 SwiftUI Components" → "1000 Expert Prompts" pattern
- Editable copy-paste templates (cover badge, description, CTA paragraph for Medium footer)

**Step 1-4:** Standard pattern.

Commit message: `feat(medium-income): bonus — medium-to-gumroad funnel SOP`

---

### Task 19: Build `bonuses/stripe-country-checklist.pdf`

**Files:**
- Create intermediate: `products/medium-income/bonuses/stripe-country-checklist.md`
- Create final: `products/medium-income/bonuses/stripe-country-checklist.pdf`

**Step 1: Write the source MD**

A 1-page checklist — 3 sections: (1) prerequisites checklist (5 items), (2) supported countries summary table grouped by continent (do not list all 100+, summarize and link to Stripe's official list), (3) post-payout tax filing notes by region (US W-9, non-US W-8BEN, EU VAT note, generic note for everyone else).

**Step 2: Render to PDF via pandoc**

Run from `products/medium-income/`:
```bash
pandoc bonuses/stripe-country-checklist.md \
  --pdf-engine=weasyprint -o bonuses/stripe-country-checklist.pdf 2>&1 || \
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-sandbox \
  --print-to-pdf="$PWD/bonuses/stripe-country-checklist.pdf" \
  --no-pdf-header-footer \
  "file://$PWD/bonuses/stripe-country-checklist.md"
```
The fallback is needed if `weasyprint` is not installed. If both fail, render via `pandoc → html` then Chrome print as in Task 25.

**Step 3: Verify the PDF exists and is < 200 KB**

```bash
ls -lh products/medium-income/bonuses/stripe-country-checklist.pdf
```

**Step 4: Commit**

```bash
git add products/medium-income/bonuses/stripe-country-checklist.{md,pdf}
git commit -m "feat(medium-income): bonus — stripe country checklist PDF"
```

---

## Phase 8: Build pipeline

### Task 20: Build `header.html` (CSS for pandoc)

**Files:**
- Create: `products/medium-income/header.html`

**Step 1: Start from the 1000-expert-prompts CSS template**

Use Read tool on `products/1000-expert-prompts/1000-expert-prompts.html` line 25–103 (the `<style type="text/css">` block). That's the proven template.

**Step 2: Write `header.html` with adapted color palette**

Same structure, but:
- Add `#1a8917` (Medium green) as a secondary brand color
- Keep `#ff7f24` (orange) as primary accent
- Change h2 `color` from `#c62641` to `#1a8917`
- Change h2 `border-top` color to match
- Change blockquote `border-left` color to `#1a8917`
- Ensure `img { max-width: 600px; display: block; margin: 1em auto; }` is present so embedded screenshots scale correctly
- Add a `figure caption` style if needed

Wrap the entire CSS in a single `<style type="text/css">...</style>` block.

**Step 3: Verify**

```bash
grep -c '<style' products/medium-income/header.html
grep -c '#1a8917' products/medium-income/header.html
grep -c 'max-width: 600px' products/medium-income/header.html
```
Expected: 1 style block; at least 3 occurrences of `#1a8917`; 1 image rule.

**Step 4: Commit**

```bash
git add products/medium-income/header.html
git commit -m "feat(medium-income): pandoc header.html with green/orange brand"
```

---

### Task 21: Assemble master MD from `src/`

**Files:**
- Create: `products/medium-income/medium-income.md`

**Step 1: Verify all 14 src files exist with trailing blank lines**

```bash
for f in products/medium-income/src/*.md; do
  printf '%s -> last 4 bytes: ' "$f"
  tail -c 4 "$f" | od -c | head -1
done
```
Expected: 14 files, each ending with `\n\n`.

**Step 2: Concatenate**

```bash
/usr/bin/python3 <<'PY'
from pathlib import Path
chunks = []
for f in sorted(Path("products/medium-income/src").glob("*.md")):
    chunks.append(f.read_text().rstrip("\n") + "\n\n")
Path("products/medium-income/medium-income.md").write_text("".join(chunks))
print("master MD built:", Path("products/medium-income/medium-income.md").stat().st_size, "bytes")
PY
```

**Step 3: Verify all 12 chapter h2 headings present, each preceded by blank line**

```bash
grep -nE '^## [0-9]+ —' products/medium-income/medium-income.md
```
Expected: 12 lines.

```bash
/usr/bin/python3 -c "
import re
from pathlib import Path
lines = Path('products/medium-income/medium-income.md').read_text().split('\n')
bad = []
for i, line in enumerate(lines):
    if re.match(r'^## [0-9]+ —', line):
        if i > 0 and lines[i-1] != '':
            bad.append((i+1, line))
print('OK' if not bad else f'BAD: {bad}')
"
```
Expected: `OK`.

**Step 4: Commit**

```bash
git add products/medium-income/medium-income.md
git commit -m "build(medium-income): assemble master MD from src/"
```

---

### Task 22: Render HTML via pandoc

**Files:**
- Create: `products/medium-income/medium-income.html`

**Step 1: Run pandoc**

From `products/medium-income/`:
```bash
pandoc medium-income.md \
  --standalone \
  --metadata title="Medium Income 2026" \
  --metadata author="Jeri P.M." \
  -H header.html \
  -o medium-income.html
```
Expected: no error output; file created.

**Step 2: Verify h2 ids match expected slugs**

```bash
grep -oE '<h2 id="[^"]+">' products/medium-income/medium-income.html | sort -u
```
Expected: 12 chapter h2 ids matching Task 1 slug list, plus `#table-of-contents` etc.

**Step 3: Commit**

```bash
git add products/medium-income/medium-income.html
git commit -m "build(medium-income): render HTML via pandoc"
```

---

### Task 23: Verify TOC links resolve to h2 ids

**Step 1: Run slug-match check**

```bash
/usr/bin/python3 <<'PY'
from pathlib import Path
import re
h = Path("products/medium-income/medium-income.html").read_text()
slugs = ['the-2026-medium-economy','eligibility-without-confusion','setting-up-your-profile-to-convert','the-numberhook-title-formula','the-7-part-article-skeleton','your-first-article-in-14-days','publications-pitch-get-in','engagement-mechanics','stripe-payout-worldwide','the-90-day-calendar','repurpose-medium-gumroad-funnel','what-comes-after-the-first-100']
for s in slugs:
    has_anchor = f'<h2 id="{s}"' in h
    has_link = f'href="#{s}"' in h
    print(f'{s}: anchor={"OK" if has_anchor else "MISSING"} link={"OK" if has_link else "MISSING"}')
PY
```
Expected: all 12 print `anchor=OK link=OK`.

**Step 2: If any MISSING, fix and re-run from Task 21**

If `anchor=MISSING`, the chapter file's h2 text doesn't generate the expected pandoc slug — fix the heading or update the slug in `00-frontmatter.md` to match what pandoc actually generated. If `link=MISSING`, update `00-frontmatter.md` TOC entry.

**Step 3: Commit if any fix made**

```bash
git add products/medium-income/
git commit -m "fix(medium-income): align TOC slugs with pandoc-generated h2 ids"
```

---

### Task 24: Print PDF via Chrome headless

**Files:**
- Create: `products/medium-income/medium-income.pdf`

**Step 1: Run Chrome print**

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-sandbox \
  --print-to-pdf="$PWD/products/medium-income/medium-income.pdf" \
  --no-pdf-header-footer \
  "file://$PWD/products/medium-income/medium-income.html"
```

**Step 2: Verify size and producer**

```bash
ls -lh products/medium-income/medium-income.pdf
head -c 2000 products/medium-income/medium-income.pdf | strings | grep -iE "creator|producer" | head -3
```
Expected: 2–4 MB PDF; producer = `Skia/PDF`; creator = HeadlessChrome.

**Step 3: Open and visually spot-check**

```bash
open products/medium-income/medium-income.pdf
```
Look for: cover page → TOC → chapter 1 starts on its own page → embedded screenshots render → no raw `## N —` text leaked → footer/page-number cleanup not required (no header/footer).

**Step 4: If any visual problem, debug then re-render. Otherwise commit.**

```bash
git add products/medium-income/medium-income.pdf
git commit -m "build(medium-income): print PDF via headless Chrome"
```

---

### Task 25: Build distribution ZIP

**Files:**
- Create: `products/medium-income/medium-income.zip`

**Step 1: Build ZIP**

From `products/medium-income/`:
```bash
rm -f medium-income.zip
zip -rq medium-income.zip \
  medium-income.md medium-income.pdf medium-income.html \
  README.md HOW-TO-USE.md \
  src/ images/ bonuses/ \
  -x "*.DS_Store"
```

**Step 2: Verify contents**

```bash
unzip -l products/medium-income/medium-income.zip | tail -20
```
Expected: master MD + PDF + HTML + README + HOW-TO-USE + 14 src files + 7 images + 5 bonus files.

**Step 3: Verify size in 3–6 MB range**

```bash
ls -lh products/medium-income/medium-income.zip
```

**Step 4: Commit**

```bash
git add products/medium-income/medium-income.zip
git commit -m "build(medium-income): package distribution ZIP"
```

(Note: README.md and HOW-TO-USE.md are written in Phase 10. If those files don't exist yet when running this task, do Phase 10 first.)

---

## Phase 9: Cover

### Task 26: Write `cover.html`

**Files:**
- Create: `products/medium-income/cover.html`

**Step 1: Start from the 1000-expert-prompts cover template**

Read `products/1000-expert-prompts/cover.html`. Copy its structure: 1280×1600 viewport, constellation SVG, vignette, top-bar, content block, bottom-bar.

**Step 2: Adapt content**

- Eyebrow: `MEDIUM PARTNER PROGRAM`
- Big number: `$100` (replacing `1000`)
- Title: `Medium Income`
- Accent line: keep
- Subtitle: `The 2026 Beginner's Playbook`
- Meta: `100+ COUNTRIES · UPDATED FOR 2026 · ZERO TO PAYOUT`
- Top bar: `THE PRO PACK` left · `EDITION I · 2026` right
- Bottom bar: `JRDEVHUB.COM` left · `12 CHAPTERS · 100+ COUNTRIES` right (with `100+` colored `#1a8917`)
- Color tweak: keep `#ff7f24` orange accent but introduce `#1a8917` Medium green for the bottom-bar `100+` and possibly the accent line glow

**Step 3: Apply the locked-height fix from 1000-expert-prompts**

Make sure html/body has `min-height: 1600px; max-height: 1600px;` and `.bottom-bar` uses `bottom: 140px` (per the prior debugging of the same cover pipeline).

**Step 4: Commit**

```bash
git add products/medium-income/cover.html
git commit -m "feat(medium-income): cover.html with green+orange brand"
```

---

### Task 27: Render `cover.png` at 2× scale

**Files:**
- Create: `products/medium-income/cover.png`

**Step 1: Render via Chrome headless**

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-sandbox \
  --hide-scrollbars \
  --window-size=1280,1600 \
  --force-device-scale-factor=2 \
  --screenshot="$PWD/products/medium-income/cover.png" \
  "file://$PWD/products/medium-income/cover.html"
```

**Step 2: Verify dimensions**

```bash
sips -g pixelWidth -g pixelHeight products/medium-income/cover.png
```
Expected: 2560 × 3200.

**Step 3: Visual check — bottom text not cut**

```bash
open products/medium-income/cover.png
```
Look for: `JRDEVHUB.COM` and `12 CHAPTERS · 100+ COUNTRIES` fully visible at the bottom edge with margin. If cut, increase `.bottom-bar { bottom: 160px; }` and re-render.

**Step 4: Commit**

```bash
git add products/medium-income/cover.png
git commit -m "build(medium-income): render cover.png 2560×3200"
```

---

## Phase 10: Marketing copy

### Task 28: Write `README.md` (buyer-facing)

**Files:**
- Create: `products/medium-income/README.md`

**Word count target:** 400–700 words

**Required sections:**
1. Title + tagline (mirror cover badge)
2. What's inside (12 chapters listed; mention bonuses)
3. Who it's for (5 personas from frontmatter)
4. Author credibility (1 paragraph + receipts: $67.99 article, $17–$92 monthly)
5. License (personal+commercial use, no resale of pack)
6. Updates policy (free email update for buyers when MPP rules change)

**Step 1-4:** Standard pattern (no blank-line trick needed since not part of master MD).

Commit: `docs(medium-income): buyer-facing README`

---

### Task 29: Write `HOW-TO-USE.md`

**Files:**
- Create: `products/medium-income/HOW-TO-USE.md`

**Word count target:** 300–500 words

**Required content:**
1. The 14-day quickstart (link to Ch 6 in main book + bonus calendar)
2. How to use the bonus templates (markdown files = open in any editor; PDFs = print or annotate)
3. Where to leave a Gumroad rating
4. Where to follow the author for updates (Medium @luffyselah, jrdevhub.com newsletter)

Commit: `docs(medium-income): HOW-TO-USE quickstart`

---

### Task 30: Write `gumroad-listing.md`

**Files:**
- Create: `products/medium-income/gumroad-listing.md`

**Word count target:** 600–900 words

**Required sections (these go directly into the Gumroad listing UI):**
1. Product name: `Medium Income 2026: The Beginner's Playbook`
2. Tagline (under 150 chars): `From zero stories to your first $100 on Medium — updated for the 2026 Partner Program. 100+ countries supported.`
3. Description body (markdown allowed in Gumroad; structure: hook paragraph → "What you'll learn" bulleted list of 12 outcomes → "What's inside" listing chapters + bonuses → "Who it's for" → "What this is NOT" → author credibility paragraph with receipts → final CTA)
4. 5 FAQ entries (Gumroad has FAQ field): "Will this work outside the US?", "Do I need a Medium Pro membership to apply?", "How is this different from free Medium guides?", "What if MPP rules change after I buy?", "Do I get the source markdown files too?"
5. Cover image filename reference: `cover.png`
6. Refund policy: 14-day money-back, no questions asked

Commit: `docs(medium-income): gumroad listing copy`

---

## Phase 11: Final QA

### Task 31: Final verification + ZIP rebuild + CLAUDE.md update

**Step 1: Re-build master MD, HTML, PDF, ZIP in correct order**

```bash
cd products/medium-income
# Re-assemble (in case any chapter was edited after Task 21)
/usr/bin/python3 -c "
from pathlib import Path
chunks=[f.read_text().rstrip('\n')+'\n\n' for f in sorted(Path('src').glob('*.md'))]
Path('medium-income.md').write_text(''.join(chunks))
"
# Re-render HTML
pandoc medium-income.md --standalone --metadata title="Medium Income 2026" --metadata author="Jeri P.M." -H header.html -o medium-income.html
# Re-print PDF
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --no-sandbox --print-to-pdf="$PWD/medium-income.pdf" --no-pdf-header-footer "file://$PWD/medium-income.html"
# Re-zip
rm -f medium-income.zip
zip -rq medium-income.zip medium-income.md medium-income.pdf medium-income.html README.md HOW-TO-USE.md src/ images/ bonuses/ -x "*.DS_Store"
```

**Step 2: Final stat check**

```bash
echo "PDF page count:"
mdls -name kMDItemNumberOfPages medium-income.pdf 2>/dev/null | awk '{print $3}'
echo "Total word count (master MD):"
wc -w medium-income.md
echo "Chapter heading count:"
grep -cE '^## [0-9]+ —' medium-income.md
echo "Image count in master MD:"
grep -c '!\[' medium-income.md
echo "ZIP size + file count:"
ls -lh medium-income.zip
unzip -l medium-income.zip | tail -1
```
Expected: 100 ≤ pages ≤ 130; 18,000 ≤ words ≤ 26,000; 12 chapter headings; ≥ 7 images; 3–6 MB ZIP; ≥ 27 files.

**Step 3: Update `CLAUDE.md` with the real Gumroad URL placeholder kept**

Already done in Task 0.3 — verify entry still present:
```bash
grep -A1 "Medium Income 2026" CLAUDE.md
```

**Step 4: Final commit**

```bash
git add products/medium-income/
git commit -m "build(medium-income): final QA pass — regen MD/HTML/PDF/ZIP"
```

**Step 5: Print launch checklist for the user**

Echo this to user after Task 31:
- Upload `medium-income.zip` and `cover.png` to Gumroad as a new product at $19
- Set product slug, fill in `gumroad-listing.md` content, paste 5 FAQs
- Update `CLAUDE.md` Gumroad list with the real Gumroad URL
- Tweet thread from @luffyselah (Profile 10), under 277 chars per tweet
- Cross-link from existing Gumroad products
- Add to jrdevhub.com sidebar/footer
- Add bottom CTA to all existing Blogger articles

---

## Verification matrix (run before declaring done)

| Check | Command | Expected |
|-------|---------|----------|
| All 14 src files present | `ls products/medium-income/src/ | wc -l` | 14 |
| All 7 images present | `ls products/medium-income/images/ | wc -l` | 7 |
| All 5 bonus files present | `ls products/medium-income/bonuses/ | wc -l` | 5 (4 md/html + 1 pdf, plus stripe-checklist.md = 6 if intermediate kept) |
| Master MD assembled | `wc -w products/medium-income/medium-income.md` | 18000–26000 |
| HTML renders | `grep -c '<h2 id=' products/medium-income/medium-income.html` | ≥ 15 |
| TOC slugs match | (Task 23 script) | all 12 OK |
| PDF renders | `ls -lh products/medium-income/medium-income.pdf` | 2–4 MB |
| Cover renders | `sips … cover.png` | 2560×3200 |
| ZIP packaged | `unzip -l … \| tail -1` | ≥ 27 files |
| README + HOW-TO + listing exist | `ls products/medium-income/*.md` | 4 files |

---

## Skills referenced

- `superpowers:executing-plans` — sub-skill for executing this plan task-by-task (REQUIRED)
- `superpowers:test-driven-development` — adapted: "test" = verification command per task
- `superpowers:verification-before-completion` — REQUIRED before claiming any task complete; run the verify step and confirm output before committing
