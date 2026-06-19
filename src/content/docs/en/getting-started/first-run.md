---
title: First Run
description: Launch your first expert panel
---

# First Run

## Start LingXiao

```bash
lingxiao
```

After launch, you will see the TUI interface and the WebUI address. The default port info is written to:

```text
~/.lingxiao/port
```

## Send Your First Goal

Enter your engineering goal in TUI or WebUI, for example:

> Create an Express REST API with user CRUD and JWT authentication

The Leader will:

1. Understand the goal and decompose tasks
2. Build a DAG task graph
3. Assemble an expert panel (Architect, Backend, QA, etc.)
4. Dispatch tasks to Workers
5. Supervise execution and verification
6. Summarize results

## Observe Runtime State

### TUI Interface

The TUI displays task lists, agent status, and tool calls in real time.

### WebUI Command Center

Open the WebUI address printed in the terminal to see:

- **Task Panel**: DAG visualization, task state transitions
- **Agent Panel**: Each Worker's role, progress, and output
- **Tool Calls**: Parameters, permissions, and results for every invocation
- **Code Changes**: File diffs and Git operations

## Session Management

```bash
# List all sessions
lingxiao list

# Resume a session
lingxiao --session <session_id>
```

All session state is persisted to SQLite and recoverable after crashes.

## Common Commands

| Command | Description |
| --- | --- |
| `lingxiao` | Start TUI + WebUI |
| `lingxiao --session <id>` | Resume a specific session |
| `lingxiao list` | List all sessions |
| `lingxiao doctor` | Environment diagnostics |

## Next Steps

- [Expert Panel](../core/expert-team) — Learn the Leader-Worker architecture
- [Task DAG](../core/task-dag) — Understand task decomposition and scheduling
