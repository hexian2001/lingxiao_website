---
title: Installation
description: Multiple ways to install LingXiao
---

# Installation

## Prerequisites

| Dependency | Requirement |
| --- | --- |
| OS | Linux / macOS / Windows / WSL |
| Node.js | >= 24.0.0 (for source install) |
| Git | Recommended |

## Option 1: Portable Package (Recommended)

Download the portable package for your platform from [GitHub Releases](https://github.com/hexian2001/lingxiao-coding/releases) and extract.

| Platform | File |
| --- | --- |
| Linux x64 | `lingxiao-v1.0.2-linux-x64.tar.gz` |
| Linux arm64 | `lingxiao-v1.0.2-linux-arm64.tar.gz` |
| macOS arm64 | `lingxiao-v1.0.2-darwin-arm64.tar.gz` |
| Windows x64 | `lingxiao-v1.0.2-win-x64.zip` |

**Linux / macOS:**

```bash
tar xzf lingxiao-v1.0.2-linux-x64.tar.gz
cd lingxiao
./lingxiao
```

**Windows:**

Extract the zip, then double-click `lingxiao.exe` or run in PowerShell:

```powershell
.\lingxiao.exe
```

## Option 2: Windows Desktop

Download the Windows installer from [Releases](https://github.com/hexian2001/lingxiao-coding/releases):

- **NSIS installer** (`LingXiao-Setup-1.0.2.exe`): Recommended, supports auto-update
- **MSI installer** (`LingXiao.1.0.2.msi`): Suitable for enterprise deployment

Launch "LingXiao" from the Start Menu after installation. Future updates are detected and downloaded automatically.

## Option 3: From Source

### Linux / macOS

```bash
git clone https://github.com/hexian2001/lingxiao-coding.git
cd lingxiao-coding
npm install
npm run build
npm link
```

### Windows (PowerShell)

```powershell
git clone https://github.com/hexian2001/lingxiao-coding.git
cd lingxiao-coding
npm install
npm run build
npm link
```

### Windows (WSL)

```bash
git clone https://github.com/hexian2001/lingxiao-coding.git
cd lingxiao-coding
npm install
npm run build
npm link
```

Then run:

```bash
lingxiao
```

The first run guides you through model and API key configuration. Config is stored at `~/.lingxiao/settings.json`.

> `npm link` registers the `lingxiao` command globally, available from any directory.

## Verify Installation

```bash
lingxiao --version
```

## Upgrade

### Portable / Source Install

```bash
lingxiao upgrade
```

`lingxiao upgrade` auto-detects the install type (source or portable), locates the install path, downloads the latest version, and completes the update.

### Windows Desktop

The desktop app checks for updates automatically on launch and downloads incrementally. You can also check manually.

### Manual Upgrade (Source — All Platforms)

#### Linux / macOS

```bash
cd lingxiao-coding
git pull
npm install
npm run build
```

#### Windows (PowerShell)

```powershell
cd lingxiao-coding
git pull
npm install
npm run build
```

#### Windows (WSL)

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

- [Connect Models](../connect-models) — Configure LLM providers
- [First Run](../first-run) — Start your first expert team
