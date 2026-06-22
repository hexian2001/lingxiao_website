---
title: MCP and Skills
description: MCP Server management, share codes, Skills 4-layer priority
---

# MCP and Skills

LingXiao uses the MCP protocol and Skills system to make Agent capabilities extensible, shareable, and injectable.

## MCP Share

MCP Share provides share code export/import for cross-environment MCP Server sharing:

- **Export**: Generate share codes, package server files + config + metadata as a bundle
- **Import**: Import MCP Server via share code, with automatic validation and registration
- **Preview**: Preview bundle contents before importing

### Share Code Structure

```typescript
interface McpBundle {
  serverFiles: Record<string, string>;  // Source files
  config: McpServerConfig;              // MCP configuration
  metadata: {
    name: string;
    description: string;
    version: string;
    createdAt: string;
  };
}
```

## Skills System

Skills are execution knowledge, processes, and domain constraints injected into Agent context.

### 4-Layer Source Priority

<div class="doc-flow doc-flow-priority" role="img" aria-label="Skills source priority: project-level outranks plugin-contributed, user-level, and built-in.">
  <strong>Project-level</strong><i>›</i><span>Plugin-contributed</span><i>›</i><span>User-level</span><i>›</i><span>Built-in</span>
</div>

| Source | Path | Description |
| --- | --- | --- |
| Project-level | `.lingxiao/skills/` | Project-specific skills, highest priority |
| Plugin-contributed | Plugin `skills/` directory | Skills installed via plugin marketplace |
| User-level | `~/.lingxiao/skills/` | Global user skills, cross-project |
| Built-in | Bundled with LingXiao | Built-in skill packages |

### Skill Structure

Each Skill consists of YAML frontmatter and Markdown body:

```yaml
---
name: security-review
description: Security review skill
phases:
  - analyze
  - review
  - report
priority: high
---

# Security Review Process

## Analysis Phase
Check dependency vulnerabilities, input validation, permission boundaries...

## Review Phase
Review security risks file by file...

## Report Phase
Generate security review report...
```

### Phase Loading

Skills support per-phase file loading:

<div class="doc-file-tree" role="img" aria-label="Skill phase file structure: skills/ root, security-review/ subdirectory, index.md main file, phases/ directory, analyze, review, report phase files.">
  <strong>skills/</strong>
  <div><strong>security-review/</strong><em>Skills security review directory</em></div>
  <div><span>index.md</span><em>Skill main file (frontmatter)</em></div>
  <div><strong>phases/</strong><em>Phase directory</em></div>
  <div><span>analyze.md</span><em>Analysis phase knowledge</em></div>
  <div><span>review.md</span><em>Review phase knowledge</em></div>
  <div><span>report.md</span><em>Report phase knowledge</em></div>
</div>

Each phase file passes Quality Gate validation before being injected into Worker prompts.

### Skill Binding

The Leader binds skills via `skill_names` in `define_agent_role` or `create_task`:

```typescript
{
  name: "security-auditor",
  skillNames: ["security-review", "owasp-top10"],
  // Skill content is auto-injected at Worker dispatch time
}
```

## Unified MCP Entry Point

All MCP Servers are accessed through the unified `mcp` tool:

```text
mcp(action="list_servers")       # List installed MCP Servers
mcp(action="list_tools")         # Discover MCP Tools
mcp(action="call_tool", ...)     # Call MCP Tool
mcp(action="list_resources")     # Discover MCP Resources
mcp(action="read_resource", ...) # Read MCP Resource
mcp(action="list_prompts")       # Discover MCP Prompts
mcp(action="get_prompt", ...)    # Get MCP Prompt
```

Plugin-contributed MCP Servers are synced to `settings.mcp.servers`, managed alongside manually installed Servers.
