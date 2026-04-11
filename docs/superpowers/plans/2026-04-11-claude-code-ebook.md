# Mastering Claude Code — Ebook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a professional 100+ page ebook "Mastering Claude Code: From Zero to Expert" covering beginner-to-expert usage with 50 hidden tips, ready for Gumroad sale at $19.

**Architecture:** Markdown chapters in `src/` → concatenated master MD → pandoc styled HTML → Chrome headless PDF. Same proven pipeline used for the 1000-expert-prompts product. Each chapter is a standalone `.md` file. Cover page is a styled HTML file screenshotted to PNG.

**Tech Stack:** Markdown, pandoc, Chrome headless (PDF), HTML/CSS (cover + ebook styling). No Python deps needed.

**Pricing:** $19 launch → $29 after social proof

---

## File Map

```
products/claude-code-ebook/
├── README.md                           # Build instructions + pre-launch checklist
├── gumroad-listing.md                  # Full Gumroad product listing copy
├── build.sh                            # Build script (MD → HTML → PDF → ZIP)
├── ebook.css                           # Professional ebook styling (dark code blocks, orange accents)
├── cover.html                          # HTML cover page for screenshot
├── src/
│   ├── 00-front-matter.md              # Title, subtitle, about, how to use this book
│   ├── 01-what-is-claude-code.md       # Ch 1: What is Claude Code
│   ├── 02-installation-setup.md        # Ch 2: Installation & Setup
│   ├── 03-first-real-task.md           # Ch 3: Your First Real Task
│   ├── 04-permission-modes.md          # Ch 4: Permission Modes
│   ├── 05-claude-md.md                 # Ch 5: CLAUDE.md
│   ├── 06-slash-commands.md            # Ch 6: Slash Commands
│   ├── 07-git-workflow.md              # Ch 7: Git Workflow
│   ├── 08-code-navigation.md           # Ch 8: Code Navigation & Editing
│   ├── 09-memory-system.md             # Ch 9: Memory System
│   ├── 10-hooks.md                     # Ch 10: Hooks
│   ├── 11-mcp-servers.md               # Ch 11: MCP Servers
│   ├── 12-ide-integration.md           # Ch 12: IDE Integration
│   ├── 13-prompt-engineering.md        # Ch 13: Prompt Engineering
│   ├── 14-parallel-development.md      # Ch 14: Subagents & Worktrees
│   ├── 15-custom-skills.md             # Ch 15: Custom Skills & Superpowers
│   ├── 16-hidden-tips.md               # Ch 16: 50 Hidden Tips & Tricks
│   ├── 17-building-feature.md          # Ch 17: Case Study — Full Feature
│   ├── 18-debugging-pro.md             # Ch 18: Debugging Like a Pro
│   ├── 19-cost-optimization.md         # Ch 19: Cost Optimization
│   └── 20-custom-setup.md              # Ch 20: Your Custom Setup Blueprint
├── mastering-claude-code.md            # Generated: concatenated master
├── mastering-claude-code.html          # Generated: styled HTML
├── mastering-claude-code.pdf           # Generated: final PDF
└── mastering-claude-code.zip           # Generated: Gumroad download bundle
```

---

## Task 1: Project Setup + Build Pipeline

**Files:**
- Create: `products/claude-code-ebook/build.sh`
- Create: `products/claude-code-ebook/ebook.css`
- Create: `products/claude-code-ebook/src/00-front-matter.md`

- [ ] **Step 1: Create project directory structure**

```bash
mkdir -p products/claude-code-ebook/src
```

- [ ] **Step 2: Write the ebook CSS stylesheet**

Create `products/claude-code-ebook/ebook.css` with professional ebook styling:

```css
/* Mastering Claude Code — Ebook Stylesheet */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Playfair+Display:wght@700;900&display=swap');

:root {
  --accent: #D97706;      /* amber-600 — Claude's orange */
  --accent-light: #FEF3C7;
  --bg: #ffffff;
  --text: #1a1a2e;
  --text-muted: #6b7280;
  --code-bg: #1e1e2e;     /* catppuccin mocha base */
  --code-text: #cdd6f4;
  --border: #e5e7eb;
  --tip-bg: #fffbeb;
  --tip-border: #D97706;
  --warning-bg: #fef2f2;
  --warning-border: #dc2626;
}

* { box-sizing: border-box; }

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 11pt;
  line-height: 1.7;
  color: var(--text);
  background: var(--bg);
  max-width: 720px;
  margin: 0 auto;
  padding: 40px 50px;
}

/* Headings */
h1 {
  font-family: 'Playfair Display', Georgia, serif;
  font-weight: 900;
  font-size: 28pt;
  color: var(--text);
  margin-top: 60px;
  margin-bottom: 20px;
  page-break-before: always;
  border-bottom: 3px solid var(--accent);
  padding-bottom: 12px;
}

h1:first-of-type { page-break-before: avoid; }

h2 {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 16pt;
  color: var(--accent);
  margin-top: 36px;
  margin-bottom: 12px;
}

h3 {
  font-weight: 600;
  font-size: 13pt;
  margin-top: 24px;
  margin-bottom: 8px;
}

/* Code blocks */
pre {
  background: var(--code-bg);
  color: var(--code-text);
  border-radius: 8px;
  padding: 16px 20px;
  font-family: 'JetBrains Mono', 'SF Mono', monospace;
  font-size: 9.5pt;
  line-height: 1.5;
  overflow-x: auto;
  margin: 16px 0;
  border-left: 4px solid var(--accent);
}

code {
  font-family: 'JetBrains Mono', 'SF Mono', monospace;
  font-size: 9pt;
  background: #f3f4f6;
  padding: 2px 6px;
  border-radius: 4px;
}

pre code {
  background: none;
  padding: 0;
  font-size: inherit;
}

/* Tables */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  font-size: 10pt;
}

th {
  background: var(--accent);
  color: white;
  padding: 10px 14px;
  text-align: left;
  font-weight: 600;
}

td {
  padding: 10px 14px;
  border-bottom: 1px solid var(--border);
}

tr:nth-child(even) td { background: #f9fafb; }

/* Blockquotes as tips */
blockquote {
  background: var(--tip-bg);
  border-left: 4px solid var(--tip-border);
  padding: 14px 20px;
  margin: 16px 0;
  border-radius: 0 8px 8px 0;
  font-size: 10.5pt;
}

blockquote p:first-child { margin-top: 0; }
blockquote p:last-child { margin-bottom: 0; }

/* Links */
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

/* Lists */
ul, ol { padding-left: 24px; margin: 12px 0; }
li { margin: 6px 0; }

/* Horizontal rule as section break */
hr {
  border: none;
  border-top: 2px solid var(--border);
  margin: 40px 0;
}

/* Table of Contents */
#TOC {
  background: #f9fafb;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 24px 32px;
  margin: 24px 0 40px;
}

#TOC ul { list-style: none; padding-left: 0; }
#TOC > ul > li { margin: 8px 0; font-weight: 600; }
#TOC > ul > li > ul > li { font-weight: 400; margin: 4px 0; padding-left: 20px; }

/* Print/PDF */
@media print {
  body { padding: 0; max-width: none; }
  h1 { page-break-before: always; }
  pre, blockquote, table { page-break-inside: avoid; }
}
```

- [ ] **Step 3: Write the build script**

Create `products/claude-code-ebook/build.sh`:

```bash
#!/bin/bash
# Mastering Claude Code — Build Script
# Usage: ./build.sh [html|pdf|zip|all]

set -euo pipefail
cd "$(dirname "$0")"

BOOK="mastering-claude-code"
CSS="ebook.css"

build_md() {
  echo "→ Concatenating chapters..."
  cat src/00-front-matter.md \
      src/01-*.md src/02-*.md src/03-*.md src/04-*.md \
      src/05-*.md src/06-*.md src/07-*.md src/08-*.md \
      src/09-*.md src/10-*.md src/11-*.md src/12-*.md \
      src/13-*.md src/14-*.md src/15-*.md src/16-*.md \
      src/17-*.md src/18-*.md src/19-*.md src/20-*.md \
      > "${BOOK}.md"
  echo "  ✓ ${BOOK}.md ($(wc -l < "${BOOK}.md") lines)"
}

build_html() {
  build_md
  echo "→ Building styled HTML..."
  pandoc "${BOOK}.md" \
    -o "${BOOK}.html" \
    --standalone \
    --toc \
    --toc-depth=2 \
    --metadata title="Mastering Claude Code" \
    -c "${CSS}" \
    --embed-resources
  echo "  ✓ ${BOOK}.html"
}

build_pdf() {
  build_html
  echo "→ Generating PDF via Chrome headless..."
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless=new --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="${BOOK}.pdf" \
    "file://$(pwd)/${BOOK}.html"
  echo "  ✓ ${BOOK}.pdf"
}

build_zip() {
  build_pdf
  echo "→ Creating Gumroad ZIP bundle..."
  zip -r "${BOOK}.zip" \
    "${BOOK}.md" \
    "${BOOK}.pdf" \
    src/
  echo "  ✓ ${BOOK}.zip"
}

case "${1:-all}" in
  md)   build_md ;;
  html) build_html ;;
  pdf)  build_pdf ;;
  zip)  build_zip ;;
  all)  build_zip ;;
  *)    echo "Usage: $0 [md|html|pdf|zip|all]" && exit 1 ;;
esac

echo "Done!"
```

