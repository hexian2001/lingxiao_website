---
title: 本地 LLM Gateway
description: OpenAI/Anthropic 双格式代理、虚拟密钥、RPM/TPM 限制
---

# 本地 LLM Gateway

凌霄可作为 OpenAI/Anthropic 双格式 LLM 代理，提供虚拟密钥管理、per-key 限流和请求追踪。默认端口 62000。

## 架构

<div class="doc-vertical-flow" role="img" aria-label="LLM Gateway 架构：客户端请求进入 Gateway，完成虚拟密钥和限流检查，转发上游响应，并记录 Trace 到 SQLite。">
  <span>客户端请求</span><i>→</i><strong>LLM Gateway</strong><i>→</i><span>上游 LLM Provider</span>
  <em>虚拟密钥验证 + 限流检查</em>
  <em>请求转发 + 响应代理</em>
  <em>Trace 记录到 SQLite</em>
</div>

## 双格式代理

Gateway 同时支持 OpenAI 和 Anthropic 两种 API 格式：

### OpenAI 格式

```text
POST /llm/openai/v1/chat/completions
Authorization: Bearer <virtual-key>
```

兼容 OpenAI SDK 和所有 OpenAI 格式兼容服务（DeepSeek、Qwen、Moonshot 等）。

### Anthropic 格式

```text
POST /llm/anthropic/v1/messages
x-api-key: <virtual-key>
```

兼容 Anthropic SDK 和 Claude 系列模型。

## 虚拟密钥

Gateway 使用虚拟密钥体系，与上游 Provider 的真实 API Key 隔离：

- **根密钥**：Gateway 主密钥，用于管理虚拟密钥
- **虚拟密钥**：按需生成，绑定限流策略和可用模型
- **密钥管理**：通过 WebUI Settings 面板或 API 管理

### 虚拟密钥属性

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

## 限流策略

| 策略 | 说明 |
| --- | --- |
| `rpm` | 每分钟请求数限制 |
| `tpm` | 每分钟 Token 数限制 |
| `daily_token_budget` | 每日 Token 预算 |

命中限流时返回 HTTP 429 + 错误体：

```json
{
  "error": {
    "type": "rate_limit_exceeded",
    "message": "RPM limit exceeded: 60/min",
    "retry_after": 30
  }
}
```

## 请求追踪

所有请求 trace 记录到 SQLite 的 `llm_gateway_requests` 表：

- 请求时间戳和虚拟密钥
- 上游 Provider 和模型
- Token 用量（prompt/completion/total）
- 延迟和状态码
- 请求体和响应体（可配置）

## 配置

在 `~/.lingxiao/settings.json` 中配置 LLM Gateway：

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

## 鉴权矩阵

| 端点族 | 鉴权方式 |
| --- | --- |
| `/llm/openai/v1/**` | Gateway 虚拟密钥（`Authorization: Bearer` 或 `x-api-key`） |
| `/llm/anthropic/v1/**` | Gateway 虚拟密钥（`x-api-key` 或 `Authorization: Bearer`） |

LLM Gateway 端点不走 Server Token，归 `llm_gateway` 配置组独立管控。
