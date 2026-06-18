---
title: 自定义命令
description: 创建和管理自定义 Slash 命令
---

# 自定义命令

凌霄支持通过配置创建自定义 Slash 命令，扩展 CLI 和 WebUI 的交互能力。

## 命令格式

自定义命令以 `/` 开头，在 TUI 和 WebUI 中均可使用。

## 配置方式

在 `~/.lingxiao/settings.json` 或项目级 `.lingxiao/settings.json` 中配置：

```json
{
  "commands": {
    "deploy": {
      "description": "部署到生产环境",
      "prompt": "执行部署流程：构建、测试、推送镜像"
    }
  }
}
```

## 内置 Slash 命令

凌霄内置多种 Slash 命令，详见 [Slash 命令参考](../reference/slash-commands)。
