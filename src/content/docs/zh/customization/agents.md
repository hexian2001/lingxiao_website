---
title: Agents
description: 自定义 Agent 角色和能力
---

# 自定义 Agents

凌霄支持自定义 Agent 角色，扩展预设的 13 种角色。

## 角色注册

通过配置文件注册自定义角色：

```json
{
  "roles": {
    "devops": {
      "description": "DevOps 工程师",
      "skills": ["docker", "k8s", "ci-cd"],
      "tools": ["shell", "file_read", "file_create"]
    }
  }
}
```

## 技能绑定

通过 `skill_names` 为角色绑定技能包，在 worker dispatch 时自动注入。

## 工具权限

为角色配置允许使用的工具列表，实现最小权限原则。

## 角色能力模型

每个角色拥有：

- 身份和描述
- 技能集
- 工具权限
- 上下文模板
- 系统提示词
