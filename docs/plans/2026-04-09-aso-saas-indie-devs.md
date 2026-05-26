# ASO Copilot SaaS for Indie Devs — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Ship an AI-powered App Store Optimization copilot that audits an app listing (iOS or Play Store) and generates optimized title/description/keywords in under 60 seconds — positioned at $19/mo for indie devs, launched within 3 weeks.

**Architecture:** Next.js 14 App Router (Vercel) + Supabase (Auth + Postgres) + Anthropic Claude API for reasoning + iTunes Search API + Play Store public scraping. Payments via LemonSqueezy (Indonesia-friendly merchant-of-record). Marketing driven by digital-marketing-expert skill (Dev.to + Twitter + Product Hunt + IndieHackers + niche subreddits).

**Tech Stack:**
- Framework: Next.js 14 (App Router, TypeScript, RSC)
- UI: shadcn/ui + Tailwind CSS + lucide-react
- DB/Auth: Supabase (Postgres + Row Level Security)
- AI: `@anthropic-ai/sdk` (claude-sonnet-4-6, streaming)
- Payments: LemonSqueezy (webhooks + checkout)
- Scraping: iTunes Search API (free, official) + `google-play-scraper` (npm)
- Deploy: Vercel (Hobby for MVP, Pro after paying users)
- Email: Resend (transactional)
- Analytics: PostHog (free tier)
- Domain: `asocopilot.io` or `listinglens.ai` (pick during Phase 0)

**Why this beats existing tools:**
| Tool | Price | Problem |
|------|-------|---------|
| AppTweak | $83+/mo | Overpriced for indies |
| AppFollow | $69+/mo | Same |
| Mobile Action Lite | $15/mo | Tracking only, no AI generation |
| AstroASO | $9/mo | macOS app only, iOS only |
| Appfigures | $9.99/mo | Analytics, not AI copilot |
| **Us** | **$19/mo** | **AI audit + copy generation, cross-platform, web-first** |

**Revenue math (conservative):**
- Month 1: 20 users × $19 = **$380**
- Month 3: 80 users × $19 = **$1,520**
- Month 6: 200 users × $19 = **$3,800**
- Month 12: 500 users × $19 + agency upgrades = **$10K+**

**Non-goals (explicit YAGNI):**
- Real-time rank tracking (deferred — commodity feature)
- Competitor deep analytics dashboards
- Mobile native app
- Team/collab features
- Custom ML models (use Claude API exclusively)

---

## Phase 0 — Validation & Setup (Day 1-2)

### Task 0.1: Create isolated worktree

**Files:** N/A (git operation)

**Step 1:** Create worktree from master
```bash
cd /Users/jeripurnamamaulid/Documents/14_Web-projects/passive-income-executor
git worktree add -b feature/aso-copilot ../aso-copilot master
cd ../aso-copilot
```

**Step 2:** Verify isolation
```bash
pwd  # Expect: .../aso-copilot
git branch --show-current  # Expect: feature/aso-copilot
```

**Commit:** No commit yet (clean branch)

---

### Task 0.2: Domain + landing page validation

**Files:**
- Create: `apps/landing/index.html` (static, deploy to GitHub Pages first)
- Create: `apps/landing/style.css`

**Step 1:** Write ONE-page landing with waitlist form
```html
<!-- apps/landing/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ASO Copilot — AI App Store Optimizer for Indie Devs</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <main>
    <h1>Stop guessing. Optimize your app listing in 60 seconds.</h1>
    <p class="sub">AI audit + copy generation for iOS and Play Store. Built by an indie iOS dev. $19/mo.</p>
    <form id="waitlist" action="https://formspree.io/f/YOUR_ID" method="POST">
      <input type="email" name="email" placeholder="you@example.com" required />
      <button type="submit">Join waitlist (first 50 get lifetime 50% off)</button>
    </form>
    <section class="problem">
      <h2>Why?</h2>
      <ul>
        <li>AppTweak charges $83/mo — too much for a 2-app indie</li>
        <li>Existing cheap tools just track ranks. You still write listings yourself.</li>
        <li>Claude can audit + generate optimized copy in one shot.</li>
      </ul>
    </section>
  </main>
</body>
</html>
```

**Step 2:** Set up Formspree free account → paste form ID into HTML.

**Step 3:** Buy domain (use Namecheap or Porkbun, pick one from: `asocopilot.io`, `listinglens.ai`, `asolift.dev`). Budget: $10-15/year.

**Step 4:** Deploy landing to Vercel
```bash
cd apps/landing
npx vercel --prod
```
Expected: Public URL returned.

**Step 5:** Point domain via DNS.

**Step 6:** Validation outreach — send the URL to these channels TODAY:
- Tweet: "Building an AI ASO tool for indie devs — $19/mo vs AppTweak's $83. Waitlist: [URL]"
- r/iOSProgramming post: "Would you use this? $19/mo AI ASO copilot for indies"
- IndieHackers post: same
- DM 10 indie iOS devs you follow on Twitter

**Step 7:** Target: 20 waitlist signups in 48 hours before writing ANY code. If <5, reconsider.

**Commit:**
```bash
git add apps/landing/
git commit -m "feat: waitlist landing page for validation"
```

---

### Task 0.3: Project scaffold

