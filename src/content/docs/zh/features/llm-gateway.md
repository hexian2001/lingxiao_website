---
title: 本地LLM Gateway
description: OpenAI/Anthropic 双格式 LLM 代理
---

# 本地 LLM Gateway

凌霄可作为 OpenAI/Anthropic 双格式 LLM 代理。

## 核心能力

- **虚拟密钥管理**：创建和管理多个虚拟 API key
- **per-key 限流**：RPM / TPM / daily token budget
- **请求 trace**：记录到 `llm_gateway_requests` 表
- **默认端口**：62000

## 端点

| 路径 | 格式 | 说明 |
| --- | --- | --- |
| `/llm/openai/v1/**` | OpenAI | 兼容 OpenAI SDK |
| `/llm/anthropic/v1/**` | Anthropic | 兼容 Anthropic SDK |

## 鉴权

使用 gateway virtual key，通过 `Authorization: Bearer <key>` 或 `x-api-key` 传递。

不走 server token，归 `llm_gateway` 配置组管控。

## 限流

| 维度 | 说明 |
| --- | --- |
| rpm | 每分钟请求数 |
| tpm | 每分钟 token 数 |
| daily_token_budget | 每日 token 预算 |

命中限流返回 429 + 错误体。
