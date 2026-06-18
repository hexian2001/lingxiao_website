---
title: Architecture
description: Runtime topology, module responsibilities, control/data flow, and failure boundaries
---

# Architecture Overview

LingXiao is a Node.js 24, TypeScript, React, Fastify, SQLite based AI engineering orchestration runtime. The backend source root is `src/`; the WebUI source root is `web/src`.

## Runtime Topology

```text
flowchart LR
  User["User"]
  CLI["CLI/TUI<br/>src/cli.ts"]
  Web["React Web UI<br/>web/src"]
  Server["Fastify Web Server<br/>src/server.ts"]
  ACP["ACP JSON-RPC + SSE<br/>AcpRoutes + AcpHandler"]
  Sessions["SessionManager + SessionRuntime<br/>src/runtime"]
  Leader["LeaderAgent<br/>src/agents"]
  DAG["TaskBoard / Orchestration DAG<br/>OrchestrationRuntime"]
  Workers["Worker Expert Agents<br/>AgentPool"]
  Tools["ToolRegistry<br/>src/tools"]
  DB["SQLite<br/>DatabaseManager"]
  RuntimeState["session:runtime_state<br/>Unified Snapshot"]
  Browser["BrowserRuntime"]
  Terminal["Terminal WS/PTY"]
  Memory["Memory System<br/>FTS5 + AutoDream"]
  Skills["Skills Catalog<br/>Phase Loader"]
  McpForge["MCP Forge<br/>Server Generation"]
  Eternal["Eternal Loop<br/>Autonomous Mode"]
  Gateway["Local LLM Gateway<br/>OpenAI/Anthropic Proxy"]

  User --> CLI
  User --> Web
  CLI --> Sessions
  Web --> Server
  Server --> ACP
  Server --> DB
  Server --> Gateway
  ACP --> Sessions
  Sessions --> Leader
  Sessions --> RuntimeState
  Sessions --> Eternal
  RuntimeState --> ACP
  Leader --> DAG
  Leader --> Workers
  Leader --> Memory
  Workers --> Skills
  DAG --> DB
  Leader --> Tools
  Workers --> Tools
  Sessions --> DB
  Tools --> DB
  Tools --> McpForge
  Server --> Browser
  Server --> Terminal
```

## Main Processes

### CLI/TUI

Primary entry: `src/cli.ts`.

The CLI runs interactive sessions and can create a web server with the same `DatabaseManager` and `SessionManager` dependencies. On launch, it prints a tokenized URL and writes the port to `~/.lingxiao/port`.

Startup also initializes:
- Memory maintenance pipeline (`runDueMemoryMaintenance`)
- Bundled skill synchronization to the global skill directory

### Web Server

Primary entry: `src/server.ts`.

Responsibilities:
- Create Fastify server, register `@fastify/websocket`
- Create shared runtime services: `DatabaseManager`, `SessionManager`, `EventEmitter`, `ConnectionManager`, `SseBridge`, `AcpHandler`, browser runtime, file/wiki/git APIs
- Register MCP Forge routes and MCP Share routes
- Register Local LLM Gateway routes when `llm_gateway.enabled` is true
- Inject `window.__LINGXIAO_TOKEN__` into served HTML
- Serve built web assets from `dist/web` or development fallback paths

### Web UI

Primary entry: `web/src`.

The UI is state-driven with Zustand stores:
- REST endpoints for listing sessions, settings, files, Git, plugins, tasks, workflows, stats, wiki, MCP Forge/Share, design market, etc.
- ACP JSON-RPC for session actions
- SSE via ACP connection for real-time state push

## Core Components

| Component | Responsibility |
| --- | --- |
| SessionManager | Session lifecycle: create, resume, message dispatch |
| SessionRuntime | Runtime context: Leader handle, Agent pool, tool registry |
| LeaderAgent | Commander: decompose tasks, build DAG, schedule Workers, verify results |
| TaskBoard / DAG | Task graph: dependencies, parallel scheduling, block/unblock |
| AgentPool | Worker process pool: spawn, recycle, heartbeat monitoring |
| ToolRegistry | Tool registration and invocation: 100+ built-in tools + MCP tools |
| SQLite DB | Persistent storage: sessions, messages, tasks, agent state, memory |
| RuntimeState | Unified snapshot: `session:runtime_state` three-way sync source |
| Memory System | Persistent memory: FTS5 full-text search + BM25 scoring + AutoDream |
| Skills Catalog | Skill catalog: Phase Loader injects into Agent context on demand |
| MCP Forge | MCP server generation: stdio/http MCP server from description |
| Eternal Loop | Autonomous mode: IDLE → CHECK → PATROL → THINK → WAIT cycle |
| Local LLM Gateway | Local LLM proxy: OpenAI/Anthropic dual-format |

