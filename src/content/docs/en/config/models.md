---
title: Model Configuration
description: Configure Leader and Worker models, compatible providers, and local gateway
---

# Model Configuration

LingXiao allows separate configuration of Leader and Worker LLM models, with support for multiple providers and compatibility layers.

## Configuration Methods

### Environment Variables

```bash
export LINGXIAO_LLM_PROVIDER=openai
export LINGXIAO_LEADER_MODEL=gpt-4o
export LINGXIAO_AGENT_MODEL=gpt-4o-mini
```

### Config File

Edit `~/.lingxiao/settings.json`:

```json
{
  "llm": {
    "provider": "openai",
    "leader_model": "gpt-4o",
    "agent_model": "gpt-4o-mini",
    "enable_streaming": true
  }
}
```

## LLM Config Group

Key settings in the `llm` group:

| Setting | Description |
| --- | --- |
| `provider` | Provider selection: `auto` / `openai` / `anthropic` |
| `leader_model` | Leader model |
| `agent_model` | Worker model |
| `wiki_model` | Wiki knowledge summary model |
| `model_providers` | Provider model registry |
| `gateway_routes` | Multi-model gateway routes |
| `gateway_fallback_models` | Gateway fallback models |
| `request_timeout_s` | Request timeout (seconds) |
| `connect_timeout_s` | Connect timeout (seconds) |
| `max_retries` | Max retry count |
| `backoff_base_ms` | Backoff base milliseconds |
| `context_max_tokens` | Context max tokens |
| `capped_max_tokens` | Capped max tokens |
| `escalated_max_tokens` | Escalated max tokens |
| `thinking_budget_tokens` | Thinking budget tokens |
| `enable_streaming` | Enable streaming output |
| `show_thinking_content` | Show thinking content |
| `enable_thinking_instruction` | Enable thinking instruction |
| `enable_extended_thinking` | Enable extended thinking |
| `reasoning_effort` | Reasoning effort |

## Supported Providers

| Provider | provider value | API format | Notes |
| --- | --- | --- | --- |
| OpenAI | `openai` | OpenAI API | Native support |
| Anthropic | `anthropic` | Anthropic API | Native support |
| DeepSeek | `openai` | OpenAI compatible | Set `LINGXIAO_OPENAI_BASE_URL` |
| Qwen | `openai` | OpenAI compatible | Set `LINGXIAO_OPENAI_BASE_URL` |
| Moonshot/Kimi | `openai` | OpenAI compatible | Set `LINGXIAO_OPENAI_BASE_URL` |
| Gemini | `openai` | OpenAI compat layer | Via compatibility layer |
| Groq | `openai` | OpenAI compatible | Set `LINGXIAO_OPENAI_BASE_URL` |
| SiliconFlow | `openai` | OpenAI compatible | Set `LINGXIAO_OPENAI_BASE_URL` |

### Compatible Provider Examples

DeepSeek example:

```bash
export LINGXIAO_LLM_PROVIDER=openai
export LINGXIAO_OPENAI_API_KEY=sk-your-deepseek-key
export LINGXIAO_OPENAI_BASE_URL=https://api.deepseek.com/v1
export LINGXIAO_LEADER_MODEL=deepseek-chat
export LINGXIAO_AGENT_MODEL=deepseek-chat
```

Qwen example:

```bash
export LINGXIAO_LLM_PROVIDER=openai
export LINGXIAO_OPENAI_API_KEY=sk-your-qwen-key
export LINGXIAO_OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
export LINGXIAO_LEADER_MODEL=qwen-plus
export LINGXIAO_AGENT_MODEL=qwen-turbo
```

## Local LLM Gateway

LingXiao includes a local LLM gateway (`/llm/*` routes) as a unified endpoint, supporting both OpenAI and Anthropic formats.

### Gateway Config

```json
{
  "llm_gateway": {
    "enabled": true,
    "provider": "openai",
    "model": "gpt-4o-mini",
    "inject_env": true,
    "default_rpm": 60,
    "default_tpm": 200000,
    "default_daily_token_budget": 2000000,
    "trace_enabled": true
  }
}
```

### Virtual Keys

The gateway supports virtual key management:

```json
{
  "llm_gateway": {
    "virtual_keys": [
      {
        "id": "key-001",
        "key": "sk-virtual-xxx",
        "label": "Dev Test",
        "enabled": true,
        "model": "gpt-4o-mini",
        "rpm": 30,
        "tpm": 100000,
        "daily_token_budget": 500000
      }
    ]
  }
}
```

Gateway routes authenticate with virtual keys (`Authorization: Bearer <key>` or `x-api-key`), not the server token.

## Leader & Worker Model Strategy

- **Leader model**: Responsible for task decomposition and orchestration decisions; recommend a more capable model
- **Worker model**: Responsible for task execution; can use a more cost-effective model
- **Wiki model**: Used for knowledge summaries; can use a lightweight model

```json
{
  "llm": {
    "leader_model": "gpt-4o",
    "agent_model": "gpt-4o-mini",
    "wiki_model": "gpt-4o-mini"
  }
}
```
