---
title: LLM Gateway
description: OpenAI/Anthropic dual-format LLM proxy
---

# Local LLM Gateway

LingXiao can serve as an OpenAI/Anthropic dual-format LLM proxy.

## Capabilities

- Virtual key management
- Per-key RPM/TPM/daily token budget
- Request trace logging
- Default port: 62000

## Endpoints

| Path | Format |
| --- | --- |
| `/llm/openai/v1/**` | OpenAI compatible |
| `/llm/anthropic/v1/**` | Anthropic compatible |
