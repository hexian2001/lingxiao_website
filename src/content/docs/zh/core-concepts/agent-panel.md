---
title: 专家团系统
description: Leader + Worker 专家团架构
---

# 专家团系统

凌霄的基本单位不是"一个助手"，而是 Leader + Worker 专家团。

## Leader

总指挥，负责：

- 理解目标、拆任务、建 DAG
- 调度专家、处理用户确认
- 监督收尾和验收

## 预设角色（13 种）

| 角色 | 职责 |
| --- | --- |
| research | 资料调研、方案比较 |
| explore | 代码探索、架构理解 |
| coding | 通用编码实现 |
| verify | 验证、回归测试 |
| review | 代码审查 |
| frontend | WebUI/TUI 交互、状态投影 |
| backend | 后端实现、状态机、API、数据库 |
| fullstack | 全栈实现 |
| qa | 测试、质量保证 |
| ux_designer | 可用性评审 |
| planner | 规划、拆解 |
| evaluator | 评估、验收 |
| architect | 架构设计、接口边界 |

## 进程隔离

每个 Worker 运行在独立进程中，通过 IPC 与 Leader 通信。30 秒心跳超时自动检测。

## 自定义角色

通过角色注册、技能系统和工具权限扩展专家能力。

## Agent 面板

WebUI 的 Agent 面板实时显示每个 Worker 的：

- 角色和身份
- 当前任务和进度
- 工具调用记录
- 运行状态和日志
- 结果回执
