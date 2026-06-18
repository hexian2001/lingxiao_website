---
title: CLI Reference
description: Complete command tree and options for the LingXiao CLI
---

# CLI Reference

The LingXiao CLI (`lingxiao`) is the primary entry point, built on Commander.js. It launches the TUI interface and WebUI service, and provides session management, environment diagnostics, background daemons, Git Worktree management, and custom Agent definitions.

## Command Tree

```text
lingxiao                  # Default: start TUI + WebUI (equivalent to lingxiao start)
lingxiao start            # Start a session
lingxiao list             # List all sessions
lingxiao init             # First-run configuration wizard
lingxiao doctor           # Environment diagnostics
lingxiao about            # Show about info
lingxiao demo <id>        # Start a specific session in demo mode
lingxiao agents ...       # Manage custom Agent definitions
lingxiao daemon ...       # Manage background daemon services
lingxiao worktree ...     # Manage Git Worktrees
```

## lingxiao start

Start a LingXiao session with TUI and WebUI by default.

```bash
lingxiao start [options]
```

### Options

| Option | Description |
| --- | --- |
| `--bg` | Run in background (no TUI, services only) |
| `--name <name>` | Specify session name |
| `--output-format <format>` | Output format (`text` \| `stream-json`), default `text` |
| `--daemon-mode` | Used internally by DaemonManager, not for direct use |
| `--worktree [name]` | Run in an isolated Git Worktree |
| `--worktree-branch <branch>` | Specify the branch name for the Worktree |
| `--tmux` | Use tmux pane splitting (experimental) |
| `-s, --session <id>` | Resume a specific session ID |

### Examples

```bash
# Default start
lingxiao

# Background mode, WebUI only
lingxiao start --bg --name my-project

# Run in isolated Worktree
lingxiao start --worktree feature-x

# Resume existing session
lingxiao start --session abc123
```

## lingxiao list

List all saved sessions.

```bash
lingxiao list
```

Output includes session ID, creation time, message count, and status.

## lingxiao init

First-run configuration wizard guiding you through model connection, permissions, and initialization.

```bash
lingxiao init [options]
```

| Option | Description |
| --- | --- |
| `--check` | Run built-in environment check only, no interactive config |

```bash
# Full interactive config
lingxiao init

# Environment check only
lingxiao init --check
```

## lingxiao doctor

Run runtime environment diagnostics, checking Node.js version, Git, dependencies, ports, etc.

```bash
lingxiao doctor [options]
```

| Option | Description |
| --- | --- |
| `--json` | Output JSON format report |

Exit code `0` means environment is ready, `1` means issues found.

## lingxiao about

Display LingXiao version, vision, and tech stack info.

```bash
lingxiao about
```

## lingxiao agents

Manage custom Agent definitions with create, show, update, and delete operations.

### agents list

List custom Agent definitions.

| Option | Description |
| --- | --- |
| `--all` | Show definitions shadowed by project/global overrides |
| `--json` | Output JSON |

### agents show

Show details of a specific Agent.

```bash
lingxiao agents show <name> [options]
```

| Option | Description |
| --- | --- |
| `--global` | View global definition |
| `--project` | View project-level definition |
| `--json` | Output JSON |

### agents create

Create a custom Agent.

```bash
lingxiao agents create <name> [options]
```

| Option | Description |
| --- | --- |
| `--description <text>` | Agent description |
| `--prompt <text>` | Agent system prompt |
| `--prompt-file <path>` | Read system prompt from file |
| `--base-role <name>` | Inherited built-in role baseline |
| `--model <model>` | Default model for this Agent |
| `--backend <backend>` | Worker backend: `worker_process` \| `claude` \| `codex` |
| `--tool <name>` | Allowed tools, repeatable or comma-separated |
| `--skill <name>` | Default skills, repeatable or comma-separated |
| `--global` | Write to global `~/.lingxiao/agents` |
| `--project` | Write to project `.lingxiao/agents` |
| `--json` | Output JSON |

### agents update

Update an existing custom Agent definition. Same options as `create`.

### agents delete

Delete a custom Agent definition.

| Option | Description |
| --- | --- |
| `--global` | Delete global definition |
| `--project` | Delete project-level definition |
| `-y, --yes` | Skip confirmation |

## lingxiao daemon

Manage LingXiao background daemon services.

### daemon start

| Option | Description |
| --- | --- |
| `-p, --port <port>` | Port number, default `8080` |
| `-H, --host <host>` | Listen address, default `127.0.0.1` |
| `-s, --session <id>` | Session ID to resume |
| `--supervisor` | Enable process self-healing (auto-restart on crash) |

### daemon stop / restart / status

```bash
lingxiao daemon stop
lingxiao daemon restart [-p <port>] [-H <host>]
lingxiao daemon status
```

### daemon supervisor-status / stop-supervisor

```bash
lingxiao daemon supervisor-status
lingxiao daemon stop-supervisor
```

### daemon ps / logs / kill / attach

```bash
lingxiao daemon ps
lingxiao daemon logs <name> [-f] [-n <lines>]
lingxiao daemon kill <name> [-f]
lingxiao daemon attach <name>
```

## lingxiao worktree

Manage Git Worktrees for isolated task execution.

```bash
lingxiao worktree list
lingxiao worktree remove <name> [--keep-branch]
lingxiao worktree prune
```

## Configuration Files

```text
~/.lingxiao/settings.json    # Global config
~/.lingxiao/port             # Web service port record
~/.lingxiao/agents/          # Global custom Agent definitions
.lingxiao/agents/            # Project-level custom Agent definitions
.lingxiao/permissions.*.json # Project-level permission configs
```

## Environment Variables

| Variable | Description |
| --- | --- |
| `LINGXIAO_WEB_HOST` | Web service listen address |
| `LINGXIAO_WEB_PORT` | Web service port |
| `LINGXIAO_NO_AUTO_START` | Set to `1` to disable auto-start |
| `LINGXIAO_DAEMON_MODE` | Daemon mode flag |
| `LINGXIAO_SESSION_NAME` | Session name |
| `LINGXIAO_LOG_PATH` | Log file path |
| `FORCE_NO_TUI` | Set to `1` to force-disable TUI |

## System Requirements

- **Node.js** >= 24.0.0
- **Git** (recommended)
- **OS**: Linux / macOS / Windows / WSL
