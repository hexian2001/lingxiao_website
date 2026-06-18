---
title: MCP Forge and Skills
description: MCP Server generation engine, share codes, Skills 4-layer priority
---

# MCP Forge and Skills

LingXiao uses the MCP Forge engine and Skills system to make Agent capabilities generatable, shareable, and injectable.

## MCP Forge

MCP Forge is a template-driven MCP Server generation engine that automatically generates, validates, and registers MCP Servers through a state machine pipeline.

### Generation Pipeline

<div class="doc-flow" role="img" aria-label="MCP Forge generation pipeline: requirements, template selection, code generation, sandbox smoke test, inspector validation, registration.">
  <span>Requirements</span><i>→</i><span>Template Selection</span><i>→</i><span>Code Generation</span><i>→</i><span>Sandbox Smoke Test</span><i>→</i><span>Inspector Validation</span><i>→</i><strong>Registration</strong>
</div>

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

<div class="doc-flow doc-flow-priority" role="img" aria-label="Skills source priority: project-level outranks plugin-contributed, user-level, and built-in.">
  <strong>Project-level</strong><i>›</i><span>Plugin-contributed</span><i>›</i><span>User-level</span><i>›</i><span>Built-in</span>
</div>

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

<div class="doc-file-tree" role="img" aria-label="Skill phase file structure: security-review contains index.md and analyze, review, report files under phases.">
  <div><strong>skills/</strong></div>
  <div><span>security-review/</span></div>
  <div><span>index.md</span><em>Skill main file (frontmatter)</em></div>
  <div><span>phases/</span></div>
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
