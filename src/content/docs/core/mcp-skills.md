---
title: MCP 与 Skills
description: MCP Server 管理、分享码、Skills 4 层优先级
---

# MCP 与 Skills

凌霄通过 MCP 协议和 Skills 技能系统，让 Agent 的能力可扩展、可分享、可注入。

## MCP Share

MCP Share 提供分享码导出/导入功能，方便跨环境分享 MCP Server：

- **导出**：生成分享码，打包 server files + config + metadata 为 bundle
- **导入**：通过分享码导入 MCP Server，自动验证和注册
- **预览**：导入前可预览 bundle 内容

### 分享码结构

```typescript
interface McpBundle {
  serverFiles: Record<string, string>;  // 源码文件
  config: McpServerConfig;              // MCP 配置
  metadata: {
    name: string;
    description: string;
    version: string;
    createdAt: string;
  };
}
```

## Skills 技能系统

Skills 是注入 Agent 上下文的执行知识、流程和领域约束。

### 4 层来源优先级

<div class="doc-flow doc-flow-priority" role="img" aria-label="Skills 来源优先级：项目级高于插件贡献，高于用户级，高于内置。">
  <strong>项目级</strong><i>›</i><span>插件贡献</span><i>›</i><span>用户级</span><i>›</i><span>内置</span>
</div>

| 来源 | 路径 | 说明 |
| --- | --- | --- |
| 项目级 | `.lingxiao/skills/` | 当前项目专属技能，最高优先级 |
| 插件贡献 | 插件 `skills/` 目录 | 通过插件市场安装的技能 |
| 用户级 | `~/.lingxiao/skills/` | 用户全局技能，跨项目可用 |
| 内置 | 随凌霄分发 | 内置技能包 |

### Skill 结构

每个 Skill 由 YAML frontmatter 和 Markdown 正文组成：

```yaml
---
name: security-review
description: 安全审查技能
phases:
  - analyze
  - review
  - report
priority: high
---

# 安全审查流程

## 分析阶段
检查依赖漏洞、输入验证、权限边界...

## 审查阶段
逐文件审查安全风险...

## 报告阶段
生成安全审查报告...
```

### 阶段加载

Skill 支持按阶段分文件加载：

<div class="doc-file-tree" role="img" aria-label="Skill 阶段文件结构：security-review 包含 index.md 和 phases 下的 analyze、review、report 文件。">
  <div><strong>skills/</strong></div>
  <div><span>security-review/</span></div>
  <div><span>index.md</span><em>Skill 主文件（frontmatter）</em></div>
  <div><span>phases/</span></div>
  <div><span>analyze.md</span><em>分析阶段知识</em></div>
  <div><span>review.md</span><em>审查阶段知识</em></div>
  <div><span>report.md</span><em>报告阶段知识</em></div>
</div>

每个阶段文件经过 Quality Gate 校验后才注入 Worker prompt。

### 技能绑定

Leader 在 `define_agent_role` 或 `create_task` 中通过 `skill_names` 绑定技能：

```typescript
{
  name: "security-auditor",
  skillNames: ["security-review", "owasp-top10"],
  // Worker dispatch 时自动注入这些 Skill 的内容
}
```

## MCP 统一入口

所有 MCP Server 通过统一 `mcp` 工具入口访问：

```text
mcp(action="list_servers")       # 列出已安装 MCP Server
mcp(action="list_tools")         # 发现 MCP Tools
mcp(action="call_tool", ...)     # 调用 MCP Tool
mcp(action="list_resources")     # 发现 MCP Resources
mcp(action="read_resource", ...) # 读取 MCP Resource
mcp(action="list_prompts")       # 发现 MCP Prompts
mcp(action="get_prompt", ...)    # 获取 MCP Prompt
```

插件贡献的 MCP Server 会同步到 `settings.mcp.servers`，与手动安装的 Server 统一管理。
