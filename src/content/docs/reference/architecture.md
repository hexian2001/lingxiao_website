---
title: 架构概览
description: 运行时拓扑、模块职责、控制/数据流与失败边界
---

# 架构概览

凌霄是一个基于 Node.js 24、TypeScript、React、Fastify、SQLite 的 AI 工程编排运行时。后端源码根目录为 `src/`，WebUI 源码根目录为 `web/src`。

## 运行时拓扑

```text
flowchart LR
  User["用户"]
  CLI["CLI/TUI<br/>src/cli.ts"]
  Web["React Web UI<br/>web/src"]
  Server["Fastify Web Server<br/>src/server.ts"]
  ACP["ACP JSON-RPC + SSE<br/>AcpRoutes + AcpHandler"]
  Sessions["SessionManager + SessionRuntime<br/>src/runtime"]
  Leader["LeaderAgent<br/>src/agents"]
  DAG["TaskBoard / Orchestration DAG<br/>OrchestrationRuntime"]
  Workers["Worker Expert Agents<br/>AgentPool"]
  Tools["ToolRegistry<br/>src/tools"]
  DB["SQLite<br/>DatabaseManager"]
  RuntimeState["session:runtime_state<br/>统一快照"]
  Browser["BrowserRuntime"]
  Terminal["Terminal WS/PTY"]
  Memory["Memory System<br/>FTS5 + AutoDream"]
  Skills["Skills Catalog<br/>Phase Loader"]
  McpForge["MCP Forge<br/>Server Generation"]
  Eternal["Eternal Loop<br/>Autonomous Mode"]
  Gateway["Local LLM Gateway<br/>OpenAI/Anthropic Proxy"]

  User --> CLI
  User --> Web
  CLI --> Sessions
  Web --> Server
  Server --> ACP
  Server --> DB
  Server --> Gateway
  ACP --> Sessions
  Sessions --> Leader
  Sessions --> RuntimeState
  Sessions --> Eternal
  RuntimeState --> ACP
  Leader --> DAG
  Leader --> Workers
  Leader --> Memory
  Workers --> Skills
  DAG --> DB
  Leader --> Tools
  Workers --> Tools
  Sessions --> DB
  Tools --> DB
  Tools --> McpForge
  Server --> Browser
  Server --> Terminal
```

## 核心进程

### CLI/TUI

主入口：`src/cli.ts`。

CLI 可以运行交互式会话，也可以创建带有相同 `DatabaseManager` 和 `SessionManager` 依赖的 Web 服务器。启动时打印带 token 的 URL，并将端口写入 `~/.lingxiao/port`。

启动时还初始化：
- 记忆维护管道（`runDueMemoryMaintenance`）
- 内置技能同步到全局技能目录

### Web Server

主入口：`src/server.ts`。

职责：
- 创建 Fastify 服务器，注册 `@fastify/websocket`
- 创建共享运行时服务：`DatabaseManager`、`SessionManager`、`EventEmitter`、`ConnectionManager`、`SseBridge`、`AcpHandler`、浏览器运行时、文件/wiki/git API
- 注册 MCP Forge 路由和 MCP Share 路由
- 当 `llm_gateway.enabled` 为 true 时注册本地 LLM Gateway 路由
- 向 HTML 注入 `window.__LINGXIAO_TOKEN__`
- 从 `dist/web` 或开发回退路径提供 Web 资源

### Web UI

主入口：`web/src`。

UI 是状态驱动的，使用 Zustand stores：
- REST 端点用于列出会话、设置、文件、Git、插件、任务、工作流、统计、wiki、MCP Forge/Share、设计市场等
- ACP JSON-RPC 用于会话操作
- SSE 通过 ACP 连接用于实时状态推送

## 核心组件

| 组件 | 职责 |
| --- | --- |
| SessionManager | 会话生命周期管理：创建、恢复、消息分发 |
| SessionRuntime | 运行时上下文：Leader 句柄、Agent 池、工具注册表 |
| LeaderAgent | 总指挥：拆解任务、建 DAG、调度 Worker、验收结果 |
| TaskBoard / DAG | 任务图管理：依赖关系、并行调度、阻塞/解除 |
| AgentPool | Worker 进程池：spawn、回收、心跳监控 |
| ToolRegistry | 工具注册和调用：100+ 内置工具 + MCP 工具 |
| SQLite DB | 持久化存储：会话、消息、任务、Agent 状态、记忆 |
| RuntimeState | 统一快照：`session:runtime_state` 三端同步源 |
| Memory System | 持久记忆：FTS5 全文搜索 + BM25 评分 + AutoDream |
| Skills Catalog | 技能目录：Phase Loader 按需注入 Agent 上下文 |
| MCP Forge | MCP 服务器生成引擎：从描述生成 stdio/http MCP server |
| Eternal Loop | 自治模式：IDLE → CHECK → PATROL → THINK → WAIT 循环 |
| Local LLM Gateway | 本地 LLM 网关：OpenAI/Anthropic 双格式代理 |

