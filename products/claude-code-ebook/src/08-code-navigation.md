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
