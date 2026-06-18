---
title: Eternal自治
description: Leader 自主巡逻与自动重启
---

# Eternal 自治模式

Eternal 模式让 Leader 自主巡逻。

## 状态机

```text
IDLE → CHECK → PATROL → THINK → WAIT
```

基座 30 秒间隔指数退避，预算熔断 8 次连续失败暂停。

## EternalSupervisor

3 层健康检查：

1. **PID 检查**：进程存活
2. **Watchdog**：心跳超时检测
3. **HTTP 探测**：服务端口可达

## 自动重启

健康检查失败时自动重启 Leader 进程，保留会话状态。
