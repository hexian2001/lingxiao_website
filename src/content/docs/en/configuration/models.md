---
title: Models
description: Configure Leader and Worker models
---

# Model Configuration

LingXiao allows separate model configuration for Leader and Workers.

## Environment Variables

```bash
export LINGXIAO_LEADER_MODEL=gpt-4o
export LINGXIAO_AGENT_MODEL=gpt-4o-mini
```

## Config File

Edit `~/.lingxiao/settings.json`:

```json
{
  "llm": {
    "leaderModel": "gpt-4o",
    "agentModel": "gpt-4o-mini"
  }
}
```

## Supported Providers

OpenAI, Anthropic, DeepSeek, Qwen, Moonshot/Kimi, Gemini, Groq, SiliconFlow.
