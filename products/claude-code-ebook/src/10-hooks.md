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