**Files:**
- Create: `apps/web/` (Next.js app)
- Create: `package.json`, `pnpm-workspace.yaml` (monorepo)
- Create: `.env.example`

**Step 1:** Init monorepo root
```bash
cd /path/to/aso-copilot
pnpm init
```

**Step 2:** Create workspace file
```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
```

**Step 3:** Scaffold Next.js
```bash
mkdir -p apps && cd apps
pnpm create next-app@latest web --typescript --tailwind --app --src-dir --import-alias "@/*" --eslint --no-turbopack
cd web
```

**Step 4:** Install core deps
```bash
pnpm add @supabase/supabase-js @supabase/ssr @anthropic-ai/sdk google-play-scraper zod react-hook-form @hookform/resolvers lucide-react
pnpm add -D @types/node
```

**Step 5:** Install shadcn/ui
```bash
pnpm dlx shadcn@latest init -d
pnpm dlx shadcn@latest add button input card form label textarea toast sonner badge tabs dialog
```

**Step 6:** Create `.env.example`
```
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Anthropic
ANTHROPIC_API_KEY=

# LemonSqueezy (Phase 3)
LEMONSQUEEZY_API_KEY=
LEMONSQUEEZY_STORE_ID=
LEMONSQUEEZY_WEBHOOK_SECRET=

# Resend
RESEND_API_KEY=

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**Step 7:** Copy to `.env.local` and fill placeholders. Ensure `.env.local` is in `.gitignore`.

**Step 8:** Verify dev server
```bash
pnpm dev
```
Expected: `http://localhost:3000` loads with Next.js default.

**Commit:**
```bash
git add apps/web pnpm-workspace.yaml package.json
git commit -m "feat: scaffold Next.js 14 app with shadcn/ui and Supabase deps"
```

---

## Phase 1 — Scraping + Audit Core (Week 1)

### Task 1.1: iTunes Search API wrapper (TDD)

**Files:**
- Create: `apps/web/src/lib/stores/itunes.ts`
- Create: `apps/web/src/lib/stores/itunes.test.ts`
- Create: `apps/web/src/lib/stores/types.ts`

**Step 1:** Install vitest
```bash
cd apps/web
pnpm add -D vitest @vitest/ui
```

Add to `package.json`:
```json
"scripts": {
  "test": "vitest run",
  "test:watch": "vitest"
}
```

**Step 2:** Define shared types (`types.ts`)
```ts
// apps/web/src/lib/stores/types.ts
export type AppListing = {
  source: 'itunes' | 'play';
  appId: string;
  title: string;
  subtitle?: string;
  description: string;
  keywords?: string[];
  category: string;
  rating: number;
  reviewCount: number;
  version: string;
  developer: string;
  iconUrl: string;
  screenshots: string[];
  priceUSD: number;
  fetchedAt: string; // ISO
};

export class AppLookupError extends Error {
  constructor(message: string, public code: 'NOT_FOUND' | 'BAD_URL' | 'UPSTREAM') {
    super(message);
  }
}
```

**Step 3:** Write the failing test
```ts
// apps/web/src/lib/stores/itunes.test.ts
import { describe, it, expect } from 'vitest';
import { extractItunesIdFromUrl, fetchItunesApp } from './itunes';
import { AppLookupError } from './types';

describe('extractItunesIdFromUrl', () => {
  it('extracts id from standard URL', () => {
    const url = 'https://apps.apple.com/us/app/things-3/id904237743';
    expect(extractItunesIdFromUrl(url)).toBe('904237743');
  });

  it('throws BAD_URL on invalid input', () => {
    expect(() => extractItunesIdFromUrl('not a url')).toThrow(AppLookupError);
  });
});

describe('fetchItunesApp', () => {
  it('fetches a real app (integration)', async () => {
    const app = await fetchItunesApp('904237743');
    expect(app.source).toBe('itunes');
    expect(app.title.toLowerCase()).toContain('things');
    expect(app.description.length).toBeGreaterThan(50);
    expect(app.screenshots.length).toBeGreaterThan(0);
  }, 15000);
});
```

**Step 4:** Run test to verify fail
```bash
pnpm test src/lib/stores/itunes.test.ts
```
Expected: FAIL (module not found).

**Step 5:** Implement minimal wrapper
```ts
// apps/web/src/lib/stores/itunes.ts
import { AppListing, AppLookupError } from './types';

const ITUNES_SEARCH = 'https://itunes.apple.com/lookup';

export function extractItunesIdFromUrl(url: string): string {
  const match = url.match(/id(\d+)/);
  if (!match) throw new AppLookupError('Cannot find app id in URL', 'BAD_URL');
  return match[1];
}

export async function fetchItunesApp(appId: string): Promise<AppListing> {
  const res = await fetch(`${ITUNES_SEARCH}?id=${appId}&country=us`);
  if (!res.ok) throw new AppLookupError('Upstream error', 'UPSTREAM');
  const json = await res.json();
  if (!json.results?.length) throw new AppLookupError('App not found', 'NOT_FOUND');
  const r = json.results[0];
  return {
    source: 'itunes',
    appId: String(r.trackId),
    title: r.trackName,
    subtitle: r.trackCensoredName,
    description: r.description ?? '',
    category: r.primaryGenreName,
    rating: r.averageUserRating ?? 0,
    reviewCount: r.userRatingCount ?? 0,
    version: r.version,
    developer: r.artistName,
    iconUrl: r.artworkUrl512 ?? r.artworkUrl100,
    screenshots: r.screenshotUrls ?? [],
    priceUSD: r.price ?? 0,
    fetchedAt: new Date().toISOString(),
  };
}
```

