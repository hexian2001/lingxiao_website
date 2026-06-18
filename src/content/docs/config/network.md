---
title: 网络配置
description: Web 服务端口、代理与 allowed_hosts 配置
---

# 网络配置

凌霄的网络配置涵盖 Web 服务、代理、主机白名单和加固模式。

## Web 服务

| 配置项 | 环境变量 | 配置路径 | 默认值 |
| --- | --- | --- | --- |
| Host | `LINGXIAO_WEB_HOST` | `server.host` | `127.0.0.1` |
| Port | `LINGXIAO_WEB_PORT` | `server.port` | 自动分配 |
| 开发代理 | `LINGXIAO_WEB_PROXY_TARGET` | - | - |

### 开发模式

```bash
# 启动 CLI + Web 服务
LINGXIAO_WEB_PORT=8787 npm run cli

# 另一终端启动 Vite 开发服务器
cd web
LINGXIAO_WEB_PROXY_TARGET=http://127.0.0.1:8787 npm run dev
```

## 代理配置

`network` 组控制代理行为：

| 设置 | 环境变量 | 说明 |
| --- | --- | --- |
| `network.proxy.url` | `LINGXIAO_PROXY_URL` | 代理 URL |
| `network.proxy.llm_enabled` | `LINGXIAO_PROXY_LLM` | LLM 请求走代理 |
| `network.proxy.tools_enabled` | `LINGXIAO_PROXY_TOOLS` | 工具请求走代理 |
| `network.user_agent` | `LINGXIAO_USER_AGENT` | 自定义 User-Agent |

### 代理配置示例

```json
{
  "network": {
    "proxy": {
      "url": "http://127.0.0.1:7890",
      "llm_enabled": true,
      "tools_enabled": false
    },
    "user_agent": "LingXiao/0.3"
  }
}
```

## 主机白名单

`allowedHosts` 控制网络工具可访问的主机列表：

```json
{
  "allowedHosts": [
    "registry.npmjs.org",
    "api.github.com",
    "pypi.org",
    "127.0.0.1",
    "localhost"
  ]
}
```

未在白名单中的主机访问将被拒绝。

## 限流

| 场景 | 行为 |
| --- | --- |
| 进程内自调用 | 始终豁免 |
| 非加固模式 localhost | 豁免 |
| 加固模式 / 非 localhost | 不豁免，429 触发冷却 |
| 非 loopback 绑定且未加固 | 强警告（不门控） |

## 加固模式

非 loopback 绑定时建议启用加固模式：

```bash
export LINGXIAO_HARDENED_MODE=true
```

加固模式开启后：

- **鉴权**：禁用 query token，仅 header `x-lingxiao-token` 接受
- **限流**：触发 429 后冷却 30 秒
- **安全**：`dangerous_command_guard` 和 `block_private_network` 强制开启
- **单向锁**：环境变量设置后无法通过 API 关闭

### 非安全绑定警告

当检测到非 loopback 绑定且未启用加固模式时，系统输出强警告日志，但不阻止启动。

## LLM 网关网络

本地 LLM 网关（端口 62000）的网络行为：

- 网关路由使用虚拟 Key 鉴权，不走 server token
- 按 virtual key 配额限流：`rpm` / `tpm` / `daily_token_budget`
- 命中限流返回 429 + 错误体