## 控制流

### 交互模式

1. 用户通过 TUI/WebUI 发送目标
2. `SessionManager` 创建会话，启动 `SessionRuntime`
3. `LeaderAgent` 接收目标，拆解为 DAG 任务图
4. `OrchestrationRuntime` 管理任务生命周期：分配 Worker、监控执行、提取验收结论
5. Worker 通过 `ToolRegistry` 调用工具执行任务
6. 结果和状态写入 SQLite，通过 `RuntimeState` 推送到三端

### Eternal 自治模式

1. `EternalLoop` 按 30 秒基础间隔（可配置）循环
2. CHECK 阶段检查目标状态和待办任务
3. SKIP/PATROL：无任务时跳过或巡逻检查
4. THINK：有任务时驱动 Leader 执行
5. WAIT：等待执行完成后回到 IDLE
6. 指数退避：连续无操作时间隔翻倍，最大 960 秒
7. 预算熔断：连续 8 次失败自动暂停

## 数据流

### 消息流

```
用户输入 → SessionManager.sendUserInput → LeaderAgent.processGoal
  → TaskBoard.createTask (DAG) → AgentPool.spawnWorker
  → Worker.execute → ToolRegistry.invoke → 结果写入 DB
  → RuntimeState.update → SSE/ACP 推送到三端
```

### 状态同步

凌霄通过 `session:runtime_state` 实现三端（TUI/WebUI/CLI）实时状态同步：

- **SSE**：Server-Sent Events，单向推送会话状态变更
- **ACP JSON-RPC**：双向往返，WebUI 通过 ACP 连接发送命令和接收结果
- **WebSocket**：终端 PTY 和浏览器实时交互

## 编排与验收

### 编排运行时

`OrchestrationRuntime` 订阅任务生命周期事件，提供：

- **验收结论提取**：从任务结果、Worker 报告和评估载荷中解析 `PASS`/`FAIL`/`BLOCKED`/`UNKNOWN`
- **默认最小评估策略**：无显式 `evaluationPolicy` 的任务自动获得 `required_evidence` + `max_repair: 1`
- **后续任务创建**：`FAIL`/`BLOCKED` 且修复预算剩余时，创建修复任务并阻塞依赖链

### 投机执行

Leader 可以在任务完成前预判结果并提前启动下游任务（speculative execution），失败时回滚投机分支。

## 失败边界

| 组件 | 失败行为 | 恢复策略 |
| --- | --- | --- |
| Worker 进程崩溃 | AgentPool 检测心跳超时 | 标记任务失败，OrchestrationRuntime 创建修复任务 |
| Leader 异常 | SessionRuntime 捕获 | 恢复已持久化的 DAG 状态 |
| Web Server 端口占用 | 自动寻找可用端口 | 写入 `~/.lingxiao/port` |
| 数据库锁 | SQLite WAL 模式 + 重试 | 事务级重试 |
| Eternal 预算耗尽 | 连续 8 次失败 | 自动暂停，等待用户介入 |
| LLM 调用失败 | 重试 + 熔断器 | 指数退避重试，熔断后降级 |

## 模块清单

| 模块 | 关键文件 | 职责 |
| --- | --- | --- |
| CLI/TUI | `src/cli.ts`, `src/tui/*` | 命令入口、Ink 终端 UI |
| Web Server | `src/server.ts`, `src/web-server/*Routes.ts` | Fastify HTTP/SSE/WS 路由 |
| Session Runtime | `src/runtime/*`, `src/core/SessionManager.ts` | 会话生命周期、状态管理 |
| Agent 系统 | `src/agents/*` | Leader/Worker、角色能力、编排 |
| 工具内核 | `src/tools/*` | ToolRegistry、100+ 内置工具 |
| LLM 层 | `src/llm/*` | Provider 客户端、流式解析、重试/熔断 |
| 数据库 | `src/core/Database.ts` | SQLite、WAL、FTS5 |
| 记忆系统 | `src/core/Memory*.ts` | 持久记忆、AutoDream |
| MCP | `src/core/McpForge*.ts` | 服务器生成、工具发现 |
| 技能 | `src/core/Skill*.ts` | Phase Loader、技能注入 |
| 编排 | `src/agents/OrchestrationRuntime.ts` | DAG 管理、验收、投机执行 |
| Eternal | `src/core/Eternal*.ts` | 自治循环、监督、遥测 |
| LLM Gateway | `src/core/LocalLlmGateway*.ts` | OpenAI/Anthropic 代理 |
| 上下文 | `src/core/ContextManifest.ts` | 上下文组装、记忆索引注入 |
| Office | `src/tools/implementations/office/*` | HTML 优先文档生成 |
| 权限 | `src/core/PermissionSystem.ts` | 工具权限、分层控制 |
