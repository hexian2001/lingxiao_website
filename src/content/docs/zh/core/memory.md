---
title: 持久记忆
description: FTS5+BM25 全文搜索、4 种记忆类型、Distill/Dream、项目级/用户级
lang: zh-CN
---

# 持久记忆

凌霄有两层记忆架构：长期记忆（FTS5 + BM25 全文搜索引擎）和短期技能注入（Worker dispatch 时注入执行知识），两者互补构成完整的记忆体系。

## 长期记忆

### 全文搜索引擎

基于 SQLite FTS5 + BM25 排序的全文搜索引擎：

- **FTS5**：SQLite 全文搜索扩展，支持中文分词
- **BM25**：概率相关性排序算法，按关键词匹配度排序
- **搜索接口**：`memory(action="search", query="关键词")`

### 4 种记忆类型

| 类型 | 标识 | 说明 |
| --- | --- | --- |
| 用户偏好 | `user` | 用户的编码风格、技术偏好、工作习惯 |
| 反馈准则 | `feedback` | Agent 做事准则、最佳实践、经验教训 |
| 项目知识 | `project` | 项目架构、技术栈、关键决策、模块关系 |
| 外部资源 | `reference` | 文档链接、API 参考、工具用法 |

### 存储位置

| 层级 | 路径 | 说明 |
| --- | --- | --- |
| 项目级 | `.lingxiao/memory/` | 当前项目专属记忆，随项目走 |
| 用户级 | `~/.lingxiao/memory/` | 用户全局记忆，跨项目共享 |

### 记忆操作

```typescript
// 保存记忆
memory(action="save", name="user-preferences", type="user",
  description="用户偏好", content="偏好 React + TypeScript...")

// 搜索记忆
memory(action="search", query="前端框架偏好")

// 读取指定记忆
memory(action="load", name="user-preferences")

// 列出所有记忆
memory(action="list", scope="project")

// 删除记忆
memory(action="delete", name="outdated-memory")
```

## 自动提炼（Distill）

`DistillCommand` 从会话历史中自动提炼有价值的记忆：

- 扫描已完成的会话
- 识别可复用的知识、模式和教训
- 自动分类为 4 种记忆类型
- 去重后保存到长期记忆库

## 联想记忆（Dream）

`DreamCommand` 在空闲时进行联想记忆维护：

- 发现记忆间的隐含关联
- 合并重复或相似的记忆条目
- 更新过时记忆的状态标记
- 优化搜索索引性能

## 维护管线

记忆系统有自动维护管线：

1. **索引重建**：`memory(action="rebuild")` 重建 FTS5 索引
2. **过期清理**：自动标记和清理过期记忆
3. **关联更新**：记忆间的引用关系自动维护
4. **容量控制**：项目级和用户级记忆容量监控

## 短期技能注入

在 Worker dispatch 时，Leader 会根据任务类型和角色绑定，注入相关的 Skill 内容到 Worker 的 prompt 中：

- Skill 来源优先级：项目级 > 插件贡献 > 用户级 > 内置
- 只有与当前任务相关的 Skill 阶段才会被注入
- Skill 内容作为执行知识指导 Worker 的工作流程

这与长期记忆互补：长期记忆提供跨会话的知识沉淀，短期技能注入提供当前任务的执行指引。
