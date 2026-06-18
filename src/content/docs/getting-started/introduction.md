---
title: 简介
description: 凌霄剑域 — AI 工程指挥系统，不是聊天壳，而是本地编排内核
---

# 凌霄剑域 LingXiao

> AI engineering command system. Not a chat shell: LingXiao is a local orchestration kernel for expert teams, task DAGs, real tools, evidence, WebUI/TUI synchronization, and recoverable engineering sessions.

凌霄把"和模型聊天"升级成"指挥一个可观测、可恢复、可审查的 AI 专家团队"。

你给目标，Leader 负责判断、拆解、规划、建 DAG、组专家团、派发任务；Worker 专家并行执行研究、前端、后端、测试、审查、文档、Git 操作等工作；WebUI/TUI 实时同步完整运行态，所有任务、工具、权限、证据和会话状态都进入同一个工程内核。

## 核心价值

| 能力 | 说明 |
| --- | --- |
| 专家团协同 | Leader + Worker 多角色并行，而非单 Agent 对话 |
| 任务 DAG | 复杂目标自动拆解为带依赖关系的任务图 |
| 全状态同步 | WebUI / TUI / CLI 三端实时同步运行态 |
| 可恢复 | SQLite 持久化，崩溃后 `--session <id>` 恢复 |
| 可审查 | 工具调用全链路追踪、证据采集、验收闭环 |

## 架构速览

```text
User ──→ TUI / CLI ──→ SessionManager ──→ SessionRuntime ──→ LeaderAgent
                                                                    │
                                     ┌──────────────────────────────┼──────────────────┐
                                     ▼                              ▼                  ▼
                               TaskBoard / DAG              AgentPool           ToolRegistry
                                     │                      │                     │
                                     ▼                      ▼                     ▼
                              Worker Experts ←────────── Pool ←─────────── Git / Workbench
                                     │
                                     ▼
                                SQLite DB
```

## 系统要求

| 依赖 | 要求 |
| --- | --- |
| Node.js | `>=24.0.0` |
| npm | 随 Node 24 配套版本 |
| Git | 推荐安装 |
| 操作系统 | Linux / macOS / Windows / WSL |

## 下一步

- [安装与启动](./install) — 从零搭建凌霄运行环境
- [连接模型](./connect-models) — 配置 LLM 提供商
- [第一次运行](./first-run) — 启动你的第一个专家团