```bash
chmod +x products/claude-code-ebook/build.sh
```

- [ ] **Step 4: Write the front matter**

Create `products/claude-code-ebook/src/00-front-matter.md`:

```markdown
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
```

- [ ] **Step 5: Test the build pipeline with front matter only**

```bash
cd products/claude-code-ebook
./build.sh html
# Expected: mastering-claude-code.html exists, opens in browser with styled content
open mastering-claude-code.html
```

- [ ] **Step 6: Commit**

```bash
git add products/claude-code-ebook/build.sh products/claude-code-ebook/ebook.css products/claude-code-ebook/src/00-front-matter.md
git commit -m "feat(claude-code-ebook): scaffold project + build pipeline"
```

---

## Task 2: Part 1 — Getting Started (Chapters 1-4)

**Files:**
- Create: `products/claude-code-ebook/src/01-what-is-claude-code.md`
- Create: `products/claude-code-ebook/src/02-installation-setup.md`
- Create: `products/claude-code-ebook/src/03-first-real-task.md`
- Create: `products/claude-code-ebook/src/04-permission-modes.md`

### Chapter 1: What Is Claude Code & Why It's Different

- [ ] **Step 1: Write Chapter 1 content**

Create `products/claude-code-ebook/src/01-what-is-claude-code.md`.

**Content brief — cover these sections:**

1. **What Claude Code Is** — CLI-based AI coding assistant by Anthropic. Runs in your terminal. Has direct access to your filesystem, git, shell. Not a chatbot with copy-paste — it's an agent that reads, writes, and executes.

2. **How It Differs from Other AI Tools**
   - vs ChatGPT/Claude web: Claude Code sees your actual codebase, runs commands, edits files directly
   - vs GitHub Copilot: Copilot autocompletes lines; Claude Code handles entire features, debugging sessions, multi-file refactors
   - vs Cursor/Windsurf: Similar concept but Claude Code is terminal-native, works with any editor, more powerful agent capabilities
   - vs Aider/Continue: Claude Code has deeper tool integration, memory system, hooks, MCP servers, subagent architecture

3. **What It Can Actually Do** — table showing capabilities:
   - Read any file in your project
   - Edit files with surgical precision (Edit tool, not rewriting whole files)
   - Run shell commands (build, test, deploy)
   - Search with Glob (file patterns) and Grep (content search)
   - Git operations (commit, branch, PR creation)
   - Web search and fetch
   - Read images, PDFs, Jupyter notebooks
   - Spawn sub-agents for parallel work
   - Persistent memory across conversations
   - Custom automation via hooks

4. **The Mental Model** — Think of Claude Code as a senior developer sitting next to you who can:
   - Read your entire codebase instantly
   - Run any command you'd run
   - Remember context across sessions
   - Work on multiple things in parallel
   - But needs your guidance on *what* to build and *why*

5. **Available Platforms** — CLI (terminal), Desktop app (Mac/Windows), Web app (claude.ai/code), IDE extensions (VS Code, JetBrains)

Include a comparison table. End with a "What you'll learn in this book" teaser.

### Chapter 2: Installation & Setup

- [ ] **Step 2: Write Chapter 2 content**

Create `products/claude-code-ebook/src/02-installation-setup.md`.

**Content brief:**

1. **Prerequisites** — Node.js 18+ (recommend 24 LTS), npm or Homebrew, Anthropic API key or Claude Pro/Max subscription

2. **Installation Methods**
   ```bash
   # npm (recommended)
   npm install -g @anthropic-ai/claude-code

   # Homebrew
   brew install claude-code

   # Verify
   claude --version
   ```

3. **Authentication**
   - Anthropic API key: `export ANTHROPIC_API_KEY=sk-ant-...`
   - Claude Pro/Max subscription: `claude` → follow browser auth flow
   - Which to choose: API key for pay-per-use, subscription for unlimited

4. **First Launch** — Run `claude` in any directory. Explain the welcome screen, permission prompt, model display.

5. **Configuration Basics**
   - `claude config` — view/set settings
   - `~/.claude/` directory structure: `CLAUDE.md`, `settings.json`, `keybindings.json`
   - Project-level: `.claude/` directory, `CLAUDE.md` in project root

6. **Model Selection**
   - Default: Claude Opus 4.6 (most capable)
   - `/fast` toggle: same model, faster output
   - `Shift+Tab`: cycle through models (Opus, Sonnet, Haiku)
   - `--model` flag: `claude --model sonnet`
   - When to use which: Opus for complex tasks, Sonnet for speed, Haiku for quick queries

> **Tip:** Run `claude --help` to see all CLI flags. We'll cover the important ones throughout this book.

### Chapter 3: Your First Real Task

- [ ] **Step 3: Write Chapter 3 content**

Create `products/claude-code-ebook/src/03-first-real-task.md`.

**Content brief — walk through a complete real task step by step:**

1. **Setup** — Create a sample project or use an existing one. `mkdir my-project && cd my-project && claude`

2. **Asking Questions About Code** — "What does this project do?" / "Explain the authentication flow" / "Find all API endpoints"

3. **Reading Files** — Claude uses Read tool. Show how it reads files, explain line numbers in output.

4. **Editing a File** — Ask Claude to fix a bug or add a function. Show Edit tool in action (old_string → new_string). Explain why Edit is preferred over Write (smaller diffs, less error-prone).

5. **Running Commands** — "Run the tests" / "Build the project". Show Bash tool usage. Explain timeout defaults.

6. **Creating New Files** — Ask Claude to create a new module. Show Write tool.

7. **Multi-step Tasks** — "Add a login endpoint with validation and tests." Show how Claude:
   - Plans the approach
   - Creates test file first (if TDD)
   - Creates implementation
   - Runs tests
   - Commits if asked

8. **Conversation Flow** — How to give follow-up instructions, correct Claude, ask for alternatives.

> **Tip:** The `!` prefix runs a shell command inline. Type `! ls -la` to run it without Claude interpreting it as a prompt. The output lands in the conversation context.

### Chapter 4: Understanding Permission Modes

- [ ] **Step 4: Write Chapter 4 content**

Create `products/claude-code-ebook/src/04-permission-modes.md`.

**Content brief:**

1. **Why Permissions Exist** — Claude Code can read/write files and run commands. Permissions give you control over what it can do without asking.

2. **The Four Modes**
   - **Ask mode** (default): Claude asks before every file edit and command. Safest. Good for learning.
   - **Auto-edit mode**: File edits are automatic, commands still ask. Good balance for daily work.
   - **Full-auto mode**: Everything automatic except destructive git operations. For trusted workflows.
   - **YOLO mode**: No permission prompts at all. For maximum speed when you trust the task.

3. **Allowlists** — Configure which tools auto-approve in `settings.json`:
   ```json
   {
     "permissions": {
       "allow": [
         "Read",
         "Glob",
         "Grep",
         "Bash(npm test)",
         "Bash(npm run build)"
       ]
     }
   }
   ```
   Pattern matching: `Bash(npm *)` allows any npm command. Exact match: `Bash(git status)`.

4. **Project vs Global Settings**
   - Global: `~/.claude/settings.json` — applies everywhere
   - Project: `.claude/settings.json` — applies to this repo only (commit this!)
   - Project-local: `.claude/settings.local.json` — your personal overrides (gitignored)

5. **When to Use Each Mode** — Decision flowchart:
   - Learning Claude Code → Ask mode
   - Daily development → Auto-edit
   - Running a known plan → Full-auto
   - Quick scripts/prototyping → YOLO (with caution)

