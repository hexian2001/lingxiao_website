---
title: 模型配置
description: 配置 Leader 和 Worker 模型
---

# 模型配置

凌霄允许分别配置 Leader 和 Worker 使用的模型。

## 配置方式

### 环境变量

```bash
export LINGXIAO_LEADER_MODEL=gpt-4o
export LINGXIAO_AGENT_MODEL=gpt-4o-mini
```

### 配置文件

编辑 `~/.lingxiao/settings.json`：

```json
{
  "llm": {
    "leaderModel": "gpt-4o",
    "agentModel": "gpt-4o-mini"
  }
}
```

## 支持的提供商

| 提供商 | provider 值 | 接口格式 |
| --- | --- | --- |
| OpenAI | `openai` | OpenAI API |
| Anthropic | `anthropic` | Anthropic API |
| DeepSeek | `openai` | OpenAI 兼容 |
| Qwen | `openai` | OpenAI 兼容 |
| Moonshot/Kimi | `openai` | OpenAI 兼容 |
| Gemini | `openai` | OpenAI 兼容层 |
| Groq | `openai` | OpenAI 兼容 |
| SiliconFlow | `openai` | OpenAI 兼容 |

## 本地 LLM Gateway

可使用凌霄内置的本地 LLM 网关（端口 62000）作为统一出口。
