---
title: Tool Kernel
description: 100+ built-in tools, ToolRegistry unified management, and permission system
---

# Tool Kernel

LingXiao has 100+ built-in tools covering the full engineering chain. All tools are registered and managed through the ToolRegistry, supporting permission evaluation, parallel execution, and preflight checks.

## Tool Categories

### File System

File read/write, directory browsing, glob search, incremental editing:

- `file_read`: Read file contents, supports line range
- `file_create`: Create or overwrite files, atomic writes
- `structured_patch`: Incremental modification, supports search/replace, line range replacement, insertion
- `list_dir`: Directory tree browsing
- `glob`: File pattern matching search

### Code Search

High-performance full-text search based on ripgrep:

- `code_search`: Regex search with file pattern filtering
- Search path scoping and timeout control
- Result pagination and offset continuation

### Shell Execution

Safe command-line execution environment:

- `shell`: Foreground/background execution, sandbox isolation, network mode control
- Working directory and environment variable support
- Background tasks persist across tool calls

### Python Execution

Embedded Python code execution:

- `python_exec`: Execute Python code snippets, returns stdout
- Timeout and output size limits

### Browser Automation

Full browser operation capabilities:

- `browser_action`: Navigate, click, fill forms, wait for elements, read text, execute JS
- `browser_visual_verify`: Page verification, assertions + screenshots
- `screenshot`: Web page screenshots
- `visual_contact_sheet`: Multi-image collage overview
- `ocr`: Local OCR text recognition (tesseract.js, supports Chinese + English)

### Office Suite

Document generation and editing:

- `generate_pptx` / `edit_pptx` / `inspect_pptx`: PPTX generation/editing/inspection
- `generate_docx`: DOCX document generation
- `generate_html_presentation` / `generate_html_document`: HTML format output

### Communication

Network communication tools:

- `web_fetch`: Web page fetching, auto-switches between fetch/browser rendering
- `web_search`: Search engine queries with advanced syntax
- `http_request`: HTTP requests supporting all HTTP methods

### Persistent Memory

- `memory`: Save, search, read, and delete long-term memory
- FTS5 + BM25 full-text search support

### MCP Integration

- `mcp`: Unified MCP entry point for discovering and calling MCP tools/resources/prompts

## ToolRegistry

All tools are registered and managed through the ToolRegistry:

- `find_tools`: Search tools by name, description, category, tier
- `tool_preflight`: Call preflight, validates parameter schema and preconditions
- `parallel_read_batch`: Parallel read-only batch processing, safe tools auto-parallelize

## Permission System

Tool calls follow a 9-layer evaluation chain:

<div class="doc-flow doc-flow-long" role="img" aria-label="Nine-layer tool permission evaluation chain: deny, allow, ask, yolo, always allowed, network, hardened, strict, default allow.">
  <span>deny</span><i>→</i><span>allow</span><i>→</i><span>ask</span><i>→</i><span>yolo</span><i>→</i><span>always-allowed</span><i>→</i><span>network</span><i>→</i><span>hardened</span><i>→</i><span>strict</span><i>→</i><strong>default allow</strong>
</div>

### Permission Levels

| Level | Description |
| --- | --- |
| `deny` | Explicitly denied, cannot be overridden |
| `allow` | Explicitly allowed |
| `ask` | Ask user for confirmation |
| `yolo` | Skip all confirmations (dangerous) |
| `always-allowed` | Permanently allowed |
| `network` | Network access permission |
| `hardened` | Hardened mode restriction |
| `strict` | Strict mode restriction |
| `default allow` | Allowed by default |

## Tool Capability Tiers

Tools are classified into four capability tiers:

| Tier | Description | Examples |
| --- | --- | --- |
| `read` | Read-only tools | file_read, code_search, list_dir |
| `write` | Write tools | file_create, structured_patch |
| `execute` | Execution tools | shell, python_exec |
| `compute` | Compute tools | node_repl, parallel_read_batch |
