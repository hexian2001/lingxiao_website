---
title: MCP Forge
description: Template-driven MCP Server generation engine
---

# MCP Forge

Template-driven MCP Server generation engine.

## Pipeline

```text
Requirements → Template → Generate → Sandbox → Inspector → Register
```

## Core Components

- **TemplateLibrary**: Preset MCP Server patterns
- **CodeGenerator**: Generate complete server code from templates
- **SandboxRunner**: Smoke test generated code
- **InspectorValidator**: Protocol compliance validation
