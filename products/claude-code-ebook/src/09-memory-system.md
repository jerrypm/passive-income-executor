# Part 3: Advanced Techniques

## Chapter 9: The Memory System

Every conversation with Claude Code starts fresh. You explain your architecture, share your preferences, clarify a naming convention — and next session, all of that is gone. Claude Code is brilliant within a conversation, but between conversations, it has amnesia.

The Memory system fixes this. It gives Claude Code persistent knowledge that survives across sessions — your preferences, your project's quirks, decisions you've made, context that would be tedious to re-explain every time. Combined with CLAUDE.md (which you learned in Chapter 5), Memory transforms Claude Code from a stateless tool into something that genuinely learns your project over time.

### The Problem Memory Solves

Consider a typical week of development:

- Monday: You tell Claude Code "we use Prisma, not Drizzle" when it suggests the wrong ORM.
- Tuesday: You explain that the `payments` service talks to Stripe through a custom wrapper, not directly.
- Wednesday: You clarify that integration tests should use a real database, not mocks — because mocked tests passed but production broke.
- Thursday: You mention that the team is in a merge freeze until April 15.

Without Memory, you'd re-explain all of this in every new session. With Memory, Claude Code remembers. Monday's correction about Prisma persists into Tuesday. Wednesday's testing lesson carries forward indefinitely. Thursday's merge freeze stays active until you tell Claude Code the freeze is over.

Memory is the difference between working with a colleague who takes notes and one who doesn't.

### How Memory Works

Memory files live at `~/.claude/projects/<project-hash>/memory/`. Each project gets its own memory directory, keyed by a hash of the project path. Inside that directory:

- **`MEMORY.md`** is the index file. The first 200 lines of this file are loaded into every conversation automatically. This is where Claude stores the most important context — a summary of what it knows about you and your project.

- **Individual topic files** store detailed knowledge about specific subjects. These are loaded on-demand when they become relevant to the conversation. If you're discussing testing, Claude loads the testing-related memory file. If you're working on the API, the API-specific file gets loaded.

Memory is populated in two ways:

1. **Automatic** — Claude Code detects important information during conversations and saves it without being asked. If you correct a mistake, explain a preference, or share project context, Claude may save that for future reference.

2. **Explicit** — You tell Claude to remember something directly:

```
Remember that we use Prisma, not Drizzle, for all database access.
```

```
Remember: integration tests must use real databases, not mocks.
```

```
Remember that the team has a merge freeze until April 15.
```

Claude Code saves these as persistent memory entries that it will recall in future sessions.

### Memory Types

Not all knowledge is the same. Claude Code organizes memory into four categories:

| Type | Purpose | Example |
|------|---------|---------|
| `user` | Who you are, your expertise | "Senior backend dev, prefers Go over Python" |
| `feedback` | How Claude should approach work | "Don't mock the DB in tests — use test containers" |
| `project` | Ongoing project context | "Merge freeze starts April 15, unfreeze May 1" |
| `reference` | External resources and tools | "Bug tracking in Linear, project CORE-backend" |

These types help Claude Code prioritize and apply knowledge correctly. A `feedback` memory about testing style is applied whenever Claude writes tests. A `project` memory about a merge freeze is applied whenever Claude tries to commit or push code.

### Memory File Format

Each memory file uses a simple markdown format with YAML frontmatter:

```markdown
---
name: testing-preferences
description: How to write tests in this project
type: feedback
---

Always use integration tests with real database, not mocks.

**Why:** Mocked tests passed but production migration failed — the 
mock didn't enforce foreign key constraints.

**How to apply:** For database operations, use the test container 
defined in `test/setup.ts`. For external APIs (Stripe, SendGrid), 
use the VCR-style recorder in `test/fixtures/`.
```

The frontmatter tells Claude what the memory is about (`name`, `description`) and how to apply it (`type`). The body contains the actual knowledge, ideally with reasoning (`**Why:**`) and actionable guidance (`**How to apply:**`).

Another example — a reference memory:

```markdown
---
name: deployment-process
description: How we deploy to production
type: reference
---

Deployments go through three stages:
1. PR merged to `main` triggers staging deploy (automatic)
2. QA team tests on staging (manual, ~2 hours)
3. Release manager runs `/deploy prod` in Slack

Never push directly to `main`. Never skip staging.
Contact @sarah-ops for emergency hotfix deployments.
```

