---
title: Environment Variables
description: Complete LINGXIAO_ prefixed environment variable reference
---

# Environment Variables

LingXiao is configured via `LINGXIAO_` prefixed environment variables, or in `~/.lingxiao/settings.json`. Environment variables take precedence over config files.

Configuration is defined in `src/config.ts` with defaults in `src/config/defaults.ts`. The current schema version is `ConfigSchema v3`, parsed with Zod.

## Complete Environment Variable Table

### LLM & Models

| Variable | Config Path | Type | Description |
| --- | --- | --- | --- |
| `LINGXIAO_LLM_PROVIDER` | `llm.provider` | string | `auto` / `openai` / `anthropic` |
| `LINGXIAO_LEADER_MODEL` | `llm.leader_model` | string | Leader model |
| `LINGXIAO_AGENT_MODEL` | `llm.agent_model` | string | Worker model |
| `LINGXIAO_WIKI_MODEL` | `llm.wiki_model` | string | Wiki knowledge summary model |
| `LINGXIAO_ENABLE_STREAMING` | `llm.enable_streaming` | boolean | Enable streaming output |

### API Keys & Endpoints

| Variable | Description |
| --- | --- |
| `LINGXIAO_OPENAI_API_KEY` | OpenAI or compatible API key |
| `LINGXIAO_OPENAI_BASE_URL` | OpenAI compatible endpoint URL |
| `LINGXIAO_ANTHROPIC_API_KEY` | Anthropic API key |
| `LINGXIAO_ANTHROPIC_BASE_URL` | Anthropic endpoint URL |

### Agent & Orchestration

| Variable | Config Path | Type | Description |
| --- | --- | --- | --- |
| `LINGXIAO_MAX_CONCURRENT_AGENTS` | `agents.max_concurrent` | number | Max concurrent workers |
| `LINGXIAO_AGENT_MAX_ITERATIONS` | `agents.max_iterations` | number | Worker max iterations |
| `LINGXIAO_AGENT_MAX_RUNTIME_MINUTES` | `agents.max_runtime_minutes` | number | Worker max runtime (minutes) |
| `LINGXIAO_WORKER_COMPLETION_JUDGE` | `agents.worker_completion_judge_enabled` | boolean | Worker completion judge |
| `LINGXIAO_EXTERNAL_AGENTS_ENABLED` | `agents.external_agents_enabled` | boolean | External agent support |
| `LINGXIAO_REMOTE_WORKERS_ENABLED` | `scaling.remoteWorkers.enabled` | boolean | Remote worker support |

### Verification & Quality Gates

| Variable | Config Path | Type | Description |
| --- | --- | --- | --- |
| `LINGXIAO_VERIFICATION_COMPLETION_GATE` | `verification.completion_gate_enabled` | boolean | Completion gate |
| `LINGXIAO_VERIFICATION_TYPECHECK` | `verification.typecheck` | boolean | Type checking |
| `LINGXIAO_VERIFICATION_BUILD` | `verification.build` | boolean | Build check |
| `LINGXIAO_VERIFICATION_AFFECTED_TESTS` | `verification.affected_tests` | boolean | Affected tests |
| `LINGXIAO_VERIFICATION_FULL_TESTS` | `verification.full_tests` | boolean | Full test suite |

### Leader Runtime

| Variable | Config Path | Type | Description |
| --- | --- | --- | --- |
| `LINGXIAO_LEADER_MAX_TOOL_ROUNDS` | `leader.max_tool_rounds` | number | Leader max tool rounds |
| `LINGXIAO_LEADER_MAX_RUNTIME_MINUTES` | `leader.max_runtime_minutes` | number | Leader max runtime |
| `LINGXIAO_LEADER_PROBE_SILENCE_SECONDS` | `leader.probe_silence_seconds` | number | Probe silence interval |
| `LINGXIAO_LEADER_PROBE_MAX_INTERVAL_SECONDS` | `leader.probe_max_interval_seconds` | number | Probe max interval |
| `LINGXIAO_LEADER_PROBE_BACKOFF_MULTIPLIER` | `leader.probe_backoff_multiplier` | number | Probe backoff multiplier |
| `LINGXIAO_LEADER_IDLE_WARNING_SECONDS` | `leader.idle_warning_seconds` | number | Idle warning threshold |

### Web Service & Network

