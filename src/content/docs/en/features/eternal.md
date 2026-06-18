---
title: Eternal Mode
description: Leader autonomous patrol and auto-restart
---

# Eternal Autonomous Mode

Eternal mode enables Leader autonomous patrol.

## State Machine

```text
IDLE → CHECK → PATROL → THINK → WAIT
```

30-second base interval with exponential backoff. Budget circuit breaker after 8 consecutive failures.

## EternalSupervisor

3-layer health check: PID check, watchdog heartbeat, HTTP probe.

## Auto-Restart

Automatic Leader process restart on health check failure, preserving session state.
