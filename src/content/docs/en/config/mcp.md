---
title: MCP
description: MCP unified entry, MCP Server configuration, and MCP Share
---

# MCP (Model Context Protocol)

LingXiao connects to external systems through the unified `mcp` tool entry, supporting three capability types: tools, resources, and prompts.

## Unified Entry

All MCP operations are performed through the `mcp` tool:

| Action | Description |
| --- | --- |
| `list_servers` | List installed MCP servers |
| `list_tools` | List server-exposed tools |
| `call_tool` | Call a server tool |
| `list_resources` | List server resources |
| `read_resource` | Read a server resource |
| `list_prompts` | List server prompts |
| `get_prompt` | Get a server prompt |
| `list_resource_templates` | List resource templates |
| `capability_snapshot` | View server capability snapshot |

## MCP Server Configuration

MCP servers are configured via `settings.mcp.servers`:

### stdio Servers

```json
{
  "mcp": {
    "servers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"],
        "env": {}
      }
    }
  }
}
```

### Remote HTTP Servers

```json
{
  "mcp": {
    "servers": {
      "remote-api": {
        "url": "https://example.com/mcp",
        "transport": "streamable-http"
      }
    }
  }
}
```

### Adding via Slash Commands

```bash
# Add remote HTTP server
/mcp add-remote my-server https://example.com/mcp "My Server"

# Add stdio server
/mcp add-stdio my-server npx -y @modelcontextprotocol/server-filesystem /tmp
```

## MCP Share

MCP Share supports importing/exporting MCP server configurations via share links and `.mcpb` bundles.

### Share Links

Generates portable share links containing the server's complete configuration (sensitive info sanitized).

### .mcpb Bundles

`.mcpb` is a portable packaging format for MCP servers, containing:

- Server code or configuration
- Dependency declarations
- Metadata

## Plugin-Contributed MCP

When a plugin is enabled, its contributed MCP servers sync to `settings.mcp.servers`, accessible through the same `mcp` tool entry.

## Runtime Relationship

- MCP tools registered to ToolRegistry can be called by Agents at runtime
- MCP resources are read via `read_resource`
- MCP prompts are obtained via `get_prompt`
- All MCP operation artifacts, URIs, and validation results are written to work notes
