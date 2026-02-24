# MuleSoft MCP Server Setup Guide

Set up the MuleSoft MCP Server to connect your AI-powered IDE (Claude Code, Cursor, VS Code) directly to Anypoint Platform. This is optional for the course but recommended for Module 7 and beyond.

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **Node.js** | Version 20 or later ([download](https://nodejs.org/)) |
| **Git** | Any recent version |
| **Anypoint Platform account** | Trial or paid ([sign up](https://anypoint.mulesoft.com/login/signup)) |
| **Organization admin access** | Required to create a Connected App |

Verify Node.js is installed:

```bash
node --version
# Should output v20.x.x or higher
```

---

## Step 1: Create a Connected App in Anypoint Platform

The MCP server authenticates to Anypoint Platform using OAuth 2.0 Client Credentials. You need a Connected App that "acts on its own behalf."

1. Log into [Anypoint Platform](https://anypoint.mulesoft.com)
2. Navigate to **Access Management** (hamburger menu, top-left)
3. Click **Connected Apps** in the left sidebar
4. Click **Create App**
5. Configure:
   - **Name:** `MCP Server` (or any descriptive name)
   - **Type:** Select **App acts on its own behalf (client credentials)**
   - **Grant type:** Client Credentials
6. Add these **scopes** (select your business group and all environments for each):

| Scope | Purpose |
|-------|---------|
| View Organization | Read org structure |
| View Connected Applications | View app configs |
| Read Applications | List deployed apps |
| Exchange Viewer | Browse Exchange assets |
| Manage API Configuration | Create/manage API instances (Module 7) |
| Manage Policies | Apply API policies (Module 7) |

> **Note:** The scope "Mule Developer Generative AI User" requires Agentforce and is not available on trial orgs. You can skip it — the MCP server still works for project scaffolding, Exchange search, deployment, and API management.

7. Click **Save**
8. **Copy the Client ID and Client Secret** — you'll need them in Step 3. The secret is only shown once!

---

## Step 2: Install the MCP Server

Run this in your terminal:

```bash
npm install -g @mulesoft/mcp-server
```

Or use `npx` (no global install needed) — the IDE configs below use `npx` which auto-downloads the latest version.

---

## Step 3: Configure Your IDE

Add the MCP server configuration to your IDE. Replace `YOUR_CLIENT_ID` and `YOUR_CLIENT_SECRET` with the values from Step 1.

### Claude Code (CLI)

Create or edit `~/.claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mulesoft": {
      "command": "npx",
      "args": ["-y", "@mulesoft/mcp-server", "start"],
      "env": {
        "ANYPOINT_CLIENT_ID": "YOUR_CLIENT_ID",
        "ANYPOINT_CLIENT_SECRET": "YOUR_CLIENT_SECRET",
        "ANYPOINT_REGION": "PROD_US"
      }
    }
  }
}
```

### Cursor

Create or edit `.cursor/mcp.json` in your project root (or global `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "mulesoft": {
      "command": "npx",
      "args": ["-y", "@mulesoft/mcp-server", "start"],
      "env": {
        "ANYPOINT_CLIENT_ID": "YOUR_CLIENT_ID",
        "ANYPOINT_CLIENT_SECRET": "YOUR_CLIENT_SECRET",
        "ANYPOINT_REGION": "PROD_US"
      }
    }
  }
}
```

### VS Code

Create or edit `.vscode/mcp.json` in your project root:

```json
{
  "mcp": {
    "servers": {
      "mulesoft": {
        "command": "npx",
        "args": ["-y", "@mulesoft/mcp-server", "start"],
        "env": {
          "ANYPOINT_CLIENT_ID": "YOUR_CLIENT_ID",
          "ANYPOINT_CLIENT_SECRET": "YOUR_CLIENT_SECRET",
          "ANYPOINT_REGION": "PROD_US"
        }
      }
    }
  }
}
```

> **Note:** VS Code uses `"mcp" > "servers"` nesting, not `"mcpServers"`. The format differs from Claude Code and Cursor.

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANYPOINT_CLIENT_ID` | Yes | Connected App Client ID from Step 1 |
| `ANYPOINT_CLIENT_SECRET` | Yes | Connected App Client Secret from Step 1 |
| `ANYPOINT_REGION` | No | Control plane region. Default: `PROD_US`. Options: `PROD_US`, `PROD_EU`, `PROD_CA`, `PROD_JP` |

---

## Step 4: Verify the Connection

After configuring your IDE, verify the MCP server is working:

1. **Restart your IDE** (or reload the window in VS Code)
2. The MCP server should start automatically when your IDE connects
3. Try a simple command to verify:
   - In Claude Code: ask "Search Exchange for the Salesforce connector"
   - In Cursor: use the MCP tools panel to run `search_asset` with query "Salesforce"

If you see connector results, the connection is working.

---

## Available MCP Tools

Once connected, your IDE has access to 40+ tools. The ones you'll use in this course:

| Tool | What It Does | Used In |
|------|-------------|---------|
| `search_asset` | Find connectors and templates on Exchange | Module 4 |
| `create_mule_project` | Scaffold a new Mule 4 project | Module 4 |
| `create_api_spec_project` | Scaffold a RAML or OAS project | Module 3 |
| `list_applications` | List deployed applications | Module 7 |
| `deploy_mule_application` | Deploy to CloudHub 2.0 | Module 7 |
| `list_api_instances` | List API instances | Module 7 |
| `manage_api_instance_policy` | Apply policies to APIs | Module 7 |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `npm ERR! code EACCES` | Run with `sudo npm install -g @mulesoft/mcp-server` or fix npm permissions |
| "Invalid client credentials" | Double-check Client ID and Secret. Regenerate if needed. |
| "Insufficient permissions" | Add missing scopes to your Connected App in Access Management |
| Server doesn't start | Ensure Node.js 20+ is installed: `node --version` |
| "Failed calling MuleDX AI API" | This is expected on trial orgs. AI generation tools require Agentforce. Other tools still work. |

---

## Security Notes

- **Never commit** your Client ID or Client Secret to Git
- Use environment variables or a `.env` file (gitignored) for credentials
- The Connected App has the permissions you granted — scope it minimally for students
- Rotate the Client Secret if it's ever exposed

---

## References

- [MuleSoft MCP Server Documentation](https://docs.mulesoft.com/mulesoft-mcp-server/)
- [Getting Started Guide](https://docs.mulesoft.com/mulesoft-mcp-server/getting-started)
- [Creating Connected Apps](https://docs.mulesoft.com/access-management/creating-connected-apps-dev)
- [@mulesoft/mcp-server on npm](https://www.npmjs.com/package/@mulesoft/mcp-server)
