---
title: "Mastering Claude Code"
subtitle: "From Zero to Expert — Including 50 Hidden Features Most Developers Don't Know"
---

# Mastering Claude Code

## From Zero to Expert

*Including 50 Hidden Features Most Developers Don't Know*

---

## About This Book

Claude Code is the most powerful AI coding assistant available today — but most developers barely scratch the surface. They use it to ask questions and edit files, missing the 90% of capabilities that transform it from "helpful chatbot" into an autonomous development partner.

This book takes you from zero to expert in a structured progression. You'll learn not just what Claude Code can do, but how expert developers actually use it — the workflows, the shortcuts, the hidden features, and the prompt patterns that 10x your productivity.

Whether you're installing Claude Code for the first time or you've been using it for months and want to unlock its full potential, this book has something for you.

## How to Use This Book

**Part 1 (Chapters 1-4)** — Start here if you're new. Installation, first tasks, understanding how Claude Code works.

**Part 2 (Chapters 5-8)** — Core productivity. CLAUDE.md, git workflows, code navigation. Read this even if you're experienced — most developers miss key features here.

**Part 3 (Chapters 9-12)** — Advanced power. Memory, hooks, MCP servers, IDE integration. This is where you graduate from "user" to "power user."

**Part 4 (Chapters 13-16)** — Expert secrets. Prompt engineering, parallel development, custom skills, and the crown jewel: 50 hidden tips most developers never discover.

**Part 5 (Chapters 17-20)** — Real-world mastery. Complete case studies, debugging workflows, cost optimization, and building your custom setup.

**Convention:** Code you should type/run appears in dark code blocks. Tips appear in orange-bordered callout boxes.

---


# Part 1: Getting Started

## Chapter 1: What Is Claude Code & Why It's Different

### What Claude Code Is

Claude Code is a CLI-based AI coding assistant built by Anthropic. It runs directly in your terminal, and that distinction matters more than you might think.

Unlike web-based AI chatbots where you copy code snippets back and forth, Claude Code operates inside your development environment. It has direct access to your filesystem, your git history, your shell, and your entire project structure. When you ask it to fix a bug, it reads the actual files, makes surgical edits, runs the tests, and commits the fix — all without you touching a single file.

Think of it this way: traditional AI coding tools are like texting a contractor photos of your broken sink. Claude Code is the contractor standing in your kitchen with a wrench.

You launch it with a single command:

```bash
claude
```

From there, you're in a conversation with an AI that can see everything in your project directory, run any command your shell can run, and modify any file with precision. It's not generating code for you to paste — it's working alongside you, directly in your codebase.

### How It Differs from Other AI Tools

The AI coding tool landscape is crowded. Here's how Claude Code compares to what you might already be using:

| Feature | ChatGPT / Claude.ai | GitHub Copilot | Cursor / Windsurf | Aider / Continue | **Claude Code** |
|---------|---------------------|----------------|-------------------|-----------------|----------------|
| **Interface** | Web browser | Editor extension | Custom editor | Terminal | Terminal / Desktop / IDE |
| **Sees your codebase** | No (paste only) | Current file + neighbors | Full project | Full project | Full project |
| **Edits files directly** | No | Inline suggestions | Yes | Yes | Yes |
| **Runs shell commands** | No | No | Limited | Yes | Full shell access |
| **Git integration** | No | No | Basic | Yes | Deep (commit, PR, branch) |
| **Memory across sessions** | Limited | No | Limited | No | Yes (CLAUDE.md + memory) |
| **Custom automation** | No | No | No | No | Hooks system |
| **Extensible** | Plugins | No | MCP support | No | MCP servers + skills |
| **Sub-agents** | No | No | No | No | Yes (parallel work) |
| **Works with any editor** | N/A | VS Code, JetBrains | Own editor only | VS Code, Neovim | Any editor + terminal |

The key differentiators are depth and autonomy. Copilot completes your current line. Cursor edits your current file. Claude Code handles multi-file refactors, runs your test suite, debugs failures, creates pull requests, and remembers what you told it last week.

### What It Can Actually Do

Here's a concrete breakdown of Claude Code's capabilities:

| Capability | What It Means | Example |
|-----------|--------------|---------|
| **Read files** | Opens any file in your project, displays with line numbers | "Show me the auth middleware" |
| **Edit files** | Surgical find-and-replace edits (not rewriting entire files) | "Add error handling to the login function" |
| **Write files** | Creates new files from scratch | "Create a migration for the users table" |
| **Run commands** | Executes any shell command, captures output | "Run the tests" / "Build the Docker image" |
| **Search by filename** | Glob patterns across the entire project | "Find all TypeScript test files" |
| **Search by content** | Regex search through file contents | "Find everywhere we call the payments API" |
| **Git operations** | Commit, branch, diff, log, create PRs via `gh` CLI | "Commit these changes with a descriptive message" |
| **Read images** | Analyzes screenshots, diagrams, UI mockups | "Here's a screenshot of the bug" |
| **Read PDFs** | Extracts and analyzes PDF content | "Summarize this API spec document" |
| **Read notebooks** | Understands Jupyter notebooks with outputs | "What does this data analysis notebook do?" |
| **Web fetch** | Downloads and reads web pages | "Read the docs at this URL" |
| **Sub-agents** | Spawns parallel workers for independent tasks | "Update all 12 API endpoints to the new format" |
| **Persistent memory** | Remembers context across conversations | CLAUDE.md files + memory system |
| **Custom hooks** | Automated actions triggered by events | Auto-lint before every commit |
| **MCP servers** | Connects to external databases, APIs, services | Query your production database directly |

This isn't a theoretical feature list. Every item above is something you'll use in your daily workflow once you know how.

### The Mental Model

The right mental model for Claude Code is this: **a senior developer sitting next to you who has already read your entire codebase.**

This developer can:

- Instantly recall any file, function, or pattern in your project
- Run any command on your machine
- Make changes across multiple files in a single coordinated operation
- Remember conversations and decisions from previous sessions
- Work on multiple independent tasks simultaneously (via sub-agents)
- Follow your team's conventions automatically (via CLAUDE.md configuration)

But like any developer — even a brilliant one — Claude Code needs your guidance on **what** to build and **why**. It doesn't know your product roadmap. It doesn't know which trade-offs your team prefers. It doesn't know the business context behind a feature request.

The developers who get the most out of Claude Code are the ones who provide clear intent and let it handle the implementation details. Instead of dictating every line of code, they describe the outcome they want and let Claude Code figure out the approach.

Bad prompt: "Add a try-catch block around line 47 of server.js"

Good prompt: "The server crashes when the database is unavailable. Make it handle connection failures gracefully and return a 503 status."

The first tells Claude Code exactly what to type. The second tells it what problem to solve — and it will often find a better solution than you had in mind.

### Available Platforms

Claude Code is available on multiple platforms, each with its own strengths:

| Platform | Best For | Notes |
|----------|---------|-------|
| **CLI (Terminal)** | Power users, server environments | Most capable, full feature set |
| **Desktop App** | Mac and Windows daily development | Native experience, same features as CLI |
| **VS Code Extension** | Developers who live in VS Code | Integrated panel, sees editor context |
| **JetBrains Plugin** | IntelliJ, PyCharm, WebStorm users | IDE integration with Claude Code features |

The CLI is where experts live. It's the most flexible, works over SSH, integrates with any editor via terminal splits, and is always the first to receive new features. This book focuses primarily on the CLI, but nearly everything applies across platforms.

### What This Book Covers

Over the next 19 chapters, you'll go from installation to expertise. You'll learn the fundamentals, then the workflows that make experienced developers productive, then the advanced features that most users never discover. By the end, you'll have a Claude Code setup that's customized to your workflow, your team, and your projects — and you'll know exactly how to get the most out of every conversation.

Let's start by getting Claude Code installed and running on your machine.

---


## Chapter 2: Installation & Setup

Getting Claude Code running takes about five minutes. This chapter covers every installation method, authentication option, and configuration detail so you start with a solid foundation.

### Prerequisites

Before installing Claude Code, you need two things:

1. **Node.js 18 or later** — Node.js 24 LTS is recommended. Check your version:

```bash
node --version
# v24.0.0 or higher
```

If you need to install or update Node.js:

```bash
# macOS (Homebrew)
brew install node

# Or use a version manager (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
nvm install 24
nvm use 24
```

2. **An Anthropic account** — Either a Claude Pro/Max subscription or an API key with credits. More on authentication below.

### Installation Methods

Claude Code offers several installation paths. Pick the one that fits your workflow.

#### Native Installer (Recommended)

The native installer is the fastest path and includes automatic updates:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

This installs the `claude` binary to your system PATH and sets up auto-updates so you always have the latest version.

#### Homebrew (macOS)

```bash
brew install --cask claude-code
```

This installs the Desktop app, which also makes the `claude` CLI available in your terminal.

#### npm (Cross-platform)

If you prefer managing it through npm:

```bash
npm install -g @anthropic-ai/claude-code
```

> **Tip:** The npm method doesn't auto-update. You'll need to run `npm update -g @anthropic-ai/claude-code` periodically. The native installer handles updates automatically.

#### Verify Installation

Regardless of which method you used:

```bash
claude --version
```

You should see a version string like `Claude Code v1.x.x`. If you get "command not found," check that your PATH includes the installation directory.

### Authentication

Claude Code supports two authentication methods.

#### Option 1: Claude Pro/Max Subscription (Easiest)

If you have a Claude Pro ($20/month) or Claude Max ($100/month or $200/month) subscription, authentication is seamless:

```bash
claude
```

On first launch, Claude Code opens your browser for OAuth authentication. Sign in with your Anthropic account, authorize Claude Code, and you're done. Your session persists across terminal restarts.

This is the simplest option and what most individual developers use.

#### Option 2: API Key

For teams, CI/CD pipelines, or if you prefer pay-per-use:

```bash
# Set your API key as an environment variable
export ANTHROPIC_API_KEY=sk-ant-api03-...

# Or add it to your shell profile for persistence
echo 'export ANTHROPIC_API_KEY=sk-ant-api03-...' >> ~/.zshrc
source ~/.zshrc
```

Then launch Claude Code normally:

```bash
claude
```

It will detect the API key automatically. No browser auth needed.

> **Tip:** Never commit your API key to git. Add it to your shell profile (`~/.zshrc` or `~/.bashrc`) or use a secrets manager. If you suspect a key has been exposed, rotate it immediately at console.anthropic.com.

#### Diagnosing Auth Issues

If something isn't working, Claude Code has a built-in diagnostic tool:

```bash
claude doctor
```

This checks your authentication status, Node.js version, network connectivity, and configuration. It's the first thing to run when something seems wrong.

### First Launch

Navigate to any project directory and start Claude Code:

```bash
cd ~/projects/my-app
claude
```

On your first launch, you'll see:

1. **A welcome message** explaining what Claude Code can do
2. **A permission prompt** asking what level of autonomy to grant (we cover this in detail in Chapter 4)
3. **The conversation interface** — a prompt where you type your requests

Try something simple to verify everything works:

```
What files are in this project? Give me a high-level overview.
```

Claude Code will use its Glob and Read tools to scan your project and give you a structured summary. If you see it reading files and providing an accurate overview, you're all set.

### Configuration Basics

