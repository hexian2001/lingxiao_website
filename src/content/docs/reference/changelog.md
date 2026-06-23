---
title: 更新日志
description: 版本历史和变更记录
---

# 更新日志

## v1.0.3（当前版本）

> **版本范围：** v1.0.2 → v1.0.3 | 19 commits | 183 files changed | +13,244 / -2,340 lines

### ✨ 新功能

#### Web UI

- **Beta 徽章** — 为实验性功能添加水墨丹青风格 Beta 徽章，视觉标识更清晰
- **会话恢复** — 从快照恢复运行中 Worker 的对话上下文，刷新/断线不丢状态

### 🐛 Bug 修复

- **长任务卡住 P0/P1** — CircuitBreaker 被 `resetCircuitBreakersForProvider` 架空导致 LLM 调用全部阻断，彻底修复断路器重置逻辑
- **思考预算被压扁** — LLM 思考预算（thinking budget）计算错误 + 用户配置优先级覆盖修复
- **用户消息队列逐条处理** — 用户连发 N 条消息需 N 轮 patrol 逐条处理，改为一次性 drain 队列让 LLM 单轮消化
- **Worker `missing_contract_compliance_proof` 反复失败** — 契约合规证明缺失导致 Worker 循环失败，三层修复
- **Agent 续跑注入 continuation prompt** — Agent 恢复续跑时不应注入续跑提示，避免上下文污染
- **Web UI 消息重复卡片** — 消息渲染重复 + Git 活动页面空白
- **Web 搜索卡死** — 搜索工具调用超时导致 Agent 卡死
- **网关 URL 提示** — LLM Gateway 地址提示信息不准确
- **Git Activity 前端加载** — 前端数据加载时序问题
- **桌面端 MSI 打包** — 减小 MSI 安装包体积和冗余

### 🔧 工程改进

- **Leader 工具描述增强** — 结构化干预层级（pause < nudge < intervene < terminate），工具描述更清晰
- **意图识别工具豁免** — `record_capability_intent` 豁免工具抑制检查
- **编排内核** — 接受黑板契约证据作为合规证明
- **版本管理统一** — 强制单一版本源，消除多处版本号不一致

## v1.0.2

> **版本范围：** v1.0.1 → v1.0.2 | 9 commits | 85 files changed | +5,814 / -380 lines

### ✨ 新功能

#### Web UI

- **Workspace 选择器** — 侧边栏快速切换工作区，自动记录最近使用的工作区
- **Git Activity 可视化** — 全新 Git 活动监控面板，展示会话级 git 事件流、Agent 统计和 Gate 结果
- **Onboarding 引导向导** — 首次使用时引导用户配置 LLM、选择工作区和初始化项目
- **版本更新通知** — 自动检测新版本，侧边栏显示版本徽章 + 一键更新
- **文件变更面板增强** — 新增 FileChanges API 和 store，实时追踪文件变更状态

#### TUI

- **Onboarding 引导** — TUI 端同步新增首次引导流程（`OnboardingTui.ts`）
- **剪贴板支持** — 新增 clipboard 模块，TUI 可复制/粘贴内容
- **Composer 优化** — 输入框交互改进，粘贴控制器增强

#### 桌面端

- **Electron 桌面应用** — 全新 `src/desktop/` 模块，支持 Windows MSI/NSIS 安装包
- IPC 通道类型安全，preload 脚本隔离渲染进程

#### Git 工具

- **GitTool 大幅增强**（+153 行）— 支持更多 git 操作和活动监控事件全链路
- **GitService 增强**（+254 行）— 后端服务层全面扩展

### 🐛 Bug 修复

- **macOS 中文输入法回车误发送** — `ChatView.tsx` 和 `MessageInput.tsx` 增加 `isComposing` 守卫，IME 组合期间的回车不再触发发送
- **CI tsc 编译失败** — `src/desktop/` 依赖 electron 类型，从主 tsconfig 排除，新建独立 `tsconfig.desktop.json` 编译
- **Windows 便携包打包失败** — Windows CI 无 `zip` 命令，改用 PowerShell `Compress-Archive`
- **release.yml YAML 语法错误** — release notes 表格行错位修复
- **desktop 配置丢失** — 合并冲突解决时误丢 desktop scripts/deps/build config，全部恢复
- **CircuitBreaker 状态** — LlmGuard recycle 后重置断路器，避免新 client 被旧失败计数阻塞

### 🔧 工程与 CI/CD

