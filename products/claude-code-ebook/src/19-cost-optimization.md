## Chapter 19: Cost Optimization & Efficiency

Claude Code is powerful, but it's not free. Whether you're on a subscription plan or paying per token via API key, understanding how costs work — and how to minimize them without reducing quality — is a practical skill that pays for itself immediately.

This chapter gives you the concrete strategies that experienced users rely on to keep costs low while maintaining high output. No vague advice — specific techniques with measurable impact.

### Understanding Token Costs

Every interaction with Claude Code consumes tokens. A token is roughly 3-4 characters of English text. Your costs come from two categories:

**Input tokens** — everything Claude Code reads: your prompts, file contents, CLAUDE.md instructions, conversation history, tool outputs, and MCP server responses. This is the context that Claude Code uses to understand your request.

**Output tokens** — everything Claude Code produces: responses, code it writes, commands it runs, tool calls it makes. Output tokens are more expensive than input tokens, typically 3-5x the cost per token.

This ratio matters. Reading a 500-line file (input) costs far less than Claude Code writing a 500-line file from scratch (output). Strategies that reduce output tokens save more than strategies that reduce input tokens by the same amount.

Track your spending with built-in commands:

```
/cost
```

This shows total tokens consumed and estimated cost for the current session. Check it periodically during long sessions — costs can accumulate faster than you expect when Claude Code is reading many files or generating long outputs.

For hard limits, set a budget cap when starting a session:

```bash
claude --max-budget-usd 5.00
```

The session ends gracefully when the budget is reached. Set low budgets for exploration sessions (browsing code, asking questions) and higher budgets for implementation sessions (building features, running tests).

### The 80/20 of Cost Reduction

Five techniques account for the vast majority of cost savings. Master these first.

**1. Read less: use offset and limit.**

When you know which part of a file you need, tell Claude Code exactly where to look. Reading a 2,000-line file when you only need lines 150-200 wastes tokens on 1,950 irrelevant lines.

```
Read lines 150-200 of src/services/payment.ts — the refund logic.
```

Claude Code reads 50 lines instead of 2,000. If you do this ten times per session across different files, the savings are substantial.

**2. Edit, don't Write.**

The Edit tool sends only the diff — the old text being replaced and the new text replacing it. The Write tool sends the entire file contents. For a 400-line file where you're changing 5 lines, Edit transmits roughly 15 lines while Write transmits all 400.

Reinforce this in your CLAUDE.md:

```markdown
- Always use Edit for modifying existing files
- Only use Write for creating new files
```

This single rule can cut output token costs by 30-50% for sessions heavy on file modifications.

**3. Compact proactively.**

The `/compact` command summarizes your conversation history into key points and frees up context space. Don't wait for auto-compression — it triggers around 60% context utilization and Claude Code decides what to keep.

```
/compact focus on the API changes and test results
```

The focus argument tells Claude Code what matters most. Without it, Claude Code might discard the exact context you need for your next prompt. Compact every 15-20 exchanges or whenever you notice the conversation getting long.

**4. Start fresh conversations.**

Long conversations carry all their history as input tokens. Every prompt in a 50-exchange conversation pays for the accumulated context of the previous 49 exchanges (compressed, but still substantial).

When you finish one task and start another, begin a new conversation. Don't reuse a debugging session for feature development. Don't keep a morning session alive into the afternoon. Fresh conversations have minimal context overhead.

```bash
# Finished debugging? Start fresh for the next task.
claude
```

**5. Choose the right model for the task.**

Not every task needs the most powerful model. Claude Code supports model switching mid-session with `Shift+Tab`. Match the model to the task complexity.

### Model Selection Strategy

| Task | Recommended Model | Why |
|------|-------------------|-----|
| "What does this function do?" | Haiku | Simple comprehension, fast response |
| "Add a CRUD endpoint" | Sonnet | Standard coding, good balance |
| "Refactor the auth architecture" | Opus | Complex reasoning, many files |
| "Fix this typo" | Haiku | Trivial change, minimal reasoning |
| "Debug a race condition" | Opus | Deep reasoning, subtle causation |
| "Write unit tests" | Sonnet | Pattern-following, moderate complexity |
| "Rename a variable across files" | Haiku | Mechanical, no judgment needed |
| "Design the database schema" | Opus | Architectural decisions, trade-offs |

The cost difference is significant. Haiku costs roughly 1/60th of Opus per token. A 10-minute session with Haiku for quick questions costs what 10 seconds of Opus output costs. Using Opus to fix a typo is like hiring an architect to change a lightbulb.

The practical workflow: start your session with Sonnet (the default). Switch to Haiku with `Shift+Tab` for quick lookups and simple changes. Switch to Opus for the hard problems — architecture decisions, complex debugging, multi-file refactors. Switch back to Sonnet when the hard part is done.

