## Chapter 4: Understanding Permission Modes

Claude Code can read your files, rewrite them, and execute arbitrary shell commands. That's what makes it powerful — and it's exactly why permissions exist. This chapter explains the permission system that lets you control how much autonomy Claude Code has, from "ask me everything" to "handle it all."

### Why Permissions Exist

Every time Claude Code wants to do something beyond reading files and searching, it needs your approval — unless you've configured it otherwise. This is a deliberate safety design:

- **File edits** change your source code
- **Shell commands** can install packages, delete files, modify system state
- **Git operations** can push to remote repositories

Permissions let you decide where on the spectrum between "manual approval for everything" and "full autonomy" you want to operate. There's no single right answer — it depends on the task, the project, and your comfort level.

### The Permission Modes

Claude Code has four distinct permission modes. You can switch between them at any time.

#### Ask Mode (Default)

```
Permission level: Most restrictive
```

In Ask mode, Claude Code requests your approval before every file edit and every shell command. It can freely read files, search with Glob and Grep, and analyze code, but any action that changes state requires a "yes" from you.

This is the default for good reason — it's how you learn what Claude Code does under the hood. You see every tool call, every edit, every command before it executes. After a few sessions in Ask mode, you'll develop intuition for when Claude Code needs more freedom.

**When to use Ask mode:**

- First week of using Claude Code (learning phase)
- Working in sensitive codebases (production configs, infrastructure)
- When you want to review every change before it happens
- Pair-programming style: you direct, Claude Code proposes, you approve

#### Auto-edit Mode

```
Permission level: Moderate
```

Auto-edit mode automatically approves file edits but still asks before running shell commands. This is the sweet spot for most daily development work.

The reasoning is practical: file edits are easily reversible with `git checkout` or undo, but shell commands can have side effects that are harder to reverse (installing packages, modifying databases, pushing to remote).

**When to use Auto-edit mode:**

- Daily feature development
- Refactoring sessions
- Bug fixes where you trust Claude Code's edits but want to control what runs

#### Full-auto Mode

```
Permission level: Most permissive
```

Full-auto mode lets Claude Code edit files, run commands, and execute multi-step workflows without asking. It will still pause before certain dangerous operations (more on that in the safety section below).

This mode is remarkably productive for well-defined tasks. You describe what you want, press Enter, and come back to find the feature implemented, tested, and ready for review.

```
Full auto: Add pagination to the /api/users endpoint. Include offset 
and limit query params, default to 20 items per page, and add tests.
```

In full-auto mode, Claude Code will plan, implement, create tests, run them, fix any failures, and report back — all without interrupting you.

**When to use Full-auto mode:**

- Executing a plan you've already reviewed
- Repetitive tasks across many files
- Tasks where the scope is well-defined and low-risk
- Prototyping and exploration in a throwaway branch

> **Tip:** Full-auto mode pairs well with git branches. Create a branch, switch to full-auto, let Claude Code implement the feature, then review the diff before merging. If you don't like the result, delete the branch. Zero risk.

#### Plan Mode

```
Permission level: Read-only
```

Plan mode is the opposite of full-auto. Claude Code can read, search, and analyze your entire codebase, but it cannot modify any files or run any commands. It proposes changes in detail without executing them.

This is the code review and architecture analysis mode. Claude Code will describe exactly what it would change, in which files, and why — but the actual execution is up to you.

**When to use Plan mode:**

- Code review: "Review the changes in this PR and flag issues"
- Architecture analysis: "How would you restructure the auth system?"
- Learning: "Explain how the caching layer works and what you'd improve"
- Sensitive systems where even file reads should be the only automated action

### Allowlists and Denylists

For finer control than the four modes provide, Claude Code supports allowlists and denylists in `settings.json`. These let you pre-approve or permanently block specific tools and commands.

