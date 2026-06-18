---
title: Memory
description: FTS5 + BM25 long-term memory
---

# Persistent Memory

LingXiao has a two-layer memory architecture.

## Long-Term Memory

FTS5 + BM25 full-text search engine with 4 memory types: user, feedback, project, reference.

## Storage

- Project-level: `.lingxiao/memory/`
- User-level: `~/.lingxiao/memory/`

## Short-Term Skill Injection

Execution knowledge injected at worker dispatch time.