### Prompt Efficiency

The way you write prompts directly affects token consumption. Vague prompts cause back-and-forth exchanges (each one consuming tokens). Specific prompts get results in one shot.

**Expensive approach (3 exchanges):**
```
Exchange 1: "Fix the bug in the user service."
Exchange 2: "The one where it returns null instead of throwing."
Exchange 3: "In the getUserById function, line 45."
```

**Cheap approach (1 exchange):**
```
"Fix getUserById in src/services/user.ts (line 45) — it returns null
instead of throwing NotFoundError when the user doesn't exist."
```

The single specific prompt costs roughly one-third of the three-exchange version because it avoids two rounds of input context being re-sent.

Include these elements when possible:
- **File paths** — eliminates searching
- **Line numbers** — eliminates scrolling
- **Expected vs actual behavior** — eliminates guessing
- **Reference files** — eliminates asking for clarification

Every clarifying question Claude Code asks is a round trip that doubles the cost of that interaction. Front-load the context and eliminate the questions.

### Subscription vs API Key

Claude Code offers two pricing approaches. Understanding when each makes sense prevents overpaying.

**Subscription plans:**
- **Pro ($20/month):** Includes a daily message allowance. Best for moderate, consistent usage — a few tasks per day. Messages reset daily. If you hit the limit, you wait or upgrade.
- **Max ($100-200/month):** Higher daily limits, priority access to powerful models. Best for professional developers who use Claude Code as their primary coding tool throughout the day.

**API key (pay-per-token):**
- No message limits — pay exactly for what you use
- Costs vary by model: Haiku is very cheap, Opus is premium
- No daily resets — use as much or as little as needed
- Best for variable usage patterns or heavy burst usage

**Rule of thumb:** Track your API spending for a month. If you're consistently spending over $100/month on API tokens, the Max plan likely saves money. If you spend $20-50/month, Pro might be sufficient. If you use Claude Code sporadically (a few sessions per week), API key is cheapest because you only pay for what you use.

You can check subscription usage with:

```
/stats
```

This shows session counts, token consumption, and usage patterns. Review it weekly to understand whether your plan matches your actual usage.

### Hidden Cost Traps

Certain patterns silently inflate your token costs. Watch for these.

**Large files in context.** `package-lock.json` can be 50,000+ lines. If Claude Code reads it (or if it's accidentally included via a broad search), you've consumed a massive number of input tokens for minimal value. Use `.claudeignore` to exclude generated files:

```
# .claudeignore
package-lock.json
yarn.lock
pnpm-lock.yaml
*.min.js
*.min.css
dist/
build/
coverage/
node_modules/
```

This single file can cut per-session costs by 10-20% depending on your project structure.

**Re-reading the same files.** In a long conversation, Claude Code might read the same file multiple times as earlier reads get compressed out of context. If you know you'll reference a file repeatedly, mention it once at the start and use `/compact` with instructions to preserve its contents.

**Write instead of Edit.** Already covered, but worth repeating because it's the single most common cost waste. Every time Claude Code uses Write to modify an existing file, you pay for the entire file as output tokens. A 300-line file modified via Write costs 60x more in output tokens than the same change via Edit (5 lines of diff).

**Overly broad searches.** "Search the entire codebase for anything related to authentication" might read hundreds of files. "Search `src/auth/` for the session validation logic" reads three. Guide Claude Code to the right directory and it won't need to search broadly.

**Long conversations without compaction.** After 30+ exchanges, your conversation history might consume 50,000+ tokens of input on every single prompt. That's 50,000 tokens of context being re-processed every time you type a one-line request. Use `/compact` or start fresh.

**Unnecessary code generation.** If Claude Code offers to generate boilerplate that your framework provides (scaffolding commands, template generators), ask it to use the framework's generator instead. `npx prisma generate` produces the Prisma client in milliseconds and zero output tokens. Having Claude Code write the equivalent code manually costs tokens and produces an inferior result.

### Cost-Effective Workflows

Combining these techniques into daily habits produces consistent savings.

**Morning startup:** Fresh conversation. Sonnet model. State the day's goal clearly. Include file paths.

**Quick questions mid-task:** Switch to Haiku. Ask the question. Switch back.

**Complex implementation:** Stay on Sonnet. Reference existing patterns. Use Edit not Write. Compact every 20 exchanges.

**Architecture decisions:** Switch to Opus for the planning phase. Get the plan approved. Switch to Sonnet for implementation.

**End of day:** Check `/cost`. Review where tokens went. Identify any wasteful patterns to avoid tomorrow.

The goal isn't to minimize spending at the expense of productivity. A $5 session that saves you 3 hours of work is excellent value. The goal is to stop spending $5 on work that should cost $0.50 — by being specific, staying focused, and matching the model to the task.

---
