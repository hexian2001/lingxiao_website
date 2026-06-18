---
title: Agents
description: Role definitions, role registration, tool permissions, and custom agents
---

# Agents

LingXiao's Agent system is based on the Leader-Worker architecture, where roles (Role) define Agent capabilities, tools, and knowledge.

## Role System

### Leader

The Leader is responsible for:

- Interpreting user goals
- Maintaining the plan/task DAG
- Creating and dispatching tasks
- Supervising worker execution
- Resolving plan review and user questions
- Coordinating tool usage and permissions
- Reacting to health/idle/stall signals

### Worker

Workers execute assigned tasks. Each worker has:

- `agent_id`: unique identifier
- `agent_name`: name
- Role/system prompt
- Task ID
- Status
- Iteration count
- Conversation history

Workers run through the AgentPool/runtime path. Task execution is worker-owned.

## Preset Roles

LingXiao includes 13 preset roles:

| Role | Description |
| --- | --- |
| architect | Architect, responsible for task decomposition and design |
| backend | Backend developer |
| frontend | Frontend developer |
| fullstack | Full-stack developer |
| explore | Exploration researcher |
| verify | Verification engineer |
| doc | Documentation engineer |
| test | Test engineer |
| devops | DevOps engineer |
| data | Data engineer |
| security | Security engineer |
| ui-design | UI designer |
| refactor | Refactoring engineer |

## Role Definition

Roles are defined via `RoleCapabilityModel`, containing key fields:

| Field | Description |
| --- | --- |
| `name` | Role name |
| `description` | Role description |
| `systemPrompt` | System prompt |
| `allowedTools` | List of allowed tools |
| `requestedTools` | List of requested tools |
| `skillNames` | Bound skill names |
| `suggestedModel` | Suggested model |

### Adding Roles

Roles come from three sources:

1. **Built-in roles**: defined in `src/agents/leader/builtinRoles.ts`
2. **Dynamic roles**: created via `define_agent_role` at runtime
3. **Web config**: overridden via Web roles routes

Steps to add a role:

1. Define responsibilities
2. Define system prompt
3. Define allowed/requested tools
4. Optionally define skills
5. Optionally define suggested model

## Custom Agents

### Via Config File

Define custom roles in `~/.lingxiao/settings.json` or project-level config:

```json
{
  "roles": {
    "custom-role": {
      "description": "Custom role",
      "systemPrompt": "You are an engineer focused on performance optimization",
      "allowedTools": ["file_read", "code_search", "shell"],
      "skillNames": ["performance-optimization"]
    }
  }
}
```

### Via Leader Tool

The Leader can dynamically create roles at runtime via `define_agent_role`:

```json
{
  "name": "performance-engineer",
  "description": "Performance Engineer",
  "systemPrompt": "Focused on code performance analysis and optimization",
  "allowedTools": ["file_read", "code_search", "shell", "python_exec"]
}
```

## Tool Permissions

The role's `allowedTools` and `requestedTools` control tool access:

- `allowedTools`: tools the role is explicitly permitted to use
- `requestedTools`: tools the role requests but requires Leader approval

Tool permissions are also governed by the permission system (`security.permission_mode`).

## Task DAG

Tasks are stored in the `tasks` table and managed through `TaskBoard`:

| Field | Description |
| --- | --- |
| `id` | Task ID (e.g., `T-1`) |
| `session_id` | Session ID |
| `subject` | Task subject |
| `description` | Task description |
| `status` | Task status |
| `blocked_by` | Dependencies |
| `assigned_agent` | Assigned agent |

### Task State Transitions

```
pending → ready → dispatched → in_progress → completed
                                    ↓
                               failed / cancelled
```

## Worker Runtime

Worker execution is surfaced through the team runtime:

- Workers are registered through roles and task bindings
- Each task is dispatched to one worker owner at a time
- Worker state, logs, conversations, and completion reports flow through normal agent channels
- Supervision and intervention use Leader orchestration tools
