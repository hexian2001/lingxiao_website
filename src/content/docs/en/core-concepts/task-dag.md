---
title: Task DAG
description: Dependency-aware task graph scheduling
---

# Task DAG Orchestration

Complex goals are decomposed into dependency-aware task graphs (DAGs).

## Task Graph Structure

```text
T-1 Requirements
  ├─ T-2 Architecture
  │    ├─ T-3 Backend
  │    └─ T-4 Frontend
  ├─ T-5 Testing
  └─ T-6 Docs & Release
```

## Task States

```text
pending → dispatched → in_progress → completed
                                   → failed
                                   → blocked
```

## Speculative Execution

Multiple parallel branches with strategies: `first_green`, `fewest_changes`, `fastest_tests`.
