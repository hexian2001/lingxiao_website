---
title: Rules
description: Project rules and custom rules
---

# Rules

LingXiao supports project-level rule files that inject engineering constraints into Agent context. Rules are Markdown files automatically injected into the Agent context without manual referencing.

## Rule File Locations

| Level | Directory | Description |
| --- | --- | --- |
| Project | `.lingxiao/rules/` | Project-specific rules |
| User | `~/.lingxiao/rules/` | Global user rules |

## Rule Format

Rule files are Markdown format, auto-injected into the Agent context:

```markdown
# Code Standards

- Use TypeScript strict mode
- Functions must have explicit return type annotations
- No use of any type
- All public APIs must have JSDoc comments
```

## Rule Priority

project > global. Project-level rules override user-level rules.

## Rule Injection

Rule files are automatically read and injected into the system prompt at Agent startup. Unlike Skills, rules do not require explicit references (no `$skill` syntax); all rule file contents are injected.

### Injection Scope

| Scope | Behavior |
| --- | --- |
| Project rules | Visible only to Agents in the current workspace |
| User rules | Visible to all Agents |

## Common Rule Examples

### Code Standards Rules

```markdown
# Code Standards

- TypeScript strict mode
- Use ESM imports (no require)
- Functions must have explicit return type annotations
- No @ts-ignore
- Public functions require JSDoc comments
```

### Git Rules

```markdown
# Git Standards

- Commit messages use conventional commits format
- feat: new feature / fix: bugfix / docs: docs / refactor: refactor
- Each commit contains only one logical change
- PR title matches commit title
```

### Testing Rules

```markdown
# Testing Standards

- New features must include unit tests
- Test coverage must be at least 80%
- Use describe/it to organize test structure
- Mock external dependencies, not the module under test
```

### Security Rules

```markdown
# Security Standards

- No hardcoded API keys or passwords
- Environment variables must be read through config.ts
- SQL queries must use parameterized statements
- User input must be validated and escaped
```

## Differences from Skills

| Feature | Rules | Skills |
| --- | --- | --- |
| Injection | Automatic | On-demand (`$skill` or role binding) |
| Content | Constraints and standards | Procedures and domain knowledge |
| Format | Plain Markdown | YAML frontmatter + Markdown |
| Location | `.lingxiao/rules/` | `.lingxiao/skills/` |
| Priority | project > global | 4-tier (project > plugin > user > bundled) |