#### Allowing Specific Commands

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(npm test)",
      "Bash(npm run build)",
      "Bash(npm run lint)",
      "Bash(git status)",
      "Bash(git diff *)"
    ]
  }
}
```

With this configuration, Claude Code can always run tests, build, lint, and check git status without asking — even in Ask mode. Everything else still requires approval.

#### Blocking Dangerous Commands

```json
{
  "permissions": {
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force *)",
      "Bash(DROP TABLE *)",
      "Edit(.env)"
    ]
  }
}
```

Denied tools are blocked regardless of permission mode. Even in full-auto, Claude Code cannot execute denied commands.

#### Pattern Matching

Allowlists and denylists support glob-style patterns:

| Pattern | Matches |
|---------|---------|
| `Bash(npm *)` | Any npm command |
| `Bash(git status)` | Exact match only |
| `Bash(docker *)` | Any Docker command |
| `Edit(*.test.ts)` | Edits to test files only |
| `Edit(src/*)` | Edits within the src directory |

This gives you surgical control. You can auto-approve Claude Code to run tests and edit source files while requiring approval for package installation and deployment commands.

### Three Layers of Settings

Settings cascade through three layers, from broadest to most specific:

| Layer | File Location | Applies To | Share With Team? |
|-------|--------------|-----------|-----------------|
| **Global** | `~/.claude/settings.json` | All projects on your machine | No (personal) |
| **Project** | `.claude/settings.json` | This repository | Yes (commit it) |
| **Local** | `.claude/settings.local.json` | This repo, only you | No (gitignored) |

**Global settings** are your personal defaults. If you always want `npm test` to be auto-approved, put it here.

**Project settings** are shared with your team. If your project uses a specific test runner or has commands that are always safe, define them here so everyone gets the same experience. This file should be committed to your repository.

**Local settings** are your personal overrides for a specific project. Maybe you trust full-auto in this repo even though the team default is Ask mode. This file is automatically gitignored.

Settings merge with increasing specificity. A project-level deny overrides a global-level allow. A local-level setting overrides both.

```
Global: allow Bash(npm test)
Project: deny Bash(npm run deploy)  
Local: allow Bash(npm run deploy)
→ Result: npm test is allowed, npm run deploy is allowed (local override)
```

### When to Use Each Mode — Decision Guide

| Situation | Recommended Mode |
|-----------|-----------------|
| First week with Claude Code | Ask |
| Learning a new codebase | Plan or Ask |
| Daily feature development | Auto-edit |
| Writing tests for existing code | Auto-edit or Full-auto |
| Refactoring with confidence | Full-auto (on a branch) |
| Running a known implementation plan | Full-auto |
| Rapid prototyping | Full-auto |
| Working in production infrastructure | Ask |
| Code review | Plan |
| Architecture discussion | Plan |

Most experienced Claude Code users land on **Auto-edit as default** with specific commands allowlisted (tests, builds, linting). They switch to Full-auto for well-scoped tasks on feature branches and drop to Ask mode when working near sensitive code.

### Built-in Safety Rails

Even in the most permissive mode, Claude Code maintains safety boundaries:

- **Never force-pushes** to a remote repository without explicit confirmation
- **Never deletes branches** without asking
- **Warns before committing sensitive files** (`.env`, credentials, API keys)
- **Respects hooks** — the hook system (Chapter 10) acts as an enforcement layer above permissions. A pre-commit hook that runs linting cannot be bypassed, regardless of permission mode
- **Respects deny rules** — denied tools are never executed, period
- **Pauses on destructive operations** — commands that could cause irreversible damage (`rm -rf`, `DROP TABLE`, `git reset --hard`) trigger additional confirmation

These safety rails mean that full-auto mode is significantly less dangerous than it might sound. Claude Code is designed to be aggressive about productivity and conservative about irreversible actions.

### Changing Modes Mid-Conversation

You don't have to decide your permission mode at the start of a session. Switch freely as the situation changes:

```
# Check current mode
/permissions

# Switch to auto-edit  
/auto-edit

# Switch to plan mode for review
/plan

# Go full auto for implementation
/auto
```

A common workflow: start in Plan mode to discuss an approach, switch to Auto-edit for implementation, then switch to Full-auto for running tests and fixing failures. This gives you maximum control when it matters and maximum speed when it's safe.

> **Tip:** If you accidentally approve a command you didn't mean to, `Ctrl+C` cancels it immediately. For file edits, `git diff` shows you exactly what changed, and `git checkout -- filename` reverts it. You always have an undo button.

### Practical Configuration Example

Here's a real-world `settings.json` that balances productivity and safety:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(npm test *)",
      "Bash(npm run build)",
      "Bash(npm run lint *)",
      "Bash(npx tsc --noEmit)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(git log *)",
      "Bash(git branch *)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force *)",
      "Bash(git reset --hard *)",
      "Edit(.env*)",
      "Edit(*secret*)",
      "Edit(*credential*)"
    ]
  }
}
```

This configuration says: "Claude Code can always read, search, test, build, lint, and check git state. It can never force-push, hard-reset, or touch secrets files. Everything else — ask me first."

That's a solid foundation. You'll refine it over time as you learn which commands you always approve and which you always want to review.

---
