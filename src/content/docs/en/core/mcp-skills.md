---
title: MCP Forge and Skills
description: MCP Server generation engine, share codes, Skills 4-layer priority
lang: en
---

# MCP Forge and Skills

LingXiao uses the MCP Forge engine and Skills system to make Agent capabilities generatable, shareable, and injectable.

## MCP Forge

MCP Forge is a template-driven MCP Server generation engine that automatically generates, validates, and registers MCP Servers through a state machine pipeline.

### Generation Pipeline

```text
Requirements → Template Selection → Code Generation → Sandbox Smoke Test → Inspector Validation → Registration
```

| Phase | Description |
| --- | --- |
| Requirements | Describe what tools/resources/prompts are needed |
| Template Selection | Match the best template from the template library |
| Code Generation | Generate TypeScript MCP Server source from template |
| Sandbox Smoke Test | Start the generated Server in an isolated sandbox for smoke testing |
| Inspector Validation | Validate MCP protocol compliance using MCP Inspector |
| Registration | Register to `settings.mcp.servers` after validation passes |

### Core Components

| Component | File | Responsibility |
| --- | --- | --- |
| Forge Engine | `McpForgeEngine.ts` | Manages generation state machine: idle → requirements → template → generate → sandbox → inspect → register |
| Template Library | `TemplateLibrary.ts` | Categorized template registry with metadata, variables, and file blueprints |
| Code Generator | `CodeGenerator.ts` | Produces TypeScript MCP Server source from templates |
| Sandbox Runner | `SandboxRunner.ts` | Runs generated Server in isolated sandbox for smoke testing |
| Inspector Validator | `InspectorValidator.ts` | Validates MCP protocol compliance using MCP Inspector |

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

```text
Project-level > Plugin-contributed > User-level > Built-in
```

| Source | Path | Description |
| --- | --- | --- |
| Project-level | `.lingxiao/skills/` | Project-specific skills, highest priority |
| Plugin-contributed | Plugin `skills/` directory | Skills installed via plugin marketplace |
| User-level | `~/.lingxiao/skills/` | Global user skills, cross-project |
| Built-in | Bundled with LingXiao | 14 built-in skill packages |

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

```text
skills/
  security-review/
    index.md          # Skill main file (frontmatter)
    phases/
      analyze.md      # Analysis phase knowledge
      review.md       # Review phase knowledge
      report.md       # Report phase knowledge
```

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

All MCP Servers (including Forge-generated ones) are accessed through the unified `mcp` tool:

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