6. **Safety Protocols** — Even in permissive modes, Claude Code has built-in safety:
   - Never force-pushes without confirmation
   - Never deletes branches without asking
   - Warns before committing `.env` or credential files
   - Checks for destructive git operations

> **Tip:** You can change permission mode mid-conversation. Just say "switch to auto-edit mode" or press the mode toggle shortcut.

- [ ] **Step 5: Build HTML to verify Part 1 renders**

```bash
cd products/claude-code-ebook && ./build.sh html
open mastering-claude-code.html
# Verify: TOC shows Parts 1, chapters 1-4 render with correct formatting
```

- [ ] **Step 6: Commit Part 1**

```bash
git add products/claude-code-ebook/src/01-*.md products/claude-code-ebook/src/02-*.md products/claude-code-ebook/src/03-*.md products/claude-code-ebook/src/04-*.md
git commit -m "feat(claude-code-ebook): Part 1 — Getting Started (Ch 1-4)"
```

---

## Task 3: Part 2 — Productive Development (Chapters 5-8)

**Files:**
- Create: `products/claude-code-ebook/src/05-claude-md.md`
- Create: `products/claude-code-ebook/src/06-slash-commands.md`
- Create: `products/claude-code-ebook/src/07-git-workflow.md`
- Create: `products/claude-code-ebook/src/08-code-navigation.md`

### Chapter 5: CLAUDE.md — Teaching Claude About Your Project

- [ ] **Step 1: Write Chapter 5 content**

Create `products/claude-code-ebook/src/05-claude-md.md`.

**Content brief:**

1. **What is CLAUDE.md** — A markdown file that Claude Code reads at the start of every conversation. It's your project's instruction manual for AI. Like a `.editorconfig` but for AI behavior.

2. **Three Levels of CLAUDE.md**
   - **Global** (`~/.claude/CLAUDE.md`): Your personal preferences across all projects. "I prefer TypeScript", "Always use conventional commits", "I'm a senior backend engineer."
   - **Project** (`CLAUDE.md` in repo root): Project-specific rules. Commit this to git — your whole team benefits. "This project uses Next.js App Router", "Run `pnpm test` before committing", "API routes are in `src/app/api/`."
   - **Local** (`.claude/CLAUDE.md`): Your personal project overrides. Gitignored.

3. **What to Put in CLAUDE.md** — Practical examples:
   - Project architecture overview
   - Tech stack and key libraries
   - File/folder conventions
   - Testing commands and patterns
   - Coding style rules not covered by linters
   - Common gotchas and pitfalls
   - Who you are and your expertise level
   - Preferred language (natural language, not programming)

4. **Real-World CLAUDE.md Examples** — Show 3 examples:
   - Simple (personal project, 10 lines)
   - Medium (team project, 30 lines)
   - Comprehensive (enterprise, 60+ lines with sections)

5. **The `/init` Command** — Auto-generates a CLAUDE.md by scanning your project:
   ```
   claude /init
   ```
   It analyzes your package.json, folder structure, git history, and creates a starter CLAUDE.md. Always review and customize the output.

6. **Pro Tips**
   - Keep it concise — Claude reads the whole thing every conversation
   - Update it as the project evolves
   - Include "don't" rules: "Don't use class components", "Don't import from barrel files"
   - Use markdown headers for organization
   - Reference file paths: "Auth middleware is in `src/middleware/auth.ts`"

> **Tip:** CLAUDE.md is the single most impactful thing you can do to improve Claude Code's output. A good CLAUDE.md turns generic responses into project-aware, convention-following code.

### Chapter 6: Every Slash Command Explained

- [ ] **Step 2: Write Chapter 6 content**

Create `products/claude-code-ebook/src/06-slash-commands.md`.

**Content brief — comprehensive reference of all slash commands:**

1. **Essential Commands**
   - `/help` — Show help and available commands
   - `/clear` — Clear conversation history, start fresh
   - `/compact` — Compress conversation context (keep key info, reduce tokens). Use when Claude starts forgetting earlier context.
   - `/cost` — Show token usage and cost for current session
   - `/init` — Generate CLAUDE.md from project analysis

2. **Mode Commands**
   - `/fast` — Toggle fast mode (same model, faster output, less thorough). Great for quick edits.
   - `/model` — Switch models mid-conversation

3. **Development Commands**
   - `/commit` — Guided git commit with smart message generation
   - `/review-pr` — Review a pull request

4. **Navigation**
   - `!command` — Run a shell command inline (output enters conversation context)
   - `@filename` — Reference a specific file in your prompt

5. **Advanced Commands**
   - Plan mode — For multi-step tasks, creates structured plans
   - `/status` — Check running background processes

