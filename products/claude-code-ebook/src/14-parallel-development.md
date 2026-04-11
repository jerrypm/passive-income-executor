## Chapter 14: Parallel Development with Subagents & Worktrees

Most development work is sequential. You work on a feature, finish it, start the next one. Even with Claude Code, the default mode is one conversation, one task at a time. But many tasks have independent parts that could happen simultaneously — writing tests for module A while implementing module B, reviewing code in one area while refactoring another, researching an approach while building a prototype.

Claude Code's subagent system and git worktree integration unlock true parallel development. This chapter shows you how to run multiple Claude Code instances simultaneously, each working on independent tasks, without them interfering with each other.

### The Problem with Sequential Work

Consider a typical feature implementation:

1. Write the API endpoint (20 minutes)
2. Write tests for the API endpoint (15 minutes)
3. Update the frontend component (15 minutes)
4. Write tests for the frontend component (10 minutes)
5. Update the documentation (5 minutes)

Sequential, that's 65 minutes. But steps 3-5 don't depend on steps 1-2. The frontend work needs the API contract, not the implementation. The docs need the feature description, not the finished code. In theory, you could do steps 1-2 and 3-5 in parallel — cutting the wall-clock time significantly.

Without tooling, parallelism is hard. You'd need multiple terminal windows, separate git branches, manual coordination. It's more effort than it's worth for most tasks. Subagents and worktrees make it effortless.

### Agent Tool — Spawning Subagents

Claude Code can spawn specialized sub-agents: independent Claude Code instances that work on isolated tasks without polluting your main conversation's context.

When you ask Claude Code to handle something that benefits from isolation — a research question, a parallel task, a code review — it can delegate to a subagent. The subagent gets its own fresh context, works independently, and reports back when finished.

You can trigger subagents explicitly:

```
Run tests for the auth module in the background while I work on the payment feature.
```

Claude Code spawns a subagent to run the tests. Your main conversation continues uninterrupted. When the tests finish, you're notified with the results.

Or implicitly — Claude Code sometimes recognizes that a task has independent sub-tasks and spawns agents on its own, especially in plan execution mode.

Each subagent is fully isolated. It has its own conversation history, its own tool context, and its own working state. Changes one subagent makes to files are visible to others (they share the filesystem), but their conversation contexts don't leak. This means a subagent researching your authentication architecture doesn't fill your main conversation with hundreds of lines of code exploration.

### Agent Types

Not all subagents are the same. Different agent types are optimized for different kinds of work:

| Type | Purpose | Best For |
|------|---------|----------|
| `general-purpose` | Multi-step tasks requiring tools | Code changes, implementations, complex research |
| `Explore` | Codebase exploration and understanding | "How does the auth system work?", architecture questions |
| `Plan` | Architecture and design planning | "Design the approach for adding multi-tenancy" |
| `code-reviewer` | Reviewing completed code changes | Pre-commit review, PR review, security audit |

**Explore agents** are lightweight. They read files and search code but don't make changes. Use them when you need to understand something about your codebase without modifying it. They're fast because they don't need write permissions.

**Plan agents** produce structured plans — step-by-step implementation approaches with file lists, dependency analysis, and risk assessment. They don't write code. They plan what code to write. Use them before starting complex features.

**Code reviewer agents** analyze changes with a critical eye. They look for bugs, performance issues, security vulnerabilities, and style inconsistencies. Spawn one after completing a feature to get a review before you commit.

**General-purpose agents** can do everything — read, write, run commands, make decisions. They're the default when a task requires actual code changes.

### Background Agents

The most practical form of parallel development is background agents. You launch a task in the background and keep working in the foreground. When the background task finishes, you're notified.

**Launching from conversation:**

```
Run the full test suite in the background and report any failures.
I'll keep working on the migration.
```

Claude Code spawns a background agent that runs the tests. Your conversation continues. When tests finish, you see the results inline.

**Using Ctrl+B:**

If you're in the middle of a task and realize it's going to take a while, press `Ctrl+B` to send it to the background. Claude Code continues working on that task in a background process, and your terminal is freed up to start a new conversation. You're notified when the background task completes.

This is surprisingly useful in practice. You ask Claude Code to refactor a large module, it starts working, and you realize you don't need to watch it. `Ctrl+B` — now you can start a new `claude` session and work on something else while the refactor continues.

**Checking status:**

Background agents run independently. When they finish, Claude Code shows their results. If you're in the middle of typing when a background agent completes, the notification waits until you're at a natural break point.

### Git Worktrees — Isolated Environments

Background agents share your filesystem. If agent A is editing `src/api/users.ts` while agent B is also editing `src/api/users.ts`, you have a conflict. Git worktrees solve this.

A git worktree is an isolated copy of your repository in a separate directory, on a separate branch, but sharing the same git history. Think of it as a lightweight clone that doesn't duplicate the entire `.git` directory.

```bash
claude --worktree feature-auth
```

This creates a new worktree in a sibling directory (e.g., `../myproject-feature-auth/`), checks out a new branch `feature-auth`, and starts Claude Code in that isolated directory. Everything you do in that session happens in the worktree — edits, commits, test runs — all isolated from your main working directory.

