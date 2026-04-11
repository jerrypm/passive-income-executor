## Chapter 15: Custom Skills & Superpowers

Every developer has workflows they repeat. Deploy to production. Review a pull request. Set up a new microservice. Debug a performance issue. These workflows have steps, checks, and decisions that you've refined over time — but they live in your head or in scattered documentation.

Skills turn these workflows into reusable recipes that Claude Code follows precisely. Instead of remembering "run tests, then build, then deploy, then verify the health endpoint, then check the logs," you invoke a skill and Claude Code executes the entire workflow. Skills are one of Claude Code's most underused features, and for teams, they're transformative.

### What Skills Are

A skill is a markdown file with structured instructions that Claude Code loads and follows when invoked. Think of skills as "runbooks for AI" — step-by-step procedures that Claude Code executes with full access to your codebase and tools.

Skills differ from CLAUDE.md instructions in two important ways. First, skills are loaded on demand — they don't consume context until you invoke them. Second, skills have metadata that controls when and how they run, including tool permissions, model selection, and activation conditions.

You invoke skills with a slash command:

```
/deploy
```

Or by describing a task that matches a skill's description — Claude Code recognizes the match and loads the appropriate skill automatically.

### Built-in Skills

Claude Code ships with a library of built-in skills that cover common development workflows. You don't need to create these — they're available immediately.

**`/brainstorming`** — Structured creative exploration. Before building a feature, this skill guides you through requirements gathering, constraint identification, and approach evaluation. It prevents the common mistake of jumping into code before understanding what you're building.

```
/brainstorming — I need to add multi-tenancy to our SaaS app
```

The skill asks targeted questions: What isolation level do you need? Shared database or separate? How do tenants authenticate? What data is tenant-specific vs global? By the end, you have a clear specification rather than a vague idea.

**`/writing-plans`** — Detailed implementation plans. Takes a feature specification and produces a step-by-step plan with file changes, dependency analysis, risk assessment, and testing strategy. The plan is concrete enough to hand to an executing agent or follow manually.

**`/executing-plans`** — Step-by-step plan execution with review checkpoints. Reads a plan (from a file or conversation) and executes it incrementally, pausing at checkpoints for your review. Useful for complex changes where you want to verify each stage before proceeding.

**`/test-driven-development`** — Red-green-refactor cycle. Writes failing tests first, then implements the code to make them pass, then refactors. This skill enforces TDD discipline even when you're tempted to skip straight to implementation.

**`/systematic-debugging`** — Methodical investigation framework. Instead of random hypothesis testing, this skill follows a structured debugging process: reproduce, isolate, identify root cause, verify fix, check for similar issues. It prevents the common trap of fixing symptoms instead of causes.

**`/verification-before-completion`** — Verify before claiming done. This skill runs after implementation to confirm that everything actually works — tests pass, the feature behaves correctly, edge cases are handled. It catches the "it compiles so it must work" false confidence.

**`/simplify`** — Reviews recent changes for unnecessary complexity, code duplication, and optimization opportunities. A post-implementation cleanup pass that catches over-engineering.

**`/batch`** — Parallel changes across multiple worktrees, as covered in Chapter 14.

These built-in skills chain naturally. A typical workflow for a new feature:

```
/brainstorming → /writing-plans → /executing-plans → /verification-before-completion
```

Each skill builds on the output of the previous one. Brainstorming produces requirements. Writing-plans produces a plan from those requirements. Executing-plans implements the plan. Verification confirms it works.

### How Skills Work Under the Hood

A skill is a markdown file with optional YAML frontmatter. When invoked, Claude Code loads the file's content as instructions and follows them for the duration of the task. The instructions can include steps, decision trees, checklists, and code templates.

Here's the structure:

```yaml
---
name: my-skill
description: What this skill does (Claude reads this to match tasks)
allowed-tools: Bash(npm *) Bash(git *) Edit Read
---

## Instructions

The actual workflow steps go here.
Claude Code follows these as its guide.
```

The frontmatter controls metadata. The markdown body contains the workflow. Claude Code reads both and executes the workflow using the permitted tools.

Skills are loaded only when invoked — they don't consume context during normal conversation. This means you can have dozens of skills defined without any performance penalty. Only the active skill's instructions occupy context space.

