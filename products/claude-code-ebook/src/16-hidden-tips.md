## Chapter 16: 50 Hidden Tips & Tricks Most Developers Don't Know

This is the chapter you came for. These aren't in the getting-started guide. They're collected from expert usage, documentation deep-dives, and real-world workflows. If you already know more than ten of these, you're in the top 1% of Claude Code users.

### Speed & Efficiency

**1. The `!` prefix runs shell commands inline.**
Type `!` followed by any shell command and the output lands directly in your conversation context. Claude sees it immediately and can act on it. Faster than switching terminals and pasting output.

```
! git log --oneline -5
! ls src/components/
! npm test -- --grep "auth"
```

**2. `/fast` uses the same model — it's not a downgrade.**
Many think fast mode switches to a weaker model. It doesn't — same Claude, optimized for faster output with slightly less thoroughness. Use it for straightforward tasks like renaming variables or adding imports. Switch back for architecture decisions.

```
/fast
rename the variable `data` to `userProfile` across all files in src/
```

**3. `Shift+Tab` cycles models instantly.**
Switch between Opus, Sonnet, and Haiku mid-conversation without restarting. Use Haiku for quick questions, Sonnet for standard tasks, Opus for complex architecture. Haiku costs roughly 1/60th of Opus — strategic switching cuts your bill dramatically.

```
Shift+Tab  →  cycles: Opus → Sonnet → Haiku → Opus
```

**4. `/compact` accepts a focus argument.**
Most developers use `/compact` bare and let Claude decide what to keep. Add a focus argument to control what matters most during compression. Without it, Claude might discard exactly the context you need next.

```
/compact focus on the authentication refactor and the database schema changes
/compact keep all the API endpoint signatures and test results
```

**5. Pipe mode for one-shot queries.**
The `-p` flag pipes stdin directly into Claude and prints the result to stdout. No interactive session needed. This is transformative for integrating Claude into shell workflows — it composes with any Unix tool.

```bash
git diff | claude -p "review this diff for bugs"
cat error.log | claude -p "what's causing these failures?"
git log --oneline -20 | claude -p "categorize these commits" | pbcopy
```

**6. `claude --print` for non-interactive scripting.**
Pass a prompt directly and get the result on stdout. No interactive session, no stdin needed. The `-o json` flag forces JSON output for script consumption.

```bash
claude --print "what node version does this project use?"
claude --print -o json "list all TODO comments in src/" > todos.json
```

**7. Resume any conversation with `--resume`.**
Every conversation is automatically saved. Resume with full context — files read, decisions made, plans discussed — exactly where you left off. You can close your terminal, reboot your machine, or switch projects and pick up right where you were. Name important sessions so you can find them later.

```bash
claude --resume                    # resume last conversation
claude -r                          # shorthand
claude --resume "auth-refactor"    # resume a named session
```

**8. `@filename` forces a file into context.**
The `@` prefix explicitly loads a file into context. Use it when Claude's suggestions don't match your conventions — force it to see the reference file. You can reference multiple files in one prompt.

```
@src/auth/middleware.ts why doesn't the new route handler follow this pattern?
@src/types.ts @src/schema.ts add a new User type matching the database schema
```

**9. Edit is 10x cheaper than Write.**
Edit sends only the diff. Write sends the entire file. For a 500-line file where you're changing 3 lines, Edit transmits ~10 lines while Write transmits all 500. Reinforce this in your CLAUDE.md:

```markdown
# Rules
- Always use Edit for modifying existing files
- Only use Write for creating new files
```

**10. Parallel tool calls happen automatically.**
When Claude needs to read 5 files, it reads all 5 simultaneously — not sequentially. You don't configure this; it's built into the architecture. The same applies to searches: multiple grep operations fire in parallel. Give Claude the full list and it analyzes everything together in one round-trip.

```
Check these files for inconsistent error handling:
src/api/users.ts, src/api/orders.ts, src/api/payments.ts,
src/api/inventory.ts, src/api/notifications.ts
```

### Configuration Secrets

**11. Three layers of settings merge top-down.**
Claude Code has three config files that merge in a specific order. Understanding this hierarchy is essential for teams. Project settings override global and are shared via git. Local settings override everything and stay private.

```
~/.claude/settings.json          # Global (your machine)
.claude/settings.json            # Project (commit this to git!)
.claude/settings.local.json      # Local (gitignored, personal overrides)
```

**12. Allowlist specific commands with regex.**
`permissions.allow` accepts patterns, not just exact strings. Auto-approve safe command families while keeping destructive ones gated.

