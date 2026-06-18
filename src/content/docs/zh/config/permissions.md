---
title: 权限系统
description: strict/dev/networked/yolo 四层权限模式与工具白名单
---

# 权限系统

凌霄的权限系统控制 Agent 工具的执行权限，支持四层权限模式和细粒度规则。

## 权限模式

| 模式 | 标签 | 说明 |
| --- | --- | --- |
| `strict` | strict | 最严格模式，所有写操作需确认 |
| `dev` | standard | 开发模式，标准权限控制 |
| `networked` | approved | 网络模式，网络工具需审批 |
| `yolo` | yolo | 最宽松模式，自动批准（默认） |

默认权限模式为 `yolo`，通过 `security.permission_mode` 配置。

### 设置权限模式

```bash
# 环境变量（加固模式单向锁）
export LINGXIAO_HARDENED_MODE=true
```

```json
{
  "security": {
    "permission_mode": "dev"
  }
}
```

### 沙箱后端

| 模式 | 沙箱后端 | 说明 |
| --- | --- | --- |
| `yolo` | `app-guard` | 轻量沙箱 |
| 其他模式 | `bubblewrap` | 强化沙箱 |

后端回退默认启用（`allowBackendFallback: true`）。

## 权限上下文

`ToolPermissionContext` 是持久化的策略对象：

```ts
interface ToolPermissionContext {
  mode: 'strict' | 'dev' | 'networked' | 'yolo';
  allowedHosts: string[];
  sandboxBackend: 'app-guard' | 'bubblewrap';
  allowBackendFallback: boolean;
  allowRules: Array<{ toolName: string; pattern?: string }>;
  denyRules: Array<{ toolName: string; pattern?: string }>;
  askRules: Array<{ toolName: string; pattern?: string }>;
}
```

## 持久化层级

有效权限按以下顺序合并（后者覆盖前者）：

| 层级 | 文件 | 说明 |
| --- | --- | --- |
| `user` | `~/.lingxiao/permissions.user.json` | 用户级 |
| `project` | `<workspace>/.lingxiao/permissions.project.json` | 项目级 |
| `local` | `<workspace>/.lingxiao/permissions.local.json` | 本地级 |
| `session` | SQLite `session_state` | 会话级 |

## 工具规则

三种规则类型控制工具执行：

### Allow 规则

自动批准匹配的工具调用：

```json
{
  "allowRules": [
    { "toolName": "file_read", "pattern": "src/**" },
    { "toolName": "code_search" }
  ]
}
```

### Deny 规则

拒绝匹配的工具调用：

```json
{
  "denyRules": [
    { "toolName": "shell", "pattern": "rm -rf *" }
  ]
}
```

### Ask 规则

需要用户确认才能执行：

```json
{
  "askRules": [
    { "toolName": "file_create", "pattern": "*.env" },
    { "toolName": "shell", "pattern": "npm publish" }
  ]
}
```

### 规则优先级

deny > ask > allow。同一工具匹配多条规则时，deny 优先。

## 网络主机白名单

`allowedHosts` 控制网络工具可访问的主机：

```json
{
  "allowedHosts": [
    "registry.npmjs.org",
    "api.github.com",
    "127.0.0.1"
  ]
}
```

## 安全配置

`security` 组的关键设置：

| 设置 | 默认值 | 说明 |
| --- | --- | --- |
| `permission_mode` | `yolo` | 权限模式 |
| `auto_allow_bash_if_sandboxed` | `true` | 沙箱内自动允许 bash |
| `dangerous_command_guard` | `false` | 危险命令拦截 |
| `block_private_network` | `false` | 阻止访问私有网络 |
| `identity_judge_llm_enabled` | `false` | LLM 身份二次判定 |
| `hardened_mode` | `false` | 加固模式 |
| `env_allowlist` | `[]` | 子进程环境变量白名单 |

### 加固模式

加固模式开启后：

- 禁用 query token，仅 header 接受鉴权
- 限流冷却 30 秒
- 强制 token 鉴权
- `dangerous_command_guard` 和 `block_private_network` 被强制开启
- `LINGXIAO_HARDENED_MODE` 环境变量为单向锁，设置后无法通过 API 关闭

## 权限请求与审批

当工具调用匹配 `ask` 规则或非 `yolo` 模式下的写操作时，系统发起权限请求：

1. **请求**：`permission:request` 事件广播到 WebUI
2. **审批**：用户在 WebUI 确认或拒绝
3. **结果**：`permission:resolved` 事件返回决策

### Eternal 模式下的权限

- 非 `yolo` 权限请求可能被自动批准
- `yolo` 请求仍需用户确认
- Eternal 模式启用时重放挂起的非 `yolo` 请求

## 审计日志

权限审计记录追加到 `session_state` 的 `PERMISSION_AUDIT_LOG`，保留最近的记录。