Claude Code's configuration lives in two locations:

#### Global Configuration: `~/.claude/`

This directory stores settings that apply to all your projects:

```
~/.claude/
├── CLAUDE.md           # Global instructions Claude always follows
├── settings.json       # Permissions, preferences, defaults
└── keybindings.json    # Custom keyboard shortcuts
```

The global `CLAUDE.md` is where you put instructions that should apply everywhere — your preferred coding style, your name, common conventions. For example:

```markdown
# Global Rules
- Always use TypeScript strict mode
- Prefer functional components in React
- Use conventional commits format
- My name is Alex — use it in co-author tags
```

#### Project Configuration: `.claude/` and `CLAUDE.md`

Each project can have its own configuration:

```
my-project/
├── .claude/
│   ├── settings.json        # Project-level permissions (commit this)
│   └── settings.local.json  # Personal overrides (gitignored)
├── CLAUDE.md                # Project instructions (commit this)
└── ...
```

The project `CLAUDE.md` is one of the most powerful features in Claude Code. It's a markdown file at your project root that Claude reads at the start of every conversation. Your team can commit it to the repo so that everyone — including Claude — follows the same conventions.

```markdown
# Project: My SaaS App

## Stack
- Next.js 15 with App Router
- PostgreSQL via Drizzle ORM
- Tailwind CSS + shadcn/ui

## Conventions
- All API routes go in app/api/
- Use server actions for mutations
- Tests go next to the file they test (*.test.ts)
- Run `npm test` before committing

## Do NOT
- Modify the database schema without discussing first
- Use any CSS framework other than Tailwind
- Add new dependencies without approval
```

We cover CLAUDE.md in full depth in Chapter 5. For now, just know it exists and that it's how you teach Claude Code about your project.

### Model Selection

Claude Code gives you access to multiple models with different speed/capability tradeoffs:

| Model | Strengths | Best For |
|-------|----------|---------|
| **Claude Opus 4** | Most capable, best reasoning | Complex architecture, multi-file refactors, debugging |
| **Claude Sonnet 4** | Fast, highly capable | Daily development, code generation, most tasks |
| **Claude Haiku** | Fastest, most affordable | Quick questions, simple edits, file lookups |

#### Switching Models

There are several ways to change your active model:

```bash
# Start with a specific model
claude --model sonnet

# Inside a conversation, use Shift+Tab to cycle models
# Opus → Sonnet → Haiku → Opus

# Or use the slash command
/model sonnet
```

#### The /fast Toggle

The `/fast` command is a quick way to optimize for speed within your current model tier:

```
/fast
```

This enables extended thinking optimizations that make responses faster while using the same model. Toggle it again to turn it off.

#### Which Model When?

A practical rule of thumb:

- **Starting a new feature** from scratch with complex requirements? Use **Opus**.
- **Everyday coding** — fixing bugs, writing tests, adding endpoints? **Sonnet** handles it well and responds faster.
- **Quick questions** — "What does this function do?" / "Where is this config?"? **Haiku** is instant and costs a fraction.

> **Tip:** You can change models mid-conversation. Start with Haiku for exploration and reading, then switch to Opus when you're ready for Claude to implement something complex. This is a simple way to manage costs without sacrificing quality.

### Essential First Commands

Before moving on, try these commands to familiarize yourself with the interface:

| Command | What It Does |
|---------|-------------|
| `/help` | Show all available slash commands |
| `/status` | Show current model, permissions, and session info |
| `/cost` | Show token usage and cost for this session |
| `/clear` | Clear conversation history (start fresh) |
| `/compact` | Compress conversation to save context window |
| `Ctrl+C` | Cancel the current operation |
| `Ctrl+D` or `/exit` | Exit Claude Code |

You now have Claude Code installed, authenticated, and configured. In the next chapter, you'll put it to work on a real coding task.

---


## Chapter 3: Your First Real Task

Theory is useful. Practice is better. In this chapter, you'll walk through a complete real-world task with Claude Code — from asking questions about an unfamiliar codebase to implementing a feature, running tests, and committing the result.

### Setting Up

Open your terminal and navigate to a project. If you don't have one handy, clone any open-source project to follow along:

```bash
git clone https://github.com/expressjs/express.git
cd express
claude
```

Claude Code starts and you're in a conversation. Everything you type from here is a request to your AI coding partner.

### Asking Questions About the Codebase

The first thing most developers do with Claude Code is understand existing code. This is where it shines — it can read your entire project far faster than you can.

**Get a high-level overview:**

```
What does this project do? Describe the architecture and main entry points.
```

Claude Code will use Glob to find key files (`package.json`, `README.md`, entry points), then Read to examine them. You'll get a structured summary within seconds.

**Trace a specific flow:**

```
How does the routing system work? Walk me through what happens when 
app.get('/users', handler) is called.
```

Claude Code will search for the relevant source files, read them in order, and explain the flow with references to specific files and line numbers.

**Find specific patterns:**

```
Find all places where error handling middleware is used.
```

Claude Code uses Grep (its content search tool) with regex patterns to locate every match across the codebase. The results include file paths and line numbers.

> **Tip:** You can reference a specific file in your prompt with `@filename`. For example: `Explain what @src/router/index.js does` will make Claude Code prioritize reading that file first.

### Reading Files

When Claude Code reads a file, it uses its Read tool and displays the content with line numbers. This matters because those line numbers become reference points for edits.

Behind the scenes, when you ask "Show me the main entry point," Claude Code does something like this:

```
Read: /path/to/project/src/index.js (lines 1-50)
```

And you'll see the tool output with numbered lines:

```
  1  const express = require('express');
  2  const app = express();
  3  
  4  app.use(express.json());
  5  app.use(express.urlencoded({ extended: true }));
  6  
  7  // Routes
  8  app.use('/api/users', require('./routes/users'));
  9  app.use('/api/posts', require('./routes/posts'));
 10  
 11  app.listen(3000, () => {
 12    console.log('Server running on port 3000');
 13  });
```

For large files, Claude Code reads only the relevant sections rather than loading the entire file. This is intentional — it keeps the conversation context efficient and focused.

### Editing a File

Now let's make a change. Say you notice the server has no health check endpoint. Ask Claude Code to add one:

```
Add a health check endpoint at GET /health that returns { status: "ok", uptime: process.uptime() }
```

Claude Code will:

1. Read the entry point file to understand the structure
2. Use the **Edit tool** to insert the new code at the right location

The Edit tool works by specifying an `old_string` (existing code to find) and a `new_string` (what to replace it with):

```
Edit: src/index.js
  old_string: "// Routes"
  new_string: "// Health check\napp.get('/health', (req, res) => {\n  
    res.json({ status: 'ok', uptime: process.uptime() });\n});\n\n// Routes"
```

This is a key concept: **Edit sends only the diff, not the entire file.** This makes it:

- **Cheaper** — fewer tokens consumed
- **Safer** — can't accidentally overwrite unrelated code
- **Precise** — targets exactly the code that needs to change

If the old_string isn't found (perhaps the code structure differs from what Claude expected), the edit fails gracefully and Claude Code re-reads the file to try again with the correct context.

> **Tip:** The Edit tool is always preferred over the Write tool for modifications. Write replaces the entire file contents, which risks losing changes. Edit touches only the specific lines that need to change. You'll see Claude Code use Edit for nearly every modification — this is by design.

### Running Commands

Claude Code can execute any shell command through its Bash tool. This means building, testing, linting, deploying — anything your terminal can do.

**Run tests:**

```
Run the test suite and tell me if anything fails.
```

Claude Code will find and execute the appropriate test command (reading `package.json` scripts, `Makefile`, or whatever your project uses):

```bash
npm test
```

It captures the full output — pass/fail counts, error messages, stack traces — and summarizes the results. If tests fail, it can immediately analyze the failures and propose fixes.

**Build the project:**

```
Build the project and make sure there are no TypeScript errors.
```

```bash
npm run build
```

**Run arbitrary commands:**

```
Check which port 3000 is currently using.
```

```bash
lsof -i :3000
```

Claude Code isn't limited to project scripts. It has full shell access, so system commands, curl requests, Docker operations — anything goes.

> **Tip:** You can run a quick shell command without waiting for Claude Code to process it by prefixing with `!`. For example, `!git status` runs immediately and injects the output into the conversation. This is useful for giving Claude Code context without a full round-trip.

### Creating New Files

When you need something that doesn't exist yet, Claude Code uses the Write tool to create files from scratch:

```
Create a middleware function in src/middleware/requestLogger.js that logs 
the method, URL, and response time for every request.
```

Claude Code will:

1. Check the project structure to understand conventions (file locations, import style, existing middleware patterns)
2. Create the file with idiomatic code that matches your project's style
3. Often suggest how to wire it into your application

The Write tool creates the file with the complete content in one operation. For new files, this is the right tool. For modifying existing files, Edit is preferred.

### Multi-step Tasks

This is where Claude Code truly differentiates itself. Give it a complex task and watch it plan and execute across multiple files:

```
Add a rate limiting middleware that:
- Limits each IP to 100 requests per 15-minute window
- Returns 429 Too Many Requests when exceeded
- Has configurable limits via environment variables
- Include tests
```

Claude Code will typically:

1. **Plan** — Identify which files to create or modify
2. **Create the middleware** — Write the rate limiter with the specified behavior
3. **Create the test file** — Write tests covering normal requests, rate limit exceeded, configuration, and edge cases
4. **Wire it up** — Edit the entry point to use the new middleware
5. **Run the tests** — Execute the test suite to verify everything works
6. **Fix issues** — If tests fail, analyze the errors and fix them

All of this happens in a single conversation. You describe the outcome, Claude Code handles the implementation across as many files and steps as needed.

### Conversation Flow Tips

How you interact with Claude Code matters. Here are patterns that experienced users rely on:

#### Give Follow-up Instructions

After Claude Code completes a task, you can refine it:

```
Good, but use Redis instead of an in-memory Map for the rate limit store.
Also make the key prefix configurable.
```

Claude Code maintains the full conversation context, so it knows exactly what you're referring to and what code it already wrote.

#### Ask for Alternatives

```
Show me a different approach — what if we used a sliding window 
instead of fixed windows?
```

#### Course-correct Early

If you see Claude Code heading in a direction you don't want:

Press `Escape` to interrupt the current operation, then:

```
Stop — don't use that library. Implement it with native Node.js only, 
no external dependencies.
```

Interrupting is free and doesn't waste your context window. It's better to stop early than let Claude Code finish something you'll reject.

#### Start Fresh for New Topics

Each conversation has a context window — a limit on how much text it can hold. Long conversations with many file reads and command outputs consume context quickly.

When you switch to a completely different task, start a new conversation:

```
/clear
```

Or exit and restart:

```bash
claude
```

This gives Claude Code a fresh context window, which means better performance and more accurate responses. Your CLAUDE.md instructions are automatically reloaded, so project context is never lost.

> **Tip:** Use `/compact` if you're deep in a productive conversation but running low on context. It compresses the conversation history, preserving key decisions and context while freeing up space for more work.

### What You Just Learned

In this chapter, you used Claude Code to:

- Explore and understand an unfamiliar codebase
- Read files with precise line numbers
- Make targeted edits without rewriting entire files
- Run shell commands and analyze their output
- Create new files that match project conventions
- Execute multi-step tasks spanning multiple files
- Manage conversation flow effectively

