---
title: API Contract Index
description: HTTP REST / SSE / WebSocket / ACP JSON-RPC endpoint index
---

# API Contract Index

The LingXiao Fastify server exposes HTTP REST + SSE + WebSocket + ACP JSON-RPC endpoints. There are 207 registered routes, assembled in `src/server.ts`, with 25 `src/web-server/*Routes.ts` files registering routes by module.

## Authentication Matrix

| Endpoint Group | Auth Method | Notes |
| --- | --- | --- |
| `/health`, `/*` (static web), `/api/v1/acp/connect` | Public / static / no auth | connect stage returns connectionId + sessionToken |
| `/api/v1/**` (except acp/connect and /llm/*) | server token | header `x-lingxiao-token` or `?token=` query; hardened mode: header only |
| `/api/v1/acp` (GET SSE / POST JSON-RPC) | server token + ACP credentials | header `acp-connection-id` + `acp-session-token` |
| `/llm/openai/v1/**`, `/llm/anthropic/v1/**` | gateway virtual key | header `Authorization: Bearer <key>` or `x-api-key` |
| `/api/v1/storage` PUT | server token | Writes to `session_state` immediately |

## Rate Limiting & Hardening

- In-process self-calls (no remoteAddress) → always exempt
- Non-hardened mode localhost (127.0.0.1/::1) → exempt
- Hardened mode / non-localhost → not exempt, 429 triggers cooldown
- Non-loopback binding without hardening → strong warning, not gated

## Endpoint Group Index

### Health / Static

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | Health probe, public |
| GET | `/*` | Static web assets + SPA fallback |

### ACP Protocol

| Method | Path | Description |
| --- | --- | --- |
| POST | `/api/v1/acp/connect` | Get connectionId + sessionToken |
| GET | `/api/v1/acp` | SSE connection (requires ACP credentials) |
| POST | `/api/v1/acp` | JSON-RPC request (requires ACP credentials) |
| DELETE | `/api/v1/acp` | Disconnect ACP connection |

ACP JSON-RPC methods include: `session/send`, `session/command`, `session/interrupt`, `session/hydrate`, etc.

### Sessions

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/sessions` | List all sessions |
| POST | `/api/sessions` | Create a new session |
| GET | `/api/v1/sessions/active` | Get active session |
| POST | `/api/v1/sessions/side-thread` | Create a side thread |

### Settings / Model / Prompt

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/v1/settings` | Get settings (masked) |
| PUT | `/api/v1/settings` | Update settings |
| GET | `/api/v1/model/list` | List configured models |
| PUT | `/api/v1/model` | Update Leader model |
| GET | `/api/v1/prompt/list` | List available prompts |
| GET | `/api/v1/intuition` | Get intuition runtime state |

### Roles / Commands

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/v1/roles` | List role definitions |
| GET | `/api/v1/commands` | List slash command registry |

### Tasks / Workflow

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/v1/tasks` | List tasks |
| POST | `/api/v1/tasks` | Create a task |
| GET | `/api/v1/workflow/state` | Workflow state |
| POST | `/api/v1/workflow/toggle` | Toggle workflow mode |

### Stats / Storage

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/v1/stats` | Session statistics |
| GET | `/api/v1/storage` | Read session_state key |
| PUT | `/api/v1/storage` | Write session_state key |

### Files / Wiki / Git

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/v1/files` | List workspace files |
| GET | `/api/v1/files/content` | Read file content |
| GET | `/api/v1/wiki` | Wiki page list |
| GET | `/api/v1/git/status` | Git status |
| POST | `/api/v1/git/init` | Initialize repository |
| GET | `/api/v1/git/platform/info` | Platform integration info |
| GET | `/api/v1/git/platform/mrs` | List MR/PR |
| POST | `/api/v1/git/platform/mrs` | Create MR/PR |

### Worktrees

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/v1/worktrees` | List worktrees |
| POST | `/api/v1/worktrees` | Create a worktree |
| GET | `/api/v1/worktrees/:id` | Get a single worktree |
| POST | `/api/v1/worktrees/:id/merge` | Merge worktree branch |
| DELETE | `/api/v1/worktrees/:id` | Remove a worktree |

### Plugins / MCP Forge / Design Market

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/v1/plugins` | List plugins |
| POST | `/api/v1/mcp-forge/generate` | Generate MCP server |
| GET | `/api/v1/design-market/themes` | List design themes |
| GET | `/api/v1/design-market/search` | Search design assets |

### Local LLM Gateway

| Method | Path | Description |
| --- | --- | --- |
| GET | `/llm/openai/v1/models` | OpenAI model list |
| POST | `/llm/openai/v1/chat/completions` | OpenAI chat proxy |
| POST | `/llm/anthropic/v1/messages` | Anthropic messages proxy |

### WebSocket

| Path | Description |
| --- | --- |
| `/ws/terminal` | Terminal PTY WebSocket |
| `/ws/browser` | Browser real-time interaction |

## Error Codes

| Status | Meaning |
| --- | --- |
| 401 | Unauthorized (token missing or invalid) |
| 403 | Forbidden (hardened mode restriction) |
| 404 | Resource not found |
| 429 | Rate limited (30s cooldown) |
| 500 | Internal server error |

## Related Docs

- [ACP Protocol Contract](https://github.com/hexian2001/lingxiao-coding/blob/main/docs/contracts/acp.md)
- [HTTP API Contract](https://github.com/hexian2001/lingxiao-coding/blob/main/docs/contracts/http-api.md)
- [Session Event Contract](https://github.com/hexian2001/lingxiao-coding/blob/main/docs/contracts/session-events.md)
