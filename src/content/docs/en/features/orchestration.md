---
title: Orchestration
description: Speculative execution, adversarial verification, adaptive orchestration
---

# Orchestration & Verification Kernel

LingXiao performs structured verification on every completed task.

## Orchestration Runtime

Task lifecycle events auto-trigger verification, extracting PASS/FAIL/BLOCKED verdicts.

## Speculative Execution

Multiple parallel implementation branches with strategies: `first_green`, `fewest_changes`, `fastest_tests`

## Adversarial Verification

Command-level breaker strategy: exit code assertions, stdout/stderr evidence collection.

## Adaptive Orchestration

Intelligent task routing based on: cross-module dependencies, hotspot overlap, historical failure rate, impact ratio.

## Contract Loop

```text
contract → implement → evaluate → repair → reset
```
