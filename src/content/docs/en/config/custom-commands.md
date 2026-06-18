---
title: Custom Commands
description: Slash command registration, custom commands, and command lifecycle
---

# Custom Commands

LingXiao supports extending CLI and WebUI interaction through the Slash command system. Slash commands are a shared command surface for TUI, Web chat input, and ACP `session/command`.

## Command Lifecycle

The complete flow from user input to execution:

1. **Detection**: Web/TUI input detects a `/`-prefixed command
2. **Registry lookup**: `slash_registry` finds command metadata
3. **Dispatch**: `dispatcher.ts` executes callback or forwards to SessionManager
4. **Return result**: `CommandResult` returned to client

## Command Definition

Each Slash command is registered via `SlashCommandDefinition`:

| Field | Description |
| --- | --- |
| `name` | Unique command name |
| `desc` | User-facing description |
| `usage` | Optional usage string |
| `handledBy` | `tui-local` (client-side) or `callback` (backend callback) |
| `includeInSuggestions` | Whether to appear in autocomplete |
| `includeInHelp` | Whether to appear in `/help` |
| `category` | Help grouping |
| `argCompleter` | Optional argument completion |

## Handler Types

| Handler | Meaning | Description |
| --- | --- | --- |
| `tui-local` | Client handles it | No backend callback |
| `callback` | Backend callback | Dispatched via `dispatcher.ts` |

## Custom Command Configuration

Configure custom commands in `~/.lingxiao/settings.json` or project-level `.lingxiao/settings.json`:

```json
{
  "commands": {
    "deploy": {
      "description": "Deploy to production",
      "prompt": "Execute deployment: build, test, push image"
    },
    "review": {
      "description": "Code review",
      "prompt": "Review current workspace code changes and suggest improvements"
    }
  }
}
```

### Command Format

Custom commands start with `/` and work in both TUI and WebUI. Enter `/deploy` to trigger the corresponding prompt.

## Built-in Slash Commands

LingXiao includes 66 built-in Slash commands covering session management, agent control, permissions, MCP, plugins, etc.:

### Session Management

| Command | Description |
| --- | --- |
| `/new` | Create new session |
| `/sessions` | List all sessions |
| `/fork` | Fork current session |
| `/exit` | Exit program |
| `/quit` | Exit program |

### Agent & Orchestration

| Command | Description |
| --- | --- |
| `/agents` | View agent list |
| `/roles` | View role definitions |
| `/board` | View task board |
| `/pool` | View agent pool |

### Permissions

| Command | Description |
| --- | --- |
| `/permission` | View current permission mode |
| `/mode` | Switch permission mode |

### MCP

| Command | Description |
| --- | --- |
| `/mcp list` | List configured MCP servers |
| `/mcp search <query>` | Search marketplace MCP entries |
| `/mcp install <entry-id>` | Install marketplace MCP entry |
| `/mcp tools [server-id]` | View server tools |
| `/mcp call <server-id> <tool-name> [args]` | Call server tool |
| `/mcp resources [server-id]` | View server resources |
| `/mcp read-resource <server-id> <uri>` | Read server resource |
| `/mcp prompts [server-id]` | View server prompts |
| `/mcp get-prompt <server-id> <prompt-name> [args]` | Get server prompt |
| `/mcp templates [server-id]` | List resource templates |
| `/mcp snapshot [server-id]` | View capability snapshot |
| `/mcp add-remote <id> <url> [name]` | Add remote HTTP server |
| `/mcp add-stdio <id> <command> [args...]` | Add stdio server |

### Other

| Command | Description |
| --- | --- |
| `/help` | Show help |
| `/config` | View config |
| `/skills` | View skills list |
| `/plugins` | Manage plugins |
| `/marketplace` | Access marketplace |

## Evolution Rules

1. New commands must be added to `slash_registry.ts`
2. Commands with `handledBy: 'callback'` must have callback behavior in `dispatcher.ts`
3. Web autocomplete must be updated only after the backend registry exists
4. Synonymous commands (e.g., `/quit` and `/exit`) are registered as separate entries; command names are not normalized
