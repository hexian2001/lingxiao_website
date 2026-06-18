---
title: Task DAG Orchestration
description: Dependency-aware task graph scheduling, parallel execution, and state recovery
---

# Task DAG Orchestration

Complex goals are decomposed into a dependency-aware task graph (DAG). The Leader handles task decomposition, dependency establishment, and execution scheduling, making complex engineering work schedulable, recoverable, and auditable.

## Task Graph Structure

```text
T-1 Requirements
  ├─ T-2 Architecture
  │    ├─ T-3 Backend
  │    └─ T-4 Frontend
  ├─ T-5 Testing
  └─ T-6 Docs & Release
```

Each node is a task; arrows represent dependencies. Tasks without dependencies execute automatically in parallel; tasks with dependencies are unlocked in order.

## DAG Engineering Benefits

- **Parallel tasks run in parallel**: Tasks without dependencies execute automatically, maximizing throughput
- **Dependent tasks unlock in order**: Completion of prerequisites automatically triggers downstream tasks
- **Each task has**: owner, status, blocking relationships, results, evidence, and recovery info
- **WebUI visualization**: Task graph, Agent panel, Review evidence, and runtime status
- **Leader global scheduling**: Scheduling, supervision, recovery, and wrap-up based on DAG

## Task State Transitions

```text
pending → dispatched → in_progress → completed
                                   → failed
                                   → blocked
```

| State | Description |
| --- | --- |
| `pending` | Task created, waiting for dependencies to complete |
| `dispatched` | Dispatched to Worker, waiting to start |
| `in_progress` | Worker executing |
| `completed` | Execution complete, result verified |
| `failed` | Execution failed |
| `blocked` | Blocked, waiting for external conditions |

## Task Attributes

Each task carries complete engineering metadata:

```typescript
interface Task {
  id: string;              // Task ID, e.g., T-1
  title: string;           // Task title
  description: string;     // Detailed description
  owner: string;           // Responsible Agent
  status: TaskStatus;      // Current status
  dependencies: string[];  // Prerequisite task IDs
  writeScope: string[];    // Allowed write files/directories
  result?: string;         // Execution result
  evidence?: string[];     // Verification evidence
  recoverable?: boolean;   // Whether recoverable
}
```

## Parallel Scheduling

The Leader's scheduler automatically analyzes DAG topology:

1. **Ready queue**: Tasks with all prerequisites completed enter the ready queue
2. **Parallel dispatch**: Ready tasks are dispatched to available Workers by owner role
3. **Dependency unlocking**: Task completion automatically unlocks downstream tasks
4. **Block propagation**: Failed or blocked tasks propagate status to the dependency chain

## State Recovery

All LingXiao runtime state is persisted to SQLite and fully recoverable after crashes:

```bash
# Resume a specific session
lingxiao --session <session_id>

# List all sessions
lingxiao list
```

On recovery:
- DAG structure and task states are rebuilt from the database
- Incomplete tasks can resume execution
- Completed results and evidence are preserved
- Agent context can be reconstructed

## Integration with Orchestration Verification

Task completion automatically triggers the verification pipeline:

- **Speculative execution**: Multiple parallel branches can run for the same task, best one wins
- **Adversarial verification**: Command-level breaker strategies verify results
- **Contract loop**: `contract → implement → evaluate → repair → reset` five-phase loop

See [Orchestration Kernel](./orchestration.md).
