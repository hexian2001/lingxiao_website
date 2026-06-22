---
title: 简介
description: 凌霄剑域 — 面向真实工程交付的本地 AI 指挥系统
---

# 凌霄剑域 LingXiao

> 以 Leader 定策，以 DAG 布阵，以专家团执行，以证据收卷。凌霄不是把模型放进一个输入框，而是把模型、工具、权限、任务、状态和验收纳入同一套本地工程秩序。

凌霄面向的是长期、复杂、必须落地的 AI 工程：从一句目标开始，系统会形成计划、拆出任务依赖、调度不同角色的 Worker 专家、调用真实工具，并把构建结果、测试输出、浏览器截图、日志、Git 变更和会话状态一并留痕。

## 凌霄能做什么

<div class="doc-feature-grid">
  <article>
    <strong>专家团系统</strong>
    <span>Leader 负责判断、规划、派发与收口；Worker 按研究、前端、后端、验证、审查等角色并行推进。</span>
  </article>
  <article>
    <strong>任务 DAG 编排</strong>
    <span>复杂目标拆成带依赖关系的任务图，哪些能并行、哪些必须等待、哪些需要修复，都清清楚楚。</span>
  </article>
  <article>
    <strong>真实工具内核</strong>
    <span>文件、Shell、Git、浏览器、HTTP、Office、MCP 与工作流工具统一接入，不停留在口头方案。</span>
  </article>
  <article>
    <strong>全状态同步</strong>
    <span>WebUI / TUI / CLI 共享同一运行态，任务板、Agent 进度、权限请求、终端输出实时可见。</span>
  </article>
  <article>
    <strong>证据与验收闭环</strong>
    <span>每次交付都回到构建、测试、截图、日志、契约和 diff 证据；失败则进入明确的 repair 流程。</span>
  </article>
  <article>
    <strong>可恢复会话</strong>
    <span>SQLite、Git、记忆、工作笔记与会话归档共同保存工程上下文，崩溃后也能接续推进。</span>
  </article>
</div>

## 架构速览

<div class="doc-arch-map" role="img" aria-label="凌霄运行架构：入口层进入会话内核，由 Leader 调度任务 DAG、专家团、工具注册表与持久化证据层。">
  <section class="doc-arch-node doc-arch-entry">
    <small>入口层</small>
    <strong>WebUI / TUI / CLI / Desktop</strong>
    <span>统一目标入口，实时展示任务板、Agent、工具与权限状态。Windows 桌面版支持 MSI/NSIS 安装与自动更新。</span>
  </section>
  <section class="doc-arch-node doc-arch-session">
    <small>会话内核</small>
    <strong>SessionManager / SessionRuntime</strong>
    <span>创建、恢复、暂停、同步会话，维护运行模式与全局事件流。</span>
  </section>
  <section class="doc-arch-node doc-arch-leader">
    <small>中枢</small>
    <strong>LeaderAgent</strong>
    <span>理解目标、拆解计划、建立 DAG、选择角色、验收证据。</span>
  </section>
  <section class="doc-arch-node doc-arch-dag">
    <small>编排</small>
    <strong>TaskBoard DAG</strong>
    <span>记录依赖、阻塞、派发、完成、失败、修复与评估状态。</span>
  </section>
  <section class="doc-arch-node doc-arch-agents">
    <small>执行</small>
    <strong>AgentPool / Worker Experts</strong>
    <span>研究、编码、测试、审查、设计、运维等专家角色并行工作。</span>
  </section>
  <section class="doc-arch-node doc-arch-tools">
    <small>百器</small>
    <strong>ToolRegistry / MCP / Skills</strong>
    <span>文件、终端、Git、浏览器、HTTP、Office、Workflow 与外部 MCP 工具。</span>
  </section>
  <section class="doc-arch-node doc-arch-proof">
    <small>留痕</small>
    <strong>SQLite / Git / Memory / Artifacts</strong>
    <span>保存会话状态、工程 diff、工作笔记、验收证据与可恢复轨迹。</span>
  </section>
</div>

## 适合的工作

| 场景 | 凌霄如何处理 |
| --- | --- |
| 产品交付 | 从需求、接口契约、前后端实现到浏览器验收与文档同步，按任务图推进。 |
| 代码治理 | 梳理技术债、迁移计划、测试缺口、重构风险，并用证据确认每一步。 |
| 内部自动化 | 把本地脚本、Office/PDF、MCP、Git、Workflow 和模型能力编成可复用流程。 |
| 长线目标 | Eternal Goal 可持续巡逻目标，直到完成、遇阻或需要人工决策。 |

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

## 系统要求

| 依赖 | 要求 |
| --- | --- |
| Node.js | `>=24.0.0` |
| npm | 随 Node 24 配套版本 |
| Git | 推荐安装，用于 diff、提交与恢复轨迹 |
| 操作系统 | Linux / macOS / Windows / WSL |

## 下一步

- [安装与启动](../install) — 从零搭建凌霄运行环境
- [连接模型](../connect-models) — 配置模型提供商与路由策略
- [第一次运行](../first-run) — 启动第一个可观测、可验收的专家团
