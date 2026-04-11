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
