---
title: Orchestration Verification Kernel
description: Speculative execution, adversarial verification, adaptive orchestration, contract loop, bug hunting, assumption tracking
lang: en
---

# Orchestration Verification Kernel

LingXiao doesn't just dispatch tasks — it performs structured verification on every completed task. The orchestration kernel uses speculative execution, adversarial verification, adaptive routing, and contract loops to make task results verifiable, traceable, and repairable.

## Orchestration Runtime

Task lifecycle events (create/update/dispatch/complete) automatically trigger the verification pipeline, extracting PASS/FAIL/BLOCKED verdicts:

```text
Task Complete → VerificationPipeline → Adversarial Verification → Adaptive Routing → verdict
```

## Speculative Execution

The same task can run multiple parallel implementation branches, with the best one selected by strategy:

```text
Task T-3: Backend Implementation
  ├─ Branch A (architect plan) → Verification passed ✓
  ├─ Branch B (simplified plan) → Verification passed ✓
  └─ Branch C (aggressive plan) → Verification failed ✗
```

### Selection Strategies

| Strategy | Description |
| --- | --- |
| `first_green` | First branch to pass verification wins |
| `fewest_changes` | Branch with minimal diff that passes wins |
| `fastest_tests` | Branch with fastest tests that passes wins |

- Each branch has an isolated working directory and write scope
- `VerificationPipeline` verifies each branch independently
- Losing branches are cleaned up automatically
- Default timeout: 30 minutes
- Maximum 6 parallel branches

## Adversarial Verification

`AdversarialVerifier` runs command-level breaker strategies:

```typescript
interface BreakerStrategy {
  command: string;        // Verification command
  expectedExitCode: number; // Expected exit code
  failOnExitCode: number;   // Failure exit code
}
```

### Verification Flow

1. Execute breaker command
2. Collect stdout, stderr, execution duration, timeout status
3. Determine verdict:
   - **PASS**: All strategies pass
   - **FAIL**: Any strategy fails
   - **BLOCKED**: Infrastructure issues

## Adaptive Orchestration

`AdaptiveHarness` uses difficulty signals to intelligently route tasks:

| Signal | Description |
| --- | --- |
| `cross_module_deps` | Cross-module dependency count |
| `hotspot_overlap` | Overlap with known hotspot regions |
| `prior_failures` | Historical failure rate |
| `impact_ratio` | Impact surface ratio |
| `has_ambiguous_path` | Whether ambiguous paths exist |
| `dependency_count` | Dependency count |

### Execution Strategies

Based on signals, execution strategy is auto-selected:

- **fast_path**: Small scope, low-risk tasks, single Worker fast execution
- **standard**: Medium complexity, standard scheduling
- **speculative**: High-difficulty tasks, multi-branch speculative execution
- **contract_first**: Cross-stack tasks, define contract before implementation

## Contract Loop

A five-phase loop ensures cross-stack implementation consistency:

```text
contract → implement → evaluate → repair → reset
    ↑                                      |
    └──────────────────────────────────────┘
```

### Five Phases

| Phase | Description |
| --- | --- |
| `contract` | Define interface contracts (schema, error codes, state flows) |
| `implement` | Implement frontend/backend code per contract |
| `evaluate` | Verify implementation matches contract |
| `repair` | Fix parts that don't match contract |
| `reset` | Reset and enter next round (if needed) |

Contract blackboard nodes are automatically materialized to the `.lingxiao/contracts/` directory, shared by all Agents.

## Bug Hunting

The Bughunt DAG scheduler runs in isolated worktrees:

- **DAG scheduling**: Bug hunting tasks are orchestrated by dependency relationships
- **Evidence collection**: Automatically collects reproduction steps, stack traces, environment info
- **Evidence extraction**: Extracts key evidence from logs and output
- **Evidence packaging**: Packages evidence for review
- **Discovery ledger**: Records all bug findings and fix history

## Assumption Tracking

Agents can declare verifiable assumptions, auto-reverified on code changes:

```typescript
interface Assumption {
  verification_type: 'type_check' | 'file_content' | 'test_execution' | 'ast_query';
  target: string;      // Verification target (file path, test name, etc.)
  expected: string;    // Expected result (exact text match)
}
```

### Verification Types

| Type | Description |
| --- | --- |
| `type_check` | TypeScript type checking |
| `file_content` | File content matching |
| `test_execution` | Test execution results |
| `ast_query` | AST query assertions |

When an assumption is falsified, the system feeds back to the Agent, requiring it to stop the current wrong direction and correct its understanding.
