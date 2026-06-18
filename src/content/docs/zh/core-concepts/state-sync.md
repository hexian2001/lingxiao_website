---
title: 全状态同步
description: WebUI/TUI/CLI 三端实时同步
---

# 全状态同步

所有运行态都进入同一工程内核，三端实时同步。

## 同步通道

- **SSE 事件流**：Server-Sent Events 推送实时状态
- **ACP JSON-RPC**：Agent Communication Protocol 双向通信
- **SQLite 持久化**：所有状态持久化到数据库

## 同步内容

- 任务生命周期事件（创建/更新/派发/完成）
- Agent 状态变更（启动/心跳/退出/结果回执）
- 工具调用全链路（参数/权限/输出/耗时）
- 代码变更（文件 diff 和 Git 操作）
- 会话状态（可恢复）

## 事件类型

22 种 SessionUpdateKind 事件覆盖全部运行态变更，包括：

- 任务状态变更
- Agent 生命周期
- 工具调用日志
- 消息流转
- 审查结果
- 错误和阻塞

## 会话恢复

```bash
lingxiao --session <session_id>
```

崩溃后可从 SQLite 恢复完整运行态。
