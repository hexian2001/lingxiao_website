---
title: Eternal Autonomous Mode
description: IDLE→CHECK→PATROL→THINK→WAIT state machine, budget circuit breaker, Supervisor 3-layer health check
---

# Eternal Autonomous Mode

Eternal mode lets the Leader self-patrol, continuously monitoring and managing engineering state without human intervention. Through state machine drive, budget circuit breaking, and 3-layer health checks, the autonomous mode is safe and controllable.

## State Machine

```text
IDLE → CHECK → PATROL → THINK → WAIT → (loop)
```

| State | Description |
| --- | --- |
| `IDLE` | Idle waiting, base 30-second interval |
| `CHECK` | Check system status, task queue, and environment health |
| `PATROL` | Patrol engineering directory, detect file changes and anomalies |
| `THINK` | Analyze discovered issues, decide whether action is needed |
| `WAIT` | Wait for next cycle, exponential backoff |

### State Flow

```text
IDLE (30s) → CHECK → Issues found? → PATROL → THINK → Action needed? → Execute
                      ↓                                ↓
                   No issues                         Not needed
                      ↓                                ↓
                    WAIT ←─────────────────────────────┘
                      ↓
                    IDLE (backoff increases)
```

## Budget Circuit Breaker

To prevent Eternal mode from running away, a budget circuit breaker is in place:

- **Consecutive failure counter**: Tracks consecutive failure count
- **Circuit breaker threshold**: Pauses Eternal mode after 8 consecutive failures
- **Auto recovery**: After circuit breaking, requires manual restart or Supervisor auto-recovery
- **Exponential backoff**: Cycle interval grows exponentially with failure count

```text
Base interval: 30s
Backoff strategy: 30s × 2^n (n = consecutive failure count)
Circuit breaker: 8 consecutive failures → pause
```

## EternalSupervisor

EternalSupervisor provides 3-layer health checks and auto-restart:

### 3-Layer Health Check

| Layer | Check Method | Description |
| --- | --- | --- |
| PID Check | Process PID liveness detection | Check if the Eternal process is running |
| Watchdog | Heartbeat watchdog | Check if Eternal is heartbeating normally |
| HTTP Probe | HTTP health endpoint | Check if Eternal can respond normally |

### Auto Restart

When any layer check fails, the Supervisor will:

1. Record the failure reason and time
2. Clean up residual processes and locks
3. Restore last state from SQLite
4. Restart the Eternal state machine
5. If consecutive restart failures exceed the threshold, enter a full stop state and notify the user

## Configuration

Configure Eternal mode in `~/.lingxiao/settings.json`:

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

## Use Cases

- **Continuous monitoring**: Long-running engineering projects needing automatic inspection
- **Auto repair**: Automatically trigger repair flows when issues are detected
- **Night patrol**: Monitor build and test status during off-hours
- **CI/CD assistance**: Continuously observe deployment status and respond to anomalies
