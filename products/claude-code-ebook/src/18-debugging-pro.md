## Chapter 18: Debugging Like a Pro

Most developers approach debugging with Claude Code backwards. They paste an error, say "fix this," and accept whatever Claude Code suggests. Sometimes this works. Often it produces a fix that addresses the symptom while leaving the root cause intact — or worse, introduces a new bug while silencing the original one.

Expert debugging with Claude Code follows a different pattern. It's methodical, evidence-driven, and produces fixes that actually solve the problem. This chapter teaches that pattern.

### The Expert Debugging Mindset

The core principle is simple: **don't guess, investigate.** When something breaks, the natural instinct is to hypothesize immediately. "It's probably a null check." "I bet the database connection timed out." "Must be a CORS issue." Resist this instinct.

Instead, let Claude Code gather evidence before proposing anything. Claude Code can read files, search patterns, trace imports, check git history, and run commands — all faster than you can manually investigate. Your job is to point it at the problem and let it work.

The difference in practice:

**Guessing approach:**
```
The login is broken. Probably a session issue. Fix the session handling.
```

Claude Code modifies session handling based on your guess. If the guess is wrong, you've now changed working code and still have the original bug.

**Investigation approach:**
```
Login returns 500 since this morning. Here's the error:
! npm test -- --grep "login" 2>&1 | tail -20
```

Claude Code sees the actual error, reads the relevant files, traces the call stack, and finds the root cause — which might be session handling, or might be something completely different. The fix addresses what's actually broken.

### The 5-Step Debugging Workflow

This workflow applies to every bug, from a one-line typo to a multi-service race condition. The steps scale with the complexity of the problem.

#### Step 1: Reproduce

Before anything else, give Claude Code a way to see the failure. The best reproduction is a failing test or a command that triggers the error.

```
Getting "TypeError: Cannot read properties of undefined (reading 'email')"
when creating a new user. Reproduce:
! npm test -- tests/api/users.test.ts -t "create user" 2>&1 | tail -30
```

The `!` prefix runs the command inline and puts the output directly into your conversation. Claude Code sees the exact error, the stack trace, and the test context. The `2>&1` captures stderr (where most error output goes), and `tail -30` keeps the output focused on the relevant part.

If you don't have a failing test, describe the steps:

```
Bug: clicking "Save" on the profile page shows a spinner forever.
No error in browser console. Network tab shows POST /api/profile
returns 200 but the response body is empty.
```

The reproduction tells Claude Code three things: what should happen, what actually happens, and where to start looking.

**If you can't reproduce it, say so.** "This happens intermittently — about 1 in 10 requests" is valuable information. Claude Code will look for race conditions, timing issues, or non-deterministic behavior rather than straightforward logic errors.

#### Step 2: Investigate

This is the step most developers skip — and it's the most important one. Let Claude Code explore before it proposes anything.

```
Investigate the root cause. Read the relevant files, trace the call stack,
and check recent git changes. Don't propose a fix yet.
```

The explicit "don't propose a fix yet" is important. Without it, Claude Code might jump to a solution after reading one file. With it, Claude Code reads the handler, the service layer, the database query, checks the types, reviews recent commits, and builds a complete picture.

During investigation, Claude Code typically:

- Reads the file where the error originates
- Traces imports to find where data flows from
- Checks the database schema or type definitions
- Searches for similar patterns that work correctly
- Reviews recent commits that might have introduced the change
- Reads test files to understand expected behavior

Let this process run. The investigation might reveal that the "bug" is actually three bugs, or that the error message is misleading, or that the real problem is in a completely different file from where the error surfaces.

#### Step 3: Hypothesize

After investigation, Claude Code proposes a root cause. This is where you apply critical thinking. Don't accept the first hypothesis unchallenged.

```
What evidence supports that hypothesis? What would disprove it?
```

This question forces Claude Code to justify its reasoning with specific evidence from the codebase rather than general plausibility. A strong hypothesis looks like:

> "The error occurs because `getUserProfile()` in `src/services/user.ts` returns `null` when the user doesn't have a profile row, but the caller in `src/app/api/profile/route.ts` (line 23) destructures `.email` without a null check. This was introduced in commit `a3f2c1d` three days ago when the profile query was refactored — the old version returned a default object, the new version returns null."

A weak hypothesis looks like:

> "The error is probably because the user object is undefined somewhere. Let me add a null check."

The strong hypothesis identifies the exact file, line, commit, and mechanism. The weak one guesses. If Claude Code gives you a weak hypothesis, push back:

```
That's too vague. Which specific function returns undefined?
Show me the line where it breaks.
```

#### Step 4: Fix Minimally

Once the root cause is confirmed, apply the smallest possible fix. Not a refactor. Not "improvements while we're here." The minimal change that fixes the bug.

```
Fix it with the smallest change possible. Don't refactor anything else.
```

This constraint is essential. When Claude Code fixes a bug, it sometimes wants to "improve" surrounding code — rename variables, extract functions, add error handling to unrelated paths. Every additional change is a potential new bug and makes the fix harder to review.

