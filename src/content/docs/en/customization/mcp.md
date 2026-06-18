---
title: MCP
description: Model Context Protocol integration
---

# MCP Integration

LingXiao connects to external systems via Model Context Protocol (MCP).

## Unified Entry

- `list_servers`: List installed servers
- `list_tools`: Discover tools
- `call_tool`: Call tools
- `list_resources`: Read resources
- `list_prompts`: Get prompts

## Configuration

```json
{
  "mcp": {
    "servers": {
      "my-server": {
        "command": "node",
        "args": ["./my-mcp-server/index.js"]
      }
    }
  }
}
```
