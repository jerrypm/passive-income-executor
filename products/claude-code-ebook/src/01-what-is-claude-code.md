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
