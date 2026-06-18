---
title: Expert Panel
description: Leader + Worker expert panel architecture
---

# Expert Panel System

LingXiao's basic unit is not "an assistant" but a Leader + Worker expert panel.

## Leader

The commander: understands goals, decomposes tasks, builds DAGs, schedules experts, handles user confirmations, supervises completion.

## Preset Roles (13)

| Role | Responsibility |
| --- | --- |
| research | Research, comparison |
| explore | Code exploration |
| coding | General coding |
| verify | Verification, regression |
| review | Code review |
| frontend | WebUI/TUI interaction |
| backend | Backend, API, database |
| fullstack | Full-stack |
| qa | Testing, QA |
| ux_designer | Usability review |
| planner | Planning, decomposition |
| evaluator | Evaluation, acceptance |
| architect | Architecture, interfaces |

## Process Isolation

Each Worker runs in a separate process, communicating with Leader via IPC. 30-second heartbeat timeout detection.
