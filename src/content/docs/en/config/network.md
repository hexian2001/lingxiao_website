---
title: Network Configuration
description: Web service ports, proxy, and allowed_hosts configuration
---

# Network Configuration

LingXiao's network configuration covers web service, proxy, host allowlist, and hardened mode.

## Web Service

| Config | Environment Variable | Config Path | Default |
| --- | --- | --- | --- |
| Host | `LINGXIAO_WEB_HOST` | `server.host` | `127.0.0.1` |
| Port | `LINGXIAO_WEB_PORT` | `server.port` | Auto-assigned |
| Dev Proxy | `LINGXIAO_WEB_PROXY_TARGET` | - | - |

### Development Mode

```bash
# Start CLI + Web service
LINGXIAO_WEB_PORT=8787 npm run cli

# In another terminal, start Vite dev server
cd web
LINGXIAO_WEB_PROXY_TARGET=http://127.0.0.1:8787 npm run dev
```

## Proxy Configuration

The `network` group controls proxy behavior:

| Setting | Environment Variable | Description |
| --- | --- | --- |
| `network.proxy.url` | `LINGXIAO_PROXY_URL` | Proxy URL |
| `network.proxy.llm_enabled` | `LINGXIAO_PROXY_LLM` | Route LLM requests through proxy |
| `network.proxy.tools_enabled` | `LINGXIAO_PROXY_TOOLS` | Route tool requests through proxy |
| `network.user_agent` | `LINGXIAO_USER_AGENT` | Custom User-Agent |

### Proxy Config Example

```json
{
  "network": {
    "proxy": {
      "url": "http://127.0.0.1:7890",
      "llm_enabled": true,
      "tools_enabled": false
    },
    "user_agent": "LingXiao/0.3"
  }
}
```

## Host Allowlist

`allowedHosts` controls the list of hosts network tools can access:

```json
{
  "allowedHosts": [
    "registry.npmjs.org",
    "api.github.com",
    "pypi.org",
    "127.0.0.1",
    "localhost"
  ]
}
```

Hosts not in the allowlist will be rejected.

## Rate Limiting

| Scenario | Behavior |
| --- | --- |
| In-process self-call | Always exempt |
| Non-hardened localhost | Exempt |
| Hardened mode / non-localhost | Not exempt, 429 triggers cooldown |
| Non-loopback binding without hardened mode | Strong warning (not gated) |

## Hardened Mode

Enable hardened mode for non-loopback bindings:

```bash
export LINGXIAO_HARDENED_MODE=true
```

When hardened mode is enabled:

- **Authentication**: Disables query token, header `x-lingxiao-token` only
- **Rate limiting**: 429 triggers 30-second cooldown
- **Security**: `dangerous_command_guard` and `block_private_network` forced on
- **One-way lock**: Cannot be turned off via API after env var is set

### Insecure Binding Warning

When non-loopback binding is detected without hardened mode, the system outputs a strong warning log but does not prevent startup.

## LLM Gateway Network

Local LLM gateway (port 62000) network behavior:

- Gateway routes authenticate with virtual keys, not server token
- Rate limited per virtual key quota: `rpm` / `tpm` / `daily_token_budget`
- Rate limit hit returns 429 + error body