**Step 6:** Run test
```bash
pnpm test src/lib/stores/itunes.test.ts
```
Expected: PASS.

**Step 7:** Commit
```bash
git add apps/web/src/lib/stores/ package.json
git commit -m "feat(stores): iTunes app lookup with TDD"
```

---

### Task 1.2: Play Store wrapper (TDD)

**Files:**
- Create: `apps/web/src/lib/stores/play.ts`
- Create: `apps/web/src/lib/stores/play.test.ts`

**Step 1:** Write failing test
```ts
// apps/web/src/lib/stores/play.test.ts
import { describe, it, expect } from 'vitest';
import { extractPlayIdFromUrl, fetchPlayApp } from './play';
import { AppLookupError } from './types';

describe('extractPlayIdFromUrl', () => {
  it('extracts package id', () => {
    const url = 'https://play.google.com/store/apps/details?id=com.whatsapp';
    expect(extractPlayIdFromUrl(url)).toBe('com.whatsapp');
  });
});

describe('fetchPlayApp', () => {
  it('fetches a real app', async () => {
    const app = await fetchPlayApp('com.whatsapp');
    expect(app.source).toBe('play');
    expect(app.title.toLowerCase()).toContain('whatsapp');
  }, 20000);
});
```

**Step 2:** Run — expect FAIL.

**Step 3:** Implement
```ts
// apps/web/src/lib/stores/play.ts
import gplay from 'google-play-scraper';
import { AppListing, AppLookupError } from './types';

export function extractPlayIdFromUrl(url: string): string {
  const match = url.match(/id=([^&]+)/);
  if (!match) throw new AppLookupError('Cannot find package id', 'BAD_URL');
  return match[1];
}

export async function fetchPlayApp(packageId: string): Promise<AppListing> {
  try {
    const r = await gplay.app({ appId: packageId, lang: 'en', country: 'us' });
    return {
      source: 'play',
      appId: r.appId,
      title: r.title,
      subtitle: r.summary,
      description: r.description ?? '',
      category: r.genre,
      rating: r.score ?? 0,
      reviewCount: r.reviews ?? 0,
      version: r.version ?? 'n/a',
      developer: r.developer,
      iconUrl: r.icon,
      screenshots: r.screenshots ?? [],
      priceUSD: r.price ?? 0,
      fetchedAt: new Date().toISOString(),
    };
  } catch (e) {
    throw new AppLookupError('Play lookup failed', 'NOT_FOUND');
  }
}
```

**Step 4:** Test — PASS.

**Step 5:** Commit
```bash
git add apps/web/src/lib/stores/play.ts apps/web/src/lib/stores/play.test.ts
git commit -m "feat(stores): Play Store app lookup"
```

---

### Task 1.3: Unified lookup entrypoint

**Files:**
- Create: `apps/web/src/lib/stores/index.ts`
- Create: `apps/web/src/lib/stores/index.test.ts`

**Step 1:** Test
```ts
// apps/web/src/lib/stores/index.test.ts
import { describe, it, expect } from 'vitest';
import { fetchAppFromUrl } from '.';

describe('fetchAppFromUrl', () => {
  it('routes iTunes URL', async () => {
    const app = await fetchAppFromUrl('https://apps.apple.com/us/app/things-3/id904237743');
    expect(app.source).toBe('itunes');
  }, 15000);

  it('routes Play URL', async () => {
    const app = await fetchAppFromUrl('https://play.google.com/store/apps/details?id=com.whatsapp');
    expect(app.source).toBe('play');
  }, 20000);
});
```

**Step 2:** Fail, then implement
```ts
// apps/web/src/lib/stores/index.ts
import { AppListing, AppLookupError } from './types';
import { extractItunesIdFromUrl, fetchItunesApp } from './itunes';
import { extractPlayIdFromUrl, fetchPlayApp } from './play';

export * from './types';

export async function fetchAppFromUrl(url: string): Promise<AppListing> {
  if (url.includes('apps.apple.com')) {
    return fetchItunesApp(extractItunesIdFromUrl(url));
  }
  if (url.includes('play.google.com')) {
    return fetchPlayApp(extractPlayIdFromUrl(url));
  }
  throw new AppLookupError('Unsupported store URL', 'BAD_URL');
}
```

**Step 3:** Test — PASS.

**Step 4:** Commit
```bash
git add apps/web/src/lib/stores/index.ts apps/web/src/lib/stores/index.test.ts
git commit -m "feat(stores): unified app lookup entrypoint"
```

---

### Task 1.4: Claude audit engine — design the prompt first

**Files:**
- Create: `apps/web/src/lib/audit/prompt.ts`
- Create: `apps/web/src/lib/audit/schema.ts`

