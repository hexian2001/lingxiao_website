---
title: 安装与启动
description: 多种方式安装凌霄剑域
---

# 安装与启动

## 前置要求

| 依赖 | 要求 |
| --- | --- |
| 操作系统 | Linux / macOS / Windows / WSL |
| Node.js | >= 24.0.0（源码安装需要） |
| Git | 推荐 |

## 方式一：便携包（推荐）

从 [GitHub Releases](https://github.com/hexian2001/lingxiao-coding/releases) 下载对应平台的便携包，解压即可使用。

| 平台 | 文件 |
| --- | --- |
| Linux x64 | `lingxiao-v1.0.2-linux-x64.tar.gz` |
| Linux arm64 | `lingxiao-v1.0.2-linux-arm64.tar.gz` |
| macOS arm64 | `lingxiao-v1.0.2-darwin-arm64.tar.gz` |
| Windows x64 | `lingxiao-v1.0.2-win-x64.zip` |

**Linux / macOS：**

```bash
tar xzf lingxiao-v1.0.2-linux-x64.tar.gz
cd lingxiao
./lingxiao
```

**Windows：**

解压 zip 文件后，双击 `lingxiao.exe` 或在 PowerShell 中运行：

```powershell
.\lingxiao.exe
```

## 方式二：Windows 桌面版

从 [Releases](https://github.com/hexian2001/lingxiao-coding/releases) 下载 Windows 安装包：

- **NSIS 安装包**（`LingXiao-Setup-1.0.2.exe`）：推荐，支持自动更新
- **MSI 安装包**（`LingXiao.1.0.2.msi`）：适合企业部署

安装后从开始菜单启动「凌霄」，后续版本更新会自动检测并增量下载。

## 方式三：源码安装

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

安装完成后直接运行：

```bash
lingxiao
```

首次运行会引导配置模型和 API 密钥。配置文件位于 `~/.lingxiao/settings.json`。

> `npm link` 会将 `lingxiao` 命令注册到全局 PATH，之后可在任意目录使用。

## 验证安装

```bash
lingxiao --version
```

## 升级

### 便携包 / 源码安装

```bash
lingxiao upgrade
```

`lingxiao upgrade` 会自动检测安装类型（源码或便携包），定位安装路径，下载最新版本并完成更新。

### Windows 桌面版

桌面版启动后自动检测更新，增量下载并提示安装。也可手动检查更新。

### 手动升级（源码 — 三平台通用）

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

## 从源码开发

```bash
git clone https://github.com/hexian2001/lingxiao-coding.git
cd lingxiao-coding
npm install
npm run build
npm run cli
```

Web 前端开发：

```bash
cd web
npm install
npm run dev
npm run build
```

Vite 开发代理示例：

```bash
LINGXIAO_WEB_PORT=8787 npm run cli
cd web
LINGXIAO_WEB_PROXY_TARGET=http://127.0.0.1:8787 npm run dev
```

## 测试

```bash
npx tsc -p tsconfig.cli.json --noEmit
npx tsc -p web/tsconfig.json --noEmit
npm run test:architecture
npm run build
npm test
```

## 许可协议

本项目采用 **AGPL v3 + 商业双授权** 模式。详见 [LICENSE](https://github.com/hexian2001/lingxiao-coding/blob/main/LICENSE)。

## 下一步

- [连接模型](../connect-models) — 配置 LLM 提供商
- [第一次运行](../first-run) — 启动你的第一个专家团
