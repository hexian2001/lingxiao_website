---
title: Permission System
description: strict/dev/networked/yolo four-tier permission modes and tool whitelists
---

# Permission System

LingXiao's permission system controls Agent tool execution permissions, supporting four permission modes and fine-grained rules.

## Permission Modes

| Mode | Label | Description |
| --- | --- | --- |
| `strict` | strict | Strictest mode, all write operations require confirmation |
| `dev` | standard | Development mode, standard permission control |
| `networked` | approved | Network mode, network tools require approval |
| `yolo` | yolo | Most permissive mode, auto-approve (default) |

Default permission mode is `yolo`, configured via `security.permission_mode`.

### Setting Permission Mode

```bash
# Environment variable (hardened mode one-way lock)
export LINGXIAO_HARDENED_MODE=true
```

```json
{
  "security": {
    "permission_mode": "dev"
  }
}
```

### Sandbox Backend

| Mode | Sandbox Backend | Description |
| --- | --- | --- |
| `yolo` | `app-guard` | Lightweight sandbox |
| Other modes | `bubblewrap` | Hardened sandbox |

Backend fallback is enabled by default (`allowBackendFallback: true`).

## Permission Context

`ToolPermissionContext` is the durable policy object:

```ts
interface ToolPermissionContext {
  mode: 'strict' | 'dev' | 'networked' | 'yolo';
  allowedHosts: string[];
  sandboxBackend: 'app-guard' | 'bubblewrap';
  allowBackendFallback: boolean;
  allowRules: Array<{ toolName: string; pattern?: string }>;
  denyRules: Array<{ toolName: string; pattern?: string }>;
  askRules: Array<{ toolName: string; pattern?: string }>;
}
```

## Persistence Layers

Effective permissions merge in this order (later layers override earlier):

| Layer | File | Description |
| --- | --- | --- |
| `user` | `~/.lingxiao/permissions.user.json` | User level |
| `project` | `<workspace>/.lingxiao/permissions.project.json` | Project level |
| `local` | `<workspace>/.lingxiao/permissions.local.json` | Local level |
| `session` | SQLite `session_state` | Session level |

## Tool Rules

Three rule types control tool execution:

### Allow Rules

Auto-approve matching tool calls:

```json
{
  "allowRules": [
    { "toolName": "file_read", "pattern": "src/**" },
    { "toolName": "code_search" }
  ]
}
```

### Deny Rules

Reject matching tool calls:

```json
{
  "denyRules": [
    { "toolName": "shell", "pattern": "rm -rf *" }
  ]
}
```

### Ask Rules

Require user confirmation before execution:

```json
{
  "askRules": [
    { "toolName": "file_create", "pattern": "*.env" },
    { "toolName": "shell", "pattern": "npm publish" }
  ]
}
```

### Rule Precedence

deny > ask > allow. When the same tool matches multiple rules, deny takes precedence.

## Network Host Allowlist

`allowedHosts` controls which hosts network tools can access:

```json
{
  "allowedHosts": [
    "registry.npmjs.org",
    "api.github.com",
    "127.0.0.1"
  ]
}
```

## Security Config

Key settings in the `security` group:

| Setting | Default | Description |
| --- | --- | --- |
| `permission_mode` | `yolo` | Permission mode |
| `auto_allow_bash_if_sandboxed` | `true` | Auto-allow bash in sandbox |
| `dangerous_command_guard` | `false` | Dangerous command interception |
| `block_private_network` | `false` | Block private network access |
| `identity_judge_llm_enabled` | `false` | LLM identity second pass |
| `hardened_mode` | `false` | Hardened mode |
| `env_allowlist` | `[]` | Subprocess env allowlist |

### Hardened Mode

When hardened mode is enabled:

- Disables query token, header-only authentication
- Rate limit cooldown 30 seconds
- Forces token authentication
- `dangerous_command_guard` and `block_private_network` are forced on
- `LINGXIAO_HARDENED_MODE` environment variable is a one-way lock; cannot be turned off via API

## Permission Requests & Approvals

When a tool call matches an `ask` rule or a write operation in non-`yolo` mode, the system initiates a permission request:

1. **Request**: `permission:request` event broadcast to WebUI
2. **Approval**: User confirms or rejects in WebUI
3. **Result**: `permission:resolved` event returns the decision

### Permissions in Eternal Mode

- Non-`yolo` permission requests may be auto-approved
- `yolo` requests still require user confirmation
- Eternal mode replays pending non-`yolo` requests on enable

## Audit Log

Permission audit records are appended to `session_state` under `PERMISSION_AUDIT_LOG`, retaining the most recent records.
