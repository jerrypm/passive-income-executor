# Part 4: Expert Secrets

## Chapter 13: Prompt Engineering for Claude Code

The difference between a developer who gets mediocre results from Claude Code and one who gets exceptional results almost always comes down to prompting. Not because Claude Code requires special syntax or magic words, but because how you frame a request determines how much context Claude Code can leverage — and context is everything.

This chapter covers the prompting patterns that expert developers use daily. These aren't theoretical guidelines. They're battle-tested techniques drawn from thousands of real development sessions.

### How Claude Code Prompts Differ

If you've used ChatGPT, Claude.ai, or any web-based AI tool, you've learned a certain prompting style: describe what you want in detail, provide background information, maybe include code snippets. That style works against you in Claude Code.

Claude Code is not a chatbot. It has tools. It can read your files, search your codebase, run commands, check git history, and inspect directory structures. It has persistent state — it remembers what you discussed earlier in the session. It knows which project you're in, what language you're using, and what framework your code is built on.

This means you don't need to provide context that Claude Code can discover on its own. Instead, you need to point it in the right direction and tell it what to accomplish.

**Bad prompt:**
```
Write a function that validates email addresses. It should check for
an @ symbol, a valid domain, and return true or false. Use TypeScript.
```

This is how you'd prompt a web chatbot. You're describing the implementation because the chatbot can't see your code. Claude Code can see your code.

**Good prompt:**
```
Add email validation to the signup handler in src/auth/signup.ts.
Use the same validation pattern as src/auth/utils.ts.
```

This prompt is shorter but far more effective. Claude Code will read both files, understand your existing validation patterns, and produce code that fits seamlessly into your codebase. The result will match your code style, your error handling patterns, your type conventions — all without you describing any of them.

The shift is fundamental: **stop describing the solution. Describe the goal and point to the context.**

### The 5 Principles of Expert Prompting

After working with hundreds of developers' Claude Code sessions, clear patterns emerge in what separates excellent prompts from average ones. These five principles account for the vast majority of quality difference.

#### Principle 1: Be Specific About Location

Claude Code can search your entire codebase, but telling it exactly where to work eliminates ambiguity and saves time. Include file paths, function names, and even line numbers when you know them.

**Vague:** "Fix the login bug."

**Specific:** "Fix the race condition in `src/auth/login.ts` in the `handleSubmit` function — the loading state isn't reset when the API call fails."

The specific prompt gets Claude Code working immediately. The vague prompt forces it to search for what "login bug" might mean, potentially finding the wrong issue or asking you clarifying questions.

This principle applies to feature requests too:

**Vague:** "Add a dark mode toggle."

**Specific:** "Add a dark mode toggle to the settings panel in `src/components/Settings.tsx`. Store the preference in the existing `usePreferences` hook from `src/hooks/usePreferences.ts`."

The more precisely you specify location, the fewer decisions Claude Code has to guess about — and the fewer guesses mean fewer mistakes.

#### Principle 2: Reference Existing Patterns

Your codebase already has patterns — how you write API routes, how you structure components, how you handle errors. Telling Claude Code to follow existing patterns produces code that reads like a human on your team wrote it.

```
Add a PATCH /users/:id endpoint to src/api/users.ts.
Follow the same pattern as the PATCH /posts/:id endpoint in src/api/posts.ts.
```

Claude Code reads the referenced file, extracts the pattern (middleware chain, validation approach, response format, error handling), and applies it to the new endpoint. The result is consistent with your codebase rather than consistent with some generic best practice that doesn't match your style.

This works at every scale:

- **Components:** "Create a ProductCard component following the pattern of `UserCard` in `src/components/UserCard.tsx`."
- **Tests:** "Add tests for the payment module. Follow the test structure in `tests/auth.test.ts`."
- **Migrations:** "Add a `last_login` column to the users table. Follow the migration format in `migrations/003_add_email_verified.sql`."

When you don't reference a pattern, Claude Code uses its general knowledge of best practices. When you do reference a pattern, it uses your team's specific conventions. The latter is almost always better.

#### Principle 3: State the Why

Including the reason behind your request helps Claude Code make better implementation decisions — especially when there are multiple valid approaches.

**Without why:** "Add caching to the user profile endpoint."

**With why:** "Add caching to the user profile endpoint — we're hitting the database 50 times per second for the same profiles during peak traffic. Use a 5-minute TTL since profiles rarely change."

The "why" tells Claude Code that this is a performance optimization, that the cache should be keyed per user, that staleness of up to 5 minutes is acceptable, and that the primary concern is database load rather than response latency. All of that context is implicit in two sentences.

Here's another example:

**Without why:** "Extract this function into a separate module."

**With why:** "Extract the PDF generation logic from `src/api/reports.ts` into `src/services/pdf.ts` — three other routes need PDF generation and they're all duplicating this logic."

Now Claude Code knows to design the extracted module with a clean public API that works for multiple callers, not just the one it was extracted from.

#### Principle 4: Scope Your Request

The right-sized request is specific enough to be clear but broad enough to be useful. Too narrow and you end up micromanaging. Too broad and Claude Code has to make too many decisions without guidance.

**Too narrow:** "On line 47 of `src/api/users.ts`, change `findOne` to `findUnique`."

You could do this yourself faster than typing the prompt. Only use this level of granularity when you need Claude Code to understand the change in context of a larger task.

**Too broad:** "Refactor the entire backend to use the repository pattern."

This is a multi-day project with hundreds of decisions. Claude Code will either ask many clarifying questions or make assumptions you disagree with. Break it up.

**Right-sized:** "Refactor `src/api/users.ts` to use a repository pattern. Extract the database queries into `src/repositories/UserRepository.ts`. Keep the same API contract — no changes to request/response shapes."

