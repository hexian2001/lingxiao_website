---
title: MCP
description: Model Context Protocol 集成
---

# MCP 集成

凌霄通过 Model Context Protocol (MCP) 连接外部系统。

## MCP 统一入口

所有 MCP server 通过统一入口访问：

- `list_servers`：列出已安装服务器
- `list_tools`：发现工具
- `call_tool`：调用工具
- `list_resources`：读取资源
- `list_prompts`：获取提示

## 安装 MCP Server

通过插件市场或 `settings.mcp.servers` 配置安装。

## MCP Forge

使用内置的 MCP Forge 引擎生成自定义 MCP Server，详见 [MCP Forge](../features/mcp-forge)。

## 配置示例

```json
{
  "mcp": {
    "servers": {
      "my-server": {
        "command": "node",
        "args": ["./my-mcp-server/index.js"]
      }
    }
  }
}
```
