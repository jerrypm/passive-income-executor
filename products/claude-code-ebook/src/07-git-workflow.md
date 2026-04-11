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
