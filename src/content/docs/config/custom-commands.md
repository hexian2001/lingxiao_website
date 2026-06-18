---
title: 自定义命令
description: Slash 命令注册、自定义命令与命令生命周期
---

# 自定义命令

凌霄支持通过 Slash 命令系统扩展 CLI 和 WebUI 的交互能力。Slash 命令是 TUI、Web 聊天输入和 ACP `session/command` 的共享命令面。

## 命令生命周期

Slash 命令从用户输入到执行的完整流程：

1. **检测**：Web/TUI 输入检测到 `/` 开头的命令
2. **注册查找**：`slash_registry` 查找命令元数据
3. **分发**：`dispatcher.ts` 执行回调或转发到 SessionManager
4. **返回结果**：`CommandResult` 返回给客户端

## 命令定义

每个 Slash 命令通过 `SlashCommandDefinition` 注册：

| 字段 | 说明 |
| --- | --- |
| `name` | 命令唯一名称 |
| `desc` | 用户可见描述 |
| `usage` | 可选用法字符串 |
| `handledBy` | `tui-local`（客户端处理）或 `callback`（后端回调） |
| `includeInSuggestions` | 是否出现在自动补全中 |
| `includeInHelp` | 是否出现在 `/help` 中 |
| `category` | 帮助分组 |
| `argCompleter` | 可选参数补全 |

## 处理器类型

| 处理器 | 含义 | 说明 |
| --- | --- | --- |
| `tui-local` | 客户端自行处理 | 不调用后端回调 |
| `callback` | 后端回调处理 | 通过 `dispatcher.ts` 分发 |

## 自定义命令配置

在 `~/.lingxiao/settings.json` 或项目级 `.lingxiao/settings.json` 中配置自定义命令：

```json
{
  "commands": {
    "deploy": {
      "description": "部署到生产环境",
      "prompt": "执行部署流程：构建、测试、推送镜像"
    },
    "review": {
      "description": "代码审查",
      "prompt": "审查当前工作区的代码变更，给出改进建议"
    }
  }
}
```

### 命令格式

自定义命令以 `/` 开头，在 TUI 和 WebUI 中均可使用。输入 `/deploy` 即可触发对应的 prompt。

## 内置 Slash 命令

凌霄内置 66 个 Slash 命令，涵盖会话管理、Agent 控制、权限、MCP、插件等：

### 会话管理

| 命令 | 说明 |
| --- | --- |
| `/new` | 创建新会话 |
| `/sessions` | 列出所有会话 |
| `/fork` | 分叉当前会话 |
| `/exit` | 退出程序 |
| `/quit` | 退出程序 |

### Agent 与编排

| 命令 | 说明 |
| --- | --- |
| `/agents` | 查看 Agent 列表 |
| `/roles` | 查看角色定义 |
| `/board` | 查看任务板 |
| `/pool` | 查看 Agent 池 |

### 权限

| 命令 | 说明 |
| --- | --- |
| `/permission` | 查看当前权限模式 |
| `/mode` | 切换权限模式 |

### MCP

| 命令 | 说明 |
| --- | --- |
| `/mcp list` | 列出已配置的 MCP 服务器 |
| `/mcp search <query>` | 搜索市场中的 MCP 条目 |
| `/mcp install <entry-id>` | 安装市场 MCP 条目 |
| `/mcp tools [server-id]` | 查看服务器暴露的工具 |
| `/mcp call <server-id> <tool-name> [args]` | 调用服务器工具 |
| `/mcp resources [server-id]` | 查看服务器资源 |
| `/mcp read-resource <server-id> <uri>` | 读取服务器资源 |
| `/mcp prompts [server-id]` | 查看服务器提示 |
| `/mcp get-prompt <server-id> <prompt-name> [args]` | 获取服务器提示 |
| `/mcp templates [server-id]` | 列出资源模板 |
| `/mcp snapshot [server-id]` | 查看能力快照 |
| `/mcp add-remote <id> <url> [name]` | 添加远程 HTTP 服务器 |
| `/mcp add-stdio <id> <command> [args...]` | 添加 stdio 服务器 |

### 其他

| 命令 | 说明 |
| --- | --- |
| `/help` | 显示帮助 |
| `/config` | 查看配置 |
| `/skills` | 查看技能列表 |
| `/plugins` | 管理插件 |
| `/marketplace` | 访问市场 |

## 演进规则

1. 新命令必须添加到 `slash_registry.ts`
2. `handledBy: 'callback'` 的命令必须在 `dispatcher.ts` 中添加回调行为
3. Web 自动补全必须在后端注册表存在后更新
4. 同义词命令（如 `/quit` 和 `/exit`）注册为独立条目，命令名不归一化