A good bug fix changes 1-5 lines. It should be obvious from the diff what was wrong and what was fixed. If the fix requires changing 50 lines, either the root cause analysis was wrong or the problem is architectural — in which case, fix the immediate bug minimally and plan the refactor separately.

```
Fix the null check in the profile handler. If getUserProfile()
returns null, return a 404 response instead of destructuring.
```

Claude Code adds a guard clause — three lines of code. The fix is clear, reviewable, and precisely targeted.

#### Step 5: Verify

Run the failing test to confirm the fix works, then run the full suite to check for regressions.

```
Run the failing test, then the full suite.
! npm test -- tests/api/users.test.ts -t "create user"
! npm test
```

Both must pass. If the targeted test passes but the full suite reveals a new failure, the fix is incomplete or has side effects. Go back to Step 2 and investigate the new failure.

Verification is non-negotiable. "It looks correct" is not verification. "All 147 tests pass" is verification.

### Common Debugging Patterns

Different bugs call for different initial prompts. Here are the patterns that work best for common scenarios.

**Runtime error with stack trace:**
```
Getting this error in production. Here's the stack trace:
[paste the full stack trace]
Find the root cause — don't just add a try-catch around it.
```

The "don't just add a try-catch" instruction prevents Claude Code from wrapping the problem instead of solving it.

**Test passes locally, fails in CI:**
```
This test passes on my machine but fails in CI. Here's the CI output:
[paste CI log]
Check for environment-dependent behavior: env vars, file paths,
timing assumptions, or dependency version differences.
```

Common causes: hardcoded paths, timezone assumptions, missing environment variables, different Node.js versions, test ordering dependencies.

**Something changed and you don't know what:**
```
The search endpoint was working yesterday and returns empty results today.
! git log --oneline -10
! git diff HEAD~5 -- src/api/search.ts src/services/search.ts
```

Feeding the recent git history and diffs directly into context lets Claude Code see exactly what changed. Often the bug is visible in the diff.

**Confusing or misleading error message:**
```
Getting "ECONNREFUSED" on the payment endpoint but the payment
service is running. Read the error source code to understand
what actually triggers this error — the message might be misleading.
```

Some errors have generic messages that don't describe the actual cause. Asking Claude Code to read the source of the error (the library code that throws it) often reveals the real trigger.

**Performance issue:**
```
The /api/reports endpoint takes 12 seconds for large date ranges.
Profile the database queries and identify which one is slow.
Check for missing indexes.
```

Be specific about what "slow" means — include the actual timing and the conditions that trigger it. "It's slow" gives Claude Code nothing to work with. "12 seconds for date ranges over 90 days" gives it a clear investigation path.

### The Systematic Debugging Skill

Claude Code includes a built-in skill for disciplined debugging:

```
/systematic-debugging
```

This skill enforces the 5-step workflow as a structured process. It prevents the common trap of jumping to fixes before completing investigation. The skill guides you through reproduction, evidence gathering, hypothesis formation, minimal fix application, and verification — with explicit checkpoints between each stage.

Use it when you catch yourself wanting to skip straight to "just fix it." The skill adds about 2 minutes of discipline that saves 20 minutes of chasing wrong hypotheses.

### Anti-Patterns That Make Debugging Worse

These habits are common and they all reduce debugging effectiveness.

**"Fix it" without sharing the error.** Claude Code can't debug what it can't see. Always include the error message, stack trace, or reproduction steps. If you don't have them, your first prompt should be: "Help me reproduce this — the search feature sometimes returns wrong results but I don't have a consistent repro."

**Guessing the cause in your prompt.** "The bug is probably in the database query — fix it" sends Claude Code down a specific path that might be wrong. "The endpoint returns wrong results — investigate" lets Claude Code follow the evidence wherever it leads.

**Accepting the first suggestion without evidence.** Claude Code's first hypothesis might be wrong. Before applying a fix, ask: "What evidence from the codebase supports this diagnosis?" If Claude Code can't point to specific lines, the hypothesis is a guess.

**Adding try-catch everywhere.** This is the debugging equivalent of putting tape over your car's warning light. The error goes away — but the problem remains, now silently. If Claude Code suggests wrapping something in try-catch, ask: "What error are we catching and why does it occur? Can we prevent it instead of catching it?"

**Adding logging "just in case."** Scattering `console.log` statements is a legacy debugging technique from before AI-assisted development. Claude Code can read the code and trace the data flow without executing it. Logging makes sense when you need runtime values that can't be inferred from code reading — but for most bugs, Claude Code can identify the issue through static analysis alone.

**Fixing the symptom instead of the cause.** If a function returns `undefined` and you add a fallback default, the function still returns `undefined` — you've just hidden it. Fix why it returns `undefined`. The extra 5 minutes of investigation saves hours of cascading bugs downstream.

The developers who get the most value from Claude Code during debugging are the ones who treat it as an investigator rather than a fixer. Point it at the problem, let it gather evidence, challenge its hypothesis, and only then apply the minimal fix. This approach is slower for trivial bugs (where "fix it" would have worked) but dramatically faster for everything else — and it never makes things worse.

---
