---
title: Custom Commands
description: Create and manage custom Slash commands
---

# Custom Commands

LingXiao supports custom Slash commands via configuration.

## Configuration

In `~/.lingxiao/settings.json`:

```json
{
  "commands": {
    "deploy": {
      "description": "Deploy to production",
      "prompt": "Execute deployment: build, test, push image"
    }
  }
}
```
