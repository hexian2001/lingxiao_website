---
title: 安全须知
description: Web server token、权限控制、密钥管理与安全最佳实践
---

# 安全须知

凌霄具有强大的系统操作能力：读写文件、执行终端命令、运行 Shell/Python、驱动浏览器、变更 Git 状态、生成和协调 Agent。请将 Web server token 视为对主机工作区的控制权。

## 本地优先

凌霄默认以本机工程目录为中心运行：

- SQLite 保存会话、任务、消息、Agent 状态
- 配置位于 `~/.lingxiao/settings.json`
- Web server token 保护本地 API

## Web Server Token

### 鉴权方式

| 端点族 | 鉴权方式 |
| --- | --- |
| `/health`、静态资源 | 公开 |
| `/api/v1/**` | server token（header `x-lingxiao-token` 或 `?token=` query） |
| `/api/v1/acp` | server token + ACP 凭据 |
| `/llm/*` | gateway virtual key |

- HTML 页面通过注入 `window.__LINGXIAO_TOKEN__` 引导后续请求
- 加固模式下禁用 `?token=` query，仅接受 header 鉴权

### 加固模式

非 loopback 绑定时自动启用加固模式：

- 禁用 query token，仅 header 接受 `x-lingxiao-token`
- 限流冷却 30 秒
- 非 localhost 请求不豁免限流
- 文件读写路由强制根路径包含检查
- Worker 任务 `write_scope` 隔离检查
- 终端会话必须使用工作区根目录内的 `cwd`

## 权限控制

### 权限模式

| 模式 | 说明 |
| --- | --- |
| `strict` | 所有写操作需确认（默认） |
| `dev` | 开发模式，放宽确认 |
| `networked` | 网络模式，允许网络工具 |
| `yolo` | 无需确认（谨慎使用） |

### 权限层

通过 `/mode`、`/allow-tool`、`/deny-tool`、`/ask-tool` 命令持久化到不同层级：

- `session`：SQLite `session_state`
- `project`：`.lingxiao/permissions.project.json`
- `local`：`.lingxiao/permissions.local.json`
- `user`：`~/.lingxiao/permissions.user.json`

### Worker 写入范围隔离

每个 Worker 任务可配置 `write_scope`，限制其文件写入范围。加固模式下强制检查，非加固模式下建议启用。

## 密钥管理

### 潜在密钥

- 模型提供商 API key（配置/凭据中）
- Git token
- Server token
- 浏览器 cookie / 会话状态
- 传递给工具的环境变量

### 规则

1. 不要通过 `/api/v1/settings` 暴露原始密钥（API 响应已脱敏）
2. 不要在生成的文档或日志中嵌入密钥
3. 用户自定义工具默认不应接收不受限的环境变量
4. UI/API 响应中 mask Git token 和 provider key
5. 不要将 token 放入 Git remote URL，使用 GitHub CLI 或凭据管理器

## Git 发布安全

推送新仓库前：

- 确认 `.gitignore` 排除了依赖、构建产物、本地运行时状态、归档、数据库和密钥
- 运行 `git status --short`，确认没有 `node_modules`、`dist`、`.lingxiao`、`.env`、SQLite、归档或含 token 的文件被暂存
- 运行 `rg` 密钥扫描，检查常见 token 前缀
- 保持 remote URL 干净（`https://github.com/owner/repo.git`，而非 `https://user:token@github.com/...`）

### 不应提交的文件

```text
node_modules/
dist/
.lingxiao/
*.db
*.db-wal
*.db-shm
.env
*.log
~/.lingxiao/
```

## 限流

- 进程内自调用（无 remoteAddress）→ 始终豁免
- 非加固模式 localhost → 豁免
- 加固模式 / 非 localhost → 不豁免，429 触发 30 秒冷却
- 本地 LLM Gateway 按 virtual key 配额：`rpm` / `tpm` / `daily_token_budget`

## Worktree 隔离

每个任务可在独立 Git worktree 中执行，避免工作目录冲突：

```bash
lingxiao start --worktree feature-x
```

退出时若有未提交变更，会询问是否保留 worktree。