This is one coherent unit of work with clear boundaries. Claude Code can complete it in a single session without guessing about scope.

A good rule of thumb: if the task would take a human developer 15 minutes to 2 hours, it's probably right-sized for a single Claude Code prompt. Smaller tasks aren't worth the overhead. Larger tasks should be broken into sequential prompts.

#### Principle 5: Give Success Criteria

Tell Claude Code what "done" looks like. This is especially important for features with multiple edge cases or tasks where correctness matters more than speed.

```
Add a payment processing function to src/services/payment.ts.

Test cases to cover:
- Successful payment (charge amount, return confirmation)
- Card declined (return specific error code)
- Invalid amount (negative, zero, exceeds maximum)
- Duplicate transaction ID (idempotency check)

Run npm test after to verify everything passes.
```

The success criteria serve three purposes. First, they tell Claude Code what edge cases to handle in the implementation. Second, they define what tests to write. Third, the "run npm test" instruction makes Claude Code verify its own work before telling you it's done.

Without success criteria, Claude Code will handle the happy path and maybe one or two obvious error cases. With them, it builds a complete, production-quality implementation.

### Anti-Patterns to Avoid

Certain prompting habits actively reduce the quality of Claude Code's output. Here are the most common ones.

**Don't start with "Can you..."** — Claude Code doesn't need politeness. "Can you add error handling to the login function?" becomes "Add error handling to the login function in `src/auth/login.ts`." The direct version is clearer and gets better results. You're not being rude — you're being precise.

**Don't explain how Claude Code works to Claude Code.** Prompts like "You have access to my filesystem, so please read the file first and then..." are wasted tokens. Claude Code knows what tools it has. Just state the goal.

**Don't paste errors without context.** Pasting a stack trace with "fix this" sometimes works, but adding one sentence of context makes it work reliably: "Getting this error when running `npm test` after adding the new user endpoint" followed by the stack trace. The context tells Claude Code where to look and what changed.

**Don't ask Claude Code to "be careful" or "double-check."** These phrases don't make Claude Code more careful. If you want verification, ask for specific verification: "Run the test suite after making changes" or "Verify the migration is reversible." Actionable instructions beat vague caution.

**Don't bundle unrelated tasks.** "Fix the login bug, add a dark mode toggle, and update the README" combines three independent tasks. Handle them in separate prompts. Each task gets full attention, and if one goes wrong, it doesn't contaminate the others.

**Don't over-specify implementation details.** "Use a for loop to iterate over the array and check each element" is micromanaging. "Filter users by active status" lets Claude Code choose the idiomatic approach for your language and codebase.

### Power Prompt Templates

These four templates cover the vast majority of development tasks. Adapt them to your needs.

#### Bug Fix Template

```
Fix [symptom] in [file/function].
Expected: [correct behavior]
Actual: [what happens instead]
Reproduce: [command or steps]
```

**Example:**
```
Fix the 500 error on POST /api/orders in src/api/orders.ts.
Expected: Returns 201 with order confirmation.
Actual: Crashes with "Cannot read property 'id' of undefined."
Reproduce: npm test -- --grep "create order"
```

#### Feature Template

```
Add [feature] to [location].
Follow the pattern in [reference file].
Include tests covering: [cases].
Run [verification command] when done.
```

**Example:**
```
Add a PATCH /users/:id/avatar endpoint to src/api/users.ts.
Follow the upload pattern in src/api/posts.ts (multer + S3).
Include tests for: valid image, file too large, invalid format, unauthorized.
Run npm test when done.
```

#### Refactor Template

```
Extract [what] from [source] into [destination].
Reason: [why this refactor matters].
Keep [constraints — what shouldn't change].
```

**Example:**
```
Extract email sending logic from src/api/auth.ts and src/api/orders.ts
into src/services/email.ts.
Reason: both files duplicate SMTP setup and template rendering.
Keep the same function signatures — callers shouldn't need changes.
```

#### Debug Template

```
Debugging [error/symptom] when [action/trigger].
Context: [what changed recently or what you've already checked].
Find the root cause and fix it.
```

**Example:**
```
Debugging intermittent timeout on the /api/search endpoint.
Context: started after adding pagination in commit abc123.
Only happens when page > 10. Already checked — DB query returns fast.
Find the root cause and fix it.
```

### Conversation Management

How you manage your conversation with Claude Code is as important as individual prompts. Long conversations accumulate context, which is powerful — but they also accumulate noise.

**Use `/compact` when context gets long.** After 20-30 exchanges, your conversation carries a lot of history. The `/compact` command summarizes the conversation into key points and frees up context space. Use it when you notice Claude Code starting to lose track of earlier decisions or when responses slow down.

**Start new conversations for new topics.** If you've been debugging a database issue and now want to add a UI feature, start a fresh conversation. The database debugging context will only confuse the UI work. Use `claude` to start fresh, or `/clear` to reset in the same session.

**Use `@filename` to bring files into context.** When you mention a file path naturally, Claude Code reads it. But `@src/api/users.ts` explicitly loads the file into the conversation at that point, ensuring Claude Code has the latest version front and center.

**Use `/cost` to monitor token usage.** If you're on a metered plan, `/cost` shows how much the current session has consumed. Useful for budgeting long sessions.

**Keep prompts conversational within a session.** Your first prompt in a session should be detailed (include file paths, context, success criteria). Follow-up prompts can be terse because Claude Code remembers the context: "Now add the same validation to the update endpoint" or "Also handle the case where the user doesn't exist."

> **Tip:** The single most impactful change you can make to your prompting is adding file paths. "Fix the auth bug" might work. "Fix the auth bug in `src/auth/middleware.ts`" almost always works. When in doubt, include the path.

---
