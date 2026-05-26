# Opportunity Scout — 2026-05-25

**Coworker for:** Jeri (iOS dev, Indonesia) — @luffyselah / jrdevhub.com
**Filter:** Things you do NOT already have in `docs/plans/` (Nostr DVM, Ollama paywall, LNbits, staking, money4band, Blogger auto-post, current 7 Gumroad products).
**Mode:** Pick 1 — start this week. Don't queue all 6.

---

## TL;DR — Pick One Today

| # | Opportunity | Effort | First $ in | 6-mo realistic | Why now |
|---|---|---|---|---|---|
| 1 | **iOS 26 Liquid Glass component pack on Gumroad** | Easy | 1–2 weeks | $300–1,500/mo | Biggest visual reset since iOS 7. Almost no competition yet. |
| 2 | **Paid Claude Skills bundle on Agensi / SkillsMP** | Easy | 1 week | $200–2,000/mo | Anthropic open-sourced spec Dec 2025. OpenAI / Codex now use same format. You already build skills. |
| 3 | **Monetized MCP server on MCPize** | Easy–Med | 2 weeks | $100–800/mo | 11,000+ MCP servers, <5% monetized. 85% rev share + Stripe. |
| 4 | **Telegram TON mini-app (iOS-skill adjacent)** | Medium | 3–4 weeks | $200–3,000/mo | CAC 90–95% lower than App Store. Still the early-mover window. |
| 5 | **Niche subscription iOS app — Lifestyle / Finance / Health** | Hard | 2–3 months | $0 or $500–5,000/mo | Hybrid monetization + hard paywall = 10.7% trial-to-paid (5x freemium). |
| 6 | **Apple Intelligence menu-bar Mac app** | Medium | 4–6 weeks | $200–1,500/mo | On-device AI = no API cost. Recurring sub. |

**Coach pick for THIS WEEK:** #1 + #2 in parallel. Both ship in days, both stack on Gumroad infra you already run, both build authority for the rest of your funnel.

---

## 1. iOS 26 Liquid Glass Component Pack (HIGHEST LEVERAGE)

**What it is:** A polished SwiftUI component library / starter kit for the new Liquid Glass design language (iOS 26 / visionOS 26). Sell on Gumroad — same flow as your current 7 products.

**Why now:**
- iOS 26's Liquid Glass is the biggest visual paradigm shift since iOS 7 (2013). Every indie has to re-learn it.
- Apple's docs cover the basics; nobody covers edge cases (accessibility, performance, fallback for iOS 25 and below, custom shapes, dark mode tinting).
- One competitor on Gumroad right now (modernwebseo). That's it.
- Compiles into a Claude Skill too — bundle later for product #2.

**What to ship (MVP, 1 weekend):**
- 12–15 Liquid Glass components (card, button, sheet, tab bar, nav bar, search field, segmented control, alert, toast, menu, slider, toggle, badge, list row, modal).
- One demo app showing them all.
- README with copy-paste install (Swift Package Manager).
- 30-page PDF: "Liquid Glass field guide" — when to use, when NOT to use, accessibility gotchas, performance numbers.

**Pricing:** $29 launch → $49 standard. Bundle later w/ your Mastering Claude Code ebook for $59.

**Tools needed:** Xcode 26, your existing Gumroad account, your Blogger for launch post (`jrdevhub.com`), Twitter @luffyselah for launch thread.

**Risks:**
- Apple might ship "official" templates in Q3 2026 WWDC follow-up. Mitigation: ship in <2 weeks.
- Pirated copies. Mitigation: pay-what-you-want tier for goodwill, license-only update channel.

**Advantages:**
- Stacks on infra you already have (Gumroad, Blogger, Twitter).
- You're an iOS dev — natural authority.
- Cross-promotes every other Gumroad product.

**Action steps (do this week):**
1. `xcode-select --install` → confirm Xcode 26 installed.
2. Create repo `liquid-glass-kit` in this workspace.
3. Pull these 2 references: `github.com/conorluddy/LiquidGlassReference`, `github.com/mertozseven/LiquidGlassSwiftUI`.
4. Build 5 components Friday, 5 Saturday, 5 Sunday.
5. Record 30s demo on iPhone simulator, post to Twitter Monday.
6. Gumroad listing live by Tuesday.
7. Launch post on `jrdevhub.com` (use your `post_to_blogger.py` script).

---

## 2. Paid Claude Skills Bundle on Agensi / SkillsMP

**What it is:** Package SKILL.md skills as a paid bundle. You already have the `1000 Expert Prompts` product — extend the idea to Claude Code skills, which are now an open spec adopted by OpenAI Codex and ChatGPT (Dec 2025).

**Market data:**
- Agensi: 80% rev share to creator, Stripe Connect instant payout, $5–$25/skill.
- Top individual skills earn $500–$3,000/mo.
- Median skill earns <$50/mo → revenue concentrated in top 10%. Domain-specific skills win.

