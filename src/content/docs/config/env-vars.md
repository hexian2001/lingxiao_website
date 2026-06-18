---
title: 环境变量
description: LINGXIAO_ 前缀环境变量完整速查表
---

# 环境变量

凌霄通过 `LINGXIAO_` 前缀环境变量进行配置，也可在 `~/.lingxiao/settings.json` 中设置。环境变量优先级高于配置文件。

配置由 `src/config.ts` 定义，默认值在 `src/config/defaults.ts` 中。当前 schema 版本为 `ConfigSchema v3`，使用 Zod 解析校验。

## 完整环境变量表

### LLM 与模型

| 变量 | 配置路径 | 类型 | 说明 |
| --- | --- | --- | --- |
| `LINGXIAO_LLM_PROVIDER` | `llm.provider` | string | `auto` / `openai` / `anthropic` |
| `LINGXIAO_LEADER_MODEL` | `llm.leader_model` | string | Leader 使用的模型 |
| `LINGXIAO_AGENT_MODEL` | `llm.agent_model` | string | Worker 使用的模型 |
| `LINGXIAO_WIKI_MODEL` | `llm.wiki_model` | string | Wiki 知识摘要模型 |
| `LINGXIAO_ENABLE_STREAMING` | `llm.enable_streaming` | boolean | 启用流式输出 |

### API Key 与接口地址

| 变量 | 说明 |
| --- | --- |
| `LINGXIAO_OPENAI_API_KEY` | OpenAI 或兼容接口 API Key |
| `LINGXIAO_OPENAI_BASE_URL` | OpenAI 兼容接口地址 |
| `LINGXIAO_ANTHROPIC_API_KEY` | Anthropic API Key |
| `LINGXIAO_ANTHROPIC_BASE_URL` | Anthropic 接口地址 |

### Agent 与编排

| 变量 | 配置路径 | 类型 | 说明 |
| --- | --- | --- | --- |
| `LINGXIAO_MAX_CONCURRENT_AGENTS` | `agents.max_concurrent` | number | 最大并发 Worker 数 |
| `LINGXIAO_AGENT_MAX_ITERATIONS` | `agents.max_iterations` | number | Worker 最大迭代轮次 |
| `LINGXIAO_AGENT_MAX_RUNTIME_MINUTES` | `agents.max_runtime_minutes` | number | Worker 最大运行时间（分钟） |
| `LINGXIAO_WORKER_COMPLETION_JUDGE` | `agents.worker_completion_judge_enabled` | boolean | Worker 完成判定 |
| `LINGXIAO_EXTERNAL_AGENTS_ENABLED` | `agents.external_agents_enabled` | boolean | 外部 Agent 支持 |
| `LINGXIAO_REMOTE_WORKERS_ENABLED` | `scaling.remoteWorkers.enabled` | boolean | 远程 Worker 支持 |

### 验证与质量门

| 变量 | 配置路径 | 类型 | 说明 |
| --- | --- | --- | --- |
| `LINGXIAO_VERIFICATION_COMPLETION_GATE` | `verification.completion_gate_enabled` | boolean | 完成门控 |
| `LINGXIAO_VERIFICATION_TYPECHECK` | `verification.typecheck` | boolean | 类型检查 |
| `LINGXIAO_VERIFICATION_BUILD` | `verification.build` | boolean | 构建检查 |
| `LINGXIAO_VERIFICATION_AFFECTED_TESTS` | `verification.affected_tests` | boolean | 受影响测试 |
| `LINGXIAO_VERIFICATION_FULL_TESTS` | `verification.full_tests` | boolean | 全量测试 |

### Leader 运行时

| 变量 | 配置路径 | 类型 | 说明 |
| --- | --- | --- | --- |
| `LINGXIAO_LEADER_MAX_TOOL_ROUNDS` | `leader.max_tool_rounds` | number | Leader 最大工具轮次 |
| `LINGXIAO_LEADER_MAX_RUNTIME_MINUTES` | `leader.max_runtime_minutes` | number | Leader 最大运行时间 |
| `LINGXIAO_LEADER_PROBE_SILENCE_SECONDS` | `leader.probe_silence_seconds` | number | 探测静默间隔 |
| `LINGXIAO_LEADER_PROBE_MAX_INTERVAL_SECONDS` | `leader.probe_max_interval_seconds` | number | 探测最大间隔 |
| `LINGXIAO_LEADER_PROBE_BACKOFF_MULTIPLIER` | `leader.probe_backoff_multiplier` | number | 探测退避倍数 |
| `LINGXIAO_LEADER_IDLE_WARNING_SECONDS` | `leader.idle_warning_seconds` | number | 空闲告警阈值 |

