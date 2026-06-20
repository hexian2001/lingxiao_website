---
title: MCP
description: MCP 统一入口、MCP Server 配置与 MCP Share
---

# MCP（Model Context Protocol）

凌霄通过统一的 `mcp` 工具入口连接外部系统，支持 tools、resources 和 prompts 三类能力。

## 统一入口

所有 MCP 操作通过 `mcp` 工具完成：

| 操作 | 说明 |
| --- | --- |
| `list_servers` | 列出已安装的 MCP 服务器 |
| `list_tools` | 列出服务器暴露的工具 |
| `call_tool` | 调用服务器工具 |
| `list_resources` | 列出服务器资源 |
| `read_resource` | 读取服务器资源 |
| `list_prompts` | 列出服务器提示 |
| `get_prompt` | 获取服务器提示 |
| `list_resource_templates` | 列出资源模板 |
| `capability_snapshot` | 查看服务器能力快照 |

## MCP Server 配置

MCP 服务器通过 `settings.mcp.servers` 配置：

### stdio 服务器

```json
{
  "mcp": {
    "servers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"],
        "env": {}
      }
    }
  }
}
```

### 远程 HTTP 服务器

```json
{
  "mcp": {
    "servers": {
      "remote-api": {
        "url": "https://example.com/mcp",
        "transport": "streamable-http"
      }
    }
  }
}
```

### 通过 Slash 命令添加

```bash
# 添加远程 HTTP 服务器
/mcp add-remote my-server https://example.com/mcp "我的服务器"

# 添加 stdio 服务器
/mcp add-stdio my-server npx -y @modelcontextprotocol/server-filesystem /tmp
```

## MCP Share

MCP Share 支持通过分享链接和 `.mcpb` 包导入/导出 MCP 服务器配置。

### 分享链接

生成可移植的分享链接，包含服务器的完整配置（敏感信息已清洗）。

### .mcpb 包

`.mcpb` 是 MCP 服务器的可移植打包格式，包含：

- 服务器代码或配置
- 依赖声明
- 元数据

## 插件贡献的 MCP

插件启用后，其贡献的 MCP 服务器会同步到 `settings.mcp.servers`，通过同一 `mcp` 工具入口访问。

## 与运行时的关系

- MCP tools 注册到 ToolRegistry 后，Agent 可在运行时调用
- MCP resources 通过 `read_resource` 读取
- MCP prompts 通过 `get_prompt` 获取
- 所有 MCP 操作产生的文件、URI 和验证结果写入工作笔记