**Step 1:** Define structured output schema with zod
```ts
// apps/web/src/lib/audit/schema.ts
import { z } from 'zod';

export const AuditReportSchema = z.object({
  overallScore: z.number().min(0).max(10),
  strengths: z.array(z.string()).max(5),
  criticalIssues: z.array(z.object({
    issue: z.string(),
    fix: z.string(),
    impact: z.enum(['high', 'medium', 'low']),
  })).max(5),
  keywords: z.object({
    primary: z.array(z.object({
      keyword: z.string(),
      volume: z.enum(['high', 'medium', 'low']),
      competition: z.enum(['high', 'medium', 'low']),
      use: z.string(),
    })).max(5),
    secondary: z.array(z.string()).max(10),
    longTail: z.array(z.string()).max(10),
  }),
  suggestedCopy: z.object({
    titleBefore: z.string(),
    titleAfter: z.string(),
    subtitleBefore: z.string().optional(),
    subtitleAfter: z.string().optional(),
    descriptionFirstLines: z.string(),
    promotionalText: z.string().optional(),
  }),
  screenshotTips: z.array(z.string()).max(5),
  actionItems: z.array(z.object({
    action: z.string(),
    priority: z.enum(['critical', 'high', 'medium', 'low']),
  })).max(10),
});

export type AuditReport = z.infer<typeof AuditReportSchema>;
```

**Step 2:** Write the prompt builder. Base it on the audit framework from the `digital-marketing-expert` skill.
```ts
// apps/web/src/lib/audit/prompt.ts
import { AppListing } from '@/lib/stores/types';

export function buildAuditPrompt(app: AppListing): string {
  const storeLabel = app.source === 'itunes' ? 'Apple App Store' : 'Google Play Store';
  const titleLimit = app.source === 'itunes' ? 30 : 50;
  const subtitleLimit = app.source === 'itunes' ? 30 : 80;

  return `You are an App Store Optimization (ASO) expert. Audit the following ${storeLabel} listing and produce a structured report.

## Listing
- Title (current): "${app.title}" (${app.title.length}/${titleLimit} chars)
- Subtitle: "${app.subtitle ?? ''}" (${(app.subtitle ?? '').length}/${subtitleLimit} chars)
- Category: ${app.category}
- Rating: ${app.rating}/5 from ${app.reviewCount} reviews
- Screenshots: ${app.screenshots.length}
- Developer: ${app.developer}
- Description (first 500 chars): "${app.description.slice(0, 500)}"

## Instructions
1. Score the listing overall 0-10 (10 = flawless).
2. List 3-5 concrete strengths.
3. Identify up to 5 critical issues, each with a specific fix and impact level.
4. Recommend keywords:
   - 3-5 primary (must-use in title/subtitle)
   - 5-10 secondary (description body)
   - 5-10 long-tail (for reviews, promotional text)
5. Generate NEW suggested copy:
   - Optimized title (respect ${titleLimit} char limit)
   - Optimized subtitle (respect ${subtitleLimit} char limit)
   - First 3 lines of description (hook + value prop + CTA)
6. 3-5 screenshot improvement tips.
7. Prioritized action list (up to 10 items).

## Output
Return ONLY valid JSON matching this shape (no markdown, no prose):
{
  "overallScore": number,
  "strengths": string[],
  "criticalIssues": [{"issue": string, "fix": string, "impact": "high"|"medium"|"low"}],
  "keywords": {
    "primary": [{"keyword": string, "volume": "high"|"medium"|"low", "competition": "high"|"medium"|"low", "use": string}],
    "secondary": string[],
    "longTail": string[]
  },
  "suggestedCopy": {
    "titleBefore": string,
    "titleAfter": string,
    "subtitleBefore": string,
    "subtitleAfter": string,
    "descriptionFirstLines": string,
    "promotionalText": string
  },
  "screenshotTips": string[],
  "actionItems": [{"action": string, "priority": "critical"|"high"|"medium"|"low"}]
}

Be specific. No generic advice. Every recommendation must be actionable.`;
}
```

**Step 3:** Commit
```bash
git add apps/web/src/lib/audit/
git commit -m "feat(audit): prompt builder + zod schema for audit reports"
```

---

### Task 1.5: Claude client + audit runner (TDD)

**Files:**
- Create: `apps/web/src/lib/audit/runner.ts`
- Create: `apps/web/src/lib/audit/runner.test.ts`

**Step 1:** Test
```ts
// apps/web/src/lib/audit/runner.test.ts
import { describe, it, expect } from 'vitest';
import { runAudit } from './runner';
import { AppListing } from '@/lib/stores/types';

const sampleApp: AppListing = {
  source: 'itunes',
  appId: '904237743',
  title: 'Things 3',
  subtitle: 'Task Manager & To-Do List',
  description: 'Things is the award-winning personal task manager...',
  category: 'Productivity',
  rating: 4.8,
  reviewCount: 12345,
  version: '3.0',
  developer: 'Cultured Code',
  iconUrl: '',
  screenshots: ['', '', '', ''],
  priceUSD: 9.99,
  fetchedAt: new Date().toISOString(),
};

describe('runAudit', () => {
  it('returns a valid audit report from Claude', async () => {
    const report = await runAudit(sampleApp);
    expect(report.overallScore).toBeGreaterThanOrEqual(0);
    expect(report.overallScore).toBeLessThanOrEqual(10);
    expect(report.keywords.primary.length).toBeGreaterThan(0);
    expect(report.suggestedCopy.titleAfter.length).toBeGreaterThan(0);
  }, 60000);
});
```

**Step 2:** Run — FAIL.

