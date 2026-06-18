---
title: 任务 DAG 编排
description: 带依赖关系的任务图调度、并行执行与状态恢复
lang: zh-CN
---

# 任务 DAG 编排

复杂目标会被拆成带依赖关系的任务图（DAG）。Leader 负责拆解任务、建立依赖关系、调度执行，让复杂工程变得可调度、可恢复、可审查。

## 任务图结构

```text
T-1 需求澄清
  ├─ T-2 架构设计
  │    ├─ T-3 后端实现
  │    └─ T-4 前端实现
  ├─ T-5 测试验证
  └─ T-6 文档与发布
```

每个节点是一个任务，箭头表示依赖关系。无依赖的任务自动并行执行，有依赖的任务按顺序解锁。

## DAG 工程收益

- **可并行任务并行跑**：无依赖的任务自动并行执行，最大化吞吐
- **有依赖任务按顺序解锁**：前置完成后自动触发后续任务
- **每个任务拥有**：owner、状态、阻塞关系、结果、证据和可恢复信息
- **WebUI 可视化**：任务图、Agent 面板、Review 证据和运行状态
- **Leader 全局调度**：基于 DAG 做调度、监督、恢复和收尾

## 任务状态流转

```text
pending → dispatched → in_progress → completed
                                   → failed
                                   → blocked
```

| 状态 | 说明 |
| --- | --- |
| `pending` | 任务已创建，等待前置依赖完成 |
| `dispatched` | 已派发给 Worker，等待启动 |
| `in_progress` | Worker 正在执行 |
| `completed` | 执行完成，结果已验收 |
| `failed` | 执行失败 |
| `blocked` | 被阻塞，等待外部条件 |

## 任务属性

每个任务携带完整的工程元数据：

```typescript
interface Task {
  id: string;              // 任务 ID，如 T-1
  title: string;           // 任务标题
  description: string;     // 详细描述
  owner: string;           // 负责的 Agent
  status: TaskStatus;      // 当前状态
  dependencies: string[];  // 前置任务 ID 列表
  writeScope: string[];    // 允许写入的文件/目录
  result?: string;         // 执行结果
  evidence?: string[];     // 验证证据
  recoverable?: boolean;   // 是否可恢复
}
```

## 并行调度

Leader 的调度器自动分析 DAG 拓扑：

1. **就绪队列**：所有前置依赖已完成的任务进入就绪队列
2. **并行派发**：就绪任务按 owner 角色并行派发给可用 Worker
3. **依赖解锁**：任务完成后自动解锁后续任务
4. **阻塞传播**：失败或阻塞的任务会传播状态到依赖链

## 状态恢复

凌霄的所有运行态持久化到 SQLite，崩溃后可完整恢复：

```bash
# 恢复指定会话
lingxiao --session <session_id>

# 列出所有会话
lingxiao list
```

恢复时：
- DAG 结构和任务状态从数据库重建
- 未完成的任务可继续执行
- 已完成的结果和证据保留
- Agent 上下文可重建

## 与编排验收集成

任务完成后自动触发验收流程：

- **投机执行**：同一任务可跑多个并行分支，择优录取
- **对抗验证**：命令级 breaker 策略验证结果
- **契约循环**：`contract → implement → evaluate → repair → reset` 五阶段闭环

详见 [编排验收内核](./orchestration.md)。
