---
title: Skills System
description: 4-tier priority, YAML frontmatter, phase loading, and auto-injection
---

# Skills System

LingXiao's Skill system is the **execution-knowledge surface** for Agents. A skill is a structured Markdown document (YAML frontmatter + body) that the runtime injects into a worker's task prompt as a `<skill>` block, giving the LLM in-context procedures, domain constraints, and quality gates.

Skills are *not* runtime tools and *not* plugin manifests. They are declarative knowledge packs, scoped and versioned by source.

## 4-Tier Priority

Skills are loaded by source priority (higher overrides lower):

| Priority | Source | Directory |
| --- | --- | --- |
| 1 (highest) | Project | `.lingxiao/skills/` |
| 2 | Plugin contributed | Plugin directory |
| 3 | User | `~/.lingxiao/skills/` |
| 4 (lowest) | Bundled | Package bundled |

## Skill Definition Format

The on-disk format is **YAML frontmatter + Markdown body**:

```markdown
---
name: my-skill
description: A one-line summary
---
<markdown body — procedures, gates, references>
```

### Required Fields

| Field | Rule | Description |
| --- | --- | --- |
| `name` | kebab-case, validated by `validateSkillName` | Skill name |
| `description` | Non-empty, single line | Skill description |

### Optional Fields

| Field | Description |
| --- | --- |
| `triggers` | Trigger conditions (reserved extension point) |
| `content` | Content reference (reserved extension point) |

### Validation Rules

- `description` and `body` are both **required** at write time
- `validateSkillName` enforces kebab-case; invalid names throw on save and are skipped on read
- Files missing both `description` and a non-empty body are silently dropped on read

## Phase Loading & Quality Gates

A skill directory may contain a `phases/` subdirectory. Each `*.md` file becomes a `SkillPhase`:

```ts
interface SkillPhase { name: string; path: string; content: string; }
interface QualityGate { checks: string[]; skipConditions: string[]; }
```

`loadSkillPhases(skillDir)` returns an ordered list of phases, each potentially containing quality gate checks and skip conditions.

## Auto-Injection Mechanism

### Injection Points

| Injection Point | Scenario | Budget |
| --- | --- | --- |
| Worker task prompt | `BaseAgentRuntime.buildTaskPrompt` | Total 18,000 chars, per-skill 7,500 chars |
| TUI messages | `SessionManagerRuntime` | On-demand injection |

### Skill Name Sources

Three sources are merged and de-duplicated for injection:

| Source | Origin | When It Applies |
| --- | --- | --- |
| `skillNames` | Role capability (`RoleCapabilityModel`) | Role-based, always when this agent runs |
| `explicitSkills` | `$skill` mentions in task description and system prompt | User/role opted in via syntax |
| `officeSkill` | `OFFICE_MODE_ACTIVE` session state + `OFFICE_SUITE_SKILL_NAME` availability | Session-level office mode |

### `$skill` Mention Syntax

Reference skills in task descriptions or system prompts using `$skill-name`:

```
$debug-frontend-backend-contract
$office_suite
$explore_implement_verify
```

Regex match: `/ \$([a-zA-Z0-9_][a-zA-Z0-9_-]*) /g`, deduplicated after matching.

### Injection Budget

| Limit | Value | Effect When Exceeded |
| --- | --- | --- |
| `maxTotalChars` | 18,000 | Subsequent skills dropped in arrival order |
| `maxPerSkillChars` | 7,500 | Each skill body clipped to this length |
| Visibility | `truncated: true` | Caller reads `descriptor.path` for full content |

## Built-in Skill Packs

LingXiao includes 14 built-in skill packs:

| Skill | Description |
| --- | --- |
| `code-quality` | Code quality checks |
| `commit-message` | Git commit message conventions |
| `doc-coauthoring` | Document collaboration |
| `docx` | Word document generation |
| `frontend-design` | Frontend design |
| `office-suite` | Office suite |
| `pdf` | PDF generation |
| `pptx` | PPT generation |
| `skill-creator` | Skill creator |
| `slidev` | Slidev presentations |
| `theme-factory` | Theme factory |
| `web-artifacts-builder` | Web artifacts builder |
| `xlsx` | Excel generation |
| `design-market` | Design asset marketplace |

## Custom Skills

### Via skill-creator

Use the `skill-creator` skill pack to auto-create custom skills.

### Manual Creation

Write in project or user-level directories:

```bash
# Project level
mkdir -p .lingxiao/skills/my-skill
cat > .lingxiao/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: My custom skill
---

# My Skill

## Procedure
1. Step one
2. Step two

## Quality Gates
- Check one
- Check two
EOF
```

### HTTP API

Manage skills via `/api/v1/skills` routes:

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v1/skills` | GET | List skills |
| `/api/v1/skills` | POST | Create skill |
| `/api/v1/skills/:name` | PUT | Update skill |
| `/api/v1/skills/:name` | DELETE | Delete skill |

## Selection Policy

`SkillSelectionPolicy.digestGuidance` defines 5 selection rules that appear in the Leader's digest prompt, guiding automatic skill selection and disabling.
