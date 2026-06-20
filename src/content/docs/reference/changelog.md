---
title: 更新日志
description: 版本历史和变更记录
---

# 更新日志

## v1.0.2（当前版本）

### 桌面版与分发

- **Windows 桌面版**：Electron 桌面客户端，支持 MSI 安装包 + NSIS 自动更新安装包，electron-updater 增量更新
- **全平台便携包**：Linux (x64/arm64)、macOS (arm64)、Windows (x64) 预构建便携包，开箱即用
- **SEA 二进制**：Node.js Single Executable Application，三平台独立可执行文件
- **跨平台自动升级**：`lingxiao upgrade` 自动定位安装路径，支持源码 / 便携包两种模式，跳过 electron 二进制下载
- **GitHub Release 自动化**：CI/CD 全平台并行构建，tag 触发自动发布

### Web UI 增强

- **Workspace 选择器**：后端 4 个 API + recent_workspaces.json，前端 WorkspacePicker 组件
- **401 Token 恢复**：Web UI 401 时自动刷新 token，随机端口默认开启
- **中文输入法修复**：IME 组合状态回车不再误触发消息发送（macOS/Windows 全平台）
- **Git 活动监控**：git:activity 事件全链路展示，按会话隔离 + Agent 统计 + Gate 结果

### CI/CD 与工程

- **CI 类型检查**：tsc --noEmit 全量检查，src/desktop 独立 tsconfig 隔离
- **Release Workflow**：5 个并行构建 job（portable × 4 平台 + binary × 4 平台 + desktop MSI/NSIS + source）
- **Windows 压缩兼容**：PowerShell Compress-Archive 替代 zip 命令
- **Desktop 编译链**：tsconfig.desktop.json 独立编译 electron 入口

## v1.0.0

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
| 桌面端 | Electron, electron-builder |
| 数据库 | SQLite (WAL + FTS5) |
| CLI | Commander.js, Inquirer, Chalk |
| LLM | OpenAI SDK, Anthropic SDK, Vercel AI SDK |
