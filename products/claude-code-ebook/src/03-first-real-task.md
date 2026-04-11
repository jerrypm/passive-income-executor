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