When you're done, the changes exist on the `feature-auth` branch. Merge them back to main via git merge or a pull request, just like any other branch.

**Why worktrees instead of separate clones?** Worktrees share the git object store. Creating one is instant — no network fetch, no disk duplication. They're also aware of each other, so git prevents you from checking out the same branch in multiple worktrees (which would cause confusion).

**The `.worktreeinclude` file:** Your main directory might have gitignored files that the worktree needs — `.env` files, local configs, build caches. Create a `.worktreeinclude` file in your project root listing the gitignored files that should be copied into new worktrees:

```
.env
.env.local
node_modules/
```

When Claude Code creates a worktree, it copies these files over so the worktree environment matches your main one.

### The `/batch` Command — Parallel Changes at Scale

Sometimes you need the same type of change across many files or modules. Migrating a component library, updating API call patterns, converting class components to functional ones. The `/batch` command automates this at scale.

```
/batch migrate all Vue components in src/components/ to React
```

Here's what happens: Claude Code analyzes the scope (finds all Vue components), creates a plan (one worktree per component or group of components), spawns subagents (each in its own worktree, each handling a subset of the migration), and opens pull requests (one per worktree, each independently reviewable).

The power of `/batch` is that each subagent works in complete isolation. If the migration of `UserProfile.vue` fails, it doesn't affect the migration of `Dashboard.vue`. Each PR can be reviewed, tested, and merged independently.

`/batch` can handle 5 to 30 parallel worktrees depending on your machine's resources. For large-scale changes — framework migrations, API version upgrades, dependency replacements — this turns days of work into hours.

Other practical `/batch` use cases:

```
/batch add error handling to all API routes in src/api/
/batch add unit tests for all services in src/services/
/batch update all imports from lodash to lodash-es
/batch add TypeScript types to all .js files in src/utils/
```

Each of these spawns parallel agents, each in its own worktree, each producing an independent PR.

### When to Use What

The parallel development toolkit has several options. Here's a decision guide:

**Quick answer or exploration** — Use an Explore agent in the foreground. "How does the caching layer work?" doesn't need background processing. Get the answer, move on.

**Independent work that takes time** — Use a general-purpose agent in the background. "Run the full test suite," "Refactor the logging module," "Add comprehensive tests to the payment service." Send it to the background with `Ctrl+B` and keep working.

**Feature work that might conflict with your current work** — Use a worktree. If you're editing `src/api/users.ts` and want Claude Code to also refactor `src/api/users.ts` in a different way, you need isolation. Worktrees give you separate branches and separate directories.

**Mass changes across many files** — Use `/batch`. When the same type of change applies to 10+ files or modules, `/batch` parallelizes the work and produces independent PRs.

**Pre-commit review** — Use a code-reviewer agent. After finishing a feature, spawn a reviewer to check your work before committing. It runs in the foreground (you want to read the review), but it doesn't pollute your main conversation's context.

**Complex feature planning** — Use a Plan agent before starting implementation. Have it analyze the codebase, identify dependencies, and produce a step-by-step plan. Then execute the plan yourself or hand it to an executing agent.

### Custom Subagents

You can define custom agent types with specialized instructions, tool restrictions, and behavioral guidelines. Create a markdown file in `.claude/agents/`:

```
.claude/agents/security-reviewer/AGENT.md
```

```yaml
---
name: security-reviewer
description: Reviews code changes for security vulnerabilities
model: claude-sonnet-4-6
tools: Read Grep Glob
---

## Review Checklist

When reviewing code, systematically check for:

1. **SQL Injection** — Parameterized queries? No string concatenation in SQL?
2. **XSS** — Output encoding? React's JSX auto-escaping intact?
3. **CSRF** — Token validation on state-changing endpoints?
4. **Auth bypass** — Every endpoint checks permissions?
5. **Secrets** — No hardcoded API keys, passwords, or tokens?
6. **Input validation** — All user input validated and sanitized?
7. **Rate limiting** — Abuse-prone endpoints rate-limited?

Report findings as:
- CRITICAL: Must fix before merge
- WARNING: Should fix, but not blocking
- INFO: Suggestion for improvement
```

Now you can invoke this agent:

```
Use the security-reviewer agent to review my changes before I commit.
```

Claude Code spawns a subagent with the `security-reviewer` configuration. It only has read access (Read, Grep, Glob — no Edit, no Bash), so it can't accidentally modify your code while reviewing it. It follows your specific review checklist rather than generic review heuristics.

Custom agents are particularly powerful for teams. Define agents for your team's specific concerns — performance review, accessibility audit, API contract verification — and every team member gets consistent, specialized review.

The `model` field lets you choose the right model for the agent's task. Use a faster, cheaper model for simple checks and a more capable model for complex analysis. The `tools` field restricts what the agent can do — a reviewer that can only read is safer than one that can also edit.

> **Tip:** Start with background agents before exploring worktrees. The simplest parallel workflow is "run tests in the background while I keep coding." Once that feels natural, add worktrees for feature isolation. `/batch` is the advanced tool — reach for it when you have 10+ similar changes to make. Build your parallelism skills incrementally.

---
