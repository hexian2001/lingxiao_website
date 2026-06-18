---
title: Environment Variables
description: LINGXIAO_ prefix environment variable reference
---

# Environment Variables

LingXiao is configured via `LINGXIAO_` prefix environment variables or `~/.lingxiao/settings.json`.

| Variable | Description |
| --- | --- |
| `LINGXIAO_LLM_PROVIDER` | `auto` / `openai` / `anthropic` |
| `LINGXIAO_OPENAI_API_KEY` | OpenAI or compatible API key |
| `LINGXIAO_OPENAI_BASE_URL` | OpenAI compatible endpoint |
| `LINGXIAO_ANTHROPIC_API_KEY` | Anthropic key |
| `LINGXIAO_ANTHROPIC_BASE_URL` | Anthropic endpoint |
| `LINGXIAO_LEADER_MODEL` | Leader model |
| `LINGXIAO_AGENT_MODEL` | Worker model |
| `LINGXIAO_WEB_HOST` | Web service host |
| `LINGXIAO_WEB_PORT` | Web service port |
| `LINGXIAO_WEB_PROXY_TARGET` | Vite dev proxy target |
