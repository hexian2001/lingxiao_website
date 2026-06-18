---
title: Eternal 自治模式
description: IDLE→CHECK→PATROL→THINK→WAIT 状态机、预算熔断、Supervisor 三层健康检查
lang: zh-CN
---

# Eternal 自治模式

Eternal 模式让 Leader 自主巡逻，无需人工干预即可持续监控和管理工程状态。通过状态机驱动、预算熔断和三层健康检查，确保自治模式安全可控。

## 状态机

```text
IDLE → CHECK → PATROL → THINK → WAIT → (循环)
```

| 状态 | 说明 |
| --- | --- |
| `IDLE` | 空闲等待，基座 30 秒间隔 |
| `CHECK` | 检查系统状态、任务队列和环境健康 |
| `PATROL` | 巡逻工程目录，检测文件变更和异常 |
| `THINK` | 分析发现的问题，决定是否需要行动 |
| `WAIT` | 等待下一个周期，指数退避 |

### 状态流转

```text
IDLE (30s) → CHECK → 有问题? → PATROL → THINK → 需要行动? → 执行
                    ↓                              ↓
                 无异常                         不需要
                    ↓                              ↓
                  WAIT ←──────────────────────────┘
                    ↓
                  IDLE (退避增长)
```

## 预算熔断

为防止 Eternal 模式失控，设有预算熔断机制：

- **连续失败计数**：记录连续失败次数
- **熔断阈值**：8 次连续失败后暂停 Eternal 模式
- **自动恢复**：熔断后需手动重启或 Supervisor 自动恢复
- **指数退避**：每次循环间隔随失败次数指数增长

```text
基座间隔: 30s
退避策略: 30s × 2^n (n = 连续失败次数)
熔断: 8 次连续失败 → 暂停
```

## EternalSupervisor

EternalSupervisor 提供三层健康检查和自动重启：

### 三层健康检查

| 层级 | 检查方式 | 说明 |
| --- | --- | --- |
| PID 检查 | 进程 PID 存活检测 | 检查 Eternal 进程是否在运行 |
| Watchdog | 心跳看门狗 | 检查 Eternal 是否在正常心跳 |
| HTTP 探针 | HTTP 健康端点 | 检查 Eternal 是否能正常响应 |

### 自动重启

当任一层级检查失败时，Supervisor 会：

1. 记录失败原因和时间
2. 清理残留进程和锁
3. 从 SQLite 恢复上次状态
4. 重启 Eternal 状态机
5. 如果连续重启失败超过阈值，进入完全停止状态并通知用户

## 配置

在 `~/.lingxiao/settings.json` 中配置 Eternal 模式：

```json
{
  "eternal": {
    "enabled": true,
    "baseInterval": 30000,
    "maxBackoff": 600000,
    "budgetCircuitBreaker": 8,
    "supervisor": {
      "enabled": true,
      "checkInterval": 60000,
      "httpTimeout": 5000
    }
  }
}
```

## 使用场景

- **持续监控**：长时间运行的工程需要自动巡检
- **自动修复**：检测到问题后自动触发修复流程
- **夜间巡逻**：非工作时间自动监控构建和测试状态
- **CI/CD 辅助**：持续观察部署状态并响应异常
