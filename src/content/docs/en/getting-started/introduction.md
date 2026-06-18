---
title: Introduction
description: LingXiao — a local AI command system for real engineering delivery
---

# LingXiao

> A Leader plans, a DAG orders the work, expert agents execute, and evidence closes the loop. LingXiao is not a model wrapped in a text box; it is a local engineering runtime for models, tools, permissions, tasks, state, and verification.

LingXiao is built for long-running, complex, high-stakes AI engineering work. From one goal, it can form a plan, create dependency-aware tasks, dispatch role-based worker experts, call real tools, and preserve build output, test results, browser screenshots, logs, Git changes, and session state as auditable evidence.

## What LingXiao Gives You

<div class="doc-feature-grid">
  <article>
    <strong>Expert Team Runtime</strong>
    <span>The Leader plans, dispatches, and verifies; workers operate as research, frontend, backend, QA, review, design, or operations specialists.</span>
  </article>
  <article>
    <strong>Task DAG Orchestration</strong>
    <span>Complex goals become dependency-aware task graphs, making parallel work, blockers, failures, and repairs visible.</span>
  </article>
  <article>
    <strong>Real Tool Kernel</strong>
    <span>Files, Shell, Git, browser automation, HTTP, Office, MCP, skills, and workflows are unified under one tool registry.</span>
  </article>
  <article>
    <strong>Full State Sync</strong>
    <span>WebUI / TUI / CLI share the same runtime state: task board, agents, permission requests, terminal output, and artifacts.</span>
  </article>
  <article>
    <strong>Evidence Loop</strong>
    <span>Delivery returns to builds, tests, screenshots, logs, contracts, and diffs. Failed gates become explicit repair work.</span>
  </article>
  <article>
    <strong>Recoverable Sessions</strong>
    <span>SQLite, Git, memory, work notes, and archived artifacts preserve engineering context across interruptions.</span>
  </article>
</div>

## Architecture Overview

<div class="doc-arch-map" role="img" aria-label="LingXiao runtime architecture: entry clients connect to the session kernel; the Leader coordinates the DAG, expert agents, tools, and evidence storage.">
  <section class="doc-arch-node doc-arch-entry">
    <small>Entry</small>
    <strong>WebUI · TUI · CLI</strong>
    <span>Unified goal entry with live visibility into tasks, agents, tools, permissions, and evidence.</span>
  </section>
  <section class="doc-arch-node doc-arch-session">
    <small>Session Kernel</small>
    <strong>SessionManager / SessionRuntime</strong>
    <span>Creates, restores, pauses, and synchronizes sessions while maintaining modes and event streams.</span>
  </section>
  <section class="doc-arch-node doc-arch-leader">
    <small>Command</small>
    <strong>LeaderAgent</strong>
    <span>Understands goals, creates plans, builds the DAG, selects roles, and verifies evidence.</span>
  </section>
  <section class="doc-arch-node doc-arch-dag">
    <small>Orchestration</small>
    <strong>TaskBoard DAG</strong>
    <span>Tracks dependencies, blockers, dispatch, completion, failure, repair, and evaluation state.</span>
  </section>
  <section class="doc-arch-node doc-arch-agents">
    <small>Execution</small>
    <strong>AgentPool / Worker Experts</strong>
    <span>Specialists for research, coding, testing, review, design, documentation, and operations.</span>
  </section>
  <section class="doc-arch-node doc-arch-tools">
    <small>Tools</small>
    <strong>ToolRegistry / MCP / Skills</strong>
    <span>Files, terminals, Git, browser, HTTP, Office, workflow tools, and external MCP servers.</span>
  </section>
  <section class="doc-arch-node doc-arch-proof">
    <small>Evidence</small>
    <strong>SQLite · Git · Memory · Artifacts</strong>
    <span>Stores session state, diffs, work notes, artifacts, verification evidence, and recovery trails.</span>
  </section>
</div>

## Best-Fit Work

| Scenario | How LingXiao Handles It |
| --- | --- |
| Product Delivery | Coordinates requirements, contracts, frontend/backend work, browser verification, and docs. |
| Code Governance | Tracks technical debt, migrations, test gaps, refactors, and proof-backed repair plans. |
| Internal Automation | Turns local scripts, Office/PDF tasks, MCP, Git, workflows, and models into reusable processes. |
| Long-Running Goals | Eternal Goal keeps pursuing a target until complete, blocked, or ready for a human decision. |

## System Requirements

| Dependency | Requirement |
| --- | --- |
| Node.js | `>=24.0.0` |
| npm | Bundled with Node 24 |
| Git | Recommended for diffs, commits, and recoverable trails |
| OS | Linux / macOS / Windows / WSL |

## Next Steps

- [Installation](./install) — Set up LingXiao from scratch
- [Connect Models](./connect-models) — Configure model providers and routing
- [First Run](./first-run) — Launch your first observable, verifiable expert team