### The MEMORY.md Index

`MEMORY.md` is the master index. Claude Code reads the first 200 lines of this file at the start of every conversation, so it needs to be concise and high-signal. Think of it as a cheat sheet — one line per fact, organized by category.

```markdown
# Project Memory

## User
- Senior backend developer, 8 years experience, prefers Go
- Uses Neovim in tmux, dark theme, minimal UI

## Project
- Merge freeze: April 15 - May 1 (spring release)
- New auth system migration in progress (see auth-migration)
- Performance budget: API responses under 200ms p99

## Feedback
- Use real DB in tests, not mocks (see testing-preferences)
- Prefer early returns over nested if/else
- Always add OpenAPI annotations to new endpoints

## Reference
- Bug tracking: Linear, project CORE-backend
- CI/CD: GitHub Actions, deploys via ArgoCD
- Monitoring: Datadog dashboards in #ops-alerts Slack channel
```

**Keep each entry under 150 characters.** The parenthetical references like `(see testing-preferences)` point to individual memory files that Claude loads on-demand when that topic comes up.

**Stay under 200 lines total.** Everything beyond line 200 is not loaded automatically — it would only be found if Claude explicitly reads the file. Put your most important context in the first 100 lines.

### What NOT to Save in Memory

Memory is for knowledge that Claude Code can't get from other sources. Don't save:

- **Code patterns** — Claude can read your codebase directly. Instead of memorizing "we use the repository pattern," just let Claude see your repository classes.

- **Git history** — Claude has `git log`. Don't memorize "we merged the auth refactor last week." Claude can look that up.

- **Debugging solutions** — The fix is in the code. If you fixed a bug, the fix exists in the diff. Don't memorize "we fixed the null pointer in UserService" — it's already in git history.

- **Anything in CLAUDE.md** — CLAUDE.md is loaded every session, just like MEMORY.md. Don't duplicate information between them. CLAUDE.md is for static project rules. Memory is for dynamic, learned context.

- **Temporary information** — "The CI is broken today" doesn't need to be memorized. It'll be fixed tomorrow. Memory is for knowledge with at least a multi-week shelf life.

The rule of thumb: if Claude could discover it by reading code or running a command, don't put it in memory. Memory is for the things that exist only in your head.

### Controlling Memory

You have several ways to manage what Claude Code remembers:

**View and edit memory:**

```
/memory
```

This opens a browser-like interface showing all memory files for the current project. You can read, edit, and delete entries.

**Explicit save and forget:**

```
Remember that we switched from REST to GraphQL for the mobile API.
```

```
Forget the merge freeze — it's been lifted.
```

Claude Code processes these as direct instructions to update or remove memory entries.

**Disable auto-memory entirely:**

If you don't want Claude Code saving information automatically, add this to your settings.json:

```json
{
  "autoMemoryEnabled": false
}
```

With auto-memory disabled, Claude Code only saves memory when you explicitly ask it to. This gives you full control over what persists.

**Memory and context compaction:**

When a conversation gets long and Claude Code compacts the context (removing older messages to stay within the context window), memory survives. Key memories are re-injected from MEMORY.md after compaction, so Claude doesn't lose critical context even in marathon sessions.

### Memory + CLAUDE.md: The Full Picture

These two systems serve different purposes and work together:

| | CLAUDE.md | Memory |
|---|-----------|--------|
| **Content** | Static project rules | Dynamic learned context |
| **Updates** | You edit manually | Claude updates automatically (or on request) |
| **Scope** | Shared with team (committed to git) | Personal (per-machine) |
| **Loaded** | Every session, full file | MEMORY.md first 200 lines + on-demand files |
| **Examples** | Build commands, coding conventions | Your preferences, project status, past decisions |

Together, they give Claude Code two layers of knowledge: what the project needs (CLAUDE.md) and what you specifically need (Memory). A new team member cloning the repo gets the CLAUDE.md rules immediately. Your personal Memory — built over weeks of working together — stays on your machine, tuned to your workflow.

> **Tip:** Think of CLAUDE.md as the employee handbook and Memory as personal notes. The handbook tells everyone the rules. Your notes remind you of the decisions, preferences, and lessons learned along the way. Claude Code reads both before every conversation — which means it starts each session knowing the rules AND your personal context.

---
