---
title: 权限系统
description: 9层工具权限评估链
---

# 权限系统

凌霄的工具调用遵循多层权限评估链，确保安全可控。

## 9 层评估链

```text
deny → allow → ask → yolo → always-allowed → network → hardened → strict → default allow
```

## 权限模式

| 模式 | 说明 |
| --- | --- |
| `strict` | 严格模式，所有写操作需确认 |
| `dev` | 开发模式，放宽限制 |
| `networked` | 网络模式，允许网络工具 |
| `yolo` | 全自动模式，无确认 |

## 配置方式

在 `~/.lingxiao/settings.json` 中设置：

```json
{
  "tools": {
    "permissionMode": "strict"
  }
}
```

## 工具白名单

可通过配置为特定工具设置 `always-allowed` 权限，跳过交互确认。
