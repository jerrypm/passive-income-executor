# Opportunity Scan — 2026-05-24

> Daily run by the business-coworker scheduled task. Focus: opportunities that fit Jeri's iOS/Swift + web/Python stack and complement (not duplicate) the existing Nostr-DVM + Ollama-paywall + Blogger + Gumroad infrastructure already in `docs/plans/`.
>
> Today's filter: **fastest path to revenue × highest leverage on existing assets × low maintenance once live.**

---

## TL;DR — what to do this week

1. **Ship a Foundation Models micro-app in 7 days** (highest-leverage NEW opening — see Opportunity #1).
2. **Publish a paid Claude Code MCP server to the marketplace** (leverages the Claude Code skill you already use daily — see Opportunity #2).
3. **List your first SwiftUI starter kit on Gumroad alongside the existing 7 products** (one-day extraction from any project you already have — see Opportunity #3).
4. **Open one Toptal + one Contra profile this weekend** (asynchronous; pays for everything else — see Opportunity #4).

Everything below is *additive* to the existing 4-phase plan, not a replacement.

---

## Opportunity #1 — Foundation Models niche app on iOS 26

**Why now (May 2026):** Apple's Foundation Models framework went GA with iOS 26 in Sept 2025. The ~3B parameter on-device LLM is **free to call, runs offline, and zero infra cost**. Most indie devs are still building OpenAI-wrapper apps that pay $0.002–$0.02 per request and get commoditized; an FM-native app has **0 API cost forever** and a privacy story Apple themselves market in keynotes. Apple is currently surfacing FM apps in App Store editorial.

**Pick one of these "high-frustration / low-supply" niches** (RevenueCat 2026 + NichesHunter data):

| Niche | App Store sentiment | Typical MRR range |
|---|---|---|
| ADHD focus / body-doubling | 56.8% negative reviews on incumbents | $2K–$8K |
| Migraine tracker | High frustration, weak SwiftUI competitors | $2K–$6K |
| Freelance time tracker (per-profession) | 56.8% productivity dissatisfaction | $5K–$15K |
| Meeting-note taker (on-device, privacy-first) | New, FM enables it without server | $5K–$20K |
| Meditation timer (just-works) | 86.1% frustration on incumbents | $2K–$5K |

**The wedge:** "Works fully offline. Your data never leaves your iPhone. Powered by Apple Intelligence." That single tagline is unbeatable by any OpenAI wrapper.

**Action steps (1 week sprint):**
- Day 1: Pick the niche. Read top 30 1-star reviews of the top 3 incumbents in App Store Connect. Write a one-paragraph wedge.
- Day 2–3: Build SwiftUI MVP. Use `LanguageModelSession` (Foundation Models framework — covered in dev.to / Apple docs below).
- Day 4: Wire RevenueCat (free up to $2.5K/mo) + Superwall (free) for paywall A/B.
- Day 5: Record 30-sec demo video for the App Store listing.
- Day 6: Submit to App Store review. Post-build content for Twitter (Profile 10) + dev.to teaser.
- Day 7: Launch on Product Hunt + r/iOSProgramming + Nostr (link to it from `nak event`).

**Pricing:** $4.99/mo or $29.99/yr with 7-day free trial. RevenueCat 2026 data shows annual emphasis converts best.

| | |
|---|---|
| Difficulty | Medium |
| Earning potential | $500–$10K MRR within 6 mo |
| Time to first revenue | 7–14 days (post-review) |
| Risks | App Store rejection (mitigate: don't promise medical advice); slow organic growth |
| Advantages | Zero AI infra cost • Apple actively features FM apps • Real moat vs GPT wrappers |
| Tools needed | Xcode 26 • RevenueCat • Superwall • App Store Connect ($99/yr — already paid) |

---

## Opportunity #2 — Paid Claude Code MCP server / plugin

**Why now:** The Claude Code marketplace hit **170,000 dev visits/month** and the public MCP catalog grew from a few dozen at start of 2025 to **500+ servers** by April 2026. Stripe, Notion, Cloudflare, Slack, and Vercel all shipped official servers. Companies (CodeRabbit, Airtable, 1inch, IdeaBrowser, AppSignal, Kryven, kone.vc) are already running paid ads to this audience — which proves both demand and willingness to pay.

You already use Claude Code daily and have shipped MCP-adjacent stuff (DVMCP is on your radar from `docs/plans/`). You're 2 days from a published plugin.

**Three angles, pick one this week:**

1. **`mcp-ios-developer`** — Swift/Xcode commands as MCP tools (run `xcrun simctl`, parse `.xcodeproj`, query App Store Connect API for sales, generate Fastlane lanes). Sell at $29 one-time on Gumroad + free tier on the marketplace for distribution.
2. **`mcp-gumroad`** — query your own (and customers') Gumroad sales, list products, draft new product descriptions. Recurring revenue via Stripe ($9/mo per seat).
3. **`mcp-blogger-autopost`** — wrap your existing `post_to_blogger.py` as an MCP tool so anyone using Claude Code can publish to Blogger. One-time $19 + free in your marketplace as a lead magnet.

**Action steps:**
- Read `code.claude.com/docs/en/mcp` (Anthropic docs — link below).
- Scaffold with `npx create-mcp-server` (TypeScript) or use the Python SDK.
- Publish to your *own* marketplace (claudemarketplaces.com lists private marketplaces) so you control distribution + paywall.
- Cross-list on `claudemarketplaces.com` (free listing, big inbound traffic).
- Write a "Why I built X" article on dev.to + Hashnode + your jrdevhub.com (you already have the autoposter).

| | |
|---|---|
| Difficulty | Easy–Medium |
| Earning potential | $200–$3K/mo per plugin (compounds with portfolio) |
| Time to first revenue | 3–7 days |
| Risks | Crowded marketplace — must pick a real niche, not a generic wrapper |
| Advantages | You ARE the target customer • Existing audience on Twitter/Nostr/Blogger • Same SDK = ship 5 of them in a month |
| Tools needed | Node.js or Python (both already installed) • Gumroad (already in use) • claudemarketplaces.com |

---

## Opportunity #3 — SwiftUI starter kit on Gumroad (extract, don't build)

**Why now:** TheSwiftKit, iosapptemplates.com, and CodeCanyon all sell SwiftUI boilerplates as their lead products. Top Gumroad sellers in this category report **$5K–$50K/mo** from template bundles. Your Gumroad store already has 7 products and an audience — adding an 8th has zero new-store cost.

**The trick:** don't *build* a starter kit. **Extract** one from work you've already done. Any iOS side project that has Sign-in-with-Apple + paywall + onboarding + dark mode = a $29–$79 product.

**Action steps:**
- Pick the most polished iOS project in your archive. Strip it to a generic shell (replace branding, remove business logic).
- Add a 5-page README.md, 30-sec Loom walkthrough, screenshots for the Gumroad listing.
- Price tiers: **$29 personal**, **$79 team (5-seat)**, **$199 lifetime + future updates**.
- Bundle it with "Ollama API Monetizer" + "Nostr AI Toolkit" as a "Solo Dev Stack" ($49 — bundling lifts AOV ~40%).
- Push via: dev.to article (already automated), one Twitter thread from Profile 10, one Nostr long-form on Habla.

| | |
|---|---|
| Difficulty | Easy |
| Earning potential | $100–$3K/mo per kit • compounds with bundle |
| Time to first revenue | 1–3 days |
| Risks | Low-quality kit gets refund requests — invest in the README and one screencast |
| Advantages | Store + audience exist • Zero new tooling • Cross-promotes existing products |
| Tools needed | Xcode • Gumroad (existing) • Loom or QuickTime • 1 evening |

---

## Opportunity #4 — High-rate remote iOS contracts (income floor)

**Why now:** ZipRecruiter shows 8,802 remote iOS roles as of Feb 2026; median contract rate **$58.70/hr**, SwiftUI front-end contracts **$90–$140/hr**, and Toptal-tier roles **$60–$200/hr** with 0% platform cut. Indonesian timezone is actually an advantage for US-EU async teams.

**Why it matters for the portfolio:** it pays cash *now* while the passive streams compound. Treat 10–20 hrs/week as the "stable floor" funding everything else.

**Action steps (this weekend):**
- Open Toptal application (3% acceptance — your iOS depth qualifies). Schedule the live coding test for next week.
- Open Contra profile (0% fee, much faster onboarding). Copy your Toptal portfolio over.
- Open Arc.dev profile (Swift remote board). One profile = 3 inbound channels.
- Set rate floor at **$70/hr**. Don't anchor low — Indonesian devs leaving rate on the table is the #1 mistake.
- Write 3 case-study one-pagers (one per past app). One of them becomes your Toptal pitch.

| | |
|---|---|
| Difficulty | Medium (Toptal vetting is real) |
| Earning potential | $5K–$15K/mo at 20 hrs/wk |
| Time to first revenue | 2–6 weeks |
| Risks | Trading time for money (no leverage) — use *only* as funding for #1–#3 |
| Advantages | Predictable cash • Forces portfolio polish • US clients trust Toptal-vetted devs |
| Tools needed | Toptal, Contra, Arc.dev profiles • LinkedIn refresh • 3 case studies |

---

## Opportunity #5 — Done-for-you AI agent for SMBs (high-margin services)

**Why now:** Solo operators running AI-agency setups report **$10K–$30K/mo** with ~80% AI automation. Typical deal structure: **$2K setup + $200/mo maintenance**, sold as "replaces 10 hrs/wk of admin labor." Indonesian SMBs + Bali expat businesses are an underserved local market.

**Three productized offers to pick from:**

1. **"WhatsApp AI receptionist"** for clinics, salons, café — Ollama + Twilio + Google Calendar. Setup $500, $99/mo.
2. **"Invoice + expense triage agent"** for freelancers — reads Gmail, categorizes, drafts in spreadsheets. $2K setup, $200/mo.
3. **"Content repurposer"** for local creators — long-form blog → 7 tweets + 3 IG captions + LinkedIn. $1K setup, $149/mo.

**Action steps:**
- Pick one. Build the demo on yourself (you already have Ollama, Blogger, Twitter Profile 10).
- Record the 90-sec demo. Post to LinkedIn + Indonesian indie founder Telegram groups + Bali Facebook groups.
- DM 20 local businesses with a personalized 1-minute Loom. Conversion ~5% = 1 client = $500–$2K.

| | |
|---|---|
| Difficulty | Medium |
| Earning potential | $1K–$10K/mo from 5–10 clients |
| Time to first revenue | 2–4 weeks |
| Risks | Services scale with time — productize hard or it eats your week |
| Advantages | High margins (80%+) • You already have Ollama + automation stack |
| Tools needed | Ollama (installed) • n8n or LangChain • Loom • Stripe/PayPal • Telegram outreach |

---

## Opportunity #6 — visionOS niche app (asymmetric bet)

**Why now:** Only **~4,200 visionOS apps** as of Q1 2026 (vs ~2M iOS). Premium tier of users with high willingness-to-pay; less competition; Apple actively features new spatial apps. Most iOS devs ignore it — that's the entire opportunity.

**Pick one:**
- **Spatial meditation environments** (paid one-time, $19.99)
- **AR fitness coaching with on-device pose detection** (subscription)
- **Virtual landmark/museum tour** for Indonesian tourism market (paid + IAP)

This is the speculative line on the portfolio — lower P(success) but higher payout if Apple features you in the Vision Pro Store.

| | |
|---|---|
| Difficulty | Medium–Hard (RealityKit learning curve) |
| Earning potential | $500–$8K/mo if featured |
| Time to first revenue | 4–8 weeks |
| Risks | Vision Pro install base still small in 2026 |
| Advantages | Almost no indie competition • Apple-featuring pipeline open • Premium pricing |
| Tools needed | Xcode 26 • Reality Composer Pro • Vision Pro simulator |

---

## Portfolio prioritization for the next 30 days

| Stream | Hours/week | Expected $/mo by Sept 2026 |
|---|---|---|
| #1 Foundation Models app | 15 (week 1), then 5 maintenance | $500–$3K |
| #2 Claude Code MCP plugin | 8 (week 2) | $200–$1.5K |
| #3 SwiftUI starter kit on Gumroad | 4 (week 3) | $200–$1K |
| #4 Toptal/Contra freelance | 20 ongoing | $5K–$12K |
| Existing Nostr/Ollama plan | 5 maintenance | $90–$200 (per plan) |
| Existing Blogger + Gumroad catalog | 3 maintenance | $200–$800 (per plan) |
| **Realistic 90-day total** |  | **$6K–$18K/mo** |

This **doubles** the original Part-1/2 estimate of $810–$2,375/mo because the iOS subscription app + Toptal contract are higher-leverage than the platform-grind streams in the original plan.

---

## What I'd skip this month

- **Vibe-coded micro-SaaS** (Replit/Lovable/Bolt) — the market is now saturated; median MRR is $1.2K and falling. Your iOS edge is wasted here.
- **YouTube Shorts pipeline** in `videos/ready/` — only ship if you've already batched 30+. Otherwise it's a content-mill trap.
- **Crypto staking** (Phase 3 in plan) — fine to delay until any of #1–#5 is profitable; the opportunity cost of capital is real.

---

## Notes for tomorrow's run

- Check whether the Foundation Models app got submitted (look in `scripts/ios/` or wherever you set up).
- Pull latest Gumroad sales for products 1–7 and log to `logs/earnings.md`.
- Re-search "Claude Code plugin marketplace top sellers" — that ranking shifts weekly.
- Watch for WWDC 2026 announcements (mid-June) — new framework drops = new wedges.

---

## Sources

- [iOS Swift Remote Jobs Hiring Now Feb 2026 — ZipRecruiter](https://www.ziprecruiter.com/Jobs/Ios-Contract-Remote)
- [Remote Swift Jobs May 2026 — Arc.dev](https://arc.dev/remote-jobs/swift)
- [Toptal Freelance Swift Developer Jobs Apr 2026](https://www.toptal.com/freelance-jobs/developers/swift)
- [Upwork Alternatives 2026 — Jobbers](https://www.jobbers.io/upwork-alternatives-15-platforms-compared-2026/)
- [Best Micro SaaS Ideas for Solopreneurs 2026 — Superframeworks](https://superframeworks.com/articles/best-micro-saas-ideas-solopreneurs)
- [50 Micro SaaS Ideas for 2026 With Revenue Data — NxCode](https://www.nxcode.io/resources/news/micro-saas-ideas-2026)
- [Mobile App Economy 2026: Monetisation, AI & Foldables — Foresight Mobile](https://foresightmobile.com/blog/mobile-app-economy-2026-monetisation-ai-foldables)
- [Apple made roughly $900M from generative AI apps in 2025 — 9to5Mac](https://9to5mac.com/2026/03/19/report-apple-made-roughly-900m-from-generative-ai-apps-in-2025/)
- [State of Subscription Apps 2026 — RevenueCat](https://www.revenuecat.com/state-of-subscription-apps/)
- [RevenueCat vs Adapty vs Superwall 2026 — PkgPulse](https://www.pkgpulse.com/guides/revenuecat-vs-adapty-vs-superwall-mobile-in-app-2026)
- [How to make money on the visionOS App Store — RevenueCat](https://www.revenuecat.com/blog/growth/how-to-make-money-on-the-visionos-app-store/)
- [48 Profitable App Niches in 2026 Ranked by Revenue — NichesHunter](https://nicheshunter.app/blog/profitable-app-niches-2026)
- [Claude Code Plugins, Skills, MCP Servers & Marketplace Directory](https://claudemarketplaces.com/)
- [Claude Code MCP Servers & Plugins: Complete 2026 Guide — Clarista](https://www.clarista.io/blog/claude-code-mcp-plugins-guide)
- [The 15 MCP Servers Worth Wiring Into Claude Code and Cursor 2026 — Codersera](https://codersera.com/blog/best-mcp-servers-claude-code-cursor-2026/)
- [Connect Claude Code to tools via MCP — Anthropic Docs](https://code.claude.com/docs/en/mcp)
- [The Swift Kit — Best SwiftUI Boilerplate 2026](https://theswiftk.it.com/)
- [31+ Premium Swift App Templates — iOS App Templates](https://iosapptemplates.com/)
- [Apple Foundation Models framework brings on-device AI to third-party apps — Cult of Mac](https://www.cultofmac.com/news/apple-foundation-models-framework)
- [Apple's Foundation Models Framework: Run AI On-Device With Just a Few Lines of Swift — dev.to](https://dev.to/arshtechpro/apples-foundation-models-framework-run-ai-on-device-with-just-a-few-lines-of-swift-lbp)
- [How to Make Money with Vibe Coding in 2026 — claw.mobile](https://claw.mobile/blog/make-money-vibe-coding-2026)
- [Vibe Coding Hits a Tipping Point 2026 — Superframeworks](https://superframeworks.com/articles/vibe-coding-tipping-point-what-founders-need-to-know)