6. **Keyboard Shortcuts Table**

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Shift+Enter` | New line |
| `Shift+Tab` | Cycle model (Opus → Sonnet → Haiku) |
| `Esc` | Cancel current generation |
| `Ctrl+C` | Exit Claude Code |
| `Up arrow` | Edit last message |
| `\` at end of line | Continue on next line |

7. **Custom Keybindings** — Brief intro (detailed in Chapter 14):
   ```json
   // ~/.claude/keybindings.json
   [
     { "key": "ctrl+s", "command": "commit" },
     { "key": "ctrl+t", "command": "run_tests" }
   ]
   ```

### Chapter 7: Git Workflow Automation

- [ ] **Step 3: Write Chapter 7 content**

Create `products/claude-code-ebook/src/07-git-workflow.md`.

**Content brief:**

1. **Smart Commits** — "commit this" or `/commit`:
   - Claude analyzes staged + unstaged changes
   - Reads recent commit messages to match style
   - Generates a concise commit message (1-2 sentences)
   - Stages relevant files (avoids .env, credentials)
   - Never amends unless explicitly asked

2. **Pull Request Creation** — "create a PR":
   - Analyzes ALL commits since branch diverged (not just latest)
   - Generates title (under 70 chars) + description
   - Uses `gh pr create` with proper formatting
   - Includes summary bullets + test plan

3. **Branch Management**
   - "create a branch for this feature"
   - "switch to the feature/auth branch"
   - Claude never force-pushes or deletes branches without asking

4. **Conflict Resolution** — "there are merge conflicts, help me resolve them":
   - Claude reads conflict markers
   - Understands both sides
   - Suggests resolution
   - Prefers resolving over discarding changes

5. **Git Safety Protocols** — Built-in protections:
   - Never `git push --force` to main/master
   - Never `git reset --hard` without confirmation
   - Never skips hooks (`--no-verify`) unless asked
   - Always creates NEW commits (never amends existing unless asked)
   - Warns before committing sensitive files

6. **Advanced Git Workflows**
   - Cherry-picking: "cherry-pick commit abc123 to this branch"
   - Rebasing: "rebase this branch onto main" (non-interactive)
   - Bisecting: "help me find which commit introduced this bug"
   - Stashing: "stash my changes, pull, then pop"

> **Tip:** Claude Code uses HEREDOC format for commit messages to preserve formatting. This is especially useful for multi-line messages with bullet points.

### Chapter 8: Smart Code Navigation & Editing

- [ ] **Step 4: Write Chapter 8 content**

Create `products/claude-code-ebook/src/08-code-navigation.md`.

**Content brief:**

1. **The Tool Arsenal** — Claude Code has dedicated tools that are faster and more reliable than shell commands:

| Instead of... | Claude uses... | Why it's better |
|---------------|----------------|-----------------|
| `find . -name "*.ts"` | **Glob** | Faster, sorted by modification time |
| `grep -r "pattern"` | **Grep** | Proper permissions, regex, output modes |
| `cat file.py` | **Read** | Line numbers, offset/limit, image/PDF support |
| `sed -i 's/old/new/'` | **Edit** | Exact string match, safer, undoable |
| `echo > file` | **Write** | Creates new files cleanly |

2. **Glob — File Pattern Matching**
   ```
   "Find all TypeScript files in src"
   → Glob: **/*.ts in src/
   
   "Find all test files"
   → Glob: **/*.test.{ts,tsx,js,jsx}
   
   "Find all files modified recently"
   → Glob: results sorted by modification time
   ```

3. **Grep — Content Search**
   - Output modes: `files_with_matches`, `content`, `count`
   - Full regex: `"function\\s+\\w+"`, `"TODO|FIXME|HACK"`
   - File filtering: `glob: "*.ts"`, `type: "py"`
   - Context lines: `-A 5` (after), `-B 3` (before), `-C 2` (both)
   - Multiline mode: patterns that span multiple lines

4. **Read — Intelligent File Reading**
   - Line numbers in output (for precise editing)
   - Offset + limit for large files: "read lines 100-150 of server.ts"
   - Reads images (PNG, JPG) — Claude sees them visually
   - Reads PDFs (with page ranges for large files)
   - Reads Jupyter notebooks (all cells + outputs)

5. **Edit — Surgical Precision**
   - Exact string matching (not regex, not line numbers)
   - Must read file first before editing
   - `old_string` must be unique in the file
   - `replace_all: true` for renaming across the file
   - Preserves indentation exactly

6. **Multi-File Operations** — "Rename the `userId` field to `user_id` across all models":
   - Claude searches with Grep
   - Reads each file
   - Edits each occurrence
   - Verifies nothing broke

7. **Navigation Patterns for Large Codebases**
   - Start broad: "What's the project structure?" (ls, glob)
   - Narrow down: "Find where authentication is handled" (grep)
   - Deep dive: "Read the auth middleware" (read specific file)
   - Edit: "Add rate limiting to the auth middleware" (edit)

> **Tip:** When working with large files (1000+ lines), always use offset/limit with Read. Reading the whole file wastes context. "Read lines 200-250 of server.ts" is much more efficient.

- [ ] **Step 5: Build HTML to verify Part 2**

```bash
cd products/claude-code-ebook && ./build.sh html
open mastering-claude-code.html
# Verify: TOC shows chapters 5-8, tables render, code blocks styled
```

- [ ] **Step 6: Commit Part 2**

```bash
git add products/claude-code-ebook/src/05-*.md products/claude-code-ebook/src/06-*.md products/claude-code-ebook/src/07-*.md products/claude-code-ebook/src/08-*.md
git commit -m "feat(claude-code-ebook): Part 2 — Productive Development (Ch 5-8)"
```

---

## Task 4: Part 3 — Advanced Techniques (Chapters 9-12)

**Files:**
- Create: `products/claude-code-ebook/src/09-memory-system.md`
- Create: `products/claude-code-ebook/src/10-hooks.md`
- Create: `products/claude-code-ebook/src/11-mcp-servers.md`
- Create: `products/claude-code-ebook/src/12-ide-integration.md`

### Chapter 9: The Memory System

- [ ] **Step 1: Write Chapter 9 content**

Create `products/claude-code-ebook/src/09-memory-system.md`.

**Content brief:**

1. **The Problem Memory Solves** — Conversations are ephemeral. You tell Claude Code about your preferences, project context, feedback — and it forgets everything next session. Memory makes knowledge persistent.

2. **How It Works**
   - Memory lives in `.claude/projects/<project-hash>/memory/`
   - `MEMORY.md` is an index file (loaded every conversation)
   - Individual memory files contain detailed information
   - Claude automatically saves relevant information (auto-memory)
   - You can explicitly ask: "remember that we use Prisma, not Drizzle"

3. **Memory Types** — 5 types, each for different purposes:

| Type | Purpose | Example |
|------|---------|---------|
| `user` | Who you are, your expertise | "Senior backend dev, prefers Go" |
| `feedback` | How to approach work | "Don't mock the database in tests" |
| `project` | Ongoing work context | "Merge freeze starts April 15" |
| `reference` | Where external info lives | "Bugs tracked in Linear project CORE" |

4. **Memory File Format**
   ```markdown
   ---
   name: testing-preferences
   description: How to write tests in this project
   type: feedback
   ---
   
   Always use integration tests with real database, not mocks.
   
   **Why:** Mocked tests passed but prod migration failed last quarter.
   **How to apply:** When writing tests for database operations,
   use the test database container.
   ```

5. **MEMORY.md Index** — Keeps the index concise (under 200 lines):
   ```markdown
   # Project Memory
   
   - [Testing preferences](feedback_testing.md) — Integration tests only, no mocks
   - [User profile](user_role.md) — Senior backend dev, Go/Python
   - [Current sprint](project_sprint.md) — Auth rewrite, deadline April 20
   ```

6. **What NOT to Save** — Memory is not for:
   - Code patterns (read the code instead)
   - Git history (use `git log`)
   - Debugging solutions (the fix is in the code)
   - Things already in CLAUDE.md
   - Ephemeral task state

7. **Pro Tips**
   - "Remember this" — explicitly ask Claude to save something
   - "Forget that" — ask Claude to remove a memory
   - Memory files can become stale — Claude verifies before acting on old memories
   - Keep MEMORY.md under 200 lines (truncated after that)
   - Organize semantically, not chronologically

> **Tip:** The combination of CLAUDE.md (static project rules) + Memory (dynamic learned context) is what makes Claude Code feel like it truly "knows" your project over time.

### Chapter 10: Hooks — Automate Everything

- [ ] **Step 2: Write Chapter 10 content**

Create `products/claude-code-ebook/src/10-hooks.md`.

**Content brief:**

1. **What Are Hooks** — Shell commands that execute automatically when specific events happen in Claude Code. Think of them as git hooks but for AI actions.

2. **Hook Types**

| Hook | When it fires | Use case |
|------|--------------|----------|
| `PreToolCall` | Before a tool executes | Block dangerous commands, add logging |
| `PostToolCall` | After a tool completes | Auto-format edited files, run linter |
| `Notification` | When Claude sends a notification | Send to Slack, play sound |
| `PreCompact` | Before context compression | Save important context |
| `Stop` | When Claude finishes a turn | Auto-run tests after changes |

3. **Configuration** — Hooks go in `settings.json`:
   ```json
   {
     "hooks": {
       "PostToolCall": [
         {
           "matcher": "Edit",
           "command": "prettier --write $CLAUDE_FILE_PATH"
         }
       ],
       "PreToolCall": [
         {
           "matcher": "Bash",
           "command": "echo 'Running: $CLAUDE_TOOL_INPUT' >> /tmp/claude-audit.log"
         }
       ],
       "Stop": [
         {
           "command": "npm test 2>&1 | tail -5"
         }
       ]
     }
   }
   ```

4. **Practical Hook Recipes**
   - **Auto-format on edit**: Run prettier/black/gofmt after every file edit
   - **Auto-lint**: Run ESLint/pylint after edits, feed errors back
   - **Audit log**: Log every command Claude runs
   - **Test runner**: Run tests after Claude stops editing
   - **Notification**: Send Slack message when a long task completes
   - **Safety gate**: Block `rm -rf`, `DROP TABLE`, force-push commands

5. **Hook Environment Variables**
   - `$CLAUDE_TOOL_NAME` — which tool was called
   - `$CLAUDE_FILE_PATH` — file being edited (for Edit/Write)
   - `$CLAUDE_TOOL_INPUT` — full tool input as JSON

6. **Hook Feedback** — Hook output is fed back to Claude. If a hook returns an error, Claude sees it and can react. This creates a feedback loop:
   - Claude edits file → hook runs linter → linter finds error → Claude sees error → Claude fixes it

> **Tip:** Start with one hook (auto-format on edit) and build up. A PostToolCall hook for prettier/black is the single highest-value hook you can add.

### Chapter 11: MCP Servers — Extend Claude Code Infinitely

- [ ] **Step 3: Write Chapter 11 content**

Create `products/claude-code-ebook/src/11-mcp-servers.md`.

**Content brief:**

1. **What Is MCP** — Model Context Protocol. An open standard that lets AI assistants connect to external tools and data sources. Think of it as USB ports for AI — plug in any capability.

2. **Why MCP Matters** — Without MCP, Claude Code can only use its built-in tools. With MCP, it can:
   - Query your database directly
   - Read/write to Notion, Linear, Jira
   - Access your Slack messages
   - Control your browser (Puppeteer)
   - Interact with any API

3. **How to Configure MCP Servers** — In `.claude/settings.json` or `~/.claude/settings.json`:
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
           "GITHUB_TOKEN": "ghp_..."
         }
       },
       "filesystem": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
       }
     }
   }
   ```

4. **Popular MCP Servers** — Table of most useful servers:

| Server | Purpose | Install |
|--------|---------|---------|
| `server-postgres` | Query PostgreSQL | `@modelcontextprotocol/server-postgres` |
| `server-github` | GitHub issues, PRs | `@modelcontextprotocol/server-github` |
| `server-slack` | Read/send Slack messages | `@modelcontextprotocol/server-slack` |
| `server-filesystem` | Sandboxed file access | `@modelcontextprotocol/server-filesystem` |
| `server-puppeteer` | Browser automation | `@modelcontextprotocol/server-puppeteer` |
| `server-sqlite` | Query SQLite databases | `@modelcontextprotocol/server-sqlite` |
| `server-memory` | Persistent knowledge graph | `@modelcontextprotocol/server-memory` |
| Vercel MCP | Vercel deployments/logs | `@vercel/mcp` |

