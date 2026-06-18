---
title: Local LLM Gateway
description: OpenAI/Anthropic dual-format proxy, virtual keys, RPM/TPM limits
---

# Local LLM Gateway

LingXiao can serve as an OpenAI/Anthropic dual-format LLM proxy, providing virtual key management, per-key rate limiting, and request tracing. Default port: 62000.

## Architecture

<div class="doc-vertical-flow" role="img" aria-label="LLM Gateway architecture: client requests enter the Gateway, virtual key and rate limit checks run, requests are proxied upstream, and traces are recorded to SQLite.">
  <span>Client Request</span><i>→</i><strong>LLM Gateway</strong><i>→</i><span>Upstream LLM Provider</span>
  <em>Virtual Key Validation + Rate Limit Check</em>
  <em>Request Forwarding + Response Proxy</em>
  <em>Trace Recording to SQLite</em>
</div>

## Dual-Format Proxy

The Gateway supports both OpenAI and Anthropic API formats simultaneously:

### OpenAI Format

```text
POST /llm/openai/v1/chat/completions
Authorization: Bearer <virtual-key>
```

Compatible with OpenAI SDK and all OpenAI-format compatible services (DeepSeek, Qwen, Moonshot, etc.).

### Anthropic Format

```text
POST /llm/anthropic/v1/messages
x-api-key: <virtual-key>
```

Compatible with Anthropic SDK and Claude model family.

## Virtual Keys

The Gateway uses a virtual key system, isolated from the upstream Provider's real API keys:

- **Root key**: Gateway master key for managing virtual keys
- **Virtual keys**: Generated on demand, bound to rate limit policies and allowed models
- **Key management**: Via WebUI Settings panel or API

### Virtual Key Properties

```json
{
  "key": "sk-lx-xxxxxxxx",
  "name": "dev-team-key",
  "rpm": 60,
  "tpm": 200000,
  "daily_token_budget": 1000000,
  "allowed_models": ["gpt-4o", "claude-sonnet-4"],
  "trace_enabled": true
}
```

## Rate Limiting

| Policy | Description |
| --- | --- |
| `rpm` | Requests per minute limit |
| `tpm` | Tokens per minute limit |
| `daily_token_budget` | Daily token budget |

When rate limited, returns HTTP 429 + error body:

```json
{
  "error": {
    "type": "rate_limit_exceeded",
    "message": "RPM limit exceeded: 60/min",
    "retry_after": 30
  }
}
```

## Request Tracing

All request traces are recorded to the SQLite `llm_gateway_requests` table:

- Request timestamp and virtual key
- Upstream Provider and model
- Token usage (prompt/completion/total)
- Latency and status code
- Request and response bodies (configurable)

## Configuration

Configure LLM Gateway in `~/.lingxiao/settings.json`:

```json
{
  "llm_gateway": {
    "enabled": true,
    "port": 62000,
    "provider": "openai",
    "upstream": {
      "openai_api_key": "sk-xxx",
      "openai_base_url": "https://api.openai.com/v1",
      "anthropic_api_key": "sk-ant-xxx"
    },
    "default_rpm": 60,
    "default_tpm": 200000,
    "default_daily_budget": 1000000,
    "trace_enabled": true,
    "log_body": false
  }
}
```

## Authentication Matrix

| Endpoint group | Auth method |
| --- | --- |
| `/llm/openai/v1/**` | Gateway virtual key (`Authorization: Bearer` or `x-api-key`) |
| `/llm/anthropic/v1/**` | Gateway virtual key (`x-api-key` or `Authorization: Bearer`) |

LLM Gateway endpoints do not use Server Token; they are governed by the `llm_gateway` configuration group independently.