```json
{
  "permissions": {
    "allow": [
      "Read", "Glob", "Grep",
      "Bash(npm test *)",
      "Bash(git (add|commit|status|diff|log) *)",
      "Bash(cargo (build|test|clippy) *)"
    ]
  }
}
```

The git pattern allows common operations but still requires approval for `git reset --hard` or `git push --force`.

**13. `.claudeignore` hides files from Claude.**
Create a `.claudeignore` file in your project root with the same syntax as `.gitignore`. Claude won't read, search, or reference matching files. This reduces noise, protects sensitive data, and keeps context focused. A 50,000-file monorepo with proper `.claudeignore` behaves like a focused 2,000-file project.

```
# .claudeignore
node_modules/
dist/
build/
*.lock
*.min.js
coverage/
.env*
vendor/
```

**14. Custom keybindings.**
Remap any shortcut in `~/.claude/keybindings.json`. Supports modifiers and VS Code-style chord bindings (press one combo, release, press another).

```json
[
  { "key": "ctrl+l", "command": "clear" },
  { "key": "ctrl+k ctrl+c", "command": "compact" },
  { "key": "ctrl+shift+p", "command": "plan" },
  { "key": "ctrl+d", "command": "diff" }
]
```

**15. Auto-format every file Claude edits.**
One PostToolUse hook and every file Claude modifies gets auto-formatted. Replace `prettier` with `black`, `gofmt`, or `rustfmt` as needed.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATH"
          }
        ]
      }
    ]
  }
}
```

**16. Desktop notifications when Claude needs attention.**
Set up a Notification hook and get alerted when Claude pauses for input. On Linux, replace `osascript` with `notify-send`.

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"$CLAUDE_NOTIFICATION\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

**17. Project-scoped MCP servers vs global ones.**
MCP servers in `.claude/settings.json` are project-scoped — they load only when you're in that project and are shared with your team via git. MCP in `~/.claude/settings.json` loads everywhere. Connection strings and secrets go in `settings.local.json` (gitignored). This gives your team shared tooling with private credentials.

```json
// .claude/settings.json (committed, shared with team)
{
  "mcpServers": {
    "team-database": {
      "command": "npx",
      "args": ["@team/db-mcp-server"],
      "env": { "DB_URL": "${DB_URL}" }
    }
  }
}
```

**18. `claude config set` from the terminal.**
Configure without editing JSON. Respects the three-layer hierarchy — without `--global`, writes to project config; with it, writes to `~/.claude/settings.json`.

```bash
claude config set permissions.allow '["Read","Glob","Grep"]'
claude config set --global theme "dark"
claude config list
```

**19. Multiple CLAUDE.md files merge automatically.**
Claude Code loads and merges instructions from multiple locations. Global for personal preferences, project for team conventions, subdirectory for module-specific rules.

```
~/.claude/CLAUDE.md              # Global (all projects)
./CLAUDE.md                      # Project root (team conventions)
./src/CLAUDE.md                  # Subdirectory (module-specific rules)
```

**20. Path-specific rules with frontmatter.**
Create markdown files in `.claude/rules/` with `paths:` frontmatter. These rules only activate when Claude works on matching files. Non-matching rules are invisible — they consume zero context. This scales beautifully for large projects with varied conventions across modules.

```yaml
---
paths: ["src/api/**/*.ts"]
---
All API handlers must validate input using Zod schemas.
Return standardized error responses using ApiError class.
```

```yaml
---
paths: ["**/*.test.ts"]
---
Use describe/it blocks. Mock external services, never hit real APIs.
```

### Advanced Workflows

**21. `/init` generates your CLAUDE.md automatically.**
Scans your project structure, package.json, git history, and coding patterns — then generates a comprehensive CLAUDE.md file. The result includes detected language conventions, testing frameworks, build commands, and common patterns. Usually 60-70% correct out of the box. Always review and customize.

```
/init
```

**22. Plan mode prevents wrong paths.**
For complex tasks, ask Claude to plan before coding. It produces a structured breakdown — files to change, order of operations, risks, and testing strategy — without modifying anything. Much cheaper to revise a plan than to undo a half-completed refactor.

```
Plan a refactor of the authentication system to support OAuth2.
Don't change any code yet — just outline the approach.
```

**23. Background agents with `Ctrl+B`.**
Send a task to a background agent that works independently while you continue your main conversation. Perfect for mechanical tasks while you focus on creative work.

```
Main conversation: "Building the payment integration..."
Ctrl+B: "Update all copyright headers to 2026"
# Notification appears when done
```

**24. `/branch` forks your conversation.**
Try two approaches without losing progress. Creates a named checkpoint you can return to if the current path doesn't work.

```
/branch explore-option-A
# ... try approach A, doesn't work? ...
/resume explore-option-A
# ... try approach B from the same starting point
```

**25. `/rewind` jumps to any checkpoint.**
Not just undo — jump to any previous point in the conversation. Think of it as `git checkout` for conversations. Context from that point forward is discarded; you restart from a known good state.

```
/rewind
# Shows a list of checkpoints — select where to return
```

**26. Claude reads images natively.**
Pass a path to any PNG/JPG and Claude sees it visually. This unlocks workflows that would otherwise require manual description: "recreate this UI," "what's wrong with this layout," "match this design." Claude analyzes visual composition — colors, spacing, typography — and generates matching code. Not pixel-perfect, but gets you 80% in one shot.

```
@screenshots/target-design.png recreate this layout in React with Tailwind CSS
```

**27. Claude reads PDFs with page ranges.**
Work directly from specs and documentation in PDF format. Max 20 pages per request — for longer docs, read in chunks.

```
Read pages 12-18 of docs/api-specification.pdf and implement
the user endpoints described there.
```

**28. Side questions with minimal context pollution.**
Need a quick answer mid-task without derailing focus? Frame it as a side question. Keeps your main conversation thread clean.

```
Quick aside: what's the syntax for TypeScript conditional types?
```

**29. `/context` visualizes your context window.**
Shows a breakdown of what's consuming context — CLAUDE.md, history, file contents, tool outputs — with capacity warnings. When approaching 60%, use `/compact` proactively (tip #4).

```
/context
```

**30. `/diff` for visual change review.**
See all session modifications in visual diff format. Your pre-commit review — catch anything unexpected before Claude commits.

```
/diff
# Shows a colored diff of all changes in the session
```

### Hidden Power

**31. The hook feedback loop.**
PostToolUse hooks create automatic feedback loops: Claude edits, hook runs linter, linter reports error, Claude sees it, fixes it, hook runs again, passes. Fully automatic, typically resolves in 1-2 iterations.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "eslint --fix $CLAUDE_FILE_PATH && eslint $CLAUDE_FILE_PATH"
          }
        ]
      }
    ]
  }
}
```

