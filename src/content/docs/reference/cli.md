---
title: CLI 命令参考
description: 凌霄命令行完整命令树与选项参考
---

# CLI 命令参考

凌霄 CLI（`lingxiao`）是系统的主入口，基于 Commander.js 构建。它启动 TUI 交互界面和 WebUI 服务，同时提供会话管理、环境诊断、后台守护、Git Worktree 管理和自定义 Agent 定义等子命令。

## 命令树概览

```text
lingxiao                  # 默认启动 TUI + WebUI（等同于 lingxiao start）
lingxiao start            # 启动会话
lingxiao list             # 列出所有会话
lingxiao init             # 首次配置向导
lingxiao doctor           # 环境诊断
lingxiao about            # 显示关于信息
lingxiao demo <id>        # 演示模式启动指定会话
lingxiao agents ...       # 管理自定义 Agent 定义
lingxiao daemon ...       # 管理后台常驻服务
lingxiao worktree ...     # 管理 Git Worktree
```

## lingxiao start

启动一个凌霄会话，默认同时启动 TUI 和 WebUI。

```bash
lingxiao start [选项]
```

### 选项

| 选项 | 说明 |
| --- | --- |
| `--bg` | 后台运行（不显示 TUI，只启动服务） |
| `--name <name>` | 指定会话名称 |
| `--output-format <format>` | 输出格式（`text` \| `stream-json`），默认 `text` |
| `--daemon-mode` | 由 DaemonManager 内部使用，不直接调用 |
| `--worktree [name]` | 在隔离的 Git Worktree 中运行 |
| `--worktree-branch <branch>` | 指定 Worktree 创建的分支名 |
| `--tmux` | 使用 tmux 窗格分割（实验性） |
| `-s, --session <id>` | 恢复指定会话 ID |

### 示例

```bash
# 默认启动
lingxiao

# 后台运行，仅 WebUI
lingxiao start --bg --name my-project

# 在隔离 Worktree 中运行
lingxiao start --worktree feature-x

# 恢复已有会话
lingxiao start --session abc123
```

## lingxiao list

列出所有已保存的会话。

```bash
lingxiao list
```

输出包括会话 ID、创建时间、消息数和状态。

## lingxiao init

首次配置向导，引导用户完成模型连接、权限设置等初始化。

```bash
lingxiao init [选项]
```

| 选项 | 说明 |
| --- | --- |
| `--check` | 只运行内置环境检测，不进入交互式配置 |

```bash
# 完整交互式配置
lingxiao init

# 仅环境检测
lingxiao init --check
```

## lingxiao doctor

运行运行时环境诊断，检查 Node.js 版本、Git、依赖、端口等。

```bash
lingxiao doctor [选项]
```

| 选项 | 说明 |
| --- | --- |
| `--json` | 输出 JSON 格式报告 |

退出码 `0` 表示环境就绪，`1` 表示存在问题。

## lingxiao about

显示凌霄版本、愿景和技术栈信息。

```bash
lingxiao about
```

## lingxiao agents

管理自定义 Agent 定义，支持创建、查看、更新、删除操作。

### agents list

列出自定义 Agent 定义。

| 选项 | 说明 |
| --- | --- |
| `--all` | 显示被 project/global 覆盖隐藏的同名定义 |
| `--json` | 输出 JSON |

### agents show

查看指定 Agent 的详细定义。

```bash
lingxiao agents show <name> [选项]
```

| 选项 | 说明 |
| --- | --- |
| `--global` | 查看全局定义 |
| `--project` | 查看当前项目定义 |
| `--json` | 输出 JSON |

### agents create

创建自定义 Agent。

```bash
lingxiao agents create <name> [选项]
```

| 选项 | 说明 |
| --- | --- |
| `--description <text>` | Agent 描述 |
| `--prompt <text>` | Agent system prompt |
| `--prompt-file <path>` | 从文件读取 system prompt |
| `--base-role <name>` | 继承的内置角色基线 |
| `--model <model>` | 该 Agent 默认模型 |
| `--backend <backend>` | Worker 后端：`worker_process` \| `claude` \| `codex` |
| `--tool <name>` | 允许工具，可重复或逗号分隔 |
| `--skill <name>` | 默认技能，可重复或逗号分隔 |
| `--global` | 写入全局 `~/.lingxiao/agents` |
| `--project` | 写入当前项目 `.lingxiao/agents` |
| `--json` | 输出 JSON |

### agents update

更新已有自定义 Agent 定义，选项与 `create` 相同。

### agents delete

删除自定义 Agent 定义。

| 选项 | 说明 |
| --- | --- |
| `--global` | 删除全局定义 |
| `--project` | 删除当前项目定义 |
| `-y, --yes` | 跳过确认 |

## lingxiao daemon

管理凌霄后台常驻服务（Daemon 模式）。

### daemon start

| 选项 | 说明 |
| --- | --- |
| `-p, --port <port>` | 端口号，默认 `8080` |
| `-H, --host <host>` | 监听地址，默认 `127.0.0.1` |
| `-s, --session <id>` | 指定要恢复的会话 ID |
| `--supervisor` | 启用进程自愈守护（崩溃自动重启） |

### daemon stop / restart / status

```bash
lingxiao daemon stop
lingxiao daemon restart [-p <port>] [-H <host>]
lingxiao daemon status
```

### daemon supervisor-status / stop-supervisor

```bash
lingxiao daemon supervisor-status
lingxiao daemon stop-supervisor
```

### daemon ps / logs / kill / attach

```bash
lingxiao daemon ps
lingxiao daemon logs <name> [-f] [-n <lines>]
lingxiao daemon kill <name> [-f]
lingxiao daemon attach <name>
```

## lingxiao worktree

管理 Git Worktree，为任务提供隔离的工作目录。

```bash
lingxiao worktree list
lingxiao worktree remove <name> [--keep-branch]
lingxiao worktree prune
```

## 配置文件

```text
~/.lingxiao/settings.json    # 全局配置
~/.lingxiao/port             # Web 服务端口记录
~/.lingxiao/agents/          # 全局自定义 Agent 定义
.lingxiao/agents/            # 项目级自定义 Agent 定义
.lingxiao/permissions.*.json # 项目级权限配置
```

## 环境变量

| 变量 | 说明 |
| --- | --- |
| `LINGXIAO_WEB_HOST` | Web 服务监听地址 |
| `LINGXIAO_WEB_PORT` | Web 服务端口 |
| `LINGXIAO_NO_AUTO_START` | 设为 `1` 时禁止自动启动 |
| `LINGXIAO_DAEMON_MODE` | Daemon 模式标记 |
| `LINGXIAO_SESSION_NAME` | 会话名称 |
| `LINGXIAO_LOG_PATH` | 日志文件路径 |
| `FORCE_NO_TUI` | 设为 `1` 时强制禁用 TUI |

