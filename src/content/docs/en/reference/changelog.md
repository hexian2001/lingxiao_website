---
title: Changelog
description: Version history and changes
---

# Changelog

## v0.3.9 (Current)

### Core System

- **Expert Panel System**: 13 preset roles (Architect, Fullstack, Backend, Frontend, QA, Review, DevOps, Doc, Explore, Verify, Office, Research, Bughunter), Leader-Worker multi-role collaboration
- **Task DAG Orchestration**: Dependency-aware task graphs, parallel scheduling, speculative execution, failure rollback
- **Full State Sync**: WebUI/TUI/CLI three-way real-time sync via `session:runtime_state` unified snapshot + SSE + ACP JSON-RPC
- **Orchestration Verification Kernel**: Structured verdict extraction (PASS/FAIL/BLOCKED/UNKNOWN), adversarial verification, adaptive orchestration, automatic repair task creation

### Tools & Capabilities

- **100+ Built-in Tools**: File I/O, Shell execution, browser automation, Git operations, code search, web fetch, OCR, etc.
- **MCP Forge Engine**: Generate stdio/http MCP servers from natural language descriptions, with tool discovery and invocation
- **14 Built-in Skill Packs**: Phase Loader injects into Agent context on demand, priority: project > plugin > user > built-in
- **Office Document Generation**: HTML-first document generation with PDF/PNG/DOCX/XLSX/PPTX export

### Persistence & Memory

- **Persistent Memory System**: FTS5 full-text search + BM25 scoring + AutoDream checkpoint consolidation
- **SQLite WAL Mode**: Sessions, messages, tasks, agent state, memory all persisted, crash-recoverable
- **Verifiable Assumption Tracking**: Agents declare assumptions that are auto-verified; falsified assumptions force correction

### Autonomy & Gateway

- **Eternal Autonomous Mode**: IDLE → CHECK → PATROL → THINK → WAIT cycle, exponential backoff, budget circuit breaker
- **Local LLM Gateway**: OpenAI/Anthropic dual-format proxy, virtual key management, per-key RPM/TPM/daily token budget rate limiting
- **Bughunt DAG Scheduler**: Structured bug hunting, ledger management, report generation

### Platform & Development

- **CLI Command Tree**: `lingxiao start/list/init/doctor/about/demo/agents/daemon/worktree`
- **Daemon Background Mode**: Process self-healing supervisor, auto-restart on crash
- **Git Worktree Isolation**: Each task can run in an isolated worktree
- **Permission System**: strict/dev/networked/yolo modes, session/project/local/user four-layer persistence
- **Team Collaboration Mode**: Multi-agent P2P messaging, task transfer, review request/result

### Security

- **Hardened Mode**: Auto-enabled on non-loopback binding, disables query token, enforces header auth
- **Rate Limiting Cooldown**: 429 triggers 30s cooldown
- **Write Scope Isolation**: Worker task `write_scope` enforcement
- **Secret Masking**: API responses mask Git tokens and provider keys

## System Requirements

| Dependency | Requirement |
| --- | --- |
| Node.js | >= 24.0.0 |
| Git | Recommended |
| OS | Linux / macOS / Windows / WSL |

## Tech Stack

| Layer | Technology |
| --- | --- |
| Runtime | Node.js 24, TypeScript (ESM) |
| Web Server | Fastify, @fastify/websocket |
| Web UI | React, Zustand, Vite |
| TUI | Ink |
| Database | SQLite (WAL + FTS5) |
| CLI | Commander.js, Inquirer, Chalk |
| LLM | OpenAI SDK, Anthropic SDK, Vercel AI SDK |
