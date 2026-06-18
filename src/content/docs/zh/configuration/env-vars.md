---
title: 环境变量
description: LINGXIAO_ 前缀环境变量速查
---

# 环境变量

凌霄通过 `LINGXIAO_` 前缀环境变量进行配置，也可在 `~/.lingxiao/settings.json` 中设置。

## 常用环境变量

| 变量 | 说明 |
| --- | --- |
| `LINGXIAO_LLM_PROVIDER` | `auto` / `openai` / `anthropic` |
| `LINGXIAO_OPENAI_API_KEY` | OpenAI 或兼容接口 key |
| `LINGXIAO_OPENAI_BASE_URL` | OpenAI 兼容接口地址 |
| `LINGXIAO_ANTHROPIC_API_KEY` | Anthropic key |
| `LINGXIAO_ANTHROPIC_BASE_URL` | Anthropic 接口地址 |
| `LINGXIAO_LEADER_MODEL` | Leader 模型 |
| `LINGXIAO_AGENT_MODEL` | Worker 模型 |
| `LINGXIAO_WEB_HOST` | Web 服务 host |
| `LINGXIAO_WEB_PORT` | Web 服务端口 |
| `LINGXIAO_WEB_PROXY_TARGET` | Vite 开发代理目标 |

## 兼容提供商

支持 OpenAI、Anthropic，以及 DeepSeek、Qwen、Moonshot/Kimi、Gemini 兼容层、Groq、SiliconFlow 等 OpenAI 格式兼容服务。
