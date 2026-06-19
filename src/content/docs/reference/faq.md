---
title: FAQ
description: 常见问题解答
---

# 常见问题

## 凌霄和普通 AI 编码工具有什么区别？

凌霄不是聊天壳，而是编排内核——一剑开天，做你所想。核心区别：

- **专家团**：Leader + Worker 多角色协同，而非单 Agent 对话
- **DAG 编排**：带依赖关系的任务图，并行执行
- **全状态同步**：WebUI/TUI/CLI 三端实时同步
- **可恢复**：SQLite 持久化，崩溃后可恢复
- **验收闭环**：结构化验收 + 对抗验证

## 需要什么 Node.js 版本？

Node.js `>=24.0.0`。运行 `lingxiao doctor` 检查环境。

## 支持哪些 LLM？

- **OpenAI**（及兼容接口：DeepSeek、Qwen、Moonshot/Kimi、Gemini、Groq、SiliconFlow 等）
- **Anthropic**

通过环境变量或 `~/.lingxiao/settings.json` 配置。详见 [连接模型](../getting-started/connect-models)。

## 数据存储在哪里？

| 类型 | 位置 |
| --- | --- |
| 全局配置 | `~/.lingxiao/settings.json` |
| 数据库 | `~/.lingxiao/` 下的 SQLite 文件 |
| 项目级配置 | `.lingxiao/` 目录 |
| 自定义 Agent（全局） | `~/.lingxiao/agents/` |
| 自定义 Agent（项目） | `.lingxiao/agents/` |
| 权限配置 | `.lingxiao/permissions.*.json` |

## 如何恢复崩溃的会话？

```bash
lingxiao list            # 列出所有会话
lingxiao --session <id>  # 恢复指定会话
```

所有会话状态（消息、任务 DAG、Agent 状态）持久化到 SQLite，崩溃后可完整恢复。

## 如何配置权限模式？

四种模式：

| 模式 | 说明 |
| --- | --- |
| `strict` | 所有写操作需确认（默认） |
| `dev` | 开发模式，放宽确认 |
| `networked` | 网络模式，允许网络工具 |
| `yolo` | 无需确认（谨慎使用） |

通过 `/mode` slash 命令或 `~/.lingxiao/settings.json` 中 `tools.permissionMode` 设置。

权限可持久化到四个层级：`session`、`project`、`local`、`user`。

## WebUI 如何访问？

启动凌霄后，终端会打印带 token 的 URL，如：

```text
http://127.0.0.1:8080/?token=xxxxxxxx
```

端口信息写入 `~/.lingxiao/port`。非 localhost 绑定时自动启用加固模式。

## 如何使用 Git Worktree 隔离？

```bash
# 启动时使用 worktree
lingxiao start --worktree feature-x

# 管理已有 worktree
lingxiao worktree list
lingxiao worktree remove <name>
lingxiao worktree prune
```

每个任务可在独立 Git worktree 中执行，避免工作目录冲突。

## 如何使用后台模式？

```bash
# 后台启动
lingxiao start --bg --name my-project

# Daemon 模式
lingxiao daemon start -p 8080
lingxiao daemon status
lingxiao daemon stop

# 查看日志
lingxiao daemon logs <name> -f
```

## 如何使用 Eternal 自治模式？

```bash
# 在 TUI/WebUI 中使用 slash 命令
/eternal <goal>       # 设置长期目标
/eternal status       # 查看状态
/eternal pause        # 暂停
/eternal resume       # 恢复
```

Eternal 模式按 30 秒基础间隔循环，指数退避最大 960 秒，连续 8 次失败自动暂停。

## 如何使用本地 LLM Gateway？

在 `~/.lingxiao/settings.json` 中启用：

```json
{
  "llm_gateway": {
    "enabled": true,
    "provider": "openai",
    "model": "gpt-4o",
    "default_rpm": 60,
    "default_tpm": 200000
  }
}
```

启用后可通过 `/llm/openai/v1/**` 和 `/llm/anthropic/v1/**` 端点访问，使用虚拟密钥鉴权。

## 如何自定义 Agent？

```bash
# 创建自定义 Agent
lingxiao agents create my-agent \
  --description "我的 Agent" \
  --base-role backend \
  --model gpt-4o-mini

# 查看所有 Agent
lingxiao agents list
```

## 如何安装 MCP 服务器？

在 TUI/WebUI 中使用 slash 命令：

```bash
/mcp list                    # 列出已配置的服务器
/mcp search <query>          # 搜索市场
/mcp install <entry-id>      # 安装
/mcp add-stdio <id> <cmd>    # 手动添加 stdio 服务器
/mcp add-remote <id> <url>   # 手动添加 HTTP 服务器
```
