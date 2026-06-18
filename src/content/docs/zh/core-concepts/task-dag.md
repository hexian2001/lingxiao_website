---
title: 任务DAG编排
description: 带依赖关系的任务图调度
---

# 任务 DAG 编排

复杂目标会被拆成带依赖关系的任务图（DAG）。

## 任务图结构

```text
T-1 需求澄清
  ├─ T-2 架构设计
  │    ├─ T-3 后端实现
  │    └─ T-4 前端实现
  ├─ T-5 测试验证
  └─ T-6 文档与发布
```

## DAG 工程收益

- **可并行任务并行跑**：无依赖的任务自动并行执行
- **有依赖任务按顺序解锁**：前置完成后自动触发
- **每个任务拥有**：owner、状态、阻塞关系、结果、证据和可恢复信息
- **WebUI 可视化**：任务图、Agent 面板、Review 证据和运行状态

## 任务状态流转

```text
pending → dispatched → in_progress → completed
                                   → failed
                                   → blocked
```

## 投机执行

同一任务可跑多个并行实现分支，按策略择优：

- `first_green`：首个通过
- `fewest_changes`：最小改动
- `fastest_tests`：最快测试

## 契约循环

```text
contract → implement → evaluate → repair → reset
```

五阶段闭环，契约 blackboard 节点自动物化到 `.lingxiao/contracts/`。
