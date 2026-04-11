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