This is the basic loop of working with Claude Code. In the next chapter, we'll look at the permission system that governs how much autonomy Claude Code has — and how to configure it for your comfort level.

---


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


# Part 2: Productive Development

## Chapter 5: CLAUDE.md — Teaching Claude About Your Project

If you only do one thing to improve your Claude Code experience, it's this: create a CLAUDE.md file.

CLAUDE.md is a markdown file that Claude reads automatically at the start of every conversation. It contains your project's rules, conventions, architecture notes, and any context that Claude needs to do its job well. Think of it as `.editorconfig` for AI — except instead of tab width and line endings, you're specifying how your entire project works.

Without a CLAUDE.md, Claude Code starts every conversation as a talented developer who has never seen your project before. With a good CLAUDE.md, it starts as a developer who has been briefed by the team lead on day one. That difference compounds across every interaction.

### Three Levels of CLAUDE.md

CLAUDE.md files cascade through three levels, from global (all projects) to project-specific to personal overrides:

| Level | Location | Applies To | Commit to Git? |
|-------|----------|-----------|----------------|
| **Global** | `~/.claude/CLAUDE.md` | Every project on your machine | No (personal) |
| **Project** | `CLAUDE.md` (repo root) | This repository, all team members | Yes |
| **Local** | `.claude/CLAUDE.md` | This repo, only you | No (gitignored) |

**Global** is your personal baseline. Put your preferred language, coding style, name, and universal habits here. These apply to every project you open with Claude Code.

**Project** is the team-shared file at the repository root. Commit it to git. When a new team member clones the repo and runs Claude Code, they get the same instructions as everyone else. This is the file that has the most impact — it teaches Claude Code about your specific project.

**Local** is your personal override for a specific project. Maybe the team uses `npm test` but you prefer running `npm test -- --watch`. Maybe you want Claude to use a different language than the rest of the team. The local CLAUDE.md lets you customize without affecting anyone else.

All three levels are merged at conversation start, with more specific levels winning on conflicts.

### What to Include

A good CLAUDE.md answers the questions Claude Code would ask if it were a new developer joining your team. Here are the categories that matter most:

**Project architecture overview** — What does this project do? What's the high-level structure?

**Tech stack and key libraries** — Framework, language version, major dependencies. Claude Code can detect these from `package.json` or `Cargo.toml`, but explicit declarations prevent guesswork.

**Build, test, and lint commands** — The commands you use daily. Claude Code uses these when running tests or checking if changes compile.

**File and folder conventions** — Where things live. Where to put new files. Naming patterns.

**Coding style rules** — Especially rules that linters don't cover. "We prefer early returns." "We use named exports." "All API responses follow this shape."

**Common gotchas** — Things that trip people up. "Don't import server modules in client components." "The database migration system requires running X first."

**"Don't" rules** — Explicit prohibitions are surprisingly effective. "Don't add new npm dependencies without asking." "Never modify the auth middleware directly."

### Real-World Examples

Here are three CLAUDE.md files at different complexity levels.

#### Simple Personal Project

```markdown
# My Portfolio Site

Static site built with Astro. Content in src/content/. Styles in 
src/styles/ using vanilla CSS.

## Commands
- `npm run dev` — local server on port 4321
- `npm run build` — production build to dist/

## Rules
- No JavaScript frameworks — this is a static site
- Images go in public/images/
- Keep pages under 100KB total
```

Ten lines. That's it. Even this small file prevents Claude Code from suggesting React components, putting images in the wrong directory, or using a build command that doesn't exist.

#### Team Web Application

```markdown
# Acme Dashboard

Next.js 15 App Router + PostgreSQL (Drizzle ORM) + Tailwind CSS + shadcn/ui

## Architecture
- `app/` — Next.js App Router pages and layouts
- `app/api/` — API route handlers
- `lib/` — Shared utilities, database client, auth helpers
- `components/` — React components (shadcn/ui based)
- `drizzle/` — Database schema and migrations

## Commands
- `npm run dev` — development server (port 3000)
- `npm test` — run Vitest suite
- `npm run db:push` — push schema changes to database
- `npm run db:generate` — generate migration files
- `npm run lint` — ESLint + Prettier check

## Conventions
- Server Components by default, "use client" only when needed
- Use server actions for mutations (not API routes)
- All database queries go through lib/db.ts
- Tests live next to their source file: `foo.ts` → `foo.test.ts`
- Use conventional commits: feat:, fix:, chore:, docs:

## Do NOT
- Add npm dependencies without discussing first
- Modify drizzle/schema.ts without creating a migration
- Use inline styles — Tailwind only
- Import from lib/db.ts in client components
```

Thirty lines covering everything a developer needs to work in this codebase. Every rule here prevents a real mistake that an AI (or human) would otherwise make.

#### Comprehensive Enterprise Project

```markdown
# Platform API — Microservices Backend

## Overview
Multi-service backend for the Acme platform. 12 services in a monorepo, 
deployed to Kubernetes via Helm charts. Language: Go 1.22. 
API standard: gRPC with REST gateway.

## Repository Structure
- `services/` — Individual microservices (each has its own go.mod)
- `proto/` — Protobuf definitions (source of truth for all APIs)
- `pkg/` — Shared Go packages used across services
- `deploy/` — Helm charts and Kubernetes manifests
- `scripts/` — Build, test, and deployment automation
- `docs/` — Architecture Decision Records (ADRs) and API docs

## Build & Test
- `make build` — build all services
- `make build-<service>` — build specific service
- `make test` — run all tests
- `make test-<service>` — test specific service
- `make lint` — golangci-lint across all services
- `make proto` — regenerate code from protobuf definitions

## Coding Standards
- Follow Uber Go Style Guide
- Error handling: always wrap errors with fmt.Errorf("context: %w", err)
- Logging: use structured logging (slog) — never fmt.Println in production
- Context: pass context.Context as first argument to all functions
- Naming: services use PascalCase, packages use lowercase, files use snake_case
- Tests: table-driven tests required for all business logic

## API Conventions
- All new APIs defined in proto/ first, then implement
- REST endpoints auto-generated via grpc-gateway — don't write REST handlers
- Pagination: use cursor-based (not offset), fields: next_cursor, page_size
- Errors: use standard gRPC status codes, include error_details field

## Do NOT
- Modify proto/ files without updating the changelog
- Add dependencies to pkg/ without team review (it affects all services)
- Use database/sql directly — use the repository pattern in pkg/database
- Deploy to staging without running `make integration-test`
- Skip code review for changes touching pkg/ or deploy/

## Common Gotchas
- The auth service uses a different database (CockroachDB, not PostgreSQL)
- Service-to-service calls go through the mesh — never use direct HTTP
- The CI pipeline runs `make lint` with stricter settings than local
- Protobuf field numbers cannot be reused — ever
```

Sixty lines, densely packed with institutional knowledge. This file saves hours of onboarding time — for humans and AI alike.

### The /init Command

Don't want to write your CLAUDE.md from scratch? Claude Code can generate one for you.

Start Claude Code in your project directory and run:

```
/init
```

Claude Code will scan your project — reading `package.json`, `Cargo.toml`, `go.mod`, folder structure, git history, README files, CI configs — and generate a CLAUDE.md tailored to what it finds. The result is a solid starting point that you can refine.

The generated file usually captures:

- Project type and framework detection
- Build and test commands from package scripts or Makefiles
- Folder structure conventions based on existing layout
- Language and framework versions

It won't capture your team's unwritten rules or gotchas — those are the parts you add yourself. But as a starting point, `/init` saves significant time.

> **Tip:** Run `/init` even on projects that already have a CLAUDE.md. Compare the output with your existing file — Claude Code might detect conventions or commands you forgot to document.

### Path-Specific Rules

Some rules only apply to certain parts of your codebase. API files need input validation. Test files need specific patterns. Database migrations need extra caution.

Claude Code supports path-specific rules through `.claude/rules/*.md` files. Each file has YAML frontmatter specifying which paths the rules apply to:

```yaml
---
paths:
  - "src/api/**/*.ts"
---
# API Route Rules

- Always validate request body with zod schema
- Return standardized error responses: { error: string, code: number }
- Include rate limiting headers in responses
- Log all 4xx and 5xx responses with request ID
```

Another example for test files:

```yaml
---
paths:
  - "**/*.test.ts"
  - "**/*.spec.ts"
---
# Test Rules

- Use describe/it blocks, not test()
- Each test file must have at least one happy path and one error case
- Mock external services, never make real HTTP calls
- Use factories for test data, not inline object literals
```

These rules are loaded only when Claude Code is working on matching files. They keep your main CLAUDE.md clean while still providing targeted guidance where it matters.

### File Imports

As your CLAUDE.md grows, you might want to reference other documentation files rather than duplicating information. Use the `@path` syntax to import context from other files:

```markdown
# My Project

## Architecture
@docs/architecture.md

## API Conventions
@docs/api-conventions.md

## Database Schema
@docs/schema-overview.md
```

When Claude Code reads the CLAUDE.md, it will also load the referenced files into context. This is powerful for projects that already have extensive documentation — you don't need to rewrite it for Claude, just point to it.

Keep in mind that every imported file consumes context window space, so be selective. Import the files Claude Code needs most often, not your entire docs folder.

### Pro Tips for Effective CLAUDE.md Files

**Keep it concise.** Claude Code reads your CLAUDE.md at the start of every conversation. A 500-line CLAUDE.md consumes context window space that could be used for actual work. Aim for 20-60 lines for most projects. If you need more, use path-specific rules or file imports.

**Update as your project evolves.** Your CLAUDE.md should be a living document. When you add a new convention, change a build command, or discover a gotcha, update the file. Stale instructions cause Claude Code to make outdated decisions.

**Include "don't" rules.** Negative instructions are surprisingly effective. "Don't use class components" prevents an entire category of wrong suggestions. "Don't modify the auth middleware" protects critical code.

**Specify your expertise level.** If you're learning a new framework, tell Claude Code: "I'm new to Rust — explain ownership decisions." If you're an expert: "I know React well — skip basic explanations, just write the code." This calibrates the level of detail in Claude's responses.

**Use markdown headers for organization.** Claude Code parses CLAUDE.md as markdown. Headers create clear sections that are easy to scan and update. Use `##` for major categories and `###` for subcategories.

**Test your CLAUDE.md.** After writing or updating it, start a new Claude Code conversation and ask it to do something covered by your rules. Verify it follows them. If it doesn't, your instructions might be ambiguous — rewrite them more explicitly.

> **Tip:** Want to see what Claude Code currently knows about your project? Use the `/memory` command. It shows your CLAUDE.md contents plus any auto-memory Claude has accumulated across sessions. This is useful for auditing what instructions Claude is actually following.

---


## Chapter 6: Every Slash Command Explained

Slash commands are Claude Code's built-in utilities — fast, single-purpose operations you trigger with `/` followed by a keyword. They manage sessions, change settings, control context, and access features that would be clunky to invoke through natural language.

Most developers learn three or four commands and ignore the rest. This chapter documents every slash command so you know exactly what's available and when to use each one.

### Session Management

These commands control the lifecycle of your conversations — starting, stopping, resuming, and organizing them.

