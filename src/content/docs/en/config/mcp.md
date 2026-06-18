---
title: MCP
description: MCP unified entry, MCP Server configuration, and MCP Forge usage
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

## MCP Forge

MCP Forge is LingXiao's natural-language to running MCP server pipeline. It auto-generates, validates, and launches MCP servers from natural language descriptions.

### Workflow

The MCP Forge pipeline has four phases:

| Phase | Description |
| --- | --- |
| Phase 1 | LLM generates MCP server code from natural language |
| Phase 2 | Code generator assembles complete project |
| Phase 3 | Sandbox runner compiles and launches server |
| Phase 3b | Inspector validator performs MCP protocol round-trip validation |
| Phase 4 | Server registered to runtime |

### REST API

MCP Forge is exposed via `/api/v1/mcp-forge/*` routes:

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v1/mcp-forge/jobs` | POST | Create generation job |
| `/api/v1/mcp-forge/jobs/:id` | GET | Query job status |
| `/api/v1/mcp-forge/jobs/:id` | DELETE | Cancel/delete job |
| `/api/v1/mcp-forge/templates` | GET | List templates |

### State Machine

Job state transitions:

```
pending → generating → compiling → validating → ready
    ↓         ↓            ↓            ↓
  failed   failed       failed       failed
```

### Template Library

MCP Forge includes a built-in template library with common templates:

- Database query server
- File system server
- HTTP API proxy
- Custom tool collection

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