| Variable | Config Path | Type | Description |
| --- | --- | --- | --- |
| `LINGXIAO_WEB_HOST` | `server.host` | string | Web service host, default `127.0.0.1` |
| `LINGXIAO_WEB_PORT` | `server.port` | number | Web service port, auto-assigned |
| `LINGXIAO_WEB_PROXY_TARGET` | - | string | Vite dev proxy target |
| `LINGXIAO_PROXY_URL` | `network.proxy.url` | string | Proxy URL |
| `LINGXIAO_PROXY_LLM` | `network.proxy.llm_enabled` | boolean | Route LLM requests through proxy |
| `LINGXIAO_PROXY_TOOLS` | `network.proxy.tools_enabled` | boolean | Route tool requests through proxy |
| `LINGXIAO_USER_AGENT` | `network.user_agent` | string | Custom User-Agent |

### Paths & Directories

| Variable | Config Path | Type | Description |
| --- | --- | --- | --- |
| `LINGXIAO_DB_PATH` | `paths.db_path` | string | Database path |
| `LINGXIAO_CHROME_PATH` | `paths.chrome_path` | string | Chrome executable path |
| `CHROME_PATH` | `paths.chrome_path` | string | Same as above (alias) |
| `CHROME_BIN` | `paths.chrome_path` | string | Same as above (alias) |
| `LINGXIAO_BUNDLED_SKILLS_DIR` | `paths.bundled_skills_dir` | string | Bundled skills directory |
| `LINGXIAO_GLOBAL_SKILLS_DIR` | `paths.global_skills_dir` | string | Global skills directory |

### Security & Permissions

| Variable | Config Path | Type | Description |
| --- | --- | --- | --- |
| `LINGXIAO_IDENTITY_JUDGE_LLM` | `security.identity_judge_llm_enabled` | boolean | LLM identity judge |
| `LINGXIAO_HARDENED_MODE` | `security.hardened_mode` | boolean | Hardened mode (one-way lock) |

:::caution[Hardened Mode One-Way Lock]
`LINGXIAO_HARDENED_MODE` is a one-way lock: setting it to a truthy value forces hardened mode on, and the Settings route rejects attempts to turn it off.
:::

### Other

| Variable | Config Path | Type | Description |
| --- | --- | --- | --- |
| `LINGXIAO_WORKER_SPAWN_TIMEOUT_MS` | `timeouts.worker_spawn_ms` | number | Worker spawn timeout |
| `LINGXIAO_LANGUAGE` | `ui.language` | string | UI language `zh` / `en` |
| `LINGXIAO_BLACKBOARD` | `blackboard.enabled` | boolean | Blackboard system toggle |

## Config File

In addition to environment variables, config can be written to `~/.lingxiao/settings.json`:

```json
{
  "llm": {
    "provider": "openai",
    "leader_model": "gpt-4o",
    "agent_model": "gpt-4o-mini"
  },
  "agents": {
    "max_concurrent": 5,
    "max_iterations": 50
  },
  "security": {
    "permission_mode": "dev"
  }
}
```

## Config Groups

LingXiao has 31 major config groups:

| Group | Description |
| --- | --- |
| `llm` | LLM provider, models, timeouts, retries |
| `llm_gateway` | Local LLM gateway config |
| `agents` | Worker capacity & runtime |
| `verification` | Completion gate & verification |
| `leader` | Leader runtime control |
| `health` | Health checks |
| `context` | Context management |
| `truncation` | Context truncation policy |
| `timeouts` | Timeout settings |
| `web_api` | Web API config |
| `paths` | File paths |
| `skills` | Skills system |
| `plugins` | Plugin management |
| `marketplaces` | Marketplace config |
| `mcp` | MCP servers |
| `tools` | Tool registration |
| `roles` | Role definitions |
| `server` | Web service |
| `network` | Network & proxy |
| `browser` | Browser automation |
| `security` | Security & permissions |
| `memory` | Memory system |
| `checkpoint` | File checkpoints |
| `ui` | UI config |
| `message_bus` | Message bus |
| `observability` | Observability |
| `taskPriority` | Task priority |
| `scaling` | Scaling |
| `git` | Git integration |
| `blackboard` | Blackboard system |
| `advanced` | Advanced options |
| `credentials` | Credentials management |

## Config Rules

1. New config values must be added to both Zod schema and defaults
2. User-adjustable values exposed through settings routes only if safe
3. Environment variable overrides must be listed in this document
4. Sensitive information (e.g., Git tokens) must not be returned raw by `/api/v1/settings`
5. Values affecting server bootstrap may require process restart