**Step 3:** Implement runner
```ts
// apps/web/src/lib/audit/runner.ts
import Anthropic from '@anthropic-ai/sdk';
import { AppListing } from '@/lib/stores/types';
import { AuditReport, AuditReportSchema } from './schema';
import { buildAuditPrompt } from './prompt';

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY! });

export async function runAudit(app: AppListing): Promise<AuditReport> {
  const prompt = buildAuditPrompt(app);

  const msg = await client.messages.create({
    model: 'claude-sonnet-4-6',
    max_tokens: 4000,
    messages: [{ role: 'user', content: prompt }],
  });

  const text = msg.content
    .filter((b): b is Anthropic.TextBlock => b.type === 'text')
    .map((b) => b.text)
    .join('');

  const jsonMatch = text.match(/\{[\s\S]*\}/);
  if (!jsonMatch) throw new Error('No JSON in Claude response');

  const parsed = JSON.parse(jsonMatch[0]);
  return AuditReportSchema.parse(parsed);
}
```

**Step 4:** Run test (requires `ANTHROPIC_API_KEY` in `.env.local`)
```bash
pnpm test src/lib/audit/runner.test.ts
```
Expected: PASS (may take 30-60s).

**Step 5:** Commit
```bash
git add apps/web/src/lib/audit/runner.ts apps/web/src/lib/audit/runner.test.ts
git commit -m "feat(audit): Claude-powered audit runner with zod validation"
```

---

### Task 1.6: API route `/api/audit` (POST)

**Files:**
- Create: `apps/web/src/app/api/audit/route.ts`

**Step 1:** Implement with rate limit placeholder
```ts
// apps/web/src/app/api/audit/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { fetchAppFromUrl, AppLookupError } from '@/lib/stores';
import { runAudit } from '@/lib/audit/runner';

export const runtime = 'nodejs';
export const maxDuration = 60;

const BodySchema = z.object({
  url: z.string().url(),
});

export async function POST(req: NextRequest) {
  try {
    const body = BodySchema.parse(await req.json());
    const app = await fetchAppFromUrl(body.url);
    const report = await runAudit(app);
    return NextResponse.json({ app, report });
  } catch (e) {
    if (e instanceof AppLookupError) {
      return NextResponse.json({ error: e.message, code: e.code }, { status: 400 });
    }
    console.error(e);
    return NextResponse.json({ error: 'Internal error' }, { status: 500 });
  }
}
```

**Step 2:** Smoke test with curl
```bash
pnpm dev
# in another terminal:
curl -X POST http://localhost:3000/api/audit \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://apps.apple.com/us/app/things-3/id904237743"}'
```
Expected: JSON with `app` + `report`.

**Step 3:** Commit
```bash
git add apps/web/src/app/api/audit/route.ts
git commit -m "feat(api): /api/audit endpoint returns app + audit"
```

---

## Phase 2 — Dashboard + UX (Week 2)

### Task 2.1: Supabase schema + RLS

**Files:**
- Create: `supabase/migrations/0001_init.sql`

**Step 1:** Create Supabase project at supabase.com, copy URL + anon + service keys to `.env.local`.

**Step 2:** Write migration
```sql
-- supabase/migrations/0001_init.sql
create extension if not exists "uuid-ossp";

create table profiles (
  id uuid primary key references auth.users on delete cascade,
  email text not null,
  plan text not null default 'free' check (plan in ('free','pro','agency')),
  audits_used_this_month int not null default 0,
  current_period_end timestamptz,
  created_at timestamptz not null default now()
);

create table audits (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid not null references profiles(id) on delete cascade,
  source text not null check (source in ('itunes','play')),
  app_id text not null,
  app_title text not null,
  app_snapshot jsonb not null,
  report jsonb not null,
  created_at timestamptz not null default now()
);

create index audits_user_id_idx on audits (user_id, created_at desc);

alter table profiles enable row level security;
alter table audits enable row level security;

create policy "own profile" on profiles for all using (id = auth.uid());
create policy "own audits" on audits for all using (user_id = auth.uid());

-- Auto-create profile on signup
create function public.handle_new_user() returns trigger as $$
begin
  insert into public.profiles (id, email) values (new.id, new.email);
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();
```

**Step 3:** Push via Supabase CLI
```bash
pnpm dlx supabase link --project-ref <ref>
pnpm dlx supabase db push
```

**Step 4:** Commit
```bash
git add supabase/
git commit -m "feat(db): initial profiles + audits schema with RLS"
```

---

### Task 2.2: Supabase client + auth helpers

**Files:**
- Create: `apps/web/src/lib/supabase/client.ts`
- Create: `apps/web/src/lib/supabase/server.ts`
- Create: `apps/web/src/middleware.ts`

**Step 1:** Follow the `@supabase/ssr` docs exactly — copy the client/server/middleware templates from https://supabase.com/docs/guides/auth/server-side/nextjs. Adapt cookie handling to App Router.

**Step 2:** Test: visit `/` and cookies should be readable server-side.

**Step 3:** Commit
```bash
git add apps/web/src/lib/supabase apps/web/src/middleware.ts
git commit -m "feat(auth): Supabase SSR client + middleware"
```

---

### Task 2.3: Magic-link login page

**Files:**
- Create: `apps/web/src/app/(auth)/login/page.tsx`
- Create: `apps/web/src/app/(auth)/callback/route.ts`

