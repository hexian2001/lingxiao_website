---
title: Changelog
description: Version history and changes
---

# Changelog

## v1.0.2 (Current)

> **Version range:** v1.0.1 → v1.0.2 | 9 commits | 85 files changed | +5,814 / -380 lines

### ✨ New Features

#### Web UI

- **Workspace Picker** — Quick workspace switching from sidebar, auto-tracks recent workspaces
- **Git Activity Visualization** — New Git activity monitor panel, session-level git event stream, Agent stats, and Gate results
- **Onboarding Wizard** — First-run guide for LLM config, workspace selection, and project initialization
- **Update Notification** — Auto-detects new versions, sidebar version badge + one-click update
- **File Changes Panel** — New FileChanges API and store, real-time file change tracking

#### TUI

- **Onboarding** — TUI-first onboarding flow (`OnboardingTui.ts`)
- **Clipboard Support** — New clipboard module, copy/paste in TUI
- **Composer Optimization** — Improved input interaction, enhanced paste controller

#### Desktop

- **Electron Desktop App** — New `src/desktop/` module, Windows MSI/NSIS installer support
- Type-safe IPC channels, preload script isolates renderer process

#### Git Tools

- **GitTool Enhancement** (+153 lines) — More git operations and activity monitoring event chain
- **GitService Enhancement** (+254 lines) — Backend service layer fully expanded

### 🐛 Bug Fixes

- **macOS IME Enter Misfire** — `ChatView.tsx` and `MessageInput.tsx` add `isComposing` guard, Enter during IME composition no longer sends
- **CI tsc Compilation Failure** — `src/desktop/` depends on electron types, excluded from main tsconfig, new `tsconfig.desktop.json` for isolated compilation
- **Windows Portable Packaging Failure** — Windows CI has no `zip` command, switched to PowerShell `Compress-Archive`
- **release.yml YAML Syntax Error** — Release notes table row misalignment fixed
- **Desktop Config Lost** — Merge conflict resolution accidentally dropped desktop scripts/deps/build config, all restored
- **CircuitBreaker State** — LlmGuard recycle resets circuit breaker, preventing new client from being blocked by stale failure counts

### 🔧 Engineering & CI/CD

- **CI Workflow** — New `ci.yml`, auto-runs tsc type check + build on push/PR
- **Release Workflow** — New `release.yml`, tag-triggered auto-build:
  - 4-platform portable packages (linux-x64, linux-arm64, darwin-arm64, win-x64)
  - 3-platform SEA binaries (linux-x64, darwin-arm64, win-x64)
  - Windows desktop (MSI artifact + NSIS published to GitHub Releases, supports electron-updater auto-update)
  - Source tarball
  - Auto-creates GitHub Release and aggregates all artifacts
- **SEA Binary** — New `sea-config.json` + `build-binary.mjs`, Node.js SEA packaging
- **Portable Packaging** — New `package-portable.mjs`, cross-platform tar.gz/zip packaging

### 📦 Dependency Changes

- Added `electron` ^42.4.1 (devDep)
- Added `electron-builder` ^26.15.3 (devDep)
- Added `electron-updater` ^6.8.9 (dependency)

### 🌐 i18n

- Chinese/English translations synced, added Workspace, Git Activity, Onboarding, update notification module copy

### 📋 File Change Details

| Area | Files | Key Modules |
| --- | --- | --- |
| Web UI | 30+ | WorkspacePicker, GitActivityView, OnboardingWizard, UpdateNotification, FileChangesApi |
| TUI | 8 | OnboardingTui, clipboard, Composer, paste/key controllers |
| Backend | 15+ | GitService, WorkspaceRoutes, FileChangesApi, MiscRoutes, ServerAuth |
| Agent Core | 10 | AgentDefinitionService, LeaderAgent, LlmGuard, RoleRegistry, LeaderThinkingLoop |
| Desktop | 3 | desktop/main.ts, desktop/preload.ts, tsconfig.desktop.json |
| CI/CD | 6 | ci.yml, release.yml, build-binary.mjs, package-portable.mjs, sea-config.json |
| CLI | 3 | cli.ts (refactor), cli_upgrade.ts (enhanced), config.ts |

## v1.0.0

### 🏗️ Core System

- **Expert Team System**: 13 preset roles, Leader-Worker multi-role collaboration
- **Task DAG Orchestration**: Dependency-aware task graph, parallel scheduling, speculative execution, rollback on failure
- **Full State Sync**: WebUI/TUI/CLI real-time sync via unified snapshot + SSE + ACP JSON-RPC
- **Orchestration Acceptance Kernel**: Structured verdict extraction, adversarial verification, adaptive orchestration, auto-repair

### 🔧 Tools & Capabilities

- **100+ Built-in Tools**: File I/O, shell, browser automation, Git, code search, web scraping, OCR
- **MCP Forge Generator**: Generate MCP servers from natural language
- **14 Built-in Skill Packs**: Phase Loader priority injection
- **Office Document Generation**: HTML-first with PDF/PNG/DOCX/XLSX/PPTX export

### 💾 Persistence & Memory

- **Persistent Memory**: FTS5 + BM25 + AutoDream checkpoint integration
- **SQLite WAL**: Full crash recovery
- **Verifiable Assumptions**: Auto-verified, falsification forces correction

### 🔄 Autonomy & Gateway

- **Eternal Mode**: Autonomous loop with exponential backoff and budget circuit breaker
- **Local LLM Gateway**: Dual-format proxy, virtual keys, per-key rate/budget limiting
- **Bughunt DAG**: Structured bug hunting with ledger and reports

### 🖥️ Platform & Development

- **CLI Tree**: `lingxiao start/list/init/doctor/about/demo/agents/daemon/worktree`
- **Daemon Mode**: Self-healing process guard
- **Git Worktree Isolation**: Per-task isolated worktrees
- **Permission System**: Four modes, four-layer persistence
- **Team Collaboration**: P2P messaging, task delegation, review workflows

### 🔒 Security

- **Hardened Mode**: Non-loopback auto-enable, header auth enforcement
- **Rate Limit Cooldown**: 429 → 30s cooldown
- **Write Scope Isolation**: Worker `write_scope` enforcement
- **Key Masking**: API response token masking