**32. Hooks override ALL permission modes.**
Hooks returning exit code 2 block operations even with `--dangerously-skip-permissions`. Hooks sit above the permission system, not below it — the ultimate safety net. This hook prevents writing to any `.env` file, period. No flag can bypass it.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo $CLAUDE_FILE_PATH | grep -q '.env'; then exit 2; fi"
          }
        ]
      }
    ]
  }
}
```

**33. Claude never amends commits unless explicitly asked.**
When a pre-commit hook fails, the commit didn't happen. If Claude used `--amend` on retry, it would modify the previous (unrelated) commit. So Claude always creates a new commit. Intentional and non-configurable — prevents data loss.

```
# After a failed pre-commit hook:
git add fixed-file.ts
git commit -m "fix: resolve lint errors"   # NEW commit, not --amend
```

**34. Context compression triggers at ~60%, not 95%.**
Automatic compression is aggressive — starts around 60% utilization, not near capacity. If you wait for it, Claude decides what to keep. Proactive compression is a strategy; automatic compression is a safety net.

```
/compact focus on: the API redesign decisions, the new schema,
and the migration strategy we discussed
```

**35. Sub-agents for codebase exploration.**
Instead of manually searching through files, describe what you want to understand. Claude launches a focused investigation — searching, reading, following imports, checking test files for behavior clues, and synthesizing across multiple files. Far more effective than manual grep-and-read cycles.

```
Figure out how the payment processing pipeline works end-to-end.
Trace from the API endpoint through to the database write.
```

**36. `--max-budget-usd` sets a hard spending limit.**
Cap session spending. Once reached, the session ends gracefully. Set low for exploration, higher for known-complex tasks. Essential for teams managing shared budgets.

```bash
claude --max-budget-usd 2.00
claude --max-budget-usd 0.50   # tight budget for quick tasks
```

**37. `--json-schema` forces structured output.**
Constrains output to match your JSON schema exactly. No markdown, no extra text — just valid, parseable JSON. Combine with `--print` for automated pipelines.

```bash
claude -p --json-schema '{
  "type": "object",
  "properties": {
    "bugs": { "type": "array", "items": { "type": "string" } },
    "severity": { "type": "string", "enum": ["low","medium","high"] }
  }
}' "analyze src/auth.ts for bugs"
```

**38. `/schedule` runs tasks on Anthropic's cloud.**
Schedule Claude on a cron — even when your computer is off. Runs on Anthropic infrastructure with access to your connected repositories. Tasks can create issues, leave PR comments, or post summaries depending on what you configure.

```
/schedule "review all open PRs and comment" every weekday at 9am
/schedule "check for outdated dependencies" every monday at 8am
```

**39. Extended cloud planning with deep reasoning.**
Cloud-based planning gives Claude up to 30 minutes of reasoning time. For decisions that affect months of development — service boundaries, database architecture, major migrations.

```
/ultraplan migrate our monolith to microservices —
analyze all 200 endpoints and propose service boundaries
```

**40. `/batch` for mass parallel changes.**
Spawns multiple parallel agents in separate git worktrees. Each handles a subset of files; results are presented as individual reviewable changes. For a 50-file migration, hours become minutes.

```
/batch update all test files from Jest to Vitest syntax
/batch add input validation to every API endpoint
```

### Pro Patterns

**41. "Follow the pattern in X" is the most powerful prompt.**
Reference an existing file and Claude replicates its structure, naming conventions, error handling, and style perfectly. Claude reads the reference file, extracts the pattern — imports, middleware chain, validation approach, response format — and applies it to the new code. Produces more consistent output than any amount of detailed description.

```
Create a new API endpoint for /api/orders.
Follow the exact pattern in src/api/users.ts.
```

**42. Start conversations scoped to a single concern.**
Don't let one conversation handle auth, database optimization, and UI styling. Short, focused conversations produce better results than marathon multi-topic sessions. When in doubt, start fresh.

```bash
# Session 1: Auth refactor
claude → "refactor the authentication middleware..."
# Session 2: Database optimization (new conversation)
claude → "optimize the slow queries in reports..."
```

**43. `!git diff` as context is better than explanation.**
Instead of describing what changed, show Claude the actual diff. More accurate and complete than verbal explanation.

```
!git diff HEAD~3
Review these changes. Are there any bugs or missed edge cases?

