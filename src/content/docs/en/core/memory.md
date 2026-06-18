---
title: Persistent Memory
description: FTS5+BM25 full-text search, 4 memory types, Distill/Dream, project/user scope
lang: en
---

# Persistent Memory

LingXiao has a two-layer memory architecture: long-term memory (FTS5 + BM25 full-text search engine) and short-term skill injection (execution knowledge injected at Worker dispatch time). Together they form a complete memory system.

## Long-Term Memory

### Full-Text Search Engine

Based on SQLite FTS5 + BM25 ranking:

- **FTS5**: SQLite full-text search extension with Chinese tokenization support
- **BM25**: Probabilistic relevance ranking algorithm, sorts by keyword match score
- **Search interface**: `memory(action="search", query="keywords")`

### 4 Memory Types

| Type | Identifier | Description |
| --- | --- | --- |
| User preferences | `user` | User's coding style, tech preferences, work habits |
| Feedback guidelines | `feedback` | Agent working principles, best practices, lessons learned |
| Project knowledge | `project` | Project architecture, tech stack, key decisions, module relationships |
| External references | `reference` | Documentation links, API references, tool usage |

### Storage Locations

| Scope | Path | Description |
| --- | --- | --- |
| Project-level | `.lingxiao/memory/` | Project-specific memory, travels with the project |
| User-level | `~/.lingxiao/memory/` | Global user memory, shared across projects |

### Memory Operations

```typescript
// Save memory
memory(action="save", name="user-preferences", type="user",
  description="User preferences", content="Prefers React + TypeScript...")

// Search memory
memory(action="search", query="frontend framework preferences")

// Load specific memory
memory(action="load", name="user-preferences")

// List all memories
memory(action="list", scope="project")

// Delete memory
memory(action="delete", name="outdated-memory")
```

## Auto Distillation (Distill)

`DistillCommand` automatically distills valuable memories from session history:

- Scans completed sessions
- Identifies reusable knowledge, patterns, and lessons
- Auto-categorizes into 4 memory types
- Deduplicates before saving to the long-term memory store

## Associative Memory (Dream)

`DreamCommand` performs associative memory maintenance during idle time:

- Discovers implicit associations between memories
- Merges duplicate or similar memory entries
- Updates status markers for outdated memories
- Optimizes search index performance

## Maintenance Pipeline

The memory system has an automatic maintenance pipeline:

1. **Index rebuild**: `memory(action="rebuild")` rebuilds FTS5 index
2. **Expiry cleanup**: Automatically marks and cleans expired memories
3. **Relationship updates**: Cross-references between memories are auto-maintained
4. **Capacity control**: Project-level and user-level memory capacity monitoring

## Short-Term Skill Injection

At Worker dispatch time, the Leader injects relevant Skill content into the Worker's prompt based on task type and role bindings:

- Skill source priority: Project-level > Plugin-contributed > User-level > Built-in
- Only Skill phases relevant to the current task are injected
- Skill content serves as execution knowledge guiding the Worker's workflow

This complements long-term memory: long-term memory provides cross-session knowledge accumulation, while short-term skill injection provides execution guidance for the current task.
