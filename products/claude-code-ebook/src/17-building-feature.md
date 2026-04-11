# Part 5: Real-World Mastery

## Chapter 17: Building a Feature Start-to-Finish

Everything in this book so far has been modular — individual techniques, commands, and configurations you can learn in isolation. This chapter puts them all together. We're going to walk through building a real feature with Claude Code, from blank slate to merged pull request, showing the exact conversation flow at each stage.

The feature: add user notification preferences to a Next.js application. Users should be able to toggle email, push, and SMS notifications independently for three categories — marketing, product updates, and security alerts. The backend needs API routes, database schema changes, input validation, and tests.

This is a realistic mid-complexity feature. Not a trivial CRUD endpoint, not a massive architecture overhaul. The kind of thing a developer builds several times a week.

### Phase 1: Planning

You open your terminal in the project directory and start Claude Code.

```bash
cd ~/projects/acme-app
claude
```

The first prompt sets the direction:

```
Plan notification preferences for our app. Users should toggle
email/push/SMS per category (marketing, updates, security).
I need: database schema, API routes, validation.
Look at our existing code structure before proposing anything.
```

Notice what this prompt does. It describes the feature clearly but doesn't dictate implementation. The instruction to "look at existing code structure" is critical — it tells Claude Code to investigate before proposing.

Claude Code reads your `package.json`, scans the `src/` directory, checks `prisma/schema.prisma` for your existing data model, and reads a few existing API routes to understand your conventions. It comes back with a plan:

```
Based on your codebase:
- Database: Prisma with PostgreSQL
- API routes: Next.js App Router in src/app/api/
- Validation: Zod schemas in src/lib/validations/
- Auth: NextAuth with session middleware

Proposed plan:
1. Add NotificationPreference model to Prisma schema
2. Create migration
3. Add Zod validation schema
4. Create GET /api/notifications/preferences
5. Create PUT /api/notifications/preferences
6. Add tests following patterns in tests/api/

Data model:
- userId (relation to User)
- channel (email | push | sms)
- category (marketing | updates | security)
- enabled (boolean)
- Unique constraint on [userId, channel, category]
```

You review the plan. The data model makes sense — a separate row per channel-category combination rather than a JSON blob. This is queryable, indexable, and clean. But you want one adjustment:

```
Good plan. One change: use PATCH instead of PUT — we want partial
updates so the client can toggle a single preference without sending all of them.
```

Claude Code acknowledges and adjusts. The plan is now locked in. Total time: about 2 minutes. You haven't written a line of code, but you've agreed on the data model, API design, and file locations. This prevents the expensive mistake of building something and then realizing the approach is wrong.

### Phase 2: Tests First

With the plan agreed, you shift to test-driven development:

```
Write tests for notification preferences. Follow the patterns
in tests/api/user.test.ts. Cover:
- GET returns all preferences for authenticated user
- GET returns 401 for unauthenticated request
- PATCH updates a single preference
- PATCH validates channel and category values
- PATCH returns 401 for unauthenticated request
- PATCH returns 400 for invalid input
```

Claude Code reads `tests/api/user.test.ts` to understand your test conventions — the testing library (likely Vitest or Jest), how you set up test fixtures, how you mock authentication, and how you structure describe/it blocks. Then it creates `tests/api/notification-preferences.test.ts`.

The test file follows your existing patterns exactly: same import style, same helper functions for authenticated requests, same assertion patterns. It covers all six cases you specified.

You run the tests:

```
! npm test -- tests/api/notification-preferences.test.ts
```

All six tests fail. This is exactly what you want. Failing tests are your specification — they define precisely what the implementation must do. Each red test is a requirement waiting to be fulfilled.

```
6 tests, 0 passed, 6 failed
- NotificationPreference model not found (schema doesn't exist yet)
- Route /api/notifications/preferences not found (404)
```

Good. The failures confirm the tests are pointing at the right things. Move on.

### Phase 3: Implementation

Now you build incrementally, starting from the foundation:

```
Implement starting with the Prisma schema. Add the NotificationPreference
model as we planned.
```

Claude Code edits `prisma/schema.prisma`, adding the model with the userId relation, the channel and category enums, the enabled boolean, and the unique constraint. Then it generates the migration:

```bash
npx prisma migrate dev --name add-notification-preferences
```

You run tests again:

```
! npm test -- tests/api/notification-preferences.test.ts
```

Two tests now have different errors — they can see the model but can't find the API route. Progress.

