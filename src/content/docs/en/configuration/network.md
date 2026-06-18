---
title: Network
description: Web service port and proxy configuration
---

# Network

## Web Service

| Config | Variable | Default |
| --- | --- | --- |
| Host | `LINGXIAO_WEB_HOST` | `127.0.0.1` |
| Port | `LINGXIAO_WEB_PORT` | Auto-assigned |
| Dev Proxy | `LINGXIAO_WEB_PROXY_TARGET` | - |

## Hardened Mode

Auto-enabled on non-loopback binding:
- Query token disabled, header-only
- Rate limit cooldown 30s
- Mandatory token authentication
