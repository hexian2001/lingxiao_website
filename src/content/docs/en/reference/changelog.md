---
title: Changelog
description: Version history and changes
---

# Changelog

## v1.0.2 (Current)

### Desktop & Distribution

- **Windows Desktop**: Electron desktop client with MSI installer + NSIS auto-updating installer, electron-updater incremental updates
- **Cross-Platform Portable Builds**: Pre-built portable packages for Linux (x64/arm64), macOS (arm64), Windows (x64) — ready to use
- **SEA Binaries**: Node.js Single Executable Application standalone executables for three platforms
- **Cross-Platform Auto-Upgrade**: `lingxiao upgrade` auto-detects install path, supports source/portable modes, skips electron binary download
- **GitHub Release Automation**: CI/CD parallel builds across all platforms, tag-triggered auto-publish

### Web UI Enhancements

- **Workspace Picker**: Backend 4 APIs + recent_workspaces.json, frontend WorkspacePicker component
- **401 Token Recovery**: Web UI auto-refreshes token on 401, random port enabled by default
- **IME Composition Fix**: Enter key during IME composition no longer triggers message send (macOS/Windows)
- **Git Activity Monitor**: git:activity event full-chain display, per-session isolation + Agent stats + Gate results

### CI/CD & Engineering

- **CI Type Checking**: Full tsc --noEmit check, src/desktop isolated via dedicated tsconfig
- **Release Workflow**: 5 parallel build jobs (portable × 4 platforms + binary × 4 platforms + desktop MSI/NSIS + source)
- **Windows Compression Compatibility**: PowerShell Compress-Archive replaces zip command
- **Desktop Build Chain**: tsconfig.desktop.json for isolated electron entry compilation

## v1.0.0

### Core System

- **Expert Team System**: 13 preset roles (Architect, Fullstack, Backend, Frontend, QA, Review, DevOps, Doc, Explore, Verify, Office, Research, Bughunter), Leader-Worker multi-role collaboration
- **Task DAG Orchestration**: Dependency-aware task graph, parallel scheduling, speculative execution, rollback on failure
- **Full State Sync**: WebUI/TUI/CLI real-time sync via `session:runtime_state` unified snapshot + SSE + ACP JSON-RPC
- **Orchestration Acceptance Kernel**: Structured verdict extraction (PASS/FAIL/BLOCKED/UNKNOWN), adversarial verification, adaptive orchestration, auto-repair task creation

### Tools & Capabilities

- **100+ Built-in Tools**: File I/O, shell execution, browser automation, Git, code search, web scraping, OCR
- **MCP Forge Generator**: Generate stdio/http MCP servers from natural language descriptions
- **14 Built-in Skill Packs**: Phase Loader injects into Agent context by priority: project > plugin > user > built-in
- **Office Document Generation**: HTML-first generation with PDF/PNG/DOCX/XLSX/PPTX export

### Persistence & Memory

- **Persistent Memory System**: FTS5 full-text search + BM25 scoring + AutoDream checkpoint integration
- **SQLite WAL Mode**: Sessions, messages, tasks, Agent state, memory all persisted, crash-recoverable
- **Verifiable Assumption Tracking**: Agents declare assumptions that are auto-verified, falsification forces correction

### Autonomy & Gateway

- **Eternal Autonomous Mode**: IDLE → CHECK → PATROL → THINK → WAIT loop, exponential backoff, budget circuit breaker
- **Local LLM Gateway**: OpenAI/Anthropic dual-format proxy, virtual key management, per-key RPM/TPM/daily token budget limiting
- **Bughunt DAG Scheduler**: Structured bug hunting, ledger management, report generation

### Platform & Development

- **CLI Command Tree**: `lingxiao start/list/init/doctor/about/demo/agents/daemon/worktree`
- **Daemon Mode**: Self-healing process guard, auto-restart on crash
- **Git Worktree Isolation**: Each task can run in an isolated worktree
- **Permission System**: strict/dev/networked/yolo modes, session/project/local/user four-layer persistence
- **Team Collaboration**: Multi-Agent P2P messaging, task delegation, review requests/results

### Security

- **Hardened Mode**: Auto-enabled on non-loopback binding, disables query token, enforces header auth
- **Rate Limit Cooldown**: 429 triggers 30s cooldown
- **Write Scope Isolation**: Worker task `write_scope` enforcement
- **Key Masking**: API responses mask Git tokens and provider keys

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
| Desktop | Electron, electron-builder |
| Database | SQLite (WAL + FTS5) |
| CLI | Commander.js, Inquirer, Chalk |
| LLM | OpenAI SDK, Anthropic SDK, Vercel AI SDK |