- **CI workflow** — 新增 `ci.yml`，push/PR 时自动跑 tsc 类型检查 + 构建
- **Release workflow** — 全新 `release.yml`，tag 触发自动构建发布：
  - 4 平台便携包（linux-x64, linux-arm64, darwin-arm64, win-x64）
  - 3 平台 SEA 二进制（linux-x64, darwin-arm64, win-x64）
  - Windows 桌面版（MSI artifact + NSIS 发布到 GitHub Releases，支持 electron-updater 自动更新）
  - 源码 tarball
  - 自动创建 GitHub Release 并汇总所有 artifacts
- **SEA 二进制** — 新增 `sea-config.json` + `build-binary.mjs`，Node.js SEA 打包
- **便携包打包** — 新增 `package-portable.mjs`，跨平台 tar.gz/zip 打包

### 📦 依赖变更

- 新增 `electron` ^42.4.1 (devDep)
- 新增 `electron-builder` ^26.15.3 (devDep)
- 新增 `electron-updater` ^6.8.9 (dependency)

### 🌐 i18n

- 中英文翻译同步更新，新增 Workspace、Git Activity、Onboarding、更新通知等模块文案

### 📋 文件变更明细

| 领域 | 文件数 | 关键模块 |
| --- | --- | --- |
| Web UI 前端 | 30+ | WorkspacePicker, GitActivityView, OnboardingWizard, UpdateNotification, FileChangesApi |
| TUI | 8 | OnboardingTui, clipboard, Composer, paste/key controllers |
| 后端服务 | 15+ | GitService, WorkspaceRoutes, FileChangesApi, MiscRoutes, ServerAuth |
| Agent 核心 | 10 | AgentDefinitionService, LeaderAgent, LlmGuard, RoleRegistry, LeaderThinkingLoop |
| 桌面端 | 3 | desktop/main.ts, desktop/preload.ts, tsconfig.desktop.json |
| CI/CD | 6 | ci.yml, release.yml, build-binary.mjs, package-portable.mjs, sea-config.json |
| CLI | 3 | cli.ts (重构), cli_upgrade.ts (增强), config.ts |

## v1.0.0

### 🏗️ 核心系统

- **专家团系统**：13 种预设角色（Architect、Fullstack、Backend、Frontend、QA、Review、DevOps、Doc、Explore、Verify、Office、Research、Bughunter），Leader-Worker 多角色协同
- **任务 DAG 编排**：带依赖关系的任务图，并行调度，投机执行（speculative execution），失败回滚
- **全状态同步**：WebUI/TUI/CLI 三端实时同步，基于 `session:runtime_state` 统一快照 + SSE + ACP JSON-RPC
- **编排验收内核**：结构化验收结论提取（PASS/FAIL/BLOCKED/UNKNOWN），对抗验证，自适应编排，修复任务自动创建

### 🔧 工具与能力

- **100+ 内置工具**：文件读写、Shell 执行、浏览器自动化、Git 操作、代码搜索、Web 抓取、OCR 等
- **MCP Forge 生成引擎**：从自然语言描述生成 stdio/http MCP server，支持工具发现和调用
- **14 个内置技能包**：Phase Loader 按需注入 Agent 上下文，项目级 > 插件 > 用户级 > 内置优先级
- **Office 文档生成**：HTML 优先文档生成，支持 PDF/PNG/DOCX/XLSX/PPTX 导出

### 💾 持久化与记忆

- **持久记忆系统**：FTS5 全文搜索 + BM25 评分 + AutoDream 自动整合检查点
- **SQLite WAL 模式**：会话、消息、任务、Agent 状态、记忆全部持久化，崩溃可恢复
- **可验证假设跟踪**：Agent 声明假设后自动验证，证伪时强制修正

### 🔄 自治与网关

- **Eternal 自治模式**：IDLE → CHECK → PATROL → THINK → WAIT 循环，指数退避，预算熔断
- **本地 LLM Gateway**：OpenAI/Anthropic 双格式代理，虚拟密钥管理，per-key RPM/TPM/daily token budget 限流
- **Bughunt DAG 调度器**：结构化 bug 狩猎，账本管理，报告生成

### 🖥️ 平台与开发

- **CLI 命令树**：`lingxiao start/list/init/doctor/about/demo/agents/daemon/worktree`
- **Daemon 后台模式**：进程自愈守护，崩溃自动重启
- **Git Worktree 隔离**：每个任务可在独立 worktree 中执行
- **权限系统**：strict/dev/networked/yolo 四种模式，session/project/local/user 四层持久化
- **Team 协作模式**：多 Agent P2P 消息、任务转派、review 请求/结果

### 🔒 安全

- **加固模式**：非 loopback 绑定时自动启用，禁用 query token，强制 header 鉴权
- **限流冷却**：429 触发 30s 冷却期
- **写入范围隔离**：Worker 任务 `write_scope` 检查
- **密钥脱敏**：API 响应中 mask Git token 和 provider key
