---
title: Installation
description: Set up LingXiao from scratch
---

# Installation

## Prerequisites

| Dependency | Requirement |
| --- | --- |
| Node.js | `>=24.0.0` |
| npm | Bundled with Node 24 |
| Git | Recommended |
| OS | Linux / macOS / Windows / WSL |

## Install Steps

```bash
git clone https://github.com/hexian2001/lingxiao.git
cd lingxiao
npm install
npm run build
npm link
```

After installation, the `lingxiao` command is globally available.

## First Configuration

```bash
lingxiao init
```

This command guides you through initial configuration. The config file is located at:

```text
~/.lingxiao/settings.json
```

## Verify Installation

```bash
lingxiao doctor
```

The diagnostics command checks Node.js version, Git, config files, LLM keys, and more.

## Development from Source

```bash
npm install
npm run build
npm run cli
```

Web frontend development:

```bash
cd web
npm install
npm run dev
npm run build
```

Vite dev proxy example:

```bash
LINGXIAO_WEB_PORT=8787 npm run cli
cd web
LINGXIAO_WEB_PROXY_TARGET=http://127.0.0.1:8787 npm run dev
```

## Testing

```bash
npx tsc -p tsconfig.cli.json --noEmit
npx tsc -p web/tsconfig.json --noEmit
npm run test:architecture
npm run build
npm test
```

## Next Steps

- [Connect Models](./connect-models) — Configure LLM providers
- [First Run](./first-run) — Launch your first expert panel