**Bundle ideas tailored to YOU:**
- **"iOS App Store Submission Toolkit"** — skills for ASO copy, screenshot generation, App Privacy report, TestFlight tester invite, version bump + changelog, Fastlane lane templates. ($19)
- **"Blogger Auto-Post Pro"** — your existing `post_to_blogger.py` flow as a polished installable skill. ($14)
- **"Gumroad Listing Optimizer"** — skill that takes a markdown brief and outputs Gumroad title, description, SEO tags, cover image prompt for AI. ($9)
- **"SwiftUI Refactor Sensei"** — skill that audits SwiftUI files for ViewBuilder antipatterns, modifier order, performance. ($25)

**Where to list:**
- Primary: Agensi (`agensi.io`)
- Secondary: SkillsMP (`skillsmp.com`)
- Discovery: `claudemarketplaces.com`
- Free tier: GitHub repo with permissive license on one skill → upsell to full bundle.

**Tools needed:** Your existing skill-creator workflow, Stripe Connect account (Indonesia → use Stripe Atlas later if blocked, or Wise + Stripe Express).

**Risks:** Stripe availability in Indonesia is the only real blocker — check today; if blocked, use Gumroad as fallback (same as your other products).

**First action:** Pick ONE bundle, draft the SKILL.md, ship by Friday.

---

## 3. Monetized MCP Server on MCPize

**What it is:** An MCP server that does something useful for AI agents, paywalled by MCPize. 85% revenue share + automatic Stripe billing.

**Stats:** 11,000+ MCP servers exist, <5% are monetized. 8M downloads, 85% MoM growth.

**Server ideas tailored to YOU:**
- **`mcp-appstore-meta`** — query App Store ranks, screenshots, reviews, competitor analysis. Pay-per-call.
- **`mcp-tradingview-screener`** — wrap TradingView's public screener API. Crypto / stock agents need this constantly.
- **`mcp-blogger-publisher`** — your `post_to_blogger.py` as MCP. Anyone running an agent that writes blog posts is a customer.
- **`mcp-indonesia-data`** — BPS statistics, Bank Indonesia rates, KRL schedules, BMKG weather. Niche but uncontested, and you have the local context advantage.

**Pricing models on MCPize:** per-call ($0.001–$0.10), monthly subscription ($5–$29), or hybrid.

**Risks:** MCP adoption could plateau. Mitigation: pick a server idea where the underlying data has value even outside MCP (you can sell it as a REST API on RapidAPI in parallel).

**Tools needed:** Python or Node, MCPize account, Stripe.

---

## 4. Telegram TON Mini-App

**What it is:** Web app served inside Telegram, monetized with Stars / ads / TON. 1B+ MAU. CAC is 90–95% lower than App Store.

**Why this fits you:**
- It's literally a web app — your web dev skills apply directly.
- Telegram payments are built-in; no Apple 30% tax.
- The 2024–2026 tap-to-earn craze is over, but utility apps are the next wave and there is much less noise.

**Niche app ideas:**
- **iOS dev tools in Telegram** — Bundle ID checker, ASO keyword density, screenshot resizer, App Store URL → metadata.
- **AI image utilities** — background remove, upscale, style transfer (paid via Stars). Backend = your Ollama on Mac mini.
- **Indonesian niche** — KRL Commuter Line schedule + Gojek/Grab fare estimator (Telegram is huge in Indonesia).

**Monetization mix:** Stars for digital goods, ads at $0.35–0.50 CPM, TON jetton tokens for power users.

**Tools needed:** Node.js or Next.js, `@telegram-apps/sdk`, Telegram Bot API, TON wallet.

**Risk:** Telegram could change the rules. Mitigation: keep the actual product web-accessible so you can pivot to standalone PWA.

---

## 5. Subscription iOS App — Lifestyle / Finance / Health

**Market reality check from RevenueCat 2026 report:**
- Top 1% of apps capture 90%+ of revenue. Top 100 subscription apps = 81% of all sub revenue.
- BUT — top 25% of subscription apps grew MRR by 80%+ YoY. Bottom 25% shrank 33%+.
- Hard paywall trial-to-paid: **10.7%** vs freemium **2.1%**.
- Hybrid monetization (ads + IAP + sub) used by 60% of top grossers.

**Best niches (RevenueCat revenue/competition multiplier):**
- Lifestyle: 0.90x (habit, journal, home organization)
- Finance: 0.85x (budgeting, crypto portfolio, expense)
- Health & Fitness: 0.80x (meditation, posture, sleep, workout)
- Food & Drink: 0.70x

**Hook for you:** You already run Nostr / Lightning / staking infra. Build the only **Bitcoin + Nostr-native finance / habit / journal app on iOS**. Differentiation = built-in BTC over Lightning, zaps to journal entries, Nostr social proof, no email signup. Subscribe via Nostr Wallet Connect → no Apple cut on Bitcoin payments (test legal first).