5. **Building Your Own MCP Server** — Brief overview:
   - MCP servers are simple programs that expose tools via JSON-RPC
   - Can be written in TypeScript, Python, or any language
   - Use `@modelcontextprotocol/sdk` for TypeScript
   - Use `mcp` package for Python

6. **Security Considerations**
   - MCP servers can access sensitive data — review what you connect
   - Use environment variables for credentials, never hardcode
   - Project-level MCP configs are committed — be careful with secrets
   - Use `settings.local.json` for personal MCP configs with secrets

### Chapter 12: IDE Integration

- [ ] **Step 4: Write Chapter 12 content**

Create `products/claude-code-ebook/src/12-ide-integration.md`.

**Content brief:**

1. **Available Platforms**

| Platform | Best for | Key advantage |
|----------|----------|---------------|
| CLI (terminal) | Power users, servers | Full feature set, fastest |
| Desktop app | Mac/Windows daily use | Native experience, system tray |
| VS Code extension | IDE-first developers | Inline code actions, sidebar |
| JetBrains plugin | IntelliJ/WebStorm users | IDE integration |
| Web app (claude.ai/code) | Quick access | No install needed |

2. **VS Code Integration**
   - Install from VS Code marketplace
   - Sidebar panel for conversation
   - Inline code actions (right-click → "Ask Claude")
   - Terminal integration
   - File context automatically included

3. **JetBrains Integration**
   - Install from JetBrains marketplace
   - Tool window for conversation
   - Code selection context
   - Terminal integration

4. **Desktop App**
   - System tray for quick access
   - Multiple project windows
   - Native notifications
   - Keyboard shortcuts

5. **CLI-First Workflow** — Why many experts prefer the terminal:
   - Fastest startup
   - Works over SSH
   - Full feature access (some features CLI-only)
   - Scriptable with pipes: `echo "explain this" | claude -p`
   - Composable: `claude -p "review this diff" < <(git diff)`

6. **Multi-Environment Setup** — Using Claude Code across machines:
   - Global CLAUDE.md syncs your preferences
   - Project CLAUDE.md travels with the repo
   - Memory is per-machine (not synced)
   - Settings can be committed to git

> **Tip:** Even if you use an IDE integration daily, learn the CLI. It's the most powerful interface and has features that IDE extensions don't expose.

- [ ] **Step 5: Build HTML to verify Part 3**

```bash
cd products/claude-code-ebook && ./build.sh html
open mastering-claude-code.html
```

- [ ] **Step 6: Commit Part 3**

```bash
git add products/claude-code-ebook/src/09-*.md products/claude-code-ebook/src/10-*.md products/claude-code-ebook/src/11-*.md products/claude-code-ebook/src/12-*.md
git commit -m "feat(claude-code-ebook): Part 3 — Advanced Techniques (Ch 9-12)"
```

---

## Task 5: Part 4 — Expert Secrets (Chapters 13-15)

**Files:**
- Create: `products/claude-code-ebook/src/13-prompt-engineering.md`
- Create: `products/claude-code-ebook/src/14-parallel-development.md`
- Create: `products/claude-code-ebook/src/15-custom-skills.md`

### Chapter 13: Prompt Engineering for Claude Code

- [ ] **Step 1: Write Chapter 13 content**

Create `products/claude-code-ebook/src/13-prompt-engineering.md`.

**Content brief — this is one of the highest-value chapters:**

1. **How Claude Code Prompts Differ** — You're not writing chat prompts. Claude Code has tools, context, and state. Your prompts should leverage this:
   - Bad: "Write a function that validates emails"
   - Good: "Add email validation to the signup handler in `src/auth/signup.ts`. Use the same validation pattern as `src/auth/utils.ts`."

2. **The 5 Principles of Expert Prompting**

   **Principle 1: Be Specific About Location**
   - "Fix the bug in the login function" → which file? which function?
   - "Fix the null check in `src/auth/login.ts:45` where `user.email` can be undefined"

   **Principle 2: Reference Existing Patterns**
   - "Add a new API route — follow the same pattern as `src/api/users.ts`"
   - Claude reads the referenced file and replicates the pattern

   **Principle 3: State the Why, Not Just the What**
   - "Add caching to the user query" (Claude guesses the cache strategy)
   - "Add caching to the user query — we're hitting the DB 50 times/second for the same user profiles. Use a 5-minute TTL." (Claude makes informed decisions)

   **Principle 4: Scope Your Request**
   - Too broad: "Refactor the authentication system"
   - Right size: "Extract the JWT validation logic from the auth middleware into its own function so we can reuse it in the WebSocket handler"

   **Principle 5: Give Success Criteria**
   - "Add tests" (vague)
   - "Add tests for the payment flow — cover: successful charge, declined card, invalid amount, duplicate charge. Run `npm test` to verify they pass."

3. **Anti-Patterns to Avoid**
   - Don't start with "Can you..." — just state what you need
   - Don't explain how Claude Code works to Claude Code
   - Don't paste error messages without context — include what you were trying to do
   - Don't ask Claude to "be careful" or "double-check" — it always tries to be accurate

4. **Power Prompts** — Template patterns:
   - Bug fix: "Fix [symptom] in [file:line]. The expected behavior is [X] but it does [Y]. Reproduce with [command]."
   - Feature: "Add [feature] to [location]. Follow the pattern in [reference file]. Include tests."
   - Refactor: "Extract [what] from [where] into [new location] because [why]."
   - Debug: "I'm getting [error] when [action]. I've already checked [things I tried]. What's the root cause?"

