## Chapter 20: Your Custom Setup Blueprint

You've learned the individual pieces — CLAUDE.md, memory, hooks, MCP servers, skills, permissions, prompt patterns, debugging workflows, cost management. This final chapter ties them all together into a complete, personalized setup that makes Claude Code feel less like a tool and more like a team member who knows your codebase, your preferences, and your workflows.

The difference between a beginner and an expert Claude Code user isn't knowledge. It's configuration. The expert configured their environment once and benefits from it every single session. This chapter gives you the blueprint to do the same.

### The Complete Setup Checklist

Work through this list over the coming weeks. You don't need to do everything at once — each item adds value independently.

- [ ] Global `CLAUDE.md` with your personal preferences and coding style
- [ ] Project `CLAUDE.md` with project-specific rules, conventions, and architecture notes
- [ ] Permission allowlists for commands you run frequently (`npm test`, `git commit`, etc.)
- [ ] `.claudeignore` to exclude generated files, lock files, and build artifacts
- [ ] PostToolUse hook for automatic code formatting on every edit
- [ ] At least one MCP server connected (database, GitHub, or project-specific)
- [ ] Custom keybindings for your most-used actions
- [ ] Auto-memory enabled for persistent context across sessions
- [ ] One custom skill for your most repeated workflow
- [ ] Three-layer settings hierarchy configured (global, project, local)

Each checked box removes friction from your daily workflow. Permissions stop interrupting you. Formatting happens automatically. Memory means you never re-explain your project. The compound effect is substantial.

### Starter Global CLAUDE.md Template

This file lives at `~/.claude/CLAUDE.md` and applies to every project you open. Keep it focused on universal preferences — language, style, and behavior that don't change between projects.

```markdown
# Global Preferences

## Coding Style
- Use TypeScript strict mode. No `any` types.
- Prefer `const` over `let`. Never use `var`.
- Use early returns over nested if-else.
- Descriptive variable names. No single-letter variables except loop counters.

## Behavior
- Always use Edit for modifying existing files, Write only for new files.
- Run tests after making changes. Don't tell me it "should work."
- When committing, use conventional commits (feat:, fix:, refactor:, etc.).
- Keep explanations brief. I'll ask if I need more detail.

## Don't
- Don't add comments explaining obvious code.
- Don't refactor unrelated code when fixing a bug.
- Don't use console.log for debugging — use proper error handling.
- Don't create documentation files unless I ask for them.
```

This template is 15 lines of actual rules. Every rule is actionable and specific. "Use early returns over nested if-else" changes how Claude Code writes every function. "Always use Edit for modifying existing files" saves tokens on every file change. These rules compound across thousands of interactions.

Customize this template to match your real preferences. If you prefer Python, replace the TypeScript rules. If you like verbose explanations, remove the brevity rule. The template is a starting point, not a prescription.

### Starter Settings.json Template

This file lives at `.claude/settings.json` in your project root. Commit it to git so your team shares the same configuration.

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(npm test *)",
      "Bash(npm run lint *)",
      "Bash(npm run build *)",
      "Bash(npx prisma *)",
      "Bash(git (add|commit|status|diff|log|push|branch) *)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATH 2>/dev/null || true"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

This template does three things. The permission allowlist auto-approves safe commands — reading files, running tests, building, and standard git operations — so Claude Code doesn't pause for approval on routine actions. The PostToolUse hook runs Prettier on every file Claude Code edits, ensuring consistent formatting without you thinking about it. The MCP server connects Claude Code to your PostgreSQL database so it can inspect schemas, run queries, and understand your data model directly.

Replace `prettier` with your formatter (`black`, `gofmt`, `rustfmt`). Replace `postgres` with your database. Adjust the git pattern if you want tighter restrictions (removing `push`, for example, to require manual approval for pushes).

The `|| true` after the prettier command prevents the hook from blocking Claude Code if formatting fails (for example, on a non-code file). Without it, a formatter error on a markdown file would halt the session.

### Recommended MCP Servers by Stack

MCP servers extend what Claude Code can access. The right servers depend on your technology stack.

**Web development (Next.js, React, Node.js):**
- **GitHub MCP** — Create PRs, manage issues, review code, check CI status without leaving Claude Code
- **PostgreSQL/MySQL MCP** — Query your database, inspect schemas, understand data relationships
- **Puppeteer MCP** — Browser automation for testing UI flows, taking screenshots, verifying deployments

**Mobile development (iOS, Android, React Native):**
- **GitHub MCP** — Same benefits as web
- **Firebase MCP** — Manage Firestore collections, check authentication setup, review security rules
- **SQLite MCP** — Inspect local databases, debug data persistence issues

**Data science and ML:**
- **SQLite MCP** — Query local datasets, inspect feature stores
- **Filesystem MCP** — Navigate large data directories, manage experiment outputs
- **Custom analysis MCP** — Wrap your analysis scripts as MCP tools for repeatable investigations

