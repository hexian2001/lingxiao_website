---
title: WebUI Command Center
description: Chat/Tasks/Agents/Review/Git/Blackboard/Terminal/Settings eight panels
lang: en
---

# WebUI Command Center

LingXiao's WebUI is not a simple chat interface but a complete engineering command center. It integrates task graphs, agent panels, code review, Git operations, terminal, settings, and other engineering capabilities into a real-time synchronized interface.

## Eight Functional Panels

### Chat

The main conversation panel for direct interaction with the Leader:

- Send goals and requirements
- Receive the Leader's decomposition plans and confirmation requests
- View Worker execution progress in real time
- Support file attachments and screenshots

### Tasks

Visual DAG task graph display:

- Task nodes and dependency relationships shown graphically
- Real-time status updates (pending/in_progress/completed/failed/blocked)
- Click tasks for details: owner, description, write scope, results, evidence
- Support task filtering and search

### Agents

Real-time monitoring of each Worker's runtime status:

- Role identity and current task
- Tool call records (parameters, permission evaluation, output, duration)
- Runtime logs and live output
- Result receipts and verification evidence
- Heartbeat status and process information

### Review

Code review and acceptance panel:

- View code changes submitted by Workers (diffs)
- Review verdict (PASS/FAIL/BLOCKED) and evidence
- Review suggestions and improvement notes
- Support multi-round review and fixes

### Git

Git repository management panel:

- Branch management and switching
- Commit history and diff viewing
- Worktree creation and management
- Merging and conflict resolution

### Blackboard

Shared knowledge graph panel:

- View Facts, Intents, Contracts, Design Docs
- Knowledge node relationship graphs
- Cross-Agent shared memory
- Contract versions and change history

### Terminal

Embedded terminal panel:

- Execute shell commands directly in the browser
- Share working directory with Worker shell calls
- Support foreground and background commands
- Command history and output records

### Settings

Configuration management panel:

- Model configuration (Leader/Worker model selection)
- Provider configuration (OpenAI/Anthropic/compatible services)
- Tool permission policies
- Theme and interface preferences
- LLM Gateway virtual key management

## Real-Time Sync

The WebUI syncs with the backend in real time via SSE event streams. All state changes are visible without page refresh:

```text
WebUI <-- SSE <-- SseBridge <-- SessionManager <-- Leader/Workers
```

## Access

After launching LingXiao, the terminal prints the WebUI address:

```bash
lingxiao
# Output: WebUI: http://127.0.0.1:3780
```

The default port info is written to `~/.lingxiao/port`. The WebUI is protected by Server Token; in dev mode, authentication is automatic via injected `window.__LINGXIAO_TOKEN__`.
