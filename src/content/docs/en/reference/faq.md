---
title: FAQ
description: Frequently asked questions
---

# FAQ

## How is LingXiao different from other AI coding tools?

LingXiao is not a chat shell — it's an orchestration kernel. Key differences:

- **Expert Panel**: Leader + Worker multi-role collaboration, not single-agent dialogue
- **DAG Orchestration**: Dependency-aware task graphs with parallel execution
- **Full State Sync**: WebUI/TUI/CLI three-way real-time synchronization
- **Recoverable**: SQLite persistence, recoverable after crashes
- **Verification Loop**: Structured verification + adversarial validation

## What Node.js version is required?

Node.js `>=24.0.0`. Run `lingxiao doctor` to check your environment.

## Which LLMs are supported?

- **OpenAI** (and compatible: DeepSeek, Qwen, Moonshot/Kimi, Gemini, Groq, SiliconFlow, etc.)
- **Anthropic**

Configured via environment variables or `~/.lingxiao/settings.json`. See [Connect Models](../getting-started/connect-models).

## Where is data stored?

| Type | Location |
| --- | --- |
| Global config | `~/.lingxiao/settings.json` |
| Database | SQLite files under `~/.lingxiao/` |
| Project-level config | `.lingxiao/` directory |
| Custom Agents (global) | `~/.lingxiao/agents/` |
| Custom Agents (project) | `.lingxiao/agents/` |
| Permission configs | `.lingxiao/permissions.*.json` |

## How to recover a crashed session?

```bash
lingxiao list            # List all sessions
lingxiao --session <id>  # Resume a specific session
```

All session state (messages, task DAG, agent state) is persisted to SQLite and fully recoverable after crashes.

## How to configure permission mode?

Four modes:

| Mode | Description |
| --- | --- |
| `strict` | All write operations require confirmation (default) |
| `dev` | Development mode, relaxed confirmation |
| `networked` | Network mode, allows network tools |
| `yolo` | No confirmation needed (use with caution) |

Set via the `/mode` slash command or `tools.permissionMode` in `~/.lingxiao/settings.json`.

Permissions can persist to four layers: `session`, `project`, `local`, `user`.

## How to access WebUI?

After starting LingXiao, the terminal prints a tokenized URL, e.g.:

```text
http://127.0.0.1:8080/?token=xxxxxxxx
```

Port info is written to `~/.lingxiao/port`. Hardened mode is auto-enabled for non-localhost bindings.

## How to use Git Worktree isolation?

```bash
# Start with a worktree
lingxiao start --worktree feature-x

# Manage existing worktrees
lingxiao worktree list
lingxiao worktree remove <name>
lingxiao worktree prune
```

Each task can run in an isolated Git worktree to avoid working directory conflicts.

## How to use background mode?

```bash
# Background start
lingxiao start --bg --name my-project

# Daemon mode
lingxiao daemon start -p 8080
lingxiao daemon status
lingxiao daemon stop

# View logs
lingxiao daemon logs <name> -f
```

## How to use Eternal autonomous mode?

```bash
# Use slash commands in TUI/WebUI
/eternal <goal>       # Set long-term goal
/eternal status       # Check status
/eternal pause        # Pause
/eternal resume       # Resume
```

Eternal mode cycles at 30-second base interval with exponential backoff up to 960 seconds. Auto-pauses after 8 consecutive failures.

## How to use the local LLM Gateway?

Enable in `~/.lingxiao/settings.json`:

```json
{
  "llm_gateway": {
    "enabled": true,
    "provider": "openai",
    "model": "gpt-4o",
    "default_rpm": 60,
    "default_tpm": 200000
  }
}
```

Access via `/llm/openai/v1/**` and `/llm/anthropic/v1/**` endpoints with virtual key authentication.

## How to create a custom Agent?

```bash
# Create a custom Agent
lingxiao agents create my-agent \
  --description "My Agent" \
  --base-role backend \
  --model gpt-4o-mini

# List all Agents
lingxiao agents list
```

## How to install MCP servers?

Use slash commands in TUI/WebUI:

```bash
/mcp list                    # List configured servers
/mcp search <query>          # Search marketplace
/mcp install <entry-id>      # Install
/mcp add-stdio <id> <cmd>    # Manually add stdio server
/mcp add-remote <id> <url>   # Manually add HTTP server
```
