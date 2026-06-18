---
title: 全状态同步
description: session_runtime_state、SSE、ACP 与 WebUI/TUI 三端同步
---

# 全状态同步

凌霄把 WebUI、TUI 和后端运行时收拢到统一状态链路，所有运行态都进入同一个工程内核，三端实时同步。

## 同步架构

<div class="doc-vertical-flow" role="img" aria-label="状态同步架构：SessionManager 生成 session runtime state，经 SseBridge 和 ACP 推送到 Web sessionStore 与 TUI event bridge。">
  <strong>SessionManager</strong>
  <em>session:runtime_state</em>
  <em>SseBridge</em>
  <em>ACP session/update: session_runtime_state</em>
  <em>Web sessionStore / TUI event bridge</em>
</div>

`session:runtime_state` 是统一运行态快照，覆盖 session status、leader busy/waiting/reviewing 状态、任务图、agent 面板、工具调用日志、消息流和审查结果。

## 同步通道

### SSE 事件流

Server-Sent Events 推送实时状态变更到 WebUI：

```text
GET /api/v1/events?token=<server_token>
Content-Type: text/event-stream
```

WebUI 通过 EventSource 连接接收推送，无需轮询。

### ACP JSON-RPC

Agent Communication Protocol 提供双向通信通道：

```text
GET  /api/v1/acp          # SSE 事件流
POST /api/v1/acp           # JSON-RPC 请求
DELETE /api/v1/acp         # 断开连接
```

ACP 连接需要 `acp-connection-id` + `acp-session-token` 双重凭据。

### SQLite 持久化

所有状态持久化到 SQLite 数据库，包括：
- 会话元数据和状态
- 任务图和执行历史
- 消息和对话记录
- Agent 状态和日志
- 工具调用全链路
- Token 使用统计

## 同步内容

| 类别 | 同步事件 |
| --- | --- |
| 任务生命周期 | 创建、更新、派发、完成、失败、阻塞 |
| Agent 状态 | 启动、心跳、退出、结果回执 |
| 工具调用 | 参数、权限评估、输出、耗时 |
| 代码变更 | 文件 diff、Git 操作 |
| 消息流转 | Leader-Worker 通信、团队消息 |
| 审查结果 | Review verdict、证据、建议 |
| 错误和阻塞 | 异常、超时、依赖阻塞 |

## 事件类型

22 种 `SessionUpdateKind` 事件覆盖全部运行态变更：

```typescript
enum SessionUpdateKind {
  // 任务事件
  task_created, task_updated, task_dispatched,
  task_completed, task_failed, task_blocked,
  // Agent 事件
  agent_started, agent_heartbeat, agent_exited,
  agent_result,
  // 工具事件
  tool_call_started, tool_call_completed,
  // 消息事件
  message_sent, message_received,
  // 审查事件
  review_requested, review_completed,
  // 会话事件
  session_status_changed, session_error,
  // 其他
  code_changed, git_operation, error, blocked
}
```

## 会话恢复

```bash
# 恢复指定会话
lingxiao --session <session_id>

# 列出所有会话
lingxiao list
```

崩溃或中断后，从 SQLite 恢复完整运行态：
- DAG 结构和任务状态重建
- Agent 上下文恢复
- 消息历史和工具调用日志保留
- 未完成任务可继续执行

## 鉴权

| 端点族 | 鉴权方式 |
| --- | --- |
| `/health`、静态资源 | 公开 |
| `/api/v1/**` | Server Token（header `x-lingxiao-token`） |
| `/api/v1/acp` | Server Token + ACP 凭据 |
| `/llm/**` | LLM Gateway 虚拟密钥 |

加固模式下，Server Token 仅接受 header 形式，禁用 query 参数传递。
