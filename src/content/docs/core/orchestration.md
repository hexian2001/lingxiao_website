---
title: 编排验收内核
description: 投机执行、对抗验证、自适应编排、契约循环、Bug 狩猎、假设跟踪
---

# 编排验收内核

凌霄不只是派任务，而是对每个完成的任务做结构化验收。编排内核通过投机执行、对抗验证、自适应路由和契约循环，让任务结果可验证、可追溯、可修复。

## 编排运行时

任务生命周期事件（创建/更新/派发/完成）自动触发验收流程，提取 PASS/FAIL/BLOCKED verdict：

<div class="doc-flow" role="img" aria-label="编排验收流程：任务完成后进入 VerificationPipeline、对抗验证、自适应路由并产出 verdict。">
  <span>任务完成</span><i>→</i><span>VerificationPipeline</span><i>→</i><span>对抗验证</span><i>→</i><span>自适应路由</span><i>→</i><strong>verdict</strong>
</div>

## 投机执行

同一任务可跑多个并行实现分支，按策略择优录取：

<div class="doc-branch-flow" role="img" aria-label="投机执行分支：T-3 后端实现并行运行三个分支，A 和 B 验证通过，C 验证失败。">
  <strong>Task T-3：后端实现</strong>
  <div><span>Branch A</span><em>architect 方案</em><b>验证通过 ✓</b></div>
  <div><span>Branch B</span><em>简化方案</em><b>验证通过 ✓</b></div>
  <div><span>Branch C</span><em>激进方案</em><b class="is-fail">验证失败 ✗</b></div>
</div>

### 选择策略

| 策略 | 说明 |
| --- | --- |
| `first_green` | 首个通过验证的分支胜出 |
| `fewest_changes` | 最小 diff 的通过分支胜出 |
| `fastest_tests` | 测试最快的通过分支胜出 |

- 每个分支拥有独立的工作目录和写入范围
- `VerificationPipeline` 独立验证每个分支
- 落选分支自动清理
- 默认超时：30 分钟
- 最多 6 个并行分支

## 对抗验证

`AdversarialVerifier` 运行命令级 breaker 策略：

```typescript
interface BreakerStrategy {
  command: string;        // 验证命令
  expectedExitCode: number; // 期望退出码
  failOnExitCode: number;   // 失败退出码
}
```

### 验证流程

1. 执行 breaker 命令
2. 采集 stdout、stderr、执行耗时、超时状态
3. 判定 verdict：
   - **PASS**：所有策略通过
   - **FAIL**：任一策略失败
   - **BLOCKED**：基础设施问题

## 自适应编排

`AdaptiveHarness` 基于难度信号智能路由任务：

| 信号 | 说明 |
| --- | --- |
| `cross_module_deps` | 跨模块依赖数量 |
| `hotspot_overlap` | 与已知热点区域的重叠 |
| `prior_failures` | 历史失败率 |
| `impact_ratio` | 影响面比例 |
| `has_ambiguous_path` | 是否存在模糊路径 |
| `dependency_count` | 依赖数量 |

### 执行策略

基于信号自动选择执行策略：

- **fast_path**：小范围、低风险任务，单 Worker 快速执行
- **standard**：中等复杂度，标准调度
- **speculative**：高难度任务，多分支投机执行
- **contract_first**：跨栈任务，先定义契约再实现

## 契约循环

五阶段闭环确保跨栈实现的一致性：

<div class="doc-flow doc-flow-loop" role="img" aria-label="契约循环：contract、implement、evaluate、repair、reset，reset 后回到 contract。">
  <span>contract</span><i>→</i><span>implement</span><i>→</i><span>evaluate</span><i>→</i><span>repair</span><i>→</i><span>reset</span><i>↺</i><strong>contract</strong>
</div>

### 五阶段说明

| 阶段 | 说明 |
| --- | --- |
| `contract` | 定义接口契约（schema、错误码、状态流） |
| `implement` | 按契约实现前后端代码 |
| `evaluate` | 验证实现是否符合契约 |
| `repair` | 修复不符合契约的部分 |
| `reset` | 重置并进入下一轮（如需） |

契约 blackboard 节点自动物化到 `.lingxiao/contracts/` 目录，供所有 Agent 共享。

## Bug 狩猎

Bughunt DAG 调度器在隔离 worktree 中运行：

- **DAG 调度**：Bug 狩猎任务按依赖关系编排
- **证据采集**：自动收集复现步骤、堆栈、环境信息
- **证据提取**：从日志和输出中提取关键证据
- **证据打包**：打包证据供审查
- **发现账本**：记录所有 Bug 发现和修复历史

## 假设跟踪

Agent 可声明可验证假设，代码变更后自动重验：

```typescript
interface Assumption {
  verification_type: 'type_check' | 'file_content' | 'test_execution' | 'ast_query';
  target: string;      // 验证目标（文件路径、测试名等）
  expected: string;    // 期望结果（精确文本匹配）
}
```

### 验证类型

| 类型 | 说明 |
| --- | --- |
| `type_check` | TypeScript 类型检查 |
| `file_content` | 文件内容匹配 |
| `test_execution` | 测试执行结果 |
| `ast_query` | AST 查询断言 |

假设被证伪时，系统会反馈给 Agent，要求停止当前错误方向并修正理解。