| Command | Description |
|---------|-------------|
| `/clear` | Clear the current conversation and start fresh. Your CLAUDE.md is reloaded automatically. Use this when switching to a completely different task. |
| `/compact [focus]` | Compress the conversation history to reclaim context window space. Optionally provide a focus hint: `/compact focus on auth changes` tells Claude what to preserve during compression. |
| `/rename [name]` | Give the current session a memorable name. `/rename auth-refactor` makes it easy to find and resume later. |
| `/resume [name]` | Resume a previous named session. Without a name, shows a list of recent sessions to choose from. |
| `/continue` | Resume the most recent conversation. Equivalent to launching with `claude --continue`. |
| `/branch [name]` | Fork the conversation at the current point. Creates a new branch of the conversation so you can explore a different approach without losing the current one. |
| `/rewind` | Undo the last exchange. Rolls back to the previous message checkpoint, removing Claude's last response and your last prompt. Useful when Claude went in the wrong direction. |
| `/exit` or `/quit` | End the session and exit Claude Code. Same as `Ctrl+D`. |

The most underused command here is `/compact`. Long conversations accumulate file contents, command outputs, and discussion history that eat into your context window. When you notice Claude Code starting to miss details or repeat itself, run `/compact` to free up space. You won't lose important context — Claude summarizes the key decisions and code changes before compressing.

> **Tip:** Add a focus hint to `/compact` when you're deep in a specific area. `/compact focus on database migration changes` ensures the compression preserves details about the exact work you care about, even if it aggressively compresses earlier discussion about unrelated files.

### Model & Configuration

These commands control how Claude Code operates — which model it uses, how much reasoning it applies, and its speed/quality tradeoff.

| Command | Description |
|---------|-------------|
| `/model [model]` | Switch to a different model. `/model opus` for maximum capability, `/model sonnet` for speed, `/model haiku` for quick lookups. |
| `/fast [on\|off]` | Toggle fast mode, which optimizes for response speed. Useful when you're doing quick iterations and don't need deep reasoning. |
| `/effort [level]` | Set the reasoning depth. Accepts `low`, `medium`, `high`, or `max`. Lower effort means faster but shallower responses. Higher effort means Claude thinks longer before responding. |
| `/config` | Open the settings interface to adjust permissions, preferences, and defaults interactively. |

A practical workflow: start your session with `/effort low` for exploration and file reading, then `/effort high` when you're ready for Claude to implement something complex. This minimizes cost and wait time during the discovery phase.

### Development

These commands directly support your coding workflow — from initializing project configuration to reviewing changes.

| Command | Description |
|---------|-------------|
| `/init` | Scan the project and generate a CLAUDE.md file with detected conventions, commands, and structure. Covered in depth in Chapter 5. |
| `/diff` | Open an interactive diff viewer showing all pending file changes Claude has made. Lets you review and accept or reject individual changes. |
| `/security-review` | Run a security audit on pending changes. Claude analyzes all modifications for potential vulnerabilities — injection risks, exposed secrets, permission issues. |
| `/batch <instruction>` | Apply changes in parallel across multiple git worktrees. Useful for making the same change across several branches or services simultaneously. |

The `/security-review` command is worth running before any commit that touches authentication, authorization, input handling, or data access. It's a free second pair of eyes that catches issues like SQL injection vectors, missing input validation, or accidentally logged secrets.

### Context & Memory

These commands give you visibility into Claude Code's context window usage, memory, and costs.

| Command | Description |
|---------|-------------|
| `/memory` | View and edit your CLAUDE.md files and auto-memory. Shows what instructions Claude is currently following and lets you modify them. |
| `/cost` | Display token usage and estimated costs for the current session. Shows input tokens, output tokens, cache hits, and total spend. |
| `/context` | Show a visual grid of context window usage. Reveals how much of the context window is consumed by conversation history, file contents, and tool outputs. |
| `/export [filename]` | Save the entire conversation as a text file. Defaults to a timestamped filename if none is provided. Useful for documentation or sharing. |
| `/copy [N]` | Copy Claude's last response (or last N responses) to your clipboard. Handy for pasting code snippets into other tools. |

The `/cost` command is your budget tracker. After completing a major task, check `/cost` to understand the token economics. Over time, this builds intuition for which types of requests are expensive (large file reads, multi-file refactors) and which are cheap (quick questions, small edits).

> **Tip:** The `/context` grid is your early warning system for context window exhaustion. When it shows you're above 70% capacity, consider running `/compact` or starting a new conversation. Performance degrades noticeably as you approach the limit.

### Advanced

These commands cover specialized features — scheduling, diagnostics, analytics, and cloud-powered capabilities.

| Command | Description |
|---------|-------------|
| `/schedule` | Create recurring tasks that run on a schedule in the cloud. Claude Code connects to a remote agent that executes your instructions on a cron schedule. |
| `/btw <question>` | Ask a side question without polluting the main conversation context. The answer is shown but the exchange is not added to the conversation history. |
| `/ultraplan` | Invoke cloud-based deep planning. Claude creates a detailed implementation plan using extended cloud compute, then returns the plan for your review. |
| `/status` | Show version info, current model, account type, and session details. First thing to check when something seems wrong. |
| `/doctor` | Run diagnostics on your Claude Code installation. Checks Node.js version, authentication, network connectivity, and configuration. |
| `/stats` | Display usage statistics — sessions count, messages sent, tools used, and usage streaks. |
| `/insights` | Generate an analysis report of the current session — what was accomplished, how tokens were spent, and suggestions for efficiency. |

The `/btw` command deserves special attention. During a complex implementation, you might suddenly need to check a syntax detail or look up a library API. A normal question would inject that tangent into the main conversation, potentially confusing Claude's focus on the primary task. `/btw what's the syntax for Go's sync.WaitGroup?` gets you the answer without derailing the session.

### Keyboard Shortcuts

These work anywhere in the Claude Code interface. Memorize the top five and add more as they become natural.

| Shortcut | Action |
|----------|--------|
| `Enter` | Send your message |
| `Shift+Enter` | Insert a new line (multi-line input) |
| `Shift+Tab` | Cycle through available models (Opus → Sonnet → Haiku) |
| `Esc` | Cancel the current generation — Claude stops immediately |
| `Ctrl+C` | Exit Claude Code (or cancel current operation) |
| `Ctrl+R` | Search through command history |
| `Ctrl+O` | Toggle verbose transcript (see raw tool calls and outputs) |
| `Ctrl+B` | Background the current task — Claude continues working while you get your prompt back |
| `Ctrl+G` | Open the current conversation in an external editor for review |
| `Up arrow` | Recall your previous message (edit and resend) |

The most important shortcut is `Esc`. The moment you see Claude heading in a wrong direction — wrong file, wrong approach, wrong library — press `Esc`. It costs nothing to interrupt and redirect. Letting Claude finish a bad approach wastes tokens and context window.

`Ctrl+B` is a power-user feature. When you give Claude a large task (refactoring a module, writing a test suite), press `Ctrl+B` to background it. You get your prompt back immediately and can ask other questions or start a new task. Claude notifies you when the backgrounded work is complete.

> **Tip:** `Shift+Tab` for model cycling is one of the fastest ways to save money. Reading files and exploring? Shift+Tab to Haiku. Ready to implement? Shift+Tab to Opus. Two keystrokes, significant cost difference.

### The `!` Prefix — Inline Shell Commands

Any message starting with `!` is executed as a shell command, and the output is injected into the conversation. This is different from asking Claude to run a command — it runs immediately, with no AI processing.

```
! git log --oneline -5
```

Output appears instantly:

```
a1b2c3d feat: add user authentication
e4f5g6h fix: resolve database connection timeout
i7j8k9l chore: update dependencies
m0n1o2p feat: add rate limiting middleware
q3r4s5t docs: update API documentation
```

This output is now part of the conversation context. You can follow up with:

```
Explain what changed in the rate limiting commit (m0n1o2p).
```

Claude Code sees the git log output and uses it to understand your question.

Common uses for the `!` prefix:

| Command | Purpose |
|---------|---------|
| `! git status` | Show Claude the current state of your working tree |
| `! git diff` | Feed Claude the exact changes you've made |
| `! cat .env.example` | Show Claude environment variables without risk |
| `! npm test 2>&1 \| tail -20` | Share the last 20 lines of test output |
| `! ls -la src/` | Show Claude a directory listing for context |

The key advantage is speed. `! git status` runs in milliseconds and injects the result. Asking Claude "run git status" goes through a full AI round-trip — Claude reads the request, decides to use the Bash tool, runs the command, reads the output, and summarizes it. When you just need raw output in the conversation, `!` is faster.

### The `@` Reference — File Mentions

Typing `@` followed by a file path loads that file into Claude's context. This is the fastest way to bring a specific file into the conversation without asking Claude to "read" it.

```
@src/middleware/auth.ts explain what this middleware does
```

Claude Code loads the file contents immediately, so it can analyze the code without a separate Read tool call. This is especially useful when you know exactly which file you want to discuss.

You can reference multiple files:

```
@src/models/user.ts @src/routes/users.ts 
Are these two files consistent in how they handle user validation?
```

The `@` reference works with relative paths from your project root. Tab completion helps you find the right file — start typing `@src/` and press Tab to see available options.

> **Tip:** Combine `!` and `@` for maximum context efficiency. Run `! git diff --name-only` to see which files changed, then `@path/to/changed/file.ts` to pull in the specific file you want Claude to focus on. This gives Claude precise context without reading everything.

---


## Chapter 7: Git Workflow Automation

Git is the backbone of every development workflow, and Claude Code is deeply integrated with it. Not just "can run git commands" integrated — Claude Code understands git semantics, follows safety protocols, and handles the entire commit-branch-PR lifecycle with minimal input from you.

This chapter covers every git capability, from one-word commits to complex merge conflict resolution.

### Smart Commits

The simplest and most common git operation: committing your changes. Tell Claude Code:

```
commit this
```

Or use the slash command:

```
/commit
```

What happens next is more sophisticated than it appears. Claude Code:

1. **Runs `git status`** to see all untracked and modified files
2. **Runs `git diff`** to see exactly what changed (both staged and unstaged)
3. **Reads recent commit messages** (`git log`) to match your repository's commit style — if you use conventional commits, it follows that; if you use sentence-case, it follows that
4. **Analyzes the actual changes** — not just file names, but the code modifications — to understand what was done and why
5. **Generates a commit message** that focuses on the "why" rather than the "what"
6. **Stages the relevant files** — and this is key — it avoids staging files that shouldn't be committed: `.env`, credentials, large binaries, unrelated changes
7. **Creates the commit** using a HEREDOC format for clean multi-line messages

The result is a commit message that reads like a thoughtful developer wrote it, because one did.

```
feat: add cursor-based pagination to users endpoint

Replace offset pagination with cursor-based approach for better
performance on large datasets. Includes backward compatibility
for clients still sending offset/limit params.
```

Compare this to what most developers write when they're tired and just want to push:

```
update users endpoint
```

> **Tip:** Claude Code always creates a **new** commit. It never amends an existing commit unless you explicitly say "amend the last commit." This is a safety protocol — amending can overwrite previous work, especially after a failed pre-commit hook where the commit didn't actually happen. If you need to amend, be explicit: "amend the previous commit with these changes."

#### Selective Staging

