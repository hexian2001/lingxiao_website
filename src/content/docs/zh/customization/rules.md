---
title: 规则
description: 项目规则和约束
---

# 规则

凌霄支持项目级规则文件，为 Agent 注入工程约束。

## 规则文件位置

- 项目级：`.lingxiao/rules/`
- 用户级：`~/.lingxiao/rules/`

## 规则格式

Markdown 文件，自动注入到 Agent 上下文：

```markdown
# 代码规范

- 使用 TypeScript strict 模式
- 函数必须有返回类型标注
- 禁止使用 any 类型
```

## 规则优先级

project > global，项目级规则覆盖用户级。
