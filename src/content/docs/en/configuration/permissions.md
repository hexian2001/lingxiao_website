---
title: Permissions
description: 9-layer tool permission evaluation chain
---

# Permission System

## 9-Layer Evaluation Chain

```text
deny → allow → ask → yolo → always-allowed → network → hardened → strict → default allow
```

## Permission Modes

| Mode | Description |
| --- | --- |
| `strict` | All write operations require confirmation |
| `dev` | Relaxed restrictions |
| `networked` | Network tools allowed |
| `yolo` | Fully automatic, no confirmation |