**Step 1:** Login form using shadcn Form. Call `supabase.auth.signInWithOtp({ email, options: { emailRedirectTo } })`.

**Step 2:** Callback route exchanges code for session, redirects to `/dashboard`.

**Step 3:** Configure Resend as custom SMTP in Supabase Auth settings (better deliverability than default). Alternative: skip and use default Supabase email for MVP.

**Step 4:** Manual test: login → check email → click link → land on `/dashboard`.

**Step 5:** Commit
```bash
git add apps/web/src/app/\(auth\)/
git commit -m "feat(auth): magic-link login + callback"
```

---

### Task 2.4: Protected `/dashboard` with audit input

**Files:**
- Create: `apps/web/src/app/(app)/dashboard/page.tsx`
- Create: `apps/web/src/app/(app)/dashboard/audit-form.tsx`
- Create: `apps/web/src/app/(app)/layout.tsx`

**Step 1:** Layout redirects unauth users to `/login`.

**Step 2:** Dashboard page shows:
- Header with email + logout
- Audit input form (paste URL)
- List of past audits (from DB)
- Remaining quota badge

**Step 3:** `audit-form.tsx` — client component, `useState` + `fetch('/api/audit')`, shows loading skeleton, redirects to `/audits/[id]` on success (requires Task 2.5 to save).

**Step 4:** Smoke test end-to-end.

**Step 5:** Commit
```bash
git add apps/web/src/app/\(app\)/
git commit -m "feat(dashboard): audit input form + recent audits list"
```

---

### Task 2.5: Persist audit + quota check

**Files:**
- Modify: `apps/web/src/app/api/audit/route.ts`
- Create: `apps/web/src/lib/quota.ts`

**Step 1:** Quota helper
```ts
// apps/web/src/lib/quota.ts
const LIMITS = { free: 1, pro: 50, agency: 200 } as const;

export function getLimit(plan: string): number {
  return LIMITS[plan as keyof typeof LIMITS] ?? 0;
}
```

**Step 2:** Update API route
- Read user from Supabase SSR
- Return 401 if no user
- Read profile, check `audits_used_this_month < getLimit(plan)`
- Return 402 `{ error: 'quota_exceeded' }` if over
- After audit succeeds, insert into `audits` and increment counter
- Return `{ auditId, app, report }`

**Step 3:** Scheduled reset: create a daily cron (Vercel Cron) that resets `audits_used_this_month` on the 1st of each month. Or: track `current_period_end` and reset lazily on next request.

Lazy reset is simpler — do that:
```ts
if (profile.current_period_end && new Date(profile.current_period_end) < new Date()) {
  // reset
  await supabase.from('profiles').update({
    audits_used_this_month: 0,
    current_period_end: nextMonthISO(),
  }).eq('id', user.id);
}
```

**Step 4:** Manual test: 2nd audit on free plan → 402.

**Step 5:** Commit
```bash
git add apps/web/src/app/api/audit/route.ts apps/web/src/lib/quota.ts
git commit -m "feat(api): persist audits + enforce free plan quota"
```

---

### Task 2.6: Audit detail page

**Files:**
- Create: `apps/web/src/app/(app)/audits/[id]/page.tsx`
- Create: `apps/web/src/app/(app)/audits/[id]/report-view.tsx`

**Step 1:** Server component fetches audit from DB (RLS guards).

**Step 2:** `report-view.tsx` renders the `AuditReport`:
- Score card (big number + color)
- Strengths (green checks)
- Critical issues (red badges with fixes)
- Keywords table (primary/secondary/long-tail)
- Suggested copy (before/after side-by-side with copy buttons)
- Screenshot tips
- Prioritized action list

**Step 3:** Add "Copy all" and "Download as Markdown" buttons.

**Step 4:** Polish typography — use shadcn Card + Tabs.

**Step 5:** Commit
```bash
git add apps/web/src/app/\(app\)/audits/
git commit -m "feat(audit): detail page with report renderer"
```

---

### Task 2.7: Landing page upgrade

**Files:**
- Create: `apps/web/src/app/(marketing)/page.tsx`
- Create: `apps/web/src/app/(marketing)/layout.tsx`
- Create: `apps/web/src/components/marketing/*.tsx`

**Step 1:** Replace the temporary Formspree landing with a real Next.js marketing page:
- Hero: "Stop guessing. AI-audit your app listing in 60 seconds."
- 3 feature cards
- Pricing table (Free / Pro $19 / Agency $49)
- "How it works" steps
- Testimonial placeholder (empty until users exist)
- CTA → `/login`
- Footer

**Step 2:** Use digital-marketing-expert skill's copy templates:
- Problem-Solution hook
- Bullet points for features
- Clear CTA

**Step 3:** Lighthouse score > 95 (test locally with Chrome DevTools).

**Step 4:** Commit
```bash
git add apps/web/src/app/\(marketing\)/ apps/web/src/components/marketing/
git commit -m "feat(marketing): production landing page"
```

---

## Phase 3 — Payments (Week 3)

### Task 3.1: LemonSqueezy setup

**Step 1:** Sign up at lemonsqueezy.com (Indonesia supported as merchant of record).

**Step 2:** Create store + 2 products:
- ASO Copilot Pro — $19/month recurring
- ASO Copilot Agency — $49/month recurring