```
Now the API routes. Create GET and PATCH for /api/notifications/preferences.
Follow the auth middleware pattern in src/app/api/user/route.ts.
```

Claude Code reads the reference file, sees how authentication is handled (checking the session, returning 401 if missing), and creates `src/app/api/notifications/preferences/route.ts` with both handlers.

The GET handler queries all preferences for the authenticated user. If no preferences exist yet (new user), it returns defaults — all channels enabled for security, all disabled for marketing, a sensible default set.

The PATCH handler accepts a body with `channel`, `category`, and `enabled`, finds or creates the matching preference row, and updates it.

Run the tests:

```
! npm test -- tests/api/notification-preferences.test.ts
```

```
6 tests, 4 passed, 2 failed
```

Four passing. The two failures are the validation tests — the PATCH handler doesn't yet reject invalid channel or category values. It accepts anything and lets the database complain with an ugly error instead of a clean 400 response.

### Phase 4: Iterate

This is where TDD pays off. The failing tests tell you exactly what's missing:

```
Add Zod validation to the PATCH handler. Reject invalid channel
and category values with a 400 response. Use the validation
pattern from src/lib/validations/user.ts.
```

Claude Code creates a Zod schema in `src/lib/validations/notification-preferences.ts`:

```typescript
import { z } from "zod";

export const updatePreferenceSchema = z.object({
  channel: z.enum(["email", "push", "sms"]),
  category: z.enum(["marketing", "updates", "security"]),
  enabled: z.boolean(),
});
```

Then it updates the PATCH handler to validate the request body against this schema before processing, returning a 400 with specific error messages when validation fails.

Run the tests one more time:

```
! npm test -- tests/api/notification-preferences.test.ts
```

```
6 tests, 6 passed
```

All green. But you're not done. Run the full test suite to check for regressions:

```
! npm test
```

```
147 tests, 147 passed
```

Clean. Your new feature doesn't break anything existing.

One more thing — you notice an edge case the original test plan missed:

```
Add one more test: PATCH should return 404 if the user account
doesn't exist (deleted user with stale session). Add handling
in the route too.
```

Claude Code adds the test and the corresponding guard in the handler. Seven tests, seven passing. Full suite still green.

### Phase 5: Polish & Commit

The feature is complete and tested. Time to ship:

```
Commit all notification preference changes with a descriptive message.
```

Claude Code stages the relevant files — the Prisma schema, migration, API route, validation schema, and test file — and creates a commit:

```
feat: add notification preferences API

Add GET/PATCH /api/notifications/preferences endpoints.
Users can toggle email/push/SMS per category (marketing,
updates, security). Includes Zod validation and full test
coverage.
```

The commit message follows your project's conventional commits format because Claude Code read your git history during the planning phase and matched the pattern.

Now create the pull request:

```
Create a PR targeting main. Summarize what we built.
```

Claude Code pushes the branch and creates the PR with a clear title and body describing the changes, the API contract, and the test coverage.

The entire feature — from planning to pull request — took about 15 minutes. A developer working alone might spend 45-90 minutes on the same feature. The time savings compound: build three features like this per day and you're saving 1.5 to 3.5 hours daily.

### Lessons From This Workflow

**Plan before you build.** The 2-minute planning phase prevented wrong turns that would have cost 20 minutes to fix. Claude Code's plan was 90% right; your one adjustment (PUT to PATCH) caught a design issue before any code existed.

**Reference existing patterns.** Every prompt pointed Claude Code at an existing file to follow. The tests matched your test conventions. The API routes matched your route conventions. The validation matched your validation conventions. The result reads like a team member wrote it, not an AI tool.

**TDD caught edge cases.** Writing tests first revealed that the PATCH handler needed input validation — something easy to forget when building implementation-first. The tests served as both a specification and a safety net.

**Multiple small prompts beat one massive prompt.** Five focused prompts produced better results than a single "build notification preferences with tests, validation, and a PR" mega-prompt would have. Each prompt had clear scope, and you could verify and adjust between steps.

**The progression matters.** Plan, then test, then implement, then iterate, then commit. This order works because each phase builds on the verified output of the previous phase. Skipping the plan leads to rework. Skipping tests leads to bugs. Skipping iteration leads to incomplete features.

This is the workflow that expert Claude Code users follow for every non-trivial feature. It feels slower at first — why plan when you could just start building? — but it's consistently faster end-to-end because you never build the wrong thing and you never ship untested code.

---
