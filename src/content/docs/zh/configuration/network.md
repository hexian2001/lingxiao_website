---
title: 网络
description: Web 服务端口与代理配置
---

# 网络

## Web 服务

| 配置项 | 环境变量 | 默认值 |
| --- | --- | --- |
| Host | `LINGXIAO_WEB_HOST` | `127.0.0.1` |
| Port | `LINGXIAO_WEB_PORT` | 自动分配 |
| 开发代理 | `LINGXIAO_WEB_PROXY_TARGET` | - |

## 开发代理

```bash
LINGXIAO_WEB_PORT=8787 npm run cli
cd web
LINGXIAO_WEB_PROXY_TARGET=http://127.0.0.1:8787 npm run dev
```

## 加固模式

非 loopback 绑定时启用加固模式：

- 禁用 query token，仅 header 接受
- 限流冷却 30s
- 强制 token 鉴权
