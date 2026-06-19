---
title: 连接模型
description: 配置 LLM 提供商和模型
---

# 连接模型

凌霄支持多种 LLM 提供商，通过环境变量或配置文件进行设置。

## 支持的提供商

- **OpenAI**（及兼容接口：DeepSeek、Qwen、Moonshot/Kimi、Gemini、Groq、SiliconFlow 等）
- **Anthropic**

## 环境变量配置

| 变量 | 说明 |
| --- | --- |
| `LINGXIAO_LLM_PROVIDER` | `auto` / `openai` / `anthropic` |
| `LINGXIAO_OPENAI_API_KEY` | OpenAI 或兼容接口 key |
| `LINGXIAO_OPENAI_BASE_URL` | OpenAI 兼容接口地址 |
| `LINGXIAO_ANTHROPIC_API_KEY` | Anthropic key |
| `LINGXIAO_ANTHROPIC_BASE_URL` | Anthropic 接口地址 |
| `LINGXIAO_LEADER_MODEL` | Leader 模型 |
| `LINGXIAO_AGENT_MODEL` | Worker 模型 |

## 配置文件方式

编辑 `~/.lingxiao/settings.json`：

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

## 使用兼容接口

以 DeepSeek 为例：

```bash
export LINGXIAO_LLM_PROVIDER=openai
export LINGXIAO_OPENAI_API_KEY=sk-xxx
export LINGXIAO_OPENAI_BASE_URL=https://api.deepseek.com/v1
export LINGXIAO_LEADER_MODEL=deepseek-chat
export LINGXIAO_AGENT_MODEL=deepseek-chat
```

以 Anthropic 为例：

```bash
export LINGXIAO_LLM_PROVIDER=anthropic
export LINGXIAO_ANTHROPIC_API_KEY=sk-ant-xxx
export LINGXIAO_LEADER_MODEL=claude-sonnet-4-20250514
export LINGXIAO_AGENT_MODEL=claude-sonnet-4-20250514
```

## 本地 LLM Gateway

凌霄自带本地 LLM 网关，可作为 OpenAI/Anthropic 双格式代理：

- 虚拟密钥管理
- per-key RPM/TPM/daily token budget 限流
- 请求 trace 记录到 `llm_gateway_requests` 表
- 默认端口 62000

在 `~/.lingxiao/settings.json` 中启用：

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

## 下一步

- [第一次运行](first-run) — 启动你的第一个专家团
