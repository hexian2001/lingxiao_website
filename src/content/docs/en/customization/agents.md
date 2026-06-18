---
title: Agents
description: Custom Agent roles and capabilities
---

# Custom Agents

LingXiao supports custom Agent roles beyond the 13 presets.

## Role Registration

```json
{
  "roles": {
    "devops": {
      "description": "DevOps Engineer",
      "skills": ["docker", "k8s", "ci-cd"],
      "tools": ["shell", "file_read", "file_create"]
    }
  }
}
```