**Step 3:** Copy store ID, API key, webhook signing secret → `.env.local`.

---

### Task 3.2: Checkout flow

**Files:**
- Create: `apps/web/src/app/api/checkout/route.ts`
- Modify: `apps/web/src/app/(app)/dashboard/page.tsx` — add "Upgrade" button

**Step 1:** Implement checkout endpoint
```ts
// apps/web/src/app/api/checkout/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';

export async function POST(req: NextRequest) {
  const { variantId } = await req.json();
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return NextResponse.json({ error: 'unauthorized' }, { status: 401 });

  const res = await fetch('https://api.lemonsqueezy.com/v1/checkouts', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.LEMONSQUEEZY_API_KEY}`,
      'Content-Type': 'application/vnd.api+json',
      Accept: 'application/vnd.api+json',
    },
    body: JSON.stringify({
      data: {
        type: 'checkouts',
        attributes: {
          checkout_data: {
            email: user.email,
            custom: { user_id: user.id },
          },
        },
        relationships: {
          store: { data: { type: 'stores', id: process.env.LEMONSQUEEZY_STORE_ID } },
          variant: { data: { type: 'variants', id: String(variantId) } },
        },
      },
    }),
  });

  const json = await res.json();
  return NextResponse.json({ url: json.data.attributes.url });
}
```

**Step 2:** Upgrade button on dashboard posts to `/api/checkout` and redirects to returned URL.

**Step 3:** Commit
```bash
git add apps/web/src/app/api/checkout/
git commit -m "feat(payments): LemonSqueezy checkout endpoint"
```

---

### Task 3.3: Webhook handler

**Files:**
- Create: `apps/web/src/app/api/webhooks/lemonsqueezy/route.ts`

**Step 1:** Implement signature verification + event handling
```ts
import { NextRequest, NextResponse } from 'next/server';
import crypto from 'node:crypto';
import { createClient } from '@supabase/supabase-js';

export async function POST(req: NextRequest) {
  const raw = await req.text();
  const sig = req.headers.get('x-signature') ?? '';
  const hmac = crypto
    .createHmac('sha256', process.env.LEMONSQUEEZY_WEBHOOK_SECRET!)
    .update(raw)
    .digest('hex');
  if (sig !== hmac) return new NextResponse('invalid signature', { status: 400 });

  const event = JSON.parse(raw);
  const eventName = event.meta.event_name;
  const userId = event.meta.custom_data?.user_id;
  if (!userId) return new NextResponse('no user id', { status: 400 });

  const admin = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  );

  if (eventName === 'subscription_created' || eventName === 'subscription_updated') {
    const variantId = event.data.attributes.variant_id;
    const plan = variantId === PRO_VARIANT_ID ? 'pro' : 'agency';
    await admin.from('profiles').update({
      plan,
      current_period_end: event.data.attributes.renews_at,
    }).eq('id', userId);
  }

  if (eventName === 'subscription_cancelled' || eventName === 'subscription_expired') {
    await admin.from('profiles').update({ plan: 'free' }).eq('id', userId);
  }

  return NextResponse.json({ ok: true });
}
```

**Step 2:** Register webhook URL in LemonSqueezy dashboard: `https://your-domain/api/webhooks/lemonsqueezy`.

**Step 3:** Test with LemonSqueezy test mode + their webhook replay.

**Step 4:** Commit
```bash
git add apps/web/src/app/api/webhooks/
git commit -m "feat(payments): LemonSqueezy webhook subscription sync"
```

---

### Task 3.4: Deploy to production

**Step 1:** Vercel project link
```bash
cd apps/web
pnpm dlx vercel link
pnpm dlx vercel env pull
```

**Step 2:** Add all env vars via `vercel env add` or dashboard.

**Step 3:** Deploy
```bash
pnpm dlx vercel --prod
```

**Step 4:** Point custom domain.

**Step 5:** Smoke test entire flow on prod: signup → audit → upgrade → webhook → plan changes.

**Step 6:** Commit + tag
```bash
git tag v0.1.0-mvp
git push --tags
```

---

## Phase 4 — Launch & Marketing (Week 3-4)

> **SUB-SKILL:** Invoke `digital-marketing-expert` skill for every asset in this phase. It has audit frameworks, copy templates, and 90-day plan templates you should use verbatim.

### Task 4.1: Pre-launch content (Dev.to)

**Deliverables:**
- 3 articles published 3 days apart on dev.to

**Article 1:** "I audited 20 indie iOS apps — here are the 5 ASO mistakes everyone makes"
- Screenshot real examples (blur names if unconsented)
- End with: "I built a tool that does this in 60s. Waitlist: [link]"

**Article 2:** "Why AppTweak's $83/mo makes no sense for indie devs (and what I built instead)"
- Honest comparison table
- Side-by-side feature gap
- Clear positioning

**Article 3:** "I built an AI ASO tool in 2 weeks with Claude Code — here's the architecture"
- Build log style
- Code snippets
- Lessons learned
- CTA: free audit

**Cross-post:** Hashnode, Medium (with canonical back to dev.to).

---

### Task 4.2: Twitter / X campaign

**Use digital-marketing-expert copy templates (Problem-Solution, Social Proof, Thread opener).**

**Week before launch:**
- Daily tweet (building in public)
- "Day N: just shipped [feature]. Here's why [insight]"
- Screenshots of audit reports
- Tag @ProductHunt, @indiehackers

