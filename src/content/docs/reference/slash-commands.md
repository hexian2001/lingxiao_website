---
title: Slash 命令
description: 内置 Slash 命令完整列表与说明
---

# Slash 命令

凌霄内置 66 个 Slash 命令，在 TUI 和 WebUI 聊天输入中均可使用。命令注册源为 `src/commands/slash_registry.ts`，回调派发由 `src/commands/dispatcher.ts` 处理。

## 命令生命周期

<div class="doc-sequence" role="img" aria-label="Slash 命令生命周期：Web 或 TUI 输入先由 registry 识别，再经 ACP 到 dispatcher，必要时触发 SessionManager，最后返回 JSON RPC 结果。">
  <div><span>Web / TUI 输入</span><i>→</i><span>slash_registry</span><em>检测 slash 命令和元数据</em></div>
  <div><span>Web / TUI 输入</span><i>→</i><span>AcpHandler session/command</span><em>session/command {command, args}</em></div>
  <div><span>AcpHandler</span><i>→</i><span>dispatchCallbackCommand</span><em>commandLine + context</em></div>
  <div><span>dispatchCallbackCommand</span><i>→</i><span>SessionManager</span><em>可选运行时操作</em></div>
  <div><span>CommandResult</span><i>→</i><strong>JSON-RPC 结果</strong></div>
</div>

## 处理器类型

| 处理器 | 含义 | 说明 |
| --- | --- | --- |
| `tui-local` | 客户端本地处理，不调用后端 | 用于视图切换、帮助、退出等纯前端操作 |
| `callback` | 必须发送到后端 dispatcher | 用于运行时状态、会话、工具、权限、模型、工作流等 |

## 命令分类

| 分类 | 用途 |
| --- | --- |
| `session` | 会话生命周期与历史 |
| `view` | TUI/Web 面板与报告 |
| `permission` | 工具权限与审批控制 |
| `project` | 编排项目控制 |
| `model` | 模型、语言与配置 |
| `tools` | 运行时工具、插件、网络辅助、技能 |
| `misc` | 帮助、诊断、退出等未分类命令 |

## 会话命令

| 命令 | 处理器 | 说明 |
| --- | --- | --- |
| `/resume` | callback | 恢复会话或打开恢复弹窗 |
| `/session` | callback | 显示当前会话/工作区/权限摘要 |
| `/clear` | callback | 清空当前对话（数据库和内存） |
| `/compact` | callback | 强制 Leader 上下文压缩 |
| `/fork` | callback | `/fork [messageId]`；从指定消息分叉会话（当前已注册但无处理函数） |
| `/dream` | callback | 将检查点整合为结构化 `MEMORY.md` |
| `/history` | callback | 最近会话弹窗 |
| `/stop` | callback | 中断当前会话 |

## 视图命令

| 命令 | 处理器 | 说明 |
| --- | --- | --- |
| `/tasks` | tui-local | 打开任务板/DAG 视图 |
| `/agents` | tui-local | 打开 Agent 总览 |
| `/graph` | tui-local | 打开知识图谱/黑板视图 |
| `/notes` | tui-local | 打开工作笔记 |
| `/git` | tui-local | 打开 Git 工作区面板 |
| `/changes` | callback | 文件变更/检查点报告 |
| `/main` | tui-local | 返回主频道 |
| `/refresh` | callback | 刷新当前会话快照 |
| `/reset` | tui-local | 重置当前视图 |

## 权限命令

| 命令 | 处理器 | 说明 |
| --- | --- | --- |
| `/permissions` | callback | 权限有效层/待审批弹窗 |
| `/mode` | callback | `/mode <strict|dev|networked|yolo> [session|project|local|user]` |
| `/allow-tool` | callback | 添加允许规则 |
| `/deny-tool` | callback | 添加拒绝规则 |
| `/ask-tool` | callback | 添加询问规则 |
| `/approve` | callback | 批准待处理权限或计划 |
| `/deny` | callback | 拒绝待处理权限请求 |

### 权限层目标

`/mode`、`/allow-tool`、`/deny-tool`、`/ask-tool` 支持持久化到不同层级：

- `session`：SQLite `session_state`，键 `TOOL_PERMISSION_CONTEXT`
- `project`：`.lingxiao/permissions.project.json`
- `local`：`.lingxiao/permissions.local.json`
- `user`：`~/.lingxiao/permissions.user.json`

未指定时默认写入 `session`。

## 项目编排命令

| 命令 | 处理器 | 说明 |
| --- | --- | --- |
| `/eternal` | callback | `/eternal <goal>|status|pause|resume|clear|delete|set`；管理 Eternal 长期目标 |
| `/team` | callback | `/team status|on|off`；显示或切换协作模式 |
| `/route` | callback | `/route <auto|direct|hybrid|delegate>`；设置 Leader 执行路由偏好 |
| `/projects` | callback | 编排项目板 |
| `/project-pause` | callback | 暂停当前项目 |
| `/project-resume` | callback | 恢复当前项目 |
| `/project-priority` | callback | `/project-priority <critical|high|normal|low>` |
| `/project-replan` | callback | 强制当前项目重新规划 |
| `/project-reset` | callback | 强制恢复/重置当前项目 |
| `/project-unblock` | callback | `/project-unblock <dependency-id>` |
| `/project-archive` | callback | 归档当前项目 |
| `/intervene` | callback | `/intervene @agent <message>` |
| `/cancel-task` | callback | `/cancel-task <task-id> [reason]` |
| `/broadcast` | callback | 向所有 Agent 广播消息 |