## Control Flow

### Interactive Mode

1. User sends a goal via TUI/WebUI
2. `SessionManager` creates a session, starts `SessionRuntime`
3. `LeaderAgent` receives the goal, decomposes into a DAG task graph
4. `OrchestrationRuntime` manages task lifecycle: assign Workers, monitor execution, extract verdicts
5. Workers execute tasks via `ToolRegistry`
6. Results and state written to SQLite, pushed to all clients via `RuntimeState`

### Eternal Autonomous Mode

1. `EternalLoop` cycles at 30-second base interval (configurable)
2. CHECK phase: inspect goal status and pending tasks
3. SKIP/PATROL: skip or patrol when no tasks
4. THINK: drive Leader execution when tasks exist
5. WAIT: wait for completion, return to IDLE
6. Exponential backoff: double interval on no-op, max 960 seconds
7. Budget circuit breaker: 8 consecutive failures → auto-pause

## Data Flow

### Message Flow

```
User input → SessionManager.sendUserInput → LeaderAgent.processGoal
  → TaskBoard.createTask (DAG) → AgentPool.spawnWorker
  → Worker.execute → ToolRegistry.invoke → results to DB
  → RuntimeState.update → SSE/ACP push to all clients
```

### State Synchronization

LingXiao achieves three-way real-time sync (TUI/WebUI/CLI) via `session:runtime_state`:

- **SSE**: Server-Sent Events, unidirectional push for session state changes
- **ACP JSON-RPC**: bidirectional, WebUI sends commands and receives results via ACP connection
- **WebSocket**: terminal PTY and browser real-time interaction

## Orchestration and Verification

### Orchestration Runtime

`OrchestrationRuntime` subscribes to task lifecycle events and provides:

- **Verdict extraction**: parses `PASS`/`FAIL`/`BLOCKED`/`UNKNOWN` from task results, worker reports, and evaluation payloads
- **Default minimal evaluation policy**: tasks without explicit `evaluationPolicy` receive `required_evidence` + `max_repair: 1`
- **Follow-up task creation**: on `FAIL`/`BLOCKED` with repair budget remaining, creates repair tasks blocked-by the failed task

### Speculative Execution

The Leader can pre-judge results and start downstream tasks before upstream completion (speculative execution), rolling back speculative branches on failure.

## Failure Boundaries

| Component | Failure Behavior | Recovery Strategy |
| --- | --- | --- |
| Worker process crash | AgentPool detects heartbeat timeout | Mark task failed, OrchestrationRuntime creates repair task |
| Leader exception | SessionRuntime catches | Restore persisted DAG state |
| Web Server port in use | Auto-find available port | Write to `~/.lingxiao/port` |
| Database lock | SQLite WAL mode + retry | Transaction-level retry |
| Eternal budget exhausted | 8 consecutive failures | Auto-pause, await user intervention |
| LLM call failure | Retry + circuit breaker | Exponential backoff, circuit-breaker degradation |

## Module Inventory

| Module | Key Files | Responsibility |
| --- | --- | --- |
| CLI/TUI | `src/cli.ts`, `src/tui/*` | Command entry, Ink terminal UI |
| Web Server | `src/server.ts`, `src/web-server/*Routes.ts` | Fastify HTTP/SSE/WS routes |
| Session Runtime | `src/runtime/*`, `src/core/SessionManager.ts` | Session lifecycle, state management |
| Agent System | `src/agents/*` | Leader/Worker, role capabilities, orchestration |
| Tool Kernel | `src/tools/*` | ToolRegistry, 100+ built-in tools |
| LLM Layer | `src/llm/*` | Provider clients, streaming parsers, retry/circuit-breaker |
| Database | `src/core/Database.ts` | SQLite, WAL, FTS5 |
| Memory System | `src/core/Memory*.ts` | Persistent memory, AutoDream |
| MCP | `src/core/McpForge*.ts` | Server generation, tool discovery |
| Skills | `src/core/Skill*.ts` | Phase Loader, skill injection |
| Orchestration | `src/agents/OrchestrationRuntime.ts` | DAG management, verification, speculative execution |
| Eternal | `src/core/Eternal*.ts` | Autonomous loop, supervisor, telemetry |
| LLM Gateway | `src/core/LocalLlmGateway*.ts` | OpenAI/Anthropic proxy |
| Context | `src/core/ContextManifest.ts` | Context assembly, memory index injection |
| Office | `src/tools/implementations/office/*` | HTML-first document generation |
| Permissions | `src/core/PermissionSystem.ts` | Tool permissions, layered control |