**Launch day:**
- Thread: "I spent 3 weeks building an AI ASO copilot for indie devs. Here's everything: 🧵"
- Pin tweet
- Reply to every comment within 1h

**Week after launch:**
- Before/after case studies from first users
- Revenue milestones
- "X signups in Y hours"

---

### Task 4.3: Reddit + IndieHackers + HN

**Reddit posts (no spam — follow each sub's rules):**
- r/iOSProgramming: "I built an AI ASO tool for indie iOS devs — free audit for first 50 commenters"
- r/androiddev: mirror
- r/SideProject: launch post with revenue/signup goals
- r/indiehackers (on Reddit AND site): milestone post

**Hacker News:**
- "Show HN: ASO Copilot — $19/mo AI app store optimization for indies"
- Post at 8am PT Tuesday (historically best time)
- Include free audit for HN commenters

**IndieHackers:**
- Milestone posts weekly
- Join product group

---

### Task 4.4: Product Hunt launch

**Prep checklist:**
- High-quality GIF (Tella.tv or Screen Studio, <3MB)
- 6 gallery images
- Topic tags: Developer Tools, iOS, Android, Marketing
- Hunter: reach out to an established hunter 1 week before
- Launch Tuesday-Thursday at 00:01 PT
- Prepare 20 "supporters" to upvote in first hour (friends, Twitter mutuals)
- First comment = founder intro with key features

**Day-of:**
- Reply to every comment
- Share hourly on Twitter
- Email waitlist at 6am PT

---

### Task 4.5: Cold outreach to indie devs

**Target list:** 50 indie devs found via:
- r/iOSProgramming weekly "Show your app" threads
- IndieHackers product pages
- Twitter search: "my indie app"

**Template (personalized):**
```
Subject: Free ASO audit for [App Name]?

Hi [Name],

Saw [App Name] on [source]. Really like [specific feature]. I built an AI ASO tool and would love to give you a free audit — no strings, just want real feedback.

Takes 60s. Here's the link: [audit URL]

If it sucks, tell me. If it helps, a tweet would mean the world.

— Jerry
```

**Track:** Open rate, reply rate, conversions. Use a simple Google Sheet for MVP.

---

## Phase 5 — Post-Launch Iteration (Week 4+)

### Task 5.1: Add A/B variant generator

Allow user to request 3 title/description variants and pick favorite. Reuse `runAudit` prompt with a different instruction mode.

### Task 5.2: Add competitor lookup

Input 1-3 competitor app URLs. Show side-by-side keyword comparison.

### Task 5.3: Weekly email digest

Cron job sends users:
- New audit suggestions (if any category keyword trends shift)
- Rank of their tracked keywords (via Claude web-search or a free ASO API)

### Task 5.4: Affiliate / referral program

Give users $5 credit per referral. Cross-promote existing Gumroad products:
- Terminal Income Starter
- iOS Developer Passive Income research bundle
- Any new Claude Code-related products

### Task 5.5: Bundle with existing Gumroad products

- Bundle "ASO Copilot 3 months" + "Terminal Income Starter" = $29 one-time
- Upsell from Gumroad products to SaaS subscription

---

## Success Criteria (Month 1)

| Metric | Target |
|--------|--------|
| Waitlist signups (pre-launch) | 50+ |
| Free audits run (week 1) | 100+ |
| Paying subscribers (month 1) | 20 |
| MRR (month 1) | $380 |
| Dev.to article views | 10K combined |
| Twitter followers added | +200 |
| Product Hunt rank | Top 10 of day |

If hit ≥70% of targets → scale marketing (Phase 5).
If hit <30% → talk to 10 users, diagnose, iterate or pivot.

---

## Testing Philosophy

- **Unit tests (vitest):** store wrappers, prompt builder, schema parsers
- **Integration tests:** real API calls for iTunes + Play (mark `@integration` for CI skip)
- **E2E (optional):** Playwright for login → audit → checkout flow (Phase 5)
- **TDD:** Write failing test BEFORE every non-trivial function

## Security Checklist

- [ ] No API keys in client bundle (use server-only env vars)
- [ ] RLS enforced on all tables
- [ ] Webhook signature verification
- [ ] Rate limit `/api/audit` by user id + IP (upstash Redis free tier, add in Phase 5)
- [ ] Input validation with zod at every API boundary
- [ ] No `eval`, no `dangerouslySetInnerHTML` except sanitized markdown

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Google Play scraper breaks | Fallback to AppFigures API (has free tier) |
| Claude API cost spikes | Cap max_tokens, cache audits for 30 days, bill usage per plan |
| Zero signups | Kill or pivot based on Phase 0 waitlist number — don't overbuild |
| LemonSqueezy rejects Indonesia | Fallback: Paddle (also merchant of record) |
| Copyright complaints from scraped apps | Store only public metadata + non-identifying thumbnails |

## Done = All of these true

- [ ] Landing page live at custom domain
- [ ] Signup → audit → persisted to DB works on prod
- [ ] Paid upgrade works end-to-end (checkout → webhook → plan change)
- [ ] 20 paying users OR 3 weeks elapsed + decision point
- [ ] Phase 4 marketing assets all shipped
- [ ] Post-launch retrospective saved to `logs/aso-copilot-retro.md`
