## Chapter 11: MCP Servers — Extend Claude Code Infinitely

Out of the box, Claude Code can read files, write files, search code, and run shell commands. That's powerful for pure code work. But real-world development involves more than code — you interact with databases, issue trackers, deployment platforms, documentation wikis, messaging systems, and dozens of other tools.

MCP — the Model Context Protocol — lets Claude Code talk to all of them. It's an open standard that gives AI models a way to connect with external tools and data sources through a simple, unified interface. Think of MCP servers as USB ports for Claude Code: plug in a PostgreSQL server, and Claude can query your database. Plug in a GitHub server, and Claude can search issues and create pull requests. Plug in a Slack server, and Claude can read and send messages.

The result is a Claude Code that doesn't just work with your code — it works with your entire development environment.

### Why MCP Matters

Without MCP, when you need Claude Code to check something in your database, the workflow looks like this:

1. You switch to your database client
2. Run a query
3. Copy the results
4. Paste them into Claude Code
5. Claude analyzes and responds

With MCP, Claude Code queries the database directly:

```
What are the most common error types in the logs table from the last 24 hours?
```

Claude Code runs the SQL query through the MCP server, gets the results, and analyzes them — all in one step. No context switching, no copy-pasting, no manual query writing.

This same pattern applies to every external tool. Instead of being the manual bridge between Claude Code and your infrastructure, MCP lets Claude Code reach out directly.

### Configuration

MCP servers are configured in your settings.json file under the `mcpServers` key. Each server has a name, a command to start it, and optional environment variables:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/mydb"
      }
    }
  }
}
```

When Claude Code starts, it launches each configured MCP server as a subprocess. The servers communicate with Claude Code using JSON-RPC over stdin/stdout — a simple, fast protocol that works everywhere.

You can configure multiple servers simultaneously:

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
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-xxxxxxxxxxxx"
      }
    }
  }
}
```

Now Claude Code can query your database, manage GitHub issues, and send Slack messages — all from the same conversation.

### Popular MCP Servers

The MCP ecosystem is growing rapidly. Here are the servers you're most likely to use:

| Server | Package | What It Does |
|--------|---------|-------------|
| PostgreSQL | `@modelcontextprotocol/server-postgres` | Run SQL queries, inspect schema, manage data |
| GitHub | `@modelcontextprotocol/server-github` | Issues, PRs, code search, repository management |
| Slack | `@modelcontextprotocol/server-slack` | Read channels, send messages, search history |
| Filesystem | `@modelcontextprotocol/server-filesystem` | Sandboxed file access with configurable root |
| Puppeteer | `@modelcontextprotocol/server-puppeteer` | Browser automation, screenshots, web scraping |
| SQLite | `@modelcontextprotocol/server-sqlite` | Query SQLite databases, inspect tables |
| Memory | `@modelcontextprotocol/server-memory` | Persistent key-value store for cross-session data |
| Vercel | `@vercel/mcp` | Deployments, logs, environment variables, domains |

Community-built servers extend this further — there are MCP servers for Notion, Jira, Linear, MongoDB, Redis, Docker, Kubernetes, and dozens more. The registry at `mcp.so` lists available servers.

### Practical Examples

**Database exploration:**

```
Show me the schema of the users table and the 10 most recent 
signups with their subscription status.
```

With the PostgreSQL MCP server configured, Claude Code runs `\d users` to get the schema, then executes `SELECT * FROM users ORDER BY created_at DESC LIMIT 10`, joined with the subscriptions table. You get a formatted table without writing any SQL yourself.

**Issue triage:**

```
Find all open GitHub issues labeled "bug" that were created in 
the last week. Summarize them and suggest which ones I should 
prioritize.
```

With the GitHub MCP server, Claude Code fetches the issues via the GitHub API, reads their descriptions and comments, and provides a prioritized summary.

**Deployment monitoring:**

```
Check the latest Vercel deployment. Did it succeed? Show me any 
error logs if it failed.
```

With the Vercel MCP server, Claude Code checks deployment status and pulls logs — saving you from navigating the Vercel dashboard.

### Building Your Own MCP Server

If an existing MCP server doesn't cover your needs, building one is straightforward. MCP servers expose tools via JSON-RPC — each tool has a name, a description, and input/output schemas.

Here's a minimal MCP server in TypeScript that exposes a single tool:

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from 
  "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "weather",
  version: "1.0.0"
});

server.tool(
  "get_weather",
  "Get current weather for a city",
  { city: z.string().describe("City name") },
  async ({ city }) => {
    const res = await fetch(
      `https://wttr.in/${city}?format=j1`
    );
    const data = await res.json();
    const current = data.current_condition[0];
    return {
      content: [{
        type: "text",
        text: `${city}: ${current.temp_C}°C, ` +
              `${current.weatherDesc[0].value}`
      }]
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

In Python, the equivalent uses the `mcp` package:

```python
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("weather")

@mcp.tool()
async def get_weather(city: str) -> str:
    """Get current weather for a city."""
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://wttr.in/{city}?format=j1"
        )
        data = r.json()
        c = data["current_condition"][0]
        return f"{city}: {c['temp_C']}°C, " \
               f"{c['weatherDesc'][0]['value']}"

mcp.run()
```

Configure your custom server the same way:

```json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": ["./my-mcp-servers/weather.js"]
    }
  }
}
```

Now Claude Code can check the weather. More practically, you can build MCP servers that connect to your company's internal APIs, proprietary databases, or custom tooling that no public server supports.

### Security Considerations

MCP servers have the same access as any process you run. A PostgreSQL MCP server can read and write your database. A filesystem MCP server can access files within its configured root. A GitHub MCP server can create issues and PRs with your token.

**Review what you connect.** Don't blindly install MCP servers from unknown sources. Each server gets real credentials and real access to your systems.

**Use environment variables for credentials.** Never hardcode tokens or passwords in settings.json:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**Use `settings.local.json` for personal secrets.** Project-level settings.json is committed to git — anyone who clones the repo sees it. Put your personal API keys and tokens in `settings.local.json`, which should be gitignored:

```
.claude/settings.local.json  ← your personal tokens (gitignored)
.claude/settings.json         ← shared team config (committed)
```

**Scope access narrowly.** If a GitHub MCP server only needs to read issues, create a token with `issues:read` scope — not full repository access. Principle of least privilege applies to AI tools just like it does to human access.

### Managing MCP Servers

Use the `/mcp` slash command to see all configured MCP servers, their status, and the tools they expose:

```
/mcp
```

This shows which servers are running, which tools are available, and any connection errors.

You can also specify an MCP configuration file when launching Claude Code:

```bash
claude --mcp-config ./mcp.json
```

This is useful for project-specific MCP setups, CI environments, or when switching between different server configurations.

To restart a specific MCP server without restarting Claude Code:

```
/mcp restart postgres
```

Useful when you've updated the server configuration or the server process crashed.

> **Tip:** Start with one MCP server that solves a real friction point in your workflow. If you're constantly copy-pasting database query results into Claude Code, add the PostgreSQL server. If you're manually checking GitHub issues, add the GitHub server. One well-configured MCP server saves more time than five you barely use.

---
