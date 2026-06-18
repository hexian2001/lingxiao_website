---
title: Connect Models
description: Configure LLM providers and models
---

# Connect Models

LingXiao supports multiple LLM providers, configured via environment variables or config files.

## Supported Providers

- **OpenAI** (and compatible: DeepSeek, Qwen, Moonshot/Kimi, Gemini, Groq, SiliconFlow, etc.)
- **Anthropic**

## Environment Variables

| Variable | Description |
| --- | --- |
| `LINGXIAO_LLM_PROVIDER` | `auto` / `openai` / `anthropic` |
| `LINGXIAO_OPENAI_API_KEY` | OpenAI or compatible API key |
| `LINGXIAO_OPENAI_BASE_URL` | OpenAI compatible endpoint |
| `LINGXIAO_ANTHROPIC_API_KEY` | Anthropic key |
| `LINGXIAO_ANTHROPIC_BASE_URL` | Anthropic endpoint |
| `LINGXIAO_LEADER_MODEL` | Leader model |
| `LINGXIAO_AGENT_MODEL` | Worker model |

## Config File

Edit `~/.lingxiao/settings.json`:

```json
{
  "llm": {
    "provider": "openai",
    "openai": {
      "apiKey": "sk-xxx",
      "baseUrl": "https://api.openai.com/v1"
    },
    "leader_model": "gpt-4o",
    "agent_model": "gpt-4o-mini"
  }
}
```

## Using Compatible Endpoints

DeepSeek example:

```bash
export LINGXIAO_LLM_PROVIDER=openai
export LINGXIAO_OPENAI_API_KEY=sk-xxx
export LINGXIAO_OPENAI_BASE_URL=https://api.deepseek.com/v1
export LINGXIAO_LEADER_MODEL=deepseek-chat
export LINGXIAO_AGENT_MODEL=deepseek-chat
```

Anthropic example:

```bash
export LINGXIAO_LLM_PROVIDER=anthropic
export LINGXIAO_ANTHROPIC_API_KEY=sk-ant-xxx
export LINGXIAO_LEADER_MODEL=claude-sonnet-4-20250514
export LINGXIAO_AGENT_MODEL=claude-sonnet-4-20250514
```

## Local LLM Gateway

LingXiao includes a local LLM gateway that serves as an OpenAI/Anthropic dual-format proxy:

- Virtual key management
- Per-key RPM/TPM/daily token budget rate limiting
- Request trace logging to `llm_gateway_requests` table
- Default port: 62000

Enable in `~/.lingxiao/settings.json`:

```json
{
  "llm_gateway": {
    "enabled": true,
    "provider": "openai",
    "model": "gpt-4o",
    "default_rpm": 60,
    "default_tpm": 200000,
    "trace_enabled": true
  }
}
```

## Next Steps

- [First Run](./first-run) — Launch your first expert panel
