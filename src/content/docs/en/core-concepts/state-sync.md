---
title: State Sync
description: WebUI/TUI/CLI real-time synchronization
---

# Full State Synchronization

All runtime state enters the same engineering kernel with three-way real-time sync.

## Sync Channels

- **SSE**: Server-Sent Events for real-time state
- **ACP JSON-RPC**: Agent Communication Protocol bidirectional
- **SQLite**: Persistent storage

## Synced Content

- Task lifecycle events
- Agent state changes
- Tool call traces
- Code changes (diffs, Git operations)
- Session state (recoverable)

## Session Recovery

```bash
lingxiao --session <session_id>
```
