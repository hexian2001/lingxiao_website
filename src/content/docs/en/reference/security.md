---
title: Security
description: Web server token, permission controls, secret management, and security best practices
---

# Security

LingXiao is powerful by design. It can read and write files, run terminals, execute shell/Python, drive browsers, mutate Git state, open terminals, execute workflows, call external models, and spawn/coordinate agents. Treat the web server token as access to the host workspace.

## Local-First

LingXiao runs centered on the local engineering directory by default:

- SQLite stores sessions, tasks, messages, and agent state
- Configuration at `~/.lingxiao/settings.json`
- Web server token protects local API

## Web Server Token

### Authentication Methods

| Endpoint Group | Auth Method |
| --- | --- |
| `/health`, static assets | Public |
| `/api/v1/**` | server token (header `x-lingxiao-token` or `?token=` query) |
| `/api/v1/acp` | server token + ACP credentials |
| `/llm/*` | gateway virtual key |

- HTML pages inject `window.__LINGXIAO_TOKEN__` to bootstrap subsequent requests
- Hardened mode disables `?token=` query, accepting only header authentication

### Hardened Mode

Auto-enabled on non-loopback binding:

- Disables query token, only `x-lingxiao-token` header accepted
- Rate limiting cooldown: 30 seconds
- Non-localhost requests not exempt from rate limiting
- File read/write routes enforce root-path containment checks
- Worker task `write_scope` isolation enforced
- Terminal sessions must use a `cwd` inside the workspace root

## Permission Controls

### Permission Modes

| Mode | Description |
| --- | --- |
| `strict` | All write operations require confirmation (default) |
| `dev` | Development mode, relaxed confirmation |
| `networked` | Network mode, allows network tools |
| `yolo` | No confirmation needed (use with caution) |

### Permission Layers

`/mode`, `/allow-tool`, `/deny-tool`, `/ask-tool` persist to different layers:

- `session`: SQLite `session_state`
- `project`: `.lingxiao/permissions.project.json`
- `local`: `.lingxiao/permissions.local.json`
- `user`: `~/.lingxiao/permissions.user.json`

### Worker Write Scope Isolation

Each Worker task can be configured with `write_scope`, limiting its file write range. Enforced in hardened mode; recommended even when not hardened.

## Secret Management

### Potential Secrets

- Model provider API keys (in config/credentials)
- Git tokens
- Server token
- Browser cookies/session state
- Environment variables passed to tools

### Rules

- Do not expose raw secrets through `/api/v1/settings` (API responses are masked)
- Do not embed secrets in generated docs or logs
- User-defined tools should not receive unrestricted env by default
- Mask Git tokens and provider keys in UI/API responses
- Do not put tokens into Git remote URLs. Use GitHub CLI or a credential manager

## Git Publishing Safety

Before pushing a fresh repository:

- Verify `.gitignore` excludes dependencies, build output, local runtime state, archives, databases, and secrets
- Run `git status --short` and confirm no `node_modules`, `dist`, `.lingxiao`, `.env`, SQLite, archive, or token-bearing file is staged
- Run a secret scan with `rg` for common token prefixes
- Keep remote URLs clean (`https://github.com/owner/repo.git`, not `https://user:token@github.com/owner/repo.git`)

### Files That Should Not Be Committed

```text
node_modules/
dist/
.lingxiao/
*.db
*.db-wal
*.db-shm
.env
*.log
~/.lingxiao/
```

## Rate Limiting

- In-process self-calls (no remoteAddress) → always exempt
- Non-hardened mode localhost → exempt
- Hardened mode / non-localhost → not exempt, 429 triggers 30-second cooldown
- Local LLM Gateway per virtual key quota: `rpm` / `tpm` / `daily_token_budget`

## Worktree Isolation

Each task can run in an isolated Git worktree to avoid working directory conflicts:

```bash
lingxiao start --worktree feature-x
```

On exit with uncommitted changes, you will be asked whether to keep the worktree.
