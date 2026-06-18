---
title: API 契约索引
description: HTTP REST / SSE / WebSocket / ACP JSON-RPC 端点索引
---

# API 契约索引

凌霄 Fastify 服务器对外暴露 HTTP REST + SSE + WebSocket + ACP JSON-RPC 全部端点。共注册 207 个路由，由 `src/server.ts` 装配，25 个 `src/web-server/*Routes.ts` 文件分模块注册。

## 鉴权矩阵

| 端点族 | 鉴权方式 | 说明 |
| --- | --- | --- |
| `/health`、`/*`（静态 web）、`/api/v1/acp/connect` | 公开 / 静态 / 无鉴权 | connect 阶段获取 connectionId + sessionToken |
| `/api/v1/**`（除 acp/connect 与 /llm/*） | server token | header `x-lingxiao-token` 或 `?token=` query；加固模式仅 header |
| `/api/v1/acp`（GET SSE / POST JSON-RPC） | server token + ACP 凭据 | header `acp-connection-id` + `acp-session-token` |
| `/llm/openai/v1/**`、`/llm/anthropic/v1/**` | gateway virtual key | header `Authorization: Bearer <key>` 或 `x-api-key` |
| `/api/v1/storage` PUT | server token | 写后立即落 `session_state` |

## 限流与加固

- 进程内自调用（无 remoteAddress）→ 始终豁免
- 非加固模式 localhost（127.0.0.1/::1）→ 豁免
- 加固模式 / 非 localhost → 不豁免，429 触发冷却
- 非 loopback 绑定且未加固 → 强警告，不门控

## 端点分组索引

### Health / Static

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/health` | 健康探测，公开 |
| GET | `/*` | 静态 Web 资源 + SPA fallback |

### ACP 协议

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/v1/acp/connect` | 获取 connectionId + sessionToken |
| GET | `/api/v1/acp` | SSE 连接（需 ACP 凭据） |
| POST | `/api/v1/acp` | JSON-RPC 请求（需 ACP 凭据） |
| DELETE | `/api/v1/acp` | 断开 ACP 连接 |

ACP JSON-RPC 方法包括：`session/send`、`session/command`、`session/interrupt`、`session/hydrate` 等。

### Sessions

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/sessions` | 列出所有会话 |
| POST | `/api/sessions` | 创建新会话 |
| GET | `/api/v1/sessions/active` | 获取活跃会话 |
| POST | `/api/v1/sessions/side-thread` | 创建侧线程 |

### Settings / Model / Prompt

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/settings` | 获取设置（脱敏） |
| PUT | `/api/v1/settings` | 更新设置 |
| GET | `/api/v1/model/list` | 列出已配置模型 |
| PUT | `/api/v1/model` | 更新 Leader 模型 |
| GET | `/api/v1/prompt/list` | 列出可用 prompt |
| GET | `/api/v1/intuition` | 获取直觉运行时状态 |

### Roles / Commands

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/roles` | 列出角色定义 |
| GET | `/api/v1/commands` | 列出 slash 命令注册表 |

### Tasks / Workflow

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/tasks` | 列出任务 |
| POST | `/api/v1/tasks` | 创建任务 |
| GET | `/api/v1/workflow/state` | 工作流状态 |
| POST | `/api/v1/workflow/toggle` | 切换工作流模式 |

### Stats / Storage

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/stats` | 会话统计 |
| GET | `/api/v1/storage` | 读取 session_state 键 |
| PUT | `/api/v1/storage` | 写入 session_state 键 |

### Files / Wiki / Git

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/files` | 列出工作区文件 |
| GET | `/api/v1/files/content` | 读取文件内容 |
| GET | `/api/v1/wiki` | Wiki 页面列表 |
| GET | `/api/v1/git/status` | Git 状态 |
| POST | `/api/v1/git/init` | 初始化仓库 |
| GET | `/api/v1/git/platform/info` | 平台集成信息 |
| GET | `/api/v1/git/platform/mrs` | 列出 MR/PR |
| POST | `/api/v1/git/platform/mrs` | 创建 MR/PR |

### Worktrees

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/worktrees` | 列出 worktree |
| POST | `/api/v1/worktrees` | 创建 worktree |
| GET | `/api/v1/worktrees/:id` | 获取单个 worktree |
| POST | `/api/v1/worktrees/:id/merge` | 合并 worktree 分支 |
| DELETE | `/api/v1/worktrees/:id` | 删除 worktree |

### Plugins / MCP Forge / Design Market

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/plugins` | 列出插件 |
| POST | `/api/v1/mcp-forge/generate` | 生成 MCP 服务器 |
| GET | `/api/v1/design-market/themes` | 列出设计主题 |
| GET | `/api/v1/design-market/search` | 搜索设计素材 |

### Local LLM Gateway

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/llm/openai/v1/models` | OpenAI 模型列表 |
| POST | `/llm/openai/v1/chat/completions` | OpenAI chat 代理 |
| POST | `/llm/anthropic/v1/messages` | Anthropic messages 代理 |

### WebSocket

| 路径 | 说明 |
| --- | --- |
| `/ws/terminal` | 终端 PTY WebSocket |
| `/ws/browser` | 浏览器实时交互 |

## 错误码

| 状态码 | 含义 |
| --- | --- |
| 401 | 未授权（token 缺失或无效） |
| 403 | 禁止访问（加固模式限制） |
| 404 | 资源不存在 |
| 429 | 限流触发（冷却期 30s） |
| 500 | 服务器内部错误 |

## 相关文档

- [ACP 协议契约](https://github.com/hexian2001/lingxiao/blob/main/docs/contracts/acp.md)
- [HTTP API 契约](https://github.com/hexian2001/lingxiao/blob/main/docs/contracts/http-api.md)
- [Session 事件契约](https://github.com/hexian2001/lingxiao/blob/main/docs/contracts/session-events.md)
