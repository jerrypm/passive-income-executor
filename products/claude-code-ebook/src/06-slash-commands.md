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
