---
title: 专家团系统
description: Leader + Worker 专家团架构、13 种预设角色与自定义角色
---

# 专家团系统

凌霄的基本单位不是"一个助手"，而是 **Leader + Worker 专家团**。你给目标，Leader 负责判断、拆解、规划、建 DAG、组专家团、派发任务；Worker 专家并行执行研究、前端、后端、测试、审查、文档等工作。

## Leader-Worker 架构

<div class="doc-hub-flow" role="img" aria-label="凌霄架构：用户目标 → LeaderAgent 中枢 → Worker 代理 → TaskBoard DAG、AgentPool、ToolRegistry 三大执行面。">
  <div class="doc-hub-line"><span>用户目标</span></div>
  <div class="doc-hub-down"><i>↓</i></div>
  <div class="doc-hub-leader-box"><strong>LeaderAgent</strong><span>中枢 · 规划 · 派发 · 验收</span></div>
  <div class="doc-hub-down"><i>↓</i></div>
  <div class="doc-hub-workers-box">
    <div class="doc-hub-workers"><span>Backend</span><span>Frontend</span><span>Researcher</span><span>QA / Reviewer</span></div>
  </div>
  <div class="doc-hub-arrows"><i>↓</i><i>↓</i><i>↓</i></div>
  <div class="doc-hub-triple">
    <div><strong>TaskBoard&nbsp;DAG</strong></div>
    <div><strong>AgentPool</strong></div>
    <div><strong>ToolRegistry</strong></div>
  </div>
</div>

### Leader 职责

- 理解用户目标，拆解为带依赖关系的任务图（DAG）
- 根据任务类型选择合适的 Worker 角色
- 处理用户确认和交互
- 监督执行进度、处理阻塞和失败
- 验收任务结果，提取 PASS/FAIL/BLOCKED 判定
- 协调跨任务依赖，收尾和汇总

### Worker 职责

- 接收 Leader 派发的任务，在独立进程中执行
- 拥有独立的上下文、工具调用、运行状态和日志
- 完成后通过 `attempt_completion` 提交结果和验证证据
- 可通过 `send_message` 向 Leader 报告进展或请求帮助

## 13 种预设角色

| 角色 | 标识 | 职责 |
| --- | --- | --- |
| 架构师 | `architect` | 架构设计、接口边界、模块拆分、风险控制 |
| 后端 | `backend` | 后端实现、状态机、API、数据库、任务调度 |
| 前端 | `frontend` | WebUI/TUI 交互、状态投影、可视化工作台 |
| 全栈 | `fullstack` | 跨前后端实现，契约优先，端到端验证 |
| 编码 | `coding` | 通用编码实现 |
| 研究 | `research` | 资料调研、方案比较、外部验证 |
| 探索 | `explore` | 代码探索、架构理解、入口文件定位 |
| 验证 | `verify` | 验证、回归测试、构建检查 |
| 审查 | `review` | 代码审查、质量评估 |
| 测试 | `qa` | 测试用例编写、质量保证 |
| 规划 | `planner` | 规划、任务拆解 |
| 评估 | `evaluator` | 评估、验收 |
| UX 设计 | `ux_designer` | 可用性评审、交互设计 |

## 进程隔离与通信

每个 Worker 运行在独立进程中，通过 IPC 与 Leader 通信：

- **心跳机制**：30 秒心跳超时自动检测 Worker 存活
- **状态通道**：Worker 状态、日志、对话和结果通过 agent 通信通道流转
- **监督与干预**：Leader 使用编排工具而非进程标志进行监督

## 自定义角色

凌霄支持通过多种方式扩展专家能力：

1. **角色注册**：在 `builtinRoles.ts` 或通过 WebUI 角色管理界面定义新角色
2. **技能系统**：通过 `skill_names` 为角色绑定领域知识和执行流程
3. **工具权限**：按角色配置允许/请求的工具集
4. **动态角色**：Leader 可在运行时通过 `define_agent_role` 动态创建角色

### 创建自定义角色

```typescript
// 角色定义示例
{
  name: "security-auditor",
  description: "安全审计专家",
  systemPrompt: "你是一名安全审计专家...",
  allowedTools: ["code_search", "file_read", "shell"],
  skillNames: ["security-review"],
  suggestedModel: "claude-sonnet-4"
}
```

## Agent 面板

WebUI 的 Agent 面板实时显示每个 Worker 的：

- 角色身份和当前任务
- 工具调用记录（参数、权限、输出、耗时）
- 运行状态和实时日志
- 结果回执和验证证据
