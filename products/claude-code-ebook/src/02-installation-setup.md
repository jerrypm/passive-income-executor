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