### Creating Your Own Skills

Custom skills live in your home directory or your project:

- **Personal skills:** `~/.claude/skills/skill-name/SKILL.md`
- **Project skills:** `.claude/skills/skill-name/SKILL.md`

Personal skills are available in every project. Project skills are available only in that project and can be committed to git for the whole team.

Here's a practical example — a deployment skill:

```yaml
---
name: deploy
description: Deploy the application to production
allowed-tools: Bash(npm *) Bash(git *) Bash(curl *) Read
---

## Pre-deployment Checks

1. Verify all tests pass:
   ```bash
   npm test
   ```
   If any test fails, STOP and report the failure. Do not proceed.

2. Verify the build succeeds:
   ```bash
   npm run build
   ```

3. Check for uncommitted changes:
   ```bash
   git status --porcelain
   ```
   If there are uncommitted changes, STOP and ask the user to commit first.

4. Verify you're on the main branch:
   ```bash
   git branch --show-current
   ```
   If not on main, STOP and warn the user.

## Deploy

5. Deploy:
   ```bash
   npm run deploy
   ```

## Post-deployment Verification

6. Wait 30 seconds for deployment to propagate.

7. Check the health endpoint:
   ```bash
   curl -sf https://api.example.com/health
   ```
   If the health check fails, immediately report and suggest rollback.

8. Check the version endpoint:
   ```bash
   curl -sf https://api.example.com/version
   ```
   Verify the deployed version matches the current git commit.

## Report

Summarize: what was deployed, which commit, health check status, any warnings.
```

Now `/deploy` executes this entire workflow. Every deployment follows the same process — tests, build, branch check, deploy, health verification. No steps forgotten, no checks skipped.

### Skill Features in Depth

The frontmatter supports several powerful features:

| Feature | Purpose | Example |
|---------|---------|---------|
| `description` | Tells Claude when to use the skill | `"Deploy to production with safety checks"` |
| `allowed-tools` | Pre-approve tools (no permission prompts) | `Bash(npm *) Edit Read Grep` |
| `model` | Use a specific model for this skill | `claude-sonnet-4-6` |
| `effort` | Set reasoning effort level | `high` |
| `context: fork` | Run in an isolated subagent | Skill doesn't pollute main context |
| `paths` | Only activate for matching file paths | `["src/api/**", "src/services/**"]` |
| `disable-model-invocation` | Only the user can invoke, not Claude | Prevents accidental invocation |

**`allowed-tools`** is particularly important. When a skill specifies allowed tools, those tools don't require user approval while the skill is active. Your deployment skill can run `npm test`, `npm run build`, and `npm run deploy` without pausing for permission at each step. This makes skills feel smooth and automatic rather than interrupted by approval dialogs.

Tool patterns support globs: `Bash(npm *)` allows any npm command. `Bash(git *)` allows any git command. `Bash(curl https://api.example.com/*)` allows curl but only to your API domain. This gives you fine-grained control over what the skill can do.

**`context: fork`** runs the skill in a subagent. The skill's execution doesn't fill your main conversation with tool calls and intermediate output. You see the final result, not the journey. Use this for skills that involve many steps and produce a lot of intermediate output.

**`paths`** restricts when the skill activates. A skill with `paths: ["*.test.ts", "*.spec.ts"]` only triggers when you're working on test files. This prevents skills from activating in the wrong context.

**`disable-model-invocation`** prevents Claude Code from invoking the skill on its own. Without this flag, Claude Code might automatically use a skill when it recognizes a matching task. With the flag, only explicit `/skill-name` invocations trigger it. Use this for destructive skills (deployment, database migrations) where you want human intent.

### Dynamic Context in Skills

Skills can include live data from your environment using shell execution syntax. When Claude Code loads the skill, it runs the embedded commands and injects their output into the instructions.

```markdown
---
name: review-pr
description: Review the current pull request
allowed-tools: Read Grep Glob Bash(gh *)
---

## PR Context

- **Diff:** !`gh pr diff`
- **PR description:** !`gh pr view`
- **Comments:** !`gh pr view --comments`
- **CI status:** !`gh pr checks`

## Review Instructions

Review the diff above for:
1. Logic errors and edge cases
2. Security vulnerabilities
3. Performance concerns
4. Test coverage gaps
5. Code style consistency

Provide feedback organized by severity: critical, warning, suggestion.
```