## 模型与配置命令

| 命令 | 处理器 | 说明 |
| --- | --- | --- |
| `/models` | callback | 列出已配置模型（按 provider 分组） |
| `/model` | callback | `/model <model-id>`；更新 Leader 模型并持久化 |
| `/language` | tui-local | `/language <zh|en>` |
| `/config` | tui-local | `/config | /config set <key> <value> | /config reset <key> | /config reset-all | /config init` |

## 工具与插件命令

| 命令 | 处理器 | 说明 |
| --- | --- | --- |
| `/bughunt` | callback | `/bughunt [target]`；启动或恢复 bughunt 账本 |
| `/bughunt-status` | callback | 显示 bughunt 账本摘要 |
| `/bughunt-report` | callback | 从账本生成 bughunt 报告 |
| `/office` | callback | `/office [on|off]`；切换 Office 插件 |
| `/workflow` | callback | `/workflow [on|off]`；切换工作流工具注入 |
| `/skills` | callback | 技能来源和角色技能弹窗 |
| `/hooks` | callback | Hooks 配置报告 |
| `/fetch` | callback | `/fetch <url>`；抓取 URL 内容 |
| `/search` | callback | `/search <query>`；网络搜索辅助 |
| `/ls` | callback | `/ls <path>`；目录预览 |
| `/open` | callback | `/open <path>`；读取前 200 行 |
| `/loop` | callback | `/loop [interval] <prompt>`；循环任务管理 |

### 插件切换语义

| 命令 | 会话键 | 运行时效果 |
| --- | --- | --- |
| `/office` | `OFFICE_MODE_ACTIVE` | 启用 Office 文档/画布能力 |
| `/workflow` | `WORKFLOW_MODE_ACTIVE` | 暴露工作流 Leader 工具 |

## MCP 命令

`/mcp` 是 MCP 服务器管理的 slash 命令入口，与 ToolRegistry 的 `mcp` 工具共享同一配置和运行时客户端。

| 子命令 | 说明 |
| --- | --- |
| `/mcp list` | 列出已配置的服务器 |
| `/mcp search <query>` | 动态查询市场源 |
| `/mcp install <entry-id>` | 安装市场 MCP 条目 |
| `/mcp tools [server-id]` | 查看服务器暴露的工具 |
| `/mcp call <server-id> <tool-name> [args]` | 调用服务器工具 |
| `/mcp resources [server-id]` | 查看服务器资源 |
| `/mcp read-resource <server-id> <uri>` | 读取服务器资源 |
| `/mcp prompts [server-id]` | 查看服务器 prompts |
| `/mcp get-prompt <server-id> <prompt-name> [args]` | 获取 prompt |
| `/mcp templates [server-id]` | 列出资源模板 |
| `/mcp snapshot [server-id]` | 显示初始化能力快照 |
| `/mcp add-remote <id> <url> [name]` | 创建 streamable-http 服务器 |
| `/mcp add-stdio <id> <command> [args...]` | 创建 stdio 服务器 |

## 其他命令

| 命令 | 处理器 | 说明 |
| --- | --- | --- |
| `/help` | tui-local | 显示分组帮助 |
| `/doctor` | callback | 运行时诊断弹窗 |
| `/quit` | tui-local | 退出客户端 |
| `/exit` | tui-local | 退出客户端 |

## 命令结果类型

每个命令结果携带 `content` 字符串和可选 `type`。结果通过 `action` 字段区分：

| 类型 | action | 附加字段 |
| --- | --- | --- |
| `CommandMessageResult` | 无 | 无，纯系统消息 |
| `CommandResumeModalResult` | `resume_modal` | `sessions` |
| `CommandItemsModalResult` | `history_modal` / `skills_modal` / `doctor_modal` / `permissions_modal` / `projects_modal` | `items` |
| `CommandReportModalResult` | `report_modal` | `title`, `report` |
| `CommandHydrateResult` | `hydrate` | `sessionStatus`, `tasks`, `messages`, `channels`, `tokenUsage?`, `agentTokens?`, `leaderStatus`, `leaderMode?`, `leaderReason?` |

## 已知限制

- `/fork` 已注册为 `callback` 类型，但 `dispatcher.ts` 的 `commandRegistry` 中无对应处理函数，当前不可用。

## 演进规则

1. 新增 slash 命令必须注册到 `slash_registry.ts`
2. `handledBy` 为 `callback` 的命令必须在 `dispatcher.ts` 中添加处理逻辑
3. Web 自动补全仅在后端注册表存在后更新
4. 新命令结果动作必须在此文档记录并由目标客户端处理
5. 同义命令（如 `/quit` 和 `/exit`）注册为独立条目，命令名不做归一化
