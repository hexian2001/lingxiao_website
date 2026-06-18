---
title: Full State Synchronization
description: session_runtime_state, SSE, ACP, and WebUI/TUI three-way sync
---

# Full State Synchronization

LingXiao consolidates WebUI, TUI, and backend runtime into a unified state pipeline. All runtime state enters the same engineering kernel, with three-way real-time synchronization.

## Sync Architecture

<div class="doc-vertical-flow" role="img" aria-label="State sync architecture: SessionManager produces session runtime state, routed through SseBridge and ACP to Web sessionStore and the TUI event bridge.">
  <strong>SessionManager</strong>
  <em>session:runtime_state</em>
  <em>SseBridge</em>
  <em>ACP session/update: session_runtime_state</em>
  <em>Web sessionStore / TUI event bridge</em>
</div>

`session:runtime_state` is the unified runtime snapshot, covering session status, leader busy/waiting/reviewing state, task graph, agent panel, tool call logs, message flow, and review results.

## Sync Channels

### SSE Event Stream

Server-Sent Events push real-time state changes to the WebUI:

```text
GET /api/v1/events?token=<server_token>
Content-Type: text/event-stream
```

The WebUI connects via EventSource to receive push updates without polling.

### ACP JSON-RPC

Agent Communication Protocol provides a bidirectional communication channel:

```text
GET  /api/v1/acp          # SSE event stream
POST /api/v1/acp           # JSON-RPC requests
DELETE /api/v1/acp         # Disconnect
```

ACP connections require dual credentials: `acp-connection-id` + `acp-session-token`.

### SQLite Persistence

All state is persisted to the SQLite database, including:
- Session metadata and status
- Task graph and execution history
- Messages and conversation records
- Agent state and logs
- Full tool call chain
- Token usage statistics

## Sync Content

| Category | Sync Events |
| --- | --- |
| Task lifecycle | Created, updated, dispatched, completed, failed, blocked |
| Agent state | Started, heartbeat, exited, result receipt |
| Tool calls | Parameters, permission evaluation, output, duration |
| Code changes | File diffs, Git operations |
| Message flow | Leader-Worker communication, team messages |
| Review results | Review verdict, evidence, suggestions |
| Errors and blocks | Exceptions, timeouts, dependency blocks |

## Event Types

22 `SessionUpdateKind` events cover all runtime state changes:

```typescript
enum SessionUpdateKind {
  // Task events
  task_created, task_updated, task_dispatched,
  task_completed, task_failed, task_blocked,
  // Agent events
  agent_started, agent_heartbeat, agent_exited,
  agent_result,
  // Tool events
  tool_call_started, tool_call_completed,
  // Message events
  message_sent, message_received,
  // Review events
  review_requested, review_completed,
  // Session events
  session_status_changed, session_error,
  // Other
  code_changed, git_operation, error, blocked
}
```

## Session Recovery

```bash
# Resume a specific session
lingxiao --session <session_id>

# List all sessions
lingxiao list
```

After a crash or interruption, the full runtime state is recovered from SQLite:
- DAG structure and task states rebuilt
- Agent context restored
- Message history and tool call logs preserved
- Incomplete tasks can resume

## Authentication

| Endpoint group | Auth method |
| --- | --- |
| `/health`, static assets | Public |
| `/api/v1/**` | Server Token (header `x-lingxiao-token`) |
| `/api/v1/acp` | Server Token + ACP credentials |
| `/llm/**` | LLM Gateway virtual key |

In hardened mode, Server Token only accepts header form; query parameter passing is disabled.