Claude Code is smart about what it stages. If you've been working on two separate features and only want to commit one:

```
commit just the authentication changes, not the UI updates
```

Claude Code will `git diff` everything, identify which files relate to authentication, stage only those, and write a commit message specific to what's being committed. The UI changes remain in your working tree, ready for a separate commit.

#### Commit with Instruction

You can guide the commit message:

```
commit this as a bug fix — the issue was that passwords weren't being hashed before storage
```

Claude Code will incorporate your context into the message:

```
fix: hash passwords before database storage

Passwords were being stored in plaintext. Add bcrypt hashing in the
user registration and password update flows.
```

### Pull Request Creation

Creating a pull request is one of Claude Code's strongest git features. Tell it:

```
create a PR
```

Claude Code performs a thorough analysis before creating anything:

1. **Checks the current branch** and identifies the base branch
2. **Reads ALL commits** since the branch diverged — not just the latest commit, but the entire branch history. This is critical for accurate PR descriptions.
3. **Runs `git diff base...HEAD`** to see the complete set of changes
4. **Checks if the branch is pushed** to remote — if not, it pushes with `-u` flag
5. **Generates a title** (under 70 characters) and a structured description

The PR is created using `gh pr create` with a clean format:

```
## Summary
- Add cursor-based pagination to /api/users endpoint
- Include backward compatibility for offset/limit params
- Add integration tests for pagination edge cases

## Test plan
- [ ] Verify cursor pagination returns correct pages
- [ ] Verify offset/limit still works (backward compat)
- [ ] Test with empty result set
- [ ] Test with single-item result set
- [ ] Load test with 100K+ users
```

The title stays short and descriptive. The body uses the Summary + Test plan format that reviewers appreciate. Details go in the body, not the title.

#### PR with Context

Add context to guide the PR description:

```
create a PR — this closes issue #42 and was requested by the 
frontend team for infinite scroll support
```

Claude Code will reference the issue, add context from your instruction, and link the PR to the issue.

#### Draft PRs

```
create a draft PR — still need to add error handling
```

Claude Code adds the `--draft` flag and notes the remaining work in the description.

### Branch Management

Claude Code handles branch operations naturally:

```
create a branch for the user authentication feature
```

```bash
git checkout -b feature/user-authentication
```

Claude Code picks conventional branch names based on your repository's existing patterns. If your branches use `feat/`, it follows that. If they use `feature/`, it follows that instead.

```
switch to the main branch
```

```bash
git checkout main
```

```
show me all branches related to payments
```

```bash
git branch -a | grep payment
```

One crucial safety protocol: **Claude Code never force-pushes or deletes branches without explicit confirmation.** If you say "clean up old branches," it will list the branches it would delete and ask for your approval before executing.

### Conflict Resolution

Merge conflicts are where most developers lose time. Claude Code handles them by understanding both sides of the conflict, not just blindly picking one.

When you run into a conflict:

```
I just merged main into my branch and got conflicts. Fix them.
```

Claude Code will:

1. Run `git diff --name-only --diff-filter=U` to find conflicted files
2. Read each conflicted file, analyzing the conflict markers
3. Understand the intent of both sides — what your branch changed and what main changed
4. Resolve the conflict by merging both intents when possible, or choosing the correct side when they're incompatible
5. Stage the resolved files

Here's what this looks like in practice. Say you have this conflict in `src/config.ts`:

```
<<<<<<< HEAD
const MAX_RETRIES = 5;
const TIMEOUT_MS = 10000;
=======
const MAX_RETRIES = 3;
const TIMEOUT_MS = 30000;
const BACKOFF_MULTIPLIER = 2;
>>>>>>> main
```

Claude Code sees that your branch increased `MAX_RETRIES` while main increased `TIMEOUT_MS` and added `BACKOFF_MULTIPLIER`. Instead of picking one side, it merges both intents:

```typescript
const MAX_RETRIES = 5;        // from your branch
const TIMEOUT_MS = 30000;     // from main
const BACKOFF_MULTIPLIER = 2; // new addition from main
```

It keeps your retry increase, keeps main's timeout increase, and keeps the new constant. If the changes truly conflict (both sides changed the same value for different reasons), Claude Code explains the conflict and asks which side you prefer.

> **Tip:** For complex conflicts involving many files, give Claude Code context about what you were working on: "My branch adds OAuth support. Main branch refactored the user model. Resolve conflicts preserving both changes." The more intent you provide, the better the resolution.

### Git Safety Protocols

Claude Code has built-in safety rails for git operations. These are not configurable — they're always active, even in full-auto mode.

| Protection | What It Does |
|-----------|-------------|
| **No force push to main/master** | Claude Code will warn and refuse to `git push --force` to protected branches. If you insist, it confirms explicitly. |
| **No hard reset without asking** | `git reset --hard` destroys uncommitted work. Claude Code always asks first. |
| **No hook bypass** | Claude Code never uses `--no-verify` to skip pre-commit hooks. If a hook fails, it fixes the issue and retries. |
| **New commits, not amends** | After a pre-commit hook failure, Claude Code creates a new commit rather than amending. Amending after a failed hook would modify the previous commit — not the failed one. |
| **Sensitive file warnings** | Before committing `.env`, credentials, API keys, or files matching `*secret*`, Claude Code warns you and asks for confirmation. |
| **No branch deletion** | Claude Code never deletes branches without listing them and getting your explicit approval. |

These protocols exist because git mistakes are among the most painful in software development. A force-push to main can overwrite a team's work. A hard reset can destroy hours of uncommitted changes. Claude Code is designed to be aggressive about productivity but conservative about irreversible actions.

### Advanced Git Operations

Beyond the basics, Claude Code handles the full range of git operations:

**Cherry-picking:**

```
cherry-pick commit a1b2c3d from the feature/payments branch
```

Claude Code runs the cherry-pick, handles any conflicts using the same conflict resolution logic, and verifies the result compiles.

**Interactive rebasing:**

```
rebase my last 3 commits to clean up the history — squash the 
fixup commits into the main feature commit
```

Claude Code restructures the commits as requested, combining related changes into clean, logical commits.

**Bisecting:**

```
the login page broke sometime in the last week. help me bisect 
to find which commit caused it.
```

Claude Code sets up `git bisect`, runs the relevant tests at each step, and narrows down to the exact commit that introduced the regression.

**Stashing:**

```
stash my current changes, switch to main, pull, then come back 
and reapply my stash
```

Claude Code handles the full stash-switch-pull-switch-apply workflow in sequence.

#### Starting from a PR

You can launch Claude Code in the context of an existing pull request:

```bash
claude --from-pr 123
```

This loads the PR description, the diff, and any review comments into the conversation. It's useful for addressing PR feedback — Claude Code has full context of what the reviewer asked and what code they're referring to.

#### Isolated Worktrees

For parallel work on multiple features:

```bash
claude --worktree feature-name
```

This creates an isolated git worktree and starts Claude Code inside it. Your main working directory is untouched. When the feature is complete, the worktree is cleaned up. This pairs well with `/batch` for making coordinated changes across multiple branches.

> **Tip:** The combination of `--worktree` and full-auto mode is extremely powerful. Create a worktree, give Claude Code a well-defined task in full-auto mode, and let it work independently while you continue in your main branch. Review the result when it's done.

---


## Chapter 8: Smart Code Navigation & Editing

When you ask Claude Code to find a function, read a file, or rename a variable, it doesn't shell out to `grep` and `sed` like a script would. It uses a set of purpose-built tools that are faster, safer, and more context-aware than their shell equivalents.

Understanding these tools — what they do, when they're used, and how to guide their usage — is the difference between Claude Code stumbling through your codebase and navigating it surgically.

### The Tool Arsenal

Claude Code has five core tools for interacting with your files. Each one replaces a common shell command with something better:

| Instead of... | Claude Uses... | Why It's Better |
|---------------|----------------|-----------------|
| `find . -name "*.ts"` | **Glob** | Faster pattern matching, results sorted by modification time |
| `grep -r "pattern" .` | **Grep** | Proper permissions, full regex, multiple output modes, file type filtering |
| `cat file.py` | **Read** | Line numbers, offset/limit for large files, reads images and PDFs |
| `sed -i 's/old/new/'` | **Edit** | Exact string match (not regex), preserves formatting, must read first |
| `echo "content" > file` | **Write** | Creates new files cleanly, requires prior Read for existing files |

You rarely invoke these tools directly — you describe what you want and Claude Code picks the right tool. But knowing how they work lets you write better prompts and understand what Claude is doing under the hood.

### Glob — File Pattern Matching

Glob finds files by name pattern. It's Claude Code's first move when exploring a project — mapping out the structure before diving into specific files.

**Standard glob patterns:**

```
**/*.ts           → all TypeScript files, any depth
src/**/*.test.tsx → test files in src/, React + TypeScript
*.config.{js,ts}  → config files, JS or TS, root only
```

**Results are sorted by modification time** (most recently modified first). This is surprisingly useful — when Claude Code searches for `**/*.ts`, the files you've been working on appear first. This natural prioritization means Claude tends to look at relevant files before stale ones.

**Example use cases:**

1. **Understanding project structure:** "What files are in this project?" triggers a broad glob (`**/*`) followed by analysis of the directory tree.

2. **Finding related files:** "Find all the migration files" triggers `**/migrations/*.{sql,ts,js}` or similar patterns based on your project's conventions.

3. **Locating config files:** "Where is the database config?" triggers globs for common config patterns (`**/*config*`, `**/*.config.*`, `**/database.*`).

> **Tip:** When you ask Claude to find something and it's not finding it, be more specific about the file type or location. "Find the auth middleware" might glob too broadly. "Find the auth middleware in the src/middleware directory" narrows the search immediately.

### Grep — Content Search

Grep searches the contents of files — finding where specific code patterns, function calls, variable references, or string literals appear across your codebase.

Claude Code's Grep is built on ripgrep, not GNU grep. This means it's fast (even on massive codebases), respects `.gitignore` automatically, and supports full regex syntax.

**Three output modes:**

| Mode | What It Returns | When Claude Uses It |
|------|----------------|-------------------|
| `files_with_matches` | Just file paths (default) | Finding which files contain a pattern |
| `content` | Matching lines with context | Reading the actual matching code |
| `count` | Number of matches per file | Gauging how widespread a pattern is |

**File filtering:** Grep can filter by glob pattern (`*.ts`, `src/**/*.py`) or by file type (`js`, `py`, `rust`). Type filtering is more efficient for standard languages.

**Context lines:** When using `content` mode, Grep can show surrounding lines — lines before the match (`-B`), after the match (`-A`), or both (`-C`). This helps Claude understand the code around a match without reading the entire file.

**Example searches:**

1. **Finding all API calls:**

```
Find everywhere we call the Stripe API.
```

Claude Code greps for patterns like `stripe.`, `Stripe(`, `@stripe/` across the codebase, returning file paths and matching lines.

2. **Finding function usage:**

```
Where is the validateEmail function used?
```

Claude greps for `validateEmail` across all files, showing each call site with surrounding context.

3. **Finding patterns across languages:**

Claude Code searches with regex: `function\s+\w+Auth` finds `function checkAuth`, `function requireAuth`, etc. The regex support means complex pattern matching without multiple search passes.

