---
title: Installation
description: Install LingXiao from source
---

# Installation

## Prerequisites

| Dependency | Requirement |
| --- | --- |
| OS | Linux / macOS / Windows / WSL |
| Node.js | >= 24.0.0 |
| Git | Recommended |

## Install

```bash
git clone https://github.com/hexian2001/lingxiao-coding.git
cd lingxiao-coding
npm install
npm run build
npm link
```

After installation, run:

```bash
lingxiao
```

First launch guides you through model and API key setup. The config file is at `~/.lingxiao/settings.json`.

> `npm link` registers the `lingxiao` command globally, so you can use it from any directory.

## Verify Installation

```bash
lingxiao --version
```

## Upgrade

```bash
cd lingxiao-coding
git pull
npm install
npm run build
```

## Development from Source

```bash
git clone https://github.com/hexian2001/lingxiao-coding.git
cd lingxiao-coding
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

## License

This project uses **AGPL v3 + Commercial Dual License**. See [LICENSE](https://github.com/hexian2001/lingxiao-coding/blob/main/LICENSE).

## Next Steps

- [Connect Models](./connect-models) — Configure LLM providers
- [First Run](./first-run) — Launch your first expert panel
