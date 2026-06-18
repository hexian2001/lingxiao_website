---
title: MCP Forge
description: 模板驱动的 MCP Server 生成引擎
---

# MCP Forge

MCP Forge 是凌霄的模板驱动 MCP Server 生成引擎。

## 状态机管线

```text
需求 → 模板 → 生成 → 沙箱 → Inspector → 注册
```

## 核心组件

- **TemplateLibrary**：模板库，预设常见 MCP Server 模式
- **CodeGenerator**：代码生成器，从模板生成完整 server 代码
- **SandboxRunner**：沙箱冒烟测试，验证生成代码可运行
- **InspectorValidator**：协议校验，确保符合 MCP 规范

## MCP Share

分享码导出/导入，bundle 打包（server files + config + metadata）。

## MCP 统一入口

所有 MCP server 通过统一入口访问：

- `list_servers`：列出已安装服务器
- `list_tools`：发现工具
- `call_tool`：调用工具
- `list_resources`：读取资源
- `list_prompts`：获取提示