**Multiline mode:** By default, patterns match within single lines. For patterns that span multiple lines (like finding a function definition with its body), Claude Code enables multiline matching:

```
Find all React components that use both useState and useEffect.
```

This triggers a multiline search for components importing or using both hooks within the same file scope.

### Read — Intelligent File Reading

Read opens files and returns their contents with line numbers. It's the most frequently used tool in every Claude Code session.

**Line numbers in output:** Every Read result looks like `cat -n` output:

```
  1  import { Router } from 'express';
  2  import { authenticate } from '../middleware/auth';
  3  
  4  const router = Router();
  5  
  6  router.get('/users', authenticate, async (req, res) => {
  7    const users = await db.users.findAll();
  8    res.json(users);
  9  });
```

These line numbers serve as reference points for discussion. You can say "what happens at line 7?" and Claude knows exactly which line you mean.

**Offset and limit for large files:** For files with hundreds or thousands of lines, Read supports partial reading:

- "Read lines 100-150 of the config file" uses `offset: 100, limit: 50`
- "Show me the last 30 lines of the log file" uses appropriate offset

This avoids loading massive files into the context window when you only need a section.

**Reading images:** Claude Code is multimodal. When Read opens a PNG, JPG, or other image format, Claude sees the image visually — not as binary data. This means you can:

```
Look at the screenshot @screenshots/bug-report.png and tell me 
what's wrong with the UI.
```

Claude Code reads the image, analyzes it visually, and describes what it sees. This is invaluable for debugging UI issues, reviewing design mockups, or understanding diagram-based documentation.

**Reading PDFs:** Read handles PDF files with page range support. For large PDFs, specify which pages you need:

```
Read pages 12-15 of the API specification document.
```

Claude Code extracts and presents the content from those specific pages. Maximum 20 pages per request — for larger documents, read in chunks.

**Reading Jupyter notebooks:** Claude Code reads `.ipynb` files and presents all cells — code, markdown, and outputs — in a coherent format. It can analyze data science notebooks, understand the analysis flow, and suggest improvements.

> **Tip:** For large files (1000+ lines), always guide Claude to read specific sections. "Read the UserController class in src/controllers/user.ts" is much more efficient than letting Claude read the entire file. "Read lines 200-250 of the config file" is even more precise. This directly impacts your token cost — reading 50 lines costs a fraction of reading 2000.

### Edit — Surgical Precision

Edit is Claude Code's primary tool for modifying existing files. It works by exact string matching — you specify the old text and the new text, and Edit replaces one with the other.

**Key characteristics:**

1. **Must read first.** Claude Code must Read a file before it can Edit it. This is a safety requirement — it prevents blind modifications to files Claude hasn't seen. If Claude tries to edit a file it hasn't read, the tool returns an error.

2. **Exact string match, not regex.** The `old_string` must appear exactly as it exists in the file — same characters, same whitespace, same indentation. This eliminates the class of bugs where a regex accidentally matches more than intended.

3. **Must be unique.** The `old_string` must appear exactly once in the file. If it appears multiple times, the edit fails and Claude Code must provide more surrounding context to make the match unique. This prevents accidental edits to the wrong location.

4. **Preserves formatting.** Edit respects the file's existing indentation — tabs vs. spaces, indent level, line endings. The replacement text is inserted exactly as specified, without reformatting.

5. **`replace_all` for bulk changes.** When you intentionally want to replace every occurrence (like renaming a variable), Edit supports a `replace_all: true` flag that replaces all matches in the file.

**Why Edit over Write?** Edit sends only the diff — the old string and the new string. Write sends the entire file contents. For a 500-line file where you're changing 3 lines, Edit transmits roughly 6 lines of data while Write transmits 500. This makes Edit approximately 10x cheaper in terms of token usage, and significantly safer since it can't accidentally overwrite unrelated code.

**Example edit flow:**

You ask: "Add error handling to the database query in the users route."

Claude Code:
1. **Reads** `src/routes/users.ts` to see the current code
2. **Identifies** the database query that needs error handling
3. **Edits** with:

```
old_string: "const users = await db.users.findAll();\n  res.json(users);"
new_string: "try {\n    const users = await db.users.findAll();\n    
  res.json(users);\n  } catch (error) {\n    console.error('Failed to 
  fetch users:', error);\n    res.status(500).json({ error: 'Internal 
  server error' });\n  }"
```

Only the affected lines are transmitted and modified. Everything else in the file remains untouched.

### Multi-File Operations

Claude Code's real strength emerges with operations spanning multiple files. A rename, a refactor, or an API change might touch dozens of files — Claude Code handles this methodically.

**Example: Renaming across a codebase**

```
Rename the userId field to user_id in all model files and 
everywhere it's referenced.
```

Claude Code executes a systematic workflow:

1. **Grep** for `userId` across all files to find every occurrence
2. **Read** each file to understand the context (is it a variable declaration, a function parameter, a database column name?)
3. **Edit** each file, replacing `userId` with `user_id` — using `replace_all: true` when appropriate
4. **Verify** by grepping again to confirm no occurrences were missed
5. **Run tests** (if available) to confirm the rename didn't break anything

This workflow handles the tricky cases that a simple find-and-replace misses:
- Import statements that reference `userId`
- TypeScript interfaces and type definitions
- Database query builder calls
- API response objects
- Test assertions that check for `userId` in responses

**Example: Updating an API response format**

```
Change all API endpoints to wrap responses in { data: ..., meta: { timestamp, requestId } }
```

Claude Code finds every API route handler, reads each one to understand the current response format, edits each to add the wrapper, and updates the corresponding tests and type definitions. One prompt, potentially dozens of coordinated edits.

### Navigation Patterns for Large Codebases

When working with unfamiliar or large codebases (thousands of files), experienced Claude Code users follow a consistent pattern:

**1. Start broad — map the terrain:**

```
What's the overall structure of this project? List the main 
directories and their purposes.
```

Claude Code globs the top-level directories, reads key files (README, package.json, main entry points), and builds a mental map.

**2. Narrow down — find the relevant area:**

```
I need to understand the payment processing flow. Where does 
that live?
```

Claude Code greps for payment-related terms, identifies the relevant directories and files, and focuses its attention.

**3. Deep dive — understand the specifics:**

```
Walk me through the checkout flow from the moment a user 
clicks "Buy" to the payment confirmation.
```

Claude Code reads the relevant files in order, tracing the flow from UI handler to API route to service layer to database, explaining each step.

**4. Edit — make the change:**

```
Add support for Apple Pay to the checkout flow.
```

Now Claude Code has full context — it knows the architecture, the conventions, the existing payment integrations, and the specific files involved. The edits it makes will be consistent with everything it learned in steps 1-3.

Skipping the exploration steps and jumping straight to "add Apple Pay support" forces Claude Code to do all the discovery and implementation in one pass. The result is usually worse — it might put code in the wrong place, miss an integration point, or violate a convention it hadn't learned yet.

> **Tip:** Treat your first few prompts in any session as investment in Claude Code's context. A minute spent on exploration saves five minutes of correction later. "Explain the auth system before you change it" is almost always worth the extra round-trip.

### Watching Claude Work

When Claude Code navigates and edits your code, you can observe its tool calls in real time. Toggling verbose mode with `Ctrl+O` shows every Glob, Grep, Read, and Edit call with their parameters and results.

This is useful for two reasons:

1. **Learning** — You see exactly how Claude Code approaches code navigation. Which patterns does it search for? How does it narrow down from hundreds of files to the one that matters? These strategies are useful for your own development.

2. **Debugging** — If Claude Code is making wrong edits, verbose mode reveals why. Maybe it read the wrong file, or its grep pattern matched something unexpected. Seeing the raw tool calls lets you diagnose and redirect: "You're editing the wrong file — the auth middleware is in `src/middleware/auth.ts`, not `src/utils/auth.ts`."

Most of the time, you don't need verbose mode — Claude Code's summaries are sufficient. But when you want to understand the machine, `Ctrl+O` pulls back the curtain.

---


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


## Chapter 10: Hooks — Automate Everything

Hooks are shell commands that run automatically at specific points in Claude Code's lifecycle. When Claude edits a file, a hook can auto-format it. When Claude runs a command, a hook can block it if it's dangerous. When Claude finishes working, a hook can run your test suite.

If CLAUDE.md teaches Claude Code what to do, hooks enforce how it's done. They're the mechanism that turns "please follow our code style" from a suggestion into an automated guarantee.

This is one of Claude Code's most powerful features, and one of its least known. Most users never touch hooks. The ones who do tend to wonder how they ever worked without them.

### What Hooks Replace

Without hooks, you rely on Claude Code to remember your rules. "Always run prettier after editing." "Don't touch files in the deploy/ directory." "Run tests before committing." Claude Code usually follows these instructions — but "usually" isn't "always."

Hooks make it automatic. Format-on-edit. Block-on-violation. Test-on-completion. No relying on memory. No forgetting. Every edit, every command, every session — the hooks fire.

### Hook Events

Hooks fire at specific lifecycle events. Here's when each one triggers:

| Event | When It Fires | Typical Use Case |
|-------|---------------|------------------|
| `PreToolUse` | Before a tool executes | Block dangerous commands, validate inputs |
| `PostToolUse` | After a tool succeeds | Auto-format, auto-lint, log actions |
| `Notification` | Claude sends a notification | Slack alert, desktop popup, sound |
| `Stop` | Claude finishes a turn | Auto-run tests, verify state |
| `SubagentStop` | A subagent finishes | Validate subagent output |
| `SessionStart` | Session begins | Inject context, check prerequisites |
| `UserPromptSubmit` | User sends a prompt | Pre-process input, add context |

The most impactful events for daily use are `PostToolUse` (auto-formatting), `PreToolUse` (blocking dangerous operations), and `Stop` (auto-testing).

### Hook Types

Hooks come in four varieties, each suited to different automation needs:

**`command`** — Run a shell command. This is the most common type. The command receives context via stdin (as JSON) and can influence Claude Code's behavior through its exit code and stderr output.

```json
{
  "type": "command",
  "command": "prettier --write $CLAUDE_FILE_PATH"
}
```

**`prompt`** — Make a single LLM call. Useful when you need an AI decision without spawning a full conversation. The LLM evaluates the situation and returns a judgment.

```json
{
  "type": "prompt",
  "prompt": "Review this edit for security issues. Return APPROVE or DENY with reason."
}
```

**`agent`** — Spawn a subagent. This is a full Claude Code instance that can read files, run commands, and make decisions. Use this for complex verification that requires multi-step reasoning.

```json
{
  "type": "agent",
  "prompt": "Verify this change doesn't break any existing tests. Run the test suite and report."
}
```

**`http`** — POST to a webhook. Sends the hook context as JSON to a URL. Use this for external integrations — logging to a service, triggering CI, notifying a dashboard.

```json
{
  "type": "http",
  "url": "https://hooks.slack.com/services/T00/B00/xxxx"
}
```

### Configuration

Hooks are configured in your settings.json file. Each hook specifies which event it fires on, an optional matcher to filter by tool name, and the hook action:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
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

This hook fires after every `Edit` tool call and runs Prettier on the edited file. The `$CLAUDE_FILE_PATH` variable is populated automatically with the path of the file that was just modified.