The `!` backtick syntax executes the command when the skill loads. By the time Claude Code starts following the instructions, it has the full PR diff, description, comments, and CI status in context. The review is grounded in actual PR data, not hypothetical code.

This makes skills context-aware. A deployment skill can check the current branch and environment. A review skill can load the actual diff. A debugging skill can capture recent error logs. The skill's instructions adapt to the current state of your project.

### String Substitutions

Skills support variable substitutions for dynamic behavior:

- **`$ARGUMENTS`** — Everything the user typed after the skill name. `/deploy staging` makes `$ARGUMENTS` equal to `"staging"`.
- **`$0`** — The full argument string (alias for `$ARGUMENTS`).
- **`$1`, `$2`, ...** — Individual arguments, space-separated. `/deploy staging --force` makes `$1` = `"staging"` and `$2` = `"--force"`.
- **`${CLAUDE_SESSION_ID}`** — Unique ID for the current session. Useful for creating unique filenames or log entries.
- **`${CLAUDE_SKILL_DIR}`** — The directory containing the skill file. Useful for referencing helper scripts or templates that ship alongside the skill.

Here's a skill that uses arguments:

```yaml
---
name: new-service
description: Scaffold a new microservice
allowed-tools: Bash(*) Edit Write Read
---

## Create Service: $1

1. Create directory structure:
   ```
   src/services/$1/
   ├── index.ts
   ├── routes.ts
   ├── service.ts
   ├── types.ts
   └── __tests__/
       └── service.test.ts
   ```

2. Use the template files in ${CLAUDE_SKILL_DIR}/templates/ as starting points.

3. Register the service in src/services/index.ts.

4. Add a health check route at GET /$1/health.
```

Invoking `/new-service payments` scaffolds a complete payments microservice. The skill knows where to put it, what files to create, and how to register it — all from the instructions.

### When Skills Shine

Skills deliver the most value in four scenarios:

**Repeatable workflows.** Deployment, release management, database migration, environment setup. Any workflow you do more than twice should be a skill. The first time you write the skill takes 10 minutes. Every subsequent execution saves 15-30 minutes and eliminates human error.

**Team standards.** When your team has specific processes — PR review checklists, code style requirements, architecture patterns — skills encode them into executable instructions. New team members don't need to learn the process from documentation. They invoke the skill and Claude Code guides them through it.

**Complex processes with many steps.** Some workflows have 10+ steps, conditional branches, and verification checks. Humans forget steps. Humans skip checks. Skills don't. A deployment skill that checks 8 things before deploying will check 8 things every time.

**Onboarding.** New developers on a team can invoke skills to understand how things work. `/setup-dev-environment` configures everything. `/architecture-overview` explains the codebase. `/add-feature` scaffolds a new feature following team conventions. Skills accelerate onboarding from weeks to days.

### Building a Skill Library

Start with one skill for your most painful repeated workflow. Deploy it, use it for a week, refine it based on experience. Then add a second skill for your second-most painful workflow. Build your library incrementally rather than trying to skill-ify everything at once.

A typical mature skill library:

```
~/.claude/skills/
├── deploy/SKILL.md            ← Production deployment
├── new-component/SKILL.md     ← Scaffold React component
├── new-api-route/SKILL.md     ← Scaffold API endpoint
├── review-security/SKILL.md   ← Security-focused review
└── debug-performance/SKILL.md ← Performance investigation

.claude/skills/  (project-specific, committed to git)
├── setup-dev/SKILL.md         ← Dev environment setup
├── run-migrations/SKILL.md    ← Database migration workflow
└── release/SKILL.md           ← Release process
```

Personal skills in `~/.claude/skills/` travel with you across projects. Project skills in `.claude/skills/` travel with the repository and are shared with the team. The combination gives you personal productivity and team consistency.

> **Tip:** When writing a skill, be explicit about failure conditions. Don't just say "run the tests." Say "run the tests. If any test fails, STOP and report the failure. Do not proceed to the next step." Claude Code follows instructions literally — if you don't specify what to do on failure, it might continue past a broken step. Every step in a skill should have a clear success condition and a clear failure action.

---
