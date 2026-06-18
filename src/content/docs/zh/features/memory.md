---
title: 持久记忆
description: FTS5 + BM25 长期记忆与短期技能注入
---

# 持久记忆

凌霄有两层记忆架构。

## 长期记忆

FTS5 + BM25 全文搜索引擎。

### 4 种记忆类型

| 类型 | 说明 |
| --- | --- |
| user | 用户偏好 |
| feedback | 做事准则 |
| project | 项目知识 |
| reference | 外部资源 |

### 存储位置

- 项目级：`.lingxiao/memory/`
- 用户级：`~/.lingxiao/memory/`

### 记忆维护

- 自动提炼（DistillCommand）
- 联想记忆（DreamCommand）
- 维护管线

## 短期技能注入

在 worker dispatch 时注入执行知识，与长期记忆互补。

## 记忆操作

```text
save   — 保存记忆
load   — 读取指定记忆
search — 搜索相关记忆
list   — 列出记忆
delete — 删除记忆
rebuild — 重建索引
```