You can have multiple hooks on the same event:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATH"
          },
          {
            "type": "command",
            "command": "eslint --fix $CLAUDE_FILE_PATH"
          }
        ]
      }
    ]
  }
}
```

Both Prettier and ESLint run after every edit, in order.

### Five Practical Hook Recipes

Here are five hooks you can drop into your settings.json today.

#### 1. Auto-Format on Edit

The most popular hook. Every file Claude edits gets formatted automatically — no "please run prettier" needed.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write $CLAUDE_FILE_PATH 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

The `2>/dev/null || true` ensures the hook doesn't fail on files Prettier doesn't support (images, binary files, etc.).

For Python projects, swap Prettier for Black:

```json
{
  "type": "command",
  "command": "black $CLAUDE_FILE_PATH 2>/dev/null || true"
}
```

#### 2. Auto-Lint with Error Feedback

This hook runs ESLint after edits and feeds any errors back to Claude Code, creating a self-correcting loop:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx eslint $CLAUDE_FILE_PATH --format compact 2>&1 || true"
          }
        ]
      }
    ]
  }
}
```

When ESLint finds issues, its output is fed back to Claude Code as hook output. Claude sees the lint errors and fixes them in the next edit. This creates an automatic format-lint-fix cycle without any manual intervention.

#### 3. Desktop Notification When Claude Needs Input

When Claude Code sends a notification (waiting for permission, asking a question), this hook triggers a macOS desktop notification:

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

On Linux, replace `osascript` with `notify-send`:

```json
{
  "type": "command",
  "command": "notify-send 'Claude Code' 'Needs your attention'"
}
```

This is invaluable when you're working in another window while Claude Code runs a long task.

#### 4. Block Edits to Protected Files

Some files should never be modified by AI — production configs, lock files, security-critical code. This hook blocks edits to protected paths:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo $CLAUDE_FILE_PATH | grep -qE '(\\.env|lock\\.json|yarn\\.lock|package-lock|deploy/prod)' && echo 'BLOCKED: Protected file' >&2 && exit 2 || exit 0"
          }
        ]
      }
    ]
  }
}
```

Exit code 2 tells Claude Code to block the action. The message on stderr is shown to Claude as the reason for the block. Claude Code sees "BLOCKED: Protected file" and knows to find an alternative approach.

#### 5. Audit Log of All Tool Calls

Track everything Claude Code does in a log file — useful for reviewing what happened in long autonomous sessions:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date +%H:%M:%S) $CLAUDE_TOOL_NAME: $CLAUDE_FILE_PATH\" >> /tmp/claude-audit.log"
          }
        ]
      }
    ]
  }
}
```

After a session, check `/tmp/claude-audit.log` to see a chronological record of every tool Claude used and which files it touched.

### Hook Input and Output

When a hook runs, it receives a JSON payload on stdin containing the full context of the event:

```json
{
  "session_id": "abc123",
  "cwd": "/Users/dev/myproject",
  "hook_event_name": "PostToolUse",
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/Users/dev/myproject/src/api/users.ts",
    "old_string": "const users = db.query(...)",
    "new_string": "const users = await db.query(...)"
  }
}
```

This means your hooks can make intelligent decisions based on context — which tool ran, what file was affected, what the edit contained.

**Exit codes control behavior:**

| Exit Code | Meaning |
|-----------|---------|
| `0` | Allow — the action proceeds normally |
| `2` | Block — the action is denied. Reason is read from stderr |
| Other | Error — logged but action still proceeds |

**Hook output is fed back to Claude.** Whatever your hook prints to stdout becomes part of Claude Code's context. This is the mechanism that makes the lint feedback loop work — ESLint's output goes to stdout, Claude reads it, and Claude fixes the issues.

### The Feedback Loop

The most powerful pattern with hooks is the automatic feedback loop. Here's how it works:

1. Claude edits a file
2. `PostToolUse` hook runs the linter
3. Linter finds 2 errors and prints them to stdout
4. Claude Code receives the linter output
5. Claude reads the errors and makes a second edit to fix them
6. `PostToolUse` hook runs the linter again
7. Linter passes — zero errors
8. Claude moves on

This happens automatically. You don't intervene. Claude edits, gets feedback, corrects, and the linter confirms. Every edit converges toward clean code.

The same pattern works for type checking:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "cd $CLAUDE_PROJECT_DIR && npx tsc --noEmit --pretty 2>&1 | head -20 || true"
          }
        ]
      }
    ]
  }
}
```

Now every edit is type-checked. If Claude introduces a type error, it sees the TypeScript compiler output and fixes it immediately. You get type-safe edits without ever asking.

### Hooks Override Permissions

Here's a critical insight that most users miss: **hooks operate above the permission system.** Even in the most permissive mode where Claude Code has full autonomy, a `PreToolUse` hook that returns exit code 2 will still block the action.

This means hooks are your ultimate safety net. You can give Claude Code broad permissions for speed while using hooks to enforce hard boundaries:

- Full autonomy for edits and commands — but hooks block modifications to `deploy/`, `.env`, and `*.lock`
- Full autonomy for git operations — but a hook prevents force-pushes to `main`
- Full autonomy for file creation — but a hook prevents creating files larger than 100KB

Permissions say what Claude Code is allowed to do. Hooks enforce what it actually does. When they conflict, hooks win.

> **Tip:** Start with one hook — auto-format on edit. It's low-risk, high-reward, and teaches you how hooks work. Once you're comfortable, add lint feedback. Then protected file blocking. Build your hook collection incrementally rather than configuring everything at once.

---


## Chapter 11: MCP Servers — Extend Claude Code Infinitely

Out of the box, Claude Code can read files, write files, search code, and run shell commands. That's powerful for pure code work. But real-world development involves more than code — you interact with databases, issue trackers, deployment platforms, documentation wikis, messaging systems, and dozens of other tools.

MCP — the Model Context Protocol — lets Claude Code talk to all of them. It's an open standard that gives AI models a way to connect with external tools and data sources through a simple, unified interface. Think of MCP servers as USB ports for Claude Code: plug in a PostgreSQL server, and Claude can query your database. Plug in a GitHub server, and Claude can search issues and create pull requests. Plug in a Slack server, and Claude can read and send messages.

The result is a Claude Code that doesn't just work with your code — it works with your entire development environment.

### Why MCP Matters

Without MCP, when you need Claude Code to check something in your database, the workflow looks like this:

1. You switch to your database client
2. Run a query
3. Copy the results
4. Paste them into Claude Code
5. Claude analyzes and responds

With MCP, Claude Code queries the database directly:

```
What are the most common error types in the logs table from the last 24 hours?
```

Claude Code runs the SQL query through the MCP server, gets the results, and analyzes them — all in one step. No context switching, no copy-pasting, no manual query writing.

This same pattern applies to every external tool. Instead of being the manual bridge between Claude Code and your infrastructure, MCP lets Claude Code reach out directly.

### Configuration

MCP servers are configured in your settings.json file under the `mcpServers` key. Each server has a name, a command to start it, and optional environment variables:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/mydb"
      }
    }
  }
}
```

When Claude Code starts, it launches each configured MCP server as a subprocess. The servers communicate with Claude Code using JSON-RPC over stdin/stdout — a simple, fast protocol that works everywhere.

