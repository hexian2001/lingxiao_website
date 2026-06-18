---
title: 模型配置
description: 配置 Leader 和 Worker 模型、兼容提供商与本地网关
---

# 模型配置

凌霄允许分别配置 Leader 和 Worker 使用的 LLM 模型，支持多种提供商和兼容层。

## 配置方式

### 环境变量

```bash
export LINGXIAO_LLM_PROVIDER=openai
export LINGXIAO_LEADER_MODEL=gpt-4o
export LINGXIAO_AGENT_MODEL=gpt-4o-mini
```

### 配置文件

编辑 `~/.lingxiao/settings.json`：

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

## LLM 配置组

`llm` 组的关键设置：

| 设置 | 说明 |
| --- | --- |
| `provider` | 提供商选择：`auto` / `openai` / `anthropic` |
| `leader_model` | Leader 使用的模型 |
| `agent_model` | Worker 使用的模型 |
| `wiki_model` | Wiki 知识摘要模型 |
| `model_providers` | 提供商模型注册表 |
| `gateway_routes` | 多模型网关路由 |
| `gateway_fallback_models` | 网关回退模型 |
| `request_timeout_s` | 请求超时（秒） |
| `connect_timeout_s` | 连接超时（秒） |
| `max_retries` | 最大重试次数 |
| `backoff_base_ms` | 退避基准毫秒 |
| `context_max_tokens` | 上下文最大 token |
| `capped_max_tokens` | 限制最大 token |
| `escalated_max_tokens` | 升级最大 token |
| `thinking_budget_tokens` | 思考预算 token |
| `enable_streaming` | 启用流式输出 |
| `show_thinking_content` | 显示思考内容 |
| `enable_thinking_instruction` | 启用思考指令 |
| `enable_extended_thinking` | 启用扩展思考 |
| `reasoning_effort` | 推理力度 |

## 支持的提供商

| 提供商 | provider 值 | 接口格式 | 说明 |
| --- | --- | --- | --- |
| OpenAI | `openai` | OpenAI API | 原生支持 |
| Anthropic | `anthropic` | Anthropic API | 原生支持 |
| DeepSeek | `openai` | OpenAI 兼容 | 设置 `LINGXIAO_OPENAI_BASE_URL` |
| Qwen（通义千问） | `openai` | OpenAI 兼容 | 设置 `LINGXIAO_OPENAI_BASE_URL` |
| Moonshot/Kimi | `openai` | OpenAI 兼容 | 设置 `LINGXIAO_OPENAI_BASE_URL` |
| Gemini | `openai` | OpenAI 兼容层 | 通过兼容层接入 |
| Groq | `openai` | OpenAI 兼容 | 设置 `LINGXIAO_OPENAI_BASE_URL` |
| SiliconFlow | `openai` | OpenAI 兼容 | 设置 `LINGXIAO_OPENAI_BASE_URL` |

### 兼容层配置示例

以 DeepSeek 为例：

```bash
export LINGXIAO_LLM_PROVIDER=openai
export LINGXIAO_OPENAI_API_KEY=sk-your-deepseek-key
export LINGXIAO_OPENAI_BASE_URL=https://api.deepseek.com/v1
export LINGXIAO_LEADER_MODEL=deepseek-chat
export LINGXIAO_AGENT_MODEL=deepseek-chat
```

以 Qwen 为例：

```bash
export LINGXIAO_LLM_PROVIDER=openai
export LINGXIAO_OPENAI_API_KEY=sk-your-qwen-key
export LINGXIAO_OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
export LINGXIAO_LEADER_MODEL=qwen-plus
export LINGXIAO_AGENT_MODEL=qwen-turbo
```

## 本地 LLM 网关

凌霄内置本地 LLM 网关（`/llm/*` 路由），可作为统一出口，支持 OpenAI 和 Anthropic 格式。

### 网关配置

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

### 虚拟 Key

网关支持虚拟 Key 管理：

```json
{
  "llm_gateway": {
    "virtual_keys": [
      {
        "id": "key-001",
        "key": "sk-virtual-xxx",
        "label": "开发测试",
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

网关路由使用虚拟 Key 鉴权（`Authorization: Bearer <key>` 或 `x-api-key`），不走 server token。

## Leader 与 Worker 模型策略

- **Leader 模型**：负责任务分解、编排决策，建议使用能力更强的模型
- **Worker 模型**：负责任务执行，可使用性价比更高的模型
- **Wiki 模型**：用于知识摘要，可使用轻量模型

```json
{
  "llm": {
    "leader_model": "gpt-4o",
    "agent_model": "gpt-4o-mini",
    "wiki_model": "gpt-4o-mini"
  }
}
```