**DevOps and infrastructure:**
- **GitHub MCP** — Monitor deployments, review infrastructure PRs
- **Docker MCP** — Manage containers, inspect logs, debug service connectivity
- **AWS/GCP/Azure MCP** — Check cloud resources, review configurations, monitor costs

Start with one MCP server — whichever addresses your biggest daily friction point. GitHub is the most universally useful. Add more as you discover needs.

### Building Your Setup Over Time

Don't configure everything in one sitting. Build your setup progressively, validating each addition before layering the next.

**Week 1: Foundation.** Create your global `CLAUDE.md` with 5-10 personal rules. Create a project `CLAUDE.md` with your project's key conventions. Add a basic permission allowlist for read operations and test commands. This alone transforms the experience — Claude Code follows your style and stops interrupting for routine approvals.

**Week 2: Formatting hook.** Add the PostToolUse hook for your formatter. From this point on, every file Claude Code touches is automatically formatted. No more inconsistent code style. No more manual formatting passes. This is the single highest-ROI configuration you can add.

**Week 3: MCP servers.** Connect your primary database and GitHub. Claude Code can now query your data model directly (no more "what columns does the users table have?") and manage PRs without leaving the terminal. These two connections eliminate the most common context-switching interruptions.

**Week 4: Keybindings and workflow optimization.** Customize keybindings for actions you repeat often. Review your first month's usage — which prompts do you type repeatedly? Which tasks follow the same pattern? Identify candidates for skills.

**Month 2: First custom skill.** Take your most repeated workflow — deployment, PR review, feature scaffolding — and encode it as a skill. Use it for two weeks. Refine based on experience. A single well-built skill saves 10-20 minutes per use.

**Month 3: Advanced automation.** Set up scheduled agents for recurring tasks (dependency updates, daily PR reviews). Add path-specific rules for different parts of your codebase. Connect additional MCP servers. At this point, your setup is mature and Claude Code operates with deep knowledge of your project, your tools, and your preferences.

### Before and After

The difference between an unconfigured and a configured Claude Code setup is stark. Here's what changes.

**Before — out of the box:**
- Claude Code asks permission for every `npm test`, every `git status`, every file read
- Code it writes uses its own style conventions, not yours
- Every new session starts from zero — no memory of your project, your preferences, or previous decisions
- You manually format code after every edit
- You switch to a browser for GitHub operations, database queries, and documentation lookups
- Generic responses that don't account for your project's architecture or conventions

**After — fully configured:**
- Routine commands run automatically; permissions only pause for genuinely dangerous operations
- Every line of code matches your team's style because CLAUDE.md defines it and hooks enforce it
- Memory persists across sessions — Claude Code remembers your architecture decisions, naming conventions, ongoing work, and known issues
- Code is auto-formatted the instant Claude Code saves a file
- GitHub PRs, database queries, and external tools are accessible directly from the conversation
- Responses are project-aware: Claude Code knows your framework, your patterns, your testing conventions, and your deployment process
- One-keypress commits, one-command deployments, automated quality checks

The unconfigured experience feels like working with a capable stranger. The configured experience feels like working with a team member who has read your entire codebase, attended every architecture meeting, and remembers everything.

### The Compound Effect

Each individual configuration saves a small amount of time. Permission allowlist: 2 seconds per approval, maybe 50 approvals per day — less than 2 minutes saved. Formatting hook: 5 seconds per manual format, 30 times per day — 2.5 minutes. Memory: 1 minute re-explaining context per session, 5 sessions per day — 5 minutes.

Individually, these feel insignificant. Combined, they save 30-45 minutes per day. Over a month, that's 10-15 hours. Over a year, it's 25-35 full working days. And the quality improvement compounds too — consistent formatting, persistent memory, and project-aware responses mean fewer bugs, less rework, and cleaner code.

The developers who report the highest satisfaction with Claude Code aren't the ones using the most advanced features. They're the ones with the best configurations. They spent 2 hours setting things up and now save 30 minutes every day, forever.

### Your Next Step

Close this book. Open your terminal. Create `~/.claude/CLAUDE.md` with five rules that matter to you. That's it — five rules. Use Claude Code for a day with those rules active and notice the difference.

Then add a permission allowlist. Then a formatting hook. Then a project CLAUDE.md. Each addition takes 5 minutes and improves every session that follows.

You now have everything you need to use Claude Code at an expert level. The knowledge is in the previous 19 chapters. The execution starts with one file, five rules, and the decision to configure your tools instead of accepting their defaults.

The difference between a developer and a 10x developer has never been typing speed. It's tooling, automation, and the discipline to invest 10 minutes of setup for 10 hours of payoff.

Configure once. Benefit forever.

---
