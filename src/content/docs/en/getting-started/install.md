---
title: Installation
description: One-line install for LingXiao
---

# Installation

## One-Line Install

### macOS / Linux / WSL

```bash
curl -fsSL https://raw.githubusercontent.com/hexian2001/lingxiao-coding/main/scripts/install.sh | sh
```

### Windows (CMD / PowerShell)

```powershell
powershell -c "irm https://raw.githubusercontent.com/hexian2001/lingxiao-coding/main/scripts/install.ps1 | iex"
```

After installation, run:

```bash
lingxiao
```

First launch guides you through model and API key setup. The script auto-detects your platform and architecture, downloads the matching portable binary, extracts it, and sets up the command link. No Node.js required.

> **Specific version**: append `-- --version v1.0.0` on macOS/Linux, or use `-Version "v1.0.0"` parameter on Windows.

## Prerequisites

| Dependency | Requirement |
| --- | --- |
| OS | Linux / macOS / Windows / WSL |
| Node.js | Not required for portable; `>=24.0.0` for source development |
| Git | Recommended |

## Verify Installation

```bash
lingxiao
```

First launch auto-guides you through configuration. The config file is at `~/.lingxiao/settings.json`.

## Upgrade

```bash
lingxiao upgrade
```

Automatically checks for the latest GitHub release, downloads the matching platform package, and replaces the installation. You can also check for updates without upgrading:

```bash
lingxiao upgrade --check
```

> For npm global installs, use `npm update -g lingxiao_cli` to upgrade.

## Development from Source

```bash
git clone https://github.com/hexian2001/lingxiao-coding.git
cd lingxiao
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
