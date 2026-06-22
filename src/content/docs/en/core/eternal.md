---
title: Eternal Autonomous Mode
description: IDLE→CHECK→PATROL→THINK→WAIT state machine, budget circuit breaker, Supervisor 3-layer health check
---

# Eternal Autonomous Mode

Eternal mode lets the Leader self-patrol, continuously monitoring and managing engineering state without human intervention. Through state machine drive, budget circuit breaking, and 3-layer health checks, the autonomous mode is safe and controllable.

## State Machine

<div class="doc-flow doc-flow-loop" role="img" aria-label="Eternal state machine: IDLE, CHECK, PATROL, THINK, WAIT, then loop.">
  <span>IDLE</span><i>→</i><span>CHECK</span><i>→</i><span>PATROL</span><i>→</i><span>THINK</span><i>→</i><span>WAIT</span><i>↺</i><strong>loop</strong>
</div>

| State | Description |
| --- | --- |
| `IDLE` | Idle waiting, base 30-second interval |
| `CHECK` | Check system status, task queue, and environment health |
| `PATROL` | Patrol engineering directory, detect file changes and anomalies |
| `THINK` | Analyze discovered issues, decide whether action is needed |
| `WAIT` | Wait for next cycle, exponential backoff |

### State Flow

<div class="doc-decision-flow" role="img" aria-label="Eternal state flow: IDLE→CHECK→Issues?→PATROL→THINK→Action?→Execute. Branches: ↘No issues→WAIT→IDLE backoff, ↘Not needed→WAIT.">
  <div class="dc-row">
    <span>IDLE (30s)</span><i> → </i><span>CHECK</span><i> → </i><span>Issues?</span><i> → </i><span>PATROL</span><i> → </i><span>THINK</span><i> → </i><span>Action?</span><i> → </i><strong>Execute</strong>
  </div>
  <div class="dc-row">
    <i class="dc-fork">↘</i><span>No issues</span><i> → </i><span>WAIT</span><i> → </i><span>IDLE (backoff)</span>
    <i class="dc-fork dc-fork-2">↘</i><span>Not needed</span><i> → </i><span>WAIT</span>
  </div>
</div>

## Budget Circuit Breaker

To prevent Eternal mode from running away, a budget circuit breaker is in place:

- **Consecutive failure counter**: Tracks consecutive failure count
- **Circuit breaker threshold**: Pauses Eternal mode after 8 consecutive failures
- **Auto recovery**: After circuit breaking, requires manual restart or Supervisor auto-recovery
- **Exponential backoff**: Cycle interval grows exponentially with failure count

<dl class="doc-kv-flow" aria-label="Eternal budget circuit breaker parameters">
  <div><dt>Base interval</dt><dd>30s</dd></div>
  <div><dt>Backoff strategy</dt><dd>30s × 2^n (n = consecutive failure count)</dd></div>
  <div><dt>Circuit breaker</dt><dd>8 consecutive failures → pause</dd></div>
</dl>

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
