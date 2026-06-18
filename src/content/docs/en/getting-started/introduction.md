---
title: Introduction
description: LingXiao — AI Engineering Command System, not a chat shell but a local orchestration kernel
lang: en
---

# LingXiao

> AI engineering command system. Not a chat shell: LingXiao is a local orchestration kernel for expert teams, task DAGs, real tools, evidence, WebUI/TUI synchronization, and recoverable engineering sessions.

LingXiao upgrades "chatting with a model" to "commanding an observable, recoverable, auditable AI expert team."

You provide the goal; the Leader handles judgment, decomposition, planning, DAG construction, team assembly, and task dispatch. Worker experts execute research, frontend, backend, testing, review, documentation, and Git operations in parallel. WebUI/TUI sync the full runtime state in real time — all tasks, tools, permissions, evidence, and session state enter the same engineering kernel.

## Core Value

| Capability | Description |
| --- | --- |
| Expert Panel | Leader + Worker multi-role parallelism, not single-agent dialogue |
| Task DAG | Complex goals auto-decomposed into dependency-aware task graphs |
| Full State Sync | WebUI / TUI / CLI three-way real-time sync |
| Recoverable | SQLite persistence, `--session <id>` recovery after crashes |
| Auditable | Full-chain tool call tracing, evidence collection, verification loop |

## Architecture Overview

```text
User ──→ TUI / CLI ──→ SessionManager ──→ SessionRuntime ──→ LeaderAgent
                                                                    │
                                     ┌──────────────────────────────┼──────────────────┐
                                     ▼                              ▼                  ▼
                               TaskBoard / DAG              AgentPool           ToolRegistry
                                     │                      │                     │
                                     ▼                      ▼                     ▼
                              Worker Experts ←────────── Pool ←─────────── Git / Workbench
                                     │
                                     ▼
                                SQLite DB
```

## System Requirements

| Dependency | Requirement |
| --- | --- |
| Node.js | `>=24.0.0` |
| npm | Bundled with Node 24 |
| Git | Recommended |
| OS | Linux / macOS / Windows / WSL |

## Next Steps

- [Installation](./install) — Set up LingXiao from scratch
- [Connect Models](./connect-models) — Configure LLM providers
- [First Run](./first-run) — Launch your first expert panel