**Risk:** AI apps churn 36% faster than non-AI. If you go AI route, design for retention from day 1 (streaks, social, lock-in data).

**Time to first $:** 2–3 months realistic. This is the medium-term bet, not the quick win.

---

## 6. Apple Intelligence Menu-Bar Mac App

**What it is:** Tiny Mac menu-bar utility using on-device Apple Intelligence (no API cost!) — sell at $4.99/mo or $39 one-time.

**Ideas:**
- **Clipboard Smart Paste** — auto-format pasted text (Markdown → plain, code → snippet, URL → title).
- **Screenshot Annotator with AI Alt-Text** — generates alt text from screenshots for accessibility, posts to Twitter directly.
- **Meeting Summarizer (Local)** — records system audio, transcribes with Whisper, summarizes with Apple Intelligence. Zero data leaves device — privacy angle for sales.

**Why this is leverage:** On-device AI = $0 marginal cost = pure margin. You skip the OpenAI / Anthropic per-call cost that's killing AI app margins right now.

**Tools needed:** Xcode 26, Apple Intelligence framework, Sparkle for updates, Paddle or Gumroad for billing (or Setapp later).

---

## Things I checked but DEFERRED for you

- **Farcaster Frames** — overlaps with your Nostr strategy. Stick with Nostr, you have momentum there.
- **Solana Mobile Seeker dApps** — Seeker phone shipped but install base still tiny. Revisit Q4 2026.
- **TikTok Shop Indonesia affiliate** — promising but consumes attention you need on Gumroad / blog. Add only if blog content slows.
- **GitHub Sponsors** — long-tail, only works if you open-source #1 (Liquid Glass kit free tier). Bundle as a future move.

---

## Recommended 7-Day Sprint

| Day | Action |
|---|---|
| Mon (today) | Pick Liquid Glass kit. Create repo `liquid-glass-kit/` in this workspace. Outline 15 components. |
| Tue | Build 5 components + demo app shell. |
| Wed | Build 5 more components. Draft Gumroad listing copy. |
| Thu | Build last 5. Record demo video (30s portrait, iPhone simulator). |
| Fri | Write 30-page Liquid Glass field guide PDF. Write SKILL.md version (= product #2 seed). |
| Sat | Gumroad listing live ($29 launch). Blog post via `post_to_blogger.py`. |
| Sun | Twitter launch thread (8 tweets, max 277 chars each — Profile 10 only). Submit to Indie Hackers. List skill on Agensi. |

**Earnings log:** Add target row to `logs/earnings.md` — "2026-06: Liquid Glass kit Gumroad — target $300."

---

## Sources

- [iOS 26 Liquid Glass UI Kit (Gumroad competitor)](https://modernwebseo.gumroad.com/l/ios-liquid-glass-ui-kit)
- [LiquidGlassReference (GitHub)](https://github.com/conorluddy/LiquidGlassReference)
- [LiquidGlassSwiftUI Sample (GitHub)](https://github.com/mertozseven/LiquidGlassSwiftUI)
- [Donny Wals — Designing custom UI with Liquid Glass](https://www.donnywals.com/designing-custom-ui-with-liquid-glass-on-ios-26/)
- [visionOS Developer Overview](https://developer.apple.com/visionos/)
- [How to Monetize Your MCP Server](https://mcpize.com/developers/monetize-mcp-servers)
- [MCP Server Monetization 2026](https://dev.to/namel/mcp-server-monetization-2026-1p2j)
- [MCP Servers Are the New SaaS (2026)](https://dev.to/krisying/mcp-servers-are-the-new-saas-how-im-monetizing-ai-tool-integrations-in-2026-2e9e)
- [Telegram Mini Apps 2026 Monetization Guide](https://merge.rocks/blog/telegram-mini-apps-2026-monetization-guide-how-to-earn-from-telegram-mini-apps)
- [How to Monetize a Telegram Mini App in 2026](https://omisoft.net/blog/how-to-monetize-telegram-mini-app/)
- [Claude Skills Marketplace — Agent37](https://www.agent37.com/blog/claude-skills-marketplace)
- [Sell Your AI Agent Skills — Agensi Guide](https://www.agensi.io/learn/agent-skills-marketplace-sell-your-skills)
- [How to Monetize SKILL.md Skills](https://www.agensi.io/learn/how-to-monetize-skill-md-skills-developer-guide-2026)
- [Claude Marketplaces Directory](https://claudemarketplaces.com/)
- [RevenueCat State of Subscription Apps 2026](https://www.revenuecat.com/state-of-subscription-apps/)
- [RevenueCat — Subscription benchmarks 2026](https://www.revenuecat.com/blog/growth/subscription-app-trends-benchmarks-2026/)
- [iOS App Revenue Data 2026](https://clonechart.io/blog/ios-app-revenue-data)
