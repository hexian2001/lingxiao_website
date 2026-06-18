---
title: 编排验收
description: 投机执行、对抗验证、自适应编排
---

# 编排验收内核

凌霄不只是派任务，而是对每个完成的任务做结构化验收。

## 编排运行时

任务生命周期事件（创建/更新/派发/完成）自动触发验收，提取 PASS/FAIL/BLOCKED verdict。

## 投机执行

同一任务可跑多个并行实现分支，按策略择优：

- `first_green`：首个通过
- `fewest_changes`：最小改动
- `fastest_tests`：最快测试

## 对抗验证

命令级 breaker 策略：

- 退出码断言
- stdout/stderr 证据采集

## 自适应编排

基于难度信号智能路由任务：

- 跨模块依赖
- 热点重叠
- 历史失败率
- 影响面比例

## 契约循环

```text
contract → implement → evaluate → repair → reset
```

五阶段闭环，契约 blackboard 节点自动物化到 `.lingxiao/contracts/`。

## Bug 狩猎

Bughunt DAG 调度器 + 证据采集/提取/打包 + 发现账本，在隔离 worktree 中运行。

## 假设跟踪

Agent 可声明可验证假设：

- `type_check`
- `file_content`
- `test_execution`
- `ast_query`

代码变更后自动重验。