### Web 服务与网络

| 变量 | 配置路径 | 类型 | 说明 |
| --- | --- | --- | --- |
| `LINGXIAO_WEB_HOST` | `server.host` | string | Web 服务监听地址，默认 `127.0.0.1` |
| `LINGXIAO_WEB_PORT` | `server.port` | number | Web 服务端口，默认自动分配 |
| `LINGXIAO_WEB_PROXY_TARGET` | - | string | Vite 开发代理目标 |
| `LINGXIAO_PROXY_URL` | `network.proxy.url` | string | 代理 URL |
| `LINGXIAO_PROXY_LLM` | `network.proxy.llm_enabled` | boolean | LLM 请求走代理 |
| `LINGXIAO_PROXY_TOOLS` | `network.proxy.tools_enabled` | boolean | 工具请求走代理 |
| `LINGXIAO_USER_AGENT` | `network.user_agent` | string | 自定义 User-Agent |

### 路径与目录

| 变量 | 配置路径 | 类型 | 说明 |
| --- | --- | --- | --- |
| `LINGXIAO_DB_PATH` | `paths.db_path` | string | 数据库路径 |
| `LINGXIAO_CHROME_PATH` | `paths.chrome_path` | string | Chrome 可执行路径 |
| `CHROME_PATH` | `paths.chrome_path` | string | 同上（别名） |
| `CHROME_BIN` | `paths.chrome_path` | string | 同上（别名） |
| `LINGXIAO_BUNDLED_SKILLS_DIR` | `paths.bundled_skills_dir` | string | 内置技能目录 |
| `LINGXIAO_GLOBAL_SKILLS_DIR` | `paths.global_skills_dir` | string | 全局技能目录 |

### 安全与权限

| 变量 | 配置路径 | 类型 | 说明 |
| --- | --- | --- | --- |
| `LINGXIAO_IDENTITY_JUDGE_LLM` | `security.identity_judge_llm_enabled` | boolean | LLM 身份判定 |
| `LINGXIAO_HARDENED_MODE` | `security.hardened_mode` | boolean | 加固模式（单向锁） |

:::caution[加固模式单向锁]
`LINGXIAO_HARDENED_MODE` 是单向锁：设置为 truthy 值后强制开启加固模式，Settings 路由会拒绝关闭请求。
:::

### 其他

| 变量 | 配置路径 | 类型 | 说明 |
| --- | --- | --- | --- |
| `LINGXIAO_WORKER_SPAWN_TIMEOUT_MS` | `timeouts.worker_spawn_ms` | number | Worker 启动超时 |
| `LINGXIAO_LANGUAGE` | `ui.language` | string | 界面语言 `zh` / `en` |
| `LINGXIAO_BLACKBOARD` | `blackboard.enabled` | boolean | 黑板系统开关 |

## 配置文件

除环境变量外，配置也可写入 `~/.lingxiao/settings.json`：

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

## 配置组

凌霄的配置分为 31 个主要组：

| 组 | 说明 |
| --- | --- |
| `llm` | LLM 提供商、模型、超时、重试 |
| `llm_gateway` | 本地 LLM 网关配置 |
| `agents` | Worker 容量与运行时 |
| `verification` | 完成门控与验证 |
| `leader` | Leader 运行时控制 |
| `health` | 健康检查 |
| `context` | 上下文管理 |
| `truncation` | 上下文截断策略 |
| `timeouts` | 超时设置 |
| `web_api` | Web API 配置 |
| `paths` | 文件路径 |
| `skills` | 技能系统 |
| `plugins` | 插件管理 |
| `marketplaces` | 市场配置 |
| `mcp` | MCP 服务器 |
| `tools` | 工具注册 |
| `roles` | 角色定义 |
| `server` | Web 服务 |
| `network` | 网络与代理 |
| `browser` | 浏览器自动化 |
| `security` | 安全与权限 |
| `memory` | 记忆系统 |
| `checkpoint` | 文件检查点 |
| `ui` | 界面配置 |
| `message_bus` | 消息总线 |
| `observability` | 可观测性 |
| `taskPriority` | 任务优先级 |
| `scaling` | 扩缩容 |
| `git` | Git 集成 |
| `blackboard` | 黑板系统 |
| `advanced` | 高级选项 |
| `credentials` | 凭据管理 |

## 配置规则

1. 新配置值必须同时添加到 Zod schema 和 defaults
2. 用户可调值仅在安全时通过 settings 路由暴露
3. 环境变量覆盖必须在此文档中列出
4. 敏感信息（如 Git token）不得由 `/api/v1/settings` 原样返回
5. 影响服务器启动的值可能需要重启进程