!git diff main..feature-branch
Write a comprehensive PR description for these changes.
```

**44. When you deny a tool call, explain why.**
A bare denial forces Claude to guess what went wrong. An explained denial teaches it your preference immediately and adjusts behavior for the rest of the conversation. It's the fastest way to steer Claude's approach.

```
# Weak:
[Deny]

# Strong:
[Deny] — Don't use Write. Use Edit instead — I want the minimal diff.
[Deny] — That file is auto-generated. Modify src/schema.prisma instead.
```

**45. Token cost scales with file size — use offset and limit.**
Reading a 5,000-line file consumes real tokens. If you only need 50 lines, say so. Dramatically cheaper and keeps context cleaner.

```
Read lines 200-250 of src/services/payment.ts — the refund handling logic.
```

**46. `claude doctor` diagnoses configuration problems.**
Checks authentication, config files, MCP servers, and dependencies. Catches expired tokens, misconfigured settings, and incompatible versions. Run it first, debug second.

```bash
claude doctor
```

**47. `.worktreeinclude` copies gitignored files to worktrees.**
When `/batch` spawns agents in worktrees, gitignored files like `.env` don't copy — because they're gitignored. Add them to `.worktreeinclude` at your project root. Without this, parallel agents fail because they can't find environment variables or generated files.

```
# .worktreeinclude
.env
.env.local
src/generated/prisma-client/
```

**48. Track your usage with `/stats`.**
See session counts, token consumption, costs, and streaks. Helps you understand usage patterns and discover which task types cost more than expected.

```
/stats
```

**49. Pre-commit hooks create an automatic quality gate.**
Claude respects git hooks. If a hook fails — linting, type checking, test execution — Claude sees the error output, fixes the issue, stages the fix, and retries the commit. All without your intervention. Strict hooks don't slow Claude down; they make its output more reliable.

```bash
# .husky/pre-commit
npm run lint
npm run typecheck
npm test -- --bail
```

**50. Combine everything into a personalized AI development environment.**
The real power of Claude Code isn't any single feature — it's the combination. CLAUDE.md defines your conventions. Memory preserves knowledge across sessions. Hooks enforce standards automatically. MCP servers connect external tools. Skills encode your workflows. Path-specific rules adapt behavior per module. A fully configured setup doesn't feel like a tool; it feels like a team member who knows your codebase and improves with every session. Chapter 20 shows the complete blueprint for building this from scratch.

```
CLAUDE.md          → What Claude should know
Memory             → What Claude should remember
Hooks              → What Claude must always do
MCP Servers        → What Claude can access
Skills             → How Claude should work
Settings layers    → How your team configures it all
```
