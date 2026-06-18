---
title: 更新日志
description: 版本历史和变更记录
---

# 更新日志

## v0.3.9（当前版本）

### 核心系统

- **专家团系统**：13 种预设角色（Architect、Fullstack、Backend、Frontend、QA、Review、DevOps、Doc、Explore、Verify、Office、Research、Bughunter），Leader-Worker 多角色协同
- **任务 DAG 编排**：带依赖关系的任务图，并行调度，投机执行（speculative execution），失败回滚
- **全状态同步**：WebUI/TUI/CLI 三端实时同步，基于 `session:runtime_state` 统一快照 + SSE + ACP JSON-RPC
- **编排验收内核**：结构化验收结论提取（PASS/FAIL/BLOCKED/UNKNOWN），对抗验证，自适应编排，修复任务自动创建

### 工具与能力

- **100+ 内置工具**：文件读写、Shell 执行、浏览器自动化、Git 操作、代码搜索、Web 抓取、OCR 等
- **MCP Forge 生成引擎**：从自然语言描述生成 stdio/http MCP server，支持工具发现和调用
- **14 个内置技能包**：Phase Loader 按需注入 Agent 上下文，项目级 > 插件 > 用户级 > 内置优先级
- **Office 文档生成**：HTML 优先文档生成，支持 PDF/PNG/DOCX/XLSX/PPTX 导出

### 持久化与记忆

- **持久记忆系统**：FTS5 全文搜索 + BM25 评分 + AutoDream 自动整合检查点
- **SQLite WAL 模式**：会话、消息、任务、Agent 状态、记忆全部持久化，崩溃可恢复
- **可验证假设跟踪**：Agent 声明假设后自动验证，证伪时强制修正

### 自治与网关

- **Eternal 自治模式**：IDLE → CHECK → PATROL → THINK → WAIT 循环，指数退避，预算熔断
- **本地 LLM Gateway**：OpenAI/Anthropic 双格式代理，虚拟密钥管理，per-key RPM/TPM/daily token budget 限流
- **Bughunt DAG 调度器**：结构化 bug 狩猎，账本管理，报告生成

### 平台与开发

- **CLI 命令树**：`lingxiao start/list/init/doctor/about/demo/agents/daemon/worktree`
- **Daemon 后台模式**：进程自愈守护，崩溃自动重启
- **Git Worktree 隔离**：每个任务可在独立 worktree 中执行
- **权限系统**：strict/dev/networked/yolo 四种模式，session/project/local/user 四层持久化
- **Team 协作模式**：多 Agent P2P 消息、任务转派、review 请求/结果

### 安全

- **加固模式**：非 loopback 绑定时自动启用，禁用 query token，强制 header 鉴权
- **限流冷却**：429 触发 30s 冷却期
- **写入范围隔离**：Worker 任务 `write_scope` 检查
- **密钥脱敏**：API 响应中 mask Git token 和 provider key

## 系统要求

| 依赖 | 要求 |
| --- | --- |
| Node.js | >= 24.0.0 |
| Git | 推荐 |
| 操作系统 | Linux / macOS / Windows / WSL |

## 技术栈

| 层 | 技术 |
| --- | --- |
| 运行时 | Node.js 24, TypeScript (ESM) |
| Web Server | Fastify, @fastify/websocket |
| Web UI | React, Zustand, Vite |
| TUI | Ink |
| 数据库 | SQLite (WAL + FTS5) |
| CLI | Commander.js, Inquirer, Chalk |
| LLM | OpenAI SDK, Anthropic SDK, Vercel AI SDK |
