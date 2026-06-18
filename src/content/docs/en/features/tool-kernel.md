---
title: Tool Kernel
description: 100+ built-in tools and ToolRegistry
---

# Tool Kernel

LingXiao includes 100+ built-in tools covering the full engineering pipeline.

## Categories

- **File System**: Read, write, directory browse, glob search, incremental edit
- **Code Search**: ripgrep full-text search, regex, file pattern filtering
- **Shell Execution**: Foreground/background, sandbox isolation, network control
- **Browser Automation**: Navigation, screenshots, clicks, form filling, JS execution, OCR
- **Office Suite**: PPTX, DOCX, XLSX, PDF generation
- **Workflow Canvas**: Visual workflow editing and execution engine
- **Communication**: Web fetch, search, HTTP requests, email

## ToolRegistry

Unified registration and management: `find_tools`, `tool_preflight`, `parallel_read_batch`

## Permission System

9-layer evaluation chain: `deny → allow → ask → yolo → always-allowed → network → hardened → strict → default allow`