5. **Conversation Management**
   - Use `/compact` when context gets long
   - Start new conversations for new topics (don't let one conversation handle everything)
   - Use `@filename` to explicitly bring files into context
   - Use `!git diff` to show Claude what changed since last time

### Chapter 14: Parallel Development with Subagents & Worktrees

- [ ] **Step 2: Write Chapter 14 content**

Create `products/claude-code-ebook/src/14-parallel-development.md`.

**Content brief:**

1. **The Problem** — Some tasks have independent parts. Writing tests for module A and module B can happen simultaneously. Why do them sequentially?

2. **Agent Tool — Spawning Subagents**
   - Claude can launch specialized sub-agents that work independently
   - Each agent gets its own context (doesn't pollute your main conversation)
   - Agents can run in foreground (wait for result) or background (continue working)

3. **Agent Types**

| Type | Purpose | Use case |
|------|---------|----------|
| `general-purpose` | Multi-step tasks | Research, code changes |
| `Explore` | Codebase exploration | "How does auth work?" |
| `Plan` | Architecture planning | Design implementation approach |
| `code-reviewer` | Code review | Review completed work |

4. **Background Agents**
   - Launch work in the background while you continue other tasks
   - Get notified when the agent completes
   - "Run tests in background while I keep coding"

5. **Git Worktrees — Isolated Environments**
   - A worktree is an isolated copy of your repo (separate directory, separate branch)
   - Agents can work in worktrees without affecting your main working directory
   - Perfect for parallel feature development
   - Changes can be merged back via git

6. **When to Use What**
   - Need a quick answer → Explore agent (foreground)
   - Need independent work done → general-purpose agent (background)
   - Need to work on a feature without affecting current state → worktree
   - Need to parallelize plan tasks → subagent-driven development

7. **Practical Example** — Implementing a plan with subagents:
   ```
   "I have a plan with 5 independent tasks. Execute tasks 1, 2, and 3 
   in parallel using subagents, each in its own worktree."
   ```

> **Tip:** Subagents are most valuable when tasks are truly independent. If task B depends on task A's output, run them sequentially.

### Chapter 15: Custom Skills & Superpowers

- [ ] **Step 3: Write Chapter 15 content**

Create `products/claude-code-ebook/src/15-custom-skills.md`.

**Content brief:**

1. **What Are Skills** — Reusable prompt templates that encapsulate expert workflows. Think of them as "recipes" that Claude Code follows for specific types of tasks. Invoked with the Skill tool or `/skill-name`.

2. **Built-in Skills** — Examples that ship with superpowers:
   - `brainstorming` — Structured creative exploration before implementation
   - `writing-plans` — Creating detailed implementation plans
   - `executing-plans` — Following plans step by step
   - `test-driven-development` — Red-green-refactor workflow
   - `systematic-debugging` — Methodical bug investigation
   - `verification-before-completion` — Verify before claiming done
   - `code-reviewer` — Structured code review

3. **How Skills Work**
   - Skills are markdown files with frontmatter (name, description, trigger conditions)
   - When invoked, the skill's content is loaded as instructions
   - Claude follows the skill's workflow exactly
   - Skills can reference other skills (chaining)

4. **Creating Your Own Skills**
   - Skills live in `~/.claude/skills/` or plugin directories
   - Each skill is a directory with a markdown file
   - The markdown describes when to trigger and what to do

5. **Skill Anatomy**
   ```markdown
   ---
   name: my-custom-skill
   description: Use when doing X to ensure Y
   ---
   
   ## Steps
   1. First, do this
   2. Then, check that
   3. Finally, verify this
   
   ## Rules
   - Always do X before Y
   - Never skip step 2
   ```

6. **When Skills Shine**
   - Repeatable workflows (deploy, review, test)
   - Enforcing team standards
   - Complex multi-step processes
   - Onboarding new developers

> **Tip:** Start by using built-in skills for a month before creating your own. You'll understand the patterns and create better custom skills.

- [ ] **Step 4: Build HTML to verify Part 4 (so far)**

```bash
cd products/claude-code-ebook && ./build.sh html
open mastering-claude-code.html
```

- [ ] **Step 5: Commit Chapters 13-15**

```bash
git add products/claude-code-ebook/src/13-*.md products/claude-code-ebook/src/14-*.md products/claude-code-ebook/src/15-*.md
git commit -m "feat(claude-code-ebook): Part 4 chapters 13-15 (prompts, parallel, skills)"
```

---

## Task 6: The Crown Jewel — 50 Hidden Tips (Chapter 16)

**Files:**
- Create: `products/claude-code-ebook/src/16-hidden-tips.md`

This is the chapter that sells the book. Every tip must be genuinely useful and non-obvious.

- [ ] **Step 1: Write Chapter 16 content**

Create `products/claude-code-ebook/src/16-hidden-tips.md`.

**Content brief — write each tip with: what it is, how to use it (with code/command), and why it's valuable. Group into categories:**

**Category: Speed & Efficiency (Tips 1-10)**

1. **`!` prefix runs shell commands inline** — Type `! git log --oneline -5` to run a command and add its output to the conversation. No need to leave Claude Code.

2. **`/fast` is the same model, not a downgrade** — Many people think fast mode switches to a weaker model. It doesn't — same Claude Opus, just optimized for faster output with slightly less thoroughness.

3. **`Shift+Tab` cycles models instantly** — Switch between Opus (complex), Sonnet (balanced), and Haiku (quick) mid-conversation without restarting.

4. **`/compact` saves your session** — When Claude starts "forgetting" earlier context, `/compact` compresses the conversation while keeping key information. Use it proactively before hitting context limits.

5. **Pipe mode for one-shot queries** — `echo "explain this error" | claude -p` — no interactive session needed. Perfect for scripts and automation.

6. **`claude -p` with stdin** — `git diff | claude -p "review this diff for bugs"` — pipe anything directly to Claude for analysis.

7. **Resume previous conversations** — `claude --resume` picks up where you left off. Your conversation history is preserved.

8. **`@filename` forces file reading** — Mentioning `@src/auth.ts` in your prompt explicitly loads that file into context, even if Claude didn't plan to read it.

9. **Edit is 10x cheaper than Write** — Edit sends only the diff. Write sends the entire file. For modifying existing files, always prefer Edit. This directly impacts your token cost.

10. **Multiple tool calls in parallel** — Claude can call multiple tools simultaneously (e.g., reading 5 files at once). You don't need to tell it to — it does this automatically when calls are independent.

**Category: Configuration Secrets (Tips 11-20)**

11. **Three layers of settings** — `~/.claude/settings.json` (global) → `.claude/settings.json` (project, committed) → `.claude/settings.local.json` (personal, gitignored). They merge in this order.

12. **Allowlist specific commands** — `"Bash(npm test)"` in permissions.allow auto-approves that exact command. Use `"Bash(npm *)"` for all npm commands.

13. **`.claudeignore` hides files from Claude** — Like `.gitignore` but for Claude Code. Use it to hide generated files, build artifacts, or sensitive directories that Claude shouldn't read.

14. **Custom keybindings** — Create `~/.claude/keybindings.json` to remap any shortcut. Supports chord bindings (e.g., `Ctrl+K Ctrl+C` for commit).

15. **Notification hooks to Slack** — Set up a PostToolCall hook to send a Slack webhook when long tasks complete. Never stare at a terminal waiting again.

16. **Auto-format on every edit** — One PostToolCall hook for prettier/black and every file Claude edits is auto-formatted:
    ```json
    {"hooks": {"PostToolCall": [{"matcher": "Edit", "command": "prettier --write $CLAUDE_FILE_PATH"}]}}
    ```

17. **Project-scoped MCP servers** — MCP configs in `.claude/settings.json` (project) vs `~/.claude/settings.json` (global). Team databases go in project config; personal tools go in global.

18. **Environment variables in settings** — MCP server configs support `env` blocks. Use this for database URLs, API keys — never hardcode them.

19. **`claude config set` from terminal** — Configure without editing JSON: `claude config set permissions.allow '["Read","Glob"]'`

20. **Multiple CLAUDE.md files are merged** — If you have `~/.claude/CLAUDE.md` AND `project/CLAUDE.md` AND `.claude/CLAUDE.md`, ALL are loaded and merged. Use this for layered instructions.

**Category: Advanced Workflows (Tips 21-30)**

21. **`/init` generates CLAUDE.md automatically** — Run in any project to generate a starter CLAUDE.md. It scans package.json, folder structure, and recent git history.

22. **Plan mode for complex tasks** — For multi-step tasks, Claude can create a structured plan before coding. This prevents going down the wrong path on complex features.

23. **Background agents for parallel work** — `run_in_background: true` launches a subagent that works while you continue. Get notified when it finishes.

24. **Worktree isolation** — Agents can work in git worktrees (isolated repo copies). Perfect for features that might break your current working state.

25. **Claude reads images** — Drag an image path or paste a screenshot path. Claude sees it visually and can describe, analyze, or replicate UI from it.

26. **Claude reads PDFs** — `Read` tool handles PDFs with page ranges. `"Read pages 5-10 of the spec"` — great for working from design docs.

27. **Jupyter notebook editing** — Claude can read `.ipynb` files (seeing all cells + outputs) and edit individual cells with NotebookEdit.

28. **Web search and fetch** — Claude can search the web and fetch URLs. "Search for the latest React 19 migration guide" or "Fetch the API docs at https://..."

29. **Task tracking built-in** — Claude can create and manage a task list during complex work. This helps track progress and prevents skipping steps.

30. **Heredoc commit messages** — Claude uses HEREDOC format for multi-line commit messages, preserving formatting perfectly.

**Category: Hidden Power (Tips 31-40)**

31. **Hook feedback loop** — Hook output is fed back to Claude. A linter hook that catches errors creates an auto-fix loop: edit → lint → error → Claude fixes → lint → clean.

32. **`--print` flag for non-interactive mode** — `claude --print "what version of node am I running?"` — one-shot, no interactive session. Great for shell scripts.

33. **Claude won't amend commits unless asked** — A safety feature many miss. Even when fixing a failed pre-commit hook, Claude creates a NEW commit instead of amending the previous one (which might destroy other changes).

34. **Conversation compression is automatic** — As you approach context limits, Claude automatically compresses earlier messages. You don't need to manage this manually (but `/compact` lets you do it proactively).

35. **Explore agent for codebase questions** — Instead of manually grepping, launch an Explore agent: "How does the payment flow work?" It does multi-step investigation and returns a summary.

36. **Code reviewer agent after features** — After implementing a feature, launch a code-reviewer agent to catch issues before you commit. It reviews against your plan and coding standards.

37. **Remote triggers for scheduled tasks** — Schedule Claude Code to run tasks automatically (like a cron job for AI). Run code reviews daily, generate reports weekly.

38. **Skills chain together** — The brainstorming skill leads into writing-plans, which leads into executing-plans. Each skill knows about the others and creates proper handoffs.

39. **`--model` overrides in subagents** — When dispatching subagents, you can specify which model they use. Use Haiku for simple searches, Opus for complex coding.

40. **Claude tracks git safety automatically** — It reads `git status` at conversation start, checks recent commits, and avoids destructive operations on shared branches.

**Category: Pro Patterns (Tips 41-50)**

41. **"Follow the pattern in X"** — The most powerful prompt pattern. Reference an existing file and Claude replicates its structure, naming, and style perfectly.

42. **Start conversations scoped** — Don't let one conversation handle everything. Start new ones for new topics. This keeps context fresh and relevant.

43. **"Read X before editing Y"** — If Claude makes an edit that doesn't match existing style, explicitly ask it to read the existing file first. It reads files before editing by default, but explicit instruction helps for complex cases.

44. **Denial recovery** — If you deny a tool call, Claude adjusts its approach. Don't deny silently — tell it WHY you denied so it makes better decisions.

45. **Token cost scales with file size** — Reading a 5000-line file costs real tokens. Use offset/limit to read only what you need. `"Read lines 100-150 of large-file.ts"` instead of the whole file.

46. **Multiple files in one prompt** — Mention multiple `@file` references in one prompt. Claude reads all of them and understands the relationships.

47. **Git diff as context** — `!git diff` or `!git diff HEAD~3` — show Claude what changed. Much more efficient than explaining changes verbally.

48. **The companion (Coppertop)** — A small dragon that occasionally comments in Claude Code's UI. It's a separate watcher, not Claude itself. Addressing it by name triggers its responses.

49. **Pre-commit hook integration** — Claude respects pre-commit hooks. If a hook fails, Claude sees the error and fixes the issue. Set up strict hooks — Claude handles them automatically.

50. **Build your own workflow** — Combine CLAUDE.md + Memory + Hooks + MCP + Skills into a custom development environment. Chapter 20 shows you how.

- [ ] **Step 2: Review the 50 tips — ensure each is accurate, non-obvious, and actionable**

Read through the chapter. Verify:
- No duplicate tips
- Each tip has a clear "how to use" (command or config)
- Tips are genuinely hidden/non-obvious (not "Claude can edit files")
- Code examples are syntactically correct

- [ ] **Step 3: Commit Chapter 16**

```bash
git add products/claude-code-ebook/src/16-*.md
git commit -m "feat(claude-code-ebook): Chapter 16 — 50 Hidden Tips & Tricks"
```

---

## Task 7: Part 5 — Real-World Mastery (Chapters 17-20)

**Files:**
- Create: `products/claude-code-ebook/src/17-building-feature.md`
- Create: `products/claude-code-ebook/src/18-debugging-pro.md`
- Create: `products/claude-code-ebook/src/19-cost-optimization.md`
- Create: `products/claude-code-ebook/src/20-custom-setup.md`

### Chapter 17: Building a Feature Start-to-Finish (Case Study)

- [ ] **Step 1: Write Chapter 17 content**

Create `products/claude-code-ebook/src/17-building-feature.md`.

**Content brief — complete walkthrough of building a real feature with Claude Code:**

1. **The Feature** — "Add a user notification preferences API to a Next.js app." Realistic, multi-file, involves testing.

2. **Phase 1: Planning**
   - Open Claude Code in project directory
   - "I need to add notification preferences — users should be able to toggle email, push, and SMS notifications per category (marketing, product updates, security). Plan the approach."
   - Claude analyzes existing code, suggests file locations, data model, API routes
   - Review and adjust the plan

3. **Phase 2: TDD — Write Tests First**
   - "Write the tests for the notification preferences API following our existing test patterns in `tests/api/`"
   - Claude reads existing tests, creates new test file
   - Run tests — all fail (expected)

4. **Phase 3: Implementation**
   - "Implement the notification preferences — start with the database model"
   - Claude creates Prisma schema, generates migration
   - "Now implement the API routes"
   - Claude creates GET/PUT endpoints
   - Run tests — some pass

5. **Phase 4: Iterate**
   - Fix failing tests, handle edge cases
   - "Add validation — preferences should reject invalid categories"
   - Claude adds Zod validation, updates tests

6. **Phase 5: Polish & Commit**
   - Run full test suite
   - "Commit with a descriptive message"
   - "Create a PR targeting main"

7. **Lessons from the Walkthrough**
   - Claude followed existing patterns because we referenced them
   - TDD caught edge cases early
   - Multiple small prompts > one massive prompt
   - Plan → Test → Implement → Iterate → Commit

### Chapter 18: Debugging Like a Pro

- [ ] **Step 2: Write Chapter 18 content**

Create `products/claude-code-ebook/src/18-debugging-pro.md`.

**Content brief:**

1. **The Expert Debugging Workflow**
   - Don't immediately guess. Gather evidence first.
   - "I'm getting [error] when [action]. Help me debug this."
   - Let Claude investigate systematically

2. **Step 1: Reproduce** — Give Claude the exact error message, stack trace, and steps to reproduce. `! npm test 2>&1 | tail -20` — pipe the error right in.

3. **Step 2: Investigate** — Claude reads relevant files, traces the call stack, searches for related patterns. Let it explore before jumping to fixes.

4. **Step 3: Hypothesize** — Claude proposes root cause. Verify with: "What evidence supports this hypothesis? What would disprove it?"

5. **Step 4: Fix Minimally** — Expert fix = smallest change that addresses root cause. Not a rewrite. Not "improvements while we're here."

6. **Step 5: Verify** — Run the failing test/scenario. Run the full test suite to catch regressions.

7. **Common Debugging Patterns**
   - **"Why isn't this working?"** → Share the error output inline with `!`
   - **"This test passes locally but fails in CI"** → Check environment differences, race conditions
   - **"Something changed but I don't know what"** → `!git diff HEAD~5` or `!git log --oneline -10`
   - **"This error message is confusing"** → Claude reads the source of the error, not just the message
   - **Performance issue** → Ask Claude to read the slow code, profile output, suggest specific optimizations

8. **Debugging Anti-Patterns**
   - Don't say "fix it" without sharing the error
   - Don't guess at the problem — let Claude investigate
   - Don't accept the first suggestion — ask for evidence
   - Don't ask Claude to add try-catch everywhere (that hides bugs, doesn't fix them)

### Chapter 19: Cost Optimization & Efficiency

- [ ] **Step 3: Write Chapter 19 content**

Create `products/claude-code-ebook/src/19-cost-optimization.md`.

**Content brief:**

1. **Understanding Token Costs**
   - Input tokens: everything Claude reads (files, conversation history, tool results)
   - Output tokens: everything Claude writes (responses, tool calls)
   - Input is cheaper than output
   - `/cost` shows current session usage

2. **The 80/20 of Cost Reduction**
   - **Read less, read smarter**: Use offset/limit. Don't read entire 5000-line files when you need 50 lines.
   - **Edit, don't Write**: Edit sends a diff. Write sends the whole file.
   - **Use /compact proactively**: Don't wait for auto-compression. Compact when you're done with a topic.
   - **Start fresh conversations**: A long conversation with 50 exchanges carries all that history. Start new for new topics.
   - **Use the right model**: Haiku for quick questions ($), Sonnet for most coding ($$), Opus for complex architecture ($$$).

3. **Model Selection Strategy**

| Task | Recommended Model | Why |
|------|------------------|-----|
| "What does this function do?" | Haiku | Simple comprehension |
| "Add a new API endpoint" | Sonnet | Standard coding task |
| "Refactor the auth system" | Opus | Complex multi-file reasoning |
| "Fix a typo" | Haiku | Trivial change |
| "Debug a race condition" | Opus | Requires deep reasoning |
| "Write tests for X" | Sonnet | Pattern-following task |

4. **Prompt Efficiency**
   - Specific prompts → fewer back-and-forth → fewer tokens
   - "Fix the bug in `src/auth.ts:45`" costs less than "there's a bug somewhere in auth"
   - Include file paths, line numbers, expected behavior
   - One clear task per prompt (don't bundle unrelated tasks)

5. **Subscription vs API Key**
   - Claude Pro ($20/mo): Limited messages per day, unlimited conversations
   - Claude Max ($100-200/mo): Higher message limits
   - API key: Pay per token, no limits, more predictable for heavy usage
   - Rule of thumb: If you're spending >$100/mo on API, consider Max subscription

6. **Hidden Cost Traps**
   - Large files in context (package-lock.json, minified files)
   - Long conversations without compaction
   - Re-reading the same files repeatedly (Claude usually caches, but starting new conversations resets)
   - Using Write instead of Edit for small changes

### Chapter 20: Your Custom Setup Blueprint

- [ ] **Step 4: Write Chapter 20 content**

Create `products/claude-code-ebook/src/20-custom-setup.md`.

**Content brief — tie everything together:**

1. **The Complete Setup Checklist**
   ```
   □ Global CLAUDE.md with your preferences
   □ Project CLAUDE.md with project rules
   □ Permission allowlists for common commands
   □ At least one PostToolCall hook (formatter)
   □ MCP server for your database (if applicable)
   □ Custom keybindings for your workflow
   □ .claudeignore for generated/build files
   ```

2. **Starter Global CLAUDE.md** — Template:
   ```markdown
   # My Preferences
   - I'm a [role] working primarily with [tech stack]
   - I prefer [coding style preferences]
   - Always use [testing framework] for tests
   - Use conventional commits (feat:, fix:, docs:)
   - Respond in [language] when I write in [language]
   ```

3. **Starter Settings.json** — Template with common allowlists, hooks, MCP servers

4. **Recommended MCP Servers by Stack**
   - Web dev: GitHub, Postgres/SQLite, Puppeteer
   - Mobile: GitHub, Firebase
   - Data science: SQLite, filesystem, Jupyter
   - DevOps: GitHub, Docker, AWS

5. **Building Your Workflow Over Time**
   - Week 1: CLAUDE.md + basic permissions
   - Week 2: Add formatting hook
   - Week 3: Configure MCP servers
   - Week 4: Create custom keybindings
   - Month 2: Build your first custom skill
   - Month 3: Set up remote triggers for automation

6. **Before/After** — Show the difference between a raw Claude Code experience and a fully configured one:
   - Before: Generic responses, constant permission prompts, no context retention
   - After: Project-aware responses, smooth auto-formatting, persistent memory, one-keypress commits

7. **Keep Evolving** — Your setup should grow with you. Claude Code is updated frequently with new features. Follow the changelog and incorporate what helps.

End with: "You now have everything you need to use Claude Code at an expert level. The difference between a beginner and an expert isn't knowledge — it's setup and habits. Configure once, benefit forever."

- [ ] **Step 5: Build HTML to verify all 20 chapters**

```bash
cd products/claude-code-ebook && ./build.sh html
open mastering-claude-code.html
# Verify: all 20 chapters in TOC, proper formatting throughout
```

- [ ] **Step 6: Commit Part 5**

```bash
git add products/claude-code-ebook/src/17-*.md products/claude-code-ebook/src/18-*.md products/claude-code-ebook/src/19-*.md products/claude-code-ebook/src/20-*.md
git commit -m "feat(claude-code-ebook): Part 5 — Real-World Mastery (Ch 17-20)"
```

---

## Task 8: Cover Page + Final Assembly

**Files:**
- Create: `products/claude-code-ebook/cover.html`
- Create: `products/claude-code-ebook/README.md`

- [ ] **Step 1: Create the cover page HTML**

Create `products/claude-code-ebook/cover.html` — a 1280×1600 HTML cover (Gumroad product image):

**Design spec:**
- Dark background (#0f0f11) with subtle amber gradient
- Title: "Mastering Claude Code" in large serif font (Playfair Display)
- Subtitle: "From Zero to Expert" in smaller sans-serif (Inter)
- Tagline: "Including 50 Hidden Features Most Developers Don't Know"
- Terminal icon or `>_` symbol as visual element
- Author: "A Practical Guide for Developers"
- Color accent: amber/orange (#D97706) matching the ebook theme
- Similar visual style to the 1000-expert-prompts cover

- [ ] **Step 2: Screenshot cover to PNG**

```bash
cd products/claude-code-ebook
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu \
  --window-size=1280,1600 \
  --screenshot=cover.png \
  "file://$(pwd)/cover.html"
```

- [ ] **Step 3: Write README.md with build instructions**

Create `products/claude-code-ebook/README.md`:

```markdown
# Mastering Claude Code — Gumroad Product

**Price:** $19 launch → $29 after social proof
**Category:** Digital download / ebook
**Status:** Ready to build

## Product Details

- 20 chapters across 5 parts (Beginner → Expert)
- 50 hidden tips and tricks
- Real-world case studies
- Complete code examples
- ~120+ pages PDF

## Build Commands

```bash
cd products/claude-code-ebook

# Build everything (MD → HTML → PDF → ZIP)
./build.sh all

# Or build incrementally:
./build.sh md     # Concatenate chapters
./build.sh html   # Build styled HTML
./build.sh pdf    # Generate PDF
./build.sh zip    # Create Gumroad ZIP

# Screenshot cover
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu \
  --window-size=1280,1600 \
  --screenshot=cover.png \
  "file://$(pwd)/cover.html"
```

## Gumroad Upload Bundle

The ZIP contains:
- `mastering-claude-code.pdf` — The main ebook
- `mastering-claude-code.md` — Plain markdown version
- `src/` — Individual chapter files

## Pre-Launch Checklist

- [ ] Build PDF and verify rendering
- [ ] Generate cover image
- [ ] Create ZIP bundle
- [ ] Upload to Gumroad (zerix1.gumroad.com)
- [ ] Set price to $19
- [ ] Paste description from gumroad-listing.md
- [ ] Add tags: claude code, ai coding, developer tools, ebook, tutorial
- [ ] Schedule launch tweet thread
- [ ] Cross-post on LinkedIn, Nostr, dev.to
- [ ] Add to CLAUDE.md Gumroad products list
```

- [ ] **Step 4: Commit cover + README**

```bash
git add products/claude-code-ebook/cover.html products/claude-code-ebook/README.md
git commit -m "feat(claude-code-ebook): cover page + README with build instructions"
```

---

## Task 9: PDF Build + Gumroad Listing + ZIP

**Files:**
- Create: `products/claude-code-ebook/gumroad-listing.md`

- [ ] **Step 1: Build the full PDF**

```bash
cd products/claude-code-ebook
./build.sh pdf
# Expected: mastering-claude-code.pdf exists, ~120+ pages
```

Open and verify:
- TOC renders correctly with clickable links
- Code blocks have dark background with syntax highlighting
- Tables are formatted properly
- Page breaks at each chapter
- No cut-off content or broken layouts

- [ ] **Step 2: Write the Gumroad listing**

Create `products/claude-code-ebook/gumroad-listing.md`:

**Include:**
- Product title: "Mastering Claude Code: From Zero to Expert"
- Short description (1 paragraph, punchy)
- Long description with:
  - Who this is for (3 bullet points)
  - What's inside (chapter highlights)
  - The "50 Hidden Tips" chapter highlight
  - What you'll learn (outcomes)
  - FAQ (format? updates? refund?)
- Tags: claude code, ai coding, developer tools, ai assistant, coding tutorial, ebook, claude, anthropic
- Price rationale
- Launch tweet thread (8 tweets for promotion)

- [ ] **Step 3: Build the Gumroad ZIP bundle**

```bash
cd products/claude-code-ebook
./build.sh zip
ls -la mastering-claude-code.zip
# Expected: ZIP with .pdf, .md, and src/
```

- [ ] **Step 4: Final commit**

```bash
git add products/claude-code-ebook/gumroad-listing.md
git commit -m "feat(claude-code-ebook): Gumroad listing + final PDF build"
```

- [ ] **Step 5: Update CLAUDE.md with new product**

Add to the Gumroad Products section in `CLAUDE.md`:
```
- Product 7: Mastering Claude Code ($19) — URL pending upload. Source: `products/claude-code-ebook/`. 20 chapters, 50 hidden tips, beginner-to-expert guide.
```

---

## Summary

| Task | Content | Chapters |
|------|---------|----------|
| 1 | Project setup + build pipeline | — |
| 2 | Part 1: Getting Started | Ch 1-4 |
| 3 | Part 2: Productive Development | Ch 5-8 |
| 4 | Part 3: Advanced Techniques | Ch 9-12 |
| 5 | Part 4: Expert Secrets (13-15) | Ch 13-15 |
| 6 | Chapter 16: 50 Hidden Tips | Ch 16 |
| 7 | Part 5: Real-World Mastery | Ch 17-20 |
| 8 | Cover page + README | — |
| 9 | PDF build + Gumroad listing + ZIP | — |

**Estimated output:** ~120-150 pages, 20 chapters, 50 hidden tips, professional PDF styling.
**Revenue target:** 20 sales/mo × $19 = $380/mo → $29 after social proof = $580/mo