You can configure multiple servers simultaneously:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/mydb"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-xxxxxxxxxxxx"
      }
    }
  }
}
```

Now Claude Code can query your database, manage GitHub issues, and send Slack messages — all from the same conversation.

### Popular MCP Servers

The MCP ecosystem is growing rapidly. Here are the servers you're most likely to use:

| Server | Package | What It Does |
|--------|---------|-------------|
| PostgreSQL | `@modelcontextprotocol/server-postgres` | Run SQL queries, inspect schema, manage data |
| GitHub | `@modelcontextprotocol/server-github` | Issues, PRs, code search, repository management |
| Slack | `@modelcontextprotocol/server-slack` | Read channels, send messages, search history |
| Filesystem | `@modelcontextprotocol/server-filesystem` | Sandboxed file access with configurable root |
| Puppeteer | `@modelcontextprotocol/server-puppeteer` | Browser automation, screenshots, web scraping |
| SQLite | `@modelcontextprotocol/server-sqlite` | Query SQLite databases, inspect tables |
| Memory | `@modelcontextprotocol/server-memory` | Persistent key-value store for cross-session data |
| Vercel | `@vercel/mcp` | Deployments, logs, environment variables, domains |

Community-built servers extend this further — there are MCP servers for Notion, Jira, Linear, MongoDB, Redis, Docker, Kubernetes, and dozens more. The registry at `mcp.so` lists available servers.

### Practical Examples

**Database exploration:**

```
Show me the schema of the users table and the 10 most recent 
signups with their subscription status.
```

With the PostgreSQL MCP server configured, Claude Code runs `\d users` to get the schema, then executes `SELECT * FROM users ORDER BY created_at DESC LIMIT 10`, joined with the subscriptions table. You get a formatted table without writing any SQL yourself.

**Issue triage:**

```
Find all open GitHub issues labeled "bug" that were created in 
the last week. Summarize them and suggest which ones I should 
prioritize.
```

With the GitHub MCP server, Claude Code fetches the issues via the GitHub API, reads their descriptions and comments, and provides a prioritized summary.

**Deployment monitoring:**

```
Check the latest Vercel deployment. Did it succeed? Show me any 
error logs if it failed.
```

With the Vercel MCP server, Claude Code checks deployment status and pulls logs — saving you from navigating the Vercel dashboard.

### Building Your Own MCP Server

If an existing MCP server doesn't cover your needs, building one is straightforward. MCP servers expose tools via JSON-RPC — each tool has a name, a description, and input/output schemas.

Here's a minimal MCP server in TypeScript that exposes a single tool:

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from 
  "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "weather",
  version: "1.0.0"
});

server.tool(
  "get_weather",
  "Get current weather for a city",
  { city: z.string().describe("City name") },
  async ({ city }) => {
    const res = await fetch(
      `https://wttr.in/${city}?format=j1`
    );
    const data = await res.json();
    const current = data.current_condition[0];
    return {
      content: [{
        type: "text",
        text: `${city}: ${current.temp_C}°C, ` +
              `${current.weatherDesc[0].value}`
      }]
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

In Python, the equivalent uses the `mcp` package:

```python
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("weather")

@mcp.tool()
async def get_weather(city: str) -> str:
    """Get current weather for a city."""
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://wttr.in/{city}?format=j1"
        )
        data = r.json()
        c = data["current_condition"][0]
        return f"{city}: {c['temp_C']}°C, " \
               f"{c['weatherDesc'][0]['value']}"

mcp.run()
```

Configure your custom server the same way:

```json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": ["./my-mcp-servers/weather.js"]
    }
  }
}
```

Now Claude Code can check the weather. More practically, you can build MCP servers that connect to your company's internal APIs, proprietary databases, or custom tooling that no public server supports.

### Security Considerations

MCP servers have the same access as any process you run. A PostgreSQL MCP server can read and write your database. A filesystem MCP server can access files within its configured root. A GitHub MCP server can create issues and PRs with your token.

**Review what you connect.** Don't blindly install MCP servers from unknown sources. Each server gets real credentials and real access to your systems.

**Use environment variables for credentials.** Never hardcode tokens or passwords in settings.json:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**Use `settings.local.json` for personal secrets.** Project-level settings.json is committed to git — anyone who clones the repo sees it. Put your personal API keys and tokens in `settings.local.json`, which should be gitignored:

```
.claude/settings.local.json  ← your personal tokens (gitignored)
.claude/settings.json         ← shared team config (committed)
```

**Scope access narrowly.** If a GitHub MCP server only needs to read issues, create a token with `issues:read` scope — not full repository access. Principle of least privilege applies to AI tools just like it does to human access.

### Managing MCP Servers

Use the `/mcp` slash command to see all configured MCP servers, their status, and the tools they expose:

```
/mcp
```

This shows which servers are running, which tools are available, and any connection errors.

You can also specify an MCP configuration file when launching Claude Code:

```bash
claude --mcp-config ./mcp.json
```

This is useful for project-specific MCP setups, CI environments, or when switching between different server configurations.

To restart a specific MCP server without restarting Claude Code:

```
/mcp restart postgres
```

Useful when you've updated the server configuration or the server process crashed.

> **Tip:** Start with one MCP server that solves a real friction point in your workflow. If you're constantly copy-pasting database query results into Claude Code, add the PostgreSQL server. If you're manually checking GitHub issues, add the GitHub server. One well-configured MCP server saves more time than five you barely use.

---


## Chapter 12: IDE Integration

Claude Code isn't locked to one interface. You can use it from a raw terminal, inside VS Code, within JetBrains IDEs, as a native desktop app, or through the web at claude.ai. Each interface has different strengths, and understanding them lets you pick the right one for the situation — or combine multiple for the best experience.

### Available Platforms

| Platform | Best For | Key Advantage |
|----------|----------|---------------|
| CLI (terminal) | Power users, scripting | Full feature access, fastest startup, composable with pipes |
| Desktop app | Daily development | Native system tray, multiple windows, drag-and-drop files |
| VS Code | IDE-first developers | Inline code actions, sidebar panel, deep editor integration |
| JetBrains | IntelliJ/PyCharm users | Tool window, code selection context, all JetBrains IDEs |
| Web (claude.ai/code) | Remote access, quick tasks | No install, cloud execution, scheduled tasks |

No single interface is universally "best." Power users tend to gravitate toward the CLI for its speed and scriptability, but many developers prefer the visual integration of VS Code or JetBrains. The web interface is ideal when you're not at your development machine. The desktop app sits in between — more visual than the CLI, more flexible than an IDE extension.

### VS Code Integration

The VS Code extension puts Claude Code in a sidebar panel within your editor. Install it from the VS Code marketplace by searching for "Claude Code" or from the command line:

```bash
code --install-extension anthropic.claude-code
```

**Sidebar panel:** Claude Code appears as a panel in your VS Code sidebar. You can chat with it, see file edits in real-time, and approve or reject changes — all without leaving the editor. The conversation history persists across panel toggles.

**Inline code actions:** Right-click any code selection and you'll see Claude Code actions in the context menu. "Explain this code," "Refactor this function," "Add tests for this selection" — these send the selected code directly to Claude Code with your instruction.

```
Right-click on a function → Claude Code → "Add error handling"
```

Claude Code receives the selected code plus its file path and surrounding context, making its edits more precise than if you described the code verbally.

**Terminal integration:** VS Code's integrated terminal runs Claude Code natively. You can have the sidebar panel open for visual feedback while running CLI commands in the terminal — two interfaces to the same underlying engine.

**File context:** When you have files open in VS Code, Claude Code can see which tabs are active. This helps it understand what you're currently working on. If you have `users.ts` and `users.test.ts` open, Claude Code infers you're working on the users module.

### JetBrains Integration

Claude Code works in all JetBrains IDEs — IntelliJ IDEA, PyCharm, WebStorm, GoLand, RubyMine, PhpStorm, CLion, and Rider. The integration is a plugin available from the JetBrains Marketplace.

**Tool window:** Claude Code appears as a tool window (similar to the terminal or git panels). You can dock it to any side of the IDE, resize it, or pop it out into a separate window.

**Code selection context:** Select code in the editor and send it to Claude Code with a keyboard shortcut. The selection, file path, and surrounding context are included automatically — just like the VS Code inline actions.

**Project-aware:** The plugin reads your project's structure, detecting the framework, language, build system, and dependencies. This information is available to Claude Code without you describing it.

**Configuration:** JetBrains plugin settings let you configure the model, permission mode, and other options through the IDE's preferences panel — no need to edit settings.json directly.

### Desktop Application

The Claude Code desktop app is a native application that runs independently of any IDE. It provides a dedicated, always-available interface to Claude Code.

**System tray:** The desktop app lives in your system tray (macOS menu bar or Windows taskbar). Click the icon to open a conversation instantly. This makes Claude Code feel like a utility that's always one click away, not a tool you need to launch.

**Multiple sessions:** Open multiple windows for different projects or conversations. Work on a frontend task in one window and a backend task in another — each with its own context, history, and project scope.

**Drag and drop:** Drop files directly into the desktop app window. Screenshots, PDFs, images, code files — the app reads them and makes them available to Claude Code. This is the fastest way to share visual context like error screenshots or design mockups.

**Launch from terminal:** The `/desktop` command in the CLI opens the desktop app with your current project context:

```bash
claude
> /desktop
```

This bridges the CLI and desktop workflows — start in the terminal, switch to the desktop app when you want a richer visual experience.

### Web Interface

Claude Code is available on the web at claude.ai, with a code-specific mode that connects to a cloud execution environment. This is the only interface that doesn't require a local installation.

**Remote cloud execution:** Code runs on Vercel's cloud infrastructure, not your local machine. This means you can use Claude Code from a tablet, a Chromebook, or any device with a web browser — no development environment needed.

**Scheduled tasks:** The web interface supports the `/schedule` command, which creates tasks that run on a cron schedule without your machine being online:

```
/schedule "Run the test suite and report failures" every day at 9am
```

This creates a cloud-based Claude Code agent that executes the task on schedule and sends you the results. Useful for daily status checks, automated reporting, and maintenance tasks.

**No local CLI needed:** For quick questions, code reviews, or tasks that don't need access to your local filesystem, the web interface is the fastest path. Open a browser, paste some code, get an answer.

**Limitations:** The web interface runs in a sandboxed cloud environment. It doesn't have access to your local files, local databases, or local services. For tasks that require your actual development environment, use the CLI or an IDE extension.

### Why Experts Prefer the CLI

Every interface is built on top of the CLI. The VS Code extension, the JetBrains plugin, and the desktop app all use the same Claude Code engine underneath. But the CLI exposes capabilities that the graphical interfaces don't.

**Fastest startup.** No extension loading, no GUI rendering. `claude` in the terminal and you're working in under a second.

**Works over SSH.** When you're debugging on a remote server, the CLI works in your SSH session. No port forwarding, no remote desktop, no workarounds. SSH in, run `claude`, and you have full Claude Code access on the remote machine.

**Full feature access.** Every Claude Code flag, every configuration option, every edge case is accessible from the CLI. IDE extensions surface the most common features but necessarily simplify the interface. The CLI hides nothing.

**Scriptable with pipes.** The CLI composes with standard Unix tools. This opens up workflows that graphical interfaces can't match:

```bash
# One-shot query — no interactive session
echo "Explain this error" | claude -p

# Pipe code for review
git diff | claude -p "Review this diff for bugs"

# Pipe a file for analysis
cat logs/error.log | claude -p "What caused these errors?"

# Generate and use output in scripts
claude --print "Write a regex that matches email addresses" \
  > /tmp/regex.txt
```

The `-p` flag (or `--print`) runs Claude Code in non-interactive mode — it reads stdin, processes the prompt, prints the result to stdout, and exits. No conversation, no session, just input-output. This makes Claude Code a composable Unix tool.

**Combine with other commands:**

```bash
# Find all TODO comments and ask for prioritization
grep -rn "TODO" src/ | claude -p "Prioritize these TODOs"

# Analyze test coverage gaps
npm test -- --coverage 2>&1 | claude -p "What areas need more tests?"

# Review a specific commit
git show abc1234 | claude -p "Review this commit"
```

**Multiple CLI flags not available in IDE extensions:**

```bash
# Specify model
claude --model claude-sonnet-4-20250514

# Set permission mode
claude --allowedTools "Edit,Read,Grep,Glob"

# Resume previous conversation
claude --resume

# Continue most recent conversation
claude --continue

# Use specific MCP config
claude --mcp-config ./custom-mcp.json

# Output format for scripting
claude -p "query" --output-format json
```

These flags give you precise control over every aspect of Claude Code's behavior — control that graphical interfaces abstract away.

### Multi-Environment Setup

Most developers use Claude Code across multiple machines and projects. Here's how configuration travels:

**Global CLAUDE.md** (`~/.claude/CLAUDE.md`) — Your personal preferences. This stays on your machine and applies to every project. It doesn't sync across machines automatically, but you can symlink it to a dotfiles repository:

```bash
ln -s ~/dotfiles/claude/CLAUDE.md ~/.claude/CLAUDE.md
```

Now your Claude Code preferences sync wherever you sync your dotfiles.

**Project CLAUDE.md** (repo root) — Travels with the repository. When you clone a project on a new machine, `git clone` brings the CLAUDE.md with it. Every team member gets the same instructions.

**Memory** (`~/.claude/projects/`) — Per-machine, per-project. Memory does not sync between machines. If you use both a laptop and a desktop, each builds its own memory independently. This is by design — memory contains machine-specific context that might not apply elsewhere.

**Settings** (`.claude/settings.json`) — Can be committed to git for team-wide settings. Use `.claude/settings.local.json` for personal overrides that shouldn't be shared (API keys, personal tool preferences).

A typical team setup:

```
Committed to git:
  CLAUDE.md                    ← project rules (team-shared)
  .claude/settings.json        ← shared settings (hooks, MCP)
  .claude/rules/*.md           ← path-specific rules

Not committed (gitignored):
  .claude/settings.local.json  ← personal API keys, overrides
  ~/.claude/CLAUDE.md          ← global personal preferences
  ~/.claude/projects/*/memory/ ← auto-memory (per-machine)
```

This separation means the team shares rules and configurations, while individual preferences and secrets stay personal.

### Choosing Your Setup

Here's a decision framework:

**You're a terminal power user** — Use the CLI as your primary interface. Keep a terminal pane dedicated to Claude Code in your tmux or terminal multiplexer. Use pipes for one-shot tasks.

**You want visual integration** — Use VS Code or JetBrains. The inline code actions and sidebar panel make Claude Code feel like part of the IDE. Fall back to the CLI for advanced flags and scripting.

**You want always-available access** — Use the desktop app. System tray presence means Claude Code is one click away regardless of what you're doing.

**You work on multiple machines** — Use the web interface for quick tasks from any device. Use the CLI or IDE extension on your primary development machines.

**Best of all worlds** — Use the IDE extension for daily development, the CLI for scripting and automation, and the desktop app or web interface for quick access. They all share the same CLAUDE.md and project configuration, so switching between them is seamless.

> **Tip:** Even if you use an IDE daily, learn the CLI. It's the most powerful interface, with features that IDE extensions don't expose. The pipe workflow alone — `git diff | claude -p "review this"` — is worth the learning curve. You'll find yourself reaching for it whenever you need something fast, scriptable, or precise.

---


