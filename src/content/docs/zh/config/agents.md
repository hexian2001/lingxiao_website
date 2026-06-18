---
title: Agents
description: 角色定义、角色注册、工具权限与自定义 Agent
---

# Agents

凌霄的 Agent 系统基于 Leader-Worker 架构，通过角色（Role）定义 Agent 的能力、工具和知识。

## 角色系统

### Leader

Leader 负责：

- 解析用户目标
- 维护计划/任务 DAG
- 创建和分发任务
- 监督 Worker 执行
- 处理计划审查和用户问题
- 协调工具使用和权限
- 响应健康/空闲/停滞信号

### Worker

Worker 执行分配的任务。每个 Worker 拥有：

- `agent_id`：唯一标识
- `agent_name`：名称
- 角色/系统提示词
- 任务 ID
- 状态
- 迭代计数
- 对话历史

Worker 通过 AgentPool/runtime 路径运行，任务执行由 Worker 拥有。

## 预设角色

凌霄内置 13 种预设角色：

| 角色 | 说明 |
| --- | --- |
| architect | 架构师，负责任务分解和方案设计 |
| backend | 后端开发 |
| frontend | 前端开发 |
| fullstack | 全栈开发 |
| explore | 探索研究员 |
| verify | 验证工程师 |
| doc | 文档工程师 |
| test | 测试工程师 |
| devops | DevOps 工程师 |
| data | 数据工程师 |
| security | 安全工程师 |
| ui-design | UI 设计师 |
| refactor | 重构工程师 |

## 角色定义

角色通过 `RoleCapabilityModel` 定义，包含以下关键字段：

| 字段 | 说明 |
| --- | --- |
| `name` | 角色名称 |
| `description` | 角色描述 |
| `systemPrompt` | 系统提示词 |
| `allowedTools` | 允许使用的工具列表 |
| `requestedTools` | 请求使用的工具列表 |
| `skillNames` | 绑定的技能名称列表 |
| `suggestedModel` | 建议使用的模型 |

### 添加角色

角色来源有三种：

1. **内置角色**：`src/agents/leader/builtinRoles.ts` 中定义
2. **动态角色**：通过 `define_agent_role` 动态创建
3. **Web 配置**：通过 Web roles 路由配置覆盖

添加角色的步骤：

1. 定义角色职责
2. 定义系统提示词
3. 定义允许/请求的工具
4. 可选定义技能
5. 可选定义建议模型

## 自定义 Agent

### 通过配置文件

在 `~/.lingxiao/settings.json` 或项目级配置中定义自定义角色：

```json
{
  "roles": {
    "custom-role": {
      "description": "自定义角色",
      "systemPrompt": "你是一个专注于性能优化的工程师",
      "allowedTools": ["file_read", "code_search", "shell"],
      "skillNames": ["performance-optimization"]
    }
  }
}
```

### 通过 Leader 工具

Leader 可在运行时通过 `define_agent_role` 动态创建角色：

```json
{
  "name": "performance-engineer",
  "description": "性能工程师",
  "systemPrompt": "专注于代码性能分析和优化",
  "allowedTools": ["file_read", "code_search", "shell", "python_exec"]
}
```

## 工具权限

角色的 `allowedTools` 和 `requestedTools` 控制工具访问：

- `allowedTools`：角色明确允许使用的工具
- `requestedTools`：角色请求使用但需 Leader 批准的工具

工具权限还受权限系统（`security.permission_mode`）的统一管控。

## 任务 DAG

任务存储在 `tasks` 表中，通过 `TaskBoard` 管理：

| 字段 | 说明 |
| --- | --- |
| `id` | 任务 ID（如 `T-1`） |
| `session_id` | 会话 ID |
| `subject` | 任务主题 |
| `description` | 任务描述 |
| `status` | 任务状态 |
| `blocked_by` | 依赖任务 |
| `assigned_agent` | 分配的 Agent |

### 任务状态流转

```
pending → ready → dispatched → in_progress → completed
                                    ↓
                               failed / cancelled
```

## Worker 运行时

Worker 执行通过 team runtime 暴露：

- Worker 通过角色和任务绑定注册
- 每个任务分派给一个 Worker
- Worker 状态、日志、对话和完成报告通过标准 agent 通道流转
- 监督和干预使用 Leader 编排工具
