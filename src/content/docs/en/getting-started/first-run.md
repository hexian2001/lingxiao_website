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

<div class="doc-vertical-flow">
  <strong>Leader Scheduling Flow</strong>
  <span>Understand the goal and decompose tasks</span>
  <span>Build a DAG task graph</span>
  <span>Assemble an expert panel (Architect, Backend, QA, etc.)</span>
  <span>Dispatch tasks to Workers</span>
  <span>Supervise execution and verification</span>
  <span>Summarize results</span>
</div>

## Observe Runtime State

### WebUI Command Center

Open the WebUI address printed in the terminal to see:

- **Task Panel**: DAG visualization, task state transitions
- **Agent Panel**: Each Worker's role, progress, and output
- **Tool Calls**: Parameters, permissions, and results for every invocation
- **Code Changes**: File diffs and Git operations

<img src="/static/screenshots/WebUI.png" alt="LingXiao WebUI Command Center" />

### TUI Interface

The TUI displays task lists, agent status, and tool calls in real time.

<img src="/static/screenshots/TUI.png" alt="LingXiao TUI Terminal Interface" />

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

